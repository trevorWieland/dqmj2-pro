import hashlib
import random
from pathlib import Path
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256
from lower_same_width_float_bitcasts_20261101 import lower
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

WORK = ROOT / 'work/same-width-bitcasts-20261101'
GENERATED = ROOT / 'generated/portability/20261101-validated-bitcast32'
BASE = 0x02400000
STACK = 0x03030000
STOP = 0x0F000000
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
    UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(body, bits, index, bound=128):
    rng = random.Random(0xB17CA570 + index)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(BASE, 4096)
    machine.mem_write(BASE, body)
    machine.mem_map(STACK, 4096)
    initial_stack = rng.randbytes(4096)
    machine.mem_write(STACK, initial_stack)
    machine.mem_map(STOP, 4096)
    cpsr = 0x10 | ((index % 16) << 28)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    initial_registers = [rng.getrandbits(32) for register in REGISTERS]
    for register, value in zip(REGISTERS, initial_registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_R0, bits)
    machine.reg_write(UC_ARM_REG_SP, STACK + 2048)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    observed, writes = set(), []
    def code(uc, address, size, unused):
        assert BASE <= address < BASE + len(body), hex(address)
        observed.add(address)
    def write(uc, access, address, size, value, unused):
        assert STACK + 1984 <= address and address + size <= STACK + 2048
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE, STOP, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP and machine.reg_read(UC_ARM_REG_SP) == STACK + 2048
    assert machine.reg_read(UC_ARM_REG_LR) == STOP and machine.reg_read(UC_ARM_REG_CPSR) == cpsr
    assert all(machine.reg_read(register) == value for register, value in zip(REGISTERS[4:12], initial_registers[4:12]))
    after = bytes(machine.mem_read(STACK, 4096))
    assert after[:1984] == initial_stack[:1984] and after[2048:] == initial_stack[2048:]
    return dict(inputWord=bits, outputWord=machine.reg_read(UC_ARM_REG_R0), actualReturn=True,
        observed=sorted(observed), privateStackWrites=writes, privateStackSha256=hashlib.sha256(after).hexdigest())


def compile_probe(source, executable, processor, label):
    compiler.WORK = WORK / label
    rows, unused = compiler.compare(source, 'main', 2, 'off', compiler=ROOT / executable, processor=processor)
    assert len(rows) == 1 and not rows[0].get('compileFailed'), rows
    row = rows[0]
    assert not row['relocations'] and '-fp' in row['compilerFlags'] and row['compilerFlags'][row['compilerFlags'].index('-fp') + 1] == 'soft'
    with (ROOT / row['object']).open('rb') as stream:
        elf = ELFFile(stream)
        body = elf.get_section(row['sectionIndex']).data()[row['sectionOffset']:row['sectionOffset'] + row['compiledBytes']]
    return row, body


