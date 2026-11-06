import hashlib
import itertools
import json
import os
import random
import struct
import subprocess
import sys
from project import ROOT, configuration, now, sha256, write_json

sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC
import match_arm7 as matcher
from elf_units import split_symbol

TARGETS = {
    0x037FFB1C: (20, '4803b27210671118dd972ac414abef6ed1fd4f384f1cb7b267c5a446fd5b23d1'),
    0x037FC9A4: (36, '60057c6a1713e6ced5c7e604a0ff62729469ee25216d833fd1b81175ea5dd45e'),
    0x037FC9C8: (36, '11c1db00901a64b55cf56e506095c86e3d00425c6db56f41a5d410cbd35d60fa'),
    0x037FCBA4: (40, '6a52b6dbc301c20e11924b358b6c8a349aaf98ee73de4ec7462aaeec9b9e3349'),
    0x037FBDBC: (48, '5e6af6aaed56ee301912ecb87934f255e7d4f9b2a935851fb60656fdbdbe9fd4')
}
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_HASH = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
LINKER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_HASH = 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
WORK = ROOT / 'work/lowlevel-recovery/20261029-arm7-lists-proof'
ARENA = 0x03002000
STOP = 0x0301E000
QUEUE, NODE, NEXT, PREVIOUS, ANCHOR = [ARENA + n for n in [0x100, 0x400, 0x700, 0xA00, 0xD00]]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def word(data, address):
    return struct.unpack_from('<I', data, address - ARENA)[0]


def put(data, address, value, writes=None):
    struct.pack_into('<I', data, address - ARENA, value)
    if writes is not None:
        writes.append([address, 4, value])


def geometries(address):
    if address == 0x037FFB1C:
        return [(value,) for value in [0, QUEUE, NODE, ARENA + 0xFB0]]
    if address == 0x037FC9A4:
        return list(itertools.product([0, PREVIOUS, NODE, QUEUE], [NODE, QUEUE, PREVIOUS]))
    if address == 0x037FC9C8:
        return list(itertools.product([0, NEXT, NODE, QUEUE], [0, PREVIOUS, NODE, QUEUE]))
    if address == 0x037FCBA4:
        return list(itertools.product([0, NEXT, NODE], [0, ANCHOR, NODE, NODE + 4]))
    return [(0, 0)] + list(itertools.product([NODE, QUEUE], [0, NEXT, NODE, QUEUE]))


def fixture(address, geometry, seed):
    rng = random.Random(0x202610290027 + seed)
    before = bytearray(rng.randbytes(4096))
    arguments = [rng.getrandbits(32), rng.getrandbits(32)]
    if address == 0x037FFB1C:
        arguments[0] = geometry[0]
    elif address == 0x037FC9A4:
        tail, new_node = geometry
        arguments = [QUEUE, new_node]
        put(before, QUEUE + 0x70, tail)
    elif address == 0x037FC9C8:
        arguments = [QUEUE, NODE]
        put(before, NODE + 0x10, geometry[0])
        put(before, NODE + 0x14, geometry[1])
    elif address == 0x037FCBA4:
        arguments[1] = NODE
        put(before, NODE, geometry[0])
        put(before, NODE + 4, geometry[1])
    else:
        arguments[0] = QUEUE
        put(before, QUEUE, geometry[0])
        if geometry[0]:
            put(before, geometry[0] + 0x10, geometry[1])
    expected, writes = bytearray(before), []
    result = arguments[0]
    if address == 0x037FFB1C:
        if arguments[0]:
            put(expected, arguments[0] + 0x48, 0, writes)
            put(expected, arguments[0] + 0x4C, 0, writes)
    elif address == 0x037FC9A4:
        owner, node = arguments
        tail = word(expected, owner + 0x70)
        put(expected, owner + 0x6C if tail == 0 else tail + 0x10, node, writes)
        put(expected, node + 0x14, tail, writes)
        put(expected, node + 0x10, 0, writes)
        put(expected, owner + 0x70, node, writes)
    elif address == 0x037FC9C8:
        owner, node = arguments
        next_node, previous = word(expected, node + 0x10), word(expected, node + 0x14)
        put(expected, owner + 0x70 if next_node == 0 else next_node + 0x14, previous, writes)
        put(expected, owner + 0x6C if previous == 0 else previous + 0x10, next_node, writes)
    elif address == 0x037FCBA4:
        node = arguments[1]
        backlink = word(expected, node + 4)
        if backlink:
            put(expected, backlink, word(expected, node), writes)
        next_node = word(expected, node)
        if next_node == 0:
            result = word(expected, node + 4)
        else:
            put(expected, next_node + 4, word(expected, node + 4), writes)
    else:
        result = word(expected, arguments[0])
        if result:
            next_node = word(expected, result + 0x10)
            put(expected, arguments[0], next_node, writes)
            put(expected, next_node + 0x14 if next_node else arguments[0] + 4, 0, writes)
    return bytes(before), bytes(expected), writes, arguments, result


