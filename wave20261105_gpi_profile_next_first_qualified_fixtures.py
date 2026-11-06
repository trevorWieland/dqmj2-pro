import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_profile_next_first_qualified_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_profile_next_first_qualified_build import build

CONN,OBJECT,PROFILE,STATUS,EXTENDED,MAP,USER,DATA,KEY,OUT,KEYOUT,INDEX,TABLE,STOP,SP=0x216f000,0x2170000,0x2171000,0x2172000,0x2172100,0x2173000,0x2173100,0x2174000,0x2176000,0x2177000,0x2178000,0x2179000,0x217a000,0x27e0000,0x2701000
PROVIDERS={0x20a89f0:'thumb',0x20a8ab0:'thumb',0x20a8ca8:'thumb',0x20a8f68:'thumb',0x201f274:'arm'}


def helpers(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();result={}
    for a,mode in [(0x201d69c,'arm'),(0x201d984,'arm'),(0x201d914,'arm'),(0x201d780,'arm'),(0x20b0c00,'thumb'),(0x20b0bd0,'thumb'),(0x20b2ae0,'thumb'),(0x20b2a38,'thumb'),(0x20b2c6c,'thumb'),(0x20acbcc,'thumb')]:
        record=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(%s,size=0x[0-9a-f]+\) addr:0x%08x'%(mode,a),x)),None)
        if record is None:raise ValueError('GPI actual bounded canonical helper differs')
        size=int(re.search(r'size=(0x[0-9a-f]+)',record)[1],0);result[a]=dict(address=hex(a),mode=mode,bytes=size,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+size]).hexdigest(),sourceCredit=0)
    return result


def vector(a,seed):
    if a==0x20b2a4c:return dict(raw=[b'normal',b'\\error\\',b'\\error\\\\errmsg\\bad',b'\\error\\\\errmsg\\bad\\fatal\\',b'\\error\\\\err\\17\\errmsg\\bad',b'x\\error\\'][seed%6],key=b'\\m\\',length=16,flag=seed%2,index=7)
    if a==0x20b2ae0:return dict(raw=[b'\\m\\17\\x\\2',b'\\m\\abcdefghijklmnop',b'|m|alpha|x|beta',b'absent',b'xx\\m\\v\\m\\other'][seed%5],key=b'|m|' if seed%5==2 else b'\\m\\',length=1+seed%17,flag=0,index=7)
    if a==0x20b2b90:return dict(raw=b'zz'+[b'\\key\\value\\next\\v',b'bad',b'\\unterminated',b'\\\\',b'\\'+b'K'*511+b'\\v',b'\\'+b'K'*512+b'\\v',b'\\k\\'+b'V'*511,b'\\k\\'+b'V'*512][seed%8],key=b'\\m\\',length=16,flag=0,index=2)
    return dict(raw=b'P'*(seed%31),key=b'email',length=16,flag=0,index=7 if seed%2==0 else 3)


def keyed(raw,key,length):
    at=raw.find(key)
    if at<0:return None
    value=raw[at+len(key):].split(key[:1])[0].split(b'\0')[0];return value[:length-1]+b'\0'


def key_value(raw,start):
    outkey=bytearray([0xc3]*512);outval=bytearray([0xb6]*512);data=raw[start:];error=False;index=start
    if not data.startswith(b'\\'):return outkey,outval,index,True
    tail=data[1:];delimiter=tail.find(b'\\');key=tail if delimiter<0 else tail[:delimiter];take=min(511,len(key));outkey[:take]=key[:take]
    if delimiter<0 or len(key)>511:return outkey,outval,index,True
    outkey[len(key)]=0;value=tail[delimiter+1:].split(b'\\')[0];take=min(511,len(value));outval[:take]=value[:take]
    if len(value)>511:return outkey,outval,index,True
    outval[len(value)]=0;index+=len(key)+len(value)+2;return outkey,outval,index,False


