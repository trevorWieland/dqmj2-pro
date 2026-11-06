import functools
import random
import struct
from project import ROOT

ENTRY,ARENA,CACHE,DESCRIPTORS,TABLE=0x02212D54,0x02243E3C,0x02231F64,0x0224373C,0x0222BAF4
SPECS={ENTRY:200}
NATIVE={0x021DF950:268,0x021DF544:52,0x021DF578:48,0x02212F80:336,0x02212804:68}

def word(v):
    return v&0xFFFFFFFF

def signed16(v):
    v=v&65535
    return v-65536 if v&32768 else v

@functools.lru_cache(maxsize=1)
def table_data():
    data=(ROOT/'extract/arm9_overlays/ov000.bin').read_bytes()
    return data[TABLE-0x021D7240:TABLE-0x021D7240+36]

def recipes():
    return[dict(entry=ENTRY,seed=305000+kind*34+slot*2+behavior,kind=kind,slot=slot,behavior=behavior)for kind in range(18)for slot in range(17)for behavior in range(2)]

def construct(recipe):
    rng=random.Random(recipe['seed'])
    state={ARENA:bytearray(rng.randbytes(16*268)),CACHE:bytearray(rng.randbytes(16*48)),DESCRIPTORS:bytearray(rng.randbytes(8*224))}
    def snapshot():
        return[(a,bytes(b))for a,b in state.items()]
    def store(base,offset,value,n=4):
        state[base][offset:offset+n]=word(value).to_bytes(4,'little')[:n]
    values=[recipe['kind'],rng.getrandbits(32),rng.getrandbits(32),rng.getrandbits(32),rng.getrandbits(32),rng.getrandbits(32),rng.getrandbits(32),[0,1,0x7FFF,0x8000,0xFFFF,0x12345678][recipe['seed']%6]]
    for slot in range(16):
        store(ARENA,slot*268+261,[1,2,127,128,255][(slot+recipe['seed'])%5],1)
        if recipe['slot']<16 and slot in[recipe['slot'],recipe['slot']+2]:
            store(ARENA,slot*268+261,0,1)
        store(CACHE,slot*48,0x10000+slot)
    token=signed16(struct.unpack_from('<H',table_data(),recipe['kind']*2)[0])
    cache_slot=recipe['seed']%16
    if not recipe['behavior']:
        store(CACHE,cache_slot*48,token)
        if cache_slot<15:
            store(CACHE,(cache_slot+1)*48,token)
    descriptor_slot=(recipe['seed']//2)%8
    for i in range(8):
        store(DESCRIPTORS,i*224+220,0 if i<descriptor_slot else[1,2,255][i%3],1)
        store(DESCRIPTORS,i*224+221,recipe['kind']if i in[descriptor_slot,min(descriptor_slot+1,7)]else(recipe['kind']+i+1)%256,1)
    initial=snapshot()
    native,services=[],[]
    def visit(address,args,result):
        native.append(dict(address=address,arguments=[word(v)for v in args],result=word(result),before=snapshot()))
    slot=next((i for i in range(16)if state[ARENA][i*268+261]==0),-1)
    if slot>=0:
        offset=slot*268
        for relative,value,n in[(112,values[1],4),(116,values[2],4),(120,values[3],4),(136,0,4),(140,values[4],4),(144,0,4),(124,4096,4),(128,4096,4),(132,4096,4),(262,values[0],1),(263,values[5],1),(256,values[7],2),(264,values[6],1),(261,1,1)]:
            store(ARENA,offset+relative,value,n)
        keys=[struct.unpack_from('<I',state[CACHE],i*48)[0]for i in range(16)]
        found=word(token)in keys
        visit(0x021DF950,[token],int(found))
        visit(0x021DF544,[token],int(found))
        if not found:
            if 0 in keys:
                raise ValueError('Allocator305 unsupported native cache-loading path')
            visit(0x021DF578,[],0xFFFFFFFF)
        pointer=ARENA+offset
        descriptor=DESCRIPTORS+descriptor_slot*224
        visit(0x02212F80,[pointer],0)
        visit(0x02212804,[recipe['kind']],descriptor)
        services.append(dict(address=0x0204106C,arguments=[pointer,descriptor+4,0],result=0,before=snapshot(),effects=[],expectedCarrierR0=None,stackBefore=[(0,struct.pack('<III',4096,4096,4096)),(12,struct.pack('<III',0,values[4],0)),(24,struct.pack('<III',*values[1:4]))]))
    return initial,snapshot(),services,native,word(slot),values