def execute(code, spec, data, seed, thumb):
    before, expected, writes, arguments, result = data
    rng = random.Random(0x202610290127 + seed)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(0x037F8000, 0x20000)
    uc.mem_map(0x03000000, 0x20000)
    uc.mem_write(spec['address'], code)
    uc.mem_write(ARENA, before)
    uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    initial = [rng.getrandbits(32) for unused in matcher.common.REGISTERS]
    initial[:2] = arguments
    initial[-2:] = [0x0301FF00, STOP | int(thumb)]
    for register, value in zip(matcher.common.REGISTERS, initial):
        uc.reg_write(register, value)
    observed, visited = [], set()
    uc.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: observed.append([address, size, value]))
    def observe(uc, address, size, user):
        if not spec['address'] <= address < spec['address'] + len(code):
            raise ValueError('Leaf pointer routine escaped its source-only body')
        visited.add(address)
    uc.hook_add(UC_HOOK_CODE, observe)
    uc.emu_start(spec['address'], STOP, count=128)
    registers = [uc.reg_read(register) for register in matcher.common.REGISTERS]
    if uc.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError('Bounded pointer routine failed to return')
    if registers[0] != result or registers[4:] != initial[4:]:
        raise ValueError('Independent return-register or preserved-register model differs')
    if uc.reg_read(UC_ARM_REG_CPSR) & 0x3F != 0x10 | (0x20 if thumb else 0):
        raise ValueError('Return mode or CPU mode differs')
    if bytes(uc.mem_read(ARENA, 4096)) != expected or observed != writes:
        raise ValueError('Independent complete-arena or ordered pointer-store model differs')
    return {
        'registers': registers,
        'cpsr': uc.reg_read(UC_ARM_REG_CPSR),
        'memorySha256': digest(bytes(uc.mem_read(ARENA, 4096))),
        'writes': observed,
        'visited': sorted(visited)
    }


def real_link(entry, native):
    directory = WORK / 'linked' / entry['name']
    directory.mkdir(parents=True, exist_ok=True)
    caller = directory / 'caller.o'
    with (ROOT / entry['object']).open('rb') as stream:
        split_symbol(ELFFile(stream), entry['name'], caller)
    lcf = directory / 'unit.lcf'
    lcf.write_text(
        'MEMORY {\nCALL: ORIGIN = ' + entry['address'] + ' > caller.bin\n}\n'
        'SECTIONS {\n.caller: { caller.o(.text) } > CALL\n}\n'
    )
    linked, raw = directory / 'linked.elf', directory / 'caller.bin'
    for output in [linked, raw]:
        output.unlink(missing_ok=True)
    command = [
        str(LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc',
        'arm7tdmi', '-main', entry['name'], str(lcf), str(caller), '-o', str(linked)
    ]
    process = subprocess.run(
        command, cwd=directory,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')),
        capture_output=True, text=True, timeout=30
    )
    if process.returncode or raw.read_bytes() != native:
        raise ValueError('ARM7 source-only MW caller link differs: ' + process.stdout + process.stderr)
    with linked.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == entry['name'])
        if symbol['st_value'] != int(entry['address'], 0) or symbol['st_size'] != entry['bytes']:
            raise ValueError('ARM7 linked symbol boundary differs')
    return {
        'exactCallerBytes': True,
        'sourceObjectSha256': entry['objectSha256'],
        'splitObjectSha256': sha256(caller),
        'linkedCallerSha256': sha256(raw),
        'linkedElf': linked.relative_to(ROOT).as_posix(),
        'linkedElfSha256': sha256(linked),
        'lcf': lcf.relative_to(ROOT).as_posix(),
        'lcfSha256': sha256(lcf),
        'linkerSha256': LINKER_HASH,
        'command': command,
        'exitCode': process.returncode,
        'stdout': process.stdout,
        'stderr': process.stderr,
        'relocations': [],
        'nativeCalleeBodiesUsed': 0,
        'wholeModuleLinked': False
    }


