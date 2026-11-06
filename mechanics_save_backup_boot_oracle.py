import hashlib
import json
import random
import re
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

CONTROL = 0x020edcf0
DEVICE = 0x020dd4b8
CONTROL_PAGE = 0x020ed000
DEVICE_PAGE = 0x020dd000
BASE = 0x02500000
STOP = 0x027ff800
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)
REGIONS = ((CONTROL_PAGE, 0x1000), (DEVICE_PAGE, 0x1000), (BASE, 0x8000))
PROVIDERS = {0x02010294: 'busy', 0x02011194: 'wait', 0x020060e4: 'allocate', 0x020102fc: 'lock', 0x0201030c: 'unlock'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dependencies(root, arm):
    wanted = {0x02027abc, 0x02027b00}
    result = []
    config = (root / 'config/arm9/symbols.txt').read_text()
    for path in ('evidence/matches/main-runtime03.json', 'evidence/matches/save-write-blocks.json'):
        report = json.loads((root / path).read_text(encoding='utf-8'))
        for entry in report['matches']:
            if int(entry['address'], 0) not in wanted:
                continue
            row = dict(entry)
            if 'source' not in row:
                row.update(source=report['source'], sourceSha256=report['sourceSha256'])
            if 'isolatedCallerBinary' not in row:
                bindings = {}
                for relocation in row['relocations']:
                    target = int(relocation['target'], 0) & ~1
                    match = re.search(r'kind:function\((arm|thumb),size=0x[0-9a-f]+\) addr:0x' + f'{target:08x}' + '$', config, re.M)
                    bindings[relocation['symbol']] = {'address': hex(target), 'mode': match[1] if match else 'data', 'module': 'main', 'processor': 'arm9', 'kind': 'function' if match else 'data'}
                row.update(freeze_link(validate_link(row, bindings)))
            for field in ('source', 'object'):
                if sha((root / row[field]).read_bytes()) != row[field + 'Sha256']:
                    raise AssertionError('Backup boot dependency source/object differs')
            binary = (root / row['isolatedCallerBinary']).read_bytes()
            address = int(row['address'], 0)
            if sha(binary) != row['isolatedCallerBinarySha256'] or binary != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
                raise AssertionError('Backup boot actual linked dependency differs')
            result.append((row, binary))
    if {int(row['address'], 0) for row, code in result} != wanted:
        raise AssertionError('Backup boot requires both previously accepted lock/unlock wrappers')
    return result


def validate(arm, save, matches, root):
    if set(matches) != {'saved_backup_boot'}:
        raise AssertionError('Backup boot source function is required')
    reused = dependencies(root, arm)
    source_rows = [*matches.values(), *reused]
    for row, code in source_rows:
        actual = (root / row['isolatedCallerBinary']).read_bytes()
        if sha(actual) != row['isolatedCallerBinarySha256'] or actual != code:
            raise AssertionError('Backup boot source MW snapshot differs')
    machines = []
    current_plan = [[], []]
    observed = [[], []]
    nonce = 0
    coverage = [set(), set()]
    for engine in range(2):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if engine:
            for row, code in source_rows:
                machine.mem_write(int(row['address'], 0), code)
        def intercept(uc, pc, size, user, engine=engine):
            if pc not in PROVIDERS:
                if not any(int(row['address'], 0) <= pc < int(row['address'], 0) + row['bytes'] for row, code in source_rows):
                    raise AssertionError(('Backup boot executed undeclared native code', hex(pc)))
                coverage[engine].add(pc)
                return
            name = PROVIDERS[pc]
            step = len(observed[engine])
            if step >= len(current_plan[engine]):
                raise AssertionError('Unexpected backup platform call')
            expected_name, result, argument, expected_locked = current_plan[engine][step]
            locked = bytes(uc.mem_read(CONTROL + 1, 1))[0]
            if name != expected_name or locked != expected_locked or argument is not None and uc.reg_read(UC_ARM_REG_R0) != argument:
                raise AssertionError(('Backup platform argument/RAM ordering differs', name, locked, argument))
            observed[engine].append(name)
            token = (nonce ^ (step << 16) ^ pc) & 0xffffffff
            uc.mem_write(BASE + 0x7000 + list(PROVIDERS).index(pc) * 4, struct.pack('<I', token))
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12), (result, token ^ 1, token ^ 2, token ^ 3, token ^ 12)):
                uc.reg_write(register, value)
            uc.reg_write(UC_ARM_REG_CPSR, (uc.reg_read(UC_ARM_REG_CPSR) & 0x0fffffff) | ((token & 15) << 28))
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        def writes(uc, access, address, size, value, user):
            if not any(start <= address and address + size <= start + extent for start, extent in (*REGIONS, (0x027f0000, 0x10000))):
                raise AssertionError(('Backup boot wrote outside complete observed arenas/stack', hex(address)))
        machine.hook_add(UC_HOOK_CODE, intercept)
        machine.hook_add(UC_HOOK_MEM_WRITE, writes)
        machines.append(machine)
    rng = random.Random(2026102796)
    cases = calls = protocols = 0
    def seed(memory):
        for machine in machines:
            for address, payload in memory.items():
                machine.mem_write(address, bytes(payload))
    def initial(flag, locked):
        memory = {address: bytearray(rng.randbytes(size)) for address, size in REGIONS}
        memory[CONTROL_PAGE][CONTROL - CONTROL_PAGE + 2] = flag
        memory[CONTROL_PAGE][CONTROL - CONTROL_PAGE + 1] = locked
        return memory
    def invoke(address, memory, busy=0, lock_id=64):
        nonlocal cases, calls, nonce
        nonce = rng.getrandbits(32)
        expected = {address: bytearray(payload) for address, payload in memory.items()}
        control = expected[CONTROL_PAGE]
        device = expected[DEVICE_PAGE]
        co, de = CONTROL - CONTROL_PAGE, DEVICE - DEVICE_PAGE
        plan = []
        def provider(name, result, argument=None):
            pc = next(pc for pc, value in PROVIDERS.items() if value == name)
            step = len(plan)
            plan.append((name, result & 0xffffffff, argument, control[co + 1]))
            token = (nonce ^ (step << 16) ^ pc) & 0xffffffff
            struct.pack_into('<I', expected[BASE], 0x7000 + list(PROVIDERS).index(pc) * 4, token)
        if address == 0x02027a14:
            result = 0
            if control[co + 2] == 0:
                provider('busy', busy)
                if busy:
                    provider('wait', nonce ^ 0xdeadbeef)
                control[co + 1] = 0
                provider('allocate', lock_id)
                struct.pack_into('<I', device, de + 4, lock_id & 0xffffffff)
                if lock_id & 0xffffffff == 0xfffffffd:
                    control[co] = 1
                else:
                    device[de] = 255
                    control[co + 4:co + 28] = bytes(24)
                    control[co + 2] = 1
                    control[co] = 0
                    result = 1
            else:
                control[co] = 12
        elif address == 0x02027abc:
            result = int(control[co + 1] == 0)
            if result:
                control[co + 1] = 1
                provider('lock', nonce, struct.unpack_from('<I', device, de + 4)[0] & 0xffff)
        elif address == 0x02027b00:
            result = int(control[co + 1] != 0)
            if result:
                provider('unlock', nonce, struct.unpack_from('<I', device, de + 4)[0] & 0xffff)
                control[co + 1] = 0
        else:
            raise AssertionError('Unknown backup protocol entry')
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        caller = [rng.getrandbits(32) for index in range(5)]
        outcomes = []
        for engine, machine in enumerate(machines):
            current_plan[engine] = plan
            observed[engine] = []
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12), caller):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
            began = time.monotonic()
            machine.emu_start(address, STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or machine.reg_read(UC_ARM_REG_R0) != result or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 32) != bool(cases & 1):
                raise AssertionError('Backup boot/protocol bounded ABI/result differs')
            if observed[engine] != [step[0] for step in plan] or any(bytes(machine.mem_read(address, len(payload))) != bytes(payload) for address, payload in expected.items()):
                raise AssertionError('Backup boot/protocol full RAM or boundary call sequence differs')
            outcomes.append(bytes(machine.mem_read(0x027f0000, 0x10000)))
            calls += 1
        if outcomes[0] != outcomes[1]:
            raise AssertionError('Backup boot complete source/native stack effects differ')
        cases += 1
        return expected, result
    for flag in range(256):
        for locked in (0, 255):
            memory = initial(flag, locked)
            seed(memory)
            invoke(0x02027a14, memory)
    for busy in (0, 1, 0x80000000, 0xffffffff):
        for lock_id in (0, 1, 63, 64, 127, 65535, 0x7fffffff, 0x80000000, 0xfffffffd, 0xffffffff):
            memory = initial(0, rng.randrange(256))
            seed(memory)
            invoke(0x02027a14, memory, busy, lock_id)
    for index in range(256):
        memory = initial(rng.choice((0, 1, 255)), rng.randrange(256))
        seed(memory)
        invoke(0x02027a14, memory, rng.getrandbits(32), rng.choice((0xfffffffd, rng.getrandbits(32))))
    for index in range(64):
        memory = initial(0, rng.randrange(256))
        seed(memory)
        lock_id = rng.randrange(65536)
        for address in (0x02027a14, 0x02027abc, 0x02027abc, 0x02027b00, 0x02027b00, 0x02027a14):
            memory, result = invoke(address, memory, index & 1, lock_id)
        protocols += 1
    if any(not all(pc in values for pc in range(0x02027a14, 0x02027ab4, 4)) for values in coverage):
        raise AssertionError('Backup boot native instruction coverage incomplete')
    return {'cases': cases, 'nativeAndRecompiledCalls': calls, 'connectedBootLockUnlockRepeatProtocols': protocols, 'instructionLimitPerCall': 1000000, 'secondsLimitPerCall': 2, 'everyInitializedByteValueCovered': 256, 'completeArenasStacksReturnsCalleeSavedAndArmThumbReturnModesVerified': True, 'allBootInstructionsReached': True, 'platformStubs': {name: {'address': hex(address), 'module': 'main', 'processor': 'arm9', 'scope': 'Controlled caller boundary with recorded arguments/RAM ordering, scratch effect and ABI caller-register/flag clobbers; native implementation receives no source credit'} for address, name in PROVIDERS.items()}, 'reusedAcceptedSources': [row for row, code in reused], 'observations': ['First initialization clears the locked flag before allocation and always stores the raw allocation result at device+4.', 'Allocation resultFFFFFFFD records status1 and leaves the type/geometry/initialized fields untouched; all other raw results store typeFF, clear six geometry words, set initialized1/status0 and return1.', 'Any nonzero signed initialized byte records status12 and returns0 without platform calls or other changes.', 'The accepted lock wrapper sets locked1 before its platform call, repeated locking returns0, and unlock clears the flag only after its platform call; raw lock identifiers are passed truncated to16 bits.'], 'limitations': ['Busy/wait/lock-allocation/lock/unlock implementations remain explicit caller boundary providers; no physical backup or OS initialization/locking behavior is inferred.', 'Synthetic full-width provider returns and all initialized byte patterns characterize target branches without claiming legal OS lock IDs or memory corruption safety.', 'No bank chronology, physical save atomicity, authentication or serialized-byte semantic promotion is claimed.']}
