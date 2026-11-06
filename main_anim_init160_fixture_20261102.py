import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from project import ROOT,read_json
from main_resource_dictionary_fixture_v4_20261101 import patricia

ENTRY,DATA,STACK,STOP=0x0202E8B8,0x02400000,0x03030000,0x0F000000
COUNT,TABLE=0x020DD5F4,0x020DD618
CALLBACKS=[0x02033B84,0x0203416C,0x02034054,0x020343FC,0x02032324]
DEFAULTS={0x02033B84:0x020DD608,0x0203416C:0x020DD604,0x02034054:0x020DD600,0x020343FC:0x020DD5F8,0x02032324:0x020DD5FC}
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
SIZES={int(f['address'],0):f['size']for m in read_json(ROOT/'evidence/regions/canonical-symbol-functions.json')['canonicalModules']
 for f in m['functions']if m['module']=='main'}


def inputs(image,index):
    rng=random.Random(0xE8B8160+index);page=bytearray(rng.randbytes(65536))
    obj,animation,model,texture=DATA+0x100,DATA+0x2000,DATA+0x1000,DATA+0xA000
    records=[list(struct.unpack_from('<BBHI',image,TABLE-0x02000000+i*8))for i in range(10)]
    choice=index%8;mode=(index//8)%5;count=5
    category=(records[choice][0],records[choice][2])if choice<5 else[(90,0xFFFF),(77,0xFFFF),(0,0)][choice-5]
    if mode==1:count=0
    if mode==2:count=10
    if mode==3:
        for record in records:record[3]=0
    if mode==4:records[1][0]=records[0][0];records[1][2]=records[0][2]
    nodes=[0,1,2,7,31,64,127,255][(index//40)%8];materials=[0,1,7,31,255,127,64,2][(index//40)%8]
    page[model-DATA+0x17]=nodes;page[model-DATA+0x18]=materials
    has_material=(index//8)%2==0
    struct.pack_into('<I',page,model-DATA+8,0x100 if has_material else 0)
    page[animation-DATA:animation-DATA+0x100]=bytes(0x100)
    struct.pack_into('<BBH',page,animation-DATA,category[0],index&255,category[1])
    selected=next((row[3]for row in records[:count]if(row[0],row[2])==category),0)
    joint_count=nodes if index%3==0 else nodes//2
    if selected==0x02032324:
        struct.pack_into('<H',page,animation-DATA+6,joint_count)
        for i in range(joint_count):
            offset=0x2000+i*8;struct.pack_into('<H',page,animation-DATA+0x14+i*2,offset)
            struct.pack_into('<I',page,animation-DATA+offset,((i*17+index)&255)<<24|rng.getrandbits(24))
    material_updates=[]
    if selected in CALLBACKS[:3]:
        available=min(materials,[0,1,2,7,15,16,31,31][(index//40)%8])
        seed=rng.randbytes(15);keys=[bytes([i])+seed for i in range(available)]
        target=model+0x104;tree_nodes=patricia(keys)
        struct.pack_into('<BBHHH',page,target-DATA,0,available,0x1000,0,0x800)
        for i,node in enumerate(tree_nodes):struct.pack_into('<4B',page,target-DATA+8+4*i,*node)
        struct.pack_into('<HH',page,target-DATA+0x800,4,0x100)
        for i,key in enumerate(keys):page[target-DATA+0x900+i*16:target-DATA+0x900+(i+1)*16]=key
        offset=12 if selected==0x0203416C else 8;source_dict=animation+offset
        struct.pack_into('<BBHHH',page,source_dict-DATA,0,available,0x1000,0,0x800)
        struct.pack_into('<HH',page,source_dict-DATA+0x800,4,0x100)
        for i in range(available):
            query=bytearray(keys[(i+index)%available])
            if i%3==0:query[12]^=0x80
            page[source_dict-DATA+0x900+i*16:source_dict-DATA+0x900+(i+1)*16]=query
            found=next((j for j,key in enumerate(keys)if key==bytes(query)),None)
            if has_material and found is not None:material_updates.append((found,i|0x100))
    expected=bytearray(page)
    struct.pack_into('<6I',expected,obj-DATA,0,4096,animation,0,0,texture if index%3 else 0)
    expected[obj-DATA+24]=127;expected[obj-DATA+25]=0
    if selected:
        value=struct.unpack_from('<I',image,DEFAULTS[selected]-0x02000000)[0]
        struct.pack_into('<I',expected,obj-DATA+12,value)
        map_count=nodes if selected in CALLBACKS[3:] else materials;expected[obj-DATA+25]=map_count
        values=[i|0x100 for i in range(map_count)]if selected==0x020343FC else[0]*map_count
        if selected==0x02032324:
            for i in range(joint_count):values[i]=((i*17+index)&255)|0x100
        for i,value in material_updates:values[i]=value
        for i,value in enumerate(values):struct.pack_into('<H',expected,obj-DATA+26+i*2,value)
    table=b''.join(struct.pack('<BBHI',*record)for record in records)
    args=[obj,animation,model,texture if index%3 else 0]
    return page,expected,args,table,count,selected,dict(choice=choice,mode=mode,nodes=nodes,materials=materials,jointCount=joint_count,hasMaterial=has_material)


def execute(image,body,index,bound=32768,callback_bodies=None):
    page,expected,args,table,count,selected,context=inputs(image,index);rng=random.Random(0x160ABCDE+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000,0x100000);machine.mem_write(0x02000000,image)
    machine.mem_write(ENTRY,body);machine.mem_write(COUNT,struct.pack('<I',count));machine.mem_write(TABLE,table)
    for address,payload in (callback_bodies or {}).items():machine.mem_write(address,payload)
    before=bytes(machine.mem_read(0x02000000,0x100000))
    machine.mem_map(DATA,65536);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,4096);machine.mem_map(STOP,4096)
    stack=rng.randbytes(4096);machine.mem_write(STACK,stack);initial=[rng.getrandbits(32)for r in REGS]
    for register,value in zip(REGS,initial):machine.reg_write(register,value)
    for register,value in zip(REGS,args):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28));machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,STOP)
    entries={address:len((callback_bodies or {}).get(address,b''))or SIZES[address]for address in CALLBACKS+[0x02008BE0,0x0202BD74]};entries[ENTRY]=len(body)
    allowed={pc for address,size in entries.items()for pc in range(address,address+size,4)}
    own=set();body_observed=set();calls=[];reads=[];writes=[];frames=[];completed=[]
    def code(uc,address,size,unused):
        assert address in allowed,hex(address)
        while frames and address==frames[-1]['lr']:completed.append(frames.pop())
        if address in entries:
            frame=dict(entry=address,lr=uc.reg_read(UC_ARM_REG_LR),sp=uc.reg_read(UC_ARM_REG_SP));frames.append(frame)
            calls.append(dict(**frame,args=[uc.reg_read(r)for r in REGS[:4]]))
        if ENTRY<=address<ENTRY+len(body):own.add(address)
        if any(a<=address<a+entries[a]for a in [ENTRY,*CALLBACKS]):body_observed.add(address)
    def read(uc,access,address,size,value,unused):
        assert 0x02000000<=address and address+size<=0x02100000 or DATA<=address and address+size<=DATA+65536 or STACK<=address and address+size<=STACK+4096
        reads.append([address,size,bytes(uc.mem_read(address,size)).hex()])
    def write(uc,access,address,size,value,unused):
        assert STACK+1024<=address and address+size<=STACK+2048 or args[0]<=address and address+size<=args[0]+1024
        writes.append([address,size,value&((1<<(size*8))-1)])
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(ENTRY,STOP,count=bound);assert machine.reg_read(UC_ARM_REG_PC)==STOP,'Prefix is not actual return'
    while frames and frames[-1]['lr']==STOP:completed.append(frames.pop())
    assert not frames and machine.reg_read(UC_ARM_REG_SP)==STACK+2048
    assert all(machine.reg_read(r)==value for r,value in zip(REGS[4:12],initial[4:12]))
    after=bytes(machine.mem_read(DATA,65536));after_stack=bytes(machine.mem_read(STACK,4096))
    assert bytes(machine.mem_read(0x02000000,0x100000))==before and after_stack[:1024]==stack[:1024]and after_stack[2048:]==stack[2048:]
    cb=[c for c in calls if c['entry']in CALLBACKS]
    model_pass=after==expected and[c['entry']for c in cb]==([selected]if selected else[])
    model_pass=model_pass and all(c['args'][:3]==args[:3]for c in cb)
    return dict(index=index,context=context,actualReturn=True,modelPassed=model_pass,selectedCallback=selected,
     rawR0=machine.reg_read(UC_ARM_REG_R0),registers=[machine.reg_read(r)for r in REGS],cpsr=machine.reg_read(UC_ARM_REG_CPSR),
     lr=machine.reg_read(UC_ARM_REG_LR),ownedObserved=sorted(own),bodyObserved=sorted(body_observed),calls=calls,reads=reads,writes=writes,
     actualNativeHelperReturns=len(completed)-1,providedCalls=0,dataSha256=hashlib.sha256(after).hexdigest(),
     stackSha256=hashlib.sha256(after_stack).hexdigest())
