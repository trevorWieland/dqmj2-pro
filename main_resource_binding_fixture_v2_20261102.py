import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from draw676_positive_divider_20261102 import PositiveDivider

BASE,DATA,STACK,STOP=0x02000000,0x02400000,0x03030000,0x0F000000
SPANS={0x02031FA4:568,0x0202EDFC:304,0x0202EFE4:256,0x0202F170:224,0x0202F250:264,0x0202F3DC:176}
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def word(page,offset):return struct.unpack_from('<I',page,offset)[0]
def half(page,offset):return struct.unpack_from('<H',page,offset)[0]
def key(index):return ('RESOURCE_%06d'%index).encode().ljust(16,b'\0')


def dictionary(page,base,rows,names):
    page[base]=0;page[base+1]=len(rows);struct.pack_into('<HHH',page,base+2,256,0,32)
    unit=len(rows[0])if rows else 4;struct.pack_into('<HH',page,base+32,unit,64)
    for index,row in enumerate(rows):page[base+36+unit*index:base+36+unit*(index+1)]=row
    for index,name in enumerate(names):page[base+96+16*index:base+112+16*index]=name


def inputs(index):
    rng=random.Random(0xB1AD1808+index);page=bytearray(rng.randbytes(65536));tex=0x1000;mdlset=0x2000
    normal,compressed,palette=[rng.getrandbits(32)for _ in range(3)]
    struct.pack_into('<I',page,tex+8,normal);struct.pack_into('<I',page,tex+24,compressed);struct.pack_into('<I',page,tex+44,palette)
    texture_count=rng.randrange(4);palette_count=rng.randrange(4)
    texture_rows=[]
    for n in range(texture_count):
        fmt=rng.randrange(8);param=(rng.getrandbits(32)&~0x1C000000)|(fmt<<26)
        width,height=[rng.choice([0,8,16,24,32,48,64])for _ in range(2)]
        texture_rows.append(struct.pack('<II',param,width|(height<<11)|(rng.getrandbits(10)<<22)))
    dictionary(page,tex+60,texture_rows,[key(i)for i in range(texture_count)])
    palette_rows=[struct.pack('<HH',rng.randrange(65536),rng.randrange(65536))for _ in range(palette_count)]
    dictionary(page,tex+0x300,palette_rows,[key(i)for i in range(palette_count)])
    struct.pack_into('<H',page,tex+52,0 if index%11==0 else 0x300)
    models=[0x3000+i*0x1800 for i in range(3)]
    dictionary(page,mdlset+8,[struct.pack('<I',m-mdlset)for m in models[:rng.randrange(4)]],[key(i+10)for i in range(3)])
    for model in models:
        mat=model+0x100;struct.pack_into('<I',page,model+8,0x100)
        struct.pack_into('<HH',page,mat,0x100,0x300)
        dictionary(page,mat+4,[struct.pack('<I',0x800+n*0x100)for n in range(3)],[key(n+20)for n in range(3)])
        for offset,tag in[(0x100,0),(0x300,1)]:
            count=rng.randrange(4);rows=[];names=[]
            for n in range(count):
                listing=0x600+tag*64+n*16;length=rng.randrange(4)
                page[mat+listing:mat+listing+length]=bytes(rng.randrange(3)for _ in range(length))
                rows.append(struct.pack('<HBB',listing,length,rng.randrange(256)));names.append(key(rng.randrange(4)))
            dictionary(page,mat+offset,rows,names)
        for n in range(3):
            record=mat+0x800+n*0x100;struct.pack_into('<HH',page,record+32,rng.choice([8,16,24,48]),rng.choice([8,16,24,48]))
    entry=[0x0202F3DC,0x0202EFE4,0x0202F250,0x0202EDFC,0x0202F170][index%5]
    texarg=0 if index%13==0 and entry in[0x0202F3DC,0x0202EFE4,0x0202F250]else DATA+tex
    mat=models[0]+0x100
    if entry==0x0202F3DC:args=[DATA+mdlset,texarg]
    elif entry in[0x0202EFE4,0x0202F250]:args=[DATA+models[0],texarg]
    elif entry==0x0202EDFC:args=[DATA+mat,DATA+mat+0x100+36,DATA+tex,DATA+tex+60+36]
    else:args=[DATA+mat,DATA+mat+0x300+36,DATA+tex,DATA+tex+0x300+36]
    if entry==0x0202EDFC and not texture_count:dictionary(page,tex+60,[struct.pack('<II',0,8|(8<<11))],[key(0)])
    if entry==0x0202F170 and not palette_count:dictionary(page,tex+0x300,[struct.pack('<HH',0,0)],[key(0)])
    if entry in[0x0202EDFC,0x0202F170]:
        binding=args[1]-DATA;struct.pack_into('<HBB',page,binding,0x600,rng.randrange(4),rng.randrange(256))
        page[mat+0x600:mat+0x604]=bytes(rng.randrange(3)for _ in range(4))
    return page,entry,args


def lookup(page,base,name):
    entry=base+half(page,base+6);unit=half(page,entry);names=entry+half(page,entry+2)
    for n in range(page[base+1]):
        if bytes(page[names+16*n:names+16*(n+1)])==name:return entry+4+n*unit
    return None


