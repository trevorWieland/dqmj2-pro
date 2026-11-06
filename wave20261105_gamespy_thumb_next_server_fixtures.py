import hashlib
import copy
import json
import random
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_server_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/server'
WORK=ROOT/'work/w5gt/server/fixtures'
SERVER,INPUT,KEY,PAIR1,PAIR2,STATE,STOP,SP=0x2170000,0x2172000,0x2174000,0x2175000,0x2176000,0x21d2360,0x27e0000,0x2701000


def qualify_string_thunk(origin,target,image,catalog,records):
    if (origin,target) not in [(0x2023f60,0x201af90),(0x2023f6c,0x2023ef8)]:raise ValueError('Unmeasured string thunk identity')
    record=f'from:0x{origin+8:08x} kind:load to:0x{target:08x} module:main';raw=image[origin-0x2000000:origin-0x2000000+12]
    if origin not in catalog or catalog[origin]['mode']!='arm' or catalog[origin]['bytes']!=12 or target not in catalog or catalog[target]['mode']!='arm' or raw[:8]!=bytes.fromhex('00c09fe51cff2fe1') or struct.unpack('<I',raw[8:])[0]!=target or record not in records:raise ValueError('Exact original canonical string thunk proof differs')
    return dict(source=hex(origin),target=hex(target),mode='arm',originalRecord=record,originalBytes=raw.hex(),sourceInventory=catalog[origin]['canonicalInventoryRecord'],targetInventory=catalog[target]['canonicalInventoryRecord'],sourceAndCalleeCredit=0)


