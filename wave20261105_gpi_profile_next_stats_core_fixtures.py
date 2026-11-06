import hashlib
import json
import random
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_profile_next_stats_core_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_profile_next_stats_core_build import build

BUFF,KEY,ARRAY,DATA,NAME,INSTANCE,GLOBAL,ENC,ENC1,CALLBACK,STOP,SP=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x21d2514,0x20e15f0,0x20e163c,0x20b2d50,0x27e0000,0x2701000
LENGTH,NTH,DELETE,VALUEKEY,STRNCMP,STATEMENT=0x20a8640,0x20a8644,0x20a8720,0x20b3250,0x201d914,0x20b34f8


def helpers(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();result={}
    for a,n in [(LENGTH,4),(NTH,24),(0x20b326c,86),(0x20b3198,48)]:
        record=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(thumb,size=0x%x\) addr:0x%08x'%(n,a),x)),None)
        if record is None:raise ValueError('Actual canonical request helper boundary/mode differs')
        result[a]=dict(address=hex(a),mode='thumb',bytes=n,originalCanonicalRecord=record,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+n]).hexdigest(),sourceCredit=0)
    if not any(re.fullmatch(r'\S+ kind:function\(thumb,size=0x60\) addr:0x020b2d50',x) for x in inventory.splitlines()):raise ValueError('Fixture callback canonical mode/entry differs')
    return result


def xor(data,key):
    out=bytearray(data);pos=0
    for i in range(len(out)):
        out[i]^=key[pos];pos+=1
        if not key[pos]:pos=0
    return bytes(out)


def vector(a,seed):
    rng=random.Random(0x51b0000+a+seed);data=bytes(rng.randrange(1,256) for _ in range(32));length=[-1,0,1,6,7,16,24,31][seed%8]
    if seed%3==0:data=b'abc\\final\\tail\0rest'+data[20:]
    elif seed%3==1:data=b'\\final\\'+data[7:]
    if a==0x20b35dc:length=seed%7-2
    reqs=[dict(type=i,localid=11+i,profileid=1001+i,pdtype=i%4,pdindex=3+i,instance=INSTANCE+i*4,callback=CALLBACK|1) for i in range(4)]
    if a==0x20b35dc and seed%5==0:reqs[max(0,min(3,length))]['callback']=0
    chosen=reqs[seed%4]
    return dict(data=data.hex(),length=length,key=([b'K\0',b'GameSpy3D\0',bytes([0xff,0x81,0x7f,0])][seed%3]).hex(),arrayNull=seed%7==0,requests=reqs,search=[chosen['type'],chosen['localid'],chosen['profileid']] if seed%3 else [9,999,888],success=seed&1,modified=0x77889900+seed,callbackData=NAME,callbackLength=17+seed)


