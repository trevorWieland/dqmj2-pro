import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gp_api_next_api_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gp_api_next_api_build import build

CONN,OBJECT,REASON,STATUS,LOCATION,STOP,SP=0x2170000,0x2171000,0x2173000,0x2174000,0x2175000,0x27e0000,0x2702000
AVAILABILITY=0x21d23ec
STRZ,ERROR,STRNCPY,STRCMP=0x20b2a38,0x20b2c88,0x201d780,0x201d800
PROVIDERS={0x20aa894,0x20ac6f4,0x20ac404,0x20aec50,0x20b0a50}


def helpers(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text().splitlines();out={}
    for a,mode,size in [(STRZ,'thumb',20),(ERROR,'thumb',16),(STRNCPY,'arm',80),(STRCMP,'arm',276)]:
        record=next((x for x in inventory if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,size,a),x)),None)
        if record is None:raise ValueError('Actual GP RAM/string helper entry/mode absent')
        out[a]=dict(address=a,mode=mode,bytes=size,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+size]).hexdigest(),sourceCredit=0)
    if image[ERROR-0x2000000+12:ERROR-0x2000000+16]!=struct.pack('<I',STRZ|1):raise ValueError('Original typed error-string tail target changed')
    return out


def clean(raw,n):
    return raw.split(b'\0')[0][:n-1].replace(b'\\',b'/')+bytes(n-len(raw.split(b'\0')[0][:n-1]))


def vectors(a):
    rows=[]
    for i in range(16):
        kind=i%8;rows.append(dict(connection='null' if kind==0 else 'empty' if kind==1 else 'valid',simulation=1 if kind==2 else 0x80000000 if kind==3 else 0,state=4 if kind==4 else 3,reasonNull=kind==5,statusNull=kind==5,locationNull=kind==6,availability=[0,1,2,0xffffffff][i%4],sameStatus=kind==7,reason=(b'a\\b\\c'+bytes([0x80+i])+b'\0').hex(),status=(b'play\\here'+bytes([0x80+i])+b'\0').hex(),location=(b'place\\there'+bytes([0x90+i])+b'\0').hex(),profile=(0x10000+i),info=0x400+i,value=(0xffffffff-i),newStatus=i%6))
    for i,raw in enumerate([b'\0',b'\\\0',bytes([0xff])*1030+b'\0',b'a'*1024+b'\\\0']):
        rows.append(dict(connection='valid',simulation=0,state=3,reasonNull=False,statusNull=False,locationNull=False,availability=1,sameStatus=False,reason=raw.hex(),status=raw.hex(),location=raw.hex(),profile=i,info=i,value=i,newStatus=2))
    return rows


