import copy
import hashlib
import re
import match_runtime
from project import ROOT,read_json,write_json,sha256
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_SP,UC_ARM_REG_LR
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_REG_R0
from wave20261106_ov000_large_actor_source_second_paths import EVIDENCE
from wave20261106_ov000_large_actor_source_second_bindings import inputs

ADDRESS=0x02028158
STOP=0x0303f000
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]


def signed(value):return(value+0x80000000)%0x100000000-0x80000000


def normalize(value):
    value=signed(value)
    while value>0xb4000:value-=0x168000
    while value < -0xb4000:value+=0x168000
    return value


def qualify(entry,main,inventory):
    if(entry.get('program')or'',entry['processor'],entry['module'],entry['mode'],int(entry['address'],0),entry['bytes'])!=('','arm9','main','arm',ADDRESS,52):raise ValueError('Exact angle helper CPU/program/module/mode/entry/extent differs')
    raw=main[ADDRESS-0x02000000:ADDRESS-0x02000000+52]
    if hashlib.sha256(raw).hexdigest()!=entry['targetSha256']or not re.search(r'^\S+ kind:function\(arm,size=0x34\) addr:0x02028158$',inventory,re.M):raise ValueError('Whole original angle body/canonical boundary differs')
    path=ROOT/entry['sourceUnit']
    if sha256(path)!=entry['sourceSha256']or not re.search(r'void\s+native_main_02028158\s*\(s32\s+arg0\)',path.read_text()):raise ValueError('Preserved accepted void definition differs')
    return raw


def execute():
    value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();entry=next(e for e in value['executedAcceptedHelpers']if int(e['address'],0)==ADDRESS);raw=qualify(entry,main,main_inventory);results=[];cs=Cs(CS_ARCH_ARM,CS_MODE_ARM);cs.detail=True;callers=[]
    for caller in value['entries']:
        for record in caller['originalRelocationRecords']:
            if 'kind:arm_call to:0x02028158 module:main'not in record:continue
            pc=int(re.search(r'from:(0x[0-9a-f]+)',record)[1],0);offset=pc-0x21d7240;call=list(cs.disasm(image[offset:offset+4],pc));following=list(cs.disasm(image[offset+4:offset+20],pc+4))
            if len(call)!=1 or call[0].mnemonic!='bl'or call[0].op_str!='#0x2028158':raise ValueError('Actual normalized-R0 caller BL target differs')
            first=following[0];reads,writes=first.regs_access()
            if ARM_REG_R0 not in reads:
                reads_next=any(ARM_REG_R0 in instruction.regs_access()[0]for instruction in following[:3])
                if not reads_next:raise ValueError('Actual signed-R0 caller consumption absent')
            callers.append(dict(caller=caller['address'],origin=hex(pc),originalRecord=record,nativeCallWord=call[0].bytes.hex(),following=[dict(address=hex(i.address),word=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in following],sourceCredit=0))
    vectors=[0,1,-1,0xb4000-1,0xb4000,0xb4000+1,-0xb4000-1,-0xb4000,-0xb4000+1,0x168000-1,0x168000,0x168000+1,-0x168000-1,-0x168000,-0x168000+1,0x7fffffff,-0x80000000,0x7ffffffe,-0x7fffffff]
    for index,argument in enumerate(vectors):
        uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x02000000,0x100000);uc.mem_map(0x03000000,0x40000);uc.mem_write(ADDRESS,raw);uc.reg_write(UC_ARM_REG_R0,argument&0xffffffff);uc.reg_write(UC_ARM_REG_SP,0x03030000);uc.reg_write(UC_ARM_REG_LR,STOP);saved=[0x44440000+i for i in range(8)]
        for reg,word in zip(SAVED,saved):uc.reg_write(reg,word)
        seen=[];returned=False
        def hook(machine,pc,size,user):
            nonlocal returned
            if pc==STOP:returned=True;machine.emu_stop();return
            if not ADDRESS<=pc<ADDRESS+52:raise ValueError('Original angle execution left actual complete body')
            seen.append(pc)
        uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(ADDRESS,STOP+4,count=30000);actual=signed(uc.reg_read(UC_ARM_REG_R0));expected=normalize(argument)
        if not returned or actual!=expected or uc.reg_read(UC_ARM_REG_SP)!=0x03030000 or[uc.reg_read(r)for r in SAVED]!=saved:raise ValueError('Actual native angle signed-R0 return or preservation differs')
        results.append(dict(argument=argument,actualSignedR0=actual,expectedSignedR0=expected,returned=True,instructions=len(seen)))
    negatives=[]
    for key,wrong in [('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address',hex(ADDRESS+4)),('bytes',48),('targetSha256','0'*64)]:
        bad=copy.deepcopy(entry);bad[key]=wrong
        try:qualify(bad,main,main_inventory)
        except ValueError as error:negatives.append(dict(case=key,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong angle return identity accepted')
    changed=bytearray(main);changed[ADDRESS-0x02000000]^=1
    try:qualify(entry,bytes(changed),main_inventory)
    except ValueError as error:negatives.append(dict(case='native-body',rejected=True,reason=str(error)))
    else:raise ValueError('Altered native angle body accepted')
    result=dict(passed=True,kind='zero-byte-accepted-interface-debt',sourceOrCalleeCredit=0,migratedAcceptedDefinition=False,canonicalCallee=entry,actualNativeStandaloneReturns=len(results),actualCallerReturnConsumption=callers,vectors=results,negativeControls=negatives,existingAcceptedSignedDeclaration=dict(path='src/runtime/parallel_wave20261104/main-arm-front/second/context.h',sha256=sha256(ROOT/'src/runtime/parallel_wave20261104/main-arm-front/second/context.h')),limitation='Original52-byte helper returns normalized signedR0; accepted runtime06 C definesvoid. New callers use measureds32 declaration. No accepted source/type migration or callee semantic repair is claimed.')
    write_json(EVIDENCE/'angle-return-interface-debt.json',result);return result
