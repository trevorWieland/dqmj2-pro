import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_large_format_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-large/format'
WORK=ROOT/'work/w5mg/format/fixtures'
ADDRESS,BUFFER,CONTEXT,FORMAT,ARGS,STOP,SP=0x2020890,0x2170000,0x2172000,0x2174000,0x2176000,0x27e0000,0x2701000

def run(image,body,vector,seed):
    capacity,nzcv=vector;cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x200000);cpu.mem_write(0x2000000,image);cpu.mem_write(ADDRESS,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x2000);regions=[(BUFFER,bytes(((i*31+seed*17)&127)|128 for i in range(160))),(CONTEXT,struct.pack('<III',BUFFER,capacity,0)),(FORMAT,bytes(2)),(ARGS,bytes([0x79]*64))]
    for at,data in regions:cpu.mem_write(at,data)
    initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=[0x2021180,CONTEXT,FORMAT,ARGS];initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,nzcv|0x10)
    for reg,word in zip(C.REGISTERS,initial):cpu.reg_write(reg,word)
    pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if not ADDRESS<=at<ADDRESS+len(body):raise ValueError('Empty-format formatter executed import/callback')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not SP-0x1000<=at or at+size>SP:raise ValueError('Empty-format formatter wrote outside own stack')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(ADDRESS,STOP+4,count=2000);regs=[cpu.reg_read(r) for r in C.REGISTERS];abi=regs[4:12]==initial[4:12] and regs[13]==SP
    if not returned or not abi or any(bytes(cpu.mem_read(at,len(data)))!=data for at,data in regions):raise ValueError('Actual empty formatter return/ABI/read-only caller memory differs')
    return dict(address=hex(ADDRESS),vector=list(vector),seed=seed,topReturned=True,returnValue=regs[0],abiPreserved=True,callerRegionsUnchanged=True,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),actualNativeCalleeBodiesExecuted=0)

def execute(rows):
    row=rows[0];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[ADDRESS-0x2000000:ADDRESS-0x2000000+2288];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();cases=[(n,f) for n in [1,2,8,79] for f in [0,0x10000000,0x80000000,0xf0000000]];records=[]
    for seed,vector in enumerate(cases):
        original=run(image,native,vector,seed);rebuilt=run(image,linked,vector,seed)
        if original!=rebuilt or original['returnValue']!=0:raise ValueError('Independent empty-format zero-written model differs')
        records.append(original)
    source=ROOT/row['source'];folder=WORK/'wrong-count';folder.mkdir(parents=True,exist_ok=True)
    for p in row['sourceDependencies']:shutil.copyfile(ROOT/p['path'],folder/(ROOT/p['path']).name)
    text=source.read_text();changed=text.replace('chars_written = 0;','chars_written = 1;',1)
    if changed==text:raise ValueError('Wrong full C written-count did not mutate source')
    wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'link',negative=True);negative=[]
    for seed,vector in enumerate(cases):
        actual=run(image,body,vector,seed)
        if actual['returnValue']!=1 or not actual['topReturned']:raise ValueError('Wrong C did not actually return wrong written-count')
        negative.append(actual)
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();limits=['Only empty UTF16 format paths execute16original/source vectors32actualtopreturns with zero written-count and unchanged output/context/varargs regions. No callback or native import executes.','Nonempty format parsing, numeric/string conversion, caller-supplied varargs, width/padding/error branches, hardware and game scenes remain unexecuted.','Native wide/narrow empty constants and all callees/storage/extent/authorship receive0sourcecredit; shared whole module/ROM acceptance is coordinator-owned.'];report=dict(status='passed',records=records,originalAndSourceReturningVectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=0,nativeDevicesOrScenesExecuted=0,traceSha256=trace,wrongC=dict(sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(negative),records=negative),limits=limits);write_json(LANE/'empty-format-fixtures.json',report);return report
