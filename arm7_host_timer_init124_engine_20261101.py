import json
import random
from functools import lru_cache
import match_runtime
import arm7_runtime
from arm7_lane_thread_init_engine_20261031 import digest, word, store
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC
from project import ROOT

PROGRAM = ''
BASE, DATA, STACK, RETURN, IO = 0x037F8000, 0x023C0000, 0x023E0000, 0x023FF000, 0x04000000
WRAM_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
MAIN_SHA = 'ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'


@lru_cache(maxsize=1)
def measured_layout():
    layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
    return layout


def setup(bodies, seed):
    layout = measured_layout()
    modules = {row['id']: row for row in layout['modules'] if row.get('processor') == 'arm7'}
    wram = (ROOT / modules['arm7-wram']['binary']).read_bytes()
    main = (ROOT / modules['arm7-main']['binary']).read_bytes()
    if digest(wram) != WRAM_SHA or digest(main) != MAIN_SHA:
        raise ValueError('Qualified host IRQ utility input modules differ')
    if bodies:
        expected={address:wram[address-BASE:address-BASE+size]for address,size in {0x037FD128:124,0x037FD1B4:104,0x037FB858:76}.items()}
        if bodies!=expected:
            raise ValueError('Only all three complete freshly linked native-equal initializer/callback/writer units may be installed')
    rng = random.Random(20261031 + seed)
    regions = {BASE: bytearray(wram + rng.randbytes(0x20000 - len(wram))),
        0x027E0000: bytearray(main + rng.randbytes(0x20000 - len(main))),
        DATA: bytearray(rng.randbytes(0x8000)), STACK: bytearray(rng.randbytes(0x4000)),
        RETURN: bytearray(0x1000), IO: bytearray(0x1000)}
    for name in ('arm7-wram', 'arm7-main'):
        row = modules[name]
        base, begin, end = int(row['base'], 0), int(row['bssStart'], 0), int(row['bssEnd'], 0)
        regions[base][begin - base:end - base] = bytes(end - begin)
    for address, body in bodies.items():
        if not BASE <= address < BASE + len(wram):
            raise ValueError('Host IRQ utility body outside qualified initialized WRAM')
        regions[BASE][address - BASE:address - BASE + len(body)] = body
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base, data in regions.items():
        cpu.mem_map(base, len(data))
        cpu.mem_write(base, bytes(data))
    inventory = json.loads((ROOT / 'evidence/arm7/ghidra-runtime-inventory.json').read_text())['functions']
    if digest(wram[0x51B4:0x521C])!='2b06d1da94b40e70c3afc49e55ad01c660c35994f4b96ac26c6ff1ad121fa0f8':
        raise ValueError('Full original host callback104 scope changed')
    if any(int(row['address'],0)==0x037FD1B4 for row in inventory):
        raise ValueError('Original host callback104 gap unexpectedly configured')
    inventory=inventory+[{'module':'arm7-wram','address':'0x37fd1b4','mode':'arm','ranges':[['0x37fd1b4','0x37fd20c']]}]
    entries = {int(row['address'], 0): row for row in inventory if row['module'] in modules}
    ranges = [(int(first, 0), int(last, 0), row['mode']) for row in inventory if row['module'] in modules for first, last in row['ranges']]
    reads, writes, visited, frames, nested, writer_entries = [], [], [], [], [], []

    def code(machine, pc, width, unused):
        mode = 'thumb' if machine.reg_read(UC_ARM_REG_CPSR) & 32 else 'arm'
        if not any(first <= pc and pc + width <= last and expected == mode for first, last, expected in ranges):
            raise ValueError('Host IRQ utility execution escaped known original instruction scope: ' + hex(pc))
        if pc==0x037FB858:
            writer_entries.append({'arguments':[machine.reg_read(register)for register in match_runtime.REGISTERS[:3]],
                'lr':machine.reg_read(match_runtime.REGISTERS[14]),'sp':machine.reg_read(match_runtime.REGISTERS[13])})
        if frames and pc == frames[-1][1]:
            frame = frames.pop()
            nested.append({'entry': hex(frame[0]), 'returnPc': hex(frame[1])})
        if pc in entries:
            lr = machine.reg_read(match_runtime.REGISTERS[14])
            if lr != RETURN:
                frames.append([pc, lr])
        visited.append(pc)

    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_READ, lambda machine, access, location, width, value, unused: reads.append([location, width]))
    cpu.hook_add(UC_HOOK_MEM_WRITE, lambda machine, access, location, width, value, unused: writes.append([location, width, value & ((1 << (8 * width)) - 1)]))

    def snapshot():
        return {base: bytearray(cpu.mem_read(base, len(data))) for base, data in regions.items() if base != STACK}

    def invoke(address, arguments, budget=100000):
        initial = [random.Random(seed * 97 + index).getrandbits(32) for index in range(15)]
        initial[:min(4, len(arguments))] = arguments[:4]
        initial[-2:] = [STACK + 0x3000, RETURN]
        if len(arguments) > 4:
            cpu.mem_write(STACK + 0x3000, b''.join(value.to_bytes(4, 'little') for value in arguments[4:]))
        guard = bytes(cpu.mem_read(STACK + 0x3000, 0x1000))
        cpu.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | (0x53 if seed & 1 else 0xD3))
        for register, value in zip(match_runtime.REGISTERS, initial):
            cpu.reg_write(register, value)
        reads.clear()
        writes.clear()
        visited.clear()
        frames.clear()
        nested.clear()
        writer_entries.clear()
        error = None
        try:
            cpu.emu_start(address, RETURN, count=budget, timeout=1000000)
        except (UcError, ValueError) as failure:
            error = str(failure)
        returned = cpu.reg_read(UC_ARM_REG_PC) == RETURN and error is None
        actual = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if returned and (actual[4:12] != initial[4:12] or actual[-2:] != initial[-2:] or frames
            or bytes(cpu.mem_read(STACK + 0x3000, 0x1000)) != guard):
            raise ValueError('Host IRQ utility callee-save/frame/guard contract differs')
        return {'actualReturn': returned, 'error': error, 'pc': hex(cpu.reg_read(UC_ARM_REG_PC)), 'registers': actual,
            'cpsr': cpu.reg_read(UC_ARM_REG_CPSR), 'reads': reads[:], 'writes': writes[:], 'visited': sorted(set(visited)),
            'nestedReturns': nested[:], 'timerWriterEntries':writer_entries[:], 'completeMemorySha256': {hex(base): digest(bytes(cpu.mem_read(base, len(data)))) for base, data in regions.items()},
            'postFaultOrBoundaryStateExcluded': not returned}

    return {'cpu': cpu, 'regions': regions, 'snapshot': snapshot, 'invoke': invoke, 'reads': reads, 'writes': writes, 'visited': visited}
