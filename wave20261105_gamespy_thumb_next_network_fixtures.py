import copy
import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_network_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/network'
WORK=ROOT/'work/w5gt/network/fixtures'
LIST,INPUT,OUTPUT,POINTER,LENGTH,RNG,STOP,SP=0x2170000,0x2172000,0x2173000,0x2174000,0x2174100,0x20dd124,0x27e0000,0x2701000
RAND_BODY='20209fe520009fe5003092e51c109fe5930000e0390080e2030a80e2000082e5200801e01eff2fe124d10d026d4ec641ff7f0000'


def qualify_rng(image,catalog,records):
    row=catalog.get(0x201d5d4);record='from:0x0201d5fc kind:load to:0x020dd124 module:main'
    if row is None or row['mode']!='arm' or row['bytes']!=52 or row['canonicalInventoryRecord']!='func_0201d5d4 kind:function(arm,size=0x34) addr:0x0201d5d4' or image[0x1d5d4:0x1d608].hex()!=RAND_BODY or record not in records:raise ValueError('Original ARM RNG body/literal/canonical entry differs')
    return dict(address='0x201d5d4',mode='arm',bytes=52,nativeSha256=hashlib.sha256(bytes.fromhex(RAND_BODY)).hexdigest(),originalRecord=record,globalState='0x20dd124',stateWidth=4,multiplier='0x41c64e6d',increment=12345,returnShift=16,returnMask=32767,sourceAndStorageCredit=0)


def helper_graph(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();catalog={int(a,0):dict(address=a,mode=m,bytes=int(n,0),canonicalInventoryRecord=line) for line,m,n,a in re.findall(r'^(\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+))$',inventory,re.M)};records=(ROOT/'config/arm9/relocs.txt').read_text().splitlines();proof=qualify_rng(image,catalog,records);negative=[]
    for label,offset in [('instruction',0x1d5d4),('state-pointer',0x1d5fc),('multiplier',0x1d600),('mask',0x1d604)]:
        changed=bytearray(image);changed[offset]^=1
        try:qualify_rng(bytes(changed),catalog,records)
        except ValueError as error:negative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Changed original RNG evidence admitted')
    for label,key,value in [('mode','mode','thumb'),('extent','bytes',48),('inventory','canonicalInventoryRecord','func_0201d5d8 kind:function(arm,size=0x30) addr:0x0201d5d8')]:
        wrong=copy.deepcopy(catalog);wrong[0x201d5d4][key]=value
        try:qualify_rng(image,wrong,records)
        except ValueError as error:negative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong original RNG entry admitted')
    try:qualify_rng(image,catalog,[r for r in records if r!=proof['originalRecord']])
    except ValueError as error:negative.append(dict(case='original-load-record',rejected=True,reason=str(error)))
    else:raise ValueError('Missing original RNG load record admitted')
    write_json(LANE/'rng-controls.json',dict(status='passed',proof=proof,negativeCases=negative,sourceAndStorageCredit=0))
    roots=[0x2026350,0x2026144,0x201d5d4,0x20a7260,0x20a75ec,0x20a75b4];selected=set(roots);pending=roots[:]
    while pending:
        a=pending.pop();row=catalog[a]
        for line in records:
            m=re.fullmatch(r'from:(0x[0-9a-f]+) kind:(arm_call|arm_branch|thumb_call|thumb_call_arm) to:(0x[0-9a-f]+) module:main',line)
            if m and a<=int(m[1],0)<a+row['bytes'] and int(m[3],0) in catalog and int(m[3],0) not in selected:selected.add(int(m[3],0));pending.append(int(m[3],0))
    return {a:dict(catalog[a],nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+catalog[a]['bytes']]).hexdigest(),sourceCredit=0) for a in selected}


def step(seed):return (seed*1103515245+12345)&0xffffffff


def setup(a,v):
    slist=bytearray(2012);struct.pack_into('<I',slist,124,0);struct.pack_into('<i',slist,128,7);struct.pack_into('<i',slist,0,v.get('state',3));struct.pack_into('<i',slist,1716,-1);struct.pack_into('<i',slist,1156,12);data=bytes.fromhex(v.get('data',''));regions={LIST:bytes(slist),INPUT:data+b'\0'+bytes(511-len(data)),OUTPUT:bytes([0xcd])*64,POINTER:struct.pack('<I',OUTPUT+v.get('offset',1)),LENGTH:struct.pack('<I',v.get('length',5)),RNG:struct.pack('<I',v.get('seed',1))};expected=dict(regions);contract='void';result=0
    if a==0x20a710c:
        args=[INPUT,v['buckets'],0,0];contract='value';h=0
        for c in data:
            c=c if c<128 else c-256;h=(h*(-1664117991)+(c+32 if 65<=c<=90 else c))&0xffffffff
        result=h%v['buckets']
    elif a in (0x20a7260,0x20a728c):
        args=[POINTER,v['value']&0xffffffff,LENGTH,0];out=bytearray(regions[OUTPUT]);out[v.get('offset',1):v.get('offset',1)+4]=struct.pack('<I',v['value']&0xffffffff);expected[OUTPUT]=bytes(out);expected[POINTER]=struct.pack('<I',OUTPUT+v.get('offset',1)+4);expected[LENGTH]=struct.pack('<I',v.get('length',5)+4)
    elif a==0x20a72f4:
        args=[LIST,0,0,0];contract='challenge';state=v['seed']
        for i in range(8):state=step(state)
        expected[RNG]=struct.pack('<I',state)
    elif a==0x20a75b4:args=[LIST,0,0,0]
    elif a==0x20a762c:
        args=[LIST,0,0,0];struct.pack_into('<i',slist,0,1);struct.pack_into('<i',slist,128,0);struct.pack_into('<i',slist,1156,-1);expected[LIST]=bytes(slist)
    else:raise ValueError('Unexecuted socket/DNS connect path')
    return regions,expected,args,contract,result&0xffffffff