def run(image,row,body,v,seed,allowed):
    a=int(row['address'],0);raw=v['raw'];cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);obj=bytearray([0xa7]*0x5d8);obj[0x1a8:0x1f0]=bytes(72);struct.pack_into('<I',obj,0x5b8,0x2468);struct.pack_into('<I',obj,0x5bc,0);struct.pack_into('<I',obj,0x5c8,TABLE);cpu.mem_write(OBJECT,bytes(obj));cpu.mem_write(CONN,struct.pack('<I',OBJECT));profile=bytearray([0x73]*44);struct.pack_into('<II',profile,8,STATUS,EXTENDED if seed%3==0 else 0);cpu.mem_write(PROFILE,bytes(profile));cpu.mem_write(STATUS,struct.pack('<I',7)+bytes(24));cpu.mem_write(EXTENDED,struct.pack('<I',3)+bytes(56));mapdata=struct.pack('<III',CONN,0x20b0c01,USER);cpu.mem_write(MAP,mapdata);userdata=bytearray(struct.pack('<II',v['index'],0xdeadbeef));cpu.mem_write(USER,bytes(userdata));payload=raw+b'\0';cpu.mem_write(DATA,payload);cpu.mem_write(KEY,v['key']+b'\0');out=bytearray([0xb6]*512);outkey=bytearray([0xc3]*512);cpu.mem_write(OUT,bytes(out));cpu.mem_write(KEYOUT,bytes(outkey));cpu.mem_write(INDEX,struct.pack('<I',v['index']));args={0x20b0b48:[CONN,PROFILE],0x20b0b90:[CONN,DATA,KEY,OUT],0x20b0bbc:[PROFILE,MAP],0x20b0bd0:[CONN,0x20b0c01,USER],0x20b0c2c:[CONN,v['index']],0x20b2a4c:[CONN,DATA,v['flag']],0x20b2ae0:[DATA,KEY,OUT,v['length']],0x20b2b24:[CONN,77,INDEX],0x20b2b90:[CONN,DATA,INDEX,KEYOUT,OUT],0x20b2c98:[DATA,OUT]}[a];initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):
        if i<4:initial[i]=arg&0xffffffff
        else:cpu.mem_write(SP+4*(i-4),struct.pack('<I',arg&0xffffffff))
    expected_obj=bytearray(obj);expected_out=bytearray(out);expected_key=bytearray(outkey);expected_user=bytearray(userdata);expected_index=v['index'];expected=None
    if a==0x20b0b48:expected=dict(kind='provider',address=hex(0x20a89f0))
    elif a in [0x20b0b90,0x20b0bd0,0x20b0c2c]:expected=dict(kind='provider',address=hex(0x20a8ab0))
    elif a==0x20b0bbc:
        match=v['index']==7 or seed%3==0 and v['index']==3;expected=dict(kind='return',value=0 if match else 1)
        if match:struct.pack_into('<I',expected_user,4,PROFILE)
    elif a==0x20b2ae0:
        value=keyed(raw,v['key'],v['length']);expected=dict(kind='return',value=int(value is not None))
        if value is not None:expected_out[:len(value)]=value
    elif a==0x20b2a4c:
        expected=dict(kind='return',value=0)
        if raw.startswith(b'\\error\\'):
            code=keyed(raw,b'\\err\\',16)
            if code is not None:expected=dict(kind='provider',address=hex(0x201f274))
            else:
                message=keyed(raw,b'\\errmsg\\',256);message=b'\0' if message is None else message;expected_obj[:len(message)]=message;expected=dict(kind='return',value=1)
                if v['flag'] and b'\\fatal\\' in raw:struct.pack_into('<I',expected_obj,0x5bc,1)
    elif a==0x20b2b24:expected=dict(kind='provider',address=hex(0x20a8ca8))
    elif a==0x20b2c98:expected=dict(kind='provider',address=hex(0x20a8f68))
    else:
        expected_key,expected_out,expected_index,error=key_value(raw,v['index']);expected=dict(kind='return',value=3 if error else 0)
        if error:expected_obj[:256]=b'Parse Error.'.ljust(255,b'\0')+b'\0';struct.pack_into('<II',expected_obj,0x5b8,1,1)
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];calls=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('GPI actual caller return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in PROVIDERS:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(PROVIDERS[at]=='thumb'):raise ValueError('GPI original provider target mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];observed=dict(kind='provider',address=hex(at))
            if at==0x20a89f0:interface=regs[:2]==[TABLE,PROFILE]
            elif at==0x20a8ab0:
                frame=struct.unpack('<III',bytes(machine.mem_read(regs[2],12)));interface=regs[:2]==[TABLE,0x20b0bbd] and frame[0]==CONN
                if a==0x20b0b90:interface=interface and frame[1]==0x20b0b5d and bytes(machine.mem_read(frame[2],16))==struct.pack('<IIII',DATA,KEY,OUT,0)
                elif a==0x20b0c2c:interface=interface and frame[1]==0x20b0c01 and bytes(machine.mem_read(frame[2],8))==struct.pack('<II',v['index'],0)
                else:interface=interface and frame[1:]==(0x20b0c01,USER)
            elif at==0x20a8ca8:interface=regs[:2]==[77,0] and regs[2]!=regs[3] and bytes(machine.mem_read(regs[2],4))==bytes(4) and bytes(machine.mem_read(regs[3],4))==bytes(4)
            elif at==0x20a8f68:interface=regs[0]==0x79707367
            else:interface=bytes(machine.mem_read(regs[0],3))==b'17\0' and SP-0x4000<=regs[0]<SP
            machine.emu_stop();return
        helper=next((r for address,r in allowed.items() if address<=at<address+r['bytes']),None)
        if at in allowed and at!=a:calls.append(at)
        mode='thumb' if a<=at<a+row['bytes'] else helper['mode'] if helper else None
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError(('GPI escaped original bounded caller/helper/mode',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP+4*max(0,len(args)-4) or OBJECT<=at and at+size<=OBJECT+256 or OBJECT+0x5b8<=at and at+size<=OBJECT+0x5c0 or OUT<=at and at+size<=OUT+512 or KEYOUT<=at and at+size<=KEYOUT+512 or INDEX<=at and at+size<=INDEX+4 or USER<=at and at+size<=USER+8):raise ValueError(('GPI unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('GPI caller did not reach actual return/provider boundary')
    guards=bytes(cpu.mem_read(OBJECT,len(obj)))==bytes(expected_obj) and bytes(cpu.mem_read(OUT,512))==bytes(expected_out) and bytes(cpu.mem_read(KEYOUT,512))==bytes(expected_key) and bytes(cpu.mem_read(INDEX,4))==struct.pack('<I',expected_index) and bytes(cpu.mem_read(USER,8))==bytes(expected_user) and bytes(cpu.mem_read(PROFILE,44))==bytes(profile) and bytes(cpu.mem_read(DATA,len(payload)))==payload and bytes(cpu.mem_read(MAP,12))==mapdata
    return dict(address=row['address'],vector={**v,'raw':raw.hex(),'key':v['key'].hex()},seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and interface and guards,providerInterfaceModelPassed=interface,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],providerInstructionExecutions=0,allObjectInputAndOutputGuardsPreserved=guards,outputSha256=hashlib.sha256(bytes(cpu.mem_read(OUT,512))+bytes(cpu.mem_read(KEYOUT,512))).hexdigest(),objectSha256=hashlib.sha256(bytes(cpu.mem_read(OBJECT,len(obj)))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();allowed=helpers(image);records=[];negative=[]
    variants={0x20b2ae0:('if(start == NULL)','if(start != NULL)'),0x20b2b90:("if(*buffer++ != '\\\\')","if(*buffer++ == '\\\\')"),0x20b2c98:('Util_RandSeed((unsigned long)GP_XOR_SEED)','Util_RandSeed((unsigned long)(GP_XOR_SEED+1))')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(32):
            v=vector(a,seed);original=run(image,row,native,v,seed,allowed);source=run(image,row,linked,v,seed,allowed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent GPI key/field/frame model differs',original,source))
            records.append(original)
        if a not in variants:continue
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError(('Whole GPI C did not mutate',row['address'],old))
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong GPI C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,0)
            if a==0x20b2ae0:v['length']=16
            result=run(image,row,body,v,seed,allowed)
            if result['modelPassed']:raise ValueError('Wrong GPI C did not violate independent field/key/frame model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],actualReturningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] for r in failures),records=failures))
    limits=['Ten ordinary C complete native extents genuinely link; actual original tagged Thumb tail-call/map callback words retain canonical same-program entries/modes and measured typed frames. No callee-source/object-storage or invented entry credit.','320 vectors compare native/genuine compiled callers to independent delimiter/key truncation,512-byte key/value boundary/error/index, profile buddy-selection/map frame, error-prefix/fatal flag and fixed-XOR-seed input models. Existing bounded original RAM/string/profile/error helper bodies execute; source callers and all helpers preserve actual native instructions/modes.','Table removal/safe traversal, socket select, random seed and integer-conversion provider bodies stop BEFORE their first instruction. No provider return is synthesized; no hash traversal mutation, socket/random/XOR/Base64/network/hardware result behavior claimed. Callback fixture inputs use only canonical tagged Thumb targets.','Three complete same-extent ordinary C variants genuinely link and violate48 key/delimiter/seed observations. Wrong profile-field layout rejects. Full game/device/native Windows execution remains unproven.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalHelperEntries=list(allowed.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
