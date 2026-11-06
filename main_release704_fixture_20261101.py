import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from project import ROOT,read_json

DATA,STACK,STOP=0x02400000,0x03030000,0x0F000000
SPECS={0x0202E858:96,0x0202F358:132,0x0202F48C:148,0x020321DC:328}
CALLEES=[0x0202BEDC,0x0202BEEC,0x0202EDDC,0x0202ED24,0x0202F0E4,0x0202F358,0x0202F48C,0x0203C054,0x0203C064]
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
CANONICAL={int(f["address"],0):f["size"]for m in read_json(ROOT/"evidence/regions/canonical-symbol-functions.json")["canonicalModules"]
 for f in m["functions"]if m["module"]=="main"}


def graph(index):
    rng=random.Random(0x70400000+index);page=bytearray(rng.randbytes(65536))
    file,mdlset,tex,anm=DATA+0x100,DATA+0x1000,DATA+0xD000,DATA+0xE000
    count=[0,1,2,4][index%4];pltt_count=[0,1,2,7,16,31][(index//4)%6];unit=[4,8,12,16][(index//24)%4]
    dictionary=mdlset+8;header=dictionary+0x100
    page[dictionary-DATA+1]=count;struct.pack_into("<H",page,dictionary-DATA+6,0x100)
    struct.pack_into("<HH",page,header-DATA,unit,4+count*unit)
    models=[];flags=[]
    for model_index in range(max(1,count)):
        mdl=DATA+0x3000+model_index*0x1000;mat=mdl+0x100
        if model_index<count:struct.pack_into("<I",page,header-DATA+4+model_index*unit,mdl-mdlset)
        struct.pack_into("<I",page,mdl-DATA+8,mat-mdl)
        page[mdl-DATA+23]=[0,1,2,15,127,254,255][(index//6)%7]
        page[mdl-DATA+24]=[255,254,127,15,2,1,0][(index//6)%7]
        struct.pack_into("<HH",page,mat-DATA,0x40,0x80)
        page[mat-DATA+0x41]=0
        pd=mat+0x80;ph=pd+0x100
        page[pd-DATA+1]=pltt_count;struct.pack_into("<H",page,pd-DATA+6,0x100)
        struct.pack_into("<HH",page,ph-DATA,unit,4+pltt_count*unit)
        model_flags=[]
        for item in range(pltt_count):
            address=ph+4+item*unit+3
            page[address-DATA]=[0,1,2,3,0x7F,0x80,0xFE,0xFF][(index+item+model_index)%8]
            model_flags.append(address)
        models.append(mdl);flags.append(model_flags)
    choices=[b"BMD0",b"BMD0",b"BTX0",b"BTX0",b"BCA0",b"BVA0",b"BMA0",b"BTP0",b"BTA0",b"NOPE"]
    signature=choices[index%len(choices)];blocks=1if index%len(choices)in[1,2]else 2
    page[file-DATA:file-DATA+4]=signature;struct.pack_into("<HH",page,file-DATA+12,16,blocks)
    first=tex if signature==b"BTX0"and blocks==1 else mdlset
    struct.pack_into("<II",page,file-DATA+16,first-file,tex-file)
    keys=[0,1,0x7FFFFFFF,0x80000000,0xFFFFFFFF]
    for number,offset in enumerate([8,24,44]):struct.pack_into("<I",page,tex-DATA+offset,keys[(index//10+number)%5])
    page[anm-DATA]=[ord("M"),ord("J"),ord("V"),0,255,ord("A")][index%6]
    return page,dict(file=file,mdlset=mdlset,tex=tex,anm=anm,models=models,flags=flags,
     signature=signature.hex(),blocks=blocks,count=count,plttCount=pltt_count,unit=unit)


def execute(image,entry,body,index,bound=65536):
    page,context=graph(index);before=bytes(page);expected=bytearray(page);expected_return=None
    if entry==0x0202E858:
        am=context["anm"]if(index//48)%4 not in[1,3]else 0
        mdl=context["models"][0]if(index//48)%4 not in[2,3]else 0
        arguments=[am,mdl]
        category=page[context["anm"]-DATA]
        expected_return=0
        if am and mdl and category in[ord("M"),ord("J"),ord("V")]:
            number=page[mdl-DATA+(24if category==ord("M")else 23)]
            expected_return=(32+2*number)&~3
    elif entry==0x0202F358:arguments=[context["models"][0]]
    elif entry==0x0202F48C:arguments=[context["mdlset"]]
    else:arguments=[context["file"]]
    signature=bytes.fromhex(context["signature"])
    has_tex=signature==b"BTX0"or(signature==b"BMD0"and context["blocks"]!=1)
    release_model=entry in[0x0202F358,0x0202F48C]or(entry==0x020321DC and signature==b"BMD0"and has_tex)
    if release_model:
        lists=context["flags"][:1]if entry==0x0202F358 else context["flags"][:context["count"]]
        for addresses in lists:
            for address in addresses:expected[address-DATA]&=0xFE
    if entry==0x020321DC and has_tex:
        for offset in[8,24,44]:struct.pack_into("<I",expected,context["tex"]-DATA+offset,0)
        for offset in[16,32,50]:
            value=struct.unpack_from("<H",expected,context["tex"]-DATA+offset)[0]
            struct.pack_into("<H",expected,context["tex"]-DATA+offset,value&~1)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.mem_map(0x02000000,0x100000);machine.mem_write(0x02000000,image)
    machine.mem_write(entry,body);main_before=bytes(machine.mem_read(0x02000000,0x100000))
    machine.mem_map(DATA,65536);machine.mem_write(DATA,before);machine.mem_map(STACK,4096)
    rng=random.Random(0x704ABC00+index);stack=rng.randbytes(4096);machine.mem_write(STACK,stack);machine.mem_map(STOP,4096)
    initial=[rng.getrandbits(32)for register in REGS]
    for register,value in zip(REGS,initial):machine.reg_write(register,value)
    for register,value in zip(REGS,arguments):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28));machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,STOP)
    entries={address:CANONICAL[address]for address in CALLEES};entries[entry]=len(body)
    allowed={pc for address,size in entries.items()for pc in range(address,address+size,4)}
    own=set();reads=[];writes=[];calls=[];frames=[];completed=[]
    def code(uc,address,size,unused):
        assert address in allowed,hex(address)
        while frames and address==frames[-1]["lr"]:completed.append(frames.pop())
        if address in entries:
            frame=dict(entry=address,lr=uc.reg_read(UC_ARM_REG_LR),sp=uc.reg_read(UC_ARM_REG_SP))
            frames.append(frame);calls.append(dict(**frame,args=[uc.reg_read(r)for r in REGS[:4]]))
        if entry<=address<entry+len(body):own.add(address)
    def read(uc,access,address,size,value,unused):
        assert 0x02000000<=address and address+size<=0x02100000 or DATA<=address and address+size<=DATA+65536 or STACK<=address and address+size<=STACK+4096,hex(address)
        reads.append([address,size,bytes(uc.mem_read(address,size)).hex()])
    def write(uc,access,address,size,value,unused):
        if STACK<=address and address+size<=STACK+4096:assert STACK+1536<=address and address+size<=STACK+2048
        else:assert DATA<=address and address+size<=DATA+65536,hex(address)
        writes.append([address,size,value&((1<<(size*8))-1)])
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP,count=bound)
    assert machine.reg_read(UC_ARM_REG_PC)==STOP,"Prefix is not actual return"
    while frames and frames[-1]["lr"]==STOP:completed.append(frames.pop())
    assert not frames
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+2048
    assert all(machine.reg_read(r)==value for r,value in zip(REGS[4:12],initial[4:12]))
    assert bytes(machine.mem_read(0x02000000,0x100000))==main_before
    after=bytes(machine.mem_read(DATA,65536));after_stack=bytes(machine.mem_read(STACK,4096))
    assert after_stack[:1536]==stack[:1536]and after_stack[2048:]==stack[2048:]
    r0=machine.reg_read(UC_ARM_REG_R0)
    return dict(index=index,context=context,arguments=arguments,actualReturn=True,rawR0=r0,
     modelPassed=after==expected and(expected_return is None or r0==expected_return),expectedReturn=expected_return,
     registers=[machine.reg_read(r)for r in REGS],cpsr=machine.reg_read(UC_ARM_REG_CPSR),lr=machine.reg_read(UC_ARM_REG_LR),
     reads=reads,writes=writes,calls=calls,completedNativeEntries=completed,actualHelperReturns=sum(f["entry"]!=entry for f in completed),
     providedCalls=0,ownedObserved=sorted(own),pageSha256=hashlib.sha256(after).hexdigest(),stackSha256=hashlib.sha256(after_stack).hexdigest())
