import hashlib
import json
from pathlib import Path
import random
import sys
import match_runtime
import arm7_lane_thread_init_engine_20261031 as engine
import link_arm7_bulk_20261030 as linker
import crossreuse_utility_c
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_CPU_ARM_TI925T
from project import write_json

ROOT = Path(__file__).resolve().parent
ADDRESS, SIZE, CODE, BASE = 0x037FD1B4, 104, 88, 0x037F8000
MODULE = ROOT / 'extract/arm7/runtime/arm7-wram.bin'
MODULE_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
IO, STATE, STACK, RETURN = 0x04000000, 0x03807898, engine.STACK, engine.RETURN
INVENTORY = ROOT / 'evidence/arm7/ghidra-runtime-inventory.json'
HELPERS = {0x037FB858: 64, 0x037FB8F0: 52, 0x037FB8D8: 20}
PINS = ROOT / 'nonmatching/arm7-bulk/20261031/lane-host-tick-callback104-boundary/generator-pins.json'
PIN_SHA = 'f0b21187482593f3cc7e50f30597e82ebfca0bc02474cf783318d5229ed2d123'
SOURCE = 'nonmatching/arm7-bulk/20261031/lane-host-tick-callback104-v2/native_arm7_wram_037fd1b4.c'
SOURCE_SHA = '7fa6d1fe4916ce0882d00cb5d6441bb43ae4d3ca4f52492b2bc68668fe6554d7'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_inputs():
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Pinned callback proof runtime differs')
    if digest(PINS.read_bytes()) != PIN_SHA:
        raise ValueError('Complete callback proof input closure differs')
    pins = json.loads(PINS.read_text())['files']
    for row in pins:
        if digest((ROOT / row['path']).read_bytes()) != row['sha256']:
            raise ValueError('Current callback characterization input changed: ' + row['path'])
    return pins


def boundary():
    raw = MODULE.read_bytes()
    if digest(raw) != MODULE_SHA:
        raise ValueError('Original callback module differs')
    native = raw[ADDRESS - BASE:ADDRESS - BASE + SIZE]
    inventory = json.loads(INVENTORY.read_text())
    if any(row['module'] == 'arm7-wram' and any(int(first, 0) < ADDRESS + SIZE and ADDRESS < int(last, 0)
        for first, last in row['ranges']) for row in inventory['functions']):
        raise ValueError('Proposed gap overlaps an existing configured code range')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = list(decoder.disasm(native[:CODE], ADDRESS))
    if len(instructions) != CODE // 4 or instructions[-1].mnemonic != 'bx' or instructions[-1].op_str != 'ip':
        raise ValueError('Callback full ARM code/tail differs')
    pools = {ADDRESS + CODE + offset: int.from_bytes(native[CODE + offset:CODE + offset + 4], 'little') for offset in range(0, 16, 4)}
    if list(pools.values()) != [STATE, 0x04000102, 0x037FB858, ADDRESS]:
        raise ValueError('Callback literal identities differ')
    modules, functions = linker.namespace('')
    references, words, interiors = [], [], []
    for row in inventory['functions']:
        if row['module'] not in modules or row.get('mode') not in ('arm', 'thumb'):
            continue
        module = modules[row['module']]
        image = (ROOT / module['binary']).read_bytes()
        base = int(module['base'], 0)
        decode = Cs(CS_ARCH_ARM, CS_MODE_THUMB if row['mode'] == 'thumb' else CS_MODE_ARM)
        decode.detail = True
        for first, last in row['ranges']:
            first, last = int(first, 0), int(last, 0)
            for instruction in decode.disasm(image[first - base:last - base], first):
                if (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) and instruction.operands and instruction.operands[0].type == 2:
                    target = instruction.operands[0].imm & ~1
                    if ADDRESS <= target < ADDRESS + SIZE:
                        references.append({'module': row['module'], 'root': row['address'], 'mode': row['mode'], 'pc': hex(instruction.address), 'target': hex(target)})
                        if target != ADDRESS:
                            interiors.append(references[-1])
    for name, module in modules.items():
        image, base = (ROOT / module['binary']).read_bytes(), int(module['base'], 0)
        for offset in range(0, len(image) - 3, 4):
            value = int.from_bytes(image[offset:offset + 4], 'little')
            if ADDRESS <= value & ~1 < ADDRESS + SIZE:
                words.append({'module': name, 'storage': hex(base + offset), 'value': hex(value), 'modeTag': 'thumb' if value & 1 else 'arm'})
                if value & ~1 != ADDRESS:
                    interiors.append(words[-1])
    if interiors or {(row['module'], row['storage'], row['value']) for row in words} != {('arm7-wram', '0x37fd1a0', hex(ADDRESS)), ('arm7-wram', '0x37fd218', hex(ADDRESS))}:
        raise ValueError('Unreconciled callback outside/interior references')
    return {'processor': 'arm7', 'program': '', 'module': 'arm7-wram', 'mode': 'arm', 'address': hex(ADDRESS), 'bytes': SIZE,
        'codeRange': [hex(ADDRESS), hex(ADDRESS + CODE)], 'literalRange': [hex(ADDRESS + CODE), hex(ADDRESS + SIZE)],
        'codeSha256': digest(native[:CODE]), 'fullSha256': digest(native), 'moduleSha256': MODULE_SHA,
        'inventorySha256': digest(INVENTORY.read_bytes()), 'canonicalEntryCurrentlyPresent': ADDRESS in functions,
        'literalWords': {hex(key): hex(value) for key, value in pools.items()}, 'directReferences': references,
        'alignedRootPointerWords': words, 'outsideInteriorReferences': interiors, 'tailDestination': hex(0x037FB858),
        'neighborBounds': {'previous': '037FD1A4:12 code+4 pool ends037FD1B4', 'following': '037FD21C:152 code+12 pool starts037FD21C'},
        'initializedDenominatorIncrement': 0, 'sourceCredit': 0, 'sharedConfigurationChanged': False}


