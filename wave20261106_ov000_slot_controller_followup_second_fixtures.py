import hashlib
import json
import struct
import match_runtime
from project import ROOT,write_json
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from wave20261106_ov000_slot_controller_followup_second_paths import EVIDENCE
from wave20261106_ov000_slot_controller_followup_second_bindings import inputs

REG=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
BASE=0x21d7240
STACK=0x3030000
STOP=0x303f000
LINK=0x3010000
TABLE=0x2102a18
SERVICES={0x20602ec:(6,None),0x2206ab8:(6,4),0x2206a20:(4,2),0x204a154:(6,1)}


def words(values):return struct.pack('<'+'I'*len(values),*[v&0xffffffff for v in values])
def s16(value):return (value&65535)-65536 if value&32768 else value&65535
def make_case(address,index):
    if address!=0x220820c:raise ValueError('Unmodeled point caller')
    return dict(index=index,args=[0x12345678+index,0x87654321-index,[0,99,100,127,128,227,0xffffff80,0xffffffff][index],[0,0x7fff,0x8000,0xffff,0x10000,0xffff0001,0x8000ffff,0xffffffff][index]],delta1=[0,1,-1,32767,-32768,40,-40,300][index],delta2=[1,-1,20,-20,32767,-32768,0,80][index],replace1=-32768 if index%3==2 else None,replace2=32760 if index%2 else None)


def execute_one(row,body,case,main,image):
    address=int(row['address'],0)
    if(address,row['bytes'])!=(0x220820c,232):raise ValueError('Point caller whole identity differs')
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x2000000,0x400000);uc.mem_map(0x3000000,0x40000);uc.mem_write(0x2000000,main);uc.mem_write(BASE,image);uc.mem_write(address,body)
    uc.mem_write(TABLE+8*12,words([LINK,0x87654321,0xabcdef01]));uc.mem_write(LINK,words([0x12345678,0x3011000]));uc.mem_write(STACK,bytes(64));uc.reg_write(UC_ARM_REG_SP,STACK);uc.reg_write(UC_ARM_REG_LR,STOP)
    for reg,value in zip(REG,case['args']):uc.reg_write(reg,value)
    saved=[0x11110000+i*0x101 for i in range(8)]
    for reg,value in zip(SAVED,saved):uc.reg_write(reg,value)
    events=[];provider_writes=[];persistent=[];pointers=[];helpers=0;helper_instructions=0;services=0;caller_instructions=0;done=False
    def capture(machine,pc,count,pair_index):
        values=[machine.reg_read(r)for r in REG[:min(count,4)]]
        if count>4:values+=list(struct.unpack('<'+'I'*(count-4),machine.mem_read(machine.reg_read(UC_ARM_REG_SP),4*(count-4))))
        event=dict(address=hex(pc),args=values)
        if pair_index is not None:
            pointer=values[pair_index]
            if not STACK-0x200<=pointer<=STACK-4 or pointer%4:raise ValueError('Point provider received invalid caller stack object')
            pointers.append(pointer);event['point']=list(struct.unpack('<hh',machine.mem_read(pointer,4)))
        events.append(event)
        return values
    def hook(machine,pc,size,user):
        nonlocal helpers,helper_instructions,services,caller_instructions,done
        if pc==STOP:done=True;machine.emu_stop();return
        if pc==0x2049ad0:helpers+=1;capture(machine,pc,1,None)
        if 0x2049ad0<=pc<0x2049ae4:helper_instructions+=1;return
        if pc in SERVICES:
            services+=1;count,pair_index=SERVICES[pc];values=capture(machine,pc,count,pair_index);result=0xdeadbeef
            if pc in[0x2206ab8,0x2206a20]:
                which=1 if pc==0x2206ab8 else 2;replacement=case['replace'+str(which)]
                if replacement is not None:
                    machine.mem_write(values[pair_index],struct.pack('<h',replacement));provider_writes.append(dict(provider=hex(pc),halfword0=replacement))
                result=case['delta'+str(which)]&0xffffffff
            for reg in REG+[UC_ARM_REG_R12]:machine.reg_write(reg,0xa1000000+services*0x100+reg)
            machine.reg_write(UC_ARM_REG_R0,result);machine.reg_write(UC_ARM_REG_CPSR,(machine.reg_read(UC_ARM_REG_CPSR)&0xfffffff)|0x50000000);machine.reg_write(UC_ARM_REG_PC,machine.reg_read(UC_ARM_REG_LR));return
        if not address<=pc<address+len(body):raise ValueError(('Point execution left actual caller/helper/provider closure',hex(pc)))
        caller_instructions+=1
    def memory(machine,access,target,size,value,user):
        if not STACK-0x1000<=target<STACK+0x1000:persistent.append(dict(address=hex(target),bytes=size,value=value))
    uc.hook_add(UC_HOOK_CODE,hook);uc.hook_add(UC_HOOK_MEM_WRITE,memory);uc.emu_start(address,STOP+4,count=1500)
    if not done or uc.reg_read(UC_ARM_REG_SP)!=STACK or[uc.reg_read(r)for r in SAVED]!=saved:raise ValueError('Point whole caller return/SP/saved registers differ')
    if len(set(pointers))!=1:raise ValueError('Provider point object identity changed')
    pointer=pointers[0];args=case['args'];point=[120,s16(args[3])];expected=[dict(address=hex(0x2049ad0),args=[8]),dict(address=hex(0x20602ec),args=[LINK,args[0],args[1],24,args[3],1]),dict(address=hex(0x2206ab8),args=[8,5,1,1,pointer,0],point=point[:])];expected_provider=[]
    if case['replace1']is not None:point[0]=case['replace1'];expected_provider.append(dict(provider=hex(0x2206ab8),halfword0=point[0]))
    point[0]=s16(point[0]+case['delta1']);expected.append(dict(address=hex(0x2206a20),args=[8,0x222f73c,pointer,0],point=point[:]))
    if case['replace2']is not None:point[0]=case['replace2'];expected_provider.append(dict(provider=hex(0x2206a20),halfword0=point[0]))
    point[0]=s16(point[0]+case['delta2']);value=(args[2]&~0x80)&255
    if value<100:expected.append(dict(address=hex(0x204a154),args=[8,pointer,5 if args[2]&0x80 else 1,value,2,0],point=point[:]))
    if(events,provider_writes,persistent)!=(expected,expected_provider,[]):raise ValueError(('Independent narrow ABI/field/order model differs',row['address'],case,events,expected,provider_writes,expected_provider,persistent))
    result=dict(events=events,providerSuppliedStackMutations=provider_writes,orderedPersistentWrites=persistent,gprs=[uc.reg_read(r)for r in REG+SAVED+[UC_ARM_REG_R12,UC_ARM_REG_SP]],cpsr=uc.reg_read(UC_ARM_REG_CPSR))
    return result,dict(helperInvocations=helpers,helperInstructions=helper_instructions,serviceEntries=services,callerInstructions=caller_instructions)


