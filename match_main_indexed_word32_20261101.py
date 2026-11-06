import gzip
import hashlib
import json
import random
import struct
from pathlib import Path
import match_runtime as compiler
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY = 0x02038008
ARRAY = 0x020F47D0
PAGE = 0x020F4000
STACK = 0x03030000
STOP = 0x0F000000
WORK = ROOT / 'work/main-indexed-word32-20261101'


def execute(image, body, index, bound=64):
    rng = random.Random(0x380080000 + index)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x100000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    slot = index % 128
    examples = [0, 1, 0x7FFF, 0x8000, 0xFFFF, 0x10000, 0x80000000, 0xFFFFFFFF]
    argument = examples[index // 128] if index < 1024 else rng.getrandbits(32)
    original = bytearray(rng.randbytes(16384))
    offset = ARRAY + slot * 36 - PAGE
    original[offset + 2:offset + 4] = b'\xcc\xdd'
    machine.mem_write(PAGE, bytes(original))
    machine.mem_map(STACK, 4096)
    machine.mem_map(STOP, 4096)
    stack = rng.randbytes(4096)
    machine.mem_write(STACK, stack)
    registers = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
        UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
        UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
    initial = [rng.getrandbits(32) for register in registers]
    for register, value in zip(registers, initial):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_R0, slot)
    machine.reg_write(UC_ARM_REG_R1, argument)
    cpsr = 0x10 | ((index % 16) << 28)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    machine.reg_write(UC_ARM_REG_SP, STACK + 2048)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    observed, writes = set(), []
    def code(uc, address, size, unused):
        assert ENTRY <= address < ENTRY + len(body), hex(address)
        observed.add(address)
    def write(uc, access, address, size, value, unused):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP, 'Instruction-bound exhaustion is not return'
    assert machine.reg_read(UC_ARM_REG_SP) == STACK + 2048
    assert machine.reg_read(UC_ARM_REG_LR) == STOP
    assert bytes(machine.mem_read(STACK, 4096)) == stack
    assert machine.reg_read(UC_ARM_REG_CPSR) == cpsr
    assert all(machine.reg_read(register) == value for register, value in zip(registers[3:], initial[3:]))
    expected = bytearray(original)
    value = argument & 0xFFFF
    struct.pack_into('<I', expected, offset, value)
    after = bytes(machine.mem_read(PAGE, 16384))
    result = machine.reg_read(UC_ARM_REG_R0)
    passed = result == value and after == expected and writes == [[ARRAY + slot * 36, 4, value]]
    return dict(slot=slot, argument=argument, result=result, expected=value, modelPassed=passed,
        actualReturn=True, registers=[machine.reg_read(register) for register in registers], cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        initialPageSha256=hashlib.sha256(original).hexdigest(), finalPageSha256=hashlib.sha256(after).hexdigest(),
        stackSha256=hashlib.sha256(stack).hexdigest(), writes=writes, observed=sorted(observed))


def build(source, template, label, exact):
    compiler.WORK = WORK / label / 'compile'
    flags = template['compilerFlags']
    rows, unused = compiler.compare(source, 'main', int(flags[0][2:]), flags[flags.index('-inline') + 1],
        speed='-opt' in flags and flags[flags.index('-opt') + 1] == 'speed', compiler=ROOT / template['compilerPath'])
    assert len(rows) == 1 and not rows[0].get('compileFailed')
    row = rows[0]
    try:
        proof = validate(row, qualified_bindings(row), WORK / label / 'link')
    except ValueError as error:
        if exact:
            raise
        assert isinstance(error.args[0], dict)
        proof = error.args[0]
    return row, proof, (WORK / label / 'link/caller.bin').read_bytes()


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    survey_path = ROOT / 'evidence/attempts/root-indexed-field-widths-20261101.json'
    survey = read_json(survey_path)
    exact = [row for row in survey['results'] if row['exactNativeBytes']]
    assert len(exact) == 1 and int(exact[0]['identity']['address'], 0) == ENTRY
    candidate = exact[0]
    source_input = ROOT / candidate['source']
    assert sha256(source_input) == candidate['sourceSha256']
    source = ROOT / 'src/runtime/20261101_indexed_word32/native_main_02038008.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    text = source_input.read_text()
    if source.exists():
        assert source.read_text() == text
    else:
        source.write_text(text, encoding='utf-8')
    row, proof, body = build(source, candidate['compilation'], 'correct', True)
    metadata, image, unused = measured_module('main')
    native = image[ENTRY - 0x02000000:ENTRY - 0x02000000 + 32]
    assert body == native and len(body) == 32
    traces, own = [], set()
    for index in range(1280):
        original = execute(image, native, index)
        recovered = execute(image, body, index)
        assert original == recovered and original['modelPassed']
        own.update(original['observed'])
        traces.append(dict(index=index, original=original, candidate=recovered))
    assert own == set(range(ENTRY, ENTRY + 28, 4))
    before = 'M2C_FIELD(native_data_020f47d0 + (arg0 * 0x24), u32 *, 0)'
    assert text.count(before) == 1
    wrong = ROOT / 'nonmatching/integration/20261101-indexed-word32/source.c'
    wrong.parent.mkdir(parents=True, exist_ok=True)
    changed = text.replace(before, before.replace('u32 *', 'u16 *'))
    if wrong.exists():
        assert wrong.read_text() == changed
    else:
        wrong.write_text(changed, encoding='utf-8')
    bad_row, bad_proof, bad_body = build(wrong, candidate['compilation'], 'wrong-halfword-store', False)
    bad_cases = [execute(image, bad_body, index) for index in range(128)]
    assert all(case['actualReturn'] and not case['modelPassed'] for case in bad_cases)
    try:
        execute(image, native, 0, bound=1)
    except AssertionError:
        pass
    else:
        raise AssertionError('Bounded prefix accepted as return')
    trace = ROOT / 'evidence/traces/main-indexed-word32-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(traces, sort_keys=True, separators=(',', ':')).encode(), mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof), exactBytes=32,
        sourceOnlyCompilerInput=True, originalObjectScaffolding=False)
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=[row], matchedFunctions=1, matchedBytes=32,
        oracle=dict(pairs=1280, actualTopReturns=2560, nativeDependencies=0, providers=0,
            actualReturnRequired=True, instructionBytesObserved=28, generatedPoolBytes=4,
            independentModel='Low unsigned halfword becomes a full word at byte stride36; return that unsigned halfword',
            fullSyntheticArrayPageStackRegistersFlagsAndOrderedWritesCompared=True),
        negativeEvidence=dict(compilation=bad_row, genuineLinkComparison=bad_proof, cases=bad_cases,
            actualWrongReturns=128, independentRejections=128, boundedPrefixCompletionCredit=0),
        replayDependencies=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in [survey_path, trace, source_input]],
        reproductionCommand='python match_main_indexed_word32_20261101.py',
        limitations=['Finite aligned array slots0..127 with synthetic backing; reachable game slot domain and complete aggregate size unproved',
            'Single-thread behavior only; historical field names and types are unproved',
            'No helpers, other source functions, whole module, source-only ROM or full native game credited'])
    write_json(ROOT / 'evidence/matches/main-indexed-word32-20261101.json', report)
    print(dict(newFunctionCandidates=1, initializedBytes=32, actualTopReturns=2560, wrongReturnsRejected=128, sourceAcceptancePending=True))


if __name__ == '__main__':
    main()
