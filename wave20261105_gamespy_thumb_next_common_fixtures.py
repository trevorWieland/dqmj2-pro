import base64
import hashlib
import json
import random
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_common_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/common'
WORK=ROOT/'work/w5gt/common/fixtures'
INPUT,OUTPUT,LENGTH,STATE,STOP,SP=0x2170000,0x2172000,0x2174000,0x20e0378,0x27e0000,0x2701000


def helper_graph(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();catalog={int(a,0):dict(address=a,mode=m,bytes=int(n,0),canonicalInventoryRecord=line) for line,m,n,a in re.findall(r'^(\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+))$',inventory,re.M)}
    roots=[0x20a8f54,0x20a8f1c,0x2026350,0x2026144,0x20a8f9c,0x20a8fe0,0x201b208];selected=set(roots);pending=roots[:]
    records=(ROOT/'config/arm9/relocs.txt').read_text().splitlines()
    while pending:
        a=pending.pop();row=catalog[a]
        for line in records:
            m=re.fullmatch(r'from:(0x[0-9a-f]+) kind:(arm_call|arm_branch|thumb_call|thumb_call_arm|load) to:(0x[0-9a-f]+) module:main',line)
            if m and a<=int(m[1],0)<a+row['bytes'] and int(m[3],0) in catalog and int(m[3],0) not in selected:selected.add(int(m[3],0));pending.append(int(m[3],0))
    return {a:dict(catalog[a],nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+catalog[a]['bytes']]).hexdigest(),sourceCredit=0) for a in selected}


def setup(address,v):
    data=bytes.fromhex(v.get('data',''));buffer=data+bytes(512-len(data));out=bytes([0xcd])*512
    regions={INPUT:buffer,OUTPUT:out,LENGTH:struct.pack('<I',0xbadbeef),STATE:struct.pack('<I',v.get('state',1))};expected=dict(regions);contract='value';result=0;stackarg=None
    if address==0x20a8ea0:args=[0,0,0,0]
    elif address==0x20a8f1c:args=[v['state'],0,0,0];result=(v['state']*16807)%2147483647
    elif address==0x20a8f84:
        low,high=v['low'],v['high'];args=[low&0xffffffff,high&0xffffffff,0,0];value=(v['state']*16807)%2147483647;result=low if high==low else low+value%(high-low)
        if high!=low:expected[STATE]=struct.pack('<I',value)
    elif address==0x20a8f9c:
        n=v['length'];args=[INPUT,OUTPUT,n,0];contract='void';value=int.from_bytes(data[:4],'big');decoded=((value>>24)<<18|((value>>16)&255)<<12|((value>>8)&255)<<6|(value&255)).to_bytes(3,'big');count=max(0,min(3,n-1));expected[OUTPUT]=decoded[:count]+out[count:]
    elif address==0x20a91a0:
        args=[INPUT,OUTPUT,len(data),v['encoding']];contract='void';encoded=base64.b64encode(data)
        if v['encoding']==1:encoded=encoded.translate(bytes.maketrans(b'+/=',b'[]_'))
        elif v['encoding']==2:encoded=encoded.translate(bytes.maketrans(b'+/',b'-_'))
        expected[OUTPUT]=encoded+b'\0'+out[len(encoded)+1:]
    elif address==0x20a9040:
        args=[INPUT,OUTPUT,len(data),0 if v.get('nullLength') else LENGTH];stackarg=v['encoding'];contract='void';raw=data
        if v['encoding']==1:raw=raw.translate(bytes.maketrans(b'[]_',b'+/='))
        elif v['encoding']==2:raw=raw.translate(bytes.maketrans(b'-_',b'+/'))
        decoded=base64.b64decode(raw+b'='*((-len(raw))%4));expected[OUTPUT]=(decoded+out[len(decoded):]) if raw else b'\0'+out[1:]
        if not v.get('nullLength'):expected[LENGTH]=struct.pack('<I',len(decoded))
    else:raise ValueError('Unqualified common caller')
    return regions,expected,args,contract,result&0xffffffff,stackarg


