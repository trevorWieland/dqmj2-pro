import hashlib
import json
import random
import re
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

ADDRESS = 0x02011194
BACKEND = 0x020E5500
RUNTIME = 0x020E5B20
FIFO = 0x020E5D60
PAGE = 0x020E5000
STACK = 0x02500000
STOP = 0x027FF800
GETTER = 0x02011204
SETUP = 0x020113E8
CALLBACK = 0x02010EB8
FIFO_CALLBACK = 0x02011414
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]
PROVIDERS = {0x020100E4: 'common', 0x0200A2C4: 'fifo-wait', 0x0200A3D0: 'fifo-register'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dependencies(root, arm):
    wanted = {0x02011204, 0x020113E8}
    rows = []
    config = (root / 'config/arm9/symbols.txt').read_text()
    for relative in ['evidence/matches/main-runtime08.json', 'evidence/matches/main-runtime09.json']:
        report = json.loads((root / relative).read_text())
        for entry in report['matches']:
            address = int(entry['address'], 0)
            if address not in wanted:
                continue
            row = {**report, **entry}
            for field in ['source', 'object']:
                if sha((root / row[field]).read_bytes()) != row[field + 'Sha256']:
                    raise AssertionError('Existing backend dependency identity changed')
            bindings = {}
            for relocation in row['relocations']:
                target = int(relocation['target'], 0)
                match = re.search(r'kind:function\((arm|thumb),size=0x[0-9a-f]+\) addr:0x' + f'{target & ~1:08x}' + '$', config, re.M)
                mode = match[1] if match else 'data'
                bindings[relocation['symbol']] = {'address': hex(target), 'mode': mode, 'module': 'main', 'processor': 'arm9', 'kind': 'data' if mode == 'data' else 'function'}
            folder = root / 'work/mechanics-save/20261029-backend/dependencies' / f'{address:08x}-{row["objectSha256"][:12]}'
            proof = validate_link(row, bindings, folder)
            row.update(freeze_link(proof))
            code = (root / row['isolatedCallerBinary']).read_bytes()
            if code != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
                raise AssertionError('Existing linked backend dependency differs')
            rows.append((entry | {key: row[key] for key in ['isolatedCallerBinary', 'isolatedCallerBinarySha256', 'isolatedCallerLinkSnapshotManifest', 'isolatedCallerLinkSnapshotManifestSha256']}, code))
    if {int(row['address'], 0) for row, code in rows} != wanted:
        raise AssertionError('Both accepted callback-getter and FIFO-setup sources are required')
    return rows


def put(data, address, value):
    struct.pack_into('<I', data, address - PAGE, value & 0xFFFFFFFF)


def get(data, address):
    return struct.unpack_from('<I', data, address - PAGE)[0]


def provider_writes(name, seed, final_flag):
    if name == 'common':
        return [(BACKEND + 0x114, final_flag), (BACKEND + 0x24, seed ^ 0x11223344), (RUNTIME, seed ^ 0x56781234), (RUNTIME + 0x20, seed ^ 0x44556677)]
    if name == 'fifo-wait':
        return [(FIFO + 4, seed ^ 0x99AABBCC)]
    return [(FIFO, seed ^ 0x67544321)]


def model(before, seed, final_flag):
    expected = bytearray(before)
    if get(expected, BACKEND + 0x114):
        return bytes(expected), []
    put(expected, BACKEND + 0x114, 1)
    for offset in [0x24, 0x20, 0x1C, 0x38, 0x3C]:
        put(expected, BACKEND + offset, 0)
    put(expected, BACKEND + 0x28, 0xFFFFFFFF)
    put(expected, RUNTIME, 0)
    for address, value in provider_writes('common', seed, final_flag):
        put(expected, address, value)
    put(expected, RUNTIME + 0x20, CALLBACK)
    for name in ['fifo-wait', 'fifo-register']:
        for address, value in provider_writes(name, seed, final_flag):
            put(expected, address, value)
    put(expected, FIFO + 4, 0)
    return bytes(expected), ['common', 'getter', 'fifo-setup', 'fifo-wait', 'fifo-register']


def run(bodies, before, stack, seed, final_flag, regs, flags):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    for address, code in bodies.items():
        machine.mem_write(address, code)
    machine.mem_write(PAGE, before)
    machine.mem_write(STACK, stack)
    machine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(REGISTERS, regs):
        machine.reg_write(register, value)
    events, writes, visited = [], [], set()
    def observe(uc, pc, size, data):
        if pc not in PROVIDERS:
            if not any(address <= pc < address + len(code) for address, code in bodies.items()):
                raise AssertionError(('Backend initialization escaped declared bodies', hex(pc)))
            visited.add(pc)
            if pc == GETTER:
                events.append('getter')
                expected = (seed ^ 0x44556677) & 0xFFFFFFFF
                if struct.unpack('<I', bytes(uc.mem_read(RUNTIME + 0x20, 4)))[0] != expected:
                    raise AssertionError('Getter was called before common initialization completed')
            elif pc == SETUP:
                events.append('fifo-setup')
                if struct.unpack('<I', bytes(uc.mem_read(RUNTIME + 0x20, 4)))[0] != CALLBACK:
                    raise AssertionError('Callback was not installed before FIFO setup')
            return
        name = PROVIDERS[pc]
        events.append(name)
        if name == 'common':
            values = {offset: struct.unpack('<I', bytes(uc.mem_read(BACKEND + offset, 4)))[0] for offset in [0x1C, 0x20, 0x24, 0x28, 0x38, 0x3C, 0x114]}
            if values != {0x1C: 0, 0x20: 0, 0x24: 0, 0x28: 0xFFFFFFFF, 0x38: 0, 0x3C: 0, 0x114: 1} or bytes(uc.mem_read(RUNTIME, 4)) != bytes(4):
                raise AssertionError('Initialization stores did not precede common initialization')
        elif name == 'fifo-register':
            if [uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)] != [14, FIFO_CALLBACK]:
                raise AssertionError('FIFO registration arguments differ')
        for address, value in provider_writes(name, seed, final_flag):
            value &= 0xFFFFFFFF
            uc.mem_write(address, struct.pack('<I', value))
            writes.append([address, 4, value])
        result = (seed ^ pc ^ (len(events) * 0x13579B)) & 0xFFFFFFFF
        for number, register in enumerate([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]):
            uc.reg_write(register, (result ^ ((number + 1) * 0x1234567)) & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_CPSR, (seed & 15) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    machine.hook_add(UC_HOOK_CODE, observe)
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, data: writes.append([address, size, value]))
    machine.emu_start(ADDRESS, STOP, count=2000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise AssertionError('Backend initialization did not actually return within its bound')
    actual = [machine.reg_read(register) for register in REGISTERS]
    if actual[4:12] != regs[4:12] or actual[-2] != regs[-2]:
        raise AssertionError('Preserved register or stack restoration failed')
    arena = bytes(machine.mem_read(PAGE, len(before)))
    expected, plan = model(before, seed, final_flag)
    if arena != expected or events != plan:
        raise AssertionError(('Independent initialization RAM/call model differs', events, plan))
    return {'registers': actual, 'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'arena': arena, 'stack': bytes(machine.mem_read(STACK, len(stack))), 'events': events, 'writes': writes, 'visited': sorted(visited)}


def validate(arm, save, matches, root):
    if set(matches) != {'saved_20261029_backend_initialize'}:
        raise AssertionError('Backend initializer source is required')
    reused = dependencies(root, arm)
    rows = [*matches.values(), *reused]
    original = {int(row['address'], 0): arm[int(row['address'], 0) - 0x02000000:int(row['address'], 0) - 0x02000000 + row['bytes']] for row, code in rows}
    rebuilt = {int(row['address'], 0): code for row, code in rows}
    rng = random.Random(20261029011194)
    cases, coverage, hashes = 0, set(), []
    flags_values = [0, *range(1, 257), 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF]
    vectors = [(value, seed, 1) for seed in range(2) for value in flags_values]
    vectors += [(0, seed + 1000, value) for seed in range(64) for value in [0, 1, 0xFFFFFFFF]]
    def compare(before, stack, seed, final_flag):
        regs = [rng.getrandbits(32) for unused in REGISTERS]
        regs[-2:] = [STACK + len(stack) - 16, STOP]
        flags = rng.getrandbits(4) << 28 | 0x10
        native = run(original, before, stack, seed, final_flag, regs, flags)
        compiled = run(rebuilt, before, stack, seed, final_flag, regs, flags)
        if native != compiled:
            raise AssertionError('Native/source initialization machine effects differ')
        coverage.update(native['visited'])
        encoded = {**native, 'arena': sha(native['arena']), 'stack': sha(native['stack'])}
        hashes.append(sha(json.dumps(encoded, sort_keys=True).encode()))
        return native
    for value, seed, final_flag in vectors:
        before = bytearray(rng.randbytes(4096))
        put(before, BACKEND + 0x114, value)
        compare(bytes(before), rng.randbytes(0x8000), seed, final_flag)
        cases += 1
    for seed in range(32):
        before = bytearray(rng.randbytes(4096))
        put(before, BACKEND + 0x114, 0)
        stack = rng.randbytes(0x8000)
        for final_flag in [1, 1, 0, 0xFFFFFFFF]:
            result = compare(bytes(before), stack, seed + 2000, final_flag)
            before, stack = bytearray(result['arena']), result['stack']
            if final_flag == 1 and get(before, BACKEND + 0x114) != 0:
                put(before, BACKEND + 0x114, 0 if cases % 2 else 1)
            cases += 1
    main_pcs = sorted(pc for pc in coverage if ADDRESS <= pc < ADDRESS + 92)
    if len(main_pcs) != 23:
        raise AssertionError('Not all native initializer instruction addresses were visited')
    return {'cases': cases, 'nativeAndRecompiledCalls': cases * 2, 'verifiedReturn': True, 'instructionLimit': 2000, 'independentMachineStatePerExecution': True, 'stateSha256': hashes, 'nativeInstructionAddressesVisited': main_pcs, 'reusedAcceptedSources': [row for row, code in reused], 'sourceBodiesExecuted': len(rows), 'retainedNativeCalleeCodeBytes': 0, 'platformProviders': {hex(address): name for address, name in PROVIDERS.items()}, 'observations': ['A nonzero full32-bit flag returns without clearing RAM or calling initialization providers.', 'A zero flag is set to1 before six backend fields and the first runtime word are initialized and before common initialization is invoked.', 'The actual accepted getter installs function address02010EB8 before the actual accepted FIFO-setup caller registers02011414 on channel14 and clears its state word.', 'The declared void API makes no return-value promise; full architectural result registers are still compared.', 'Repeated calls and explicit flag reset/common-provider flag changes follow the current RAM flag rather than a hidden host cache.'], 'limitations': ['Common initialization, FIFO readiness and callback-registration implementations remain qualified synthetic boundaries.', 'These RAM/call observations do not establish physical FIFO timing, backup-device initialization, IRQ safety or concurrent reentrancy.']}
