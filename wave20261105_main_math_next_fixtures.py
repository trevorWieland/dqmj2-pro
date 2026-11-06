import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_math_next_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/main-math-next'
WORK=ROOT/'work/w5mn/fixtures'
DEC,STATE,STOP,SP=0x2174000,0x20ec9b8,0x27e0000,0x2701000


def run(image,row,body,vector,seed):
    address=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x200000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x2000)
    initial=[(0x22110000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP];nzcv=vector[-1]
    if address==0x2026ac0:
        region=STATE;before=bytearray((i*37+seed*23)&255 for i in range(24));struct.pack_into('<I',before,4,vector[0]);struct.pack_into('<I',before,8,vector[0]^0x13579bdf);struct.pack_into('<I',before,20,vector[1])
    else:
        region=DEC;before=bytearray((i*37+seed*23)&255 for i in range(38));initial[0]=DEC
        if address==0x2023790:before[0]=vector[0];before[4]=vector[1];before[5]=ord('N')
        else:initial[1:3]=[0,0]
    cpu.mem_write(region,bytes(before));cpu.reg_write(ar.UC_ARM_REG_CPSR,nzcv|0x10)
    for register,word in zip(C.REGISTERS,initial):cpu.reg_write(register,word)
    pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if not address<=at<address+row['bytes']:raise ValueError('Bounded fixture entered an original callee/callback or another body')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x1000<=at and at+size<=SP:return
        if address==0x2022a94 and region<=at and at+size<=region+len(before):return
        raise ValueError('Bounded fixture wrote outside declared caller memory/stack')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address,STOP+4,count=2000);registers=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Actual caller return/callee-saved ABI differs')
    after=bytes(cpu.mem_read(region,len(before)));expected=bytearray(before)
    if address==0x2022a94:expected[0]=0;expected[2:4]=b'\xff\xff';expected[4]=0;model=after==expected
    elif address==0x2023790:model=after==before and registers[0]==0 and registers[1]==(0x7ff80000|(0x80000000 if vector[0] else 0))
    else:model=after==before and registers[0]==vector[0]
    return dict(address=hex(address),vector=list(vector),seed=seed,topReturned=True,calleeSavedAbiPreserved=True,modelPassed=model,before=bytes(before).hex(),after=after.hex(),returnWords=registers[:2],pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),nativeCalleeExecutions=0)


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negatives=[]
    for row in rows:
        address=int(row['address'],0);native=image[address-0x2000000:address-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        if address==0x2023790:cases=[(sign,length,nzcv) for sign in [0,1,127,255] for length in [1,32,255] for nzcv in [0,0x10000000,0x80000000,0xf0000000]];old,new='0x0008000000000000ULL','0x0004000000000000ULL'
        elif address==0x2022a94:cases=[(i,nzcv) for i in range(8) for nzcv in [0,0x10000000,0x80000000,0xf0000000]];old,new='sig.length - 1','sig.length - 2'
        elif address==0x2026ac0:cases=[(value,initialized,nzcv) for value in [0,1,0xffffffff,0x80000000] for initialized in [1,0xffffffff,0x100] for nzcv in [0,0x10000000,0x80000000,0xf0000000]];old,new='return native_data_020ec9b8.value;','return native_data_020ec9b8.pad8[0];'
        else:raise ValueError('Unowned fixture target')
        for seed,vector in enumerate(cases):
            original=run(image,row,native,vector,seed);rebuilt=run(image,row,linked,vector,seed)
            if original!=rebuilt or not original['modelPassed']:raise ValueError('Independent actual caller state/result model differs')
            records.append(original)
        source=ROOT/row['source'];folder=WORK/format(address,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        text=source.read_text();changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole wrong C did not mutate selected source')
        wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Wrong whole C does not preserve complete function extent')
        controls=[]
        for seed,vector in enumerate(cases[:16]):
            actual=run(image,row,body,vector,seed)
            if actual['modelPassed'] or not actual['topReturned']:raise ValueError('Wrong whole C did not actually return a model violation')
            controls.append(actual)
        negatives.append(dict(address=row['address'],sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(controls),records=controls))
    result=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=0,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),wrongC=negatives,wholeCNegativeControlsRejected=len(negatives),limits=['Only zero-input unsigned64 decimal, signed quiet-NaN decimal return and already-initialized runtime-state getter paths execute. All actual caller return words, declared memory effects and callee-saved ABI are checked against independent models.','No finite decimal payload, unsigned64 helper invoked by a caller, uninitialized getter/callee, external constant-array read, hardware or scene execution is claimed. Separate original unsigned64 standalone entry controls have zero callee source credit.'])
    write_json(LANE/'caller-fixtures.json',result);return result
