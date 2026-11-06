import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_browser_query_next_engine_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/browser-query-next/engine'
WORK=ROOT/'work/w5bq/engine/fixtures'
ENGINE,SERVER,FIFO,NODES,DATA,KEY,VALUE,STOP,SP=0x2170000,0x2172000,0x2174000,0x2175000,0x2178000,0x217a000,0x217b000,0x27e0000,0x2701000
HELPERS={0x20a5840:('thumb',30),0x20a5860:('thumb',22),0x20a5878:('thumb',28),0x20a58d0:('thumb',10),0x20a8ef0:('thumb',2),0x201d984:('arm',108)}
BOUNDARIES={0x20a5a74:(0x20a8b5c,'thumb'),0x20a5cb0:(0x20a6180,'thumb'),0x20a5d1c:(0x20a8d88,'thumb'),0x20a5e14:(0x20a8ef8,'thumb'),0x20a5f98:(0x20a6f34,'thumb')}


def original_entries(image):
    entries={};symbols=(ROOT/'config/arm9/symbols.txt').read_text().splitlines()
    for a,(mode,size) in HELPERS.items():
        record=next((x for x in symbols if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,size,a),x)),None)
        if record is None:raise ValueError('Original query helper entry/boundary absent')
        entries[a]=dict(address=a,mode=mode,bytes=size,canonicalRecord=record,targetSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+size]).hexdigest(),sourceCredit=0)
    for a,(target,mode) in BOUNDARIES.items():
        if not any(re.fullmatch(r'\S+ kind:function\(%s,size=0x[0-9a-f]+\) addr:0x%08x'%(mode,target),x) for x in symbols):raise ValueError('Original query boundary canonical mode/entry absent')
    return entries


def setup(v):
    engine=bytearray([0xa5])*76;server=bytearray([0x5a])*44;nodes={NODES+i*64:bytearray([0x70+i])*44 for i in range(v.get('nodes',0))};chain=list(nodes)
    for i,p in enumerate(chain):struct.pack_into('<I',nodes[p],36,chain[i+1] if i+1<len(chain) else 0)
    struct.pack_into('<ii',engine,0,v.get('version',1),v.get('max',0));struct.pack_into('<III',engine,8,0,0,v.get('queryCount',0));struct.pack_into('<III',engine,20,chain[0] if chain else 0,chain[-1] if chain else 0,len(chain));struct.pack_into('<ii',engine,32,v.get('socket',7),v.get('icmpSocketValue',11));struct.pack_into('<I',engine,64,v.get('keys',0));server[20]=v.get('state',0);server[40]=0xcc;struct.pack_into('<I',server,32,0x12345678);struct.pack_into('<I',server,36,0x55555555)
    fifo=struct.pack('<III',chain[0] if chain else 0,chain[-1] if chain else 0,len(chain));return engine,server,nodes,fifo,chain


