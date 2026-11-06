import gzip
import hashlib
import json
import random
import struct
from pathlib import Path
import match_runtime as compiler
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

WORK = ROOT / 'work/main-list-count60-20261101'
ENTRY = 0x02009A5C
DATA = 0x02400000
STACK = 0x03030000
STOP = 0x0F000000


def execute(image, body, index, bound=4096):
    rng = random.Random(0x9A5C0000 + index)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x100000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    machine.mem_map(DATA, 16384)
    page = bytearray(rng.randbytes(16384))
    count = index % 33
    addresses = [DATA + 0x100 * (value + 1) for value in range(count)]
    rng.shuffle(addresses)
    for position, address in enumerate(addresses):
        struct.pack_into('<I', page, address - DATA, addresses[position + 1] if position + 1 < count else 0)
    machine.mem_write(DATA, bytes(page))
    head = addresses[0] if addresses else 0
    machine.mem_write(0x020E3780, struct.pack('<I', head))
    machine.mem_map(STACK, 8192)
    guard = rng.randbytes(8192)
    machine.mem_write(STACK, guard)
    machine.mem_map(STOP, 4096)
    cpsr = [0x1F, 0x9F, 0x5F, 0xDF][index % 4] | ((index % 16) << 28)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    registers = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
        UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
    initial = [rng.getrandbits(32) for unused in registers]
    for register, value in zip(registers, initial):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 4096)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    observed, helper, writes, calls, returns = set(), set(), [], [], []

    def code(unused, address, size, context):
        if ENTRY <= address < ENTRY + 56:
            observed.update(range(address, address + size))
        if 0x02007FF4 <= address < 0x02008020:
            helper.update(range(address, address + size))
        if address in [0x02007FF4, 0x02008008]:
            calls.append(address)
        if address in [0x02009A64, 0x02009A8C]:
            returns.append(address)

    def write(unused, access, address, size, value, context):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == STACK + 4096
    for register, value in zip(registers[4:12], initial[4:12]):
        assert machine.reg_read(register) == value
    assert machine.reg_read(UC_ARM_REG_CPSR) & 0xDF == cpsr & 0xDF
    assert bytes(machine.mem_read(DATA, 16384)) == page
    assert bytes(machine.mem_read(0x020E3780, 4)) == struct.pack('<I', head)
    stack = bytes(machine.mem_read(STACK, 8192))
    assert stack[:4088] == guard[:4088] and stack[4096:] == guard[4096:]
    assert len(writes) == 2 and all(STACK + 4088 <= event[0] < STACK + 4096 for event in writes)
    assert calls == [0x02007FF4, 0x02008008] and returns == [0x02009A64, 0x02009A8C]
    return dict(result=machine.reg_read(UC_ARM_REG_R0), expected=count,
        registers=[machine.reg_read(register) for register in registers], cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        pageSha256=hashlib.sha256(page).hexdigest(), stackSha256=hashlib.sha256(stack).hexdigest(),
        writes=writes, ownObserved=sorted(observed), helperObserved=sorted(helper), actualHelperReturns=2)


def build(source, label, exact):
    compiler.WORK = WORK / label / 'compile'
    rows, unused = compiler.compare(source, 'main', 2, 'off', speed=True)
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
    metadata, image, unused = measured_module('main')
    source = ROOT / 'src/runtime/20261101_list_count60/native_main_02009a5c.c'
    row, proof, body = build(source, 'correct', True)
    assert body == image[ENTRY - 0x02000000:ENTRY - 0x02000000 + 60]
    cases, own, helpers = [], set(), set()
    for index in range(264):
        original = execute(image, body, index)
        candidate = execute(image, body, index)
        assert original == candidate and original['result'] == index % 33
        own.update(original['ownObserved'])
        helpers.update(original['helperObserved'])
        cases.append(dict(index=index, original=original, candidate=candidate))
    assert len(own) == 56 and len(helpers) == 44
    wrong = ROOT / 'generated/recovery/20261101-root-breadth/arm-02009a5c.c'
    bad_row, bad_proof, bad_body = build(wrong, 'wrong-byte-head', False)
    bad_cases = [execute(image, bad_body, index) for index in range(264)]
    rejected = sum(case['result'] != case['expected'] for case in bad_cases)
    assert rejected == 256
    try:
        execute(image, body, 0, bound=1)
    except AssertionError:
        pass
    else:
        raise AssertionError('Instruction-bound prefix counted as a return')
    trace = ROOT / 'evidence/traces/main-pointer-chain9a5c-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(dict(pairs=cases, wrong=bad_cases), sort_keys=True, separators=(',', ':')).encode()
    trace.write_bytes(gzip.compress(raw, mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof), exactBytes=60,
        sourceOnlyCompilerInput=True, originalObjectScaffolding=False)
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=[row], matchedFunctions=1, matchedBytes=60,
        oracle=dict(pairs=264, actualTopReturns=528, actualNativeHelperReturnsSeparate=1056, suppliedCalls=0,
            ownInstructionBytesObserved=56, ownLiteralBytes=4, nativeHelperBytesObservedSeparate=44,
            actualReturnRequired=True, independentModel='Count a finite acyclic word-pointer chain and restore the incoming IRQ mask',
            fullCoreRegistersFlagsDataPagesStackAndOrderedWritesCompared=True),
        negativeEvidence=dict(compilation=bad_row, genuineLinkComparison=bad_proof, actualReturns=264,
            independentModelRejections=rejected, unchangedPositives=8, prefixCompletionCredit=0),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace)),
            dict(path=wrong.relative_to(ROOT).as_posix(), sha256=sha256(wrong))],
        reproductionCommand='python match_main_pointer_chain9a5c_20261101.py',
        limitations=['Finite acyclic lists0..32 only; cycles and invalid pointers remain unsupported',
            'Original IRQ save/restore ARM routines execute; no scheduler, concurrency or atomic snapshot guarantee',
            'Node is a measured next-word prefix only; gameplay meaning and historical type name remain unknown',
            'Whole-module/source-only ROM acceptance and a full Windows game remain separate'])
    write_json(ROOT / 'evidence/matches/main-pointer-chain9a5c-20261101.json', report)
    print(dict(newFunctionCandidates=1, bytes=60, actualTopReturns=528, originalHelperReturns=1056,
        wrongReturns=264, wrongRejections=rejected))


if __name__ == '__main__':
    main()
