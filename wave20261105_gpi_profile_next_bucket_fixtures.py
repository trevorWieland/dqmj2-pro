import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_profile_next_bucket_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_profile_next_bucket_build import build

SET,SET2,TABLE,TABLE2,BUCKET,NAME,VALUE,OLD,GLOBAL,STOP,SP=0x2170000,0x2170010,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x2176000,0x21d2504,0x27e0000,0x2701000
PROVIDERS={0x20a8ea0,0x20a8a3c,0x20a929c}


def helpers(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();out={}
    for a in [0x20b3048,0x20b3030]:
        record=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(thumb,size=0x[0-9a-f]+\) addr:0x%08x'%a,x)),None)
        if record is None:raise ValueError('Bucket actual canonical helper entry differs')
        size=int(re.search('size=(0x[0-9a-f]+)',record)[1],0);out[a]=dict(address=hex(a),mode='thumb',bytes=size,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+size]).hexdigest(),sourceCredit=0)
    return out


def vector(a,seed):
    return dict(kind=seed%3,useDefault=seed%2==0,valueNull=seed%4==0,oldNull=seed%4<2,string=[b'',b'a\\b',b'\\\\x/y',b'A\\B\\C',b'normal'][seed%5],raw64=[0,0x8000000000000000,0x3ff8000000000000,0x7ff0000000000000,0x7ff8000012345678,0x7ff0000000000001,0xffffffffffffffff][seed%7])


