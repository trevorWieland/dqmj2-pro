import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_sorting_build import build
from wave20261105_gamespy_thumb_next_server_fixtures import qualify_string_thunk

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/sorting'
WORK=ROOT/'work/w5gt/sorting/fixtures'
LIST,SERVER1,SERVER2,POINTERS,ARRAY,STATE,STOP,SP=0x2170000,0x2172000,0x2172100,0x2172200,0x2173000,0x21d236c,0x27e0000,0x2701000


def helper_graph(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();catalog={int(a,0):dict(address=a,mode=m,bytes=int(n,0),canonicalInventoryRecord=line) for line,m,n,a in re.findall(r'^(\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+))$',inventory,re.M)}
    roots=[0x20a601c,0x20a6090,0x20a5fe4,0x201d800,0x2023f6c,0x2023ef8,0x20a8750,0x20a69f8,0x20a6b10,0x20a6b5c,0x20a6c10,0x20a6c68];selected=set(roots);pending=roots[:];records=(ROOT/'config/arm9/relocs.txt').read_text().splitlines()
    while pending:
        a=pending.pop();row=catalog[a]
        for line in records:
            m=re.fullmatch(r'from:(0x[0-9a-f]+) kind:(arm_call|arm_branch|thumb_call|thumb_call_arm|load) to:(0x[0-9a-f]+) module:main',line)
            if m and a<=int(m[1],0)<a+row['bytes']:
                target=int(m[3],0);target=target&~1 if m[2]=='load' else target
                if target in catalog and target not in selected:selected.add(target);pending.append(target)
    proof=qualify_string_thunk(0x2023f6c,0x2023ef8,image,catalog,records)
    write_json(LANE/'string-thunk-controls.json',dict(status='passed',proof=proof,sourceAndCalleeCredit=0))
    return {a:dict(catalog[a],nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+catalog[a]['bytes']]).hexdigest(),sourceCredit=0) for a in selected}


def info(key,mode):
    b=bytearray(260);b[:len(key)+1]=key.encode()+b'\0';struct.pack_into('<i',b,256,mode);return bytes(b)


def setup(address,v):
    slist=bytearray(2012);server1=bytearray(44);server2=bytearray(44);array=bytearray(24)
    current=info(v.get('currentKey','missing'),v.get('currentMode',0));previous=info(v.get('previousKey','ping'),v.get('previousMode',0));slist[1176:1436]=current;slist[1436:1696]=previous;struct.pack_into('<i',slist,1696,v['ascending']);struct.pack_into('<I',slist,4,ARRAY);struct.pack_into('<i',array,8,4);struct.pack_into('<I',server1,28,10);struct.pack_into('<I',server2,28,20)
    regions={LIST:bytes(slist),SERVER1:bytes(server1),SERVER2:bytes(server2),POINTERS:struct.pack('<II',SERVER1,SERVER2),ARRAY:bytes(array),STATE:struct.pack('<II',0xa5a5a5a5,LIST)};expected=dict(regions);stack=[];result=0;contract='value'
    previous_result=-10 if v.get('previousMode',0)==0 and v.get('previousKey','ping')=='ping' else 0
    if not v['ascending']:previous_result=-previous_result
    if address==0x20a69f8:args=[SERVER1,SERVER2,0,0];result=previous_result
    elif address in (0x20a6b10,0x20a6b5c,0x20a6c10,0x20a6c68):
        args=[POINTERS,POINTERS+4,0,0];value=-10 if address==0x20a6b10 and v.get('currentKey','missing')=='ping' else 0;result=previous_result if value==0 else value if v['ascending'] else -value
    elif address==0x20a6cc0:
        incoming=info(v['newKey'],v['newMode']);args=[LIST,v['ascending'],*struct.unpack('<II',incoming[:8])];stack=list(struct.unpack('<'+'I'*63,incoming[8:]));contract='void'
        if v.get('previousKey','ping')=='':slist[1436:1696]=incoming
        elif v['newKey']!=v.get('currentKey','missing'):slist[1436:1696]=current
        slist[1176:1436]=incoming;expected[LIST]=bytes(slist)
    else:raise ValueError('Unqualified sorting caller')
    return regions,expected,args,stack,contract,result&0xffffffff


