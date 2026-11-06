import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_list_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/list'
WORK=ROOT/'work/w5gt/list/fixtures'
LIST,ARRAY,POINTERS,SERVERS,STOP,SP=0x2170000,0x2171000,0x2171100,0x2172000,0x27e0000,0x2701000


def helper_graph(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();catalog={int(a,0):dict(address=a,mode=m,bytes=int(n,0),canonicalInventoryRecord=line) for line,m,n,a in re.findall(r'^(\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+))$',inventory,re.M)}
    return {a:dict(catalog[a],nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+catalog[a]['bytes']]).hexdigest(),sourceCredit=0) for a in [0x20a8640,0x20a8644,0x20a60b0,0x20a60cc,0x20a6100,0x20a6104]}


def setup(address,v):
    slist=bytearray(2012);array=bytearray(24);struct.pack_into('<I',slist,4,ARRAY);struct.pack_into('<6I',array,0,v.get('count',0),4,4,4,0,POINTERS);slots=[SERVERS+i*256 for i in [0,1,2,0]];regions={LIST:bytes(slist),ARRAY:bytes(array),POINTERS:struct.pack('<4I',*slots)}
    for i in range(3):
        server=bytearray(44);struct.pack_into('<I',server,0,0x11223300+i);struct.pack_into('<H',server,4,[0,0x1234,65535][i]);struct.pack_into('<I',server,36,0xabcd0000+i);regions[SERVERS+i*256]=bytes(server)
    contract='value';result=0
    if address==0x20a6db0:
        target=SERVERS+v['target']*256 if v['target']>=0 else 0x2178000;args=[LIST,target,0,0];result=next((i for i,p in enumerate(slots[:v['count']]) if p==target),-1)
    elif address==0x20a6de4:
        target=v['target'];ip=0x11223300+target if target>=0 else 0xdeadbeef;port=([0,0x1234,65535][target] if target>=0 else 1)+(1 if v.get('wrongPort') else 0);port&=65535;args=[LIST,ip,port,0];result=next((i for i,p in enumerate(slots[:v['count']]) if struct.unpack_from('<I',regions[p],0)[0]==ip and struct.unpack_from('<H',regions[p],4)[0]==port),-1)
    elif address==0x20a6e34:
        head=SERVERS+256 if v['nonempty'] else 0;struct.pack_into('<I',slist,2008,head);regions[LIST]=bytes(slist);args=[LIST,SERVERS,0,0];contract='void'
    elif address==0x20a6ea8:args=[LIST,0,0,0];contract='void'
    else:raise ValueError('Unsupported allocation/refcount/callback graph')
    expected=dict(regions)
    if address==0x20a6e34:
        struct.pack_into('<I',slist,2008,SERVERS);expected[LIST]=bytes(slist);server=bytearray(regions[SERVERS]);struct.pack_into('<I',server,36,head);expected[SERVERS]=bytes(server)
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
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError(('List fixture graph/mode escape',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        allowed=SP-0x4000<=at and at+size<=SP
        if a==0x20a6e34 and size==4 and at in [LIST+2008,SERVERS+36]:allowed=True
        if not allowed:raise ValueError(('List fixture unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('List fixture return/callee-saved ABI differs')
    actual={a:bytes(cpu.mem_read(a,len(value))) for a,value in regions.items()};correct=contract=='void' or regs[0]==result
    return dict(address=row['address'],vector=v,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,returnContract=contract,returnValue=regs[0],modelPassed=actual==expected and correct,actualOriginalHelperEntries={hex(a):n for a,n in entries.items()},actualOriginalHelperInvocations=sum(entries.values()),initialCallerExcludedFromHelperMetric=True,memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def cases(a):
    if a==0x20a6db0:return [dict(count=n,target=t) for n in range(5) for t in [-1,0,1,2]]
    if a==0x20a6de4:return [dict(count=n,target=t,wrongPort=w) for n in range(5) for t in [-1,0,1,2] for w in [False,True]]
    if a==0x20a6e34:return [dict(nonempty=b) for i in range(4) for b in [False,True]]
    if a==0x20a6ea8:return [dict() for i in range(4)]
    return []


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers=helper_graph(image);records=[];negative=[];unsupported=[]
    for row in rows:
        a=int(row['address'],0);vectors=cases(a)
        if not vectors:unsupported.append(dict(address=row['address'],returningVectors=0,reason='Actual allocation, reference-table/refcount or dynamic list callback graph unexecuted'));continue
        native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(vectors):
            original=run(image,row,native,v,seed,helpers);source=run(image,row,linked,v,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent list model differs',original,source))
            records.append(original)
        mutation={0x20a6db0:('findserver ==','findserver !=',dict(count=3,target=1)),0x20a6de4:('== ip','!= ip',dict(count=1,target=0,wrongPort=False)),0x20a6e34:('slist->deadlist == NULL','slist->deadlist != NULL',dict(nonempty=True))}
        if a not in mutation:continue
        old,new,v=mutation[a];folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;wrong.write_text(source.read_text());changed=wrong.read_text().replace(old,new,1)
        if changed==wrong.read_text():raise ValueError('Whole wrong list C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong full list C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            result=run(image,row,body,v,seed,helpers)
            if not result['topReturned'] or result['modelPassed']:raise ValueError('Whole wrong list C did not actually return model violation')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(failures),records=failures))
    limits=['Actual Thumb list callers and real original length/index/getter/next-pointer helpers execute without substitutes; independent models cover first pointer/IP+port match including duplicates,0..4 server arrays, native raw port values, empty/nonempty dead-list insertion and empty dead-list free.','Complete returns, mode, callee-saved ABI and all input/model memory are checked. Initial caller entries are excluded from helper counts. Three full same-extent wrong C units genuinely link and actually return model violations.','Actual append/remove callback dispatch, string-table allocation/reference-counting, nonempty heap frees, malformed/oversized inputs, scenes/network/hardware and complete external storage extent/authorship remain unexecuted/uncredited. Unused structure meanings remain comparative.']
    report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),helperBodies=list(helpers.values()),unsupported=unsupported,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
