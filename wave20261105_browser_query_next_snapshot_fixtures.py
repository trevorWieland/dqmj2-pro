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
from wave20261105_browser_query_next_snapshot_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/browser-query-next/snapshot'
WORK=ROOT/'work/w5bq/snapshot/fixtures'
PACKED,OUT,STOP,SP=0x21d2318,0x2170000,0x27e0000,0x2701000
MASK43=(1<<43)-1


def qualify_graph(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text().splitlines();records=(ROOT/'config/arm9/relocs.txt').read_text().splitlines();entries={}
    for a,mode,n in [(0x20a4660,'thumb',144),(0x2008e0c,'arm',304)]:
        canonical=next((x for x in inventory if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,n,a),x)),None)
        if canonical is None:raise ValueError('Snapshot original helper entry/boundary absent')
        entries[a]=dict(address=a,mode=mode,bytes=n,canonicalRecord=canonical,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+n]).hexdigest(),sourceCredit=0)
    expected=[f'from:0x{a:08x} kind:thumb_call_arm to:0x02008e0c module:main' for a in [0x20a466a,0x20a4688,0x20a46b8,0x20a46d2]]+[f'from:0x{a:08x} kind:load to:0x{p:08x} module:main' for a,p in [(0x20a46d8,PACKED),(0x20a46e0,PACKED+5),(0x20a46e4,PACKED+10),(0x20a46ec,PACKED+12)]]
    if not all(x in records for x in expected):raise ValueError('Snapshot actual copy/literal provenance differs')
    if struct.unpack_from('<I',image,0x20a46dc-0x2000000)[0]!=0x7ff or struct.unpack_from('<I',image,0x20a46e8-0x2000000)[0]!=0x3ff:raise ValueError('Snapshot actual43/10-bit masks differ')
    if not any(re.fullmatch(r'\S+ kind:function\(thumb,size=0x[0-9a-f]+\) addr:0x020a46f0',x) for x in inventory):raise ValueError('Snapshot setter boundary lacks actual canonical Thumb entry')
    return entries,dict(entries=list(entries.values()),actualCopyAndLiteralRecords=expected,decodedInputLayout=dict(bytes=14,firstBits=[0,43],secondBits=[43,86],opaqueLow16Bits=[86,96],opaqueHigh16Bits=[96,112]),semanticNamesProven=False,helperSourceCredit=0,originalDataStorageExtentAuthorshipCredit=0)


def model(raw):
    value=int.from_bytes(raw,'little');return struct.pack('<QQHH',value&MASK43,(value>>43)&MASK43,(value>>86)&0x3ff,(value>>96)&0xffff)


