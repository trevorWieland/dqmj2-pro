import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_large_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-large'
WORK=ROOT/'work/w5mg/fixtures'
DATA,SOURCE,STOP,SP=0x2170000,0x2172000,0x27e0000,0x2701000

def model(address,vector,seed):
    if address==0x2020120:
        digits,n=vector;length=len(digits);exponent=[-3,0,32767][seed%3];data=bytearray([0xa5]*38);data[0]=seed%256;struct.pack_into('<h',data,2,exponent);data[4]=length;data[5:5+length]=digits.encode();expected=bytearray(data)
        if n<0:struct.pack_into('<h',expected,2,0);expected[4]=1;expected[5]=48
        elif n<length:
            discarded=digits[n:];tail=int(discarded);half=5*10**(len(discarded)-1);prior=(int(digits[n-1]) if n else length)&1;carry=tail>half or (tail==half and prior!=0);prefix=int(digits[:n] or '0')+int(carry)
            if prefix==0:struct.pack_into('<h',expected,2,0);expected[4]=1;expected[5]=48
            elif len(str(prefix))>n:struct.pack_into('<H',expected,2,(exponent+1)&0xffff);expected[4]=1;expected[5]=49
            else:
                text=str(prefix).rjust(n,'0').rstrip('0');expected[4]=len(text);expected[5+len(text)-1]=ord(text[-1])
        return dict(args=[DATA,n&0xffffffff],regions=[(DATA,bytes(data),bytes(expected))],returnValue=None)
    if address==0x2021294:
        left,right=vector;payload=struct.pack('<'+str(len(left))+'H',*left);source=struct.pack('<'+str(len(right))+'H',*right,);initial=bytearray([0xa5]*160);initial[:len(payload)]=payload;expected=bytearray(initial);offset=(len(left)-1)*2;expected[offset:offset+len(source)]=source;return dict(args=[DATA,SOURCE],regions=[(DATA,bytes(initial),bytes(expected)),(SOURCE,source,source)],returnValue=DATA)
    values,char=vector;payload=struct.pack('<'+str(len(values))+'H',*values);first=next((i for i,c in enumerate(values) if c==char),None);return dict(args=[DATA,char],regions=[(DATA,payload,payload)],returnValue=0 if first is None else DATA+2*first)

def run(image,address,body,vector,seed):
    expected=model(address,vector,seed);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x200000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x1000)
    for at,initial,after in expected['regions']:cpu.mem_write(at-8,bytes([0x79]*8)+initial+bytes([0x71]*8))
    initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:len(expected['args'])]=expected['args'];initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,(0xf0000000 if seed%2 else 0)|0x10)
    for reg,word in zip(C.REGISTERS,initial):cpu.reg_write(reg,word)
    pcs=[];writes=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if not address<=at<address+len(body):raise ValueError('Pure original caller escaped to another body')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not any(base<=at and at+size<=base+len(before) for base,before,after in expected['regions']) and not SP-0x1000<=at<SP:raise ValueError('Pure source write escaped initialized test regions')
        if not SP-0x1000<=at<SP:writes.append([hex(at),size,value])
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address,STOP+4,count=3000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP or expected['returnValue'] is not None and regs[0]!=expected['returnValue']:raise ValueError('Pure actual return/ABI/model differs')
    snapshots=[]
    for at,before,after in expected['regions']:
        actual=bytes(cpu.mem_read(at-8,len(before)+16))
        if actual!=bytes([0x79]*8)+after+bytes([0x71]*8):raise ValueError('Independent pure memory model or guard differs')
        snapshots.append(hashlib.sha256(actual).hexdigest())
    return dict(address=hex(address),vector=vector,seed=seed,topReturned=True,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),snapshots=snapshots,writes=writes,nativeCalleeExecutions=0)

def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];vectors={};digits=['0','1','5','9','15','25','35','45','55','95','150','250','450','550','999','1000','14999','15000','15500','99950','9'*32]
    vectors[0x2020120]=[(s,n) for s in digits for n in sorted(set([-1,0,1,len(s)-1,len(s),len(s)+1]))];values=[[0],[65,0],[0x8000,0xffff,65,0],[65,66,65,0]];vectors[0x2021294]=[(a,b) for a in values for b in values];vectors[0x20212c4]=[(a,c) for a in values for c in [0,65,66,0x8000,0xffff,127]]
    for row in rows:
        address=int(row['address'],0)
        if address not in vectors:continue
        native=image[address-0x2000000:address-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,vector in enumerate(vectors[address]):
            original=run(image,address,native,vector,seed);rebuilt=run(image,address,linked,vector,seed)
            if original!=rebuilt:raise ValueError('Original/closed compiled pure trace differs')
            records.append(original)
    row=next(r for r in rows if r['address']=='0x2020120');source=ROOT/row['source'];folder=WORK/'wrong-round';folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    wrong=folder/source.name;text=source.read_text();changed=text.replace('if (c == 5)','if (c == 4)')
    if changed==text:raise ValueError('Wrong C decimal tie control did not change source')
    wrong.write_text(changed);bad,body=build(wrong,folder/'link',negative=True);negative=[]
    for seed,s in enumerate(['15','35','55','75','95','150','350','550','750','950']):
        try:run(image,0x2020120,body,(s,1),seed)
        except ValueError as error:negative.append(dict(digits=s,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong decimal tie C passed actual independent model')
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();limits=['Only decimal-record rounding, nonoverlapping uint16 concatenation and uint16 first-match search finite domains execute. Numeric parsing, formatting callbacks, actual native import bodies, floating-point payloads, devices and game scenes remain unexecuted.','Decimal new_length0 half-ties use prior length-byte parity, matching measured native behavior; positive lengths use last-kept-digit parity. Full untouched record tails/guards and ABI returns are checked.','External ASCII tables/errno/reader storage and helper/callee bodies receive0source/extent/authorship credit.'];report=dict(status='passed',records=records,originalAndSourceReturningVectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=0,nativeDevicesOrScenesExecuted=0,traceSha256=trace,wrongC=dict(sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(negative),cases=negative),limits=limits);write_json(LANE/'pure-fixtures.json',report);return report