def execute(case, seed, budget=10000):
    raw = MODULE.read_bytes()
    original = engine.setup(0x037FBF64, raw[0x3F64:0x4054], seed)
    original['cpu'].mem_write(0x03807678, bytes(0x0380B4E4 - 0x03807678))
    original['cpu'].mem_map(IO, 0x1000)
    original['cpu'].mem_write(IO, bytes(0x1000))
    original['regions'][IO] = bytes(0x1000)
    launch = original['invoke'](0x037FD128)
    if not launch['actualReturn'] or int.from_bytes(original['cpu'].mem_read(0x038076B0, 4), 'little') != ADDRESS:
        raise ValueError('Actual original initializer did not install this ARM callback')
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    images = {}
    for base, data in original['regions'].items():
        images[base] = bytearray(original['cpu'].mem_read(base, len(data)))
    images[BASE][STATE + 8 - BASE:STATE + 16 - BASE] = case['counter'].to_bytes(8, 'little')
    images[BASE][STATE + 4 - BASE:STATE + 8 - BASE] = case['reset'].to_bytes(4, 'little')
    images[IO][0x208:0x20A] = case['ime'].to_bytes(2, 'little')
    images[IO][0x210:0x214] = case['ie'].to_bytes(4, 'little')
    for base, data in images.items():
        cpu.mem_map(base, len(data))
        cpu.mem_write(base, bytes(data))
    initial = [random.Random(seed * 31 + index).getrandbits(32) for index in range(15)]
    initial[-2:] = [STACK + 0x3000, RETURN]
    cpu.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
    for register, value in zip(match_runtime.REGISTERS, initial):
        cpu.reg_write(register, value)
    visited, writes, reads, frames, returns, tail = [], [], [], [], [], []

    def code(machine, pc, width, unused):
        if frames and pc == frames[-1][1]:
            returns.append(frames.pop()[0])
        if pc in HELPERS:
            if pc == 0x037FB858:
                args = [machine.reg_read(register) for register in match_runtime.REGISTERS[:3]]
                if args != [0, ADDRESS, 0] or machine.reg_read(UC_ARM_REG_LR) != RETURN:
                    raise ValueError('Callback typed tail arguments or original LR differ')
                tail.append(args)
            else:
                frames.append([pc, machine.reg_read(UC_ARM_REG_LR)])
        if not (ADDRESS <= pc < ADDRESS + CODE or any(start <= pc < start + size for start, size in HELPERS.items())):
            raise ValueError('Callback entered unqualified code/pool/dispatcher')
        visited.append(pc)

    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_READ, lambda machine, access, location, width, value, unused: reads.append([location, width]))
    cpu.hook_add(UC_HOOK_MEM_WRITE, lambda machine, access, location, width, value, unused: writes.append([location, width, value & ((1 << (width * 8)) - 1)]))
    cpu.emu_start(ADDRESS, RETURN, count=budget, timeout=1000000)
    returned = cpu.reg_read(UC_ARM_REG_PC) == RETURN
    if not returned:
        return {'actualReturn': False, 'postBoundaryStateExcluded': True, 'pc': hex(cpu.reg_read(UC_ARM_REG_PC))}
    expected = {base: bytearray(data) for base, data in images.items() if base != STACK}
    stores = []

    def put(address, width, value):
        stores.append([address, width, value])
        for base, data in expected.items():
            if base <= address and address + width <= base + len(data):
                data[address - base:address - base + width] = value.to_bytes(width, 'little')
                return
        raise ValueError('Callback model escaped mapped backing')

    counter = (case['counter'] + 1) & 0xFFFFFFFFFFFFFFFF
    put(STATE + 8, 4, counter & 0xFFFFFFFF)
    put(STATE + 12, 4, counter >> 32)
    if case['reset']:
        put(IO + 0x102, 2, 0)
        put(IO + 0x100, 2, 0)
        put(IO + 0x102, 2, 0xC1)
        put(STATE + 4, 4, 0)
    put(0x038076B0, 4, ADDRESS)
    put(0x038076B8, 4, 0)
    put(IO + 0x208, 2, 0)
    put(IO + 0x210, 4, case['ie'] | 8)
    put(IO + 0x208, 2, case['ime'])
    put(0x038076B4, 4, 1)
    actual = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
    nonstack = [row for row in writes if not STACK <= row[0] < STACK + 0x4000]
    if any(bytes(cpu.mem_read(base, len(data))) != bytes(data) for base, data in expected.items()) or nonstack != stores or tail != [[0, ADDRESS, 0]] or frames:
        raise ValueError('Actual callback state/store/tail model differs')
    if actual[4:12] != initial[4:12] or actual[-2:] != initial[-2:] or actual[0] != 0x038076B4:
        raise ValueError('Actual original callback register/tail-return contract differs')
    return {'actualReturn': True, 'case': case, 'actualOriginalInitializerReturnSeparate': True, 'originalInitInstalledPointer': hex(ADDRESS),
        'registers': actual, 'cpsr': cpu.reg_read(UC_ARM_REG_CPSR), 'visited': sorted(set(visited)), 'orderedNonstackWrites': nonstack,
        'reads': reads, 'tailArguments': tail, 'actualNestedHelperReturns': [hex(value) for value in returns],
        'tailHelperReturnedThroughOriginalLr': True, 'memorySha256': {hex(base): digest(bytes(cpu.mem_read(base, len(data)))) for base, data in images.items()}}


