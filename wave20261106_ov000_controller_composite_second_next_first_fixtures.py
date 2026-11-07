import hashlib
import json
import struct
import match_runtime
from project import ROOT,write_json
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from wave20261106_ov000_controller_composite_second_next_first_paths import EVIDENCE
from wave20261106_ov000_controller_composite_second_next_first_bindings import inputs

REG=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
BASE=0x21d7240
TABLE=0x2102a18
STACK=0x3030000
STOP=0x303f000
SERVICES={0x204a010:5,0x204a104:4,0x204a154:6}


def words(values):return struct.pack('<'+'I'*len(values),*[v&0xffffffff for v in values])
def halfs(values):return struct.pack('<HH',*[v&65535 for v in values])
def s16(value):return(value&65535)-65536 if value&32768 else value&65535
def resource(slot):return 0x3014000+slot*256
def event(pc,args,point=None):
    value=dict(address=hex(pc),args=[v&0xffffffff for v in args])
    if point is not None:value['point']=point
    return value
def make_case(address,index):return dict(index=index,args=[0x87654321+index,0xffffffff-index],textX=[0,32760,32767,-32768,-1,72,128,255][index],textY=[0,-32768,32767,1][index%4],numericY=[13,-1,32767,-32768][index%4])


def execute_one(row,body,case,main,image):
    address=int(row['address'],0)
    if(address,row['bytes'])!=(0x21ec044,272):raise ValueError('Two-point complete caller identity differs')
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x2000000,0x400000);uc.mem_map(0x3000000,0x40000);uc.mem_write(0x2000000,main);uc.mem_write(BASE,image);uc.mem_write(address,body)
    for slot in[7,8]:
        link=0x3010000+slot*32;uc.mem_write(TABLE+slot*12,words([link,0x12345678,0x87654321]));uc.mem_write(link,words([0,resource(slot)]));uc.mem_write(resource(slot),bytes(108))
    uc.mem_write(STACK,bytes(64));uc.reg_write(UC_ARM_REG_SP,STACK);uc.reg_write(UC_ARM_REG_LR,STOP)
    for reg,value in zip(REG,case['args']+[0,0]):uc.reg_write(reg,value&0xffffffff)
    saved=[0x11110000+i*0x101 for i in range(8)]
    for reg,value in zip(SAVED,saved):uc.reg_write(reg,value)
    events=[];persistent=[];pointers=[];helpers=0;helper_instructions=0;services=0;caller_instructions=0;done=False
    def capture(machine,pc,count):
        args=[machine.reg_read(r)for r in REG[:min(count,4)]]
        if count>4:args+=list(struct.unpack('<'+'I'*(count-4),machine.mem_read(machine.reg_read(UC_ARM_REG_SP),4*(count-4))))
        point=None
        if pc in[0x204a104,0x204a154]:
            pointer=args[1]
            if not STACK-0x100<=pointer<=STACK-4 or pointer%4:raise ValueError('Two-point caller stack extent/alignment differs')
            pointers.append(pointer);point=list(struct.unpack('<hh',machine.mem_read(pointer,4)))
        events.append(event(pc,args,point));return args
    def hook(machine,pc,size,user):
        nonlocal helpers,helper_instructions,services,caller_instructions,done
        if pc==STOP:done=True;machine.emu_stop();return
        if pc==0x2049ad0:helpers+=1;capture(machine,pc,1)
        if 0x2049ad0<=pc<0x2049ae4:helper_instructions+=1;return
        if pc in SERVICES:
            services+=1;args=capture(machine,pc,SERVICES[pc]);result=0xdeadbeef
            if pc==0x204a104:machine.mem_write(args[1],halfs([case['textX'],case['textY']]))
            elif pc==0x204a154:machine.mem_write(args[1],halfs([-7,case['numericY']]));result=0xc0000000+args[0]
            for reg in REG+[UC_ARM_REG_R12]:machine.reg_write(reg,0xa1000000+services*0x100+reg)
            machine.reg_write(UC_ARM_REG_R0,result);machine.reg_write(UC_ARM_REG_CPSR,(machine.reg_read(UC_ARM_REG_CPSR)&0xfffffff)|0xa0000000);machine.reg_write(UC_ARM_REG_PC,machine.reg_read(UC_ARM_REG_LR));return
        if not address<=pc<address+len(body):raise ValueError(('Two-point execution left proven native closure',hex(pc)))
        caller_instructions+=1
    def memory(machine,access,target,size,value,user):
        if not STACK-0x1000<=target<STACK+0x1000:persistent.append(dict(address=hex(target),bytes=size,value=value))
    uc.hook_add(UC_HOOK_CODE,hook);uc.hook_add(UC_HOOK_MEM_WRITE,memory);uc.emu_start(address,STOP+4,count=2000)
    if not done or uc.reg_read(UC_ARM_REG_SP)!=STACK or[uc.reg_read(r)for r in SAVED]!=saved:raise ValueError('Two-point return/SP/callee-saved registers differ')
    if len(set(pointers))!=1:raise ValueError('Two-point stack object identity changed')
    point=pointers[0];expected=[];y=0
    for slot,value,text in[(7,case['args'][0],0x222ee48),(8,case['args'][1],0x222ee4c)]:
        expected.extend([event(0x2049ad0,[slot]),event(0x204a010,[resource(slot),88,0,80,16]),event(0x204a104,[slot,point,1,text],[72,y]),event(0x204a154,[slot,point,1,value,7,0],[s16(case['textX']+8),case['textY']])]);y=case['numericY']
    if(events,persistent,uc.reg_read(UC_ARM_REG_R0))!=(expected,[],0xc0000008):raise ValueError(('Independent two-point ABI/mutation/order model differs',row['address'],case,events,expected,persistent))
    return dict(events=events,orderedPersistentWrites=persistent,gprs=[uc.reg_read(r)for r in REG+SAVED+[UC_ARM_REG_R12,UC_ARM_REG_SP]],cpsr=uc.reg_read(UC_ARM_REG_CPSR)),dict(helperInvocations=helpers,helperInstructions=helper_instructions,serviceEntries=services,callerInstructions=caller_instructions)


