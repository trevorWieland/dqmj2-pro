import base64
import hashlib
import json
import random
import re
import struct
import match_runtime as C
import unicorn as un
import unicorn.arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261106_auth_resume_next_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK


STOP,SP,INPUT,OUTPUT=0x04000000,0x027e0000,0x03001000,0x03002000
HELPERS=[(0x020961c8,'thumb'),(0x020963b4,'thumb'),(0x0209636c,'thumb'),(0x02008e0c,'arm'),(0x0201b248,'arm'),(0x02026144,'arm')]


def classifier(value):
    if 65<=value<=90:return value-65
    if 97<=value<=122:return value-97+26
    if 48<=value<=57:return value-48+52
    return {43:62,47:63,61:0}.get(value,-1)


def decode(source,capacity):
    count=len(source);result=bytearray([0xcc])*128;answer=count*3//4
    if capacity<answer:return bytes(result),0xffffffff
    limit=count-count%4
    for at in range(0,limit,4):
        word=0
        for j in range(4):word|=(classifier(source[at+j])&0xffffffff)<<((3-j)*6)
        word&=0xffffffff
        for k in range(3):result[at//4*3+k]=(word>>(16-k*8))&255
    word=0
    for j in range(count%4):word|=(classifier(source[limit+j])&0xffffffff)<<((3-j)*6)
    word&=0xffffffff
    for k in range(count%4):result[limit*3//4+k]=(word>>(16-k*8))&255
    return bytes(result),answer


def values(image):
    pointers=struct.unpack_from('<4I',image,0xdea70)
    masks=[image[p-0x02000000:p-0x02000000+24]for p in pointers]
    return masks,image[0xdc4a3:0xdc4a3+24],image[0xdc4bc:0xdc4bc+13],image[0xdc4cc:0xdc4cc+16]


def vector(address,seed,image):
    rng=random.Random(0x61630000+seed);source=bytes(rng.randrange(256)for unused in range(96));output=bytearray([0xcc])*128;args=[INPUT,OUTPUT,0,0];answer=None;partial=False
    masks,permutation,order,nibbles=values(image)
    if address==0x0209636c:args[0]=seed;answer=classifier(seed)&0xffffffff
    elif address==0x020963b4:
        size=[0,1,2,3,4,5,6,7,8,9,10,11,32,37][seed%14];alphabet=b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=?@';source=bytes(alphabet[rng.randrange(len(alphabet))]for unused in range(size))+bytes(96-size);capacity=size*3//4-(seed//14%2);capacity=max(capacity,0);args=[INPUT,OUTPUT,size,capacity];expected,answer=decode(source[:size],capacity);output[:]=expected
    elif address==0x02096288:
        key=bytearray(source[i]^source[13+i%7]for i in range(13))
        for i in range(7):key[3+i]^=source[13+i]
        key=bytearray(value^masks[1][i]for i,value in enumerate(key));temp=bytes(key)
        for i,target in enumerate(order):key[target]=temp[i]
        key=bytearray(value^masks[3][i]for i,value in enumerate(key));key=bytearray((nibbles[v>>4]<<4)|nibbles[v&15]for v in key)
        for i in range(3):key[i]^=key[i+6];key[3+i]^=key[9+i];key[6+i]^=key[3+i];key[9+i]^=key[i];key[12]^=key[i]
        output[:13]=key
    elif address==0x02096174:
        expected=(b'NDWCSHAP'if seed%2 else b'NDWCSHAX')+bytes(48+(seed+i)%10 for i in range(10))+bytes([seed])*6;before=bytes(v^masks[0][i]for i,v in enumerate(expected));raw=bytes(before[permutation[i]]^masks[2][i]for i in range(24));source=base64.b64encode(raw)+bytes(64)
        if seed%2:output[:10]=expected[8:18]
    elif address==0x02096258:partial=True
    else:raise ValueError('Unknown exact source fixture identity')
    return dict(source=source,expectedOutput=bytes(output),args=args,answer=answer,partial=partial)


def helper_specs(image,inventory):
    result=[]
    for address,mode in HELPERS:
        record=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\('+mode+r',size=(0x[0-9a-f]+)\) addr:0x%08x'%address,line)),None)
        if record is None:raise ValueError('Actual pure helper original entry/mode missing')
        size=int(re.search(r'size=(0x[0-9a-f]+)',record).group(1),0)
        result.append(dict(address=address,mode=mode,bytes=size,canonicalInventoryRecord=record,targetSha256=hashlib.sha256(image[address-0x02000000:address-0x02000000+size]).hexdigest(),sourceCredit=0))
    return result


def run(image,row,body,seed,specs):
    address=int(row['address'],0);case=vector(address,seed,image);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x02000000,0x400000);cpu.mem_write(0x02000000,image);cpu.mem_write(address,body);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);cpu.mem_map(INPUT,0x4000);cpu.mem_write(INPUT,case['source']);cpu.mem_write(OUTPUT,bytes([0xcc])*128);cpu.mem_map(STOP,0x1000)
    initial=[0x6a000000+i*0x101+seed for i in range(15)];initial[:4]=case['args'];initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for register,value in zip(C.REGISTERS,initial):cpu.reg_write(register,value)
    observed=None;pcs=[];active=[];calls=0;returns=0
    def code(machine,at,size,user):
        nonlocal observed,calls,returns
        regs=[machine.reg_read(r)for r in C.REGISTERS];thumb=bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)
        while active and at==active[-1]:active.pop();returns+=1
        if at==STOP:
            if active or regs[4:12]!=initial[4:12]or regs[13]!=SP:raise ValueError('Exact caller/helper ABI return failed')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if address==0x02096258 and at==0x0200cad0:
            if thumb or regs[0]!=regs[13]+20 or regs[4]!=OUTPUT or regs[5]!=INPUT:raise ValueError('Actual digest context/initial provider ABI differs')
            observed=dict(kind='provider-stop',address=hex(at),contextOffset=20,providerInstructionsExecuted=0);machine.emu_stop();return
        if address<=at<address+len(body):
            if not thumb:raise ValueError('Caller left exact Thumb mode')
        else:
            helper=next((h for h in specs if h['address']<=at<h['address']+h['bytes']),None)
            if helper is None or thumb!=(helper['mode']=='thumb'):raise ValueError(('Execution escaped actual qualified pure helpers',hex(at)))
            if at==helper['address']:calls+=1;active.append(regs[14]&~1)
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if OUTPUT<=at and at+size<=OUTPUT+128:return
        raise ValueError(('Unexpected caller/helper write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=200000)
    if observed is None:raise ValueError('Caller did not reach genuine bounded return/provider')
    guards=bytes(cpu.mem_read(INPUT,len(case['source'])))==case['source']and bytes(cpu.mem_read(OUTPUT,128))==case['expectedOutput']
    expected='provider-stop'if case['partial']else'return';passed=observed['kind']==expected and guards and calls==returns
    if case['answer']is not None:passed=passed and observed['value']==case['answer']
    if not passed:raise ValueError(('Actual caller disagrees with independent algorithm/RAM model',hex(address),seed,observed,case['answer'],guards,calls,returns))
    return dict(address=row['address'],seed=seed,observed=observed,topReturned=expected=='return',partialProviderStopped=case['partial'],modelPassed=passed,actualOriginalHelperInvocations=calls,actualOriginalHelperReturns=returns,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();specs=helper_specs(image,inventory);records=[]
    for row in rows:
        address=int(row['address'],0);native=image[address-0x02000000:address-0x02000000+row['bytes']];compiled=(ROOT/row['realLink']['binary']).read_bytes()if'bin' in row['realLink']else(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        count=256 if address==0x0209636c else 28 if address==0x020963b4 else 4 if address==0x02096258 else 8
        for seed in range(count):
            left=run(image,row,native,seed,specs);right=run(image,row,compiled,seed,specs)
            if left!=right:raise ValueError('Complete original and freshly linked C traces differ')
            records.append(left)
    trace=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest();result=dict(status='passed',traceSha256=trace,records=records,actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*sum(r['topReturned']for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped']for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),limits='Classifier exhausts byte domain; Base64 bounded partial/full/invalid/capacity cases; USB8 and postal8 disjoint RAM vectors. Original qualified pure copy/compare/remainder/decoder/classifier bodies execute with0source/extent credit. MD5 wrapper stops BEFORE first actual digest provider instruction;0MD5/provider/device/network/game/Windows executions or imported storage credit.',wholeCNegativeControlsRejected=0)
    write_json(LANE/'caller-fixtures.json',result);return result
