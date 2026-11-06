import hashlib
import json
import random
import re
import shutil
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_browser_query_next_rpc_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_browser_query_next_rpc_build import build

STOP,SP,BUFFER=0x27e0000,0x2701000,0x2170000


def entries(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text().splitlines();result={}
    for a in [0x20072d0,0x200a41c]:
        record=next((x for x in inventory if re.fullmatch(r'\S+ kind:function\(arm,size=0x[0-9a-f]+\) addr:0x%08x'%a,x)),None)
        if record is None:raise ValueError('First actual canonical ARM helper absent')
        size=int(re.search('size=(0x[0-9a-f]+)',record)[1],0);result[a]=dict(address=a,mode='arm',bytes=size,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+size]).hexdigest(),sourceCredit=0)
    return result


def run(image,row,body,v,seed,helpers):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);guard=bytes((i*7+seed)&255 for i in range(256));cpu.mem_write(BUFFER,guard)
    initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1];initial[:3]=[v['address'],v['length'],v['buffer']]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    target=0x20072d0 if a==0x20a4cb8 else 0x200a41c;stopped=False;pcs=[]
    def code(machine,at,size,user):
        nonlocal stopped
        if at==target:
            if machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('First helper entered wrong instruction mode')
            stopped=True;machine.emu_stop();return
        if not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('RPC escaped caller before qualified boundary',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not SP-0x4000<=at or not at+size<=SP:raise ValueError(('RPC unexpected write before hardware boundary',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=1000)
    if not stopped:raise ValueError('RPC did not reach first actual helper boundary')
    actual=[cpu.reg_read(ar.UC_ARM_REG_R0),cpu.reg_read(ar.UC_ARM_REG_R1)];expected=[v['buffer'],v['length']] if a==0x20a4cb8 else [4,1];unchanged=bytes(cpu.mem_read(BUFFER,256))==guard
    return dict(address=row['address'],vector=v,seed=seed,partialCallerStopped=True,topReturned=False,actualOriginalHelperInvocations=0,stopBeforeCanonicalHelper=hex(target),helperMode='arm',actualArguments=actual,expectedArguments=expected,modelPassed=actual==expected and unchanged,bufferGuardPreserved=unchanged,helperInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def vectors():
    rng=random.Random(0x4cb8)
    return [dict(address=a,length=n,buffer=b) for a,n,b in [(0,0,BUFFER),(0xffffffff,0xffffffff,BUFFER),(1,1,BUFFER+1),(0x100,0xffff,BUFFER+4),(0x20000,0x10000,BUFFER+8),(0x80000000,0x80000000,BUFFER+3)]]+[dict(address=rng.getrandbits(32),length=rng.getrandbits(32),buffer=BUFFER+rng.randrange(16)) for i in range(26)]


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers=entries(image);records=[];negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(vectors()):
            original=run(image,row,native,v,seed,helpers);source=run(image,row,linked,v,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent partial RPC argument model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=('native_fn_020072d0(buffer,length);','native_fn_020072d0(0,length);') if a==0x20a4cb8 else ('native_fn_0200a41c(4,1)','native_fn_0200a41c(5,1)');changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole RPC C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong RPC C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed,v in enumerate(vectors()[:16]):
            result=run(image,row,body,v,seed,helpers)
            if result['modelPassed']:raise ValueError('Wrong complete RPC C did not violate partial argument model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],partialModelRejections=len(failures),records=failures))
    limits=['All three ordinary C complete native function extents and original relocations genuinely link exactly, including original tagged Thumb callback literals. Canonical callback body/source/storage receives0 additional credit.','96 independent native/source partial argument vectors stop BEFORE the first actual cache or FIFO readiness helper instruction. Cache caller stages original buffer/32-bit length; two readiness callers stage channel4/flag1. No hardware/cache/FIFO helper instruction, caller return, callback delivery, retry completion or service effect executes.','Three same-extent whole wrong C units genuinely link and violate the independent partial argument model48 times; zero complete returning model failures are claimed. Native/source caller-only instruction traces and buffer guards agree across scalar edge/random values and4NZCV patterns.','Halfword narrowing at the first send-loop length is retained in source and original full native bytes; that later send stage is not reached by these partial fixtures. Complete hardware behavior/device/game scenes and Windows execution remain unproven.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=0,nativeAndCompiledPartialStops=2*len(records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalStoppedHelperEntries=list(helpers.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