def run(image,row,body,v,seed,allowed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);cpu.mem_write(SET,struct.pack('<I',TABLE));cpu.mem_write(SET2,struct.pack('<I',TABLE2));cpu.mem_write(GLOBAL,struct.pack('<I',SET2));bucket=bytearray(struct.pack('<IIIQ',NAME,v['kind'],3,0x8877665544332211));struct.pack_into('<I',bucket,12,0 if v['oldNull'] else OLD) if v['kind']==2 else None;cpu.mem_write(BUCKET,bytes(bucket));cpu.mem_write(NAME,b'key\0');raw=bytearray(struct.pack('<Q',v['raw64'])+bytes([0x93])*56)
    if a==0x20b2fc0:raw[:len(v['string'])+1]=v['string']+b'\0'
    cpu.mem_write(VALUE,bytes(raw));cpu.mem_write(OLD,b'old\0');setptr=0 if v['useDefault'] else SET;value=0 if v['valueNull'] else VALUE;args=[setptr,NAME,v['kind'],value] if a==0x20b2ce8 else [VALUE] if a==0x20b2fc0 else [BUCKET,value] if a==0x20b2fe4 else [setptr,NAME] if a==0x20b3048 else [setptr,NAME,VALUE];initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:len(args)]=args;initial[-2:]=[SP,STOP|1]
    if a==0x20b2fe4 and v['kind']!=2:initial[1]=VALUE
    expected_bucket=bytearray(bucket);expected_raw=bytearray(raw);expected=None
    if a==0x20b2ce8:expected=dict(kind='provider',address=hex(0x20a8ea0))
    elif a==0x20b2fc0:expected=dict(kind='return',value=VALUE);expected_raw[:len(v['string'])]=v['string'].replace(b'\\',b'/')
    elif a==0x20b2fe4:
        if v['kind'] in [0,1]:
            width=4 if v['kind']==0 else 8;expected_bucket[12:12+width]=raw[:width];expected=dict(kind='return',value=BUCKET+12)
        elif not v['oldNull']:expected=dict(kind='provider',address=hex(0x20a929c))
        elif v['valueNull']:expected=dict(kind='return',value=0)
        else:expected=dict(kind='provider',address=hex(0x20a8ea0))
    else:expected=dict(kind='provider',address=hex(0x20a8a3c))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];calls=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Bucket actual return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in PROVIDERS:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Bucket original provider mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];observed=dict(kind='provider',address=hex(at))
            if at==0x20a8ea0:interface=regs[0]==(NAME if a==0x20b2ce8 else VALUE)
            elif at==0x20a929c:interface=regs[0]==OLD
            else:interface=regs[0]==(TABLE2 if v['useDefault'] else TABLE) and bytes(machine.mem_read(regs[1],4))==struct.pack('<I',NAME) and SP-0x4000<=regs[1]<SP
            machine.emu_stop();return
        helper=next((r for address,r in allowed.items() if address<=at<address+r['bytes']),None)
        if at in allowed and at!=a:calls.append(at)
        if not a<=at<a+row['bytes'] and helper is None or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('Bucket escaped actual caller/helper/mode',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP or BUCKET<=at and at+size<=BUCKET+20 or VALUE<=at and at+size<=VALUE+64):raise ValueError(('Bucket unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Bucket did not reach actual return/provider')
    guards=bytes(cpu.mem_read(BUCKET,20))==bytes(expected_bucket) and bytes(cpu.mem_read(VALUE,64))==bytes(expected_raw) and bytes(cpu.mem_read(NAME,4))==b'key\0' and bytes(cpu.mem_read(SET,4))==struct.pack('<I',TABLE) and bytes(cpu.mem_read(SET2,4))==struct.pack('<I',TABLE2) and bytes(cpu.mem_read(GLOBAL,4))==struct.pack('<I',SET2)
    return dict(address=row['address'],vector={**v,'string':v['string'].hex()},seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],providerInstructionExecutions=0,allObjectInputAndOutputGuardsPreserved=guards,bucketSha256=hashlib.sha256(bytes(cpu.mem_read(BUCKET,20))).hexdigest(),valueSha256=hashlib.sha256(bytes(cpu.mem_read(VALUE,64))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();allowed=helpers(image);records=[];negative=[]
    variants={0x20b2fc0:("if (*s == '\\\\')","if (*s == '/')"),0x20b2fe4:('pbucket->type == bt_int','pbucket->type != bt_int'),0x20b3048:('if (set == NULL)','if (set != NULL)')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(36):
            v=vector(a,seed);original=run(image,row,native,v,seed,allowed);source=run(image,row,linked,v,seed,allowed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent bucket bit-copy/string/provider model differs',original,source))
            records.append(original)
        if a not in variants:continue
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError(('Whole bucket C did not mutate',row['address'],old))
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong bucket C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,seed)
            if a==0x20b2fc0:v['string']=b'A\\B'
            elif a==0x20b2fe4:v.update(kind=0,raw64=0x12345678,valueNull=False)
            else:v['useDefault']=False
            result=run(image,row,body,v,seed,allowed)
            if result['modelPassed']:raise ValueError('Wrong bucket C did not violate independent type/string/lookup frame model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],actualReturningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] for r in failures),records=failures))
    limits=['Ten ordinary C complete native extents genuinely link with original branch/data/typed ABI proof. Actual primary double remains8bytes; measured MW ARM alignment4 yields20-byte bucket with8-byte union at12. No f32 rewrite. Six compiler helpers map only original specific BLX origins to existing same-program canonical ARM functions under pinned compiler/flags;0helper source credit.','360 paired vector inputs compare actual native/genuine caller instructions to independent raw4/8-byte union copies, slash sanitization, default-set selection and typed allocation/hash lookup/free argument models. DoSet performs bit copies, including NaN/signed-zero patterns, without executing numeric operations. Original bounded DoFind/DoGet helpers execute; remaining allocation/hash/free bodies stop BEFORE first instruction,0synthetic returns.','Three same-extent whole C variants genuinely link and violate48 string/type/default-selection observations. Wrong float4 union layout rejects by compiler geometry. Public AVG/compiler scheduling is preserved in exact native bytes; arithmetic, overflow/zero-division, floating-point result semantics and portable-host evaluation remain unexecuted/uncredited.','No table mutation, allocator/free effects, actual numeric helper execution, network, hardware/device/scenes or complete native Windows behavior proved. Original global pointer/storage authorship/extent and external helper source remain0credit.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalHelperEntries=list(allowed.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
