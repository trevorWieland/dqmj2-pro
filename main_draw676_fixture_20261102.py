import bisect
import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from project import ROOT,read_json
from draw676_positive_divider_20261102 import PositiveDivider

ENTRY,DATA,STACK,STOP=0x0202DAFC,0x02400000,0x03030000,0x0F000000
STATE,FIFO,TABLE,DMA=0x020EDF84,0x04000400,0x020DD680,0x020DCB44
CALLBACKS=[0x0202CE38,0x0202D2C8,0x0202C584,0x0202D974]
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
FUNCTIONS={int(f['address'],0):f for m in read_json(ROOT/'evidence/regions/canonical-symbol-functions.json')['canonicalModules']
 for f in m['functions']if m['module']=='main'}
STARTS=sorted(FUNCTIONS)


def inputs(index):
    rng=random.Random(0xDAFC676+index);page=bytearray(rng.randbytes(65536))
    model,matbase,shapebase=DATA+0x1000,DATA+0x2000,DATA+0x4000
    flags=index%64;mode=(index//64)%4;matid=rng.choice([0,1,2,3,0xFFFFFFFF])
    shapeid=rng.choice([0,1,2,3,0xFFFFFFFF]);send=rng.choice([1,0,2,0xFFFFFFFF])
    pos=rng.choice([4096,2048,0,0xFFFFF000]);inv=rng.choice([4096,8192,0,0xFFFFF000])
    struct.pack_into('<II',page,model-DATA+8,matbase-model,shapebase-model)
    page[model-DATA+22]=mode;page[model-DATA+24]=3;page[model-DATA+25]=3
    struct.pack_into('<II',page,model-DATA+28,pos,inv)
    for base,offset in[(matbase,4),(shapebase,0)]:
        dictionary=base+offset;page[dictionary-DATA+1]=3
        struct.pack_into('<H',page,dictionary-DATA+6,0x100);struct.pack_into('<HH',page,dictionary-DATA+0x100,4,0x40)
        for i in range(3):struct.pack_into('<I',page,dictionary-DATA+0x104+i*4,0x800+i*(0x100 if base==matbase else 0x200))
    alpha=rng.choice([0,1,15,31]);diff,spec,texture=[rng.getrandbits(32)for i in range(3)];palette=rng.getrandbits(16)
    polygon=(rng.getrandbits(32)&~0x1F0000)|(alpha<<16)
    width,height=[8,16,32,64][index%4],[8,16,32,64][(index//4)%4]
    scale=[2048,4096];rotation=[0,4096];translation=[1024,0xFFFFFC00]
    for i in range(3):
        material=matbase+0x800+i*0x100
        struct.pack_into('<HH6I4H2I',page,material-DATA,0,64,diff,spec,polygon,0xFFFFFFFF,texture,0xFFFFFFFF,palette,flags,width,height,4096,4096)
        at=material-DATA+44
        if not flags&2:struct.pack_into('<2I',page,at,*scale);at+=8
        if not flags&4:struct.pack_into('<2h',page,at,*rotation);at+=4
        if not flags&8:struct.pack_into('<2I',page,at,*translation)
    dlbytes=rng.choice([4,8,16,28,64,128,252,256]);dl=[rng.getrandbits(32)for i in range(dlbytes//4)]
    for i in range(3):
        shape=shapebase+0x800+i*0x200
        struct.pack_into('<HHIII',page,shape-DATA,0,16,0,0x20,dlbytes)
        struct.pack_into('<'+str(len(dl))+'I',page,shape-DATA+0x20,*dl)
    commands=[];expected_texture=None;early=bool(send and matid<3 and not alpha)
    if pos!=4096:commands.append([0x1B,[pos]*3])
    if send and matid<3 and alpha:
        commands.append([0x293130,[diff,spec,polygon&~0x1F0000 if flags&32 else polygon,0x2B2A,texture,palette]])
        if flags&1:
            expected_texture={0:(4,8|(1 if flags&2 else 0)|(2 if flags&4 else 0)|(4 if flags&8 else 0)),
             44:(2,width),46:(2,height),48:(4,4096),52:(4,4096)}
            if not flags&2:expected_texture.update({24:(4,scale[0]),28:(4,scale[1])})
            if not flags&4:expected_texture.update({32:(2,rotation[0]&65535),34:(2,rotation[1]&65535)})
            if not flags&8:expected_texture.update({36:(4,translation[0]),40:(4,translation[1])})
    if not early:
        if shapeid<3:commands.append([dl[0],dl[1:]])
        if inv!=4096:commands.append([0x1B,[inv]*3])
    return page,[model,matid,shapeid,send],commands,expected_texture,dict(flags=flags,mode=mode,alpha=alpha,early=early,dlBytes=dlbytes)


def execute(image,body,index,bound=65536):
    page,args,expected_commands,expected_texture,context=inputs(index);rng=random.Random(0x676ABCDE+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000,0x100000);machine.mem_write(0x02000000,image);machine.mem_write(ENTRY,body)
    machine.mem_write(STATE,bytes(12));machine.mem_write(DMA,bytes.fromhex('ffffffff'));before_main=bytes(machine.mem_read(0x02000000,0x100000))
    machine.mem_map(DATA,65536);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_map(STOP,4096)
    machine.mem_map(0x04000000,65536);hardware=rng.randbytes(65536);machine.mem_write(0x04000000,hardware)
    divider=PositiveDivider(machine,hardware)
    stack=rng.randbytes(8192);machine.mem_write(STACK,stack);initial=[rng.getrandbits(32)for r in REGS]
    for register,value in zip(REGS,initial):machine.reg_write(register,value)
    for register,value in zip(REGS,args):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28));machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    own=set();calls=[];reads=[];writes=[];frames=[];completed=[];commands=[];texture_fields=[];fifo=[]
    def code(uc,address,size,unused):
        while frames and address==frames[-1]['lr']:completed.append(frames.pop())
        if ENTRY<=address<ENTRY+len(body):own.add(address)
        else:
            at=bisect.bisect_right(STARTS,address)-1;assert at>=0
            base=STARTS[at];assert base<=address<base+FUNCTIONS[base]['size'],hex(address)
        if address==ENTRY or address in FUNCTIONS:
            frame=dict(entry=address,lr=uc.reg_read(UC_ARM_REG_LR),sp=uc.reg_read(UC_ARM_REG_SP));frames.append(frame)
            calls.append(dict(**frame,args=[uc.reg_read(r)for r in REGS[:4]]))
        if address in CALLBACKS:
            pointer=uc.reg_read(UC_ARM_REG_R0);assert expected_texture is not None
            fields={offset:int.from_bytes(bytes(uc.mem_read(pointer+offset,length)),'little')for offset,(length,value)in expected_texture.items()}
            texture_fields.append(dict(entry=address,fields=fields,modelPassed=fields=={offset:value for offset,(length,value)in expected_texture.items()}))
        if address==0x0202E434:
            op,source,count=[uc.reg_read(r)for r in REGS[:3]];assert count<=64
            payload=list(struct.unpack('<'+str(count)+'I',bytes(uc.mem_read(source,count*4))))if count else[]
            commands.append(dict(op=op,payload=payload,texture=any(f['entry']in CALLBACKS for f in frames)))
    def read(uc,access,address,size,value,unused):
        if 0x04000280<=address and address+size<=0x040002B0:divider.read(address,size)
        else:assert 0x02000000<=address and address+size<=0x02100000 or DATA<=address and address+size<=DATA+65536 or STACK<=address and address+size<=STACK+8192,hex(address)
        reads.append([address,size,bytes(uc.mem_read(address,size)).hex()])
    def write(uc,access,address,size,value,unused):
        if address==FIFO:assert size==4;fifo.append(value&0xFFFFFFFF)
        elif 0x04000280<=address and address+size<=0x040002A0:divider.write(address,size,value)
        else:assert STACK+2048<=address and address+size<=STACK+4096,hex(address)
        writes.append([address,size,value&((1<<(size*8))-1)])
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(ENTRY,STOP,count=bound);assert machine.reg_read(UC_ARM_REG_PC)==STOP,'Prefix is not actual return'
    while frames and frames[-1]['lr']==STOP:completed.append(frames.pop())
    assert not frames and machine.reg_read(UC_ARM_REG_SP)==STACK+4096
    assert all(machine.reg_read(r)==value for r,value in zip(REGS[4:12],initial[4:12]))
    after_stack=bytes(machine.mem_read(STACK,8192));assert after_stack[:2048]==stack[:2048]and after_stack[4096:]==stack[4096:]
    assert bytes(machine.mem_read(DATA,65536))==page and bytes(machine.mem_read(0x02000000,0x100000))==before_main
    actual_commands=[[c['op'],c['payload']]for c in commands if not c['texture']]
    expected_fifo=[v for c in commands for v in[c['op'],*c['payload']]]
    expected_hardware=divider.expected
    if fifo:struct.pack_into('<I',expected_hardware,FIFO-0x04000000,fifo[-1])
    model=actual_commands==expected_commands and fifo==expected_fifo and bytes(machine.mem_read(0x04000000,65536))==expected_hardware
    model=model and len(texture_fields)==int(expected_texture is not None)and all(f['modelPassed']for f in texture_fields)
    return dict(index=index,context=context,actualReturn=True,modelPassed=model,ownedObserved=sorted(own),commands=commands,
     textureFields=texture_fields,calls=calls,reads=reads,writes=writes,providedCalls=0,nativeEntryCompletions=len(completed)-1,
     modeledPositiveDivisionOperations=divider.operations,
     registers=[machine.reg_read(r)for r in REGS],cpsr=machine.reg_read(UC_ARM_REG_CPSR),lr=machine.reg_read(UC_ARM_REG_LR),
     stackSha256=hashlib.sha256(after_stack).hexdigest(),fifo=fifo)
