import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json
from wave20261106_dwc_match_next_seventh_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_match_next_seventh_build import build
from wave20261106_dwc_match_next_seventh_helpers import EXPECTED,validate,validate_layout

ADDRESS,STATE,BITMAP,GLOBAL,CTRL,STOP,SP=0x209c05c,0x209be60,0x209beac,0x21d19e0,0x2171000,0x27e0000,0x2701000
PROVIDERS={0x209f1c0,0x209f640}


def vector(seed):
    return dict(error=[0,0,0,1,6,9][seed%6],cancel=seed%3==0,matchState=[0,3][(seed//4)%2],connections=seed%4,profileMatch=seed%5!=0,self=seed%2,server=seed%3==1,index=seed%4,coreState=[2,3,5,6][seed%4])


def run(image,row,body,v,seed):
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(ADDRESS,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);context=bytearray([0x61])*2048;struct.pack_into('<II',context,0x24,v['coreState'],0x12345678);struct.pack_into('<I',context,0x64,42 if v['profileMatch'] else 99);struct.pack_into('<I',context,0x518,v['matchState']);context[0x385]=v['connections'];aids=[0,31,3,7];context[0x648:0x64c]=bytes(aids);struct.pack_into('<iiii',context,0x46c,11,42,13,14);expected_context=bytearray(context);early=v['error']==0 and v['cancel'] and v['matchState']==0;set_state=v['error']==0 and not v['cancel'];bitmap_value=0
    if not early:
        if set_state:
            struct.pack_into('<II',expected_context,0x24,6,v['coreState'])
            if v['profileMatch'] and v['connections']>=1:expected_context[0x2c]=31
        for aid in aids[:v['connections']+1]:bitmap_value|=1<<aid
        struct.pack_into('<I',expected_context,0x668,bitmap_value)
    cpu.mem_write(GLOBAL,struct.pack('<I',CTRL));cpu.mem_write(CTRL,bytes(context));initial=[0x64d00000+i*0x101+seed for i in range(15)];initial[:4]=[v['error'],int(v['cancel']),v['self'],int(v['server'])];initial[-2:]=[SP,STOP|1];cpu.mem_write(SP,struct.pack('<II',v['index'],0x12348899));cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    expected=dict(kind='provider',address=hex(0x209f1c0 if early else 0x209f640));observed=None;interface=True;pcs=[];counts={STATE:0,BITMAP:0};checked={STATE:0,BITMAP:0};helper_return=None;saved=None;helper_kind=None
    def code(machine,at,size,user):
        nonlocal observed,interface,helper_return,saved,helper_kind
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if helper_return is not None and at==helper_return:
            if regs[4:12]!=saved[0] or regs[13]!=saved[1]:raise ValueError('Actual accepted helper return ABI differs')
            if helper_kind==BITMAP and regs[0]!=bitmap_value:interface=False
            checked[helper_kind]+=1;helper_return=None
        if at in EXPECTED:
            helper_kind=at;counts[at]+=1;helper_return=regs[14]&~1;saved=(regs[4:12],regs[13]);interface=interface and (regs[0]==6 if at==STATE else regs[:2]==[CTRL+0x648,v['connections']+1])
        for start,hexadecimal in EXPECTED.items():
            if start<=at<start+len(bytes.fromhex(hexadecimal)):
                if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual accepted helper mode differs')
                return
        if at in PROVIDERS:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual callback provider mode differs')
            observed=dict(kind='provider',address=hex(at));machine.emu_stop();return
        if at==STOP or not ADDRESS<=at<ADDRESS+len(body) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Callback escaped bounded caller/helpers before provider')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if (at,size) in [(CTRL+0x24,4),(CTRL+0x28,4),(CTRL+0x2c,1),(CTRL+0x668,4)]:return
        raise ValueError('Unexpected callback/helper write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(ADDRESS|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Callback did not reach bounded provider')
    helpers_ok=counts==checked=={STATE:int(set_state and not early),BITMAP:int(not early)};memory=bytes(cpu.mem_read(CTRL,2048))==expected_context and struct.unpack('<I',cpu.mem_read(GLOBAL,4))[0]==CTRL
    return dict(address=row['address'],seed=seed,vector=v,observed=observed,expected=expected,topReturned=False,partialProviderStopped=True,modelPassed=observed==expected and memory and interface and helpers_ok,providerInterfaceModelPassed=interface,independentMutationModelPassed=memory,actualOriginalHelperInvocations=sum(counts.values()),actualOriginalStateHelperInvocations=counts[STATE],actualOriginalBitmapHelperInvocations=counts[BITMAP],actualHelpersReturnedAndAbiPassed=helpers_ok,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();records_text=(ROOT/'config/arm9/relocs.txt').read_text();validate(read_json(LANE/'helpers.json'),image,inventory,records_text);validate_layout(read_json(LANE/'initializer-layout.json'),image,inventory,records_text);proof=read_json(LANE/'helpers-proof.json')
    if proof['root']!=str(ROOT) or proof['status']!='passed' or proof['standaloneOriginalEntries']!=128:raise ValueError('Fresh actual helper qualification absent')
    records=[];negatives=[]
    for row in rows:
        native=image[ADDRESS-0x2000000:ADDRESS-0x2000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);left=run(image,row,native,v,seed);right=run(image,row,compiled,v,seed)
            if left!=right or not left['modelPassed']:raise ValueError(('Independent callback/helper state/bitmap model differs',left,right))
            records.append(left)
        directory=WORK/'wrong-c/0209c05c';directory.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
        text=(ROOT/row['source']).read_text();before='stpDwcCnt->matchcnt.aidList, stpDwcCnt->matchcnt.gt2NumConnection + 1';changed=text.replace(before,'stpDwcCnt->matchcnt.aidList, stpDwcCnt->matchcnt.gt2NumConnection + 0',1)
        if changed==text:raise ValueError('Whole callback count negative did not mutate')
        source=directory/'wrong.c';source.write_text(changed);bad,body=build(source,directory/'proof',negative=True);failed=sum(not run(image,row,body,vector(seed),seed)['modelPassed'] for seed in range(16))
        if not failed:raise ValueError('Genuine wrong callback count did not reject independent helper/bitmap model')
        negatives.append(dict(address=row['address'],genuinelyLinked=True,matchedNative=False,independentModelFailures=failed,changedExpression=[before,'connection count without+1'],realLink=bad['realLink']))
    coverage=sorted({r['observed']['address'] for r in records})
    if coverage!=sorted(hex(a) for a in PROVIDERS):raise ValueError('Callback provider branch coverage incomplete')
    limits=['128 paired actual original/source callback entries,0caller returns; stop before ClearQR2Key or SetNumValidConnection. Actual original accepted20-byte SetState and32-byte bitmap helper bodies execute and return;128 separate standalone original helper entries/strict negative contracts qualify them.0new helper source credit.','Connection counts0..3, aids0..31, initialized core/match fields, null-free context and bounded profile-list matches only. State/last-state/aid/bitmap mutations and no-other-write model qualified.0callback/QR2/valid-count/network/device/hardware/game/nativeWindows provider execution or synthetic returns.','Main initializer pointer construction is original-byte/namespace/inventory evidence only;0initializer instructions executed.96-byte inter-start span includes opaque gap; formal FriendControl type size and storage extent/authorship stay unproven.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,requiredProviderBranchCoverage=coverage,nativeAndCompiledReturningCalls=0,nativeAndCompiledPartialStops=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),standaloneOriginalHelperEntries=128,wholeCNegativeControlsRejected=len(negatives),wrongC=negatives,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