def main():
    rng = random.Random(0xB17CA573)
    words = [0, 1, 0x80000000, 0xFFFFFFFF, 0x3F800000, 0xBF800000, 0x7F800000, 0xFF800000,
        0x7FC00001, 0x7F800001, 0xFFC00001, 0xFF800001, 0x007FFFFF, 0x00800000, 0x7F7FFFFF, 0xFF7FFFFF]
    words += [rng.getrandbits(32) for index in range(128)]
    examples = [('float-to-word', 's32', 'f32', 'M2C_BITWISE(s32, value)'),
        ('word-to-float', 'f32', 's32', 'M2C_BITWISE(f32, value)'),
        ('float-inverse-pair', 'f32', 'f32', 'M2C_BITWISE(f32, M2C_BITWISE(s32, value))'),
        ('word-inverse-pair', 's32', 's32', 'M2C_BITWISE(s32, M2C_BITWISE(f32, value))')]
    GENERATED.mkdir(parents=True, exist_ok=True)
    sources, syntax_controls = [], []
    for label, destination, origin, expression in examples:
        original = f'typedef float f32;\ntypedef signed int s32;\n{destination} native_main_02038008({origin} value) {{ return {expression}; }}\n'
        text, records = lower(original, {})
        source = GENERATED / (label + '.c')
        if source.exists():
            assert source.read_text() == text
        else:
            source.write_text(text, encoding='utf-8')
        sources.append((label, source, records))
    for destination, origin, expression in [('s32', 'f64', 'value'), ('f64', 's32', 'value'),
            ('s32', 's64', 'value'), ('s32', 'f32', 'unknown(value)')]:
        text = f'{destination} result({origin} value) {{ return M2C_BITWISE({destination}, {expression}); }}'
        try:
            lower(text, {})
        except ValueError as error:
            syntax_controls.append(dict(input=text, rejected=True, reason=str(error)))
        else:
            raise AssertionError('Unqualified or differing-width reinterpretation accepted')
    literal = 'const char *message = "M2C_BITWISE(s32, unknown())";'
    assert lower(literal, {}) == (literal, [])
    targets, actual_returns = [], 0
    for compiler_path, compiler_hash in sorted(compiler.COMPILER_PINS.items()):
        assert sha256(ROOT / compiler_path) == compiler_hash
        for processor in ['arm946e', 'arm7tdmi']:
            for label, source, records in sources:
                compilation, body = compile_probe(source, compiler_path, processor, compiler_hash[:12] + '-' + processor + '-' + label)
                executions = [execute(body, word, index) for index, word in enumerate(words)]
                assert all(row['outputWord'] == row['inputWord'] and row['actualReturn'] for row in executions)
                actual_returns += len(executions)
                targets.append(dict(compilerPath=compiler_path, compilerSha256=compiler_hash, processor=processor,
                    probe=label, source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), lowering=records,
                    compilation=compilation, compiledBodyHex=body.hex(), compiledBodyBytes=len(body),
                    actualReturns=len(executions), bitPatternDifferences=0, executions=executions))
    wrong = GENERATED / 'wrong-bit-flip.c'
    text = 'typedef signed int s32;\ns32 native_main_02038008(s32 value) { return value ^ 1; }\n'
    if wrong.exists():
        assert wrong.read_text() == text
    else:
        wrong.write_text(text, encoding='utf-8')
    compiler_path = sorted(compiler.COMPILER_PINS)[0]
    wrong_compilation, wrong_body = compile_probe(wrong, compiler_path, 'arm946e', 'wrong-bit-flip')
    wrong_executions = [execute(wrong_body, word, index) for index, word in enumerate(words)]
    assert all(row['actualReturn'] and row['outputWord'] != row['inputWord'] for row in wrong_executions)
    try:
        execute(bytes.fromhex(targets[0]['compiledBodyHex']), 0, 0, bound=1)
    except AssertionError:
        pass
    else:
        raise AssertionError('Bound exhaustion accepted as completion')
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), sourceCredit=0,
        adapter=dict(path='lower_same_width_float_bitcasts_20261101.py', sha256=sha256(ROOT / 'lower_same_width_float_bitcasts_20261101.py')),
        pinnedM2cSemantics=[dict(path=name, sha256=sha256(ROOT / name)) for name in [
            'tools/m2c/m2c-c632946b8cfbe8fce442b522dba92dfa72f1f317/m2c/translate.py',
            'tools/m2c/m2c-c632946b8cfbe8fce442b522dba92dfa72f1f317/m2c_macros.h']],
        wordsPerProbe=len(words), targets=targets, actualCorrectReturns=actual_returns,
        actualWrongReturns=len(wrong_executions), wrongRejections=len(wrong_executions), wrongCompilation=wrong_compilation,
        wrongExecutions=wrong_executions, syntaxControls=syntax_controls, stringLiteralPreserved=True,
        allPassed=True, originalArmGameByteCredit=0,
        limitations=['Synthetic primitive compiler/ABI probes, not recovered game functions or original scene execution',
            'The compiler driver borrows a boundary-qualified symbol solely to compile probes; no ROM comparison is accepted',
            'Only explicit f32/s32 equal-width casts; known function return types must be supplied from qualified context',
            'Union compound literals can add private stack traffic and are functional hypotheses until caller comparisons pass',
            'Floating payload identity is measured for pinned ARM soft-float compilers only; no Windows or Android floating-call ABI claim',
            'Unknown arithmetic/carry/stack/type placeholders remain unsupported; inverse pairs alone may cancel without a union'])
    write_json(ROOT / 'evidence/portability/same-width-bitcast32-probe-20261101.json', report)
    print(dict(targetConfigurations=len(targets), correctReturns=actual_returns, wrongRejections=len(wrong_executions), allPassed=True, sourceCredit=0))


if __name__ == '__main__':
    main()
