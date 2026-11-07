import hashlib
import json
import struct
import match_runtime
from project import ROOT,write_json
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from wave20261106_ov000_controller_composite_next_first_paths import EVIDENCE
from wave20261106_ov000_controller_composite_next_first_bindings import inputs

REG=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
BASE=0x21d7240
STACK=0x3030000
STOP=0x303f000
TABLE=0x2102a18
STATE=0x22461c4
ARRAY=0x22461d4
SETUP=0x22460d4
HELPERS={0x2049ad0:(20,1),0x2049be4:(172,11),0x221c658:(12,0),0x221c758:(200,9)}
SERVICES={0x205fe20:1,0x205fe74:11,0x221e85c:1,0x2087554:1,0x204a808:5,0x205dc70:3,0x2046af4:6,0x2049f4c:1,0x2087a48:6,0x2086b14:2,0x20877bc:4}


def words(values):return struct.pack('<'+'I'*len(values),*[v&0xffffffff for v in values])
def halfs(values):return struct.pack('<'+'H'*len(values),*[v&65535 for v in values])
def s16(value):return(value&65535)-65536 if value&32768 else value&65535
def link(slot):return 0x3010000+slot*32
def resource(slot):return 0x3014000+slot*256
def event(pc,args,**extra):return dict(address=hex(pc),args=[v&0xffffffff for v in args],**extra)
def make_case(address,index):return dict(index=index,flags=[0,1,2,3,0x80000003,3,2,1][index],tag=[-128,-1,127,0][index%4],counter=[0,0xffffffff,0xffffff80,7][index%4],listStart=index%4,resourceFlags=[0,0xffffffff,0x80000000][index%3],args=[index%4,(index+1)%4,0x12345678+index,0x87654321-index,[0,128,255][index%3],[-128,-1,127][index%3]],pointMutation=index%2!=0)


