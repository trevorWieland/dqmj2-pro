import bisect
import hashlib
import json
import random
import re
import struct
import sys
import zipfile
from project import ROOT, configuration, now, sha256, write_json

sys.path.insert(0, str(ROOT / 'deps/native'))
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC
from link_runtime_unit import measured_module
from match_lowlevel import REGISTERS

MAIN_HASH = 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
PARENT, ALTERNATE, JOIN, PARENT_SIZE = 0x02025F1C, 0x02025F2C, 0x02025F3C, 448
HELPER, HELPER_SIZE, STACK, STOP = 0x02026144, 524, 0x0301F000, 0x0301E000
MASK64 = (1 << 64) - 1


def digest(data):
    return hashlib.sha256(data).hexdigest()


def signed64(value):
    value &= MASK64
    return value - (1 << 64) if value & (1 << 63) else value


def arithmetic(entry, numerator, denominator):
    if denominator == 0:
        return numerator, 'denominator-zero-passthrough'
    quotient = abs(numerator) // abs(denominator)
    if (numerator < 0) != (denominator < 0):
        quotient = -quotient
    if entry == PARENT:
        return numerator - quotient * denominator, 'signed-remainder'
    if numerator == -(1 << 31) and denominator == -1:
        return -(1 << 31), 'signed32-fast-path-overflow-sign-extension'
    if numerator == -(1 << 63) and denominator == -1:
        return -(1 << 63), 'signed64-overflow-wrap'
    return signed64(quotient), 'signed-quotient'


def execute(binary, entry, numerator, denominator, seed, thumb, masks):
    rng = random.Random(0x20261029025F2C + seed)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(0x02000000, 0x100000)
    uc.mem_write(0x02000000, binary)
    uc.mem_map(0x03000000, 0x20000)
    uc.mem_write(STACK, rng.randbytes(4096))
    uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | masks)
    initial = [rng.getrandbits(32) for unused in REGISTERS]
    initial[:4] = [numerator & 0xFFFFFFFF, (numerator >> 32) & 0xFFFFFFFF, denominator & 0xFFFFFFFF, (denominator >> 32) & 0xFFFFFFFF]
    initial[-2:] = [0x0301FF00, STOP | int(thumb)]
    for register, value in zip(REGISTERS, initial):
        uc.reg_write(register, value)
    visited, prefix, writes = set(), [], []
    joined, instructions = False, 0
    def record(uc, access, address, size, value, user):
        if not STACK <= address < initial[-2] or size != 4:
            raise ValueError('Arithmetic entry wrote outside its bounded stack frame')
        writes.append([address, size, value])
    def observe(uc, address, size, user):
        nonlocal joined, instructions
        instructions += 1
        if not (PARENT <= address < PARENT + PARENT_SIZE or HELPER <= address < HELPER + HELPER_SIZE):
            raise ValueError('Arithmetic entry escaped the measured parent/helper bodies')
        visited.add(address)
        if len(prefix) < 5:
            prefix.append(address)
        if address == JOIN and not joined:
            joined = True
            expected = (initial[1] | 1) if entry == PARENT else (initial[1] ^ initial[3]) & 0xFFFFFFFE
            if uc.reg_read(REGISTERS[4]) != expected or uc.reg_read(REGISTERS[-2]) != initial[-2] - 28:
                raise ValueError('Alternate prologue did not establish its own measured common-tail frame')
            saved = [initial[index] for index in [4, 5, 6, 7, 11, 12, 14]]
            if list(struct.unpack('<7I', bytes(uc.mem_read(initial[-2] - 28, 28)))) != saved:
                raise ValueError('Independent push-frame model differs')
    uc.hook_add(UC_HOOK_CODE, observe)
    uc.hook_add(UC_HOOK_MEM_WRITE, record)
    uc.emu_start(entry, STOP, count=20000)
    registers = [uc.reg_read(register) for register in REGISTERS]
    actual = signed64(registers[0] | (registers[1] << 32))
    expected, classification = arithmetic(entry, numerator, denominator)
    if not joined or prefix != [entry, entry + 4, entry + 8, entry + 12, JOIN]:
        raise ValueError('Entry did not independently reach the shared-tail join')
    if uc.reg_read(UC_ARM_REG_PC) != STOP or registers[4:] != initial[4:] or actual != expected:
        raise ValueError('Native arithmetic result, actual return or preserved-register model differs')
    if uc.reg_read(UC_ARM_REG_CPSR) & 0xFF != 0x10 | masks | (0x20 if thumb else 0):
        raise ValueError('Arithmetic entry changed control bits or returned in the wrong mode')
    state = {
        'registers': registers, 'cpsr': uc.reg_read(UC_ARM_REG_CPSR), 'writes': writes,
        'visited': sorted(visited), 'stackSha256': digest(bytes(uc.mem_read(STACK, 4096)))
    }
    return {
        'entry': hex(entry), 'numerator': str(numerator), 'denominator': str(denominator),
        'result': str(actual), 'classification': classification, 'returnMode': 'thumb' if thumb else 'arm',
        'interruptMasks': hex(masks), 'actualReturn': True, 'instructions': instructions,
        'usedNativeSigned32Helper': HELPER in visited, 'stateSha256': digest(json.dumps(state, sort_keys=True).encode()),
        'stackWriteBytesBelowEntrySp': initial[-2] - min(address for address, unused, value in writes)
    }


