import hashlib
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

ENTRY=0x020D1154
DATA=0x02500000
STACK=0x03030000
STOP=0x0F000000
WRAPPERS=DATA+0x1000
METADATA=DATA+0x2000
EKT=DATA+0x8000
MASK=0xFFFFFFFF
NATIVE=[0x02049AD0,0x02049F4C,0x02049FFC,0x02061DCC,0x020CF29C,0x02062A10,0x02044CDC]
PROVIDERS=[0x020875B4,0x02087E44,0x020602EC]
IDS=[1,257,65537,0x80000101,MASK,256]
SPECIES=[0,1,255,256,353,500]


def word(data,offset):return struct.unpack_from('<I',data,offset)[0]


def put(data,offset,value):struct.pack_into('<I',data,offset,value&MASK)


def layout(arm):
    return dict(holders=word(arm,0x49AE0),records=word(arm,0x62A4C),ektState=word(arm,0x44D0C))


def cases():
    for selected in range(4):
        for variant in range(16):
            for nibble in range(16):
                choices=[0,*IDS,0xAABBCCDD]
                first=[choices[(variant+i*3)%8] for i in range(3)]
                second=[choices[(variant*3+i*5+1)%8] for i in range(3)]
                yield dict(selected=selected,first=first,second=second,nibble=nibble)


def initial(arm,case,tag,positions):
    main=bytearray(0x200000);main[:len(arm)]=arm
    arena=bytearray((i*31+tag*11)&255 for i in range(0x20000))
    main[0x1D6BB4]=case['selected']
    for index,value in enumerate(case['first']):put(main,0x1D6BC0+index*4,value)
    context=0x1D69D8+case['selected']*40
    for index,value in enumerate(case['second']):put(main,context+0x18+index*4,value)
    offset=positions['records']-0x02000000
    main[offset:offset+100*0x84]=bytes(100*0x84)
    for index,(uid,species) in enumerate(zip(IDS,SPECIES)):
        put(main,offset+index*0x84+0x14,uid)
        struct.pack_into('<h',main,offset+index*0x84+0x18,species)
    put(main,offset+9*0x84+0x14,IDS[0]);struct.pack_into('<h',main,offset+9*0x84+0x18,499)
    put(main,positions['ektState']-0x02000000+4,EKT)
    for index,species in enumerate(SPECIES):
        struct.pack_into('<H',arena,EKT-DATA+species*100+4,((case['nibble']+index*3)&15)<<8)
    for slot in range(40):
        wrapper=WRAPPERS+slot*8;metadata=METADATA+slot*128
        put(main,positions['holders']-0x02000000+(slot+36)*12,wrapper)
        put(arena,wrapper-DATA+4,metadata)
        put(arena,metadata-DATA+0x44,0x51000000+slot)
        put(arena,metadata-DATA+0x58,0xABCD0000+slot)
    put(arena,0,0)
    return main,arena


def model(case,arena):
    events=[]
    for slot in range(6,12):
        p=METADATA-DATA+slot*128
        events.append((PROVIDERS[0],(METADATA+slot*128,arena[p+0x5E],arena[p+0x5F],arena[p+0x5C],arena[p+0x5D],word(arena,p+0x58))))
    for slot in range(6,12):events.append((PROVIDERS[1],(0x51000000+slot,0)))
    for values,base in [(case['first'],6),(case['second'],9)]:
        y=0
        for uid in values:
            if uid not in IDS:continue
            index=IDS.index(uid);species=SPECIES[index]
            category=((case['nibble']+index*3)&15)//3
            events.append((PROVIDERS[2],(WRAPPERS+(base+y)*8,species,index,0,0,1)))
            y=(y+category+1)&255
    return events