def execute_one(row,body,case,main,image):
    address=int(row['address'],0);index=case['index'];uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x2000000,0x400000);uc.mem_map(0x3000000,0x40000);uc.mem_write(0x2000000,main);uc.mem_write(BASE,image);uc.mem_write(address,body)
    uc.mem_write(0x21029c8,bytes([3,7,2,9,4,8,1,6]));uc.mem_write(0x21029d0,bytes([5,11,1,2,3,4,6,7]));uc.mem_write(SETUP+16,bytes([case['tag']&255]))
    slots=list(range(16,26))if address==0x221f910 else sorted(set(case['args'][:2]));entry_initial={};resource_initial={}
    for slot in slots:
        entry_initial[slot]=bytearray(words([0 if address==0x221f910 else link(slot),0x99887766,0xabcdef01]));resource_initial[slot]=bytearray((j+slot+index)&255 for j in range(100));struct.pack_into('<I',resource_initial[slot],24,case['resourceFlags']);uc.mem_write(TABLE+slot*12,bytes(entry_initial[slot]));uc.mem_write(link(slot),bytes([(128+slot+index)&255,0,0,0])+words([resource(slot)]));uc.mem_write(resource(slot),bytes(resource_initial[slot]))
    state=words([0x12345678,0xabcdef01,case['counter'],case['listStart']]);array=bytes(range(64));uc.mem_write(STATE,state);uc.mem_write(ARRAY,array)
    args=[]if address==0x221f910 else case['args'];uc.mem_write(STACK,words(args[4:]+[0]*8));uc.reg_write(UC_ARM_REG_SP,STACK);uc.reg_write(UC_ARM_REG_LR,STOP)
    for reg,value in zip(REG,args[:4]+[0]*(4-len(args[:4]))):uc.reg_write(reg,value&0xffffffff)
    saved=[0x11110000+i*0x101 for i in range(8)]
    for reg,value in zip(SAVED,saved):uc.reg_write(reg,value)
    events=[];writes=[];helpers=0;helper_instructions=0;services=0;caller_instructions=0;done=False;current_slot=None;points=[];buffers=[]
    def capture(machine,pc,count):
        values=[machine.reg_read(r)for r in REG[:min(count,4)]]
        if count>4:values+=list(struct.unpack('<'+'I'*(count-4),machine.mem_read(machine.reg_read(UC_ARM_REG_SP),4*(count-4))))
        extra={}
        if pc==0x204a808:
            points.append(values[1]);buffers.append(values[3]);extra=dict(point=list(struct.unpack('<hh',machine.mem_read(values[1],4))),symbol=list(struct.unpack('<HH',machine.mem_read(values[3],4))))
        if pc==0x2087a48:
            buffers.append(values[5]);extra=dict(buffer=list(struct.unpack('<'+'H'*8,machine.mem_read(values[5],16))))
        events.append(event(pc,values,**extra));return values
    def hook(machine,pc,size,user):
        nonlocal helpers,helper_instructions,services,caller_instructions,done,current_slot
        if pc==STOP:done=True;machine.emu_stop();return
        if pc in HELPERS:
            helpers+=1;values=capture(machine,pc,HELPERS[pc][1])
            if pc==0x2049be4:current_slot=(values[0]-TABLE)//12
        if any(a<=pc<a+length for a,(length,count)in HELPERS.items()):helper_instructions+=1;return
        if pc in SERVICES:
            services+=1;values=capture(machine,pc,SERVICES[pc]);result=0xdeadbeef
            if pc==0x205fe20:result=link(current_slot)
            elif pc==0x221e85c:result=case['flags']
            elif pc==0x2087554:result=0xf1238000+index*2+values[0]
            elif pc==0x204a808 and case['pointMutation']:
                machine.mem_write(values[1],halfs([32760,1]))
            elif pc==0x205dc70:result=0x12340000|values[2]&65535
            elif pc==0x2046af4:machine.mem_write(values[4],halfs([index*100+j for j in range(32)]));buffers.append(values[4])
            elif pc==0x20877bc:machine.mem_write(values[1],halfs([index*200+j+50 for j in range(32)]));buffers.append(values[1])
            elif pc==0x2086b14:result=0xc0000000+values[0]-0x3014000
            for reg in REG+[UC_ARM_REG_R12]:machine.reg_write(reg,0xa1000000+services*0x100+reg)
            machine.reg_write(UC_ARM_REG_R0,result);machine.reg_write(UC_ARM_REG_CPSR,(machine.reg_read(UC_ARM_REG_CPSR)&0xfffffff)|0xa0000000);machine.reg_write(UC_ARM_REG_PC,machine.reg_read(UC_ARM_REG_LR));return
        if not address<=pc<address+len(body):raise ValueError(('Composite execution left exact caller/helper/provider closure',hex(pc)))
        caller_instructions+=1
    def memory(machine,access,target,size,value,user):
        if not STACK-0x1000<=target<STACK+0x1000:writes.append(dict(address=hex(target),bytes=size,value=value&((1<<(size*8))-1)))
    uc.hook_add(UC_HOOK_CODE,hook);uc.hook_add(UC_HOOK_MEM_WRITE,memory);uc.emu_start(address,STOP+4,count=8000)
    if not done or uc.reg_read(UC_ARM_REG_SP)!=STACK or[uc.reg_read(r)for r in SAVED]!=saved:raise ValueError('Composite caller return/SP/callee-saved contract differs')
    expected=[];expected_writes=[];expected_entries={k:bytearray(v)for k,v in entry_initial.items()};expected_resources={k:bytearray(v)for k,v in resource_initial.items()};expected_state=list(struct.unpack('<IIII',state));expected_array=bytearray(array)
    def call(pc,values,**extra):expected.append(event(pc,values,**extra))
    def store(target,size,value):expected_writes.append(dict(address=hex(target),bytes=size,value=value&((1<<(size*8))-1)))
    if address==0x221f910:
        specs=[(16,12,17,5,15,14,1,0),(17,18,17,11,1,1,1,0),(18,19,17,12,1,6,1,0),(19,20,17,18,1,1,1,0)]+[(20+i,1,18,6+i*2,13,2,0,1)for i in range(6)]
        for slot,field,p0,p1,width,height,tag,enabled in specs:
            counter=expected_state[2];call(0x221c658,[]);call(0x221c758,[slot,case['tag'],field,p0,p1,width,height,tag,enabled]);call(0x2049ad0,[slot]);call(0x2049be4,[TABLE+12*slot,1,case['tag'],field,p0,p1,width,height,counter,tag,enabled]);call(0x205fe20,[1]);call(0x205fe74,[link(slot),1,7,11,p0,p1,width,height,counter,tag,enabled])
            first=(128+slot+index)&255;expected_entries[slot][:8]=words([link(slot)])+bytes([case['tag']&255,field,first,0x99]);store(TABLE+12*slot+6,1,first);store(TABLE+12*slot,4,link(slot));store(TABLE+12*slot+4,1,case['tag']);store(TABLE+12*slot+5,1,field);store(resource(slot)+24,4,case['resourceFlags']|2);struct.pack_into('<I',expected_resources[slot],24,case['resourceFlags']|2)
            if enabled:expected_state[2]=(counter+width*height)&0xffffffff;store(STATE+8,4,expected_state[2])
            at=expected_state[3];expected_state[3]+=1;store(STATE+12,4,expected_state[3]);expected_array[at]=slot;store(ARRAY+at,1,slot)
        expected_return=STATE
    else:
        if buffers:
            if len(set(buffers))!=1 or not STACK-0x200<=buffers[0]<=STACK-64 or buffers[0]%4:raise ValueError('Composite buffer extent/identity/alignment differs')
        buffer=buffers[0];point=points[0]if points else buffer-4
        if points and(len(set(points))!=1 or point!=buffer-4):raise ValueError('Composite point extent/identity differs')
        selector0,selector1,field2,field3,width,tag=args;call(0x221e85c,[field2]);call(0x2049ad0,[selector0]);xy=[16,0]
        if case['flags']&1:
            call(0x2087554,[0]);call(0x204a808,[selector0,point,1,buffer,0],point=xy[:],symbol=[0x8000+index*2,0])
            if case['pointMutation']:xy=[32760,1]
        xy[0]=s16(xy[0]+8)
        if case['flags']&2:
            call(0x2087554,[1]);call(0x204a808,[selector0,point,1,buffer,0],point=xy[:],symbol=[0x8001+index*2,0])
        call(0x205dc70,[8,0,field2]);call(0x2046af4,[0x21c9698,0x12340000|field2&65535,width,24,buffer,255]);call(0x2049f4c,[TABLE+12*selector0]);call(0x2087a48,[resource(selector0),0,32,0,tag,buffer],buffer=[index*100+j for j in range(8)]);call(0x2086b14,[resource(selector0),0]);call(0x2049ad0,[selector1]);call(0x20877bc,[field3,buffer,4,3]);call(0x2049f4c,[TABLE+12*selector1]);call(0x2087a48,[resource(selector1),0,48,0,tag,buffer],buffer=[index*200+j+50 for j in range(8)]);call(0x2086b14,[resource(selector1),0]);expected_return=0xc0000000+resource(selector1)-0x3014000
    actual_memory=dict(entries={str(k):bytes(uc.mem_read(TABLE+12*k,12)).hex()for k in slots},resources={str(k):bytes(uc.mem_read(resource(k),100)).hex()for k in slots},state=bytes(uc.mem_read(STATE,16)).hex(),array=bytes(uc.mem_read(ARRAY,64)).hex())
    model_memory=dict(entries={str(k):bytes(expected_entries[k]).hex()for k in slots},resources={str(k):bytes(expected_resources[k]).hex()for k in slots},state=words(expected_state).hex(),array=bytes(expected_array).hex())
    if(events,writes,actual_memory,uc.reg_read(UC_ARM_REG_R0))!=(expected,expected_writes,model_memory,expected_return):raise ValueError(('Independent composite ABI/field/order model differs',row['address'],case,events,expected,writes,expected_writes,actual_memory,model_memory))
    result=dict(events=events,orderedPersistentWrites=writes,memory=actual_memory,gprs=[uc.reg_read(r)for r in REG+SAVED+[UC_ARM_REG_R12,UC_ARM_REG_SP]],cpsr=uc.reg_read(UC_ARM_REG_CPSR));return result,dict(helperInvocations=helpers,helperInstructions=helper_instructions,serviceEntries=services,callerInstructions=caller_instructions)


