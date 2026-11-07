import hashlib
import json
import struct
import match_runtime
from project import ROOT,write_json
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from wave20261106_ov000_slot_controller_followup_first_paths import EVIDENCE
from wave20261106_ov000_slot_controller_followup_first_bindings import inputs

REG=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
HELPERS={0x2049ad0:(20,1),0x2049be4:(172,11),0x2049ffc:(20,1)}
SERVICES={0x205fe20:1,0x205fe74:11,0x21ef688:9,0x21ef1cc:1,0x21ef2a8:2,0x204b53c:2,0x205f9e4:1,0x2207b7c:1,0x2208918:1,0x2216260:9,0x204a04c:4,0x206db90:1,0x2045dc4:6,0x2087e44:2}
BASE=0x21d7240
STACK=0x3030000
STOP=0x303f000
LINK=0x3010000
RESOURCE=0x3011000
SELECTION=0x3012000
COUNTER=0x3013000
TABLE=0x2102a18
FLAG=0x2101ae8+0xc84


def words(values):return struct.pack('<'+'I'*len(values),*[v&0xffffffff for v in values])
def s8(value):return (value&255)-256 if value&128 else value&255
def event(address,args,pair=None):
    value=dict(address=hex(address),args=[v&0xffffffff for v in args])
    if pair is not None:value['pair16']=pair
    return value


