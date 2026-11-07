import match_runtime
import hashlib
import json
import re
import struct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT,write_json
from wave20261106_dwc_match_continuation_second_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_gpi_buddy_resume_first_fixtures import BASE,STACK,END,CONNECTION,STATE,REGS

OPTION=0x02302000
HELPERS={0x020a3d70:12,0x020a2c80:72}
LIMITS='Complete original/C712-byte minimum-completion callers return on null/invalid option,SC-mode,non-poll state and all-replies polling transitions. One genuine original/C partial stop is before the actual canonical ARM unsigned64-divide entry;0division body instructions or returns. Original Thumb MatchControl getter12 and AID-bitmask72 bodies execute. Clock,status setter,reservation send and postprocess providers are supplied boundaries with0bodyinstructions. Timeout/retry/send-loop/cancel paths beyond that helper are unexecuted. No real clock/network,I/O,callbacks,storage authorship,game scenes,concurrency or Windows/Android execution.'


def case_count(a):return 9


def run(image,row,body,seed,bound=100000,strict=True):
    a=int(row['address'],0)
    if(row.get('program')or'',row['processor'],row['module'],row['mode'],a)!=('','arm9','main','thumb',0x020a2d30):raise ValueError('Exact minimum-completion caller namespace differs')
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(BASE,0x400000);uc.mem_write(BASE,image);uc.mem_write(a,body);uc.mem_map(STACK,0x10000);uc.mem_map(END,0x1000);uc.mem_write(STACK,b'\xa5'*0x10000);sp=STACK+0xf000
    initial=[((i+1)*0x11223344^(seed*0x01010101))&0xffffffff for i in range(13)]
    for r,v in zip(REGS,initial):uc.reg_write(r,v)
    uc.reg_write(UC_ARM_REG_CPSR,0x30|((seed%4)<<28));uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,END|1)
    def sw(p,v):uc.mem_write(p,struct.pack('<I',v&0xffffffff))
    uc.mem_write(STATE,b'\x5a'*1156);uc.mem_write(OPTION,b'\0'*32);sw(0x021d1b88,0 if seed==0 else OPTION);sw(0x021d1b8c,STATE);uc.mem_write(OPTION,bytes([int(seed!=1),32,1,0]));sw(OPTION+4,6000);sw(OPTION+8,0 if seed==8 else 10);sw(OPTION+12,10 if seed==4 else 2);uc.mem_write(STATE+13,b'\x02');uc.mem_write(STATE+21,bytes([2 if seed==2 else 3 if seed==3 else 1 if seed==6 else 0]));uc.mem_write(STATE+720,b'\x00\x01\x03');sw(STATE+416,0 if seed==7 else 19);clock=1000
    before=bytes(uc.mem_read(BASE,0x400000));expected=bytearray(before);calls=[];expected_calls=[];helpers={};providers={};observed=set();failures=[];returned=False;partial=False
    if seed==4:expected[STATE-BASE+22]=2;expected[STATE-BASE+420]=1;expected_calls=[['postprocess',0]]
    if seed in[5,6]:
        struct.pack_into('<Q',expected,OPTION-BASE+24,clock);struct.pack_into('<I',expected,OPTION-BASE+8,0);expected_calls=[['clock'],['set-state',3 if seed==5 else 4]];struct.pack_into('<I',expected,STATE-BASE+416,3 if seed==5 else 4)
        if seed==5:struct.pack_into('<I',expected,STATE-BASE+232,2);struct.pack_into('<Q',expected,STATE-BASE+236,clock);expected_calls+=[['clock']]
        else:expected_calls+=[['reserve-friend',1,0,0]]
    if seed==8:expected_calls=[['clock'],['unsigned64-helper-entry',[64000,0,33514,0]]]
    def finish(v,wide=False):
        for r,x in zip([*REGS[:4],UC_ARM_REG_R12],[v&0xffffffff,(v>>32)&0xffffffff if wide else 0xa1a1a1a1,0xa2a2a2a2,0xa3a3a3a3,0xacacacac]):uc.reg_write(r,x)
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def hook(machine,pc,size,opaque):
        nonlocal returned,partial
        if pc==END:returned=True;machine.emu_stop();return
        if a<=pc<a+len(body):observed.add(pc);return
        if pc in HELPERS:
            if not machine.reg_read(UC_ARM_REG_CPSR)&32:failures.append('Actual original getter/bitmask Thumb mode differs');machine.emu_stop();return
            helpers[hex(pc)]=helpers.get(hex(pc),0)+1
        if any(p<=pc<p+n for p,n in HELPERS.items()):return
        r=[machine.reg_read(x)for x in REGS[:4]];binding=next((b for b in row['nativeSymbolEntries'].values()if b['kind']=='function'and int(b['address'],0)==pc),None)
        if binding and bool(machine.reg_read(UC_ARM_REG_CPSR)&32)!=(binding['mode']=='thumb'):failures.append('Actual supplied provider/helper entry mode differs')
        providers[hex(pc)]=providers.get(hex(pc),0)+1
        if pc==0x02007a9c:calls.append(['clock']);finish(clock,True);return
        if pc==0x020a19b4:calls.append(['postprocess',r[0]]);finish(0);return
        if pc==0x020a3d7c:calls.append(['set-state',r[0]]);sw(STATE+416,r[0]);finish(0);return
        if pc==0x020a13d8:calls.append(['reserve-friend',*r[:3]]);finish(0);return
        if pc==0x020260dc:calls.append(['unsigned64-helper-entry',r]);partial=True;machine.emu_stop();return
        failures.append('Execution escaped declared option caller/helper/provider set:'+hex(pc));machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(a|1,END+4,count=bound)
    if returned!=(seed!=8)or partial!=(seed==8)or calls!=expected_calls:failures.append('Independent full/partial option transition contract differs')
    if bytes(uc.mem_read(BASE,0x400000))!=expected:failures.append('Full protected option/Match/native memory differs')
    if returned and(uc.reg_read(UC_ARM_REG_SP)!=sp or[uc.reg_read(r)for r in REGS[4:12]]!=initial[4:12]):failures.append('Complete option caller stack/callee-save differs')
    if bytes(uc.mem_read(STACK,0xd000))!=b'\xa5'*0xd000:failures.append('Lower stack guard differs')
    value=dict(actualReturn=returned,partialProviderStopped=partial,modelPassed=not failures,failures=failures,calls=calls,expectedCalls=expected_calls,helperEntries=helpers,suppliedProviderEntries=providers,callerInstructionAddresses=sorted(observed))
    if strict and failures:raise ValueError(value)
    return value


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if len(rows)!=1:raise ValueError('Exact single option caller differs')
    row=rows[0];a=int(row['address'],0);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[a-BASE:a-BASE+row['bytes']];body=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();specs=[];records=[]
    for address,n in HELPERS.items():
        line=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(thumb,size=0x%x\) addr:0x%08x'%(n,address),s)),None)
        if line is None:raise ValueError('Actual original helper full mode/extent differs')
        specs.append(dict(address=hex(address),bytes=n,mode='thumb',canonicalInventoryRecord=line,nativeSha256=hashlib.sha256(image[address-BASE:address-BASE+n]).hexdigest(),sourceCredit=0))
    for seed in range(case_count(a)):
        left=run(image,row,native,seed);right=run(image,row,body,seed)
        if left!=right:raise ValueError('Actual original/C option caller observations differ')
        records.append(dict(address=row['address'],case=seed,topReturned=left['actualReturn'],partialProviderStopped=left['partialProviderStopped'],actualOriginalHelperInvocations=sum(left['helperEntries'].values()),suppliedServiceCalls=sum(left['suppliedProviderEntries'].values()),original=left,candidate=right))
    if run(image,row,native,0,bound=1,strict=False)['modelPassed']:raise ValueError('Incomplete prefix admitted')
    result=dict(status='passed',records=records,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*sum(r['topReturned']for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped']for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),suppliedServiceCalls=2*sum(r['suppliedServiceCalls']for r in records),suppliedServiceBodyInstructionsExecuted=0,unsigned64HelperBodyInstructionsExecuted=0,unsigned64HelperReturns=0,boundedPrefixRejected=True,helperSourceCodeCredit=0,limits=LIMITS)
    write_json(LANE/'caller-fixtures.json',result);return result
