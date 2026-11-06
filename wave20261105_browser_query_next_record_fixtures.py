from wave20261105_browser_query_next_record_paths import assert_owned,assert_compile,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
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
from wave20261105_browser_query_next_record_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/browser-query-next/record'
WORK=ROOT/'work/w5bq/record/fixtures'
INPUT,OTHER,GLOBAL,STOP,SP=0x2170000,0x2172000,0x21d230c,0x27e0000,0x2701000


def helper_entries(image):
    entries={};inventory=(ROOT/'config/arm9/symbols.txt').read_text().splitlines()
    for a,mode,size in [(0x20a4990,'thumb',30),(0x2008e0c,'arm',304)]:
        record=next((x for x in inventory if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,size,a),x)),None)
        if record is None:raise ValueError('Original record predicate/copy entry absent')
        entries[a]=dict(address=a,mode=mode,bytes=size,canonicalRecord=record,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+size]).hexdigest(),sourceCredit=0)
    return entries


def run(image,row,body,v,seed,helpers):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);left=bytes.fromhex(v.get('left',''));right=bytes.fromhex(v.get('right',''));inputbytes=left+bytes([0xcc])*32;otherbytes=right+bytes([0xee])*32;old=struct.pack('<HHI',0x1234,0x5678,0x89abcdef);cpu.mem_write(INPUT,inputbytes);cpu.mem_write(OTHER,otherbytes);cpu.mem_write(GLOBAL,old+bytes([0xdd])*16)
    initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1];initial[:3]=[v.get('ignored',0),v.get('value',0),v.get('error',0)] if a==0x20a4dcc else [INPUT,OTHER,0]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    allowed={a:dict(address=a,mode='thumb',bytes=row['bytes'])}
    if a==0x20a4950:allowed.update(helpers)
    returned=False;pcs=[];calls=[];root_entered=False
    def code(machine,at,size,user):
        nonlocal returned,root_entered
        if at==STOP:returned=True;machine.emu_stop();return
        entry=next((r for start,r in allowed.items() if start<=at<start+r['bytes']),None)
        if entry is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(entry['mode']=='thumb'):raise ValueError(('Record escaped original CPU/mode graph',hex(at)))
        if at==a and not root_entered:root_entered=True
        elif at in allowed:calls.append(at)
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP or a==0x20a4dcc and GLOBAL<=at and at+size<=GLOBAL+8):raise ValueError(('Record unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Record full return/callee-saved ABI differs')
    if a==0x20a4938:expected=int(any(left));expected_global=old
    elif a==0x20a4950:valid=1<=left[0]<=223 and left[0]!=127;expected=int(valid and bool(int.from_bytes(left,'little')&(~int.from_bytes(right,'little')&0xffffffff)));expected_global=old
    else:expected=255 if v['error'] else v['value']&255;expected_global=struct.pack('<HHI',expected,0x5678,1)
    globalbytes=bytes(cpu.mem_read(GLOBAL,24));correct=regs[0]==expected and globalbytes==expected_global+bytes([0xdd])*16 and bytes(cpu.mem_read(INPUT,len(inputbytes)))==inputbytes and bytes(cpu.mem_read(OTHER,len(otherbytes)))==otherbytes
    return dict(address=row['address'],vector=v,seed=seed,topReturned=True,returnValue=regs[0],modelPassed=bool(correct),calleeSavedAbiPreserved=True,globalSha256=hashlib.sha256(globalbytes).hexdigest(),inputGuardsPreserved=True,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],initialCallerExcludedFromHelperMetric=True,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def vectors(a):
    rng=random.Random(0x4938)
    if a==0x20a4938:return [dict(left=v.hex()) for v in [bytes(32),bytes([255])*32,*[(1<<b).to_bytes(32,'little') for b in range(256)],*[bytes(rng.randrange(256) for i in range(32)) for n in range(16)]]]
    if a==0x20a4950:
        values=[]
        for first in range(256):
            left=bytes([first,0x80,0xff,1]);x=int.from_bytes(left,'little')
            for y in [0,0xffffffff,x,x^0xffffffff]:values.append(dict(left=left.hex(),right=y.to_bytes(4,'little').hex()))
        return values+[dict(left=bytes(rng.randrange(256) for i in range(4)).hex(),right=bytes(rng.randrange(256) for i in range(4)).hex()) for n in range(32)]
    return [dict(value=value,error=error,ignored=0x98765432) for value in [*range(256),0x12345678,0xffffff00,0xffffffff] for error in [0,1,0xffffffff]]


def execute(rows):
    assert_owned(LANE,OWN_SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers=helper_entries(image);records=[];negative=[];changes={0x20a4938:('if(p[i])','if(p[i]==0)'),0x20a4950:('return(x&~y)!=0','return(x&~y)==0'),0x20a4dcc:('if(error)','if(!error)')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(vectors(a)):
            original=run(image,row,native,v,seed,helpers);source=run(image,row,linked,v,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent bounded record model differs',original,source))
            records.append(original)
        folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=changes[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole record C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong record C extent changed',row['address'],bad['compiledBytes']))
        v=dict(left=bytes(32).hex()) if a==0x20a4938 else dict(left='c0a80101',right='ffffffff') if a==0x20a4950 else dict(value=7,error=0,ignored=0);failures=[]
        for seed in range(16):
            result=run(image,row,body,v,seed,helpers)
            if result['modelPassed']:raise ValueError('Wrong complete record C did not violate independent model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],returningModelRejections=len(failures),records=failures))
    limits=['Actual original/source complete returns match independent any-nonzero32-byte, first-byte numeric eligibility plus integer-set-difference, and16-bit status/32-bit ready models; input/opaque-field/guards and callee-saved ABI remain exact. Every32-byte input bit, every first-byte value and all256 low scalar values plus upper-bit cases are exercised.','The64-byte predicate executes actual canonical30-byte first-byte helper and304-byte ARM copy helper; no helper source credit. No account/network semantics are inferred from the numeric ranges or field identities.','The32-byte routine is entered standalone with explicit scalar register inputs and mutable8-byte BSS view at existing canonical230c; volatile status/readiness/opaque accesses retain native widths0:16,2:16,4:32. No FIFO event delivery, service callback pipeline or hardware executes.','Three same-extent whole wrong C units genuinely link and actually return independent model failures. Complete external object storage extent/authorship, hardware/device/scenes and full native game execution remain unproven/uncredited.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalHelperEntries=list(helpers.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
