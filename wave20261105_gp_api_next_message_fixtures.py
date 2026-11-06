import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gp_api_next_message_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gp_api_next_message_build import build

VIEW,DATA,MESSAGE,TYPE,LENGTH,KEY,STOP,SP=0x2170000,0x2171000,0x2172000,0x2172010,0x2172020,0x20b2ae0,0x27e0000,0x2701000


def helpers(image):
    text=(ROOT/'config/arm9/symbols.txt').read_text();result={}
    for a,size in [(0x201d948,60),(0x201d914,52)]:
        record=next((x for x in text.splitlines() if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(size,a),x)),None)
        if record is None:raise ValueError('Actual original ARM header string helper entry differs')
        result[a]=dict(address=hex(a),mode='arm',bytes=size,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+size]).hexdigest(),sourceCredit=0)
    return result


def vector(seed):
    cases=[b'',b'a',b'abcd',b'abcde',b'abcdefghi',b'abcde\nabc',b'\\m\\1\\len\\3\\msg\\\nabc\0',b'\\m\\7\\len\\0\\msg\\\n\0'];return cases[seed%len(cases)]


def run(image,row,body,raw,seed,allowed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);payload=raw+b'\0';cpu.mem_write(DATA,payload);view=struct.pack('<Iiii',DATA,512,len(raw),7);cpu.mem_write(VIEW,view);cpu.mem_write(MESSAGE,struct.pack('<I',0xdeadbeef));cpu.mem_write(TYPE,struct.pack('<I',0x12345678));cpu.mem_write(LENGTH,struct.pack('<I',0x87654321));cpu.mem_write(SP,struct.pack('<I',LENGTH));initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=[0,VIEW,MESSAGE,TYPE];initial[-2:]=[SP,STOP|1]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    expected_data=bytearray(payload);newline=raw.find(b'\n');expected=dict(kind='return',value=0)
    if len(raw)>=5 and newline>=0:
        if newline<5:raise ValueError('Fixtures do not supply undefined short LF headers')
        if raw[newline-5:newline]!=b'\\msg\\':expected=dict(kind='return',value=3)
        else:expected=dict(kind='provider',address=hex(KEY));expected_data[newline]=0
    observed=None;pcs=[];calls=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Message parser actual return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at==KEY:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Message key provider original Thumb mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];observed=dict(kind='provider',address=hex(KEY));interface=regs[0]==DATA and bytes(machine.mem_read(regs[1],4))==b'\\m\\\0' and regs[3]==16 and SP-0x4000<=regs[2]<SP;machine.emu_stop();return
        helper=next((r for address,r in allowed.items() if address<=at<address+r['bytes']),None)
        if at in allowed:calls.append(at)
        mode='thumb' if a<=at<a+row['bytes'] else helper['mode'] if helper else None
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError(('Message parser escaped actual body/helper/mode',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP+4 or DATA<=at and at+size<=DATA+len(payload) or MESSAGE<=at and at+size<=MESSAGE+4):raise ValueError(('Message parser unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Message parser did not reach actual return/provider')
    guards=bytes(cpu.mem_read(DATA,len(payload)))==bytes(expected_data) and bytes(cpu.mem_read(VIEW,16))==view and bytes(cpu.mem_read(MESSAGE,4))==bytes(4) and bytes(cpu.mem_read(TYPE,4))==struct.pack('<I',0x12345678) and bytes(cpu.mem_read(LENGTH,4))==struct.pack('<I',0x87654321)
    return dict(address=row['address'],inputHex=raw.hex(),seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],providerInstructionExecutions=0,frameAndOutputGuardsPreserved=guards,dataSha256=hashlib.sha256(bytes(cpu.mem_read(DATA,len(payload)))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();allowed=helpers(image);records=[];negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(64):
            raw=vector(seed);original=run(image,row,native,raw,seed,allowed);source=run(image,row,linked,raw,seed,allowed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent structural message header model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();changed=text.replace('inputBuffer->len < 5','inputBuffer->len >= 5',1)
        if changed==text:raise ValueError('Whole message parser C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Wrong message parser C extent changed')
        failures=[]
        for seed in range(16):
            result=run(image,row,body,vector(6),seed,allowed)
            if result['modelPassed']:raise ValueError('Wrong message parser C did not violate structural header model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],actualReturningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] for r in failures),records=failures))
    limits=['One184-byte ordinary C complete message parser genuinely links with unchanged original native calls/BLX/data literal witnesses. Actual16-byte input buffer layout and16-byte decimal-key workspace are compiled/checked.','64structural header inputs compare actual native/genuine source early minimum5-byte gates, missing LF, malformed LF header rejection, output pointer default and LF capping against an independent byte model. Actual original ARM strchr60/strncmp52 execute on RAM. Valid headers stop BEFORE the first canonical gpiValueForKey body; no synthetic return, key parsing/atoi/provider execution or payload completion claimed.','One same-extent genuine wrong-C length-gate variant violates16 actual-returning structural expectations; one wrong buffer scalar-width layout rejects. Complete numeric type/length/payload/NUL protocol behavior, network/callback/device/native Windows execution and helper/object-storage source remain0credit.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalHelperEntries=list(allowed.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
