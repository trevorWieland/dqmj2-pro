import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gpi_connect_next_set_info_int_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_set_info_int_build import build

SPRINTF,LOCAL,USER,ERROR=0x200616c,0x20ae8e8,0x20ae918,0x20b2c88
REFERENCE,CONNECTION,STOP,SP=0x2170000,0x2171000,0x27e0000,0x2701000
INFOS=[1800,1803,1798,1804,1805,1806,1808,1810,1811,1812,1813,1816,1817,1818,1819,1820,1821,1822,0,2147483647]
VALUES=[-2147483648,2147483647,0,1,-1,4,-4,16,17,-16,-17,1280,1281,1282,1283,256]
FORMATTED={1800,1798,1804,1805,1806,1808,1810,1811,1812,1813,1816,1817,1818,1819,1820,1821,1822}


def divided(value,n):return -(abs(value)//n) if value<0 else value//n


def run(image,row,body,info,value,seed,roles):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);memory={REFERENCE:struct.pack('<I',CONNECTION),CONNECTION:bytes([0x77])*0x600}
    for at,data in memory.items():cpu.mem_write(at,data)
    expected_value=value;provider=ERROR;args=[REFERENCE,roles['Invalid info.']]
    if info==1800 and value<0:args=[REFERENCE,roles['Invalid zipcode.']]
    elif info==1803:
        if value in [1280,1281,1282]:provider=LOCAL;args=[REFERENCE,roles['\\sex\\'],roles[str(value-1280)]]
        else:args=[REFERENCE,roles['Invalid sex.']]
    elif info in FORMATTED:
        provider=SPRINTF;args=[]
        if info==1806:expected_value=divided(value,16)
        elif info in [1808,1810]:expected_value=divided(value,4)
        elif info==1813:expected_value=int(value!=0)
    expected=dict(kind='provider',address=hex(provider));initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:3]=[REFERENCE,info&0xffffffff,value&0xffffffff];initial[-2:]=[SP,STOP|1]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,val in zip(C.REGISTERS,initial):cpu.reg_write(reg,val)
    observed=None;pcs=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if at in [SPRINTF,LOCAL,USER,ERROR]:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(at!=SPRINTF):raise ValueError('Actual integer-info provider ARM/Thumb mode differs')
            observed=dict(kind='provider',address=hex(at))
            if at==SPRINTF:interface=SP-0x100<=regs[0] and regs[0]+16<=SP and regs[1:3]==[roles['%d'],expected_value&0xffffffff]
            else:interface=regs[:len(args)]==args
            machine.emu_stop();return
        if at==STOP:raise ValueError('Unexpected integer-info return before real provider')
        if not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Integer-info escaped bounded caller/mode')
        pcs.append(at)
    def write(machine,access,at,size,val,user):
        if not(SP-0x4000<=at and at+size<=SP):raise ValueError('Unexpected integer-info pre-provider RAM write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Integer-info caller failed to reach actual provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in memory.items())
    return dict(address=row['address'],seed=seed,info=info,value=value,expectedIntegerArgument=expected_value,observed=observed,expected=expected,topReturned=False,partialProviderStopped=True,modelPassed=observed==expected and interface and guards,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);row=rows[0];a=int(row['address'],0);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();roles={k:int(v,0) for k,v in read_json(LANE/'native-string-roles.json')['roles'].items()};records=[]
    for i,info in enumerate(INFOS):
        for j,value in enumerate(VALUES):
            seed=i*len(VALUES)+j;original=run(image,row,native,info,value,seed,roles);source=run(image,row,linked,info,value,seed,roles)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent signed-integer/enum/error/provider model differs',original,source))
            records.append(original)
    folder=WORK/'fixtures/wrong-C';folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    wrong=folder/'match.c';text=(ROOT/row['source']).read_text();changed=text.replace('value /= 16;','value /= 8;',1)
    if changed==text:raise ValueError('Whole integer-info wrong-C did not mutate')
    wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
    if bad['compiledBytes']!=row['bytes']:raise ValueError('Whole integer-info wrong-C extent differs')
    failures=[]
    for seed,value in enumerate([16,17,-16,-17,-2147483648,2147483647,32,-32,64,-64,128,-128,256,-256,512,-512]):
        result=run(image,row,body,1806,value,seed,roles)
        if result['modelPassed']:raise ValueError('Whole wrong integer-info C accepted independent signed division model')
        failures.append(result)
    limits=['One complete ordinary C integer-info776 caller genuinely matches all original native bytes/imports and int32 enum/result ABI. Actual CHECK_RESULT propagation macro is defined;no implicit macro-as-function is adopted.0external storage allocation/authorship credit.','320paired actual entries independently cover20info selectors and16signed/enum values,including INTMIN/MAX,invalid negative zipcode,sex1280/1281/1282/error,unsupportedselectors,boolean nonzero normalization,and signed truncation-toward-zero by16/4 before actual provider frames.0synthetic returns.','0complete caller returns and0sprintf/local-info/user-info/error-setter bodies execute;allproviders stop BEFORE instructions. One sameextent whole wrong-C776 genuinely links and violates16independent signed-division/printf frames;wrong enum-width ABI and original binding negatives reject.0formattedoutput/network/game/device/nativeWindows execution.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=0,nativeAndCompiledPartialStops=640,actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=1,wrongC=[dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures)],nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