def run(image,row,body,v,seed,helpers):
    a=int(row['address'],0);regions,expected,args,contract,result=setup(a,v);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    for at,data in regions.items():cpu.mem_write(at,data)
    initial=[(0x55660000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=args;initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    entries={a:0 for a in helpers};pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if at in entries and not (at==a and not pcs):entries[at]+=1
        mode='thumb' if a<=at<a+row['bytes'] else next((r['mode'] for start,r in helpers.items() if start<=at<start+r['bytes']),None)
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError(('Network utility graph/mode escape',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        allowed=SP-0x4000<=at and at+size<=SP
        if a in (0x20a7260,0x20a728c) and ((OUTPUT<=at and at+size<=OUTPUT+64) or (at in [POINTER,LENGTH] and size==4)):allowed=True
        if a==0x20a72f4 and ((LIST+116<=at and at+size<=LIST+124) or (at==RNG and size==4)):allowed=True
        if a in (0x20a75b4,0x20a762c) and size==4 and at in [LIST,LIST+124,LIST+128,LIST+1716,LIST+1156,LIST+1152]:allowed=True
        if not allowed:raise ValueError(('Network utility escaped measured writes',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Network utility return/callee-saved ABI differs')
    actual={a:bytes(cpu.mem_read(a,len(value))) for a,value in regions.items()};correct=contract!='value' or regs[0]==result
    if contract=='challenge':
        chars=actual[LIST][116:124];reference=bytearray(expected[LIST]);reference[116:124]=chars;expected[LIST]=bytes(reference);odd=0;correct=all(33<=c<=126 for c in chars) and chars[0]==33+(((step(v['seed'])>>16)&32767)%93)
        for i in range(1,8):odd=(chars[i-1]&1)^(i&1)^odd^(chars[0]&1)^int(chars[0]<79)^int(chars[i-1]<chars[0]);correct=correct and (chars[i]&1)==odd
    return dict(address=row['address'],vector=v,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,returnContract=contract,returnValue=regs[0],modelPassed=actual==expected and correct,challengeBytes=actual[LIST][116:124].hex() if contract=='challenge' else None,actualOriginalHelperEntries={hex(a):n for a,n in entries.items()},actualOriginalHelperInvocations=sum(entries.values()),initialCallerExcludedFromHelperMetric=True,memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def cases(a):
    if a==0x20a710c:return [dict(data=s.hex(),buckets=n) for s in [b'',b'ABC',b'abc',b'QueryID',b'Hello World',b'\x80\xffA'] for n in [1,2,7,100,0xffffffff]]
    if a in (0x20a7260,0x20a728c):return [dict(value=v,offset=o,length=n) for v in [0,1,-1,0x12345678,-2147483648,2147483647] for o in [0,1,3] for n in [0,5]]
    if a==0x20a72f4:return [dict(seed=s) for i in range(4) for s in [0,1,139,0x12345678,0xffffffff]]
    if a==0x20a75b4:return [dict() for i in range(4)]
    if a==0x20a762c:return [dict(state=s) for i in range(4) for s in [0,1,2,3]]
    return []


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers=helper_graph(image);records=[];negative=[];unsupported=[]
    for row in rows:
        a=int(row['address'],0);vectors=cases(a)
        if not vectors:unsupported.append(dict(address=row['address'],returningVectors=0,reason='Actual DNS/socket connect path unexecuted'));continue
        native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(vectors):
            original=run(image,row,native,v,seed,helpers);source=run(image,row,linked,v,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent network utility model differs',original,source))
            records.append(original)
        mutation={0x20a710c:('MULTIPLIER -1664117991','MULTIPLIER -1664117990',dict(data=b'ABC'.hex(),buckets=97)),0x20a7260:('(*len) += 4','(*len) += 3',dict(value=0x12345678,offset=1,length=5)),0x20a72f4:('buffer[0]<79','buffer[0]<80',dict(seed=139)),0x20a762c:('slist->state = sl_disconnected','slist->state = sl_mainlist',dict(state=2))}
        if a not in mutation:continue
        old,new,v=mutation[a];folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;wrong.write_text(source.read_text());owner=wrong if old in wrong.read_text() else folder/'context.h';text=owner.read_text();changed=text.replace(old,new,1)
        if text==changed:raise ValueError('Whole wrong network utility C did not mutate')
        owner.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong whole network utility C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            result=run(image,row,body,v,seed,helpers)
            if not result['topReturned'] or result['modelPassed']:raise ValueError('Whole wrong network utility C did not actually return model violation')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(failures),records=failures))
    limits=['Actual Thumb callers and original ARM/Thumb helpers execute without substitutes. Independent integer and byte-representation models check signed-char ASCII hashing, unaligned four-byte buffer writes/pointer/length updates and endian-serialization identity. Exact original LCG body/literal qualification plus8 negatives supports seeded challenge range/first-sample/parity and8-step RNG-state invariants.','Empty popular-value cleanup and already-closed socket cleanup execute complete returns and model all fields. Full returns, mode, memory and ABI are checked; initial caller entries are excluded from helper metrics.','Actual DNS/socket connection and sends, nonempty reference/allocator cleanup, negotiated traffic, dynamic callbacks, scenes/hardware/network and full external storage extent/authorship remain unexecuted/uncredited. Helper/global storage proofs carry0 extra source credit.']
    report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),helperBodies=list(helpers.values()),unsupported=unsupported,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