def run(image,row,body,v,seed,helpers):
    address=int(row['address'],0);regions,expected,args,contract,result,stackarg=setup(address,v);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    for at,data in regions.items():cpu.mem_write(at,data)
    if stackarg is not None:cpu.mem_write(SP,struct.pack('<I',stackarg))
    initial=[(0x55660000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=args;initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    entries={a:0 for a in helpers};pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if at in entries and not (at==address and not pcs):entries[at]+=1
        mode='thumb' if address<=at<address+row['bytes'] else next((r['mode'] for a,r in helpers.items() if a<=at<a+r['bytes']),None)
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError(('Common fixture graph/mode escape',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        allowed=SP-0x4000<=at and at+size<=SP
        allowed=allowed or (address in (0x20a8f9c,0x20a9040,0x20a91a0) and OUTPUT<=at and at+size<=OUTPUT+512)
        allowed=allowed or (address==0x20a9040 and at==LENGTH and size==4) or (address==0x20a8f84 and at==STATE and size==4)
        if not allowed:raise ValueError(('Common fixture escaped measured writes',hex(at),size,hex(machine.reg_read(ar.UC_ARM_REG_PC))))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=100000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Common fixture return/callee-saved ABI differs')
    actual={a:bytes(cpu.mem_read(a,len(v))) for a,v in regions.items()};correct=contract=='void' or regs[0]==result
    return dict(address=hex(address),vector=v,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,returnContract=contract,modelPassed=actual==expected and correct,returnValue=regs[0],memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),actualOriginalHelperEntries={hex(a):n for a,n in entries.items()},actualOriginalHelperInvocations=sum(entries.values()),nativeEntryModesChecked=True,initialCallerExcludedFromHelperMetric=True)


def cases(address):
    seeds=[1,2,7,16807,1234567,2147483646]
    if address==0x20a8ea0:return [dict() for i in range(4)]
    if address==0x20a8f1c:return [dict(state=s) for i in range(4) for s in seeds]
    if address==0x20a8f84:return [dict(state=s,low=l,high=h) for s in seeds for l,h in [(0,0),(5,5),(0,1),(0,100),(-100,100),(100,200)]]
    if address==0x20a8f9c:return [dict(data=bytes(q).hex(),length=n) for q in [(0,0,0,0),(63,63,63,63),(3,4,5,6),(21,42,63,0),(0,63,1,62)] for n in range(5)]
    randomizer=random.Random(0x1105);values=[b'',b'a',b'ab',b'abc',b'hello',bytes([255])*6,bytes(range(64)),bytes(randomizer.randrange(256) for i in range(31))]
    if address==0x20a91a0:return [dict(data=b.hex(),encoding=t) for b in values for t in [0,1,2,7]]
    if address==0x20a9040:
        result=[]
        for b in values:
            for t in [0,1,2,7]:
                encoded=base64.b64encode(b)
                if t==1:encoded=encoded.translate(bytes.maketrans(b'+/=',b'[]_'))
                elif t==2:encoded=encoded.translate(bytes.maketrans(b'+/',b'-_'))
                for null in [False,True]:
                    for strip in [False,True]:result.append(dict(data=(encoded.rstrip(b'_') if t==1 else encoded.rstrip(b'=') if strip else encoded).hex() if strip else encoded.hex(),encoding=t,nullLength=null))
        return result
    return []


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers=helper_graph(image);records=[];negative=[]
    for row in rows:
        address=int(row['address'],0);native=image[address-0x2000000:address-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(cases(address)):
            original=run(image,row,native,v,seed,helpers);source=run(image,row,linked,v,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent common model differs',original,source))
            records.append(original)
        mutations={0x20a8f1c:('RANa 16807','RANa 16808',dict(state=1)),0x20a8f9c:('quart[0] << 2','quart[0] << 3',dict(data=bytes([3,4,5,6]).hex(),length=4)),0x20a9040:('input[readpos] - 65','input[readpos] - 64',dict(data=b'YQ=='.hex(),encoding=0,nullLength=False)),0x20a91a0:('*output + 65','*output + 66',dict(data=b'a'.hex(),encoding=0))}
        if address not in mutations:continue
        old,new,v=mutations[address];folder=WORK/format(address,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;wrong.write_text(source.read_text());owner=wrong if old in wrong.read_text() else folder/'context.h';text=owner.read_text();changed=text.replace(old,new,1)
        if text==changed:raise ValueError(('Whole wrong common C did not mutate',row['address']))
        owner.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong complete common C extent changed',row['address'],bad['compiledBytes']))
        controls=[]
        for seed in range(16):
            result=run(image,row,body,v,seed,helpers)
            if not result['topReturned'] or result['modelPassed']:raise ValueError('Wrong common C did not actually return a model violation')
            controls.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(controls),records=controls))
    report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),helperBodies=list(helpers.values()),unsupported=[],wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),limits=['Actual Thumb callers and original ARM/Thumb helpers execute without substitutes; initial caller entries are excluded from the helper metric. Complete returns, code-entry modes, allowed writes, region contents and callee-saved ABI are checked.','Independent integer models exercise Park-Miller states1..2147483646 and valid bounded ranges. Python standard base64 provides independent valid-input models for default, bracket and URL alphabets, padding, unpadded tails and optional output length. Direct quart conversion covers valid sextets and lengths0..4.','String duplication executes only its null-input path. Allocator/non-null duplication, malformed codec input, invalid pointers, RNG states outside the stated domain, network/devices/scenes and complete external storage extent/authorship remain unexecuted/uncredited. Helper bodies/data carry0 extra source credit.'])
    write_json(LANE/'caller-fixtures.json',report);return report
