import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_responses_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_responses_build import build

PROVIDER,REFERENCE,CONNECTION,NODE,INPUT,STOP,SP=0x20b2a4c,0x2170000,0x2171000,0x2172000,0x2173000,0x27e0000,0x2701000


def run(image,row,body,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    memory={REFERENCE:struct.pack('<I',CONNECTION),CONNECTION:bytes((i*17+seed)&255 for i in range(0x5d8)),NODE:bytes((i*31+seed)&255 for i in range(36)),INPUT:(b'\\npr\\' if a==0x20b0910 else b'\\dpr\\')+b'\\profileid\\123\\final\\\0'}
    for at,data in memory.items():cpu.mem_write(at,data)
    initial=[(0x55bb0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:3]=[REFERENCE,NODE,INPUT];initial[-2:]=[SP,STOP|1]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=False
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==PROVIDER:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual response provider mode differs')
            observed=dict(kind='provider',address=hex(at));interface=[machine.reg_read(ar.UC_ARM_REG_R0),machine.reg_read(ar.UC_ARM_REG_R1),machine.reg_read(ar.UC_ARM_REG_R2)]==[REFERENCE,INPUT,1];machine.emu_stop();return
        if at==STOP:raise ValueError('Unexpected response return before error provider')
        if not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Response escaped actual bounded entry prefix')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP):raise ValueError('Unexpected response pre-provider RAM write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Response did not reach actual error-provider entry')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in memory.items())
    return dict(address=row['address'],seed=seed,observed=observed,expected=dict(kind='provider',address=hex(PROVIDER)),topReturned=False,partialProviderStopped=True,modelPassed=interface and guards,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(128):
            original=run(image,row,native,seed);source=run(image,row,linked,seed)
            if original!=source or not original['modelPassed']:raise ValueError('Actual profile-response provider frame differs')
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/'match.c';text=(ROOT/row['source']).read_text();changed=text.replace('gpiCheckForError(connection, input, GPITrue)','gpiCheckForError(connection, input, GPIFalse)',1)
        if changed==text:raise ValueError('Whole response wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Whole response wrong-C extent changed')
        failures=[run(image,row,body,seed) for seed in range(16)]
        if any(r['modelPassed'] for r in failures):raise ValueError('Wrong response C accepted independent provider model')
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures))
    limits=['Two complete ordinary C profile-response callers372B genuinely match full native extents/all original imports and exact response8/profile4,operation36/callback12,knownconnection/profileid1a0 layouts;0external storage allocation/authorship credit.','256paired actual entries stop BEFORE original CheckForError provider020b2a4c and independently require connection/input/true argument frame plus untouchedRAM.0complete returns,0provider instruction executions,0synthetic returns.','All post-provider parser/error/allocator/response/callback/remove-operation effects remain unexecuted;0network/device/game/nativeWindows execution.2sameextent whole wrong-C variants genuinely link and violate32independent argument models;2wrong response layouts plus original binding negatives reject.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=0,nativeAndCompiledPartialStops=512,actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=2,wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