def execute(rows):
    value,image,inventory,relocations,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();records=[];helpers=0;helper_instructions=0;services=0
    for row in rows:
        address=int(row['address'],0);native=image[address-BASE:address-BASE+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        for index in range(8):
            case=make_case(address,index);pair=[];counts=[]
            for body in[native,compiled]:
                result,count=execute_one(row,body,case,main,image);pair.append(result);counts.append(count);helpers+=count['helperInvocations'];helper_instructions+=count['helperInstructions'];services+=count['serviceEntries']
            if pair[0]!=pair[1]:raise ValueError('Original/compiled complete composite CPU/effects differ')
            records.append(dict(address=row['address'],case=case,result=pair[0],executions=counts,returned=True))
    trace=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest();limits=['Synthetic valid mapped slots,links,resources,global-prefix/list and bounded stack-wide-buffer/point domains only;no actual gameplay/render/scene/device execution.','Original221c658/12B,221c758/200B,main49ad0/20B and49be4/172B execute only where called; their imported code earns0extra credit and deeper providers execute0body instructions.','Opaque providers have explicit bounded writes/returns/clobbers; no real formatting/graphics/allocator semantics or failure coverage is claimed. Imported globals/data/BSS have0initialized-byte source credit.','Private signed-byte selector call views intersect the frozen unsigned-byte c758 export view on slots16–25; nominal whole-program portable declarations remain unresolved and are separately recorded.','Renderer signed-halfword point mutations,flags0/1/2/3,narrow stack arguments and byte-buffer prefixes are measured caller-local fixtures; supplied raw return words have no inferred game-purpose meaning.']
    result=dict(passed=True,functions=len(rows),vectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualOriginalHelperInvocations=helpers,actualOriginalHelperInstructions=helper_instructions,suppliedServiceCalls=services,suppliedServiceBodyInstructionsExecuted=0,traceSha256=trace,limits=limits,records=records);write_json(EVIDENCE/'caller-fixtures.json',result);return result
