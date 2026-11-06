import random
import struct
from main_resource_binding_fixture_20261102 import inputs,model,half,word,DATA,STOP
from main_resource_binding_fixture_v2_20261102 import execute as run_machine

ENTRY=0x02031FA4
ALLOC_TEX,FREE_TEX,ALLOC_PLTT,FREE_PLTT=[STOP+n for n in[0x100,0x110,0x120,0x130]]
TEX_LOAD,PLTT_LOAD=0x0202EC6C,0x0202ED8C


class Services:
    def __init__(self,index):
        rng=random.Random(0xA110C+index);self.keys=[rng.getrandbits(32)|1 for _ in range(3)]
        self.fail=(index//72)%8;self.calls=[]
        self.globals={0x020DD8C0:ALLOC_TEX,0x020DD8C4:FREE_TEX,0x020DD8B8:ALLOC_PLTT,0x020DD8BC:FREE_PLTT}
        self.entries={ALLOC_TEX,FREE_TEX,ALLOC_PLTT,FREE_PLTT,TEX_LOAD,PLTT_LOAD}

    def invoke(self,address,words):
        count=3 if address in[ALLOC_TEX,ALLOC_PLTT]else 2 if address in[TEX_LOAD,PLTT_LOAD]else 1
        self.calls.append([address,words[:count]])
        if address in[ALLOC_TEX,ALLOC_PLTT]:
            slot=2 if address==ALLOC_PLTT else words[1]
            assert slot in[0,1,2]
            return 0 if self.fail&(1<<slot)else self.keys[slot]
        return (0xD00D0000+len(self.calls))&0xFFFFFFFF


def prepare(index):
    page,unused_entry,unused_args=inputs(index);rng=random.Random(0x5E7+index)
    signatures=[b'BMD0',b'BTX0',b'BMD0',b'FAIL',b'BCA0',b'BVA0',b'BMA0',b'BTP0',b'BTA0']
    signature=signatures[index%9];count=1 if index%9 in[1,2]else 2
    if index%16==15:signature=[b'CAA0',b'CTA0',b'CTP0',b'CTX0',b'CVA0',b'CMA0'][(index//16)%6]
    struct.pack_into('<4sHHIHHII',page,0,signature,0xFEFF,2,65536,16,count,0x1000 if signature==b'BTX0'else 0x2000,0x1000)
    sizes=[];mask=(index//9)%8;tex=0x1000
    for slot,offset in enumerate([12,28,48]):
        size=rng.choice([1,8,13])if mask&(1<<slot)else 0;sizes.append(size*8);struct.pack_into('<H',page,tex+offset,size)
    expected=bytearray(page);services=Services(index);calls=[];return_value=0
    if signature in[b'BMD0',b'BTX0']:
        present=not(signature==b'BMD0'and count==1);return_value=1
        if present:
            keys=[];success=[]
            for slot,size in enumerate(sizes):
                if size:
                    address=ALLOC_PLTT if slot==2 else ALLOC_TEX
                    flags=half(page,tex+32)&0x8000 if slot==2 else slot
                    calls.append([address,[size,flags,0]])
                    key=0 if services.fail&(1<<slot)else services.keys[slot]
                    keys.append(key);success.append(key!=0)
                else:keys.append(0);success.append(True)
            if not all(success):
                for slot in[2,1,0]:
                    if success[slot]:calls.append([FREE_PLTT if slot==2 else FREE_TEX,[keys[slot]]])
                return_value=0
            else:
                for slot,offset in enumerate([8,24,44]):
                    if slot==2 or keys[slot]:struct.pack_into('<I',expected,tex+offset,keys[slot])
                calls.extend([[TEX_LOAD,[DATA+tex,1]],[PLTT_LOAD,[DATA+tex,1]]])
                if signature==b'BMD0':expected,_=model(expected,0x0202F3DC,[DATA+0x2000,DATA+tex]);expected=bytearray(expected)
    elif signature in[b'BCA0',b'BVA0',b'BMA0',b'BTP0',b'BTA0']:return_value=1
    return page,bytes(expected),return_value,calls,services


def execute(image,bodies,index,bound=50000):
    page,expected,result,calls,services=prepare(index)
    output=run_machine(image,bodies,index,bound=bound,prepared=(page,ENTRY,[DATA],expected,result),services=services)
    output['modelPassed']=output['modelPassed']and calls==services.calls
    output.update(modeledBackendCalls=calls,actualBackendCalls=services.calls)
    return output
