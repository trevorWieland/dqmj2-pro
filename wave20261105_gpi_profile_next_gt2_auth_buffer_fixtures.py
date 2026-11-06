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
from wave20261105_gpi_profile_next_gt2_auth_buffer_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_profile_next_gt2_auth_buffer_build import build

BUFF,CHALLENGE,RESPONSE,RECORD,KEY,CLOCK,RAND,STRLEN,VERIFY,STOP,SP=0x2170000,0x2171000,0x2172000,0x2173000,0x20e16e8,0x20a8ef8,0x201d5d4,0x201d69c,0x20b395c,0x27e0000,0x2701000
GET_CHALLENGE,GET_RESPONSE,CHECK,WRITE_BYTE,WRITE_SHORT=0x20b39c4,0x20b3a58,0x20b3b0c,0x20b3b58,0x20b3b64


def helpers(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();out={}
    for a,n,mode,executed in [(STRLEN,28,'arm',True),(VERIFY,104,'thumb',True),(CLOCK,28,'thumb',False),(RAND,52,'arm',False)]:
        record=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,n,a),x)),None)
        if record is None:raise ValueError('Actual canonical auth helper/provider boundary/mode differs')
        out[a]=dict(address=hex(a),mode=mode,bytes=n,canonicalInventoryRecord=record,bodyMayExecute=executed,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+n]).hexdigest(),sourceCredit=0)
    return out


def oddmode(first,previous,i,mode):return (previous&1)^(i&1)^mode^(first&1)^int(first<79)^int(previous<first)


def valid_challenge(seed,first):
    rng=random.Random(0x51b395c+seed);data=bytearray([first]);mode=0
    for i in range(1,32):
        mode=oddmode(first,data[-1],i,mode);data.append((rng.randrange(256)&254)|mode)
    return bytes(data)


def verify(data):
    mode=0
    for i in range(1,32):
        mode=oddmode(data[0],data[i-1],i,mode)
        if data[i]&1!=mode:return 0
    return 1