def run(image,row,body,v,seed,allowed_helpers):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x8000,0x9000);cpu.mem_write(SP-0x8000,bytes([0xa5])*0x8000);raws=[bytes.fromhex(v[k]) for k in ['reason','status','location']]
    for at,raw in zip([REASON,STATUS,LOCATION],raws):cpu.mem_write(at,raw+bytes([0xcc])*32)
    state=bytearray([0xa7]*0x5d8);state[:256]=b'old-error\0'+bytes([0x51])*246;struct.pack_into('<I',state,0x108,v['simulation']);struct.pack_into('<I',state,0x1f4,v['state']);struct.pack_into('<I',state,0x198,0x12345678);oldstatus=clean(raws[1],256) if v['sameStatus'] else b'old-status\0'+bytes([0x54])*245;oldlocation=clean(raws[2],256) if v['sameStatus'] else b'old-location\0'+bytes([0x55])*243;state[0x3b8:0x4b8]=oldstatus;state[0x4b8:0x5b8]=oldlocation;struct.pack_into('<I',state,0x23c,v['newStatus'] if v['sameStatus'] else 0xabcdef01);cpu.mem_write(OBJECT,bytes(state));cpu.mem_write(CONN,struct.pack('<I',0 if v['connection']=='empty' else OBJECT));cpu.mem_write(AVAILABILITY,struct.pack('<I',v['availability']));conn=0 if v['connection']=='null' else CONN;rptr=0 if v['reasonNull'] else REASON;sptr=0 if v['statusNull'] else STATUS;lptr=0 if v['locationNull'] else LOCATION;args={0x20a9f2c:[conn,12,34,56],0x20aa1d0:[conn,v['profile'],rptr],0x20aa5f8:[conn,v['newStatus'],sptr,lptr],0x20aa2f8:[conn,v['profile']],0x20aa194:[conn,v['info'],v['value']],0x20aa334:[conn,v['profile']]}[a];initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):initial[i]=arg
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    expected_state=bytearray(state);error_address=None
    if a==0x20a9f2c:expected=dict(kind='return',value=2) if v['availability']!=1 or not conn else dict(kind='provider',address=hex(0x20aa894))
    elif v['connection']!='valid':expected=dict(kind='return',value=2)
    elif v['simulation']:expected=dict(kind='return',value=0)
    elif v['state']==4:error_address=0x20e0440;expected=dict(kind='return',value=2)
    elif a==0x20aa1d0 and not rptr:error_address=0x20e0470;expected=dict(kind='return',value=2)
    elif a==0x20aa5f8 and not sptr:error_address=0x20e04dc;expected=dict(kind='return',value=2)
    elif a==0x20aa5f8 and not lptr:error_address=0x20e04f4;expected=dict(kind='return',value=2)
    elif a==0x20aa5f8 and v['sameStatus']:expected=dict(kind='return',value=0)
    else:expected=dict(kind='provider',address=hex({0x20aa1d0:0x20ac6f4,0x20aa5f8:0x20ac6f4,0x20aa2f8:0x20ac404,0x20aa194:0x20aec50,0x20aa334:0x20b0a50}[a]))
    if error_address is not None:
        raw=image[error_address-0x2000000:].split(b'\0')[0];expected_state[:256]=raw+bytes(256-len(raw))
    if a==0x20aa5f8 and expected['kind']=='provider':struct.pack_into('<I',expected_state,0x23c,v['newStatus']);expected_state[0x3b8:0x4b8]=clean(raws[1],256);expected_state[0x4b8:0x5b8]=clean(raws[2],256)
    observed=None;pcs=[];calls=[];stack_copies=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('GP authentic caller return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in PROVIDERS:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('GP provider stop mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];observed=dict(kind='provider',address=hex(at));interface=regs[0]==conn
            if at==0x20aa894:interface=interface and regs[1:4]==[12,34,56]
            elif at==0x20ac6f4:interface=interface and regs[1]==OBJECT+0x210 and regs[2]==(0x20e0480 if a==0x20aa1d0 else 0x20e050c)
            elif at==0x20ac404:interface=interface and regs[1]==v['profile']
            elif at==0x20aec50:interface=interface and regs[1:3]==[v['info'],v['value']]
            elif at==0x20b0a50:interface=interface and regs[1]==v['profile'] and SP-0x8000<=regs[2]<SP
            machine.emu_stop();return
        if at in allowed_helpers:
            calls.append(at)
            if at==STRZ:
                dst,src,n=[machine.reg_read(r) for r in [ar.UC_ARM_REG_R0,ar.UC_ARM_REG_R1,ar.UC_ARM_REG_R2]]
                if SP-0x8000<=dst<SP:stack_copies.append(dict(dst=dst,src=src,n=n))
        entry=next((r for start,r in allowed_helpers.items() if start<=at<start+r['bytes']),None)
        if a<=at<a+row['bytes']:mode='thumb'
        elif entry:mode=entry['mode']
        else:raise ValueError(('GP escaped actual RAM/string helper graph',hex(at)))
        if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError('GP helper/caller original instruction mode differs')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x8000<=at and at+size<=SP or OBJECT<=at and at+size<=OBJECT+0x5d8):raise ValueError(('GP unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('GP did not reach authentic return/qualified provider boundary')
    private_ok=True
    for slot in stack_copies:
        index={REASON:0,STATUS:1,LOCATION:2}.get(slot['src'])
        if index is None or slot['n']!=(1025 if a==0x20aa1d0 else 256):raise ValueError('GP private string source/extent differs')
        private_ok=private_ok and bytes(cpu.mem_read(slot['dst'],slot['n']))==clean(raws[index],slot['n'])
    guards=bytes(cpu.mem_read(OBJECT,0x5d8))==bytes(expected_state) and all(bytes(cpu.mem_read(at,len(raw)))==raw for at,raw in zip([REASON,STATUS,LOCATION],raws))
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and interface and guards and private_ok,providerInterfaceModelPassed=interface,privateSanitizedStringModelPassed=private_ok,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],stateSha256=hashlib.sha256(bytes(cpu.mem_read(OBJECT,0x5d8))).hexdigest(),inputAndObjectGuardsPreserved=guards,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();allowed=helpers(image);records=[];negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(vectors(a)):
            original=run(image,row,native,v,seed,allowed);source=run(image,row,linked,v,seed,allowed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent GP RAM/string/provider model differs',original,source))
            records.append(original)
        if a==0x20a9f2c:continue
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();changed=text.replace("= '/';","= '!';") if a in [0x20aa1d0,0x20aa5f8] else text.replace('return GP_PARAMETER_ERROR;','return 3;',1)
        if changed==text:raise ValueError('Whole GP C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong GP C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vectors(a)[8].copy();v.update(connection='valid',simulation=0,state=3,reasonNull=False,statusNull=False,locationNull=False,sameStatus=False)
            if a not in [0x20aa1d0,0x20aa5f8]:v['connection']='null'
            result=run(image,row,body,v,seed,allowed)
            if result['modelPassed']:raise ValueError('Wrong GP C did not violate independent state/string model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],returningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] for r in failures),records=failures))
    limits=['Six whole ordinary C GP API extents genuinely link with exact original calls/data loads. The actual consumed context describes a measured minimum GPI connection prefix through profile-list fields, not the complete allocated connection object or storage authorship.','Actual native/source caller execution includes canonical RAM-only error-string tail forwarding,20-byte bounded string helper,80-byte ARM strncpy and276-byte ARM strcmp as applicable. No provider return is synthesized. Valid paths stop BEFORE original GP profile/buffer/constructor providers; no allocation/network/app callback body executes.','Independent byte models validate connection/backend/simulation/error state,1025/256-byte truncation and backslash replacement, unchanged-status early return, measured last-status fields and exact next-provider arguments. Five same-extent whole wrong C units genuinely link and violate80 independent state/sanitization observations; authentic-return and partial failures remain separate.','Later buddy-request/profile mutation, successful GP authentication/buffer delivery, source helper ownership, hardware/full game/native Windows execution remain unproven/uncredited.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalHelperEntries=list(allowed.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