def apply_record(page,mat,binding,tex,item,palette):
    indices=mat+half(page,binding);count=page[binding+2]
    entry=mat+4+half(page,mat+10);unit=half(page,entry)
    for n in range(count):
        record=mat+word(page,entry+4+page[indices+n]*unit)
        if palette:
            offset=half(page,item);vram=word(page,tex+44)&65535
            if not half(page,item+2)&1:offset>>=1;vram>>=1
            struct.pack_into('<H',page,record+28,(offset+vram)&65535)
        else:
            param=word(page,item);compressed=(param&0x1C000000)==5<<26
            vram=word(page,tex+(24 if compressed else 8))&65535
            struct.pack_into('<I',page,record+20,word(page,record+20)|((param+vram)&0xFFFFFFFF))
            extra=word(page,item+4)
            for dim,orig,out in[(extra&2047,half(page,record+32),record+36),((extra>>11)&2047,half(page,record+34),record+40)]:
                value=4096 if dim==orig else (((dim<<32)//orig+(1<<19))>>20)
                struct.pack_into('<I',page,out,value)
    page[binding+3]|=1


def model(page,entry,args):
    expected=bytearray(page)
    def bind(model,tex,palette):
        mat=model+word(expected,model+8);dictionary=mat+half(expected,mat+(2 if palette else 0));result=1
        header=dictionary+half(expected,dictionary+6);unit=half(expected,header);names=header+half(expected,header+2)
        for n in range(expected[dictionary+1]):
            name=bytes(expected[names+n*16:names+(n+1)*16]);item=None
            if tex is not None:
                target=tex+half(expected,tex+52)if palette else tex+60
                if not palette or half(expected,tex+52):item=lookup(expected,target,name)
            if item is None:result=0;continue
            binding=header+4+unit*n
            if not expected[binding+3]&1:apply_record(expected,mat,binding,tex,item,palette)
        return result
    if entry==0x0202F3DC:
        base=args[0]-DATA;d=base+8;header=d+half(expected,d+6);result=1
        for n in range(expected[d+1]):
            mdl=base+word(expected,header+4+n*half(expected,header));tex=args[1]-DATA if args[1]else None
            result&=bind(mdl,tex,False);result&=bind(mdl,tex,True)
    elif entry in[0x0202EFE4,0x0202F250]:result=bind(args[0]-DATA,args[1]-DATA if args[1]else None,entry==0x0202F250)
    else:apply_record(expected,*[a-DATA for a in args],entry==0x0202F170);result=None
    return bytes(expected),result


def execute(image,bodies,index,bound=50000,prepared=None,services=None):
    if prepared is None:
        page,entry,args=inputs(index);expected,result=model(page,entry,args)
    else:page,entry,args,expected,result=prepared
    rng=random.Random(0xF300+index);expected_main=bytearray(image);provided=[]
    if services is not None:
        for address,value in services.globals.items():struct.pack_into('<I',expected_main,address-BASE,value)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,bytes(expected_main))
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_map(DATA,65536);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192))
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');hardware=rng.randbytes(4096)
    machine.mem_map(0x04000000,4096);machine.mem_write(0x04000000,hardware);divider=PositiveDivider(machine,hardware)
    machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xF0000000]))
    for reg in REGS:machine.reg_write(reg,rng.getrandbits(32))
    for reg,value in zip(REGS,args):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    reads=[];writes=[];seen=set();returned=False
    def code(uc,address,size,user):
        nonlocal returned
        if address==STOP:returned=True;uc.emu_stop();return
        if services is not None and address in services.entries:
            words=[uc.reg_read(r)for r in REGS[:4]];result=services.invoke(address,words);provided.append(dict(entry=address,words=words,result=result))
            for n,reg in enumerate([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12]):uc.reg_write(reg,(0xC3110000+len(provided)*17+n)&0xFFFFFFFF)
            uc.reg_write(UC_ARM_REG_R0,result);uc.reg_write(UC_ARM_REG_CPSR,0x10|((len(provided)&15)<<28));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR));return
        assert BASE<=address<BASE+len(image),hex(address);seen.add(address)
    def read(uc,access,address,size,value,user):
        if 0x04000000<=address<0x04001000:divider.read(address,size)
        reads.append((address,size,int.from_bytes(bytes(uc.mem_read(address,size)),'little')))
    def write(uc,access,address,size,value,user):
        if 0x04000000<=address<0x04001000:divider.write(address,size,value)
        else:assert DATA<=address and address+size<=DATA+65536 or STACK<=address and address+size<=STACK+8192
        writes.append((address,size,value))
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP+4,count=bound);assert returned,('no top return',index)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096
    observed_page=bytes(machine.mem_read(DATA,65536));passed=observed_page==expected and(result is None or machine.reg_read(UC_ARM_REG_R0)==result)
    for address,body in bodies.items():machine.mem_write(address,image[address-BASE:address-BASE+len(body)])
    assert bytes(machine.mem_read(BASE,len(image)))==bytes(expected_main)
    assert bytes(machine.mem_read(0x04000000,4096))==bytes(divider.expected)
    return dict(index=index,entry=entry,args=args,actualReturn=True,modelPassed=passed,expectedReturn=result,
     registers=[machine.reg_read(r)for r in REGS],flags=machine.reg_read(UC_ARM_REG_CPSR),
     dataSha256=hashlib.sha256(observed_page).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     reads=reads,writes=writes,divisionOperations=divider.operations,providedCalls=provided,
     ownedObserved=sorted(a for a in seen if any(b<=a<b+n for b,n in SPANS.items())))