def execute(rows):
    value,image,inventory,relocations,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();records=[];helpers=0;helper_instructions=0;services=0
    for row in rows:
        address=int(row['address'],0);native=image[address-BASE:address-BASE+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        for index in range(8):
            case=make_case(address,index);pair=[];counts=[]
            for body in[native,compiled]:
                result,count=execute_one(row,body,case,main,image);pair.append(result);counts.append(count);helpers+=count['helperInvocations'];helper_instructions+=count['helperInstructions'];services+=count['serviceEntries']
            if pair[0]!=pair[1]:raise ValueError('Original/compiled point caller effects differ')
            records.append(dict(address=row['address'],case=case,result=pair[0],executions=counts,returned=True))
    trace=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest();limits=['Synthetic valid slot/link and aligned signed-halfword stack-point domains only; no gameplay/render/device execution.','Actual original accepted main getter20B executes; four opaque providers supply bounded returns and explicit optional point mutations, execute0body instructions and earn0source/storage credit.','Models cover low-byte mask,99/100 boundary,high-bit style,word-to-signed16 truncation,post-provider point rereads and16-bit wrap; signed32 sums remain within defined int range.','Imported literal/global declarations express pointers only, with0initialized storage ownership; nominal portable type unification and void-return meanings remain unproved.']
    result=dict(passed=True,functions=len(rows),vectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualOriginalHelperInvocations=helpers,actualOriginalHelperInstructions=helper_instructions,suppliedServiceCalls=services,suppliedServiceBodyInstructionsExecuted=0,traceSha256=trace,limits=limits,records=records);write_json(EVIDENCE/'caller-fixtures.json',result);return result
