import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR

DATA, STACK, STOP, ENTRY = 0x02380000, 0x03030000, 0x0F000000, 0x0202AE9C
HELPERS = {0x0202AD78: 44, 0x0202ADA4: 40, 0x0202ADCC: 48,
           0x0202ADFC: 44, 0x02008C14: 20, 0x0202B9CC: 16}


def execute(original, code, index, budget=20000):
    rng = random.Random(ENTRY * 10000 + index)
    page = bytearray(rng.randbytes(4096))
    heap, block = DATA + 0x40, DATA + 0x300 + index % 8 * 16
    capacity = 256 + index % 5 * 64
    gap = [0, 4, 16, 20, 28, 60, 124][index % 7]
    requested = [0, 4, 20, 64, 128][index // 7 % 5]
    start, end = block + 16 + gap, block + 16 + capacity
    used_end, header = start + requested, start - 16
    flags, group, direction = index // 35 % 4, rng.randrange(65536), rng.randrange(65536)
    old_used = DATA + 0xC00 if index & 1 else 0
    struct.pack_into('<IIIIIH', page, heap - DATA - 4, flags, block, block, old_used, old_used, group)
    struct.pack_into('<HHIII', page, block - DATA, 0x4652, 0, capacity, 0, 0)
    if old_used:
        struct.pack_into('<HHIII', page, old_used - DATA, 0x5544, 0, 64, 0, 0)
    expected = bytearray(page)
    free = []
    fill_start = header if gap >= 20 else block
    if gap >= 20:
        free.append((block, header - block - 16))
    if end - used_end >= 20:
        free.append((used_end, end - used_end - 16))
    else:
        used_end = end
    pattern = rng.getrandbits(32)
    if flags & 3:
        word = struct.pack('<I', 0 if flags & 1 else pattern)
        for offset in range(fill_start - DATA, used_end - DATA, 4):
            expected[offset:offset + 4] = word
    for position, (node, size) in enumerate(free):
        previous = free[position - 1][0] if position else 0
        following = free[position + 1][0] if position + 1 < len(free) else 0
        struct.pack_into('<HHIII', expected, node - DATA, 0x4652, 0, size, previous, following)
    struct.pack_into('<II', expected, heap - DATA, free[0][0] if free else 0, free[-1][0] if free else 0)
    attributes = (direction & 1) << 15 | (header - fill_start & 127) << 8 | group & 255
    struct.pack_into('<HHIII', expected, header - DATA, 0x5544, attributes, used_end - header - 16, old_used, 0)
    struct.pack_into('<II', expected, heap - DATA + 8, old_used or header, header)
    if old_used:
        struct.pack_into('<I', expected, old_used - DATA + 12, header)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(ENTRY, code)
    table = struct.unpack_from('<I', original, 0x2B9D8)[0]
    uc.mem_write(table + 4, struct.pack('<I', pattern))
    uc.mem_write(DATA, bytes(page))
    uc.mem_map(STACK, 4096)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    uc.mem_write(STACK + 0x800, struct.pack('<I', direction))
    uc.mem_map(STOP, 4096)
    control = 0x10 | (index % 4 << 6)
    uc.reg_write(UC_ARM_REG_CPSR, index % 16 << 28 | control)
    initial = [rng.getrandbits(32) for unused in REGISTERS]
    initial[:4], initial[-2:] = [heap, block, start, requested], [STACK + 0x800, STOP | (index & 1)]
    for register, value in zip(REGISTERS, initial):
        uc.reg_write(register, value)
    stopped, active, returns, writes, reads, visited, helper_entries = False, [], [], [], [], [], []

    def instruction(engine, address, width, user):
        nonlocal stopped
        visited.append(address)
        while active and active[-1][1] == address:
            returns.append(active.pop()[0])
        if address == STOP:
            stopped = True
            engine.emu_stop()
            return
        if address in HELPERS:
            arity={0x0202AD78:2,0x0202ADA4:2,0x0202ADCC:3,0x0202ADFC:2,0x02008C14:3,0x0202B9CC:1}[address]
            helper_entries.append(dict(address=hex(address),arguments=[engine.reg_read(register)for register in REGISTERS[:arity]],lr=hex(engine.reg_read(REGISTERS[-1]))))
            active.append((address, engine.reg_read(REGISTERS[-1]) & ~1))
        assert ENTRY <= address < ENTRY + len(code) or any(a <= address < a + size for a, size in HELPERS.items()), hex(address)

    def memory(engine, access, address, width, value, user):
        writes.append([address,width,value&((1<<(8*width))-1)])
        assert DATA <= address and address + width <= DATA + 4096 or STACK + 0x700 <= address and address + width <= STACK + 0x800

    uc.hook_add(UC_HOOK_MEM_READ,lambda engine,access,address,width,value,user:reads.append([address,width]))
    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(ENTRY, STOP + 4, count=budget)
    assert stopped and not active and uc.reg_read(REGISTERS[-2]) == STACK + 0x800
    assert all(uc.reg_read(REGISTERS[i]) == initial[i] for i in range(4, 12))
    assert uc.reg_read(UC_ARM_REG_CPSR) & 0xDF == control
    assert bytes(uc.mem_read(STACK, 0x700)) == bytes([0xA5]) * 0x700
    assert bytes(uc.mem_read(STACK + 0x800, 4)) == struct.pack('<I', direction)
    assert bytes(uc.mem_read(STACK + 0x804, 0x7FC)) == bytes([0xA5]) * 0x7FC
    actual = bytes(uc.mem_read(DATA, 4096))
    result = uc.reg_read(REGISTERS[0])
    return dict(modelPassed=actual == bytes(expected) and result == start,
        actualReturns=1, actualHelperReturns=len(returns), helperReturns=[hex(a) for a in returns],
        result=result, backingSha256=hashlib.sha256(actual).hexdigest(), expectedBackingSha256=hashlib.sha256(expected).hexdigest(),
        flags=flags, requestedBytes=requested, gap=gap, group=group, direction=direction,
        suppliedCalls=0, existingUsedNode=bool(old_used),rawRegisters=[uc.reg_read(register)for register in REGISTERS],
        cpsr=uc.reg_read(UC_ARM_REG_CPSR),orderedWrites=writes,orderedReads=reads,helperEntries=helper_entries,visited=sorted(set(visited)),
        fullMappedMemorySha256={hex(base):hashlib.sha256(bytes(uc.mem_read(base,size))).hexdigest()for base,size in[(0x02000000,0x400000),(STACK,4096),(STOP,4096)]})



def oracle(code,root,work):
    import gzip
    import json
    original=(root/'extract/arm9/arm9.bin').read_bytes()
    if hashlib.sha256(original).hexdigest()!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':
        raise ValueError('Measured original heap main image differs')
    native=original[ENTRY-0x02000000:ENTRY-0x02000000+424]
    if code!=native:raise ValueError('Complete freshly linked heap C differs from measured native bytes')
    records=[];visited=set();helpers={}
    for index in range(560):
        first,second=execute(original,native,index),execute(original,code,index)
        if first!=second or not first['modelPassed']or first['suppliedCalls']:
            raise ValueError('Original/compiled full CPU/memory/effect/independent heap model differs')
        records.append(first);visited.update(pc for pc in first['visited']if ENTRY<=pc<ENTRY+416)
        for name in first['helperReturns']:helpers[name]=helpers.get(name,0)+2
    missing=sorted(set(range(ENTRY,ENTRY+416,4))-visited)
    if missing:raise ValueError('Supported heap corpus did not visit every caller instruction')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=work/'supported-native-records.json.gz'
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(vectors=560,actualOriginalAndCompiledReturns=1120,actualOriginalHelperReturnsSeparate=helpers,
        actualOriginalHelperReturnTotalSeparate=sum(helpers.values()),allRawRegistersFlagsStackAndMappedMemoryCompared=True,
        allOrderedDataReadsAndWritesAndNativeHelperArgumentsCompared=True,independentHeapModel=True,
        providerReplacements=[],instructionCoverage=dict(visited=sorted(visited),unvisited=missing,codeBytes=416,literalBytes=8),
        originalHelpersAdditionalSourceCredit=0,trace=dict(path=path.relative_to(root).as_posix(),
            rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=hashlib.sha256(path.read_bytes()).hexdigest(),gzipMtime=0),
        maxInstructionsPerExecution=20000,externalReplayDeadlineSeconds=300,
        limitations=['One selected free block and zero/one pre-existing used node in a disposable synthetic heap page',
            'Requests0/4/20/64/128 and measured gaps0/4/16/20/28/60/124, all four low flag modes and deterministic fullu16 group/direction inputs',
            'All six original lower routines execute; no substituted outcomes, malformed/cyclic/concurrent heap or scene-reachability claim',
            'Original32-bit pointer/address/layout ABI only; this does not establish native64-bit/Android portability'])


def wrong_body(code,root,work,label):
    import gzip
    import json
    original=(root/'extract/arm9/arm9.bin').read_bytes();records=[];failed=[];helpers=0
    for index in range(560):
        result=execute(original,code,index);records.append(result);helpers+=result['actualHelperReturns']
        if not result['modelPassed']:failed.append(index)
    if not failed:raise ValueError('Wrong heap C escaped independent native model: '+label)
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=work/(label+'-native-records.json.gz')
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(label=label,actualWrongSourceReturns=560,actualOriginalHelperReturnsSeparate=helpers,
        independentModelRejections=len(failed),rejectedIndexes=failed,providerReplacements=[],sourceCredit=0,
        trace=dict(path=path.relative_to(root).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),
            compressedSha256=hashlib.sha256(path.read_bytes()).hexdigest(),gzipMtime=0))