def run(image,row,body,v,seed,allowed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);raw=bytes.fromhex(v['data']);cpu.mem_write(BUFF,raw+bytes([0x5a])*64);cpu.mem_write(KEY,bytes.fromhex(v['key']));cpu.mem_write(NAME,b'opaque-response-data\0');globals=bytearray([0xa7]*24);struct.pack_into('<I',globals,20,0 if v['arrayNull'] else ARRAY);cpu.mem_write(GLOBAL,bytes(globals));array=bytearray([0xd3]*24);struct.pack_into('<I',array,0,len(v['requests']));struct.pack_into('<I',array,8,28);struct.pack_into('<I',array,20,DATA);cpu.mem_write(ARRAY,bytes(array));reqbytes=b''.join(struct.pack('<7I',r['type'],r['localid'],r['profileid'],r['pdtype'],r['pdindex'],r['instance'],r['callback'] if not v.get('wrongMode') else r['callback']&~1) for r in v['requests']);cpu.mem_write(DATA,reqbytes);cpu.mem_write(ENC,struct.pack('<I',KEY));original_enc=KEY;expected_buffer=raw+bytes([0x5a])*64;expected=None;provider_args=None;provider_stack=[]
    if a==0x20b3198:
        args=[BUFF,v['length']];n=max(0,v['length']);expected_buffer=xor(raw[:n],bytes.fromhex(v['key']))+expected_buffer[n:];expected=dict(kind='return')
    elif a==0x20b326c:
        args=[BUFF,v['length']];position=next((i for i in range(max(0,v['length']-6)) if raw[i:i+7]==b'\\final\\'),None);expected=dict(kind='return',value=0 if position is None else BUFF+position)
    elif a==0x20b32c4:
        args=v['search'];index=next((i for i,r in enumerate(v['requests']) if [r['type'],r['localid'],r['profileid']]==v['search']),-1) if not v['arrayNull'] else -1;expected=dict(kind='return',value=index&0xffffffff)
    elif a==0x20b3588:
        args=[BUFF,v['length']];position=next((i for i in range(max(0,v['length']-6)) if raw[i:i+7]==b'\\final\\'),None)
        if v['length']>0 and position is not None:
            key=image[ENC1-0x2000000:ENC1-0x2000000+16];expected_buffer=xor(raw[:position],key)+expected_buffer[position:];original_enc=ENC1;expected=dict(kind='provider',address=hex(STATEMENT));provider_args=[BUFF,position]
        else:expected=dict(kind='return',value=0)
    elif a in [0x20b331c,0x20b338c,0x20b348c]:
        args=[BUFF,max(0,v['length'])];expected=dict(kind='provider',address=hex(VALUEKEY));provider_args=[BUFF];provider_key={0x20b331c:b'pauthr\0',0x20b338c:b'getpidr\0',0x20b348c:b'setpdr\0'}[a]
    elif a==0x20b34f8:
        args=[BUFF,max(0,v['length'])];expected=dict(kind='provider',address=hex(STRNCMP));provider_args=[BUFF];provider_key=b'\\pauthr\\\0';expected_buffer=expected_buffer[:args[1]]+b'\0'+expected_buffer[args[1]+1:]
    else:
        args=[v['length'],v['success'],v['modified'],NAME,v['callbackLength']];index=v['length']
        if index<0 or index>=len(v['requests']):expected=dict(kind='return')
        else:
            req=v['requests'][index]
            if req['callback']:
                expected=dict(kind='provider',address=hex(CALLBACK));t=req['type'];provider_args=[req['localid'],req['profileid'],req['pdtype'],req['pdindex']] if t in [1,2] else [req['localid'],req['profileid'],v['success'],NAME if t==0 else req['instance']];provider_stack=[v['success'],v['modified'],NAME,v['callbackLength'],req['instance']] if t==1 else [v['success'],v['modified'],req['instance']] if t==2 else [req['instance']] if t==0 else []
            else:expected=dict(kind='provider',address=hex(DELETE));provider_args=[ARRAY,index]
    initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):
        if i<4:initial[i]=arg&0xffffffff
        else:cpu.mem_write(SP+4*(i-4),struct.pack('<I',arg&0xffffffff))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];calls=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Request actual return ABI differs')
            observed=dict(kind='return',value=regs[0]) if 'value' in expected else dict(kind='return');machine.emu_stop();return
        if at in [VALUEKEY,STRNCMP,STATEMENT,DELETE,CALLBACK] and at!=a:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(at!=STRNCMP):raise ValueError('Request actual callback/provider mode differs')
            observed=dict(kind='provider',address=hex(at));regs=[machine.reg_read(r) for r in C.REGISTERS]
            if expected['kind']=='provider':
                interface=regs[:len(provider_args)]==provider_args
                if at in [VALUEKEY,STRNCMP]:interface=interface and bytes(machine.mem_read(regs[1],len(provider_key)))==provider_key and (at!=STRNCMP or regs[2]==8)
                if provider_stack:interface=interface and bytes(machine.mem_read(regs[13],4*len(provider_stack)))==struct.pack('<'+'I'*len(provider_stack),*provider_stack)
            machine.emu_stop();return
        helper=next((r for address,r in allowed.items() if address<=at<address+r['bytes']),None)
        if at in allowed and at!=a:calls.append(at)
        if (not a<=at<a+row['bytes'] and helper is None) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('Request escaped bounded caller/helper/mode',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP+4*max(0,len(args)-4)) and not (BUFF<=at and at+size<=BUFF+len(expected_buffer)) and not (at==ENC and size==4):raise ValueError(('Request unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Request caller did not reach actual return/provider')
    memory=bytes(cpu.mem_read(BUFF,len(expected_buffer)))==expected_buffer and bytes(cpu.mem_read(GLOBAL,24))==bytes(globals) and bytes(cpu.mem_read(ARRAY,24))==bytes(array) and bytes(cpu.mem_read(DATA,len(reqbytes)))==reqbytes and bytes(cpu.mem_read(ENC,4))==struct.pack('<I',original_enc)
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and memory and interface,providerInterfaceModelPassed=interface,independentMemoryModelPassed=memory,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();allowed=helpers(image);records=[];negative=[];mode_negative=[];variants={0x20b3198:('buf[i] ^=','buf[i] |='),0x20b326c:("pos[1] == 'f'","pos[1] == 'g'"),0x20b32c4:('req->profileid == profileid','req->localid == profileid')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(48):
            v=vector(a,seed);original=run(image,row,native,v,seed,allowed);source=run(image,row,linked,v,seed,allowed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent request model differs',original,source))
            records.append(original)
        if a==0x20b35dc:
            v=vector(a,3);v.update(length=1,arrayNull=False,wrongMode=True)
            for label,body in [('native',native),('genuine-source',linked)]:
                try:run(image,row,body,v,3,allowed)
                except ValueError as error:
                    if 'callback/provider mode differs' not in str(error):raise
                    mode_negative.append(dict(version=label,rejectedBeforeTargetBody=True,reason=str(error)))
                else:raise ValueError('Even request callback pointer admitted')
        if a not in variants:continue
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole request wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong request C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,seed);v.update(length=24,arrayNull=False)
            if a==0x20b3198:v.update(data=(bytes([255])*32).hex(),key=b'ABC\0'.hex())
            elif a==0x20b326c:v.update(data=(b'abc\\final\\tail'+bytes(18)).hex())
            else:v['search']=[v['requests'][0]['type'],v['requests'][0]['localid'],v['requests'][0]['profileid']]
            result=run(image,row,body,v,seed,allowed)
            if result['modelPassed']:raise ValueError('Wrong request C independent model accepted')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],actualReturningModelRejections=sum(r['topReturned'] for r in failures),records=failures))
    limits=['Nine complete ordinary C stats coding/search/response callers have genuine exact links. External original coding pointer/string storage and BSS request pointer field20 of minimum24-byte group carry0storage/extent/authorship credit.28-byte server-request source layout and32-bit time/mode/field offsets are compiler-checked.','432 paired entry vectors use independent byte-XOR/final-marker/record-search/argument-frame/mutation models. Actual canonical4-byte array-length and24-byte array-index helpers execute directly against explicitly supplied24-byte array prefix(count0,stride8,data20) and28-byte records. Native FindFinal86/xcode48 execute where called;0helper code doublecredit.','Response key lookup, ARM string compare, statement, array deletion and supplied callback providers stop BEFORE bodies;0synthetic returns. Valid callback cases check all original type0-3 register/stack frames and original BLX mode. Negative indices/out-of-range calls return through actual entry.0authentication/persistence/network/heap/device effects.','Three complete same-extent wrong-C variants genuinely link and violate48 actual returning independent models. Even fixture callback mode rejects before body. These pointer values are supplied runtime input, never claimed original callback storage or callee ABI/source reconstruction. No complete native Windows/game execution is inferred.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,wrongFixturePointerModesRejected=mode_negative,originalHelperEntries=list(allowed.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