def vector(a,seed):
    rng=random.Random(0x51b0000+a+seed);first=[0,1,78,79,80,127,128,255][(seed//3)%8];challenge=bytearray(valid_challenge(seed,first))
    if seed%3==1:challenge[1+seed%31]^=1
    elif seed%3==2:challenge=bytearray(rng.randrange(256) for _ in range(32))
    one=bytes(rng.randrange(256) for _ in range(32));two=bytearray(one)
    if seed%4==1:two[0]^=0x55;two[13]^=0x81
    elif seed%4==2:two[1+(seed%11)]^=1
    elif seed%4==3:two=bytearray(rng.randrange(256) for _ in range(32))
    return dict(challenge=bytes(challenge).hex(),response1=one.hex(),response2=bytes(two).hex(),bufferLength=seed%8,value=(0xabcd+seed*997)&0xffff)


def run(image,row,body,v,seed,allowed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);raw=bytes([0x5a])*96;cpu.mem_write(BUFF,raw);challenge=bytes.fromhex(v['challenge']);one=bytes.fromhex(v['response1']);two=bytes.fromhex(v['response2']);cpu.mem_write(CHALLENGE,challenge);cpu.mem_write(RESPONSE,two);record=struct.pack('<III',BUFF,64,v['bufferLength']);cpu.mem_write(RECORD,record);expected_record=record;expected_buffer=raw;key=image[KEY-0x2000000:KEY-0x2000000+33]
    if a==VERIFY:args=[CHALLENGE];expected=dict(kind='return',value=verify(challenge))
    elif a==CHECK:cpu.mem_write(CHALLENGE,one);challenge=one;args=[CHALLENGE,RESPONSE];expected=dict(kind='return',value=int(all(one[i]==two[i] for i in range(32) if i not in [0,13])))
    elif a in [WRITE_BYTE,WRITE_SHORT]:
        value=v['value']&255 if a==WRITE_BYTE else v['value'];args=[RECORD,value];data=bytes([value]) if a==WRITE_BYTE else struct.pack('>H',value);pos=v['bufferLength'];expected_buffer=raw[:pos]+data+raw[pos+len(data):];expected_record=struct.pack('<III',BUFF,64,pos+len(data));expected=dict(kind='return')
    elif a==GET_CHALLENGE:args=[BUFF];expected=dict(kind='provider',address=hex(CLOCK),mode='thumb')
    else:args=[BUFF,CHALLENGE];expected=dict(kind='provider',address=hex(RAND),mode='arm')
    initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):initial[i]=arg&0xffffffff
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];calls=[]
    def code(machine,at,size,user):
        nonlocal observed
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Auth/buffer actual caller return ABI differs')
            observed=dict(kind='return',value=regs[0]) if 'value' in expected else dict(kind='return');machine.emu_stop();return
        if at in [CLOCK,RAND]:
            mode='thumb' if machine.reg_read(ar.UC_ARM_REG_CPSR)&32 else 'arm';observed=dict(kind='provider',address=hex(at),mode=mode);machine.emu_stop();return
        helper=next((r for address,r in allowed.items() if r['bodyMayExecute'] and address<=at<address+r['bytes']),None)
        if at in allowed and at!=a:calls.append(at)
        wanted='thumb' if a<=at<a+row['bytes'] else helper['mode'] if helper else None;mode='thumb' if machine.reg_read(ar.UC_ARM_REG_CPSR)&32 else 'arm'
        if wanted is None or wanted!=mode:raise ValueError(('Auth/buffer escaped original helper/caller/mode',hex(at),mode,wanted))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP) and not(BUFF<=at and at+size<=BUFF+96) and not(RECORD<=at and at+size<=RECORD+12):raise ValueError(('Auth/buffer unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Auth/buffer caller did not reach actual return/provider')
    memory=bytes(cpu.mem_read(BUFF,96))==expected_buffer and bytes(cpu.mem_read(RECORD,12))==expected_record and bytes(cpu.mem_read(CHALLENGE,32))==challenge and bytes(cpu.mem_read(RESPONSE,32))==two and bytes(cpu.mem_read(KEY,33))==key
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and memory,independentMutationModelPassed=memory,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();allowed=helpers(image);records=[];negative=[];variants={VERIFY:None,CHECK:('i != 13','i != 12'),WRITE_SHORT:('s >> 8','s >> 7')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(96):
            v=vector(a,seed);original=run(image,row,native,v,seed,allowed);source=run(image,row,linked,v,seed,allowed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent auth/buffer byte/ABI model differs',original,source))
            records.append(original)
        if a not in variants:continue
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name
        if a==VERIFY:
            changed=source.read_text();header=folder/'context.h';text=header.read_text();new=text.replace('(buffer[0]<79)','(buffer[0]<80)',1)
            if text==new:raise ValueError('Whole auth consumed macro did not mutate')
            header.write_text(new)
        else:
            text=source.read_text();old,new=variants[a];changed=text.replace(old,new,1)
            if changed==text:raise ValueError('Whole auth/buffer wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong auth/buffer C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,seed)
            if a==VERIFY:v['challenge']=valid_challenge(seed,79).hex()
            elif a==CHECK:
                one=bytes.fromhex(v['response1']);two=bytearray(one);two[0]^=1;two[13]^=1;v['response2']=bytes(two).hex()
            else:v['value']=0xabcd
            result=run(image,row,body,v,seed,allowed)
            if result['modelPassed']:raise ValueError('Wrong auth/buffer C accepted independent model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],actualReturningModelRejections=sum(r['topReturned'] for r in failures),records=failures))
    limits=['Six complete ordinary C GT2 challenge/check and buffer-write bodies genuinely match complete original extents, original ARM/Thumb call/data words and measured compiler division helper. Original33-byte challenge-key string stays external with0storage/extent/authorship credit.12-byte buffer offset8len and32-byte challenge/response constants compiler-checked.','576paired entry vectors independently model parity recurrence with valid/invalid/random/high-bit challenges, response equality ignoring positions0/13, and guarded byte/big-endian ushort buffer writes. Actual canonical ARMstrlen28 and ThumbVerifyChallenge104 execute directly in response caller before first rand call.0helpercode doublecredit.','Challenge generation stops BEFORE original clock body; response stops BEFORE original rand body.0synthetic returns,random/clock/I/O/provider-body execution, generated challenge/response output or authentication success claim. Full response arithmetic remains byte-exact yet unexecuted beyond first rand boundary.','Three complete same-extent wrong-C/consumed-macro variants genuinely link and violate48 actual returning independent models.6wrong buffer layouts and strict original namespace/mode/data/addend/opcode negative controls reject. No complete game/native Windows/hardware execution inferred.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalHelperEntries=list(allowed.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
