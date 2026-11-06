import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3


def seed_record_copy003(engine,address,vector):
    if address!=0x021DB4A8:return {}
    source=bytearray(engine.mem_read(0x03006000,132));struct.pack_into('<h',source,24,[-32768,-1,0,1,32767][vector%5]);source[26]=[0,127,128,255][vector//5%4]
    engine.mem_write(0x03006000,bytes(source));return {'source':bytes(source),'target':bytes(engine.mem_read(0x0300A000,320)),'present':vector%2,'calls':[]}


def record_copy_arguments003(address,vector,args):
    if address==0x021DB4A8:args[:2]=[0x0300A000,0x03006000 if vector%2 else 0]


def generated(source):
    species=int.from_bytes(source[24:26],'little',signed=True);variant=source[26];skills=source[122:132]
    family=bytes(((species&255)^variant^skills[i%10]^i)&255 for i in range(64));stats=bytes((skills[i%10]+family[i]+i)&255 for i in range(32));extra=bytes((family[i]+species+variant)&255 for i in range(32))
    return species,variant,family,stats,extra


def record_copy_call003(engine,address,name,value,state):
    if address!=0x021DB4A8:return value
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]];species,variant,family,stats,extra=generated(state['source'])
    if name=='func_0207b460':
        if args!=[species&0xFFFFFFFF,variant,0x0300607A,0x0300A04A]:raise ValueError('Record conversion family-generation arguments differ')
        engine.mem_write(args[3],family)
    if name=='func_0207b1c4':
        if args[:3]!=[0x0300607A,0x0300A04A,0x0300A00C] or bytes(engine.mem_read(args[1],64))!=family:raise ValueError('Record conversion skill/stat generation differs')
        engine.mem_write(args[2],stats)
    if name=='func_0207c078':
        if args!=[species&0xFFFFFFFF,variant,0x0300A04A,0x0300A08A] or bytes(engine.mem_read(args[2],64))!=family:raise ValueError('Record conversion derived-field generation differs')
        engine.mem_write(args[3],extra)
    return value


def assert_record_copy003(engine,address,args,calls,state):
    if address!=0x021DB4A8:return
    target=bytearray(state['target']);source=state['source'];expected=[]
    if not state['present']:struct.pack_into('<h',target,46,-1);struct.pack_into('<I',target,0,0xFFFFFFFF)
    else:
        species,variant,family,stats,extra=generated(source)
        target[182:202]=source[:20];struct.pack_into('<i',target,0,species);target[46:48]=source[24:26];target[48]=variant;target[4:8]=source[20:24];target[177]=source[27];target[178]=source[30];target[175]=source[28]
        target[214:224]=source[122:132];target[224:282]=source[64:122];target[284:316]=source[32:64];target[74:138]=family;target[12:44]=stats;target[138:170]=extra
        expected=['func_02008e0c']*4+['func_0207b460','func_0207b1c4','func_0207c078']
        copies=[[0x03006000,0x0300A0B6,20],[0x0300607A,0x0300A0D6,10],[0x03006040,0x0300A0E0,58],[0x03006020,0x0300A11C,32]]
        if [c['args'][:3] for c in calls if c['name']=='func_02008e0c']!=copies:raise ValueError('Record conversion four native copy spans differ')
    if [c['name'] for c in calls]!=expected or bytes(engine.mem_read(0x0300A000,320))!=bytes(target) or bytes(engine.mem_read(0x03006000,132))!=source:raise ValueError('Record conversion complete target/padding/source effects differ')
