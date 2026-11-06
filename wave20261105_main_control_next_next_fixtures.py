import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_main_control_next_next_build import build
from wave20261105_main_control_next_next_controls import original_helpers,HELPERS

LANE=ROOT/'evidence/lanes/parallel-wave20261105/main-control-next/next'
WORK=ROOT/'work/w5cn/next/fixtures'
INFO,OUTPUT,STOP,SP=0x2174000,0x2178000,0x27e0000,0x2701000


def setup(vector):
    model=read_json(HELPERS)['model'];state=int(model['randomState'],0);lookup=int(model['lookupState'],0)
    info=bytearray(8);info[0]=vector['mode'];info[3]=vector['kind'];info[4]=vector['subtype']
    initial={state:struct.pack('<I',vector['randomSeed']),lookup:struct.pack('<I',INFO),INFO:bytes(info),OUTPUT:struct.pack('<i',-1234567)}
    expected=dict(initial);result=0;calls=0
    eligible=vector['mode']!=0 and ((vector['kind'] in (4,6,8) and vector['subtype']==3) or (vector['kind']==7 and vector['subtype'] in (3,4)))
    if eligible:
        next_seed=(vector['randomSeed']*model['multiplier']+model['increment'])&0xffffffff;expected[state]=struct.pack('<I',next_seed);calls=1
        bound=800 if vector['kind']==7 and vector['subtype']==4 else 1600
        if ((next_seed>>16)%bound)<vector['threshold']:
            result={4:2,6:42,8:53,7:8}[vector['kind']];expected[OUTPUT]=struct.pack('<i',1 if vector['kind'] in (6,8) else -1)
    return initial,expected,[vector['mode'],vector['threshold']&0xffffffff,OUTPUT,0],result,calls


def run(image,row,body,vector,seed,helpers):
    address=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    regions,expected,args,result,calls=setup(vector)
    for at,data in regions.items():cpu.mem_write(at,data)
    initial=[(0x55660000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=args;initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x10)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    entries={a:0 for a in helpers};pcs=[];returned=False;state=int(read_json(HELPERS)['model']['randomState'],0)
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if at in entries:entries[at]+=1
        if not address<=at<address+row['bytes'] and not any(a<=at<a+helpers[a]['bytes'] for a in helpers):raise ValueError(('Conditional result fixture escaped original graph',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not ((SP-0x4000<=at and at+size<=SP) or (at==state and size==4) or (at==OUTPUT and size==4)):raise ValueError('Conditional result fixture wrote outside stack/state/output')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address,STOP+4,count=30000);registers=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Actual conditional result caller return/ABI differs')
    actual={a:bytes(cpu.mem_read(a,len(v))) for a,v in regions.items()};passed=actual==expected and registers[0]==result and entries[0x207d2c8]==1 and entries[0x203d294]==calls and entries[0x2026350]==calls
    return dict(address=hex(address),vector=vector,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,modelPassed=passed,returnValue=registers[0],memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),actualOriginalHelperEntries={hex(a):n for a,n in entries.items()},actualOriginalHelperInvocations=sum(entries.values()))


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers={int(r['address'],0):r for r in original_helpers()};records=[];negative=[]
    for row in rows:
        address=int(row['address'],0);native=image[address-0x2000000:address-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        cases=[dict(mode=1,kind=k,subtype=s,threshold=t,randomSeed=r) for k in [4,6,7,8,9] for s in [3,4] for t in [-1,0,100,800,1600] for r in [0,1,0xffffffff,0x12345678]]
        cases += [dict(mode=m,kind=4 if m==0 else 0,subtype=3 if m==0 else 0,threshold=1600,randomSeed=r) for m in [0,1] for r in [0,1,0xffffffff,0x12345678]]
        for seed,vector in enumerate(cases):
            original=run(image,row,native,vector,seed,helpers);source=run(image,row,linked,vector,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent conditional result model differs',original,source))
            records.append(original)
        folder=WORK/format(address,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];text=source.read_text();changed=text.replace('return 2;','return 3;',1)
        if changed==text:raise ValueError('Whole wrong conditional result C did not mutate')
        wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Whole wrong conditional result C changed complete extent')
        controls=[];badvector=dict(mode=1,kind=4,subtype=3,threshold=1600,randomSeed=0)
        for seed in range(16):
            actual=run(image,row,body,badvector,seed,helpers)
            if actual['modelPassed'] or not actual['topReturned']:raise ValueError('Wrong whole C did not return an actual model violation')
            controls.append(actual)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(controls),records=controls))
    positive=2*sum(r['actualOriginalHelperInvocations'] for r in records);bad=sum(r['actualOriginalHelperInvocations'] for n in negative for r in n['records'])
    report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=positive,actualPositiveOriginalHelperInvocations=positive,actualWrongCOriginalHelperInvocations=bad,totalActualOriginalHelperInvocations=positive+bad,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),wholeCNegativeControlsRejected=len(negative),wrongC=negative,limits=['Synthetic eight-byte first-match mode records and independent 32-bit LCG arithmetic exercise original lookup/RNG/unsigned-division helpers; all five chance cases include taken/rejected thresholds and output -1/+1, with mode-zero and unsupported-kind cases.','Each original/source run checks complete return, all allowed caller memory, RNG state transition, exact original helper entry counts and callee-saved ABI. Values avoid signed overflow; original external code/storage carries zero additional source credit.','Invalid lookup/null pointers, impossible sentinel traversal, full gameplay/callbacks/devices and complete external storage extent/authorship are unexecuted/uncredited. Kind/subtype labels describe measured bytes rather than established gameplay names.'])
    write_json(LANE/'caller-fixtures.json',report);return report
