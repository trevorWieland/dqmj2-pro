import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_disconnect_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_disconnect_build import build

APPEND,SEND,UDP,FREE=0x20ac6f4,0x20ac954,0x20a99c0,0x20a929c
REFERENCE,CONNECTION,BUFFER,STOP,SP=0x2170000,0x2171000,0x2175000,0x27e0000,0x2701000


def run(image,row,body,seed,fragment=False):
    a=int(row['address'],0);state=3 if fragment else [4,0,1,3][seed%4];tell=(seed//4)%2;cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    connection=bytearray([0x77]*0x600);struct.pack_into('<II',connection,0x19c,seed+11,seed+21);struct.pack_into('<III',connection,0x1f0,0xffffffff,state,BUFFER);expected_connection=bytearray(connection)
    if fragment:
        struct.pack_into('<II',expected_connection,0x19c,0,0);struct.pack_into('<I',expected_connection,0x1f4,4);expected=dict(kind='provider',address=hex(UDP))
    elif state==4:expected=dict(kind='return')
    else:expected=dict(kind='provider',address=hex(UDP if state==0 else APPEND if state==3 and tell else SEND))
    memory={REFERENCE:struct.pack('<I',CONNECTION),CONNECTION:bytes(connection),BUFFER:bytes([0xc5])*32}
    for at,data in memory.items():cpu.mem_write(at,data)
    initial=[(0x44dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:2]=[REFERENCE,tell];initial[-2:]=[SP,STOP|1]
    if fragment:initial[4:6]=[CONNECTION,REFERENCE]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if at==STOP:
            if fragment or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Disconnect actual return ABI differs')
            observed=dict(kind='return');machine.emu_stop();return
        if at in [APPEND,SEND,UDP,FREE]:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual disconnect provider mode differs')
            observed=dict(kind='provider',address=hex(at))
            if at==APPEND:interface=regs[:3]==[REFERENCE,CONNECTION+0x210,0x20e0c54]
            elif at==SEND:interface=regs[:3]==[REFERENCE,0xffffffff,CONNECTION+0x210] and SP-0x100<=regs[3]<SP and struct.unpack('<II',machine.mem_read(regs[13],8))==(1,0x20e0c68)
            elif at==FREE:interface=regs[0]==BUFFER
            machine.emu_stop();return
        if not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Disconnect escaped bounded original code/mode')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if fragment and size==4 and at in [CONNECTION+0x19c,CONNECTION+0x1a0,CONNECTION+0x1f4]:return
        raise ValueError(('Unexpected disconnect RAM write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);start=0x20adec6 if fragment else a;cpu.emu_start(start|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Disconnect failed to reach bounded return/provider')
    expected_memory=dict(memory);expected_memory[CONNECTION]=bytes(expected_connection);guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in expected_memory.items())
    return dict(address=row['address'],seed=seed,initialState=state,tellServer=tell,enteredFunctionEntry=not fragment,internalFragmentStart=hex(start) if fragment else None,fragmentPrecondition='R4=connection,R5=reference,closed socket;manual internal-block context,not a function call' if fragment else None,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def wrong_source(text):
    start=text.index('iconnection->connectState = GPI_DISCONNECTED;');end=text.index('iconnection->profileid = 0;',start)+len('iconnection->profileid = 0;');engine=text.index('if( gsUdpEngine',end);b=text.index('{',engine);depth=1;e=b+1
    while depth:depth+=(text[e]=='{')-(text[e]=='}');e+=1
    if text[end:engine].strip()!='}':raise ValueError('Measured native outer block geometry differs')
    return text[:start]+text[engine:e]+'\n'+text[start:end]+'\n}\n'+text[e:]


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);row=rows[0];a=int(row['address'],0);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();records=[];fragments=[]
    for fragment,destination in [(False,records),(True,fragments)]:
        for seed in range(128):
            original=run(image,row,native,seed,fragment);source=run(image,row,linked,seed,fragment)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent disconnect gate/order model differs',original,source))
            destination.append(original)
    folder=WORK/'fixtures/wrong-C';folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    wrong=folder/'match.c';wrong.write_text(wrong_source((ROOT/row['source']).read_text()));bad,body=build(wrong,folder/'genuine-link',negative=True)
    if bad['compiledBytes']!=row['bytes']:raise ValueError('Whole wrong disconnect C changed extent')
    failures=[]
    for fragment in [False,True]:
        for seed in range(16):
            chosen=seed*4+1 if not fragment else seed;result=run(image,row,body,chosen,fragment)
            if result['modelPassed']:raise ValueError('Whole wrong disconnect C accepted independent gate/order model')
            failures.append(result)
    limits=['One complete ordinary C disconnect384 body genuinely matches full original extent/imports,original tagged cleanupcallback020add5d/canonicalThumb020add5c and private minimumconnection600/profileList12/peer5d4/updatebuffers5e0/5f0/peer-next76 views;0callee or external storage allocation/authorship credit.','128paired actual functionentries cover already-disconnected voidreturns,initialstate0 UDPcleanup and connected logout/send provider frames.0synthetic returns;allUDP/socket/send/append/free/callback providers stop BEFORE instructions.','Separately128paired INTERNAL BASIC BLOCK starts020adec6 manually seedR4connection/R5reference afterclosed-socket condition and verify three original state/user/profile stores BEFOREUDPprovider. These are not functionentry calls/returns or caller-path reachability executions.','One sameextent complete wrong-C variant genuinely links;16functionentry state0 models and16separate internal-block state-order models reject the publiccomparison condition/order. Wrong layout,6native-flow and original binding negatives reject.0UDP/socket/free/profilemap/cleanup callback bodies,network/device/game/nativeWindows execution.']
    trace=hashlib.sha256(json.dumps(dict(entries=records,internalBlocks=fragments),sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,internalBlockRecords=fragments,actualNativeAndSourceInternalBlockStops=256,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=1,wrongC=[dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures)],nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
