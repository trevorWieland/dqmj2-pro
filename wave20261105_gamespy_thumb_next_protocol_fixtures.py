import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_protocol_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/protocol'
WORK=ROOT/'work/w5gt/protocol/fixtures'
LIST,SERVER,ARRAY,KEYS,INPUT,IP,PORT,NULLSERVER,STOP,SP=0x2170000,0x2172000,0x2173000,0x2173100,0x2174000,0x2175000,0x2175100,0x21d2368,0x27e0000,0x2701000


def incoming_parameter_store(a,pc,at,size,value,argument,prior,body):
    return a==0x20a7858 and pc==0x20a7862 and at==SP and size==4 and value==argument and prior==struct.pack('<I',argument) and body[:12]==bytes.fromhex('f0b587b000900c98151c0c90')


def parameter_store_controls():
    args=[0x20a7858,0x20a7862,SP,4,1,1,struct.pack('<I',1),bytes.fromhex('f0b587b000900c98151c0c90')];bad=[]
    if not incoming_parameter_store(*args):raise ValueError('Measured same-value incoming parameter spill rejected')
    for name,index,wrong in [('caller',0,0x20a785a),('pc',1,0x20a7864),('slot',2,SP+4),('width',3,2),('value',4,2),('argument',5,2),('prior',6,bytes(4)),('store-instruction',7,args[7][:-1]+b'\x91'),('frame',7,b'\x00\x00'+args[7][2:])]:
        changed=args[:];changed[index]=wrong
        if incoming_parameter_store(*changed):raise ValueError('Invalid incoming parameter write admitted')
        bad.append(dict(case=name,rejected=True))
    return dict(status='passed',nativePrefix=args[7].hex(),frameBytes=48,argumentSlot=5,storeIsSameValue=True,negativeCases=bad,sharedAbiHelpersUnchanged=True)


def helper_graph(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();catalog={int(a,0):dict(address=a,mode=m,bytes=int(n,0),canonicalInventoryRecord=line) for line,m,n,a in re.findall(r'^(\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+))$',inventory,re.M)}
    roots=[0x20a6fa8,0x20a8640,0x20a8644,0x20a6538,0x20a653c,0x20a6544,0x20a6548,0x20a654c,0x20a6ea8,0x201b1bc];selected=set(roots);pending=roots[:];records=(ROOT/'config/arm9/relocs.txt').read_text().splitlines()
    while pending:
        a=pending.pop();row=catalog[a]
        for line in records:
            m=re.fullmatch(r'from:(0x[0-9a-f]+) kind:(arm_call|arm_branch|thumb_call|thumb_call_arm|load) to:(0x[0-9a-f]+) module:main',line)
            if m and a<=int(m[1],0)<a+row['bytes']:
                target=int(m[3],0);target=target&~1 if m[2]=='load' else target
                if target in catalog and target not in selected:selected.add(target);pending.append(target)
    return {a:dict(catalog[a],nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+catalog[a]['bytes']]).hexdigest(),sourceCredit=0) for a in selected}


def full_rules(data,n):
    at=0
    while at<n and data[at]:
        for field in range(2):
            end=data.find(b'\0',at,n)
            if end<0:return 0
            at=end+1
    return int(at<n and data[at]==0)


def keys_present(schema,data,n):
    at=0
    for kind in schema:
        if kind in (1,2):at+=kind
        elif kind==0:
            if at>=n:return 0
            index=data[at];at+=1
            if index==255:
                end=data.find(b'\0',at,n)
                if end<0:return 0
                at=end+1
        else:return 0
        if at>n:return 0
    return 1


def packet(flags):
    value=bytes([flags])+bytes.fromhex('01020304')
    if flags&16:value+=bytes.fromhex('5678')
    if flags&2:value+=bytes.fromhex('11223344')
    if flags&32:value+=bytes.fromhex('1234')
    if flags&8:value+=bytes.fromhex('aabbccdd')
    if flags&128:value+=b'\0'
    return value


