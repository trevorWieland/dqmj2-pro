import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_availability_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/availability'
WORK=ROOT/'work/w5gt/availability/fixtures'
INPUT,OUTPUT,ADDR,STOP,SP=0x2170000,0x2172000,0x2174000,0x27e0000,0x2701000
RESULT,GAME,HOST,AC=0x21d23ec,0x21d23f0,0x21d2430,0x21d2470


def helper_entries(image):
    entries={};lines=(ROOT/'config/arm9/symbols.txt').read_text().splitlines()
    for a,mode,size in [(0x201b248,'arm',64),(0x201d6b8,'arm',200),(0x20a8ef0,'thumb',2)]:
        record=next((s for s in lines if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,size,a),s)),None)
        if record is None:raise ValueError('Actual original availability helper boundary absent')
        body=image[a-0x2000000:a-0x2000000+size];entries[a]=dict(address=a,mode=mode,bytes=size,canonicalRecord=record,targetSha256=hashlib.sha256(body).hexdigest(),sourceCredit=0)
    return entries


def run(image,row,body,v,seed,helpers):
    a=int(row['address'],0);partial=a in (0x20a92b0,0x20a932c);target=0x20a8c84 if a==0x20a92b0 else 0x200616c;targetmode='thumb' if a==0x20a92b0 else 'arm'
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    context=bytearray(88);struct.pack_into('<I',context,0,0xffffffff);context[4:12]=struct.pack('<BBHI',8,2,0xabcd,0x11223344);cpu.mem_write(AC,bytes(context));cpu.mem_write(RESULT,struct.pack('<I',v.get('result',0)));cpu.mem_write(HOST,bytes(64));cpu.mem_write(GAME,bytes([0xcc])*64);cpu.mem_write(OUTPUT,struct.pack('<I',0x55667788)+bytes([0xee])*16)
    address=struct.pack('<BBHI',0xee,0xdd,v.get('port',0xabcd)&0xffff,v.get('ip',0x11223344));cpu.mem_write(ADDR,address)
    payload=bytes.fromhex(v.get('data','')) if a==0x20a93cc else (v.get('name','dqmj2pro').encode()+b'\0');inputbytes=payload+bytes([0xcc])*64;cpu.mem_write(INPUT,inputbytes);initial=[(0x55890000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    if a==0x20a92b0:initial[:3]=[INPUT,v['port']&0xffffffff,ADDR]
    elif a==0x20a932c:initial[0]=INPUT
    elif a==0x20a93cc:initial[:4]=[INPUT,v['length'],ADDR,OUTPUT]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    allowed={a:dict(address=a,mode='thumb',bytes=row['bytes'])}
    if a==0x20a93cc:allowed[0x201b248]=helpers[0x201b248]
    if a==0x20a932c:allowed.update({k:helpers[k] for k in (0x201d6b8,0x20a8ef0)})
    pcs=[];calls=[];returned=False;capture=None;root_entered=False
    def code(machine,at,size,user):
        nonlocal returned,capture,root_entered
        if partial and at==target:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(targetmode=='thumb'):raise ValueError('Availability canonical boundary mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];capture=dict(target=hex(target),mode=targetmode,registers=regs[:4],callerSp=hex(regs[13]),callerLr=hex(regs[14]));machine.emu_stop();return
        if at==STOP:
            if partial:raise ValueError('Availability partial caller unexpectedly returned')
            returned=True;machine.emu_stop();return
        entry=next((r for start,r in allowed.items() if start<=at<start+r['bytes']),None)
        if entry is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(entry['mode']=='thumb'):raise ValueError(('Availability escaped exact original CPU/mode graph',hex(at)))
        if at==a and not root_entered:root_entered=True
        elif at in allowed:calls.append(at)
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        legal=SP-0x4000<=at and at+size<=SP
        if a==0x20a92b0:legal=legal or ADDR<=at and at+size<=ADDR+8
        elif a==0x20a932c:legal=legal or GAME<=at and at+size<=GAME+64 or AC<=at and at+size<=AC+4
        elif a==0x20a93cc:legal=legal or OUTPUT<=at and at+size<=OUTPUT+4
        else:legal=legal or RESULT<=at and at+size<=RESULT+4
        if not legal:raise ValueError(('Unexpected availability write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000);regs=[cpu.reg_read(r) for r in C.REGISTERS];correct=bytes(cpu.mem_read(INPUT,len(inputbytes)))==inputbytes
    if partial:
        if capture is None:raise ValueError('Original availability boundary not reached')
        if a==0x20a92b0:
            expected=bytearray(address);expected[1]=2;expected[2:4]=struct.pack('>H',v['port']&0xffff);correct=correct and bytes(cpu.mem_read(ADDR,8))==bytes(expected) and capture['registers'][0]==INPUT and bytes(cpu.mem_read(AC,88))==bytes(context)
        else:
            p=capture['registers'][0];correct=correct and SP-0x4000<=p<=SP-64 and capture['registers'][1:3]==[0x20e03f4,INPUT] and struct.unpack('<I',cpu.mem_read(AC,4))[0]==0xffffffff and bytes(cpu.mem_read(GAME,len(payload)))==payload
    else:
        if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Availability full return/callee-saved ABI differs')
        if a==0x20a93cc:
            valid=v['length']>=7 and v['ip']==0x11223344 and v['port']==0xabcd and payload[:3]==bytes.fromhex('fefd09');word=int.from_bytes(payload[3:7],'big') if valid else 0x55667788;actual=bytes(cpu.mem_read(OUTPUT,20));correct=correct and regs[0]==int(not valid) and actual==struct.pack('<I',word)+bytes([0xee])*16 and bytes(cpu.mem_read(AC,88))==bytes(context)
        else:correct=correct and regs[0]==1 and struct.unpack('<I',cpu.mem_read(RESULT,4))[0]==1 and bytes(cpu.mem_read(AC,88))==bytes(context)
    return dict(address=row['address'],vector=v,seed=seed,topReturned=returned,modelPassed=bool(correct),actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],initialCallerExcludedFromHelperMetric=True,returnValue=regs[0] if returned else None,scope='complete-return' if returned else 'entry-before-original-inet-or-format-helper',stoppedBeforeBoundaryHelperInstruction=partial,boundaryHelperInstructions=0,capture=capture,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers=helper_entries(image);records=[];stops=[];negative=[];boundary_negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        if a==0x20a92b0:vectors=[dict(port=p,repeat=s) for p in [0,1,27900,65535,0x12345678] for s in range(4)];old,new='saddr->sin_family = AF_INET','saddr->sin_family = 3'
        elif a==0x20a932c:vectors=[dict(name=n,repeat=s) for n in ['a','dqmj2pro','x'*30] for s in range(4)];old,new='AC.sock = INVALID_SOCKET','AC.sock = -2'
        elif a==0x20a93cc:
            vectors=[dict(data=((bytes.fromhex('fefd09') if good else bytes.fromhex('fffd09'))+word.to_bytes(4,'big')).hex(),length=n,ip=ip,port=p) for n in [0,6,7,8] for good in [False,True] for ip in [0x11223344,0x11223345] for p in [0xabcd,0xabce] for word in [0,1,2,3,0x80000000,0xffffffff,0x12345678]];old,new='len < 7','len < 8'
        else:vectors=[dict(result=n) for n in [0,1,2,3,0xdeadbeef]];old,new='__GSIACResult = GSIACAvailable','__GSIACResult = GSIACUnavailable'
        for seed,v in enumerate(vectors):
            original=run(image,row,native,v,seed,helpers);source=run(image,row,linked,v,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent availability model differs',original,source))
            (records if original['topReturned'] else stops).append(original)
        folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole availability C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Wrong whole availability C extent changed')
        v=dict(data='fefd0912345678',length=7,ip=0x11223344,port=0xabcd) if a==0x20a93cc else vectors[-1];failures=[]
        for seed in range(16):
            result=run(image,row,body,v,seed,helpers)
            if result['modelPassed']:raise ValueError('Whole wrong availability C did not violate independent model')
            failures.append(result)
        item=dict(address=row['address'],compiledBytes=bad['compiledBytes'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],genuineLink=bad['realLink'],modelRejections=len(failures),records=failures);(negative if failures[0]['topReturned'] else boundary_negative).append(item)
    limits=['Actual complete packet-validator returns independently check length, raw IPv4/port identity,FEFD09 prefix, big-endian disabled-service word and output preservation. Invalid-socket think returns explicitly check available1 result/store. Two same-extent whole wrong C units actually return independent model failures.','Address setup executes only to the original inet_addr entry; startup executes actual canonical strcpy and no-op SocketStartUp then stops before original ARM sprintf. Partial models check8-byte address/port staging, game-name copy, socket-1 and actual format arguments. No inet/DNS/formatter/I/O helper instruction or partial caller return executes; two separate whole wrong C boundary controls fail these models.','Native socket protocol argument is measured0, differing from the comparative source17. Existing canonical BSS2474/2478/2481 field views preserve original literal addresses and ABS32 addend0, without alias/binder exceptions.','Successful DNS/socket traffic, availability replies through live sockets, retries/timing, callbacks/devices/scenes, complete external object storage extent/authorship and full game execution remain unexecuted/uncredited.']
    trace=hashlib.sha256(json.dumps(dict(returns=records,boundaries=stops),sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,boundaryRecords=stops,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records+stops),wholeCNegativeControlsRejected=len(negative),wrongC=negative,boundaryWholeCNegativeControlsRejected=len(boundary_negative),boundaryWrongC=boundary_negative,actualNativeAndSourceEntryToIOStops=2*len(stops),boundaryCallerReturns=0,boundaryHelperInstructions=0,originalHelpers=list(helpers.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
