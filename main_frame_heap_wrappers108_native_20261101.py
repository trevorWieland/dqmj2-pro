import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS as REGS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ,UcError
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_CPSR,UC_ARM_REG_PC

DATA,GLOBAL,STACK,STOP=0x02380000,0x020ED000,0x03030000,0x0F000000
HEADER,EXP=0x0202B914,0x0202AE28
CREATOR,ALLOCATOR=0x0202B740,0x0202B784
HELPERS={0x0202B54C:72,0x0202B594:128,0x0202B614:124,HEADER:160,0x0202B9CC:16,
    0x0202B9DC:24,0x0202B8EC:40,0x0202B884:104,0x0202BA20:84,0x0202B9F4:44,0x0202BB88:24,0x02008C14:20}


def scenario(image, entry, index):
    rng = random.Random(entry * 100000 + index)
    pages = [bytearray(rng.randbytes(4096)) for unused in range(2)]
    heap = DATA + 0x500
    flags = [0, 1, 2, 3, 0x80, 0xFF, 0x100, 0x102, 0xFFFF, 0xFFFFFFFF][index // 6 % 10]
    initialized = [0, 1, 0x100, 0x80000000][index // 60 % 4]
    shape = index % 6 if initialized else 0
    span = [20, 24, 64, 256, 512][index // 240 % 5]
    start = heap + (0x38 if entry == EXP else 0x24)
    end = start + span
    signature = 0x45585048 if entry == EXP else [0, 0x46524D48, 0xFFFFFFFF, rng.getrandbits(32)][index % 4]

    def put(page, offset, value, half=False):
        struct.pack_into('<H' if half else '<I', page, offset, value)

    def initial_list(address, objects):
        page = pages[1] if address >= GLOBAL and address < GLOBAL + 4096 else pages[0]
        offset = address - (GLOBAL if page is pages[1] else DATA)
        put(page, offset, objects[0] if objects else 0)
        put(page, offset + 4, objects[-1] if objects else 0)
        put(page, offset + 8, len(objects), True)
        put(page, offset + 10, 4, True)
        for slot, obj in enumerate(objects):
            put(pages[0], obj - DATA + 4, objects[slot - 1] if slot else 0)
            put(pages[0], obj - DATA + 8, objects[slot + 1] if slot + 1 < len(objects) else 0)

    def existing(obj, begin, finish):
        put(pages[0], obj - DATA + 0x18, begin)
        put(pages[0], obj - DATA + 0x1C, finish)
        initial_list(obj + 0xC, [])

    root = GLOBAL + 0xF78
    target = root
    roots = []
    if shape in [1, 2, 4]:
        parent = DATA + 0x100
        existing(parent, DATA + 0x200, DATA + 0xF00)
        roots = [parent]
        target = parent + 0xC
        if shape == 2:
            child = DATA + 0x300
            existing(child, DATA + 0x400, DATA + 0xE00)
            initial_list(parent + 0xC, [child])
            target = child + 0xC
        elif shape == 4:
            child = DATA + 0x380
            existing(child, DATA + 0x3C0, DATA + 0x480)
            initial_list(parent + 0xC, [child])
    elif shape == 3:
        first, second = DATA + 0x100, DATA + 0x300
        existing(first, DATA + 0x200, DATA + 0x280)
        existing(second, DATA + 0x400, DATA + 0xF00)
        roots = [first, second]
        target = second + 0xC
    elif shape == 5:
        parent = DATA + 0x100
        existing(parent, DATA + 0x200, DATA + 0x300)
        roots = [parent]
    initial_list(root, roots)
    put(pages[1], 0xF74, initialized)
    expected = [bytearray(page) for page in pages]
    put(expected[0], 0x500, signature)
    put(expected[0], 0x518, start)
    put(expected[0], 0x51C, end)
    put(expected[0], 0x520, flags & 255)
    if flags & 2:
        fill = image[0x020DD588 - 0x02000000:0x020DD58C - 0x02000000]
        expected[0][start - DATA:end - DATA] = fill * (span // 4)
    for offset in [0x50C, 0x510]:
        put(expected[0], offset, 0)
    put(expected[0], 0x514, 0, True)
    put(expected[0], 0x516, 4, True)
    if not initialized:
        put(expected[1], 0xF74, 1)
        for offset in [0xF78, 0xF7C]:
            put(expected[1], offset, 0)
        put(expected[1], 0xF80, 0, True)
        put(expected[1], 0xF82, 4, True)
    page = expected[1] if target == root else expected[0]
    offset = target - (GLOBAL if target == root else DATA)
    old_tail = struct.unpack_from('<I', page, offset + 4)[0]
    put(expected[0], 0x504, old_tail)
    put(expected[0], 0x508, 0)
    if old_tail:
        put(expected[0], old_tail - DATA + 8, heap)
    else:
        put(page, offset, heap)
    put(page, offset + 4, heap)
    count = struct.unpack_from('<H', page, offset + 8)[0]
    put(page, offset + 8, (count + 1) & 0xFFFF, True)
    if entry == EXP:
        put(expected[0], 0x534, 0, True)
        put(expected[0], 0x536, 0, True)
        put(expected[0], start - DATA, 0x4652, True)
        put(expected[0], start - DATA + 2, 0, True)
        put(expected[0], start - DATA + 4, span - 16)
        put(expected[0], start - DATA + 8, 0)
        put(expected[0], start - DATA + 12, 0)
        for offset in [0x524, 0x528]:
            put(expected[0], offset, start)
        for offset in [0x52C, 0x530]:
            put(expected[0], offset, 0)
    registers = [rng.getrandbits(32) for unused in REGS]
    registers[:4] = [heap, signature, start, end] if entry == HEADER else [heap, end, flags, registers[3]]
    return pages, expected, registers, flags, heap, rng


def creator_case(image,index):
    pages,expected,initial,flags,heap,rng=scenario(image,HEADER,index)
    if 1200<=index<1330:
        starts=[0,1,2,3,0xFFFFFFFC,0xFFFFFFFD,0xFFFFFFFE,0xFFFFFFFF,0x80000000,0x7FFFFFFF]
        sizes=[0,1,3,4,44,47,48,49,52,63,64,0xFFFFFFFF,0x80000000]
        raw_start=starts[(index-1200)//len(sizes)];raw_bytes=sizes[(index-1200)%len(sizes)]
        aligned=(raw_start+3)&0xFFFFFFFC;end=(raw_start+raw_bytes)&0xFFFFFFFC
        accepted=aligned<=end and end-aligned>=48
        initial[:3]=[raw_start,raw_bytes,0]
        return pages,[bytearray(page)for page in pages],initial,0,rng,dict(kind='creator-wrap-guard',rawStart=raw_start,rawBytes=raw_bytes,
            alignedStart=aligned,alignedEnd=end,guardAccepted=accepted,modelDomain=not accepted)
    end=initial[3]
    if index>=1330:
        end=heap+48+(index-1330)%4*4
        last=max(end,initial[3]);begin=heap+48
        expected[0][begin-DATA:last-DATA]=pages[0][begin-DATA:last-DATA]
        if flags&2:expected[0][begin-DATA:end-DATA]=image[0xDD588:0xDD58C]*((end-begin)//4)
        struct.pack_into('<I',expected[0],heap-DATA+28,end)
    raw_start=heap-(index%4);raw_bytes=end-raw_start+(index%4)
    struct.pack_into('<I',expected[0],heap-DATA,0x46524D48)
    struct.pack_into('<I',expected[0],heap-DATA+24,heap+48)
    struct.pack_into('<III',expected[0],heap-DATA+36,heap+48,end,0)
    initial[:3]=[raw_start,raw_bytes,flags]
    return pages,expected,initial,heap,rng,dict(kind='mapped-creator',rawStart=raw_start,rawBytes=raw_bytes,flags=flags,alignedStart=heap,alignedEnd=end,modelDomain=True)


def allocation_case(image,index):
    rng=random.Random(ALLOCATOR*10000+index);pages=[bytearray(rng.randbytes(4096)),bytearray(rng.randbytes(4096))]
    heap=DATA+0x500;head=DATA+0x800+(index//8%4)*4;tail=DATA+0xC00-(index//16%4)*4
    requested=[0,1,3,4,16,63,64,255,1024,0xFFFFFFFC,0xFFFFFFFD,0xFFFFFFFE,0xFFFFFFFF,0x80000000][index%14]
    alignment=[0,1,2,3,4,8,16,64,-1,-3,-4,-16,-0x80000000,0x7FFFFFFF][index//14%14]
    flags=[0,1,2,3,0x80,0x100,0xFFFF,0xFFFFFFFF][index//196%8]
    struct.pack_into('<IIII',pages[0],heap-DATA+32,flags,head,tail,rng.getrandbits(32));expected=[bytearray(page)for page in pages]
    normalized=((requested or 1)+3)&0xFFFFFFFC;backwards=alignment<0;mask_alignment=(-alignment if backwards else alignment)&0xFFFFFFFF
    mask=(~((mask_alignment-1)&0xFFFFFFFF))&0xFFFFFFFF
    result=(((tail-normalized)&0xFFFFFFFF)&mask)if backwards else(((head+mask_alignment-1)&0xFFFFFFFF)&mask)
    updated=result if backwards else(result+normalized)&0xFFFFFFFF
    accepted=result>=head if backwards else updated<=tail
    begin=result if backwards else head;length=((tail-result)&0xFFFFFFFF)if backwards else((updated-head)&0xFFFFFFFF)
    model_domain=True
    if accepted:
        if flags&3:
            finish=(begin+length)&0xFFFFFFFF
            signed_begin=begin-0x100000000 if begin&0x80000000 else begin
            signed_finish=finish-0x100000000 if finish&0x80000000 else finish
            effective=max(0,signed_finish-signed_begin)
            if effective and(not DATA<=begin<=DATA+4096 or begin+effective>DATA+4096):model_domain=False
            elif effective:
                table=struct.unpack_from('<I',image,0x2B9D8)[0]-0x02000000
                pattern=bytes(4)if flags&1 else image[table+4:table+8]
                expected[0][begin-DATA:begin-DATA+effective]=pattern*(effective//4)
        struct.pack_into('<I',expected[0],heap-DATA+(40 if backwards else 36),updated)
    else:result=0
    initial=[rng.getrandbits(32)for unused in REGS];initial[:3]=[heap,requested,alignment&0xFFFFFFFF]
    return pages,expected,initial,result,rng,dict(kind='allocator',requested=requested,normalized=normalized,alignment=alignment,
        flags=flags,oldHead=head,oldTail=tail,backwards=backwards,accepted=accepted,modelDomain=model_domain,
        resultingHead=(head if backwards or not accepted else updated),resultingTail=(tail if not backwards or not accepted else updated))


def execute(image,entry,body,index,budget=20000):
    maker=creator_case if entry==CREATOR else allocation_case
    pages,expected,initial,result,rng,spec=maker(image,index)
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_946)
    cpu.mem_map(0x02000000,0x800000);cpu.mem_write(0x02000000,image);cpu.mem_write(entry,body)
    for address,page in zip([DATA,GLOBAL],pages):cpu.mem_write(address,bytes(page))
    cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xA5])*4096);cpu.mem_map(STOP,4096)
    initial[-2:]=[STACK+0x800,STOP|(index&1)];control=0x10|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|control)
    for reg,value in zip(REGS,initial):cpu.reg_write(reg,value)
    pending=[];returned=[];calls=[];reads=[];writes=[];visited=[];stopped=False
    def code(machine,address,width,user):
        nonlocal stopped
        while pending and pending[-1][1]==address:returned.append(pending.pop()[0])
        if address==STOP:stopped=True;machine.emu_stop();return
        if address in HELPERS:
            sp=machine.reg_read(REGS[-2]);calls.append([address,[machine.reg_read(r)for r in REGS[:4]],struct.unpack('<I',machine.mem_read(sp,4))[0]])
            pending.append((address,machine.reg_read(REGS[-1])&~1))
        if not(entry<=address<entry+len(body)or any(a<=address<a+n for a,n in HELPERS.items())):raise ValueError('Frame heap instruction escaped qualified native/source scope')
        visited.append(address)
    def write(machine,access,address,width,value,user):
        if not(any(a<=address and address+width<=a+4096 for a in(DATA,GLOBAL))or STACK+0x600<=address and address+width<=STACK+0x800):
            raise ValueError('Frame heap write crossed disposable backing boundary')
        writes.append([address,width,value&((1<<(8*width))-1)])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    cpu.hook_add(UC_HOOK_MEM_READ,lambda machine,access,address,width,value,user:reads.append([address,width]))
    failure=None
    try:cpu.emu_start(entry,STOP+4,count=budget)
    except (UcError,ValueError) as error:failure=dict(type=type(error).__name__,reason=str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)))
    if not stopped:
        return dict(case=spec,actualOwnReturn=False,postStateExcluded=True,failure=failure or dict(type='InstructionCapOrBoundary',reason='No actual return'),
            instructionCount=len(visited),observedCompletedHelperReturnsBeforeStop=returned,sourceCredit=0)
    if pending or cpu.reg_read(REGS[-2])!=STACK+0x800:raise ValueError('Frame heap return stack/nested return evidence differs')
    if any(cpu.reg_read(REGS[i])!=initial[i]for i in range(4,12))or cpu.reg_read(UC_ARM_REG_CPSR)&0xDF!=control:raise ValueError('Frame heap callee-save/control ABI differs')
    if bytes(cpu.mem_read(STACK,0x600))!=bytes([0xA5])*0x600 or bytes(cpu.mem_read(STACK+0x800,0x800))!=bytes([0xA5])*0x800:raise ValueError('Frame heap outer stack guards differ')
    actual=[bytes(cpu.mem_read(a,4096))for a in(DATA,GLOBAL)];value=cpu.reg_read(REGS[0])
    return dict(case=spec,actualOwnReturn=True,modelPassed=spec['modelDomain']and actual==expected and value==result,
        expectedResult=result,result=value,rawRegisters=[cpu.reg_read(r)for r in REGS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
        mappedMemorySha256=hashlib.sha256(bytes(cpu.mem_read(0x02000000,0x800000))).hexdigest(),
        stackSha256=hashlib.sha256(bytes(cpu.mem_read(STACK,4096))).hexdigest(),pagesSha256=hashlib.sha256(b''.join(actual)).hexdigest(),expectedPagesSha256=hashlib.sha256(b''.join(expected)).hexdigest(),
        orderedReads=reads,orderedWrites=writes,typedCallObservations=calls,actualOriginalHelperReturnsSeparate=returned,
        visited=sorted(set(visited)),instructionCount=len(visited),providerReplacements=[])