def execute(arm,sizes,case,tag,check=True,parent_code_bytes=372):
    positions=layout(arm);main,arena=initial(arm,case,tag,positions)
    expected=model(case,arena);events=[];pending=[];pcs=set();entered={};returned={};tails={};writes=[]
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000,0x200000);uc.mem_write(0x02000000,bytes(main));uc.mem_protect(0x02000000,0x200000,UC_PROT_READ|UC_PROT_EXEC)
    uc.mem_map(DATA,len(arena));uc.mem_write(DATA,bytes(arena))
    uc.mem_map(STACK,4096);uc.mem_write(STACK,b'\xB7'*4096)
    uc.mem_map(STOP,4096,UC_PROT_READ|UC_PROT_EXEC)
    uc.reg_write(UC_ARM_REG_CPSR,((tag&15)<<28)|0x1F)
    for index,reg in enumerate(REGISTERS):uc.reg_write(reg,(0xA1000000+tag*137+index*0x101)&MASK)
    sp=STACK+0xF00;uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,STOP|(tag&1))
    saved=[uc.reg_read(reg) for reg in REGISTERS[4:12]]
    state=dict(instructions=0,actualTopReturns=0,providedCompletions=0)
    def code(machine,address,size,user):
        state['instructions']+=1
        if pending and address==pending[-1][1]:
            entry,_,_=pending.pop();returned[entry]=returned.get(entry,0)+1
        if address==STOP:
            state['actualTopReturns']+=1;machine.emu_stop();return
        assert size==4 and not machine.reg_read(UC_ARM_REG_CPSR)&32
        if address in NATIVE+PROVIDERS:
            lr=machine.reg_read(UC_ARM_REG_LR);current_sp=machine.reg_read(UC_ARM_REG_SP)
            if pending and (lr,current_sp)==pending[-1][1:]:
                prior,_,_=pending.pop();key=f'{prior:08x}->{address:08x}';tails[key]=tails.get(key,0)+1
            if address in NATIVE:
                entered[address]=entered.get(address,0)+1;pending.append((address,lr,current_sp))
        if address in PROVIDERS:
            count=2 if address==PROVIDERS[1] else 6
            args=[machine.reg_read(reg) for reg in REGISTERS[:min(count,4)]]
            if count>4:args.extend(struct.unpack('<II',bytes(machine.mem_read(machine.reg_read(UC_ARM_REG_SP),8))))
            if address==PROVIDERS[2]:
                offset=args[2]-positions['records'];assert offset%0x84==0 and 0<=offset//0x84<100;args[2]=offset//0x84
            events.append((address,tuple(args)))
            machine.mem_write(DATA,struct.pack('<I',len(events)))
            for index in [0,1,2,3,12]:machine.reg_write(REGISTERS[index],(0xE1000000+tag*31+index*0x100)&MASK)
            machine.reg_write(UC_ARM_REG_CPSR,((tag*3&15)<<28)|0x1F);machine.reg_write(UC_ARM_REG_PC,lr);state['providedCompletions']+=1;return
        assert ENTRY<=address<ENTRY+parent_code_bytes or any(start<=address<start+sizes[start] for start in NATIVE),hex(address)
        if ENTRY<=address<ENTRY+parent_code_bytes:pcs.add(address)
    def write(machine,access,address,size,value,user):
        assert sp-160<=address and address+size<=sp,(hex(address),size)
        writes.append((address-sp,size,value))
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_WRITE,write)
    uc.emu_start(ENTRY,STOP+4,count=18000)
    assert state['actualTopReturns']==1 and not pending and state['instructions']<18000
    assert uc.reg_read(UC_ARM_REG_SP)==sp and [uc.reg_read(reg) for reg in REGISTERS[4:12]]==saved
    assert bytes(uc.mem_read(STACK,0xE60))==b'\xB7'*0xE60 and bytes(uc.mem_read(sp,256))==b'\xB7'*256
    final_arena=bytes(uc.mem_read(DATA,len(arena)));put(arena,0,len(events))
    passed=events==expected and final_arena==bytes(arena) and uc.reg_read(REGISTERS[0])==0x03000000
    if check:assert passed,(case,events,expected)
    return dict(modelPassed=passed,events=events,state=state,nativeEntries=entered,nativeActualReturns=returned,tailTransfers=tails,
        pcs=sorted(pcs),registers=[uc.reg_read(reg) for reg in REGISTERS]+[uc.reg_read(UC_ARM_REG_SP),uc.reg_read(UC_ARM_REG_CPSR)],
        arenaSha256=hashlib.sha256(final_arena).hexdigest(),stackWritesSha256=hashlib.sha256(repr(writes).encode()).hexdigest())
