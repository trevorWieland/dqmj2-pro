import hashlib
import random
import struct
import main_joint_scalar752_fixture_20261102 as scalar
from main_joint_rotation1884_fixture_20261102 import normalize,DegenerateRotation
from blend_math_hardware_20261102 import BlendMathHardware
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,DATA,STACK,STOP=scalar.BASE,scalar.DATA,scalar.STACK,scalar.STOP
ENTRY=0x0202DE74
HELPERS={0x02008C28:24,0x02008C58:76,0x0200235C:16,0x020023C4:56,0x02002458:40,
 0x02002534:132,0x02002618:280,0x0202DE04:112}
SPANS={ENTRY:1004,**HELPERS}
CALLBACK=STOP+0x100


def cross(a,b):
    return[(a[1]*b[2]-a[2]*b[1]+2048)//4096,(a[2]*b[0]-a[0]*b[2]+2048)//4096,(a[0]*b[1]-a[1]*b[0]+2048)//4096]


def inputs(index):
    rng=random.Random(0x1004+index);page=bytearray(rng.randbytes(16384));count=index%5;node=index//5%5;scenario=index//25%4
    objects=[];payloads={};eligible=[]
    for i in range(count):
        offset=0x1000+i*0x100;address=DATA+offset;next_address=address+0x100 if i+1<count else 0
        mapped=node<rng.randrange(6);enabled=bool(rng.randrange(2));callback=bool(rng.randrange(2));ratio=rng.choice([-1,0,1,2048,4096,8192])
        if scenario==1:mapped=False
        elif scenario==2:mapped=i==count-1;enabled=True;callback=bool(index//100%2)
        elif count>1 and i==0:mapped=True;enabled=True;callback=True;ratio=rng.choice([1,2048,4096,8192])
        if index%100 in[2,3]and count in[2,3]:mapped=True;enabled=True;callback=i==0;ratio=1 if i==0 else 8192
        num=5 if mapped else node;mapping=(0x100 if mapped else 0)|(0 if enabled else 0x200)|rng.randrange(256)
        struct.pack_into('<iiIIII',page,offset,rng.randrange(4096),ratio,0,CALLBACK if callback else 0,next_address,0)
        struct.pack_into('<BB',page,offset+24,0,num)
        for n in range(5):struct.pack_into('<H',page,offset+26+n*2,mapping if n==node else rng.randrange(65536))
        flags=rng.randrange(64);scale=[rng.randrange(1,8193)for _ in range(9)];rotation=[4096,0,0,0,4096,0,0,0,4096]
        translation=[rng.randrange(-32768,32768)for _ in range(3)]
        payload=struct.pack('<I21i',flags,*scale,*rotation,*translation);payloads[address]=payload
        item=dict(address=address,ratio=ratio,eligible=mapped and enabled,callback=callback,mapValue=mapping,
         flags=flags,scale=scale,rotation=rotation,translation=translation);objects.append(item)
        if item['eligible']:eligible.append(item)
    expected=bytearray(page);calls=[];result=0;output=None
    if count==1:
        if eligible and eligible[0]['callback']:output=payloads[eligible[0]['address']];calls=eligible;result=1
    elif count>1:
        total=sum(max(0,min(p['ratio'],4096))for p in eligible)
        if total and len(eligible)==1:
            if eligible[0]['callback']:output=payloads[eligible[0]['address']];calls=eligible;result=1
        elif total:
            active=[p for p in eligible if p['ratio']>0 and p['callback']]
            if not active or active[0]['address']!=objects[0]['address']:
                raise DegenerateRotation('Original blend fallback basis is uninitialized when the first list node supplies no active callback; excluded C-domain path')
            flags=0xFFFFFFFF;scale=[0]*9;rotation=[0]*6;translation=[0]*3
            for p in active:
                ratio=p['ratio']if total==4096 else(((p['ratio']<<32)//total+0x80000)>>20)
                for j in range(9):scale[j]+=ratio if p['flags']&[1,8,16][j//3]else(ratio*p['scale'][j])//4096
                if not p['flags']&4:
                    for j in range(3):translation[j]+=(ratio*p['translation'][j])//4096
                if p['flags']&2:rotation[0]+=ratio;rotation[4]+=ratio
                else:
                    for j in range(6):rotation[j]+=(ratio*p['rotation'][j])//4096
                flags&=p['flags']
            axis_x=rotation[:3];axis_z=cross(axis_x,rotation[3:6])
            axis_x=normalize(axis_x)if any(axis_x)else active[0]['rotation'][:3]
            axis_z=normalize(axis_z)if any(axis_z)else active[0]['rotation'][6:9]
            axis_y=cross(axis_z,axis_x)
            output=struct.pack('<I21i',flags,*scale,*axis_x,*axis_y,*axis_z,*translation);calls=active;result=1
    if output:expected[0x800:0x858]=output
    context=dict(count=count,node=node,scenario=scenario,objects=objects,expectedReturn=result,
     expectedCalls=[dict(object=p['address'],index=p['mapValue']&255)for p in calls])
    return page,bytes(expected),[DATA+0x800,DATA+0x1000 if count else 0,node],context,payloads


def execute(image,bodies,index,bound=20000):
    page,expected,args,context,payloads=inputs(index);rng=random.Random(0x1004F+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_map(DATA,16384);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192))
    machine.mem_map(0x04000000,4096);hardware=BlendMathHardware(machine)
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1')
    machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xF0000000]))
    for reg in scalar.REGS:machine.reg_write(reg,rng.getrandbits(32))
    for reg,value in zip(scalar.REGS,args):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    seen=set();reads=[];writes=[];returned=False;pending=[];helper_returns=[];calls=[]
    def code(uc,address,size,user):
        nonlocal returned
        if pending and address==pending[-1][1]:helper_returns.append(pending.pop()[0])
        if address in HELPERS:pending.append((address,uc.reg_read(UC_ARM_REG_LR)))
        if address==CALLBACK:
            destination,obj,selected=[uc.reg_read(r)for r in scalar.REGS[:3]];assert obj in payloads
            assert DATA<=destination and destination+88<=DATA+16384 or STACK<=destination and destination+88<=STACK+8192
            calls.append(dict(object=obj,index=selected));uc.mem_write(destination,payloads[obj])
            for reg in[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12]:uc.reg_write(reg,rng.getrandbits(32))
            uc.reg_write(UC_ARM_REG_CPSR,(uc.reg_read(UC_ARM_REG_CPSR)&0x0FFFFFFF)|rng.choice([0,0x80000000,0xF0000000]))
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR));return
        if address==STOP:assert not pending;returned=True;uc.emu_stop();return
        assert any(base<=address<base+n for base,n in SPANS.items()),hex(address);seen.add(address)
    def read(uc,access,address,size,value,user):
        if 0x04000000<=address<0x04001000:hardware.read(address,size)
        reads.append((address,size,int.from_bytes(bytes(uc.mem_read(address,size)),'little')))
    def write(uc,access,address,size,value,user):
        if 0x04000000<=address<0x04001000:hardware.write(address,size,value)
        else:assert DATA<=address and address+size<=DATA+16384 or STACK<=address and address+size<=STACK+8192
        writes.append((address,size,value))
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(ENTRY,STOP+4,count=bound);assert returned,('no top return',index)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096;hardware.verify();output=bytes(machine.mem_read(DATA,16384))
    for address,body in bodies.items():machine.mem_write(address,image[address-BASE:address-BASE+len(body)])
    assert bytes(machine.mem_read(BASE,len(image)))==image
    return dict(index=index,args=args,context=context,actualReturn=True,
     modelPassed=output==expected and machine.reg_read(UC_ARM_REG_R0)==context['expectedReturn']and calls==context['expectedCalls'],
     registers=[machine.reg_read(r)for r in scalar.REGS],flags=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,
     dataSha256=hashlib.sha256(output).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     ownObserved=sorted(seen),suppliedCallbacks=calls,hardwareOperations=hardware.operations,actualHelperReturns=helper_returns)
