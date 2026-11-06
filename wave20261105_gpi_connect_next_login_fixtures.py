import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_login_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_login_build import build

PROVIDER,REFERENCE,CONNECTION,DATA,STOP,SP=0x20aced4,0x2170000,0x2171000,0x2173000,0x27e0000,0x2701000


def run(image,row,body,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    memory={REFERENCE:struct.pack('<I',CONNECTION),CONNECTION:bytes((i*17+seed)&255 for i in range(0x630)),DATA:bytes((i*31+seed)&255 for i in range(776))}
    for at,data in memory.items():cpu.mem_write(at,data)
    initial=[(0x55aa0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[0:2]=[REFERENCE,DATA];initial[-2:]=[SP,STOP|1]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=False
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==PROVIDER:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual login provider Thumb mode differs')
            observed=dict(kind='provider',address=hex(at));interface=[machine.reg_read(ar.UC_ARM_REG_R0),machine.reg_read(ar.UC_ARM_REG_R1)]==[DATA+128,32];machine.emu_stop();return
        if at==STOP:raise ValueError('Unexpected login return before random provider')
        if not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Login escaped actual bounded entry prefix')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP):raise ValueError('Unexpected login pre-provider RAM write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Login failed to reach real provider entry')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in memory.items())
    return dict(address=row['address'],seed=seed,observed=observed,expected=dict(kind='provider',address=hex(PROVIDER)),topReturned=False,partialProviderStopped=True,modelPassed=interface and guards,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);row=rows[0];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();records=[]
    for seed in range(128):
        original=run(image,row,native,seed);source=run(image,row,linked,seed)
        if original!=source or not original['modelPassed']:raise ValueError('Actual native/source random-provider interface differs')
        records.append(original)
    folder=WORK/'fixtures/wrong-C';folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    wrong=folder/'match.c';text=(ROOT/row['source']).read_text();changed=text.replace('sizeof(data->userChallenge) - 1','sizeof(data->userChallenge) - 2',1)
    if changed==text:raise ValueError('Whole login wrong-C did not mutate')
    wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
    if bad['compiledBytes']!=row['bytes']:raise ValueError('Whole login wrong-C changed extent')
    failures=[run(image,row,body,seed) for seed in range(16)]
    if any(r['modelPassed'] for r in failures):raise ValueError('Wrong login C accepted independent provider-frame model')
    limits=['One complete ordinary C login928 body genuinely matches original whole native extent,all original imported call/data words and scoped native608/60c/62c field-load proofs.Original SDKrevision3 and emptyNULbyte020e0a10 retained;0external initialized/BSS storage extent/authorship credit.','128paired actual entries stop BEFORE original randomString provider020aced4; independently require challenge-bufferDATA+128 and length32 plus untouched caller memory.0complete returns,0provider instruction executions,0synthetic returns.','One same-extent whole wrong-C genuinely links and violates16provider argument models. Wrong connection suffix layout,original field/instruction/pool proofs and unchanged original binding negatives reject. All post-random-provider branch/MD5/hash/string/cache/login/network behavior and suffix-field execution remain unexecuted;0device/game/nativeWindows execution.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=0,nativeAndCompiledPartialStops=256,actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=1,wrongC=[dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures)],nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
