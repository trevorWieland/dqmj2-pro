import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_cache_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_cache_build import build

GETINFO,SETCACHE,GETPROFILE,FREECACHE,ADDOP=0x20af244,0x20af33c,0x20b0a50,0x20af3c8,0x20afa1c
REFERENCE,CONNECTION,PROFILE,CACHE,PARAM,STOP,SP=0x2170000,0x2171000,0x2172000,0x2173000,0x2175000,0x27e0000,0x2701000


def vector(seed):return dict(infoCaching=seed%2,checkCache=(seed//2)%3,callbackPresent=(seed//6)%2!=0,blocking=seed%2,profileid=seed*17-100)


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    connection=bytearray([0x77]*0x5d8);struct.pack_into('<I',connection,256,v['infoCaching']);profile=bytearray([0xa6]*32);struct.pack_into('<I',profile,16,CACHE);callback=0x2178001 if v['callbackPresent'] else 0
    memory={REFERENCE:struct.pack('<I',CONNECTION),CONNECTION:bytes(connection),PROFILE:bytes(profile),CACHE:bytes([0xc3])*240,SP:struct.pack('<II',callback,PARAM)}
    for at,data in memory.items():cpu.mem_write(at,data)
    if a==SETCACHE:args=[REFERENCE,PROFILE,CACHE];expected=dict(kind='provider',address=hex(FREECACHE)) if v['infoCaching'] else dict(kind='return',value=1)
    else:
        args=[REFERENCE,v['profileid'],v['checkCache'],v['blocking']];expected=dict(kind='provider',address=hex(GETPROFILE if callback and v['infoCaching'] and v['checkCache']==1 else ADDOP))
    initial=[(0x77cc0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):initial[i]=arg&0xffffffff
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if at==STOP:
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual cache return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in [FREECACHE,GETPROFILE,ADDOP]:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual cache provider mode differs')
            observed=dict(kind='provider',address=hex(at))
            if at==FREECACHE:interface=regs[0]==PROFILE
            elif at==GETPROFILE:interface=regs[:2]==[REFERENCE,v['profileid']&0xffffffff] and SP-0x100<=regs[2]<SP
            else:interface=regs[:3]==[REFERENCE,2,0] and SP-0x100<=regs[3]<SP and bytes(machine.mem_read(regs[3],4))==bytes(4) and struct.unpack('<III',machine.mem_read(regs[13],12))==(v['blocking'],callback,PARAM)
            machine.emu_stop();return
        if not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Cache caller escaped bounded code/mode')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP):raise ValueError('Unexpected pre-provider cache memory write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Actual cache caller did not reach bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in memory.items())
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);original=run(image,row,native,v,seed);source=run(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent cache gate/frame model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/'match.c';text=(ROOT/row['source']).read_text();changed=text.replace('if(!iconnection->infoCaching)','if(iconnection->infoCaching)',1)
        if changed==text:raise ValueError('Whole cache wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Whole wrong cache C changed extent')
        failures=[]
        for seed in range(16):
            v=vector(seed);v.update(infoCaching=0,callbackPresent=True,checkCache=1);result=run(image,row,body,v,seed)
            if result['modelPassed']:raise ValueError('Wrong cache C accepted independent gate model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures))
    limits=['Two complete ordinary C cache/info callers388B genuinely match native full extents and imports.240-byte cache layout,32-byte profile/cachepointer16,516-byte response and operation36/id24 compiler-qualified;0external cache storage allocation/authorship credit.','256paired actual entries cover cachingdisabled return1,actual cache/checkCache/callback gates,pre-free/profilelookup/addoperation provider frames includingstack blocking/callback/parameter values and untouched callerRAM.0synthetic returns;all providers stop BEFORE instructions.','No free/allocator/cachecopy/duplicate/profiletable/operation/callback bodies,post-provider mutation,complete get-info return,network/device/game/nativeWindows execution.2sameextent whole wrong-C variants genuinely link and violate32independent models;2wrong cachelayouts and original binding negatives reject.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
