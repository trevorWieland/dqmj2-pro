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
from wave20261105_browser_query_next_crypto_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/browser-query-next/crypto'
WORK=ROOT/'work/w5bq/crypto/fixtures'
STATE,DATA,KEY,RSUM,KPOS,STOP,SP=0x2170000,0x2172000,0x2174000,0x2175000,0x2176000,0x27e0000,0x2701000
EXTENTS={0x20a5660:('thumb',116),0x20a56d4:('thumb',58),0x20a5710:('thumb',124),0x20a578c:('thumb',146),0x20a5820:('thumb',32),0x2026350:('arm',484)}
GRAPHS={0x20a5660:[0x20a5660,0x2026350],0x20a56d4:[0x20a56d4],0x20a5710:[0x20a5710,0x20a5660,0x20a56d4,0x2026350],0x20a578c:[0x20a578c],0x20a5820:[0x20a5820,0x20a578c]}


def native_entries(image):
    entries={};inventory=(ROOT/'config/arm9/symbols.txt').read_text().splitlines()
    for a,(mode,size) in EXTENTS.items():
        record=next((s for s in inventory if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,size,a),s)),None)
        if record is None:raise ValueError('Original exact cipher/ARM-division entry absent')
        entries[a]=dict(address=a,program='',processor='arm9',module='main',mode=mode,bytes=size,canonicalRecord=record,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+size]).hexdigest(),calleeSourceCredit=0)
    return entries


def state_bytes(seed):
    rng=random.Random(0x56110+seed);deck=list(range(256));rng.shuffle(deck);return bytes(deck+[rng.randrange(256) for i in range(5)])