def unaccepted_source():
    source = ROOT / SOURCE
    if digest(source.read_bytes()) != SOURCE_SHA:
        raise ValueError('Unaccepted ordinary C hypothesis changed')
    compiler = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
    if digest(compiler.read_bytes()) != '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880':
        raise ValueError('Pinned hypothesis compiler differs')
    directory = ROOT / 'work/arm7-bulk-20261030/lane-host-tick-callback104-boundary'
    flags = match_runtime.FLAGS[:]
    flags[0] = '-O2'
    flags[flags.index('-proc') + 1] = 'arm7tdmi'
    flags[flags.index('-inline') + 1] = 'all'
    flags += ['-lang', 'c99', '-opt', 'space']
    pin = {'source': SOURCE, 'sourceSha256': SOURCE_SHA, 'name': 'native_arm7_wram_037fd1b4'}
    directory.mkdir(parents=True, exist_ok=True)
    match_runtime.WORK = directory / 'isolated-runtime'
    attempt, result = crossreuse_utility_c.compile_origin(pin, compiler, flags, directory)
    if result is None:
        raise ValueError(attempt)
    derived, masks, body = result
    if len(body) != SIZE:
        raise ValueError('Full unaccepted C hypothesis size changed')
    original = MODULE.read_bytes()[ADDRESS - BASE:ADDRESS - BASE + SIZE]
    with (ROOT / derived['probeObject']).open('rb') as stream:
        elf = ELFFile(stream)
        own = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == pin['name'])
        index, offset = own['st_shndx'], own['st_value'] & ~1
    relocations = [dict(row, format='SHT_RELA', explicitAddend=row['addend'], originalEncodedWord=body[row['offset']:row['offset'] + 4].hex()) for row in derived['relocations']]
    entry = dict(pin, program='', processor='arm7', module='arm7-wram', mode='arm', address=hex(ADDRESS), bytes=SIZE,
        inputModuleSha256=MODULE_SHA, targetSha256=digest(original), compiler=compiler.relative_to(ROOT).as_posix(),
        compilerSha256=digest(compiler.read_bytes()), compilerFlags=flags, object=derived['probeObject'], objectSha256=derived['probeObjectSha256'],
        sectionIndex=index, sectionOffset=offset, relocations=relocations)
    try:
        linker.validate(entry, directory / 'unchanged-canonical-guard')
    except ValueError as error:
        if str(error) != 'Complete candidate span or canonical ARM7 entry differs':
            raise
        refusal = {'stage': 'unchanged base linker canonical-entry check', 'exception': 'ValueError', 'reason': str(error)}
    else:
        raise ValueError('Unknown canonical entry was unexpectedly accepted')
    covered = {offset + index for offset, unused in masks for index in range(4)}
    return dict(entry, compiledBytes=len(body), comparableNonrelocationBytes=len(body) - len(covered),
        equalNonrelocationBytes=sum(a == b for index, (a, b) in enumerate(zip(original, body)) if index not in covered),
        genuineLinkSucceeded=False, canonicalRefusal=refusal, sourceCredit=0, scaffoldingCredit=0)