def make_case(address,index):
    return dict(index=index,selector=[0,3,-1,127,-128,1,19,4][index],first=[0,0xffffffff,3,128][index%4],base=[0,1,3,0][index%4],value=[0,2,127,-128,255,1,19,4][index],occupied=index%4!=1,enabled=[0,1,0xffffffff][index%3],flags=[0,0xffffffff,0x80000002][(index//2)%3],counter=[0,1,0xffffffff,0xffff8000][index%4],width=[255,0,1,255][index%4],height=[255,2,0,255][index%4],tag=[-128,-1,127,0][index%4],valueByte=[0,253,254,255,128,1,2,127][index],handle=[0,0x12345678,0x87654321][index%3],secondHandle=[0,0xabcdef01][index%2],resourceTail=index%2,indexReturn=index%3)


def execute_one(row,body,case,main,image):
    address=int(row['address'],0);index=case['index'];selector=case['selector'];selected=s8(case['first']-case['base']+case['value'])
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x2000000,0x400000);uc.mem_map(0x3000000,0x40000)
    uc.mem_write(0x2000000,main);uc.mem_write(BASE,image);uc.mem_write(address,body)
    uc.mem_write(0x21029c8,bytes([3,7,2,9,4,8,1,6]));uc.mem_write(0x21029d0,bytes([5,11,1,2,3,4,6,7]))
    slots={selector,selected,0,18,19};entry_words={slot:bytearray(words([LINK if case['occupied']else 0,0x7f80ff11,0x87654321]))for slot in slots}
    if address in[0x2206868,0x22162e4]:entry_words[selector if address==0x2206868 else 0][:4]=words([LINK])
    for slot,data in entry_words.items():uc.mem_write(TABLE+12*slot,bytes(data))
    resource=bytearray((i*19+index*31)&255 for i in range(100));struct.pack_into('<I',resource,24,case['flags']);struct.pack_into('<I',resource,68,0x13579bdf);struct.pack_into('<I',resource,96,case['resourceTail'])
    resource[28:32]=bytes([0,128,255,1]if index%2==0 else[255,1,128,0]);resource[92:96]=bytes([1,128,255,0]if index%2==0 else[255,0,1,128])
    uc.mem_write(LINK,bytes([128,0xc1,0xc2,0xc3])+words([RESOURCE]));uc.mem_write(RESOURCE,bytes(resource));uc.mem_write(SELECTION,words([case['first'],case['base']]));uc.mem_write(COUNTER,words([case['counter']]))
    uc.mem_write(0x2236da4,words([0x33333333,case['handle']]));uc.mem_write(0x22382c8+0x118,words([case['handle']]));uc.mem_write(0x22383e8+0x10c,words([case['handle'],case['secondHandle']]))
    uc.mem_write(0x224536c+16,bytes([case['tag']&255]));uc.mem_write(FLAG,words([0x12345678]));table=bytes((i*13+29)&255 for i in range(36));uc.mem_write(0x2246227,table)
    if address==0x21efec4:args=[case['valueByte'],selector]
    elif address in[0x21f29ac,0x2207acc,0x2208854]:args=[SELECTION,case['value']]
    elif address==0x2206868:args=[selector,128+index,255-index,255,index,case['width'],case['height'],case['tag'],case['enabled'],COUNTER]
    elif address==0x22162e4:args=[]
    elif address==0x221d05c:args=[selector,case['enabled']]
    else:raise ValueError('Unmodeled caller identity')
    uc.mem_write(STACK,words(args[4:]+[0]*8));uc.reg_write(UC_ARM_REG_SP,STACK);uc.reg_write(UC_ARM_REG_LR,STOP)
    for reg,value in zip(REG,args[:4]+[0]*(4-len(args))):uc.reg_write(reg,value&0xffffffff)
    saved=[0x11110000+i*0x101 for i in range(8)]
    for reg,value in zip(SAVED,saved):uc.reg_write(reg,value)
    events=[];writes=[];helpers=0;helper_instructions=0;services=0;done=False;caller_instructions=0
    def capture(machine,pc,count):
        values=[machine.reg_read(reg)for reg in REG[:min(count,4)]]
        if count>4:values+=list(struct.unpack('<'+'I'*(count-4),machine.mem_read(machine.reg_read(UC_ARM_REG_SP),4*(count-4))))
        if pc==0x204b53c and not(STACK-0x200<=values[1]<=STACK-4 and values[1]%4==0):raise ValueError('Caller pair is not its bounded aligned stack object')
        pair=list(struct.unpack('<HH',machine.mem_read(values[1],4)))if pc==0x204b53c else None
        events.append(event(pc,values,pair))
    def hook(machine,pc,size,user):
        nonlocal helpers,helper_instructions,services,done,caller_instructions
        if pc==STOP:done=True;machine.emu_stop();return
        if pc in HELPERS:helpers+=1;capture(machine,pc,HELPERS[pc][1])
        if any(a<=pc<a+span for a,(span,count)in HELPERS.items()):helper_instructions+=1;return
        if pc in SERVICES:
            services+=1;capture(machine,pc,SERVICES[pc]);result=LINK if pc==0x205fe20 else case['indexReturn']if pc==0x206db90 else 0xdeadbeef
            for reg in REG+[UC_ARM_REG_R12]:machine.reg_write(reg,0xa1000000+services*0x100+reg)
            machine.reg_write(UC_ARM_REG_R0,result);machine.reg_write(UC_ARM_REG_CPSR,(machine.reg_read(UC_ARM_REG_CPSR)&0xfffffff)|0xa0000000);machine.reg_write(UC_ARM_REG_PC,machine.reg_read(UC_ARM_REG_LR));return
        if not address<=pc<address+len(body):raise ValueError(('Execution left explicit caller/helper/provider closure',hex(pc)))
        caller_instructions+=1
    def memory(machine,access,target,size,value,user):
        if not STACK-0x1000<=target<STACK+0x1000:writes.append(dict(address=hex(target),bytes=size,value=value&((1<<(size*8))-1)))
    uc.hook_add(UC_HOOK_CODE,hook);uc.hook_add(UC_HOOK_MEM_WRITE,memory);uc.emu_start(address,STOP+4,count=3000)
    if not done or uc.reg_read(UC_ARM_REG_SP)!=STACK or[uc.reg_read(r)for r in SAVED]!=saved:raise ValueError('Complete caller return/SP/callee-saved proof failed')
    expected_events=[];expected_writes=[];expected_entries={slot:bytearray(v)for slot,v in entry_words.items()};expected_resource=bytearray(resource);expected_counter=case['counter'];expected_flag=0x12345678
    def call(pc,values,pair=None):expected_events.append(event(pc,values,pair))
    def store(target,size,value):expected_writes.append(dict(address=hex(target),bytes=size,value=value&((1<<(size*8))-1)))
    def lookup(slot):call(0x2049ad0,[slot]);return TABLE+12*slot
    def rectangle(handle):call(0x204b53c,[handle,0],[resource[28]*8,resource[29]*8])
    if address==0x21efec4:
        target=lookup(19);lookup(selector);link=struct.unpack('<I',entry_words[selector][:4])[0];expected_entries[19][:4]=words([link]);store(target,4,link);value=(case['valueByte']+2)&255
        call(0x21ef688,[18,2,127,22,value,7,2,1,1]);call(0x21ef1cc,[1]);call(0x21ef2a8,[176,(value*8)&255])
    elif address in[0x21f29ac,0x2207acc,0x2208854]:
        active=address==0x21f29ac or case['handle']!=0
        if active:
            lookup(selected)
            if case['occupied']:
                rectangle(case['handle'])
                if address!=0x21f29ac:call(0x2207b7c if address==0x2207acc else 0x2208918,[resource[94]])
            call(0x205f9e4,[case['handle']])
        if address==0x2208854 and case['secondHandle']:call(0x205f9e4,[case['secondHandle']])
        if address!=0x21f29ac:expected_flag=1;store(FLAG,4,1)
    elif address==0x2206868:
        slot=lookup(selector);call(0x2049be4,[slot,1,*args[1:7],case['counter'],*args[7:9]]);call(0x205fe20,[1]);call(0x205fe74,[LINK,1,7,11,*args[3:7],case['counter'],*args[7:9]])
        expected_entries[selector][:8]=words([LINK])+bytes([args[1]&255,args[2]&255,128,0x7f]);store(slot+6,1,128);store(slot,4,LINK);store(slot+4,1,args[1]);store(slot+5,1,args[2]);store(RESOURCE+24,4,case['flags']|2);struct.pack_into('<I',expected_resource,24,case['flags']|2)
        if case['enabled']:expected_counter=(case['counter']+case['width']*case['height'])&0xffffffff;store(COUNTER,4,expected_counter)
    elif address==0x22162e4:call(0x2216260,[0,case['tag'],127,1,1,30,2,1,1]);lookup(0);call(0x204a04c,[RESOURCE,5,0,case['tag']])
    elif address==0x221d05c:
        lookup(selector);call(0x206db90,[s8(entry_words[selector][5])])
        if case['occupied']:
            flags=case['flags']|2 if case['enabled']else case['flags']&~2;store(RESOURCE+24,4,flags);struct.pack_into('<I',expected_resource,24,flags)
            if not case['enabled']:
                call(0x2045dc4,[1,table[case['indexReturn']*12],*resource[92:96]])
                if case['resourceTail']:call(0x2049ffc,[RESOURCE]);call(0x2087e44,[0x13579bdf,0])
    if len(events)!=len(expected_events):raise ValueError(('Independent caller provider count differs',row['address'],case,events,expected_events))
    for actual,expected in zip(events,expected_events):
        if expected['address']=='0x204b53c':expected['args'][1]=actual['args'][1]
    actual_memory=dict(entries={str(slot):bytes(uc.mem_read(TABLE+12*slot,12)).hex()for slot in sorted(slots)},resource=bytes(uc.mem_read(RESOURCE,100)).hex(),counter=struct.unpack('<I',uc.mem_read(COUNTER,4))[0],flag=struct.unpack('<I',uc.mem_read(FLAG,4))[0])
    expected_memory=dict(entries={str(slot):bytes(expected_entries[slot]).hex()for slot in sorted(slots)},resource=bytes(expected_resource).hex(),counter=expected_counter,flag=expected_flag)
    if(events,writes,actual_memory)!=(expected_events,expected_writes,expected_memory):raise ValueError(('Independent narrow ABI/field/order model differs',row['address'],case,events,expected_events,writes,expected_writes,actual_memory,expected_memory))
    result=dict(events=events,orderedPersistentWrites=writes,memory=actual_memory,gprs=[uc.reg_read(r)for r in REG+SAVED+[UC_ARM_REG_R12,UC_ARM_REG_SP]],cpsr=uc.reg_read(UC_ARM_REG_CPSR))
    return result,dict(helperInvocations=helpers,helperInstructions=helper_instructions,serviceEntries=services,callerInstructions=caller_instructions)


def execute(rows):
    value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();records=[];helpers=0;helper_instructions=0;services=0
    for row in rows:
        address=int(row['address'],0);native=image[address-BASE:address-BASE+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        for index in range(8):
            case=make_case(address,index);pair=[];counts=[]
            for body in[native,compiled]:
                result,count=execute_one(row,body,case,main,image);pair.append(result);counts.append(count);helpers+=count['helperInvocations'];helper_instructions+=count['helperInstructions'];services+=count['serviceEntries']
            if pair[0]!=pair[1]:raise ValueError('Original/source complete caller CPU/effect results differ')
            records.append(dict(address=row['address'],case=case,result=pair[0],executions=counts,returned=True))
    trace=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    limits=['Synthetic valid mapped slot/link/resource/global-prefix memory and narrow argument domains only; no gameplay/render/scene/device/network execution.','Original accepted main getter20B,initializer172B,clear20B execute only where called; all other provider callbacks have explicit supplied ABI contracts and execute0body instructions. Imported/provider/storage initialized-byte credit0.','Resource28/72/100-byte declarations and imported global arrays are consumed views, not full native allocation or nominal portable ABI proofs; semantic labels and void-return incidental register values have no inferred gameplay meaning.','Unchecked initializer fixtures require successful allocation; the null link branches and handle/flag/byte/counter boundary cases are caller-local proofs, not callee failure or actual game-domain validation.']
    result=dict(passed=True,functions=len(rows),vectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualOriginalHelperInvocations=helpers,actualOriginalHelperInstructions=helper_instructions,suppliedServiceCalls=services,suppliedServiceBodyInstructionsExecuted=0,traceSha256=trace,limits=limits,records=records)
    write_json(EVIDENCE/'caller-fixtures.json',result);return result