def external_references():
    modules = json.loads((ROOT / 'provenance/seed-manifest.json').read_text())['modules']
    result = []
    arm, thumb = Cs(CS_ARCH_ARM, CS_MODE_ARM), Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    arm.detail, thumb.detail, thumb.skipdata = True, True, True
    for descriptor in modules:
        name = descriptor['name']
        module, binary, symbols = measured_module(name)
        functions = sorted((int(address, 16), int(size, 16), mode, label) for label, mode, size, address in re.findall(r'^(\S+) kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:0x([0-9a-f]{8})$', symbols, re.M))
        starts = [function[0] for function in functions]
        base = int(module['base'], 0)
        def append(instruction, function):
            if not instruction.id or not instruction.mnemonic.startswith('b') or not instruction.operands or instruction.operands[0].type != 2:
                return
            target = instruction.operands[0].imm & 0xFFFFFFFF
            if target not in (PARENT, ALTERNATE) or (name == 'main' and PARENT <= instruction.address < PARENT + PARENT_SIZE):
                return
            result.append({
                'processor': 'arm9', 'sourceModule': name, 'sourceModuleSha256': module['sha256'],
                'sourceFunction': function[3], 'sourceFunctionAddress': hex(function[0]),
                'sourceMode': function[2], 'address': hex(instruction.address),
                'instructionBytes': instruction.bytes.hex(), 'mnemonic': instruction.mnemonic,
                'targetModule': 'main', 'targetAddress': hex(target), 'targetMode': 'arm',
                'evidenceClass': 'direct-native-branch-within-configured-function'
            })
        for offset in range(0, len(binary) - 3, 4):
            value = struct.unpack_from('<I', binary, offset)[0]
            if value & 0x0E000000 != 0x0A000000:
                continue
            immediate = (value & 0xFFFFFF) << 2
            if immediate & 0x02000000:
                immediate -= 0x04000000
            address = base + offset
            target = (address + 8 + immediate) & 0xFFFFFFFF
            if target not in (PARENT, ALTERNATE):
                continue
            index = bisect.bisect_right(starts, address) - 1
            if index < 0 or functions[index][2] != 'arm' or not address < functions[index][0] + functions[index][1]:
                continue
            instruction = next(arm.disasm(binary[offset:offset + 4], address), None)
            if instruction is not None:
                append(instruction, functions[index])
        for function in functions:
            if function[2] != 'thumb':
                continue
            offset = function[0] - base
            for instruction in thumb.disasm(binary[offset:offset + function[1]], function[0]):
                append(instruction, function)
    return sorted(result, key=lambda item: (item['sourceModule'], int(item['address'], 0)))


def local_reference_search():
    archive = ROOT / 'tools/mwccarm.zip'
    with zipfile.ZipFile(archive) as package:
        members = [name for name in package.namelist() if re.search(r'(?:runtime|div2|mod2|msl|source)', name, re.I)]
    patterns = re.compile(r'(?:Runtime_ARM|div2i|mod2i|libntr|NitroSDK|MSL_ARM|armrt)', re.I)
    paths = [path.relative_to(ROOT).as_posix() for directory in ['tools', 'deps'] for path in (ROOT / directory).rglob('*') if path.is_file() and patterns.search(path.name)]
    return {
        'searchedRoots': ['tools', 'deps'], 'compilerArchiveSha256': sha256(archive),
        'archiveNameMatches': members, 'filesystemNameMatches': paths,
        'originalArmAssemblyReferenceEstablished': False,
        'limitations': 'Repository-local name searches and archive member inspection found host MSL DLLs, not an authenticated ARM runtime assembly source. No assembly/source credit is granted.'
    }


