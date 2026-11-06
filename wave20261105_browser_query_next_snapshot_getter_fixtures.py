import hashlib
import json
import random
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_browser_query_next_snapshot_getter_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_browser_query_next_snapshot_getter_build import build

OUTPUT,GLOBAL,STOP,SP=0x2170000,0x21d2318,0x27e0000,0x2701000
COPY=0x2008e0c


def helper(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text().splitlines();record=next((x for x in inventory if re.fullmatch(r'\S+ kind:function\(arm,size=0x130\) addr:0x02008e0c',x)),None)
    if record is None:raise ValueError('Actual canonical ARM304 copy entry absent')
    return dict(address=COPY,mode='arm',bytes=304,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[COPY-0x2000000:COPY-0x2000000+304]).hexdigest(),sourceCredit=0)


def model(raw):
    bits=int.from_bytes(raw,'little');mask=(1<<43)-1;return struct.pack('<QQHH',bits&mask,(bits>>43)&mask,(bits>>86)&1023,(bits>>96)&65535)


def run(image,row,body,v,seed,copy):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);raw=bytes.fromhex(v['raw']);globalguard=bytes([0x37])*8+raw+bytes([0xa7])*8;cpu.mem_write(GLOBAL-8,globalguard);initialout=bytes((i*11+seed)&255 for i in range(20));outputguard=bytes([0xbb])*8+initialout+bytes([0xcc])*8;cpu.mem_write(OUTPUT-8,outputguard);initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1];initial[0]=OUTPUT
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    returned=False;pcs=[];helper_entries=[]
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if a<=at<a+row['bytes']:mode='thumb'
        elif COPY<=at<COPY+copy['bytes']:mode='arm'
        else:raise ValueError(('Getter escaped actual bounded original graph',hex(at)))
        if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError('Getter/helper actual entry mode differs')
        if at==COPY:helper_entries.append(at)
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP or OUTPUT<=at and at+size<=OUTPUT+20):raise ValueError(('Getter unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP or len(helper_entries)!=4:raise ValueError('Getter full return/copy invocation/callee-saved ABI differs')
    actual=bytes(cpu.mem_read(OUTPUT,20));guards=bytes(cpu.mem_read(GLOBAL-8,30))==globalguard and bytes(cpu.mem_read(OUTPUT-8,8))==bytes([0xbb])*8 and bytes(cpu.mem_read(OUTPUT+20,8))==bytes([0xcc])*8
    return dict(address=row['address'],vector=v,seed=seed,topReturned=True,rawReturnRegister=regs[0],modelPassed=actual==model(raw) and guards,output=actual.hex(),expected=model(raw).hex(),calleeSavedAbiPreserved=True,inputAndOutputGuardsPreserved=guards,actualOriginalHelperInvocations=len(helper_entries),initialCallerExcludedFromHelperMetric=True,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def vectors():
    rng=random.Random(0x4660);values=[bytes(14),bytes([255])*14,*[(1<<b).to_bytes(14,'little') for b in range(112)],*[bytes(rng.randrange(256) for i in range(14)) for n in range(16)]];return [dict(raw=v.hex()) for v in values]


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();copy=helper(image);records=[];negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(vectors()):
            original=run(image,row,native,v,seed,copy);source=run(image,row,linked,v,seed,copy)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent packed112-bit getter model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/'wrong-C';folder.mkdir(parents=True,exist_ok=True);source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();changed=text.replace('out->first&=0x7ffffffffffULL','out->first&=0x3ffffffffffULL',1)
        if changed==text:raise ValueError('Whole getter C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Wrong whole getter C changed native extent')
        failures=[]
        for seed in range(16):
            result=run(image,row,body,dict(raw=(1<<42).to_bytes(14,'little').hex()),seed,copy)
            if result['modelPassed']:raise ValueError('Wrong getter mask did not violate independent complete model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],returningModelRejections=len(failures),records=failures))
    limits=['130 actual native/genuine compiled complete caller vectors execute real canonical ARM304 copy code four times per caller. Every112 input bit,zero/all-one and16 deterministic random RAM inputs match an independent43/43/10/16-bit little-endian mathematical model; all caller returns/callee-saved ABI and input/output guards are observed.','One same-extent whole wrong C mask genuinely links and returns16 independent model failures; wrong unsigned64/structure geometry is rejected by the measured compiler.','Four canonical BSS reads overlap by measured bits; minimum accessed ranges are witnesses only, not complete object extents or data storage/source authorship. Numeric source field names convey no account/channel/firmware semantic qualification.','No hardware/FIFO service, whole game scene, network or Windows execution occurs. Original copy helper source reconstruction receives0 additional credit.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalHelperEntries=[copy],nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
