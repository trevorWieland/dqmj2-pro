import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_large_longlong_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-large/longlong'
WORK=ROOT/'work/w5mg/longlong/fixtures'
ADDRESS,BUFFER,END,STOP,SP=0x201fa88,0x2170000,0x2170080,0x27e0000,0x2701000

def run(image,body,vector,seed):
    conversion,alternate,nzcv=vector;cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x200000);cpu.mem_write(0x2000000,image);cpu.mem_write(ADDRESS,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x2000);before=bytes(((i*31+seed*17)&127)|128 for i in range(160));cpu.mem_write(BUFFER,before);stack=struct.pack('<III',4|(conversion<<16),0x12345678,0);cpu.mem_write(SP,stack);initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=[0,0,END,(seed%3)|((seed%3)<<8)|(alternate<<24)];initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,nzcv|0x10)
    for reg,word in zip(C.REGISTERS,initial):cpu.reg_write(reg,word)
    pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if not ADDRESS<=at<ADDRESS+len(body):raise ValueError('Zero-value/precision path executed an arithmetic helper')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not ((SP-0x1000<=at and at+size<=SP) or (BUFFER<=at and at+size<=BUFFER+160)):raise ValueError('Zero-value formatter wrote outside bounded own regions')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(ADDRESS,STOP+4,count=1000);regs=[cpu.reg_read(r) for r in C.REGISTERS];actual=bytes(cpu.mem_read(BUFFER,160));abi=regs[4:12]==initial[4:12] and regs[13]==SP
    if not returned or not abi or regs[0]!=END-2 or bytes(cpu.mem_read(SP,12))!=stack:raise ValueError('Zero-value actual formatter return/ABI/caller arguments differ')
    return dict(address=hex(ADDRESS),vector=list(vector),seed=seed,topReturned=True,returnPointer=regs[0],abiPreserved=True,firstTerminator=int.from_bytes(actual[126:128],'little'),otherBufferBytesPreserved=actual[:126]==before[:126] and actual[128:]==before[128:],pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),nativeCalleeBodyExecutions=0)

def execute(rows):
    row=rows[0];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[ADDRESS-0x2000000:ADDRESS-0x2000000+768];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();cases=[(ord(c),alternate,n) for c in ['d','i','u','x','X','o'] for alternate in [0,1] if c!='o' or not alternate for n in [0,0xf0000000]];records=[]
    for seed,vector in enumerate(cases):
        original=run(image,native,vector,seed);rebuilt=run(image,linked,vector,seed)
        if original!=rebuilt or original['firstTerminator']!=0 or not original['otherBufferBytesPreserved']:raise ValueError('Independent zero-number/precision empty-UTF16 model differs')
        records.append(original)
    source=ROOT/row['source'];folder=WORK/'wrong-terminator';folder.mkdir(parents=True,exist_ok=True)
    for p in row['sourceDependencies']:shutil.copyfile(ROOT/p['path'],folder/(ROOT/p['path']).name)
    text=source.read_text();changed=text.replace('*--p = 0;','*--p = 1;',1)
    if changed==text:raise ValueError('Wrong whole C terminator did not mutate source')
    wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'link',negative=True);negative=[]
    for seed,vector in enumerate(cases[:12]):
        actual=run(image,body,vector,seed)
        if actual['firstTerminator']!=1 or not actual['topReturned'] or not actual['otherBufferBytesPreserved']:raise ValueError('Wrong C did not actually return with wrong terminator')
        negative.append(actual)
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();limits=['Only zero64bit value/zero precision/nonalternate-o guard paths execute22original/source vectors44actualtopreturns, writing one UTF16 terminator and returning bufferEnd-2. Native arithmetic entries do not run as callees on these caller paths.','Separately16fresh direct original quotient/remainder ABI invocations revalidate the already-active zero-credit entry certificate through unchanged model.execute; no original table/report/verifier writes occur.','Nonzero number formatting, wider precision/padding/sign branches, helper invocations from this caller, hardware and scenes remain unexecuted. Existing unsigned64 helpers/entry evidence receive0source/extent credit.'];report=dict(status='passed',records=records,originalAndSourceReturningVectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=0,nativeDevicesOrScenesExecuted=0,traceSha256=trace,wrongC=dict(sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(negative),records=negative),limits=limits);write_json(LANE/'guard-fixtures.json',report);return report