def build_report():
    pins = verify_inputs()
    scope = boundary()
    cases = [{'counter': counter, 'reset': reset, 'ie': ie, 'ime': ime}
        for counter in (0, 0xFFFFFFFF, 0xFFFFFFFFFFFFFFFF) for reset in (0, 1, 0xFFFFFFFF)
        for ie in (0, 0xFFFFFFFF) for ime in (0, 1, 0xFFFF)]
    records = [execute(case, index) for index, case in enumerate(cases)]
    if any(not row['actualReturn'] for row in records):
        raise ValueError('Original full callback did not return')
    own = {pc for row in records for pc in row['visited'] if ADDRESS <= pc < ADDRESS + CODE}
    if own != set(range(ADDRESS, ADDRESS + CODE, 4)):
        raise ValueError('Full callback code was not visited')
    cap = execute(cases[0], 0, budget=1)
    if cap['actualReturn']:
        raise ValueError('Exhausted callback gained return credit')
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'pinnedInputs': pins, 'pinFile': PINS.relative_to(ROOT).as_posix(), 'pinSha256': PIN_SHA,
        'unacceptedC': unaccepted_source(),
        'scope': scope, 'records': records, 'actualCallbackReturns': len(records), 'separateActualInitializerReturns': len(records) + 1,
        'actualNestedHelperReturns': sum(len(row['actualNestedHelperReturns']) for row in records), 'actualTailReturnTransfers': len(records),
        'sourceCredit': 0, 'originalAssemblyProvenanceCredit': 0, 'denominatorIncrease': 0,
        'allOwnInstructionsVisited': True, 'boundedExhaustionControl': cap, 'instructionLimit': 10000, 'timeoutMicroseconds': 1000000,
        'providersReplaced': [], 'originalModuleSha256': MODULE_SHA, 'linkerUnknownEntryGuardsChanged': False,
        'limitations': ['Original initializer genuinely installs the pointer; callback is then explicitly invoked in an isolated fresh machine',
            'This is not asynchronous IRQ delivery, a real BIOS/device execution or proof of enclosing scheduler/scene reachability',
            'All88 code bytes and16 pool bytes were already initialized; no source or denominator bytes are added',
            'Direct/aligned pointer references and neighboring configured bounds are measured; opaque program-wide reference absence remains unproved']}
    return report


def main():
    report = build_report()
    path = ROOT / 'evidence/arm7/tick-callback104-boundary-20261031.json'
    write_json(path, report)
    print(json.dumps({'report': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'actualCallbackReturns': report['actualCallbackReturns'], 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
