import hashlib
import random
import shutil
import sys
from pathlib import Path

import wave20261104_main_sdk_compiler as C
import link_runtime_unit as L
from recover_linked_runtime import qualified_bindings
from project import ROOT, sha256, read_json
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR

REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]
BASE, SENTINEL, STACK = 0x02000000, 0x02001000, 0x027FF000


def machine(body, address):
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(BASE, 0x800000)
    uc.mem_write(address, body)
    writes = []
    uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, access, addr, size, value, data: writes.append((addr, size, value)))
    return uc, writes


def execute(uc, writes, address, end, registers, cpsr, limit):
    uc.reg_write(UC_ARM_REG_CPSR, cpsr)
    for reg, word in zip(REGS, registers):
        uc.reg_write(reg, word)
    writes.clear()
    uc.emu_start(address, end, timeout=1000000, count=limit)
    state = [uc.reg_read(reg) for reg in REGS]
    assert uc.reg_read(UC_ARM_REG_PC) == end and not writes
    return state, uc.reg_read(UC_ARM_REG_CPSR)


def prove(inputs, matches, directory):
    import unicorn
    import capstone
    import elftools
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    lock = read_json(ROOT / 'tools.lock.json')
    assert sha256(sys.executable) == lock['python']['sha256']
    for module in [unicorn, capstone, elftools]:
        dependency = next(row for row in lock['nativeDependencies'] if row['module'] == module.__name__)
        assert Path(module.__file__).resolve() == (ROOT / dependency['file']).resolve()
        assert all(sha256(ROOT / name) == pin for name, pin in dependency['fileHashes'].items())
    directory.mkdir(parents=True, exist_ok=True)
    item = inputs['entries'][0]
    for pin in item['sourceDependencies']:
        shutil.copyfile(ROOT / pin['path'], directory / Path(pin['path']).name)
    source = directory / 'native_main_0200829c.c'
    source.write_text('#include "context.h"\nunsigned long native_main_0200829c(unsigned long x)\n{\n    return MATH_CountLeadingZerosInline(x);\n}\n')
    C.FLAGS = list(item['flags'])
    C.WORK = directory / 'compile'
    rows, unused = C.compare(source, 'main', C.FLAGS[0][2:], C.FLAGS[C.FLAGS.index('-inline') + 1], compiler=ROOT / item['compilerPath'])
    probe = rows[0]
    probe['sourceDependencies'] = item['sourceDependencies']
    link = L.validate(probe, qualified_bindings(probe), directory / 'link')
    linked = (directory / 'link/caller.bin').read_bytes()
    module, image, unused = L.measured_module('main')
    address = 0x0200829C
    native = image[address - BASE:address - BASE + 8]
    assert linked == native == bytes.fromhex('100f6fe11eff2fe1') and probe['compiledBytes'] == 8
    rng = random.Random(20261104041)
    values = sorted({0, 0xFFFFFFFF, *[1 << bit for bit in range(32)], *[((1 << bit) - 1) & 0xFFFFFFFF for bit in range(33)], *[((1 << bit) + 1) & 0xFFFFFFFF for bit in range(32)], *[rng.getrandbits(32) for unused in range(64)]})
    machines = [machine(body, address) for body in [native, linked]]
    traces, returns = [], 0
    for value in values:
        for flags in [0, 0x50000000, 0xA0000000, 0xF8000000]:
            registers = [rng.getrandbits(32) for unused in REGS]
            registers[0], registers[-2], registers[-1] = value, STACK, SENTINEL
            expected = list(registers)
            expected[0] = 32 - value.bit_length()
            cpsr = flags | 0x10
            results = [execute(uc, writes, address, SENTINEL, registers, cpsr, 4) for uc, writes in machines]
            assert results[0] == results[1] == (expected, cpsr)
            returns += 2
            traces.append((value, cpsr, expected[0]))
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    positions, instruction_steps = [], 0
    bit_values = [0, 0xFFFFFFFF, *[1 << bit for bit in range(32)]]
    for row in matches:
        start = int(row['address'], 0)
        body = Path(row['realLink']['linkerAttempt']['cwd']) / 'caller.bin'
        compiled = body.read_bytes()
        original = image[start - BASE:start - BASE + row['bytes']]
        for offset in range(0, row['bytes'], 4):
            decoded = list(decoder.disasm(original[offset:offset + 4], start + offset))
            if not decoded or not decoded[0].mnemonic.startswith('clz'):
                continue
            instruction = decoded[0]
            assert instruction.mnemonic == 'clzlt' and original[offset:offset + 4] == compiled[offset:offset + 4]
            register_name = instruction.op_str.split(',')[0].strip()
            assert instruction.op_str == register_name + ', ' + register_name
            register_index = int(register_name[1:])
            uc_pairs = [machine(code, start) for code in [original, compiled]]
            for value in bit_values:
                for flags in range(16):
                    cpsr = flags << 28 | 0x10
                    registers = [rng.getrandbits(32) for unused in REGS]
                    registers[register_index], registers[-2], registers[-1] = value, STACK, SENTINEL
                    expected = list(registers)
                    if ((cpsr >> 31) ^ (cpsr >> 28)) & 1:
                        expected[register_index] = 32 - value.bit_length()
                    result = [execute(uc, writes, start + offset, start + offset + 4, registers, cpsr, 1) for uc, writes in uc_pairs]
                    assert result[0] == result[1] == (expected, cpsr)
                    instruction_steps += 2
            positions.append(dict(caller=row['address'], offset=offset, instruction=instruction.mnemonic + ' ' + instruction.op_str,
                originalEncodedWord=instruction.bytes.hex(), bytes=4, behaviorScope='One original/source-recompiled predicated CLZ instruction; no caller return credit'))
    assert len(positions) == 6
    return dict(allPassed=True, originalHelperIdentity=dict(program='', processor='arm9', module='main', mode='arm', address=hex(address), bytes=8, targetSha256=hashlib.sha256(native).hexdigest()),
        freshlyCompiledPrimitiveProbeSource=source.relative_to(ROOT).as_posix(), freshlyCompiledPrimitiveProbeSourceSha256=sha256(source),
        probeRealLink=link, completeHelperOriginalAndCompiledReturns=returns, testedRawInputWords=len(values),
        nativeZeroResult=32, everySingleBitPositionCovered=True, helperGprSpLrAndCpsrCompared=True,
        orderedCpuWritesEmptyForEveryFixture=True, predicatedInlineSites=positions, predicatedInstructionSteps=instruction_steps,
        all16NzcvPatternsAndTakenUntakenLtCovered=True, instructionStepStopsAreNotFunctionReturns=True,
        inlineAssemblyBytes=24, newHelperSourceCredit=0, callerExecutionCredit=0,
        modelTraceSha256=hashlib.sha256(repr(traces).encode()).hexdigest(), nativeInstructionLimit=4, nativeTimeoutMicroseconds=1000000,
        limits=['Only the original CLZ helper and individual inline instructions execute; full algorithms and callees receive no behavior proof.',
                'No original executable bytes are patched, and the probe is freshly compiled and genuinely linked at an existing measured helper boundary.'])
