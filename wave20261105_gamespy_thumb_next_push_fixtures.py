import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_push_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/push'
WORK=ROOT/'work/w5gt/push/fixtures'
LIST,ARRAY,POINTER,SERVER,INPUT,STOP,SP=0x2170000,0x2171000,0x2171100,0x2172000,0x2174000,0x27e0000,0x2701000


def helper_graph(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();catalog={int(a,0):dict(address=a,mode=m,bytes=int(n,0),canonicalInventoryRecord=line) for line,m,n,a in re.findall(r'^(\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+))$',inventory,re.M)}
    roots=[0x20a6fa8,0x20a6de4,0x20a6e9c,0x20a8640,0x20a8644,0x20a60b0,0x20a60cc];selected=set(roots);records=(ROOT/'config/arm9/relocs.txt').read_text().splitlines();pending=roots[:]
    while pending:
        a=pending.pop();row=catalog[a]
        for line in records:
            m=re.fullmatch(r'from:(0x[0-9a-f]+) kind:(arm_call|arm_branch|thumb_call|thumb_call_arm) to:(0x[0-9a-f]+) module:main',line)
            if m and a<=int(m[1],0)<a+row['bytes'] and int(m[3],0) in catalog and int(m[3],0) not in selected:selected.add(int(m[3],0));pending.append(int(m[3],0))
    return {a:dict(catalog[a],nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+catalog[a]['bytes']]).hexdigest(),sourceCredit=0) for a in selected}


def player_model(data,n):
    if n<2:return 4
    at=2
    for i in range(data[1]):
        end=data.find(b'\0',at,n)
        if end<0:return 4
        at=end+1
        if n-at<11:return 4
        at+=10;end=data.find(b'\0',at,n)
        if end<0:return 4
        raise ValueError('Unexecuted actual player callback excluded')
    if data[0]:raise ValueError('Unexecuted final callback excluded')
    return 0


def map_model(data,n,present):
    if n<11:return 4
    if not present:return 0
    at=11
    for i in range(min(data[10],16)):
        if at>=n:break
        end=data.find(b'\0',at,n)
        if end<0:return 4
        at=end+1
    return 0


def run(image,row,body,v,seed,helpers):
    a=int(row['address'],0);data=bytes.fromhex(v['data']);n=v.get('length',len(data));slist=bytearray(2012);array=bytearray(24);server=bytearray(44);server[:4]=bytes.fromhex('01020304');server[4:6]=bytes.fromhex('1234');struct.pack_into('<I',slist,4,ARRAY);struct.pack_into('<6I',array,0,1 if v.get('present') else 0,4,4,4,0,POINTER)
    regions={LIST:bytes(slist),ARRAY:bytes(array),POINTER:struct.pack('<I',SERVER),SERVER:bytes(server),INPUT:data+bytes([0xcc])*(512-len(data))};expected=dict(regions)
    if a==0x20a7e94:result=player_model(data,n)
    elif a==0x20a7fb0:result=map_model(data,n,v['present'])
    elif a==0x20a80a4:
        result=4 if n<6 else 0
        if n>=6 and v.get('present') and data[:6]==server[:6]:raise ValueError('Actual delete callback path excluded')
    elif a==0x20a80f8:
        if n>=5:raise ValueError('Actual server insertion/allocation callback path excluded')
        result=4
    else:raise ValueError('Actual key-list allocation path excluded')
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    for at,raw in regions.items():cpu.mem_write(at,raw)
    initial=[(0x55660000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=[LIST,INPUT,n,0];initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    entries={at:0 for at in helpers};pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if at in entries and not (at==a and not pcs):entries[at]+=1
        mode='thumb' if a<=at<a+row['bytes'] else next((r['mode'] for start,r in helpers.items() if start<=at<start+r['bytes']),None)
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError(('Push parser graph/mode escape',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not SP-0x4000<=at or at+size>SP:raise ValueError(('Push fixture unexpected non-stack write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Push parser return/callee-saved ABI differs')
    actual={at:bytes(cpu.mem_read(at,len(raw))) for at,raw in regions.items()}
    return dict(address=row['address'],vector=v,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,returnValue=regs[0],modelPassed=actual==expected and regs[0]==result,actualOriginalHelperEntries={hex(at):count for at,count in entries.items()},actualOriginalHelperInvocations=sum(entries.values()),initialCallerExcludedFromHelperMetric=True,memorySha256=hashlib.sha256(b''.join(actual[at] for at in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def cases(a):
    if a==0x20a7e94:
        samples=[b'',b'\0',b'\0\0',b'\0\1',b'\1\1',b'\0\1A',b'\0\1A\0'+bytes(10),b'\0\1A\0'+bytes(10)+b'unterminated']
        return [dict(data=s.hex(),length=n) for s in samples for n in range(len(s)+1) if n<=1 or s[:2]!=b'\1\1' or n<2]
    if a==0x20a7fb0:
        samples=[b'',bytes(10)]+[bytes.fromhex('01020304123400000000')+bytes([c])+tail for c in [0,1,2,16,17] for tail in [b'',b'A\0',b'A\0B\0',b'unterminated']]
        return [dict(data=s.hex(),length=n,present=p) for s in samples for n in sorted({0,len(s),max(0,len(s)-1)}) for p in [False,True]]
    if a==0x20a80a4:return [dict(data=b.hex(),length=n,present=False) for b in [bytes(6),bytes.fromhex('010203041234'),bytes(8)] for n in range(len(b)+1)]
    if a==0x20a80f8:return [dict(data=bytes(4).hex(),length=n) for i in range(4) for n in range(5)]
    return []


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers=helper_graph(image);records=[];negative=[];unsupported=[]
    for row in rows:
        a=int(row['address'],0);vectors=cases(a)
        if not vectors:unsupported.append(dict(address=row['address'],returningVectors=0,reason='Actual pushed-key-list allocation/reference/callback path unexecuted'));continue
        native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(vectors):
            original=run(image,row,native,v,seed,helpers);source=run(image,row,linked,v,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent push parser model differs',original,source))
            records.append(original)
        mutation={0x20a7e94:('return sbe_dataerror','return sbe_allocerror',dict(data='00',length=1)),0x20a7fb0:('maplen == -1','maplen != -1',dict(data=(bytes.fromhex('01020304123400000000')+b'\1A\0').hex(),present=True)),0x20a80a4:('len < 6','len > 6',dict(data=bytes(8).hex(),length=5,present=False)),0x20a80f8:('return sbe_dataerror','return sbe_allocerror',dict(data=bytes(4).hex(),length=4))}
        if a not in mutation:continue
        old,new,v=mutation[a];folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;wrong.write_text(source.read_text());changed=wrong.read_text().replace(old,new,1)
        if changed==wrong.read_text():raise ValueError('Whole wrong push C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong whole push C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            result=run(image,row,body,v,seed,helpers)
            if not result['topReturned'] or result['modelPassed']:raise ValueError('Whole wrong push C did not actually return model violation')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(failures),records=failures))
    limits=['Independent bounded player/map/IP-port/message-prefix schema models check truncated fields, absent servers, present-server maps with null optional callback and server-prefix errors. Actual Thumb callers and real original lookup/getter/NUL helpers execute without substitutes; all memory, return, mode and ABI checks apply.','Actual player/final/map/delete/server-added callback dispatch, pushed key allocation/reference mutation, successful server insertion and full traffic/device/network/scenes remain unexecuted. Typed callback ABI is separately byte/link/layout-qualified; helpers and external storage receive0 extra source credit. Initial caller entries are excluded from helper metrics.']
    report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),helperBodies=list(helpers.values()),unsupported=unsupported,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