def run(image,row,body,v,seed,entries):
    a=int(row['address'],0);partial=a==0x20a5488;raw=bytes.fromhex(v['packed']);decoded=model(raw);before=struct.pack('<QQI',0x1122334455,0x66778899aa,0xdeadbeef);expected=bytearray(before)
    if partial:expected[:8]=before[8:16];expected[8:16]=decoded[8:16]
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);cpu.mem_write(PACKED,raw);cpu.mem_write(OUT,before+bytes([0xcc])*16);initial=[(0x55cc0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1];initial[:2]=[OUT,v.get('argument',0)]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    allowed={a:dict(address=a,mode='thumb',bytes=row['bytes']),**entries};pcs=[];calls=[];returned=False;capture=None;root_entered=False
    def code(machine,at,size,user):
        nonlocal returned,capture,root_entered
        if partial and at==0x20a46f0:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Snapshot setter canonical mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];capture=dict(target='0x20a46f0',mode='thumb',registers=regs[:4],callerSp=hex(regs[13]),callerLr=hex(regs[14]));machine.emu_stop();return
        if at==STOP:
            if partial:raise ValueError('Snapshot setter-prefix unexpectedly returned')
            returned=True;machine.emu_stop();return
        entry=next((r for start,r in allowed.items() if start<=at<start+r['bytes']),None)
        if entry is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(entry['mode']=='thumb'):raise ValueError(('Snapshot escaped original CPU/mode graph',hex(at)))
        if at==a and not root_entered:root_entered=True
        elif at in allowed:calls.append(at)
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        legal=SP-0x4000<=at and at+size<=SP or partial and OUT<=at and at+size<=OUT+20
        if not legal:raise ValueError(('Snapshot unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not partial and (not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP):raise ValueError('Snapshot complete return/callee-saved ABI differs')
    if partial and capture is None:raise ValueError('Actual original snapshot setter boundary not reached')
    correct=bytes(cpu.mem_read(PACKED,14))==raw and bytes(cpu.mem_read(OUT,36))==bytes(expected)+bytes([0xcc])*16
    if partial:correct=correct and capture['registers'][:2]==[OUT,v['argument']&0xffffffff]
    else:correct=correct and regs[0]==int(int.from_bytes(decoded[:8],'little')==0 and int.from_bytes(decoded[8:16],'little')==0)
    return dict(address=row['address'],vector=v,seed=seed,topReturned=returned,modelPassed=bool(correct),returnValue=regs[0] if returned else None,scope='complete-return' if returned else 'entry-before-original-setter-instruction',boundaryHelperInstructions=0,capture=capture,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],initialCallerExcludedFromHelperMetric=True,calleeSavedAbiPreserved=True if returned else None,outputSha256=hashlib.sha256(cpu.mem_read(OUT,36)).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();entries,proof=qualify_graph(image);rng=random.Random(0x56488);values=[bytes(14),bytes([255])*14]+[(1<<bit).to_bytes(14,'little') for bit in range(112)]+[bytes(rng.randrange(256) for i in range(14)) for n in range(16)];records=[];stops=[];negative=[];boundary_negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();vectors=[dict(packed=raw.hex(),argument=argument) for raw in values for argument in ([0,1,0xffffffff] if a==0x20a5488 else [0])]
        for seed,v in enumerate(vectors):
            original=run(image,row,native,v,seed,entries);source=run(image,row,linked,v,seed,entries)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent packed-field snapshot model failed',original,source))
            (records if original['topReturned'] else stops).append(original)
        old,new=('out->second=local.second','out->second=local.first') if a==0x20a5488 else ('local.second==0 && local.first==0','local.second==0 || local.first==0');folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole snapshot C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong snapshot C extent changed',row['address'],bad['compiledBytes']))
        failures=[];v=dict(packed=(1<<43).to_bytes(14,'little').hex(),argument=1)
        for seed in range(16):
            result=run(image,row,body,v,seed,entries)
            if result['modelPassed']:raise ValueError('Wrong whole snapshot C did not violate independent bitfield model')
            failures.append(result)
        item=dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],modelRejections=len(failures),records=failures);(negative if failures[0]['topReturned'] else boundary_negative).append(item)
    limits=['The actual original144-byte snapshot helper and304-byte ARM copy helper execute against an explicit14-byte mutable RAM input at canonical2318. Independent integer-field extraction checks two43-bit fields and opaque10/16-bit tail; every112 input bit, zero/all-one and deterministic random inputs are exercised with a deliberately nonzero local stack fill.','The54-byte predicate fully returns and preserves the caller ABI. The56-byte mover executes through real snapshot/copy bodies and stops BEFORE the original canonical setter first instruction; independent models check previous-second to first/new-second movement, opaque tail/input/guards and actual forwarded argument. No setter instruction or mover return executes.','One same-extent whole wrong C actually returns incorrect AND/OR predicate results; another whole wrong C violates separate pre-setter field models. The20-byte ABI is measured; Snapshot/first/second/opaque are conservative field identities, not proven account/firmware semantics.','All native helper/callee bodies, packed external object storage extent/authorship, setter effects, hardware/FIFO/device/scenes and full native game execution remain0 additional source credit and unexecuted where not explicitly covered.']
    trace=hashlib.sha256(json.dumps(dict(returns=records,boundaries=stops),sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,boundaryRecords=stops,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records+stops),wholeCNegativeControlsRejected=len(negative),wrongC=negative,boundaryWholeCNegativeControlsRejected=len(boundary_negative),boundaryWrongC=boundary_negative,actualNativeAndSourceEntryToBoundaryStops=2*len(stops),boundaryCallerReturns=0,boundaryHelperInstructions=0,originalGraphProof=proof,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
