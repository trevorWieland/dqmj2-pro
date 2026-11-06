import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_browser_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/browser'
WORK=ROOT/'work/w5gt/browser/fixtures'
BROWSER,SERVER,ARRAY,AVAILABLE,STOP,SP=0x2170000,0x2172000,0x2173000,0x21d23ec,0x27e0000,0x2701000


def helper_graph(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();catalog={int(a,0):dict(address=a,mode=m,bytes=int(n,0),canonicalInventoryRecord=line) for line,m,n,a in re.findall(r'^(\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+))$',inventory,re.M)}
    selected={0x20a5ac0,0x20a8640,0x20a6db0,0x20a8644};pending=list(selected);records=(ROOT/'config/arm9/relocs.txt').read_text().splitlines()
    while pending:
        a=pending.pop();row=catalog[a]
        for line in records:
            m=re.fullmatch(r'from:(0x[0-9a-f]+) kind:(arm_call|arm_branch|thumb_call|thumb_call_arm) to:(0x[0-9a-f]+) module:main',line)
            if m and a<=int(m[1],0)<a+row['bytes'] and int(m[3],0) in catalog and int(m[3],0) not in selected:selected.add(int(m[3],0));pending.append(int(m[3],0))
    return {a:dict(catalog[a],nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+catalog[a]['bytes']]).hexdigest(),sourceCredit=0) for a in selected}


def setup(address,v):
    browser=bytearray(2112);server=bytearray(44);array=bytearray(24);struct.pack_into('<i',browser,16,v.get('queries',1));struct.pack_into('<I',browser,80,ARRAY);struct.pack_into('<i',browser,76,v.get('state',1));struct.pack_into('<I',browser,1776,0xaabbccdd);struct.pack_into('<I',browser,2096,0x11223344);struct.pack_into('<H',browser,2100,0x1234);struct.pack_into('<I',server,0,0x11223344 if not v.get('wrongIp') else 0x44332211);struct.pack_into('<H',server,4,0x1234 if not v.get('wrongPort') else 0x4321);struct.pack_into('<i',array,0,v.get('arrayCount',1))
    regions={BROWSER:bytes(browser),SERVER:bytes(server),ARRAY:bytes(array),AVAILABLE:struct.pack('<I',v.get('available',0)&0xffffffff)};expected=dict(regions);contract='void';result=0;stack=[]
    if address==0x20a6564:
        args=[BROWSER+76,v['reason'],0 if v.get('nullServer') else SERVER,BROWSER]
        if v['reason']==6:struct.pack_into('<I',browser,40,0xaabbccdd)
    elif address==0x20a66c0:args=[BROWSER,v['reason']&0xffffffff,0 if v.get('nullServer') else SERVER,BROWSER]
    elif address==0x20a6744:args=[0,0,0,0];stack=[4,1,0,0,0];contract='value'
    elif address==0x20a691c:args=[BROWSER,SERVER,0,0]
    elif address==0x20a6978:
        args=[BROWSER,0,0,0];contract='value';result=2 if v['queries']>0 else 1 if v['state'] in [0,3] else 0 if v['state']==1 else 3
    else:raise ValueError('Unexecuted browser sort/callback provider path')
    if address in (0x20a6564,0x20a66c0) and not v.get('nullServer') and not v.get('wrongIp') and not v.get('wrongPort'):struct.pack_into('<I',browser,2096,0)
    expected[BROWSER]=bytes(browser)
    return regions,expected,args,contract,result,stack


def run(image,row,body,v,seed,helpers):
    address=int(row['address'],0);regions,expected,args,contract,result,stackargs=setup(address,v);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
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
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError(('Browser fixture graph/mode escape',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        allowed=SP-0x4000<=at and at+size<=SP
        if address in (0x20a6564,0x20a66c0) and size==4 and at in (BROWSER+40,BROWSER+2096):allowed=True
        if not allowed:raise ValueError(('Browser fixture unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=10000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Browser fixture return/callee-saved ABI differs')
    actual={a:bytes(cpu.mem_read(a,len(value))) for a,value in regions.items()};correct=contract=='void' or regs[0]==result
    return dict(address=row['address'],vector=v,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,returnContract=contract,modelPassed=actual==expected and correct,returnValue=regs[0],actualOriginalHelperEntries={hex(a):n for a,n in entries.items()},actualOriginalHelperInvocations=sum(entries.values()),initialCallerExcludedFromHelperMetric=True,memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def cases(address):
    if address==0x20a6564:return [dict(reason=reason,nullServer=n,wrongIp=i,wrongPort=p) for reason in [3,4,6] for n,i,p in [(True,False,False),(False,False,False),(False,True,False),(False,False,True)]]
    if address==0x20a66c0:return [dict(reason=reason,nullServer=n,wrongIp=i,wrongPort=p) for reason in [4,5,7,-1] for n,i,p in [(True,False,False),(False,False,False),(False,True,False),(False,False,True)]]
    if address==0x20a6744:return [dict(available=a) for i in range(4) for a in [0,2,-1,0x40000000]]
    if address==0x20a691c:return [dict(arrayCount=0) for i in range(8)]
    if address==0x20a6978:return [dict(queries=q,state=s) for q in [-10,0,1,0x7fffffff] for s in [-1,0,1,2,3,4,255]]
    return []


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers=helper_graph(image);records=[];negative=[];unsupported=[]
    for row in rows:
        a=int(row['address'],0);vectors=cases(a)
        if not vectors:unsupported.append(dict(address=row['address'],returningVectors=0,reason='Aggregate sort/string/callback graph unexecuted'));continue
        native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(vectors):
            original=run(image,row,native,v,seed,helpers);source=run(image,row,linked,v,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent browser model differs',original,source))
            records.append(original)
        mutation={0x20a6564:('sb->triggerIP = 0','sb->triggerIP = 1',dict(reason=4,nullServer=False)),0x20a66c0:('sb->triggerIP = 0','sb->triggerIP = 1',dict(reason=4,nullServer=False)),0x20a6978:('return sb_querying','return 4',dict(queries=1,state=1))}
        if a not in mutation:continue
        old,new,v=mutation[a];folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;wrong.write_text(source.read_text());changed=wrong.read_text().replace(old,new,1)
        if changed==wrong.read_text():raise ValueError('Wrong complete browser C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong complete browser C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            result=run(image,row,body,v,seed,helpers)
            if not result['topReturned'] or result['modelPassed']:raise ValueError('Wrong complete browser C did not actually return model violation')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(failures),records=failures))
    limits=['Actual Thumb callers and actual original helpers execute without substitutes; initial caller entries are excluded from the helper metric. Independent models check raw trigger IP/port reset conditions, public-IP propagation, idle list filtering, constructor availability rejection, empty server removal and state precedence.','Constructor executes only non-LAN availability rejection; allocation, list/engine construction, callback dispatch, network/device paths and sorting remain unexecuted. Source layout names follow pinned primary comparison and explicitly measured native version differences; unused structure field meaning is comparative.','No complete scenes, hardware/network behavior or external storage extent/authorship is credited. Canonical odd callback literals and full caller extents are separately byte/link-qualified with0 extra helper/callback source credit.']
    report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),helperBodies=list(helpers.values()),unsupported=unsupported,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