def run(image,row,body,v,seed,entries):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);before=bytes.fromhex(v['state']);payload=bytes.fromhex(v.get('data',''));key=bytes.fromhex(v.get('key',''));cpu.mem_write(STATE,before+bytes([0xcc])*16);cpu.mem_write(DATA,payload+bytes([0xcc])*64);cpu.mem_write(KEY,key+bytes([0xee])*64);cpu.mem_write(RSUM,bytes([v.get('rsum',23)]));cpu.mem_write(KPOS,struct.pack('<I',v.get('keypos',0)))
    initial=[(0x55aa0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    if a==0x20a5660:initial[:4]=[STATE,v['limit'],KEY,len(key)];cpu.mem_write(SP,struct.pack('<II',RSUM,KPOS))
    elif a==0x20a56d4:initial[0]=STATE
    elif a==0x20a5710:initial[:3]=[STATE,KEY,len(key)]
    elif a==0x20a578c:initial[:2]=[STATE,v['byte']]
    else:initial[:3]=[STATE,DATA,v['length']&0xffffffff]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    allowed={n:entries[n] for n in GRAPHS[a]};pcs=[];calls=[];returned=False;root_entered=False
    def code(machine,at,size,user):
        nonlocal returned,root_entered
        if at==STOP:returned=True;machine.emu_stop();return
        entry=next((r for start,r in allowed.items() if start<=at<start+r['bytes']),None)
        if entry is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(entry['mode']=='thumb'):raise ValueError(('Cipher escaped original program/CPU/mode graph',hex(at)))
        if at==a and not root_entered:root_entered=True
        elif at in allowed:calls.append(at)
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        legal=SP-0x4000<=at and at+size<=SP or STATE<=at and at+size<=STATE+261
        if a==0x20a5660:legal=legal or RSUM<=at and at+size<=RSUM+1 or KPOS<=at and at+size<=KPOS+4
        if a==0x20a5820:legal=legal or DATA<=at and at+size<=DATA+max(0,v['length'])
        if not legal:raise ValueError(('Cipher wrote outside measured state/data bounds',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=200000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Cipher original return/callee-saved ABI differs')
    after=bytes(cpu.mem_read(STATE,277));data=bytes(cpu.mem_read(DATA,len(payload)+64));key_after=bytes(cpu.mem_read(KEY,len(key)+64));rsum=cpu.mem_read(RSUM,1)[0];keypos=struct.unpack('<I',cpu.mem_read(KPOS,4))[0];correct=after[261:]==bytes([0xcc])*16 and sorted(after[:256])==list(range(256)) and key_after==key+bytes([0xee])*64 and data[len(payload):]==bytes([0xcc])*64
    if a==0x20a5660:
        correct=correct and after[:261]==before and data==payload+bytes([0xcc])*64 and 0<=regs[0]<=v['limit'] and keypos<len(key)
        if v['limit']==0:correct=correct and regs[0]==0 and rsum==v['rsum'] and keypos==v['keypos']
    elif a==0x20a56d4 or a==0x20a5710 and not key:correct=correct and after[:261]==bytes(range(255,-1,-1))+bytes([1,3,5,7,11])
    elif a==0x20a5710:correct=correct and after[256:260]==bytes(after[i] for i in [1,3,5,7])
    elif a==0x20a578c:correct=correct and after[260]==v['byte'] and after[259]==regs[0]
    else:
        if v['length']<=0:correct=correct and after[:261]==before and data==payload+bytes([0xcc])*64
        else:correct=correct and after[260]==payload[v['length']-1] and after[259]==data[v['length']-1]
    return dict(address=row['address'],vector=v,seed=seed,topReturned=True,modelPassed=bool(correct),returnValue=regs[0] if a in (0x20a5660,0x20a578c) else None,stateSha256=hashlib.sha256(after).hexdigest(),dataSha256=hashlib.sha256(data).hexdigest(),rsum=rsum,keypos=keypos,calleeSavedAbiPreserved=True,initialCallerExcludedFromHelperMetric=True,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def vectors(a):
    if a==0x20a5660:return [dict(state=state_bytes(seed).hex(),key=bytes((i*37+seed)&255 for i in range(n)).hex(),limit=limit,rsum=(seed*19+23)&255,keypos=seed%n) for seed in range(2) for n in [1,3,16,255] for limit in [0,1,3,16,127,255]]
    if a==0x20a56d4:return [dict(state=state_bytes(seed).hex()) for seed in range(16)]
    if a==0x20a5710:return [dict(state=state_bytes(seed).hex(),key=bytes((i*37+seed)&255 for i in range(n)).hex()) for seed in range(4) for n in [0,1,3,16,255]]
    if a==0x20a578c:return [dict(state=state_bytes(seed).hex(),byte=b) for seed in range(4) for b in range(256)]
    return [dict(state=state_bytes(seed).hex(),data=bytes((i*37+11)&255 for i in range(max(n,0))).hex(),length=n) for seed in range(4) for n in [-1,0,1,2,7,16,64,255]]


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();entries=native_entries(image);records=[];negative=[];unsupported=[];changes={0x20a5660:('if (!limit) return 0','if (!limit) return 1'),0x20a56d4:('state->last_plain = 7','state->last_plain = 9'),0x20a5710:('keysize < 1','keysize < 2'),0x20a5820:('GOADecryptByte(state, bp[i])','GOADecryptByte(state, 0)')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(vectors(a)):
            original=run(image,row,native,v,seed,entries);source=run(image,row,linked,v,seed,entries)
            if original!=source or not original['modelPassed']:raise ValueError(('Actual cipher differential/state invariant failed',original,source))
            records.append(original)
        if a not in changes:unsupported.append(dict(address=row['address'],sameExtentWholeCNegative=0,reason='Two incorrect-feedback/arithmetic attempts compiled144 rather than146 bytes; preserved diagnostics receive0 negative credit. Actual256-byte-domain state differential/invariant returns and negative compiler layout remain qualified.'));continue
        folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=changes[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole cipher C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Wrong whole cipher C extent changed')
        choices=vectors(a);v=next(x for x in choices if x.get('limit')==0) if a==0x20a5660 else next(x for x in choices if len(bytes.fromhex(x.get('key','')))==1) if a==0x20a5710 else next(x for x in choices if x.get('length')==1) if a==0x20a5820 else choices[0];failures=[]
        for seed in range(16):
            result=run(image,row,body,v,seed,entries)
            if result['modelPassed']:raise ValueError('Whole wrong cipher C did not violate independent invariant')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],returningModelRejections=len(failures),records=failures))
    limits=['Actual complete original/compiled cipher callers return with identical261-byte state/data/seed/position observations, exact canonical Thumb/ARM code graphs and callee-saved ABI. Independent properties check permutation preservation, mathematical reverse-deck default state, keyrand range/zero-limit behavior, derived keyed initial fields, decrypt feedback consistency and array bounds; the cipher algorithm is not reimplemented as its own test oracle.','Byte inputs cover all256 values across four deterministic shuffled states; key initialization includes0/1/3/16/255-byte keys, array lengths include negative/zero/1/2/7/16/64/255. Original ARM unsigned division helper is reached only through its actual native BLX/canonical entry and receives0 extra source credit.','Four whole wrong C units genuinely link at full native extents and actually return state/range/feedback invariant failures. Two byte-feedback/arithmetic and one array off-by-one attempts with different compiled extents are retained as diagnostics and receive0 negative/source credit.','GOADecryptByte identification is established by full146-byte source/native/link equality; comparative encrypt-byte differs140/146. Canonical helper bodies, cryptographic strength/security, network/device/scenes and full native game execution remain uncredited/unproven.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,unsupported=unsupported,canonicalOriginalEntries=list(entries.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
