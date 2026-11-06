import hashlib
import random
import struct
from itertools import product

from project import ROOT
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, HELPER = 0x021D8900, 0x021D7480
GLOBAL, HEAP, INPUT, VTABLE = 0x021E78CC, 0x02300000, 0x02320000, 0x02330000
WIDGET, OUTER, INNER, STOP, SP = HEAP + 0x5760, 0x07000000, 0x07001000, 0x08000000, 0x0301FF00
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
        UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
        UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def recipes():
    rows = []
    patterns = ('zero', 'missing', 'first', 'last', 'generic', 'any-high', 'no-generic', 'exact-high', 'literal-generic')
    for index, (pattern, inner, outer, outer_thumb, inner_thumb) in enumerate(product(patterns,
            (0, 1, 0x80000000, 0xFFFFFFFF), (0, 1, 0xFFFFFFFF), (False, True), (False, True))):
        rows.append(dict(pattern=pattern, innerResult=inner, outerResult=outer,
                         outerThumb=outer_thumb, innerThumb=inner_thumb, seed=0x500600 + index))
    return rows


def selection(recipe):
    ids = [0x100 + index for index in range(16)]
    name = recipe['pattern']
    query = {'zero': 0, 'missing': 0x777, 'first': 0x100, 'last': 0x10F, 'generic': 0x80000005,
             'any-high': 0x80400120, 'no-generic': 0x80000005, 'exact-high': 0x80000005,
             'literal-generic': 0x80000000}[name]
    if name == 'generic':
        ids[0] = 0x80000000
    if name == 'any-high':
        ids[0], ids[7] = 0x80000000, 0x80000008
    if name == 'exact-high':
        ids[15] = query
    if name == 'literal-generic':
        ids[4] = query
    chosen, selected_key = None, query
    if query:
        for index, value in enumerate(ids):
            if value == query:
                chosen = index
                break
            if query & 0x80000000 and value & 0x80000000:
                if query == 0x80400120 and value != 0x80000000:
                    chosen, selected_key = index, value
                    break
                if query != 0x80400120 and value == 0x80000000:
                    chosen = index
                    break
    return query, ids, chosen, selected_key


