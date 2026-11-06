import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov000_criteria52_models_20261031 import RECORDS, HEADERS, GROUPS, MODE, GATES, SEEN, inputs, model
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x022189E4, 0x08000000, 0x0301FF00
NATIVE = {0x0205BF3C: 16, 0x0205FB90: 36, 0x0205FBB4: 92, 0x02063B40: 32, 0x02063E38: 12, 0x02215048: 28, 0x021DF3BC: 20}


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(start, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    for data, offset, expected in [(main, 0x5BF48, MODE), (main, 0x63B5C, GATES), (main, 0x63E40, SEEN),
        (overlay, 0x02215060 - 0x021D7240, RECORDS), (overlay, 0x021DF3CC - 0x021D7240, HEADERS)]:
        if struct.unpack_from('<I', data, offset)[0] != expected:
            raise ValueError('Criteria52 qualified native data literal differs')
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    group_table = bytes(machine.mem_read(GROUPS, 32))
    records, gates, seen = inputs(recipe, group_table)
    machine.mem_write(RECORDS, records)
    machine.mem_write(GATES, gates)
    machine.mem_write(SEEN, seen)
    machine.mem_write(MODE, bytes([recipe['mode']]))
    header = HEADERS + 14 * recipe['second']
    machine.mem_write(header, struct.pack('<H', recipe['category'] << 11 | rng.getrandbits(11)))
    expected_seen, changed = model(recipe, records, gates, seen, group_table)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[SEEN - 0x02000000:SEEN - 0x02000000 + 96] = expected_seen
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:2] = [recipe['first'], recipe['second']]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    visits, pending, counts, changes, gate_inputs, seen_inputs = set(), [], {}, [], [], []
    instructions, writes = 0, 0
    pc_trace, write_trace, return_trace = hashlib.sha256(), hashlib.sha256(), hashlib.sha256()

    def step(engine, pc, size, unused):
        nonlocal instructions
        while pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['sp'] or [engine.reg_read(REGS[i]) for i in range(4, 12)] != item['preserved']:
                raise ValueError('Criteria52 actual dependency stack/preserved registers differ')
            counts[hex(item['address'])] = counts.get(hex(item['address']), 0) + 1
            return_trace.update(struct.pack('<II', item['address'], engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        instructions += 1
        if instructions > 100000 or engine.reg_read(UC_ARM_REG_CPSR) & 32:
            raise ValueError('Criteria52 instruction/mode bound differs')
        pc_trace.update(struct.pack('<I', pc))
        if ENTRY <= pc < ENTRY + 360:
            visits.update(range(pc, pc + 4))
            return
        if pc in NATIVE:
            index = engine.reg_read(REGS[0])
            if pc == 0x02063B40:
                if index >= 64:
                    raise ValueError('Criteria52 unsupported full-word bit index')
                gate_inputs.append(index)
            if pc == 0x0205FBB4:
                if index >= 768 or engine.reg_read(REGS[1]) not in (0, 1):
                    raise ValueError('Criteria52 malformed native bit-store call')
                changes.append((index, engine.reg_read(REGS[1])))
            if pc == 0x02215048:
                if index != len(seen_inputs):
                    raise ValueError('Criteria52 actual768-slot scan order differs')
                seen_inputs.append(index)
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(REGS[i]) for i in range(4, 12)]))
            return
        if not any(start < pc < start + size for start, size in NATIVE.items()):
            raise ValueError(('Criteria52 escaped qualified actual native bodies', hex(pc)))

    def written(engine, access, address, size, value, unused):
        nonlocal writes
        if not (0x03000000 <= address <= SP - size or SEEN <= address <= SEEN + 96 - size and size == 4):
            raise ValueError(('Criteria52 unexpected native write', hex(address), size))
        writes += 1
        write_trace.update(struct.pack('<IIQ', address, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=100001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending:
        raise ValueError('Criteria52 top-level actual return/stack/completion differs')
    if actual[4:12] != registers[4:12] or actual[0] != bool(changed):
        raise ValueError('Criteria52 return/preserved-register model differs')
    if changes != [(index, 1) for index in changed] or len(seen_inputs) != (768 if recipe['mode'] in (1, 2, 5) else 0):
        raise ValueError('Criteria52 independent selected-record/call-order model differs')
    if bytes(machine.mem_read(0x02000000, 0x400000)) != bytes(expected_ram):
        raise ValueError('Criteria52 complete independent RAM model differs')
    return dict(actualReturn=True, returnWord=actual[0], instructions=instructions, writes=writes, registers=actual,
        cpsr=machine.reg_read(UC_ARM_REG_CPSR), nativeDependencyActualReturns=sum(counts.values()), nativeReturnsByAddress=counts,
        returnTraceSha256=return_trace.hexdigest(), providedCalls=0, observedNativeCallerInstructionBytes=len(visits), observedNativeCallerInstructionRanges=sorted(visits),
        changedRecords=changed, rawGateInputs=gate_inputs, scannedSlots=len(seen_inputs), pcTraceSha256=pc_trace.hexdigest(),
        writeTraceSha256=write_trace.hexdigest(), ramSha256=hashlib.sha256(expected_ram).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