def run(image,row,body,v,seed,entries):
    a=int(row['address'],0);partial=a in BOUNDARIES and not(a==0x20a5a74 and not v.get('lan',0) and v.get('available',0)!=1);target,mode=BOUNDARIES.get(a,(0,None));cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);engine,server,nodes,fifo,chain=setup(v);regions={ENGINE:bytes(engine),SERVER:bytes(server),FIFO:fifo,**{p:bytes(data) for p,data in nodes.items()}};expected=dict(regions)
    payload=bytes.fromhex(v.get('data','01'))+bytes([0xcc])*64;key=b'hostname\0';value=b'value\0';cpu.mem_write(DATA,payload);cpu.mem_write(KEY,key);cpu.mem_write(VALUE,value);cpu.mem_write(0x21d23ec,struct.pack('<I',v.get('available',0)))
    for p,data in regions.items():cpu.mem_write(p,data)
    initial=[(0x55bb0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    if a==0x20a5894:
        wanted=chain[v['remove']] if 0<=v['remove']<len(chain) else SERVER;initial[:2]=[FIFO,wanted];remaining=[p for p in chain if p!=wanted]
        if len(remaining)!=len(chain):
            expected[FIFO]=struct.pack('<III',remaining[0] if remaining else 0,remaining[-1] if remaining else 0,len(remaining))
            for i,p in enumerate(remaining):changed=bytearray(expected[p]);struct.pack_into('<I',changed,36,remaining[i+1] if i+1<len(remaining) else 0);expected[p]=bytes(changed)
        result_expected=int(len(remaining)!=len(chain))
    elif a==0x20a5a74:
        initial[:4]=[ENGINE,v.get('max',3),v.get('version',1),v.get('lan',0)];cpu.mem_write(SP,struct.pack('<II',0x217e001,0x217d000))
        if partial:
            changed=bytearray(engine);struct.pack_into('<ii',changed,0,v.get('version',1),v.get('max',3));struct.pack_into('<I',changed,40,0);struct.pack_into('<III',changed,64,0,0x217e001,0x217d000);expected[ENGINE]=bytes(changed)
    elif a==0x20a5afc:
        initial[:4]=[ENGINE,SERVER,v.get('front',0),v['type']];cpu.mem_write(SP,struct.pack('<I',v.get('challenge',0)));changed=bytearray(server);changed[20]=server[20]&0x43;changed[40]=0;struct.pack_into('<I',changed,32,0)
        if v['type'] in (0,1):
            changed[20]|=(4 if v['type']==0 else 8)|(128 if v.get('challenge',0) else 0);queued=[SERVER,*chain] if v.get('front',0) else [*chain,SERVER];e=bytearray(engine);struct.pack_into('<III',e,20,queued[0],queued[-1],len(queued));expected[ENGINE]=bytes(e)
            for i,p in enumerate(queued):data=bytearray(changed if p==SERVER else expected[p]);struct.pack_into('<I',data,36,queued[i+1] if i+1<len(queued) else 0);expected[p]=bytes(data)
            changed=bytearray(expected[SERVER])
        expected[SERVER]=bytes(changed)
    elif a in (0x20a5b74,0x20a5cb0):initial[:4]=[ENGINE,SERVER,DATA,len(bytes.fromhex(v.get('data','01')))]
    elif a==0x20a5d1c:initial[:2]=[ENGINE,v.get('icmp',0)]
    elif a==0x20a5ec8:
        initial[:2]=[ENGINE,v['key']];changed=bytearray(engine)
        if v['keys']<20:changed[44+v['keys']]=v['key'];struct.pack_into('<I',changed,64,v['keys']+1)
        expected[ENGINE]=bytes(changed)
    elif a==0x20a5f98:initial[:3]=[SERVER,KEY,VALUE]
    else:initial[0]=ENGINE
    allowed={a:dict(address=a,mode='thumb',bytes=row['bytes'])}
    if a==0x20a5afc:allowed.update({x:entries[x] for x in (0x20a5840,0x20a5860)})
    if a==0x20a5a74:allowed[0x20a8ef0]=entries[0x20a8ef0]
    if a==0x20a5cb0:allowed[0x201d984]=entries[0x201d984]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value_ in zip(C.REGISTERS,initial):cpu.reg_write(reg,value_)
    pcs=[];calls=[];returned=False;capture=None;root_entered=False
    def code(machine,at,size,user):
        nonlocal returned,capture,root_entered
        if partial and at==target:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError('Query boundary CPU entry mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];capture=dict(target=hex(target),mode=mode,registers=regs[:4],callerSp=hex(regs[13]),callerLr=hex(regs[14]));machine.emu_stop();return
        if at==STOP:
            if partial:raise ValueError('Expected partial query caller returned before original boundary')
            returned=True;machine.emu_stop();return
        entry=next((r for start,r in allowed.items() if start<=at<start+r['bytes']),None)
        if entry is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(entry['mode']=='thumb'):raise ValueError(('Query escaped bounded original CPU/mode graph',hex(at)))
        if at==a and not root_entered:root_entered=True
        elif at in allowed:calls.append(at)
        pcs.append(at)
    def write(machine,access,at,size,value_,user):
        legal=SP-0x4000<=at and at+size<=SP
        if a in (0x20a5894,0x20a5afc,0x20a5ec8) or a==0x20a5a74 and partial:legal=legal or any(p<=at and at+size<=p+len(data) for p,data in regions.items())
        if not legal:raise ValueError(('Query wrote outside bounded frame/objects',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=20000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if partial and capture is None:raise ValueError('Original query boundary not reached')
    if not partial and (not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP):raise ValueError('Query full return/callee-saved ABI differs')
    correct=all(bytes(cpu.mem_read(p,len(data)))==expected[p] for p,data in regions.items()) and bytes(cpu.mem_read(DATA,len(payload)))==payload and bytes(cpu.mem_read(KEY,len(key)))==key and bytes(cpu.mem_read(VALUE,len(value)))==value
    if a==0x20a5894:correct=correct and regs[0]==result_expected
    if partial:
        args=capture['registers']
        if a==0x20a5a74:correct=correct and args[:3]==[2,2,0]
        elif a==0x20a5cb0:correct=correct and args[:2]==[SERVER,DATA]
        elif a==0x20a5d1c:correct=correct and args[0]==(0 if v.get('icmp',0) else v.get('socket',7))&0xffffffff
        elif a==0x20a5f98:correct=correct and args[:2]==[0,KEY]
    return dict(address=row['address'],vector=v,seed=seed,topReturned=returned,modelPassed=bool(correct),returnValue=regs[0] if a==0x20a5894 else None,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],initialCallerExcludedFromHelperMetric=True,scope='complete-return' if returned else 'entry-before-original-canonical-boundary',boundaryCallerReturned=False if partial else None,boundaryHelperInstructions=0,capture=capture,objectsSha256=hashlib.sha256(b''.join(cpu.mem_read(p,len(data)) for p,data in sorted(regions.items()))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def vectors(a):
    if a==0x20a5894:return [dict(nodes=n,remove=i) for n in range(7) for i in range(-1,n)]
    if a==0x20a5a74:return [dict(available=v,lan=0) for v in [0,2,3,0xffffffff]]+[dict(available=1,lan=lan,max=n,version=q) for lan in [0,1] for n in [0,3] for q in [0,1]]
    if a==0x20a5afc:return [dict(state=s,type=2) for s in range(256)]+[dict(state=255,type=t,front=f,challenge=c,nodes=n) for t in [0,1] for f in [0,1] for c in [0,1] for n in [0,2]]
    if a==0x20a5b74:return [dict(data=bytes([b,0,0,0,0,0]).hex(),state=s) for b in range(256) if b not in (0,9) for s in [0,255]]
    if a==0x20a5cb0:return [dict(data=s.hex()) for s in [b'\0',b'abc\0',b'\\final\\\0']]
    if a==0x20a5d1c:return [dict(socket=s,icmp=i) for s in [-1,0,7,0x7fffffff] for i in [0,1]]
    if a==0x20a5e14:return [dict(nodes=n) for n in [0,2]]
    if a==0x20a5e68:return [dict(max=m,queryCount=q,nodes=n) for m in range(4) for q in range(5) for n in range(3) if q>=m or n==0]
    if a==0x20a5e90:return [dict(queryCount=0,nodes=n) for n in range(5)]
    if a==0x20a5ec8:return [dict(keys=n,key=k) for n in [0,1,18,19,20,21] for k in range(256)]
    return [dict(state=s) for s in [0,1,255]]


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();entries=original_entries(image);records=[];stops=[];negative=[];boundary_negative=[];changes={0x20a5894:('fifo->count--','fifo->count++'),0x20a5a74:('engine->mypublicip = 0','engine->icmpsock = 0'),0x20a5afc:('STATE_PENDINGQUERYCHALLENGE|STATE_QUERYFAILED','STATE_PENDINGQUERYCHALLENGE|STATE_VALIDPING'),0x20a5d1c:('recvSock = engine->querysock','recvSock = engine->icmpsock'),0x20a5ec8:('engine->numserverkeys < MAX_QUERY_KEYS','engine->numserverkeys < (MAX_QUERY_KEYS-1)')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();cases=vectors(a)
        for seed,v in enumerate(cases):
            original=run(image,row,native,v,seed,entries);source=run(image,row,linked,v,seed,entries)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent query-object/boundary model failed',original,source))
            (records if original['topReturned'] else stops).append(original)
        if a not in changes:continue
        folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=changes[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole query C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong whole query C extent changed',row['address'],bad['compiledBytes'],row['bytes']))
        if a==0x20a5894:v=dict(nodes=3,remove=1)
        elif a==0x20a5a74:v=dict(available=1,lan=0,max=3,version=1)
        elif a==0x20a5afc:v=dict(state=64,type=2)
        elif a==0x20a5d1c:v=dict(socket=7,icmp=0)
        elif a==0x20a5ec8:v=dict(keys=19,key=77)
        else:v=dict(state=0)
        failures=[]
        for seed in range(16):
            result=run(image,row,body,v,seed,entries)
            if result['modelPassed']:raise ValueError('Wrong complete query C did not violate independent model')
            failures.append(result)
        item=dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],modelRejections=len(failures),records=failures);(negative if failures[0]['topReturned'] else boundary_negative).append(item)
    limits=['Actual full native/source returns check independent Python FIFO removal/relink/count models, capacity20 key insertion, measured state-mask/bitmap/challenge clearing, queued-front/rear updates, invalid QR2 header rejection, availability gate, empty think and stalled queue preservation with exact object/argument bounds and callee-saved ABI.','Separate native/source entry-to-canonical-boundary records check initializer fields/socket2,2,0 arguments, GOA reply parser arguments after real original strstr, receive-socket selection, timeout clock entry and NULL-list reference-string arguments. Original no-op/FIFO/string helper bodies execute where declared; no stopped helper instruction or partial caller return executes.','Native UDP protocol0, non-PS3/non-PSP socket-error==-1, no-ICMP receive descriptor0 and existing source-version timeout flags-field behavior remain explicitly measured. Registered-key pointer array is an unbounded minimum4-byte initialized view, with0 external storage extent/authorship credit.','Successful socket traffic, clock/timing returns, key-value allocation/insertion, accepted QR2 parsing through callbacks, dynamic callback targets, devices/scenes and full native game execution remain unexecuted/uncredited. Only selected caller full native extents are source-credit candidates; helper/source storage credit remains0.']
    trace=hashlib.sha256(json.dumps(dict(returns=records,boundaries=stops),sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,boundaryRecords=stops,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records+stops),wholeCNegativeControlsRejected=len(negative),wrongC=negative,boundaryWholeCNegativeControlsRejected=len(boundary_negative),boundaryWrongC=boundary_negative,actualNativeAndSourceEntryToBoundaryStops=2*len(stops),boundaryCallerReturns=0,boundaryHelperInstructions=0,unsupportedSameExtentNegatives=[dict(address='0x20a5f98',nativeBytes=38,wrongCompiledBytes=36,diagnosticRetainedOutsideRuntimeClosure=True,negativeControlCredit=0)],originalHelpers=list(entries.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
