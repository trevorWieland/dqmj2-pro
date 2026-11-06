import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_keys_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_keys_build import build

DESTROY,ADD,SET,CHECK=0x20af494,0x20af4bc,0x20af510,0x20af578
ERROR,DUP,ARRAYFREE=0x20b2c88,0x20a8ea0,0x20a8614
REFERENCE,CONNECTION,ARRAY,NAME,VALUE,OUTPUT,STOP,SP=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x27e0000,0x2701000


def vector(a,seed):return dict(arrayPresent=seed%2!=0,namePresent=seed%3!=0,valuePresent=(seed//3)%2!=0)


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);cpu.mem_write(REFERENCE,struct.pack('<I',CONNECTION));connection=bytearray([0x77]*0x5d8);struct.pack_into('<I',connection,0x3b4,ARRAY if v['arrayPresent'] else 0);cpu.mem_write(CONNECTION,bytes(connection));cpu.mem_write(ARRAY,bytes([0xd3])*24);cpu.mem_write(NAME,b'key-name\0');cpu.mem_write(VALUE,b'key-value\0');cpu.mem_write(OUTPUT,struct.pack('<I',0xabcdef77));name=NAME if v['namePresent'] else 0;value=VALUE if v['valuePresent'] else 0
    if a==DESTROY:
        args=[REFERENCE];expected=dict(kind='provider',address=hex(ARRAYFREE)) if v['arrayPresent'] else dict(kind='return');provider_args=[ARRAY]
    else:
        args=[REFERENCE,ARRAY,name,OUTPUT if a==CHECK else value]
        if not name:expected=dict(kind='provider',address=hex(ERROR));provider_args=[REFERENCE,0x20e0f64]
        elif a==ADD and not value:expected=dict(kind='provider',address=hex(ERROR));provider_args=[REFERENCE,0x20e0f78]
        else:expected=dict(kind='provider',address=hex(DUP));provider_args=[name]
    initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):initial[i]=arg&0xffffffff
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Key actual return ABI differs')
            observed=dict(kind='return');machine.emu_stop();return
        if at in [ERROR,DUP,ARRAYFREE]:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual key provider mode differs')
            observed=dict(kind='provider',address=hex(at));regs=[machine.reg_read(r) for r in C.REGISTERS];interface=regs[:len(provider_args)]==provider_args;machine.emu_stop();return
        if not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('Keys escaped bounded caller/mode',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP) and not(CONNECTION<=at and at+size<=CONNECTION+len(connection)):raise ValueError(('Key unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Key caller did not reach actual return/provider')
    guards=bytes(cpu.mem_read(CONNECTION,len(connection)))==bytes(connection) and bytes(cpu.mem_read(REFERENCE,4))==struct.pack('<I',CONNECTION) and bytes(cpu.mem_read(ARRAY,24))==bytes([0xd3])*24 and bytes(cpu.mem_read(NAME,9))==b'key-name\0' and bytes(cpu.mem_read(VALUE,10))==b'key-value\0' and bytes(cpu.mem_read(OUTPUT,4))==struct.pack('<I',0xabcdef77)
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=0,helperEntries=[],providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[];variants={DESTROY:('if (iconnection->extendedInfoKeys)','if (!iconnection->extendedInfoKeys)'),ADD:('if (!theKeyName)','if (theKeyName)'),SET:('if (!keyName)','if (keyName)'),CHECK:('if (!keyName)','if (keyName)')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(a,seed);original=run(image,row,native,v,seed);source=run(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent key input/provider frame differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole key wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong key C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,seed);v.update(arrayPresent=True,namePresent=True,valuePresent=True);result=run(image,row,body,v,seed)
            if result['modelPassed']:raise ValueError('Wrong key C accepted independent model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],actualReturningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] for r in failures),records=failures))
    limits=['Four complete ordinaryC key-destroy/add/set/check bodies genuinely match whole native extents and exact original imports.8-byte keypair(name0/value4),known connection prefix5d8/extendedInfoKeys3b4 compiler-qualified; original comparator literal020af4b1 retains actual Thumb tag and canonicalentry020af4b0,0callee source/storage credit.','512paired actual entry vectors independently cover missing-key-array actualreturns and null-name/null-value/valid-string provider gates, original error/duplicate/free argument frames and untouched RAM.0synthetic returns; error setter/string duplication/arrayfree/search/comparator bodies stop BEFORE instructions and remain unexecuted.','Four complete same-extent wrong-C variants genuinely link and violate64 independent frame/gate models.4wrong keypair layouts and unchanged native CPU/program/module/mode/kind/entry/addend/origin/opcode/tag/literal negatives reject. Literal callback word exactness is static binding/link evidence; no callback dispatch result,heap mutation,new key output or network/game/nativeWindows execution inferred.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
