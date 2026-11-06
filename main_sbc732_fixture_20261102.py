import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,DATA,STACK,STOP=0x02000000,0x02400000,0x03030000,0x0F000000
STATE,FIFO=0x020EDF84,0x04000400
MAT_TABLE,SHP_TABLE=0x020DD6A0,0x020DD6B0
SPANS={0x0202FB48:40,0x0202FB70:40,0x0202FD14:204,0x02030268:176,0x020303EC:160,0x02031790:112}
COMMANDS={0x0202FB48:0,0x0202FB70:1,0x0202FD14:3,0x02030268:4,0x020303EC:5,0x02031790:11}
CALLBACK=STOP+0x100
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def word(page,at):return struct.unpack_from('<I',page,at)[0]
def put(page,at,value):struct.pack_into('<I',page,at,value&0xFFFFFFFF)


def inputs(index):
    rng=random.Random(0x5BC732+index);page=bytearray(rng.randbytes(65536));entry=list(SPANS)[index%6];command=COMMANDS[entry]
    flags=rng.getrandbits(32)&~0x34B
    for n,bit in enumerate([1,2,8,64,256,512]):
        if(index//6)&(1<<n):flags|=bit
    rs=0x100;cmd=0x1000;mat=0x2000;shape=0x4000;current=rng.randrange(3);selected=rng.randrange(3)
    timing=(index//384)%4;present=(index//1536)%2
    put(page,rs,DATA+cmd);put(page,rs+8,flags);page[rs+173]=current
    for n in range(32):put(page,rs+12+4*n,0);page[rs+140+n]=rng.randrange(4)
    put(page,rs+12+4*command,CALLBACK if present else 0);page[rs+140+command]=timing
    put(page,rs+216,DATA+mat);put(page,rs+220,DATA+shape)
    put(page,rs+224,rng.choice([0,1,4096,0xFFFFF000,0x80000000]));put(page,rs+228,rng.choice([0,8192,0x80000000,0xFFFFFFFF]))
    page[cmd]=command;page[cmd+1]=selected
    for root,offset,stride in[(mat,4,44),(shape,0,16)]:
        d=root+offset;page[d]=0;page[d+1]=3;struct.pack_into('<H',page,d+6,0x100);struct.pack_into('<HH',page,d+0x100,4,0x40)
        for n in range(3):put(page,d+0x104+n*4,0x800+n*0x100);struct.pack_into('<HH',page,root+0x800+n*0x100,rng.randrange(4),stride)
    context=dict(command=command,skip=bool(rng.getrandbits(1)),move=rng.choice([0,3,7]),
     timingAfter=rng.randrange(4),disable=bool(rng.getrandbits(1)),extraFlag=rng.choice([0,0x100,0x40000000]))
    opt=rng.choice([0,1,32,0xFFFFFFFF]);return page,entry,[DATA+rs,opt],context


def callback_effect(page,rs,context):
    flag=word(page,rs+8)^context['extraFlag']
    flag=(flag|64)if context['skip']else(flag&~64)
    put(page,rs+8,flag);put(page,rs,word(page,rs)+context['move'])
    page[rs+140+context['command']]=context['timingAfter']
    if context['disable']:put(page,rs+12+4*context['command'],0)


def dispatch_effect(page,rs,index,palette):
    put(page,rs+8,word(page,rs+8)^(0x80000000 if palette else 0x40000000));page[rs+(174 if palette else 173)]=index
    put(page,rs,word(page,rs)+3)


def model(initial,entry,args,context):
    page=bytearray(initial);rs=args[0]-DATA;command=context['command'];calls=[];geometry=[]
    def callback():
        calls.append(dict(entry=CALLBACK,words=[DATA+rs]));callback_effect(page,rs,context)
    def timing():return page[rs+140+command]if word(page,rs+12+4*command)else 0
    flag=word(page,rs+8)
    if command in[0,1]:
        if word(page,rs+12+4*command):callback()
        if command==0:put(page,rs,word(page,rs)+1)
        else:put(page,rs+8,word(page,rs+8)|32)
    elif command==3:
        if not flag&512 and flag&1:
            phase=timing();skip=False
            if phase==1:
                put(page,rs+8,word(page,rs+8)&~64);callback();phase=timing();skip=bool(word(page,rs+8)&64)
            if not skip and not word(page,rs+8)&256:geometry.append(dict(op=0x14,values=[page[word(page,rs)-DATA+1]]))
            if phase==3:put(page,rs+8,word(page,rs+8)&~64);callback()
        put(page,rs,word(page,rs)+2)
    elif command in[4,5]:
        selected=page[word(page,rs)-DATA+1];eligible=not flag&512
        if command==4:eligible=eligible and(bool(flag&1)or not(flag&8 and selected==page[rs+173]))
        else:eligible=eligible and bool(flag&1)and not flag&2
        if eligible:
            root=word(page,rs+(220 if command==5 else 216))-DATA;d=root+(0 if command==5 else 4)
            header=d+struct.unpack_from('<H',page,d+6)[0];item=root+word(page,header+4+selected*4)
            tag=struct.unpack_from('<H',page,item)[0];target=STOP+(0x300 if command==5 else 0x200)+tag*16
            calls.append(dict(entry=target,words=[DATA+rs,args[1],DATA+item,selected]));dispatch_effect(page,rs,selected,command==5)
        put(page,rs,word(page,rs)+2)
    else:
        if not flag&256 and not flag&512:geometry.append(dict(op=0x1B,values=[word(page,rs+(224 if args[1]==0 else 228))]*3))
        put(page,rs,word(page,rs)+1)
    return bytes(page),calls,geometry


def execute(image,bodies,index,bound=10000):
    page,entry,args,context=inputs(index);expected,expected_calls,expected_geometry=model(page,entry,args,context)
    rng=random.Random(0x732+index);machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    main=bytearray(image)+bytearray(0x100000-len(image));main[STATE-BASE:STATE-BASE+12]=bytes(12)
    for table,start in[(MAT_TABLE,STOP+0x200),(SHP_TABLE,STOP+0x300)]:
        for n in range(4):struct.pack_into('<I',main,table-BASE+4*n,start+16*n)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,bytes(main))
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_map(DATA,65536);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192))
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');machine.mem_map(0x04000000,4096)
    machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xF0000000]))
    for reg in REGS:machine.reg_write(reg,rng.getrandbits(32))
    for reg,value in zip(REGS,args):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    reads=[];writes=[];seen=set();calls=[];geometry=[];returned=False
    providers={CALLBACK,*[STOP+b+16*n for b in[0x200,0x300]for n in range(4)]}
    def code(uc,address,size,user):
        nonlocal returned
        if address==STOP:returned=True;uc.emu_stop();return
        if address in providers:
            words=[uc.reg_read(r)for r in REGS[:4]];rs=words[0]-DATA;count=1 if address==CALLBACK else 4
            calls.append(dict(entry=address,words=words[:count]));changed=bytearray(uc.mem_read(DATA,65536))
            if address==CALLBACK:callback_effect(changed,rs,context)
            else:dispatch_effect(changed,rs,words[3],address>=STOP+0x300)
            for n,(old,new)in enumerate(zip(bytes(uc.mem_read(DATA,65536)),changed)):
                if old!=new:uc.mem_write(DATA+n,bytes([new]))
            for n,reg in enumerate([UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12]):uc.reg_write(reg,0xC7320000+len(calls)*16+n)
            uc.reg_write(UC_ARM_REG_CPSR,0x10|((len(calls)&15)<<28));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR));return
        assert BASE<=address<BASE+len(image),hex(address);seen.add(address)
        if address==0x0202E434:
            op,pointer,count=[uc.reg_read(r)for r in REGS[:3]];assert count<=3
            geometry.append(dict(op=op,values=list(struct.unpack('<'+str(count)+'I',bytes(uc.mem_read(pointer,4*count))))))
    def read(uc,access,address,size,value,user):reads.append((address,size,int.from_bytes(bytes(uc.mem_read(address,size)),'little')))
    def write(uc,access,address,size,value,user):
        assert DATA<=address and address+size<=DATA+65536 or STACK<=address and address+size<=STACK+8192 or address==FIFO
        writes.append((address,size,value))
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP+4,count=bound);assert returned,('no actual top return',index)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096
    output=bytes(machine.mem_read(DATA,65536));passed=output==expected and calls==expected_calls and geometry==expected_geometry
    for address,body in bodies.items():machine.mem_write(address,image[address-BASE:address-BASE+len(body)])
    final_main=bytes(machine.mem_read(BASE,len(main)))
    assert final_main==bytes(main),(index,[(hex(BASE+n),a,b)for n,(a,b)in enumerate(zip(main,final_main))if a!=b][:32])
    expected_fifo=[value for command in geometry for value in[command['op'],*command['values']]]
    assert [value for address,size,value in writes if address==FIFO]==expected_fifo
    return dict(index=index,entry=entry,args=args,context=context,actualReturn=True,modelPassed=passed,providedCalls=calls,geometry=geometry,
     registers=[machine.reg_read(r)for r in REGS],flags=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,
     dataSha256=hashlib.sha256(output).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     ownedObserved=sorted(a for a in seen if any(b<=a<b+n for b,n in SPANS.items())))