def run(image,row,body,v,seed,helpers):
    address=int(row['address'],0);regions,expected,args,stackargs,contract,result=setup(address,v);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    for at,data in regions.items():cpu.mem_write(at,data)
    if stackargs:cpu.mem_write(SP,struct.pack('<'+'I'*len(stackargs),*stackargs))
    initial=[(0x55660000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=args;initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    entries={a:0 for a in helpers};pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if at in entries and not (at==address and not pcs):entries[at]+=1
        mode='thumb' if address<=at<address+row['bytes'] else next((r['mode'] for a,r in helpers.items() if a<=at<a+r['bytes']),None)
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError(('Sorting fixture graph/mode escape',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        allowed=SP-0x4000<=at and at+size<=SP
        if address==0x20a6cc0 and ((LIST+1176<=at and at+size<=LIST+1700) or (STATE<=at and at+size<=STATE+8)):allowed=True
        if not allowed:raise ValueError(('Sorting fixture escaped measured writes',hex(at),size,hex(machine.reg_read(ar.UC_ARM_REG_PC))))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=200000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Sorting return/callee-saved ABI differs')
    actual={a:bytes(cpu.mem_read(a,len(value))) for a,value in regions.items()};correct=contract=='void' or regs[0]==result
    return dict(address=row['address'],vector=v,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,returnContract=contract,returnValue=regs[0],modelPassed=actual==expected and correct,actualOriginalHelperEntries={hex(a):n for a,n in entries.items()},actualOriginalHelperInvocations=sum(entries.values()),initialCallerExcludedFromHelperMetric=True,memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def cases(address):
    if address==0x20a69f8:return [dict(ascending=a,previousKey=k,previousMode=m) for a in [0,1] for m in range(5) for k in ['ping','missing']]
    if address in (0x20a6b10,0x20a6b5c,0x20a6c10,0x20a6c68):return [dict(ascending=a,currentKey=c,previousKey=p,previousMode=m) for a in [0,1] for c in ['ping','missing'] for p in ['ping','missing'] for m in [0,2]]
    if address==0x20a6cc0:return [dict(ascending=a,currentKey=c,previousKey=p,newKey=n,newMode=m) for a in [0,1] for c in ['old','same'] for p in ['','previous'] for n in ['new','same'] for m in range(4)]
    return []


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers=helper_graph(image);records=[];negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(cases(a)):
            original=run(image,row,native,v,seed,helpers);source=run(image,row,linked,v,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent sorting model differs',original,source))
            records.append(original)
        mutation={0x20a69f8:('!currentSortList->sortascending','currentSortList->sortascending',dict(ascending=1,previousKey='ping',previousMode=0)),0x20a6b10:('diff == 0','diff != 0',dict(ascending=1,currentKey='ping',previousKey='missing',previousMode=0)),0x20a6c10:('diff == 0','diff != 0',dict(ascending=1,currentKey='missing',previousKey='ping',previousMode=0)),0x20a6c68:('diff == 0','diff != 0',dict(ascending=1,currentKey='missing',previousKey='ping',previousMode=0)),0x20a6cc0:('#define currentSortList (native_data_021d236c.active)','#define currentSortList (*(SBServerList **)(void *)&native_data_021d236c)',dict(ascending=1,currentKey='old',previousKey='',newKey='new',newMode=0))}
        if a not in mutation:continue
        old,new,v=mutation[a];folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;wrong.write_text(source.read_text());owner=wrong if old in wrong.read_text() else folder/'context.h';text=owner.read_text();changed=new.join(text.rsplit(old,1)) if a==0x20a69f8 else text.replace(old,new,1)
        if text==changed:raise ValueError('Whole wrong sorting C did not mutate')
        owner.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong complete sorting C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            result=run(image,row,body,v,seed,helpers)
            if not result['topReturned'] or result['modelPassed']:raise ValueError('Whole wrong sorting C did not actually return model violation')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(failures),records=failures))
    report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),helperBodies=list(helpers.values()),unsupported=[],wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),limits=['Actual Thumb callers and real original ARM/Thumb getters, string routines, software floating helpers and zero-element array/qsort graph execute without substitutes. Initial caller entries are excluded from helper counts.','Independent models check bounded ping integer differences, missing/null-table defaults, integer tie-break/direction, zero floating difference, empty-string equivalence,260-byte sort-info selection/copies, ascending flag and mutable global pointer slot at original aggregate+4 while preserving its preceding word.','Nonzero/nan/infinite floating data, numeric parsing, nonempty table lookups/server array sorts, dynamic comparison callbacks, scenes/hardware/network and complete external storage extent/authorship remain unexecuted/uncredited. Existing ARM string thunk is revalidated by exact original body/load record/canonical target, with0 callee source credit.'])
    write_json(LANE/'caller-fixtures.json',report);return report
