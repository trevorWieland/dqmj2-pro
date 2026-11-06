import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json
from wave20261106_dwc_auth_next_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_auth_next_first_build import build

CREATE,ABORT,DESTROY,JOIN=0x2097488,0x20975b8,0x2097618,0x2097654
GLOBAL,CTRL,PARAM,HTTP,STOP,CALLBACK,SP=0x21d18f0,0x2171000,0x2178000,0x217c000,0x27e0000,0x27e1000,0x2701000
PROVIDERS={0x200708c:'arm',0x2006890:'arm',0x20987b0:'thumb'}


def vector(seed):return dict(present=seed%5!=0,httpPresent=(seed//2)%3!=0,activityWord=[0,1,3,0xffffffff][seed%4],callbackThumb=seed%2==0)


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x2000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);callback=CALLBACK|int(v['callbackThumb']);context=bytearray([0x61])*5108;struct.pack_into('<I',context,0x1314,HTTP if v['httpPresent'] else 0);struct.pack_into('<I',context,0x1384,v['activityWord']);struct.pack_into('<I',context,0x1210,callback);param=bytearray([0x62])*72;struct.pack_into('<II',param,64,callback,callback);memory={GLOBAL:struct.pack('<III',0x11223344,0x22334455,CTRL if v['present'] or a==JOIN else 0),CTRL:bytes(context),PARAM:bytes(param),HTTP:bytes([0x63])*7188}
    for at,data in memory.items():cpu.mem_write(at,data)
    if a==CREATE:
        args=[PARAM,HTTP];expected=dict(kind='return',value=2) if v['present'] else dict(kind='provider',address=hex(CALLBACK));frame=[0x20deb70,5108] if not v['present'] else None
    elif a==ABORT:args=[];expected=dict(kind='provider',address=hex(0x200708c)) if v['present'] else dict(kind='return');frame=[CTRL+0x13d8] if v['present'] else None
    elif a==DESTROY:
        args=[];target=0x20987b0 if v['httpPresent'] else CALLBACK;expected=dict(kind='provider',address=hex(target)) if v['present'] else dict(kind='return');frame=[HTTP] if v['httpPresent'] else [0x20deb80,CTRL,0]
    else:args=[];expected=dict(kind='provider',address=hex(0x2006890)) if v['activityWord'] else dict(kind='return');frame=[CTRL+0x1318] if v['activityWord'] else None
    initial=[0x64d00000+i*0x101+seed for i in range(15)];initial[:len(args)]=args;initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;interface=True;captured=True;pcs=[]
    def code(machine,at,size,user):
        nonlocal observed,interface,captured
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if at==STOP:
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual Auth caller return ABI differs')
            observed=dict(kind='return')
            if a==CREATE:observed['value']=regs[0]
            machine.emu_stop();return
        if at==CALLBACK or at in PROVIDERS:
            mode='thumb' if at==CALLBACK and v['callbackThumb'] else 'arm' if at==CALLBACK else PROVIDERS[at]
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError('Actual Auth provider/indirect callback mode differs')
            observed=dict(kind='provider',address=hex(at));interface=frame is None or regs[:len(frame)]==frame
            if a==DESTROY:captured=regs[4]==callback
            machine.emu_stop();return
        if not a<=at<a+len(body) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Auth caller escaped genuine bounded body')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        raise ValueError('Unexpected Auth caller RAM write before provider')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Auth caller did not reach bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in memory.items())
    return dict(address=row['address'],seed=seed,vector=v,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface and captured,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,earlyFreeCallbackCapturePassed=captured,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    variants={CREATE:('return DWCAUTH_E_MEMERR;','return 1;'),ABORT:('OS_LockMutex(&DWCauth->mutex);','OS_LockMutex((OSMutex*)&DWCauth->thread);'),DESTROY:('native_data_020deb80,DWCauth,0','native_data_020deb80,DWCauth,4'),JOIN:('activityWord108 != 0','activityWord108 == 0')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);left=run(image,row,native,v,seed);right=run(image,row,compiled,v,seed)
            if left!=right or not left['modelPassed']:raise ValueError(('Independent Auth argument/guard/lifecycle model differs',left,right))
            records.append(left)
        directory=WORK/'wrong-c'/f'{a:08x}';directory.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
        before,after=variants[a];text=(ROOT/row['source']).read_text();changed=text.replace(before,after,1)
        if changed==text:raise ValueError(('Meaningful Auth wrong-C negative did not mutate',row['address']))
        source=directory/'wrong.c';source.write_text(changed);bad,body=build(source,directory/'proof',negative=True);failed=sum(not run(image,row,body,vector(seed),seed)['modelPassed'] for seed in range(16))
        if not failed:raise ValueError('Wrong whole Auth C did not reject independent model')
        negative.append(dict(address=row['address'],genuinelyLinked=True,matchedNative=False,independentModelFailures=failed,changedExpression=[before,after],realLink=bad['realLink']))
    coverage={row['address']:sorted({r['observed'].get('address','return') for r in records if r['address']==row['address']}) for row in rows}
    if coverage[hex(DESTROY)]!=sorted(['return',hex(CALLBACK),hex(0x20987b0)]):raise ValueError('Auth destroy callback/provider branch coverage incomplete')
    for target in [CREATE,DESTROY]:
        if {r['vector']['callbackThumb'] for r in records if r['address']==hex(target) and r['observed']==dict(kind='provider',address=hex(CALLBACK))}!={False,True}:raise ValueError('Both original indirect callback modes were not exercised')
    limits=['512 paired actual original/source entries: complete null/already-allocated/inactive-lifecycle guards and exact allocator/free/HTTP/mutex/thread provider frames. Both ARM/Thumb indirect callback modes, read-only work/param/global guards and early free-callback R4 capture checked.0callee/provider instructions or synthetic returns.','All allocation/free/clear callbacks, Auth creation remainder, mutex locking/abort mutation, actual HTTP abort/destroy, thread joins and post-provider paths remain unexecuted.0network/device/hardware/game/nativeWindows execution.','Work5108 layout, stack-first ordering and exact original tags/default result/termination/reset/callback-capture code compile and genuinely whole-link byte-exact. No original BSS/data storage extent or callee source credit. Thread+108 is an observed lifecycle word; id/state meaning unproven.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,requiredProviderBranchCoverage=coverage,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