def setup(address,v):
    data=bytes.fromhex(v.get('data',''));slist=bytearray(2012);server=bytearray(44);array=bytearray(24);schema=v.get('schema',[]);struct.pack_into('<I',slist,8,ARRAY);struct.pack_into('<6I',array,0,len(schema),4,8,4,0,KEYS);struct.pack_into('<H',slist,1708,0x3412);struct.pack_into('<I',slist,124,INPUT);struct.pack_into('<i',slist,128,v.get('length',len(data)));struct.pack_into('<i',slist,1996,v.get('pstate',5));struct.pack_into('<i',slist,1156,2);struct.pack_into('<i',slist,1152,1);struct.pack_into('<i',slist,0,1)
    server[:20]=bytes.fromhex('0403020134120000bebafecaefbe0000efbeadde');server[20]=v.get('state',0x83)
    regions={LIST:bytes(slist),SERVER:bytes(server),ARRAY:bytes(array),KEYS:b''.join(struct.pack('<II',0,k) for k in schema)+bytes(64-8*len(schema)),INPUT:data+bytes([0xcc])*(512-len(data)),IP:bytes.fromhex('deadbeef'),PORT:bytes.fromhex('efbe'),NULLSERVER:bytes(4)};expected=dict(regions);stack=[];contract='value';result=0
    if address==0x20a7744:args=[INPUT,v['length'],0,0];result=full_rules(data,v['length'])
    elif address==0x20a7794:args=[LIST,INPUT,v['length'],0];result=keys_present(schema,data,v['length'])
    elif address==0x20a7814:
        args=[LIST,INPUT,v['length']&0xffffffff,IP];stack=[PORT];contract='void'
        if v['length']>=5:
            expected[IP]=data[1:5]
            if data[0]&16:
                if v['length']>=7:expected[PORT]=data[5:7]
            else:expected[PORT]=struct.pack('<H',0x3412)
    elif address==0x20a7858:
        flags=v['flags'];data=packet(flags);regions[INPUT]=data+bytes([0xcc])*(512-len(data));expected[INPUT]=regions[INPUT];args=[LIST,SERVER,INPUT,len(data)];stack=[v.get('popular',0)];contract='value';result=len(data);server[21]=flags;server[8:12]=bytes.fromhex('11223344') if flags&2 else bytes(4);server[12:14]=bytes.fromhex('1234') if flags&32 else struct.pack('<H',0x3412)
        if flags&8:server[16:20]=bytes.fromhex('aabbccdd')
        if flags&64:server[20]|=1
        if flags&128:server[20]|=2
        if not flags&192:server[20]&=252
        expected[SERVER]=bytes(server)
    elif address==0x20a7b30:
        args=[LIST,0,0,0]
        if v.get('transition'):
            struct.pack_into('<i',slist,1156,0);struct.pack_into('<i',array,0,0);regions[LIST]=bytes(slist);regions[ARRAY]=bytes(array);expected[ARRAY]=bytes(array);struct.pack_into('<i',slist,1996,4);struct.pack_into('<i',slist,1152,0);struct.pack_into('<i',slist,128,0);expected[LIST]=bytes(slist)
    elif address==0x20a855c:args=[LIST,0,0,0];struct.pack_into('<i',slist,0,v['listState']);regions[LIST]=bytes(slist);expected[LIST]=bytes(slist)
    else:raise ValueError('Cryptographic initialisation/provider path unexecuted')
    return regions,expected,args,stack,contract,result&0xffffffff