def main():
    module, binary, symbols = measured_module('main')
    if module['sha256'] != MAIN_HASH:
        raise ValueError('Measured modified ARM9 main image differs')
    parent_line = next(line for line in symbols.splitlines() if line == 'func_02025f1c kind:function(arm,size=0x1c0) addr:0x02025f1c')
    alternate_line = next(line for line in symbols.splitlines() if re.search(r'addr:0x02025f2c$', line))
    helper_line = next(line for line in symbols.splitlines() if line == 'func_02026144 kind:function(arm,size=0x20c) addr:0x02026144')
    edges = [0, 1, -1, 2, -2, 3, -3, 7, -7, (1 << 15) - 1, -(1 << 15), (1 << 31) - 1, -(1 << 31), 1 << 31, -(1 << 31) - 1, (1 << 32) - 1, 1 << 32, -(1 << 32), (1 << 63) - 1, -(1 << 63), 1 << 62, -(1 << 62)]
    vectors = {(numerator, denominator) for numerator in edges for denominator in edges}
    rng = random.Random(20261029025)
    vectors.update((signed64(rng.getrandbits(64)), signed64(rng.getrandbits(64))) for unused in range(64))
    vectors.update((rng.randrange(-(1 << 31), 1 << 31), rng.randrange(-(1 << 31), 1 << 31)) for unused in range(64))
    results = []
    for index, (numerator, denominator) in enumerate(sorted(vectors)):
        for entry in [PARENT, ALTERNATE]:
            for thumb in [False, True]:
                for masks in [0, 0xC0]:
                    results.append(execute(binary, entry, numerator, denominator, index, thumb, masks))
    start = PARENT - int(module['base'], 0)
    prologues = {}
    for entry in [PARENT, ALTERNATE]:
        offset = entry - int(module['base'], 0)
        code = binary[offset:offset + 16]
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
        prologues[hex(entry)] = {'bytes': code.hex(), 'sha256': digest(code), 'instructions': [{'address': hex(item.address), 'mnemonic': item.mnemonic, 'operands': item.op_str} for item in decoder.disasm(code, entry)]}
    report = {
        'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
        'processor': 'arm9', 'module': 'main', 'mode': 'arm', 'moduleInputSha256': MAIN_HASH,
        'parent': {'address': hex(PARENT), 'bytes': PARENT_SIZE, 'configuredIdentity': parent_line, 'spanSha256': digest(binary[start:start + PARENT_SIZE])},
        'alternateEntry': {'address': hex(ALTERNATE), 'configuredIdentity': alternate_line, 'independentPrologue': True, 'sharedJoinAddress': hex(JOIN), 'sharedParentEnd': hex(PARENT + PARENT_SIZE), 'separateExecutableBytesCredited': 0},
        'entryPrologues': prologues, 'externalBranchReferences': external_references(),
        'abi': {'inputWords': ['R0 numerator low', 'R1 numerator high', 'R2 denominator low', 'R3 denominator high'], 'resultWords': ['R0 result low', 'R1 result high'], 'preserved': 'R4-R14 including SP and LR', 'clobberedOrUnspecified': ['R2', 'R3', 'NZCV'], 'entryRoles': {hex(PARENT): 'signed64 remainder', hex(ALTERNATE): 'signed64 quotient'}, 'denominatorZero': 'unchanged numerator returned at both entries', 'signed32FastPathOverflow': '(-2147483648)/(-1) produces -2147483648; remainder zero', 'signed64Overflow': '(-9223372036854775808)/(-1) wraps to -9223372036854775808; remainder zero'},
        'nativeHelper': {'address': hex(HELPER), 'bytes': HELPER_SIZE, 'configuredIdentity': helper_line, 'spanSha256': digest(binary[HELPER - int(module['base'], 0):HELPER - int(module['base'], 0) + HELPER_SIZE]), 'sourceCredit': 0},
        'fixtures': {'operandPairs': len(vectors), 'executions': len(results), 'actualReturns': len(results), 'freshMachinePerExecution': True, 'instructionLimit': 20000, 'maximumObservedInstructions': max(item['instructions'] for item in results), 'results': results},
        'localReferenceSearch': local_reference_search(), 'reproduction': 'python verify_main_20261029_div64_entry.py',
        'reconstructedCodeBytes': 0, 'justifiedAssemblyBytes': 0, 'ordinaryCBytes': 0,
        'limitations': ['Entry/ABI evidence does not recover original vendor symbol names or establish original assembly provenance.', 'Native parent/helper bytes are execution scaffolding, not decompiled source.', 'Configured function spans can contain literal pools; direct branch evidence retains source identities and raw instruction bytes for review.']
    }
    write_json(ROOT / 'evidence/entrypoints/main-20261029-div64-entry.json', report)
    print({'operandPairs': len(vectors), 'actualReturningExecutions': len(results), 'externalBranches': len(report['externalBranchReferences']), 'sourceCredit': 0})


if __name__ == '__main__':
    main()