def main():
    if sha256(COMPILER) != COMPILER_HASH or sha256(LINKER) != LINKER_HASH:
        raise ValueError('Pinned compiler/linker differs')
    matcher.WORK = WORK / 'compile'
    specs = {spec['address']: spec for spec in matcher.candidates(10000)}
    matches = []
    for address, (size, source_hash) in TARGETS.items():
        spec = specs[address]
        if spec['bytes'] != size or spec['module'] != 'arm7-wram' or spec.get('mode', 'arm') != 'arm':
            raise ValueError('Canonical ARM7 function boundary differs')
        source = ROOT / f'src/arm7/20261029rotated27/native_arm7_wram_{address:08x}.c'
        if sha256(source) != source_hash:
            raise ValueError('Frozen pointer-routine C source differs')
        for output in (matcher.WORK / 'compile' / source.stem).glob('*.o'):
            output.unlink()
        entry, code = matcher.compare(source, spec, COMPILER, COMPILER_HASH, 2, 'off')
        if code is None or entry['relocations']:
            raise ValueError('Complete ordinary C body must match without external relocations')
        offset = address - spec['base']
        native = (ROOT / spec['binary']).read_bytes()[offset:offset + size]
        entry['isolatedRealMwCallerLink'] = real_link(entry, native)
        hashes, covered = [], set()
        for index, geometry in enumerate(geometries(address)):
            for seed in range(8):
                data = fixture(address, geometry, index * 8 + seed)
                for thumb in [False, True]:
                    first = execute(native, spec, data, index * 8 + seed, thumb)
                    second = execute(code, spec, data, index * 8 + seed, thumb)
                    if first != second:
                        raise ValueError('Fresh native/source pointer machines differ')
                    covered.update(first['visited'])
                    hashes.append(digest(json.dumps(first, sort_keys=True).encode()))
        if covered != set(range(address, address + size, 4)):
            raise ValueError('Pointer fixtures did not cover every native instruction')
        entry['oracle'] = {
            'cases': len(hashes),
            'nativeAndRecompiledCalls': len(hashes) * 2,
            'verifiedReturn': True,
            'returnModes': ['arm', 'thumb'],
            'instructionLimit': 128,
            'nativeInstructions': size // 4,
            'nativeInstructionCoverage': len(covered),
            'externalCalleesExecuted': 0,
            'independentModel': 'Sequential pointer-field reads/writes, aliases, complete RAM, ordered stores, R0, R4-R14, CPU/return modes',
            'stateSha256': hashes,
            'limitations': [
                'Valid aligned RAM graphs and supported null branches are exercised; arbitrary unmapped roots are unsupported C pointer inputs.',
                'R1-R3 and NZCV are compared between native and source machines without assigning independent API meanings.',
                'List/queue names describe the measured pointer operations; native SDK API types and broader ownership invariants remain inferred.'
            ]
        }
        entry['ordinaryCBytes'], entry['justifiedAssemblyBytes'] = size, 0
        matches.append(entry)
    report = {
        'schemaVersion': 1,
        'createdUtc': now(),
        'romSha256': configuration()['romSha256'],
        'processor': 'arm7',
        'runtimeMappingCanonical': True,
        'matches': matches,
        'nativeSymbols': {},
        'wholeModuleLinked': False,
        'sourceReconstructionComplete': False
    }
    write_json(ROOT / 'evidence/matches/arm7-20261029rotated27.json', report)
    print({
        'functions': len(matches),
        'bytes': sum(entry['bytes'] for entry in matches),
        'nativeAndRecompiledCalls': sum(entry['oracle']['nativeAndRecompiledCalls'] for entry in matches)
    })


if __name__ == '__main__':
    main()