def run(image,row,body,v,seed,helpers):
    a=int(row['address'],0);regions,expected,args,stackargs,contract,result=setup(a,v);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    for at,data in regions.items():cpu.mem_write(at,data)
    if stackargs:cpu.mem_write(SP,struct.pack('<'+'I'*len(stackargs),*stackargs))
    initial=[(0x55660000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=args;initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    entries={a:0 for a in helpers};pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if at in entries and not (at==a and not pcs):entries[at]+=1
        mode='thumb' if a<=at<a+row['bytes'] else next((r['mode'] for start,r in helpers.items() if start<=at<start+r['bytes']),None)
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError(('Protocol fixture graph/mode escape',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        allowed=SP-0x4000<=at and at+size<=SP
        if stackargs and incoming_parameter_store(a,machine.reg_read(ar.UC_ARM_REG_PC),at,size,value,stackargs[0],bytes(machine.mem_read(SP,4)),body):allowed=True
        if a==0x20a7814 and ((IP<=at and at+size<=IP+4) or (PORT<=at and at+size<=PORT+2)):allowed=True
        if a==0x20a7858 and SERVER+8<=at and at+size<=SERVER+22:allowed=True
        if a==0x20a7b30 and ((LIST<=at and at+size<=LIST+2012) or (INPUT<=at and at+size<=INPUT+512)):allowed=True
        if not allowed:raise ValueError(('Protocol fixture escaped measured writes',hex(at),size,hex(machine.reg_read(ar.UC_ARM_REG_PC))))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Protocol return/callee-saved ABI differs')
    actual={a:bytes(cpu.mem_read(a,len(value))) for a,value in regions.items()};correct=contract=='void' or regs[0]==result
    return dict(address=row['address'],vector=v,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,returnContract=contract,returnValue=regs[0],modelPassed=actual==expected and correct,actualOriginalHelperEntries={hex(a):n for a,n in entries.items()},actualOriginalHelperInvocations=sum(entries.values()),initialCallerExcludedFromHelperMetric=True,memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def cases(a):
    if a==0x20a7744:return [dict(data=b.hex(),length=n) for b in [b'',b'\0',b'key\0value\0\0',b'key\0value\0',b'k\0v\0x\0y\0\0',b'unterminated'] for n in range(len(b)+1)]
    if a==0x20a7794:return [dict(schema=s,data=b.hex(),length=n) for s in [[],[1],[2],[0],[1,2],[0,1],[0,0],[3]] for b in [b'',b'\0',b'\xffa\0',b'\xffab',b'\x01',b'\xff\0\xfe',b'\0xy'] for n in sorted({0,len(b),max(0,len(b)-1)})]
    if a==0x20a7814:return [dict(data=(bytes([f])+bytes.fromhex('012345671234')).hex(),length=n) for f in [0,16,255] for n in range(-1,9)]
    if a==0x20a7858:return [dict(flags=sum(value for i,value in enumerate([2,8,16,32,64,128]) if mask&(1<<i)),state=s,popular=mask%2) for mask in range(64) for s in [0,1,3,0x84]]
    if a==0x20a7b30:return [dict(pstate=p,data=(b'A'*n).hex(),length=n,schema=[1]) for p in [0,1,2,3,4,5,6,-1] for n in range(5 if p==4 else 6)]+[dict(pstate=2,data='00',length=1,schema=[],transition=True)]
    if a==0x20a855c:return [dict(listState=s) for i in range(4) for s in [1,4,5,-1,0x7fffffff]]
    return []


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers=helper_graph(image);records=[];negative=[];unsupported=[]
    for row in rows:
        a=int(row['address'],0);vectors=cases(a)
        if not vectors:unsupported.append(dict(address=row['address'],returningVectors=0,reason='Complete cryptographic key/state initialization unexecuted'));continue
        native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(vectors):
            original=run(image,row,native,v,seed,helpers);source=run(image,row,linked,v,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent protocol model differs',original,source))
            records.append(original)
        mutation={0x20a7744:('len == 0','len != 0',dict(data='00',length=1)),0x20a7794:('len < 0','len > 0',dict(schema=[1],data='0102',length=2)),0x20a7814:('d[1]=s[1]','d[1]=s[2]',dict(data='00012345671234',length=7)),0x20a7858:('if (flags & PRIVATE_IP_FLAG)','if (!(flags & PRIVATE_IP_FLAG))',dict(flags=2,state=3,popular=0)),0x20a7b30:('slist->pstate = pi_servers','slist->pstate = pi_finished',dict(pstate=2,data='00',length=1,schema=[],transition=True))}
        if a not in mutation:continue
        old,new,v=mutation[a];folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;wrong.write_text(source.read_text());owner=wrong if old in wrong.read_text() else folder/'context.h';text=owner.read_text();changed=text.replace(old,new,1)
        if text==changed:raise ValueError('Whole wrong protocol C did not mutate')
        owner.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong full protocol C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            result=run(image,row,body,v,seed,helpers)
            if not result['topReturned'] or result['modelPassed']:raise ValueError('Whole wrong protocol C did not actually return model violation')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(failures),records=failures))
    limits=['Independent byte/packet-schema models check NUL key/value completeness, typed key-length availability, bounded/truncated IP-port buffers,64 valid server flag combinations with empty key schema/rules, preserved raw network bytes/state bits, incomplete-list parsing/zero-count state transition and disconnected/default think behavior. Actual callers and original helpers execute without substitutes, with full returns, all memory, mode and ABI checks.','Cryptographic initialization, actual key/value insertion/reference allocation, populated server lists, complete negotiated list traffic, callbacks, heap frees, network/devices/scenes and complete external storage extent/authorship remain unexecuted/uncredited. Initial caller entries are excluded from helper metrics; all helpers/global storage receive0 extra source credit.']
    report=dict(status='passed',incomingParameterSpillControls=parameter_store_controls(),records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),helperBodies=list(helpers.values()),unsupported=unsupported,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
