import hashlib
import json
from pathlib import Path
import random
import re
import match_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_CPU_ARM_946
from project import write_json

ROOT = Path(__file__).resolve().parent
BASE, STACK, RETURN = 0x02000000, 0x02300000, 0x02500000
QUOTIENT, REMAINDER, JOIN, CORE, SCALAR = 0x020260DC, 0x020260E8, 0x020260F0, 0x02025FA0, 0x02026358
IMAGE = ROOT / 'extract/arm9/arm9.bin'
IMAGE_SHA = 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
ROM_SHA = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def functions():
    text = (ROOT / 'config/arm9/symbols.txt').read_text()
    return [{'name': name, 'mode': mode, 'address': int(address, 0), 'bytes': int(size, 0)}
        for name, mode, size, address in re.findall(r'^(\S+) kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)$', text, re.M)]


def execute(entry, numerator, denominator, seed):
    raw = IMAGE.read_bytes()
    if sha(raw) != IMAGE_SHA or entry not in (QUOTIENT, REMAINDER):
        raise ValueError('Qualified original ARM9 runtime input/entry changed')
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_946)
    cpu.mem_map(BASE, (len(raw) + 0xFFF) & ~0xFFF)
    cpu.mem_write(BASE, raw)
    cpu.mem_map(STACK, 0x4000)
    rng = random.Random(20261031 + seed)
    cpu.mem_write(STACK, rng.randbytes(0x4000))
    initial = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    initial[:4] = [numerator & 0xFFFFFFFF, numerator >> 32, denominator & 0xFFFFFFFF, denominator >> 32]
    initial[-2:] = [STACK + 0x3F00, RETURN]
    cpu.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
    for register, value in zip(match_runtime.REGISTERS, initial):
        cpu.reg_write(register, value)
    visited, writes, nested, frame = set(), [], [], []

    def code(machine, pc, size, unused):
        if frame and pc == 0x02026110:
            args = frame.pop()
            quotient = machine.reg_read(match_runtime.REGISTERS[0])
            remainder = machine.reg_read(match_runtime.REGISTERS[1])
            if quotient != args[0] // args[1] or remainder != args[0] % args[1]:
                raise ValueError('Actual nested original unsigned32 ABI result differs')
            nested.append({'entry': hex(SCALAR), 'inputWords': args, 'actualReturnPc': hex(pc), 'quotient': quotient, 'remainder': remainder})
        if pc == SCALAR:
            args = [machine.reg_read(register) for register in match_runtime.REGISTERS[:2]]
            if frame or not args[1]:
                raise ValueError('Unexpected scalar denominator/call nesting')
            frame.extend([args])
        if not (0x02025F1C <= pc < QUOTIENT or QUOTIENT <= pc < QUOTIENT + 72 or 0x02026350 <= pc < 0x02026534):
            raise ValueError('Execution escaped configured original runtime parents')
        visited.add(pc)

    def write(machine, access, location, size, value, unused):
        if not initial[-2] - 0x400 <= location < initial[-2]:
            raise ValueError('Runtime division wrote outside its bounded stack backing')
        writes.append([location - initial[-2], size, value & ((1 << (size * 8)) - 1)])

    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    cpu.emu_start(entry, RETURN, count=100000, timeout=1000000)
    actual = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
    if cpu.reg_read(UC_ARM_REG_PC) != RETURN or actual[4:] != initial[4:] or frame or cpu.reg_read(UC_ARM_REG_CPSR) & 0xFF != 0xD3:
        raise ValueError('Original runtime failed actual return or saved-register/stack ABI')
    result = actual[0] | actual[1] << 32
    if denominator and result != (numerator // denominator if entry == QUOTIENT else numerator % denominator):
        raise ValueError('Independent unsigned64 quotient/remainder model differs')
    return {'entry': hex(entry), 'numerator': numerator, 'denominator': denominator, 'seed': seed, 'raw64Result': result,
        'actualReturn': True, 'returnPc': hex(RETURN), 'registers': actual, 'cpsr': cpu.reg_read(UC_ARM_REG_CPSR),
        'savedR4ThroughR12AndSpLrPreserved': True, 'actualNestedScalarReturns': len(nested), 'nestedScalarReturns': nested,
        'visited': sorted(visited), 'stackWrites': writes, 'sourceCredit': 0, 'supportedCErrorPathCredit': 0}


def main():
    import sys
    import unicorn
    if unicorn.__version__ != '2.1.4' or sys.version_info[:3] != (3, 13, 5):
        raise ValueError('Pinned Unicorn runtime differs')
    if sha((ROOT / 'inputs/game.nds').read_bytes()) != ROM_SHA:
        raise ValueError('Original measured ROM differs')
    raw = IMAGE.read_bytes()
    if sha(raw) != IMAGE_SHA:
        raise ValueError('Original measured ARM9 differs')
    specs = functions()
    for address, size in ((0x02025F1C, 448), (QUOTIENT, 72), (0x02026350, 484)):
        if not any(row['address'] == address and row['bytes'] == size and row['mode'] == 'arm' for row in specs):
            raise ValueError('Configured runtime parent/label layout changed')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    prologues = []
    for address in (QUOTIENT, REMAINDER):
        body = raw[address - BASE:address - BASE + (12 if address == QUOTIENT else 8)]
        instructions = [{'pc': hex(row.address), 'mnemonic': row.mnemonic, 'operands': row.op_str} for row in decoder.disasm(body, address)]
        if body[:4] != bytes.fromhex('f0582de9'):
            raise ValueError('Independent actual entry push frame differs')
        prologues.append({'entry': hex(address), 'bytes': body.hex(), 'sha256': sha(body), 'instructions': instructions,
            'independentSavedFrame': True, 'sharedJoin': hex(JOIN)})
    edges = (0, 1, 0xFFFFFFFF, 0x100000000, 0x7FFFFFFFFFFFFFFF, 0x8000000000000000, 0xFFFFFFFFFFFFFFFF)
    divisors = (1, 2, 3, 10, 0xFFFFFFFF, 0x100000000, 0x8000000000000000, 0xFFFFFFFFFFFFFFFF)
    normal = [execute(entry, numerator, denominator, seed) for seed, (entry, numerator, denominator) in enumerate(
        (entry, numerator, denominator) for entry in (QUOTIENT, REMAINDER) for numerator in edges for denominator in divisors)]
    zero = [execute(entry, numerator, 0, seed + 1000) for seed, (entry, numerator) in enumerate(
        (entry, numerator) for entry in (QUOTIENT, REMAINDER) for numerator in (0, 1, 0xFFFFFFFFFFFFFFFF))]
    if any(row['raw64Result'] != row['numerator'] for row in zero):
        raise ValueError('Original zero-divisor characterization changed')
    references = []
    for row in specs:
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM if row['mode'] == 'arm' else CS_MODE_THUMB)
        decoder.detail = True
        first = row['address'] - BASE
        for instruction in decoder.disasm(raw[first:first + row['bytes']], row['address']):
            if (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) and instruction.operands and instruction.operands[0].type == 2:
                target = instruction.operands[0].imm & ~1
                if target in (QUOTIENT, REMAINDER, JOIN, CORE, SCALAR):
                    references.append({'module': 'main', 'root': hex(row['address']), 'mode': row['mode'], 'pc': hex(instruction.address),
                        'instruction': instruction.mnemonic, 'target': hex(target)})
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': sha(Path(__file__).read_bytes()),
        'romSha256': ROM_SHA,
        'inputModule': IMAGE.relative_to(ROOT).as_posix(), 'inputModuleSha256': IMAGE_SHA, 'processor': 'arm9', 'module': 'main', 'mode': 'arm',
        'configuredParent': {'address': hex(QUOTIENT), 'bytes': 72}, 'configuredRemainderLabel': hex(REMAINDER),
        'prologues': prologues, 'sharedJoin': hex(JOIN), 'sharedCoreInsideParent': {'parent': '0x02025f1c', 'bytes': 448, 'entry': hex(CORE)},
        'originalScalarDependency': {'parent': '0x02026350', 'bytes': 484, 'entry': hex(SCALAR)},
        'normalRecords': normal, 'actualNonzeroDivisorReturns': len(normal), 'actualNestedScalarReturns': sum(row['actualNestedScalarReturns'] for row in normal),
        'separateZeroDivisorCharacterization': zero, 'actualZeroDivisorReturns': len(zero), 'zeroDivisorSupportedCErrorCredit': 0,
        'configuredMainDirectReferences': references, 'cpuModel': 'Unicorn ARM946', 'instructionLimit': 100000, 'timeoutMicroseconds': 1000000,
        'configuredSymbols': {'path': 'config/arm9/symbols.txt', 'sha256': sha((ROOT / 'config/arm9/symbols.txt').read_bytes())},
        'freshMachinePerExecution': True, 'providerReplacements': [], 'sourceOrBoundaryOrCompilerAliasCredit': 0, 'sharedFilesChanged': False,
        'limitations': ['Read-only ABI characterization; no source/function/boundary/alias acceptance or original-assembly provenance',
            'Direct references scanned only configured main ARM/Thumb scopes; data-pool false positives and other modules require separate review',
            'Zero-divisor observed native return is separate from C division/modulus semantics and receives zero supported-C-error credit']}
    output = ROOT / 'evidence/research/main-u64-unsigned-entries-arm7-20261031.json'
    write_json(output, report)
    print(json.dumps({'report': output.relative_to(ROOT).as_posix(), 'sha256': sha(output.read_bytes()), 'nonzeroReturns': len(normal),
        'nestedScalarReturns': report['actualNestedScalarReturns'], 'zeroReturnsSeparate': len(zero), 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
