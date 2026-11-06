import copy
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
from wave20261105_gamespy_thumb_next_md5_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/md5'
WORK=ROOT/'work/w5gt/md5/fixtures'
INPUT,OUTPUT,STOP,SP=0x2170000,0x2172000,0x27e0000,0x2701000
SDK={0x209426c:(0x200cad0,64),0x2094274:(0x200cb10,200),0x209427c:(0x200cbd8,184)}


def sdk_veneer(entry,body,record,target):
    a=entry['address']
    if a not in SDK or any(entry[k]!=v for k,v in dict(program='',processor='arm9',module='main',mode='thumb',bytes=8).items()):raise ValueError('SDK veneer namespace/mode/boundary differs')
    destination,size=SDK[a]
    if body!=bytes.fromhex('004b1847')+struct.pack('<I',destination):raise ValueError('SDK Thumb ldr-r3/bx-r3/native literal differs')
    if record!=f'from:0x{a+4:08x} kind:load to:0x{destination:08x} module:main':raise ValueError('SDK original literal record differs')
    expected=dict(program='',processor='arm9',module='main',mode='arm',address=destination,bytes=size)
    if any(target[k]!=v for k,v in expected.items()):raise ValueError('SDK original canonical ARM target differs')
    return dict(address=hex(a),bytes=body.hex(),originalLiteralRecord=record,canonicalTarget=expected,targetEntryProven=True,sourceCredit=0,calleeCodeCredit=0)


def graph(image,root):
    symbols={};records=[]
    for line in (ROOT/'config/arm9/symbols.txt').read_text().splitlines():
        m=re.fullmatch(r'\S+ kind:function\((arm|thumb),size=0x([0-9a-f]+)\) addr:0x([0-9a-f]+)',line)
        if m:symbols[int(m[3],16)]=dict(program='',processor='arm9',module='main',mode=m[1],address=int(m[3],16),bytes=int(m[2],16),originalInventoryRecord=line)
    for line in (ROOT/'config/arm9/relocs.txt').read_text().splitlines():
        m=re.fullmatch(r'from:0x([0-9a-f]+) kind:(\S+) to:0x([0-9a-f]+) module:(\S+)',line)
        if m:records.append(dict(origin=int(m[1],16),kind=m[2],target=int(m[3],16),module=m[4],record=line))
    pending=[root];seen={};veneers=[];negative=[]
    while pending:
        a=pending.pop()
        if a in seen:continue
        if a not in symbols or len(seen)>=20:raise ValueError('SDK graph unbounded or unconfigured entry')
        entry=copy.deepcopy(symbols[a]);b=image[a-0x2000000:a-0x2000000+entry['bytes']];out=[r for r in records if a<=r['origin']<a+entry['bytes'] and r['kind']!='load']
        if a in SDK:
            literal=next(r for r in records if r['origin']==a+4);target=symbols[SDK[a][0]];veneers.append(sdk_veneer(entry,b,literal['record'],target));out.append(literal)
            controls=[]
            for k,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','arm'),('bytes',12)]:
                wrong=copy.deepcopy(entry);wrong[k]=value;controls.append((wrong,b,literal['record'],target))
            controls.extend([(entry,bytes([b[0]^1])+b[1:],literal['record'],target),(entry,b[:-1]+bytes([b[-1]^1]),literal['record'],target),(entry,b,literal['record'].replace(f'{a+4:08x}',f'{a+6:08x}'),target)])
            for k,value in [('mode','thumb'),('address',SDK[a][0]+4),('bytes',4),('program','child'),('processor','arm7')]:
                wrong=copy.deepcopy(target);wrong[k]=value;controls.append((entry,b,literal['record'],wrong))
            for n,arguments in enumerate(controls):
                try:sdk_veneer(*arguments)
                except ValueError as exc:negative.append(dict(address=hex(a),control=n,rejected=True,reason=str(exc)))
                else:raise ValueError('Wrong SDK veneer proof accepted')
        for r in out:
            if r['module']!='main':raise ValueError('SDK graph crosses module')
            pending.append(r['target'])
        entry.update(targetSha256=hashlib.sha256(b).hexdigest(),originalOutgoingRecords=[r['record'] for r in out]);seen[a]=entry
    return seen,dict(entries=list(seen.values()),veneers=veneers,veneerNegatives=negative,helperCodeCredit=0,originalDataStorageExtentAuthorshipCredit=0)


