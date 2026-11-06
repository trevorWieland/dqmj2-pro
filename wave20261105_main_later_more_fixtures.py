import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_later_more_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later/more'
WORK=ROOT/'work/w5ml/more/fixtures'
OBJECT,STOP,SP=0x2170000,0x27e0000,0x2701000

def run(image,address,body,vector,seed):
    flags,value,nzcv=vector;data=bytearray((i*19+seed*7)&255 for i in range(0x5c));struct.pack_into('<I',data,0x24,flags);after=bytearray(data);args=[OBJECT]
    if address==0x203b560:
        struct.pack_into('<IIII',after,8,0x203ba70,OBJECT,int.from_bytes(data[0x10:0x14],'little'),0x203babc);struct.pack_into('<I',after,0x18,OBJECT);struct.pack_into('<II',after,0x44,0,0);struct.pack_into('<I',after,0x24,flags&~3&0xffffffff)
    else:
        channels=(0,-1,-2147483648)[seed%3];struct.pack_into('<I',data,0x48,channels&0xffffffff);struct.pack_into('<I',after,0x48,channels&0xffffffff);struct.pack_into('<I',after,0x3c,value&0xffffffff);args.append(value&0xffffffff)
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x200000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x1000);cpu.mem_write(OBJECT,bytes(data));cpu.mem_write(0x20f5afc,struct.pack('<I',value&0xffffffff if address==0x203b560 else 1));initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:len(args)]=args;initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,nzcv|0x10)
    for reg,word in zip(C.REGISTERS,initial):cpu.reg_write(reg,word)
    pcs=[];writes=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if not address<=at<address+len(body)-(16 if address==0x203b560 else 4):raise ValueError('Administrative stream path reached import/callback or literal execution')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (OBJECT<=at and at+size<=OBJECT+len(data)) and not SP-0x1000<=at<SP:raise ValueError('Unexpected stream administrative memory write')
        if OBJECT<=at<OBJECT+len(data):writes.append([hex(at),size,value])
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address,STOP+4,count=1000);regs=[cpu.reg_read(r) for r in C.REGISTERS];actual=bytes(cpu.mem_read(OBJECT,len(data)))
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP or actual!=bytes(after):raise ValueError('Stream administrative model or actual returning ABI differs')
    if int.from_bytes(cpu.mem_read(0x20f5afc,4),'little')!=(value&0xffffffff if address==0x203b560 else 1):raise ValueError('Initialized global unexpectedly changed')
    return dict(address=hex(address),vector=list(vector),seed=seed,topReturned=True,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),memorySha256=hashlib.sha256(actual).hexdigest(),writes=writes,calleeExecutions=0,hardwareExecutions=0)

def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];vectors={}
    for row in rows:
        address=int(row['address'],0)
        if address==0x203b9c0:continue
        flags=[0,1,2,3,4,7,0xffffffff,0x80000000,0x12345678];values=[1,37,0xffffffff] if address==0x203b560 else [0,1,-128,2147483647];cases=[(f,v,n) for f in flags for v in values for n in (0,0xf0000000)];vectors[address]=cases;native=image[address-0x2000000:address-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,vector in enumerate(cases):
            original=run(image,address,native,vector,seed);rebuilt=run(image,address,linked,vector,seed)
            if original!=rebuilt:raise ValueError('Original/rebuilt stream administrative trace differs')
            records.append(original)
    row=next(r for r in rows if r['address']=='0x203b560');source=ROOT/row['source'];directory=WORK/'wrong-start-flag';directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    wrong=directory/source.name;text=source.read_text();changed=text.replace('stream->startFlag = 0 ;','stream->startFlag = 1 ;')
    if changed==text:raise ValueError('Wrong full C flag control did not mutate source')
    wrong.write_text(changed);bad,body=build(wrong,directory/'link',negative=True);rejected=0
    for seed,vector in enumerate(vectors[0x203b560]):
        try:run(image,0x203b560,body,vector,seed)
        except ValueError:rejected+=1
        else:raise ValueError('Wrong compiled start flag passed actual administrative model')
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();limits=['Only initialized-nonzero stream Init and nonpositive-channel SetVolume administrative paths execute; initialized-zero Init, positive channel audio setters, division/callback routine, sound/hardware/I/O and gameplay-valid domains remain unexecuted.','Canonical native call/data entries, complete genuine links and type geometry are separate from this finite execution evidence. External BSS/storage/callback bodies receive0source/extent/authorship credit.']
    report=dict(status='passed',records=records,originalAndSourceReturningVectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=0,nativeDevicesOrScenesExecuted=0,traceSha256=trace,wrongC=dict(sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=rejected),limits=limits);write_json(LANE/'administrative-fixtures.json',report);return report