def execute(main, overlay, recipe, source_bytes=None):
    rng = random.Random(recipe['seed'])
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (OUTER, 0x2000), (STOP, 0x1000)]:
        machine.mem_map(start, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(HEAP, rng.randbytes(0x6000))
    machine.mem_write(INPUT, rng.randbytes(0x100))
    machine.mem_write(GLOBAL, struct.pack('<II', HEAP, rng.getrandbits(32)))
    machine.mem_write(HEAP + 4, struct.pack('<I', OUTER | recipe['outerThumb']))
    query, ids, chosen, selected_key = selection(recipe)
    machine.mem_write(INPUT + 0x44, struct.pack('<I', query))
    for index, value in enumerate(ids):
        node = WIDGET + 0x24 + index * 0x30
        machine.mem_write(node + 4, struct.pack('<I', value))
        machine.mem_write(node + 0xC, struct.pack('<I', VTABLE))
    machine.mem_write(VTABLE + 8, struct.pack('<I', INNER | recipe['innerThumb']))
    original_selected = WIDGET + 0x24 + 9 * 0x30
    machine.mem_write(WIDGET + 0x20, struct.pack('<I', original_selected))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    helper_result = recipe['innerResult'] if chosen is not None else 0
    selected = original_selected
    if helper_result:
        selected = WIDGET + 0x24 + chosen * 0x30
        struct.pack_into('<I', expected_ram, WIDGET + 0x20 - 0x02000000, selected)
        struct.pack_into('<I', expected_ram, WIDGET + 0x324 - 0x02000000, selected_key)
    if recipe['outerResult']:
        selected_id = ids[(selected - WIDGET - 0x24) // 0x30]
        struct.pack_into('<I', expected_ram, HEAP + 0xE8 - 0x02000000, selected_id)
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[0], registers[1] = 6, INPUT
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    visits, writes, providers, pending, native_returns = [], [], [], [], []
    source_length = len(source_bytes) if source_bytes is not None else 1500

    def step(engine, pc, size, data):
        if pending and pc == pending[-1]['returnPc']:
            event = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != event['sp'] or engine.reg_read(UC_ARM_REG_R0) != helper_result:
                raise ValueError('Actual native search helper return/stack differs')
            native_returns.append(dict(module='ov005', address=hex(HELPER), actualReturn=True, returnWord=helper_result))
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 10000:
            raise ValueError('Dispatcher mode6 instruction bound exceeded')
        visits.append(pc)
        if pc == HELPER:
            arguments = [engine.reg_read(REGS[0]), engine.reg_read(REGS[1])]
            if arguments != [WIDGET, INPUT]:
                raise ValueError(('Native dispatcher helper input differs', arguments, [WIDGET, INPUT]))
            pending.append(dict(returnPc=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP)))
            return
        if ENTRY <= pc < ENTRY + source_length or HELPER <= pc < HELPER + 196:
            if engine.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('Original/source dispatcher or helper mode differs')
            return
        if pc not in (OUTER, INNER):
            raise ValueError(('Dispatcher escaped qualified code/provider ranges', hex(pc)))
        thumb = recipe['outerThumb'] if pc == OUTER else recipe['innerThumb']
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != thumb:
            raise ValueError('Synthetic callback target mode differs')
        if pc == INNER:
            if chosen is None or providers or [engine.reg_read(REGS[0]), engine.reg_read(REGS[1])] != [WIDGET, INPUT]:
                raise ValueError('Native search callback order/input differs')
            result = recipe['innerResult']
            event = dict(classification='provided synthetic search callback', mode='thumb' if thumb else 'arm',
                         arguments=[WIDGET, INPUT], returnWord=result)
        else:
            if len(providers) != (1 if chosen is not None else 0) or engine.reg_read(REGS[0]) != 6:
                raise ValueError('Dispatcher method6 callback order/code differs')
            pointer = engine.reg_read(REGS[1])
            words = list(struct.unpack('<II', bytes(engine.mem_read(pointer, 8))))
            if not 0x03000000 <= pointer <= SP - 8 or words != [helper_result, INPUT]:
                raise ValueError(('Dispatcher adjacent8-byte payload differs', hex(pointer), words, [helper_result, INPUT]))
            result = recipe['outerResult']
            engine.mem_write(pointer, struct.pack('<I', result))
            event = dict(classification='provided synthetic dispatcher callback', mode='thumb' if thumb else 'arm',
                         arguments=[6, 'stack-payload8'], inputWords=words, outputWord=result,
                         pointerEscapes=False, rawPayloadPointer=hex(pointer))
        providers.append(event)
        engine.reg_write(REGS[0], result)
        for index in [1, 2, 3, 12]:
            engine.reg_write(REGS[index], (recipe['seed'] * 0x9E3779B9 + len(providers) * 0x654321 + index) & 0xFFFFFFFF)
        flags = (engine.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF) | ((recipe['seed'] + len(providers)) & 15) << 28
        target = engine.reg_read(UC_ARM_REG_LR)
        engine.reg_write(UC_ARM_REG_CPSR, (flags & ~32) | (32 if target & 1 else 0))
        engine.reg_write(UC_ARM_REG_PC, target & ~1)

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda engine, access, a, size, value, data: writes.append((a, size, value)))
    machine.emu_start(ENTRY, STOP + 4, count=10001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending:
        raise ValueError('Dispatcher source/native failed actual return/stack/pending gate')
    if actual[0] != recipe['outerResult'] or actual[4:12] != registers[4:12]:
        raise ValueError('Dispatcher model return/preserved-register gate failed')
    if len(native_returns) != 1 or len(providers) != (2 if chosen is not None else 1):
        raise ValueError('Dispatcher native/provider protocol incomplete')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        difference = [(hex(0x02000000 + i), a, b) for i, (a, b) in enumerate(zip(ram, expected_ram)) if a != b][:12]
        raise ValueError(('Dispatcher independent complete-memory model differs', recipe, difference))
    allowed = [WIDGET + 0x20, WIDGET + 0x324, HEAP + 0xE8]
    for address, size, value in writes:
        if not (0x03000000 <= address < 0x03020000 or size == 4 and address in allowed):
            raise ValueError(('Dispatcher unexpected native/source write', hex(address), size))
    normalized = bytearray(ram)
    normalized[ENTRY - 0x02000000:ENTRY - 0x02000000 + 1500] = bytes(1500)
    return dict(actualReturn=True, returnWord=actual[0], imageClass='original-native' if source_bytes is None else 'compiled-draft',
        instructions=len(visits) - len(providers), providedEntryHooks=len(providers), nativeDependencyActualReturns=native_returns,
        providedCalls=providers, normalizedRamSha256=hashlib.sha256(normalized).hexdigest(), registers=actual,
        cpsr=machine.reg_read(UC_ARM_REG_CPSR), pcTrace=visits, pcTraceIncludesProvidedEntryHooks=True, writes=writes,
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