def run(image,row,body,v,seed,allowed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    payload=bytes.fromhex(v['data']);original=payload+bytes([0xcc])*64;cpu.mem_write(INPUT,original);cpu.mem_write(OUTPUT,bytes([0xcc])*49);initial=[(0x55770000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1];initial[:3]=[INPUT,OUTPUT,0] if a==0x20a8ae0 else [INPUT,len(payload),OUTPUT]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    pcs=[];helpers=[];returned=False;root_entered=False
    def code(machine,at,size,user):
        nonlocal returned,root_entered
        if at==STOP:returned=True;machine.emu_stop();return
        entry=next((r for start,r in allowed.items() if start<=at<start+r['bytes']),None)
        if entry is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(entry['mode']=='thumb'):raise ValueError(('MD5 escaped actual canonical CPU/mode graph',hex(at)))
        if entry['address'] in SDK and at>=entry['address']+4:raise ValueError('MD5 attempted to execute veneer literal')
        if at==a and not root_entered:root_entered=True
        elif at in allowed:helpers.append(at)
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP or OUTPUT<=at and at+size<=OUTPUT+33):raise ValueError(('Unexpected MD5 write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('MD5 original return/callee-saved ABI differs')
    expected=(payload.hex() if a==0x20a8ae0 else hashlib.md5(payload).hexdigest()).encode()+b'\0';actual=bytes(cpu.mem_read(OUTPUT,49));correct=actual[:33]==expected and actual[33:]==bytes([0xcc])*16 and bytes(cpu.mem_read(INPUT,len(original)))==original
    return dict(address=row['address'],vector=v,seed=seed,topReturned=True,modelPassed=correct,outputHex=actual.hex(),calleeSavedAbiPreserved=True,initialCallerExcludedFromHelperMetric=True,actualOriginalHelperInvocations=len(helpers),helperEntries=[hex(x) for x in helpers],pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];graphs=[];negative=[];rng=random.Random(0x51105)
    for row in rows:
        a=int(row['address'],0);allowed,proof=graph(image,a);graphs.append(proof);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        values=[bytes((n+17*i)&255 for i in range(16)) for n in range(256)]+[bytes(16),bytes([255])*16] if a==0x20a8ae0 else [b'',b'a',b'abc',b'message digest',*[bytes((i*37+11)&255 for i in range(n)) for n in [55,56,63,64,65,127,128]]]
        if a==0x20a8ae0:values += [bytes(rng.randrange(256) for i in range(16)) for n in range(16)]
        for seed,payload in enumerate(values):
            v=dict(data=payload.hex());original=run(image,row,native,v,seed,allowed);source=run(image,row,linked,v,seed,allowed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent MD5/hex model differs',original,source))
            records.append(original)
        old,new=('i < 16','i < 15') if a==0x20a8ae0 else ('MD5Update(&ctx, input, len)','MD5Update(&ctx, input + 4, len)');folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole MD5 C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Wrong whole MD5 C extent changed')
        failures=[];v=dict(data=(bytes([255])*16 if a==0x20a8ae0 else bytes(range(64))).hex())
        for seed in range(16):
            result=run(image,row,body,v,seed,allowed)
            if result['modelPassed']:raise ValueError('Whole wrong MD5 C did not violate independent return model')
            failures.append(result)
        negative.append(dict(address=row['address'],compiledBytes=bad['compiledBytes'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],genuineLink=bad['realLink'],returningModelRejections=len(failures),records=failures))
    limits=['Independent Python byte-to-lowercase-hex and hashlib MD5 models check actual complete original/compiled Thumb caller returns,33 output bytes, input/guard preservation and callee-saved ABI. MD5 vectors cover padding/block boundaries0/55/56/63/64/65/127/128.','The digest wrapper executes the real closed original11-entry main ARM9 graph, including three exact8-byte Thumb ldr-r3/bx-r3 veneers, original literal records and genuine canonical ARM MD5 entries.39 negative namespace/mode/native-byte/literal/boundary controls reject altered veneer proofs; no alias or shared binder change.','Only the selected60-byte print and46-byte wrapper are source-credit candidates. Executed original SDK callee bodies, internal context field semantics, hexadecimal-table storage extent/authorship, devices/scenes/network and full game execution receive0 additional reconstruction credit.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,canonicalCpuGraphs=graphs,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
