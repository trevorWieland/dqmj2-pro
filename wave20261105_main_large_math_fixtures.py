import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_large_math_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-large/math'
WORK=ROOT/'work/w5mg/math/fixtures'
ADDRESS,STOP,SP=0x20212f8,0x27e0000,0x2701000

def run(image,body,vector,seed):
    lo,hi,sign,nzcv=vector;cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x200000);cpu.mem_write(0x2000000,image);cpu.mem_write(ADDRESS,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x2000);cookie=struct.pack('<I',0x13579bdf);cpu.mem_write(0x20ec9b0,cookie);initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=[lo,hi,0,sign];initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,nzcv|0x10)
    for reg,word in zip(C.REGISTERS,initial):cpu.reg_write(reg,word)
    pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if not ADDRESS<=at<ADDRESS+len(body):raise ValueError('Zero-exponent path escaped to actual native helper')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x1000<=at and at+size<=SP):raise ValueError('Zero-exponent path wrote outside own stack')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(ADDRESS,STOP+4,count=1000);regs=[cpu.reg_read(r) for r in C.REGISTERS];abi=regs[4:12]==initial[4:12] and regs[13]==SP
    if not returned or not abi or bytes(cpu.mem_read(0x20ec9b0,4))!=cookie:raise ValueError('Zero-exponent actual return/ABI/errno preservation differs')
    return dict(address=hex(ADDRESS),vector=list(vector),seed=seed,topReturned=True,abiPreserved=True,errnoUnchanged=True,returnWords=regs[:2],pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),nativeCalleeExecutions=0,originalDataSourceCredit=0)

def execute(rows):
    row=rows[0];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[ADDRESS-0x2000000:ADDRESS-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();values=[(0,0),(0,0x80000000),(0,0x3ff00000),(0,0xbff00000),(0,0x40000000),(1,0),(0xffffffff,0x7fefffff),(0,0x7ff00000),(0,0xfff00000),(1,0x7ff00000),(0xffffffff,0x7fffffff),(0x12345678,0xfff80000)];cases=[(a,b,sign,n) for a,b in values for sign in [0,0x80000000] for n in [0,0x10000000,0x80000000,0xf0000000]];records=[]
    for seed,vector in enumerate(cases):
        original=run(image,native,vector,seed);rebuilt=run(image,linked,vector,seed)
        if original!=rebuilt or original['returnWords']!=[0,0x3ff00000]:raise ValueError('Independent double1.0 zero-exponent model differs')
        records.append(original)
    source=ROOT/row['source'];folder=WORK/'wrong-one';folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=source.read_text();changed=text.replace('if ((iy | ly) == 0)\n\t\treturn one;','if ((iy | ly) == 0)\n\t\treturn two;',1)
    if changed==text:raise ValueError('Wrong full C exponent-zero constant did not mutate source')
    wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'link',negative=True);negative=[]
    for seed,vector in enumerate(cases[:16]):
        actual=run(image,body,vector,seed)
        if actual['returnWords']!=[0,0x40000000]:raise ValueError('Wrong C control did not actually return double2.0')
        negative.append(actual)
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();limits=['Only plus/minus-zero-exponent guards execute96original/source vectors192actualtopreturns over finite/subnormal/infinite/NaN incomingx bit patterns and4NZCV patterns. No floating arithmetic/helper body, nonzero-exponent power algorithm, errno-domain branch, constant-array/NaN-object read, hardware or game scene execution is claimed.','Original errno-cookie preservation, caller ABI, exact double1.0 words and guard PC traces are checked independently. Wrong full C genuinely links and actually returns double2.0 in16 rejected models.','Native double arrays/float-NaN/errno storage, original source provenance and callee code/extent receive0sourcecredit; whole module/ROM acceptance is coordinator-owned.'];report=dict(status='passed',records=records,originalAndSourceReturningVectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=0,nativeDevicesOrScenesExecuted=0,traceSha256=trace,wrongC=dict(sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(negative),records=negative),limits=limits);write_json(LANE/'guard-fixtures.json',report);return report