def helper_graph(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();catalog={int(a,0):dict(address=a,mode=m,bytes=int(n,0),canonicalInventoryRecord=line) for line,m,n,a in re.findall(r'^(\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+))$',inventory,re.M)}
    roots=[0x201d800,0x201d69c,0x2023f60,0x2023f6c,0x2026350,0x20a6140,0x20a6108,0x20a6fa8,0x20a5fe4,0x20a8a3c];selected=set(roots)
    records=(ROOT/'config/arm9/relocs.txt').read_text().splitlines();pending=roots[:5]
    while pending:
        a=pending.pop();row=catalog[a]
        for line in records:
            m=re.fullmatch(r'from:(0x[0-9a-f]+) kind:(arm_call|arm_branch|thumb_call|thumb_call_arm) to:(0x[0-9a-f]+) module:main',line)
            if m and a<=int(m[1],0)<a+row['bytes'] and int(m[3],0) in catalog and int(m[3],0) not in selected:selected.add(int(m[3],0));pending.append(int(m[3],0))
    thunk_proofs=[]
    for origin,target in [(0x2023f60,0x201af90),(0x2023f6c,0x2023ef8)]:
        thunk_proofs.append(qualify_string_thunk(origin,target,image,catalog,records));selected.add(target)
    negative=[]
    for label,origin,target in [('origin',0x2023f64,0x201af90),('entry-interior',0x2023f60,0x201af94)]:
        try:qualify_string_thunk(origin,target,image,catalog,records)
        except ValueError as error:negative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong original string thunk identity admitted')
    for label in ['instruction','literal','callee-mode','source-mode','extent','target-inventory','load-record']:
        wrong_image=bytearray(image);wrong_catalog=copy.deepcopy(catalog);wrong_records=records[:]
        if label=='instruction':wrong_image[0x23f60]^=1
        elif label=='literal':wrong_image[0x23f68]^=4
        elif label=='callee-mode':wrong_catalog[0x201af90]['mode']='thumb'
        elif label=='source-mode':wrong_catalog[0x2023f60]['mode']='thumb'
        elif label=='extent':wrong_catalog[0x2023f60]['bytes']=8
        elif label=='target-inventory':del wrong_catalog[0x201af90]
        else:wrong_records.remove('from:0x02023f68 kind:load to:0x0201af90 module:main')
        try:qualify_string_thunk(0x2023f60,0x201af90,bytes(wrong_image),wrong_catalog,wrong_records)
        except ValueError as error:negative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Changed original string thunk evidence admitted')
    write_json(LANE/'string-thunk-controls.json',dict(status='passed',proofs=thunk_proofs,negativeCases=negative,sourceAndCalleeCredit=0))
    result={}
    for a in selected:
        row=dict(catalog[a]);row['nativeSha256']=hashlib.sha256(image[a-0x2000000:a-0x2000000+row['bytes']]).hexdigest();row['sourceCredit']=0;row['qualifiedStringThunks']=thunk_proofs if a in (0x2023f60,0x2023f6c) else [];result[a]=row
    return result


def token(buffer,start,delimiter):
    at=start
    while buffer[at] and (buffer[at] if buffer[at]<128 else buffer[at]-256)!=delimiter:at+=1
    result=start if at!=start else None
    if buffer[at]:buffer[at]=0;at+=1
    return result,at


def setup(address,v):
    server=bytearray(64);server[40]=v.get('bitmap',0);data=bytearray(bytes.fromhex(v.get('data',''))+bytes(256));data=data[:256];key=v.get('key','ordinary').encode('latin1')+b'\0';key=key+bytes(64-len(key));p1=struct.pack('<II',0 if v.get('null1') else INPUT,0);p2=struct.pack('<II',0 if v.get('null2') else KEY,0);state=INPUT+v.get('offset',0)
    regions={SERVER:bytes(server),INPUT:bytes(data),KEY:key,PAIR1:p1,PAIR2:p2,STATE:struct.pack('<I',state)};expected=dict(regions);contract='value';result=0;high=None
    if address==0x20a6090:args=[0 if v.get('null') else SERVER,KEY,v['low'],v['high']];result=v['low'];high=v['high']
    elif address==0x20a6108:args=[KEY,0,0,0];result=int(v['key'] not in ['queryid','final'])
    elif address==0x20a6140:
        start=v.get('offset',0);args=[INPUT+start if v.get('reset') else 0,v['delimiter']&0xffffffff,0,0];where,newstate=token(data,start,v['delimiter']);result=0 if where is None else INPUT+where;expected[INPUT]=bytes(data);expected[STATE]=struct.pack('<I',INPUT+newstate)
    elif address==0x20a6180:
        args=[SERVER,INPUT,0,0];where,newstate=token(data,1,92)
        while where is not None:
            k=bytes(data[where:]).split(b'\0')[0]
            if k not in [b'queryid',b'final']:raise ValueError('Unqualified key insertion excluded')
            unused,newstate=token(data,newstate,92);where,newstate=token(data,newstate,92)
        expected[INPUT]=bytes(data);expected[STATE]=struct.pack('<I',INPUT+newstate);contract='void'
    elif address==0x20a6300:
        args=[SERVER,INPUT,v['length']&0xffffffff,0];contract='void';raw=bytes.fromhex(v['data']);n=v['length'];end=raw.find(b'\0',0,max(n,0))
        if raw and raw[0] and end>=0 and raw[:end].lower()==b'splitnum' and n-end-1>=1:
            number=raw[end+1];final=bool(number&128);number&=127
            if number<=7:
                server[40]|=((255<<number)&255) if final else (1<<number);expected[SERVER]=bytes(server)
    elif address==0x20a6454:
        args=[INPUT,v['buckets'],0,0];value=0
        for c in bytes(data).split(b'\0')[0]:
            c=c if c<128 else c-256;lower=c+32 if 65<=c<=90 else c;value=(value*(-1664117991)+lower)&0xffffffff
        result=value%v['buckets']
    elif address==0x20a64b8:
        args=[PAIR1,PAIR2,0,0];contract='key-equivalence';result=1 if v.get('null1') or v.get('null2') else int(bytes(data).split(b'\0')[0].lower()!=v['key'].encode('latin1').lower())
    elif address==0x20a6fa8:
        args=[INPUT,v['length']&0xffffffff,0,0];result=-1
        for i in range(max(v['length'],0)):
            if data[i]==0:result=i+1;break
    else:raise ValueError('Unexecuted constructor/provider graph')
    return regions,expected,args,contract,result&0xffffffff,high


def run(image,row,body,v,seed,helpers):
    address=int(row['address'],0);regions,expected,args,contract,result,high=setup(address,v);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    for at,data in regions.items():cpu.mem_write(at,data)
    initial=[(0x55660000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=args;initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    entries={a:0 for a in helpers};pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if at in entries and not (at==address and not pcs):entries[at]+=1
        mode='thumb' if address<=at<address+row['bytes'] else next((r['mode'] for a,r in helpers.items() if a<=at<a+r['bytes']),None)
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError(('Server fixture graph/mode escape',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        allowed=(SP-0x4000<=at and at+size<=SP) or (address in (0x20a6140,0x20a6180) and ((at==STATE and size==4) or (INPUT<=at and at+size<=INPUT+256))) or (address==0x20a6300 and at==SERVER+40 and size==1)
        if not allowed:raise ValueError(('Server fixture escaped measured writes',hex(at),size,hex(machine.reg_read(ar.UC_ARM_REG_PC))))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=100000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Server fixture return/callee-saved ABI differs')
    actual={a:bytes(cpu.mem_read(a,len(v))) for a,v in regions.items()};correct=True if contract=='void' else bool(regs[0])==bool(result) if contract=='key-equivalence' else regs[0]==result and (high is None or regs[1]==high)
    return dict(address=hex(address),vector=v,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,returnContract=contract,modelPassed=actual==expected and correct,returnValue=regs[0],returnHighWord=regs[1] if high is not None else None,memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),actualOriginalHelperEntries={hex(a):n for a,n in entries.items()},actualOriginalHelperInvocations=sum(entries.values()),nativeEntryModesChecked=True,initialCallerExcludedFromHelperMetric=True)


def cases(address):
    if address==0x20a6090:return [dict(null=n,low=a,high=b) for n in [False,True] for a,b in [(0,0),(0,0x3ff00000),(0,0xbff00000),(0x12345678,0x7ff80000)]]
    if address==0x20a6108:return [dict(key=s) for unused in range(4) for s in ['queryid','final','Queryid','ordinary','', 'finalx']]
    if address==0x20a6140:return [dict(data=s.hex(),delimiter=d,reset=r,offset=0) for s in [b'',b'a',b'a\\b',b'\\a',b'a\\',b'a,b,c',b'\xffA',b',,'] for d in [0,44,92,-1] for r in [False,True]]
    if address==0x20a6180:return [dict(data=s.hex()) for unused in range(4) for s in [b'\\',b'\\queryid\\x',b'\\final',b'\\queryid\\x\\final\\z',b'\\final\\x\\queryid\\y']]
    if address==0x20a6300:
        packets=[b'\0',b'wrong\0\0',b'splitnum',b'SPLITNUM\0\x01']+[b'splitnum\0'+bytes([n])+tail for n in [0,1,7,8,127,128,129,135,136,255] for tail in [b'',b'\x03',b'\xff',b'\0\0']]
        return [dict(data=p.hex(),length=len(p),bitmap=b) for p in packets for b in [0,0x11]]
    if address==0x20a6454:return [dict(data=s.hex(),buckets=n) for s in [b'',b'ABC',b'abc',b'QueryID',b'Hello World',b'\x80\xffA'] for n in [1,2,7,100,0xffffffff]]
    if address==0x20a64b8:return [dict(data=s.encode().hex(),key=k,null1=n1,null2=n2) for s,k in [('same','same'),('ABC','abc'),('first','second'),('','')] for n1,n2 in [(False,False),(True,False),(False,True),(True,True)]]
    if address==0x20a6fa8:return [dict(data=s.hex(),length=n) for s in [b'',b'a',b'abc',b'a\0z',bytes([255])*32] for n in [-1,0,1,2,4,32]]
    return []


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers=helper_graph(image);records=[];negative=[];unsupported=[]
    expected_lower=bytes(c+32 if 65<=c<=90 else c for c in range(128))
    if image[0xd8d04:0xd8d04+128]!=expected_lower:raise ValueError('Original lowercase map differs from independent ASCII model')
    for row in rows:
        address=int(row['address'],0);vectors=cases(address)
        if not vectors:unsupported.append(dict(address=row['address'],returningVectors=0,reason='Allocator/constructor callback graph unexecuted'));continue
        native=image[address-0x2000000:address-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(vectors):
            original=run(image,row,native,v,seed,helpers);source=run(image,row,linked,v,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent server model differs',original,source))
            records.append(original)
        mutations={0x20a6108:('== 0','!= 0',dict(key='ordinary')),0x20a6140:('!= delim','== delim',dict(data=b'abc,def'.hex(),delimiter=44,reset=True,offset=0)),0x20a6300:('QR2_SPLITPACKET_MAX 7','QR2_SPLITPACKET_MAX 6',dict(data=(b'splitnum\0\x07').hex(),length=10,bitmap=0)),0x20a6454:('MULTIPLIER -1664117991','MULTIPLIER -1664117990',dict(data=b'ABC'.hex(),buckets=97)),0x20a64b8:('return native_fn_02023f6c','return native_fn_0201d800',dict(data=b'ABC'.hex(),key='abc',null1=False,null2=False)),0x20a6fa8:('return i + 1','return i + 2',dict(data=b'a'.hex(),length=2))}
        if address not in mutations:continue
        old,new,v=mutations[address];folder=WORK/format(address,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;wrong.write_text(source.read_text());owner=wrong if old in wrong.read_text() else folder/'context.h';text=owner.read_text();changed=text.replace(old,new,1)
        if text==changed:raise ValueError(('Whole wrong server C did not mutate',row['address']))
        owner.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong complete server C extent changed',row['address'],bad['compiledBytes']))
        controls=[]
        for seed in range(16):
            result=run(image,row,body,v,seed,helpers)
            if not result['topReturned'] or result['modelPassed']:raise ValueError('Wrong server C did not actually return a model violation')
            controls.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(controls),records=controls))
    report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),helperBodies=list(helpers.values()),unsupported=unsupported,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),limits=['Actual Thumb callers and original ARM/Thumb helpers execute without substitutes, checking code-entry modes, complete caller returns, all allowed memory and callee-saved ABI.','Independent models cover raw64-bit float defaults, invalid-key filtering, stateful delimiter splitting, ignored queryid/final key pairs, split-header validation/bitmap updates/empty or invalid type sections, signed-byte ASCII lowercase hashing, key equivalence and bounded NUL length.','Constructor allocation/callback execution, numeric float conversion, general key insertion/full protocol payloads, malformed pointers, network/devices/scenes and complete external storage/authorship remain unexecuted/uncredited. Canonical callback entries and original Thumb tag words are separately byte/link-qualified and receive0 extra callee source credit.'])
    write_json(LANE/'caller-fixtures.json',report);return report