def execute(rows):
    value,image,inventory,relocations,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();records=[];helpers=0;helper_instructions=0;services=0
    for row in rows:
        address=int(row['address'],0);native=image[address-BASE:address-BASE+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        for index in range(8):
            case=make_case(address,index);pair=[];counts=[]
            for body in[native,compiled]:
                result,count=execute_one(row,body,case,main,image);pair.append(result);counts.append(count);helpers+=count['helperInvocations'];helper_instructions+=count['helperInstructions'];services+=count['serviceEntries']
            if pair[0]!=pair[1]:raise ValueError('Original/source two-point complete effects differ')
            records.append(dict(address=row['address'],case=case,result=pair[0],executions=counts,returned=True))
    trace=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest();limits=['Synthetic mapped slots7/8,link/resource and one aligned signed-halfword stack point only;no gameplay/graphics/device execution.','Actual original main49ad020B executes twice per caller; other three provider entrypoints have bounded supplied arguments/point mutations/returns/clobbers and execute0body instructions.','Models cover halfword +8 wrap,provider-mutated point rereads and preservation of y between the two groups;final raw provider return word has no inferred game-purpose meaning.','No imported provider/literal/global storage or nominal portable type credit; string pointers are passed without claiming original text ownership or rendering semantics.']
    result=dict(passed=True,functions=len(rows),vectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualOriginalHelperInvocations=helpers,actualOriginalHelperInstructions=helper_instructions,suppliedServiceCalls=services,suppliedServiceBodyInstructionsExecuted=0,traceSha256=trace,limits=limits,records=records);write_json(EVIDENCE/'caller-fixtures.json',result);return result
