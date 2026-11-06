import hashlib
import json
import re
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT

KEY,BUFFER,SP,STOP=0x2170000,0x2172000,0x2701000,0x27e0000


def cipher(key,data):
    state=list(range(256));position=0;accumulator=0
    for index in range(256):
        accumulator=(key[position]+state[index]+accumulator)&255;position=(position+1)%len(key)
        state[index],state[accumulator]=state[accumulator],state[index]
    x=y=0;out=bytearray()
    for value in data:
        x=(x+value+1)&255;y=(state[x]+y)&255;state[x],state[y]=state[y],state[x]
        out.append(value^state[(state[x]+state[y])&255])
    return bytes(out)


def helpers(image):
    lines=(ROOT/'config/arm9/symbols.txt').read_text().splitlines();out=[]
    for address in [0x2026144,0x2026350,0x20b7678]:
        record=next(line for line in lines if line.endswith(' addr:0x%08x'%address));match=re.fullmatch(r'\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:0x[0-9a-f]+',record)
        assert match
        size=int(match[2],0);out.append(dict(address=address,mode=match[1],bytes=size,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[address-0x2000000:address-0x2000000+size]).hexdigest(),sourceCredit=0))
    return out


def vectors():
    keys=[b'\0',b'\xff',b'secret',bytes(range(64))];data=[b'',b'\0',b'\xff',b'challenge',bytes(range(64)),bytes(range(256))]
    return [dict(key=key.hex(),data=value.hex(),length=len(value)) for key in keys for value in data]+[dict(key=key.hex(),data=b'unused'.hex(),length=-1) for key in keys]


def run(image,row,body,vector,seed):
    key=bytes.fromhex(vector['key']);data=bytes.fromhex(vector['data']);length=vector['length'];expected=cipher(key,data[:max(0,length)]);before=data+bytes([0xcd])*(1024-len(data));after=expected+before[len(expected):]
    address=int(row['address'],0);catalog=helpers(image);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946)
    cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_write(KEY,key);cpu.mem_write(BUFFER,before);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_map(STOP,0x1000)
    initial=[(0x55770000+seed*0x101+index*0x111)&0xffffffff for index in range(15)];initial[:4]=[KEY,len(key),BUFFER,length&0xffffffff];initial[-2:]=[SP,STOP|1]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0x30,0x10000030,0x80000030,0xf0000030][seed%4])
    for register,value in zip(C.REGISTERS,initial):cpu.reg_write(register,value)
    returned=[];pcs=[];writes=[];entries={helper['address']:0 for helper in catalog}
    def instruction(machine,at,size,user):
        if at==STOP:returned.append(at);machine.emu_stop();return
        mode='thumb' if address<=at<address+len(body) else next((helper['mode'] for helper in catalog if helper['address']<=at<helper['address']+helper['bytes']),None)
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError(('Crypto caller/helper graph or entry mode escaped',hex(at)))
        if at in entries:entries[at]+=1
        pcs.append(at)
    def store(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP or BUFFER<=at and at+size<=BUFFER+max(0,length)):raise ValueError(('Crypto write escaped stack/output extent',hex(at),size))
        writes.append((at,size,value))
    cpu.hook_add(un.UC_HOOK_CODE,instruction);cpu.hook_add(un.UC_HOOK_MEM_WRITE,store);cpu.emu_start(address|1,STOP+4,count=500000)
    registers=[cpu.reg_read(register) for register in C.REGISTERS];actual=bytes(cpu.mem_read(BUFFER,1024));actual_key=bytes(cpu.mem_read(KEY,len(key)))
    if returned!=[STOP] or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Crypto top return/callee-saved ABI differs')
    trace=(registers,cpu.reg_read(ar.UC_ARM_REG_CPSR),pcs,writes,actual.hex(),actual_key.hex())
    return dict(topReturned=True,modelPassed=actual==after and actual_key==key,traceSha256=hashlib.sha256(json.dumps(trace).encode()).hexdigest(),bufferSha256=hashlib.sha256(actual).hexdigest(),actualOriginalHelperEntries={hex(at):count for at,count in entries.items()},actualOriginalHelperInvocations=sum(entries.values()),calleeSavedStackAndModesChecked=True)


def prove(row,native,source):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[]
    for seed,vector in enumerate(vectors()):
        original=run(image,row,native,vector,seed);rebuilt=run(image,row,source,vector,seed)
        if original!=rebuilt or not original['modelPassed']:raise ValueError(('Independent GameSpy byte-permutation/cipher model differs',vector,original,rebuilt))
        records.append(dict(seed=seed,vector=vector,traceSha256=original['traceSha256'],helperInvocations=original['actualOriginalHelperInvocations']))
    return dict(address=row['address'],cases=len(records),actualNativeAndSourceCallerReturns=2*len(records),records=records,
        actualOriginalHelperInvocations=2*sum(item['helperInvocations'] for item in records),actualOriginalHelperBodies=helpers(image),
        noSuppliedCalleeBodiesOrHooks=True,allGprsCpsrCalleeSavedStackAndOrderedWritesCompared=True,helperSourceCredit=0,hardwareOrGameExecutionCredit=0,
        limits=['The full original signed/unsigned arithmetic helpers and byte-swap helper execute within their measured ARM/Thumb extents. They earn zero extra source credit.','Independent permutation arithmetic covers keys1..64 bytes and output lengths -1,0,1,9,64,256, including all byte values. Empty keys, aliasing key/output, invalid pointers and signed16 counter wrap are outside the proved domain.'])
