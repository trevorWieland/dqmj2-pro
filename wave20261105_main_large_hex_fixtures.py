import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_large_hex_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-large/hex'
WORK=ROOT/'work/w5mg/hex/fixtures'
ADDRESS,BUFFER,STOP,SP=0x201fd88,0x2170000,0x27e0000,0x2701000

def run(image,body,vector,seed):
    lo,hi,precision,nzcv=vector;cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x200000);cpu.mem_write(0x2000000,image);cpu.mem_write(ADDRESS,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x2000);memory=bytes((i*31+seed*17)&255 for i in range(160));cpu.mem_write(BUFFER,memory);arguments=struct.pack('<III',0x0047a504,0x12345678,precision);cpu.mem_write(SP,arguments);initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=[lo,hi,BUFFER,0x01020100];initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,nzcv|0x10)
    for reg,word in zip(C.REGISTERS,initial):cpu.reg_write(reg,word)
    pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if not ADDRESS<=at<ADDRESS+876:raise ValueError('Precision-limit path executed another body/literal/callback')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x1000<=at and at+size<=SP):raise ValueError('Precision-limit caller wrote outside own stack')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(ADDRESS,STOP+4,count=1000);regs=[cpu.reg_read(r) for r in C.REGISTERS];unchanged=bytes(cpu.mem_read(BUFFER,len(memory)))==memory and bytes(cpu.mem_read(SP,len(arguments)))==arguments;abi=regs[4:12]==initial[4:12] and regs[13]==SP
    if not returned or not unchanged or not abi:raise ValueError('Precision-limit actual return/ABI/caller memory differs')
    return dict(address=hex(ADDRESS),vector=list(vector),seed=seed,topReturned=True,abiPreserved=True,callerMemoryUnchanged=True,returnValue=regs[0],pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),nativeCalleeExecutions=0,sourceCreditForOriginalData=0)

def execute(rows):
    row=rows[0];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[ADDRESS-0x2000000:ADDRESS-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();cases=[(a,b,p,n) for a,b in [(0,0),(0,0x3ff00000),(0,0xbff00000),(1,0x7ff80000),(0xffffffff,0x7fefffff)] for p in [510,511,2147483647] for n in [0,0x10000000,0x80000000,0xf0000000]];records=[]
    for seed,vector in enumerate(cases):
        original=run(image,native,vector,seed);rebuilt=run(image,linked,vector,seed)
        if original!=rebuilt or original['returnValue']!=0:raise ValueError('Independent maximum-precision null-return model differs')
        records.append(original)
    source=ROOT/row['source'];folder=WORK/'wrong-return';folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=source.read_text();changed=text.replace('if (format.precision > 509) {\n        return 0;','if (format.precision > 509) {\n        return buff;',1)
    if changed==text:raise ValueError('Wrong whole C return did not mutate source')
    wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'link',negative=True);controls=[]
    for seed,vector in enumerate(cases[:12]):
        actual=run(image,body,vector,seed)
        if actual['returnValue']!=BUFFER or not actual['topReturned']:raise ValueError('Wrong C control was not an actual returning nonnull mismatch')
        controls.append(actual)
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();limits=['Only precision>509 early-null-return paths execute60original/source vectors120topreturns across several incoming double bit patterns and NZCV states. No floating payload arithmetic, conversion helper, decimal/copy/strlen/mbstowcs body, wide data reads, device or game scene execution is claimed.','External native wide literals are byte/typed-view qualified separately; original storage/extent/authorship credit0.','Wrong full C preserves actual returning ABI/memory but returns nonnull buffer instead of0;12 actually returning controls reject it after a genuine MW link.'];report=dict(status='passed',records=records,originalAndSourceReturningVectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=0,nativeDevicesOrScenesExecuted=0,traceSha256=trace,wrongC=dict(sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(controls),records=controls),limits=limits);write_json(LANE/'limit-fixtures.json',report);return report
