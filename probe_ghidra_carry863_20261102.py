import hashlib
import random
import struct
import sys
import match_runtime as C
import unicorn
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_CPU_ARM_946
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_REG
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov001_action822_machine_20261102 as R

WORK = ROOT / 'work/ol863-carry-probe'
BASE = ROOT / 'nonmatching/overlay-lane/20261102-carry863'
ENTRY = 0x02650000
SP = 0x027F0000
STOP = 0x027FF000


def cases():
    values = [0, 1, 2, 0x7FF, 0x800, 0xFFFF, 0x10000, 0x7FFFFFFF, 0x80000000, 0xFFFFF7FF, 0xFFFFF800, 0xFFFFFFFE, 0xFFFFFFFF]
    result = [(x, y) for x in values for y in values]
    rng = random.Random(863)
    result.extend((rng.getrandbits(32), rng.getrandbits(32)) for unused in range(343))
    return result


def compile_probe(path, compiler, label):
    C.WORK = WORK / label / 'compile'
    rows, unused = C.compare(path, 'main', '2', 'off', compiler=ROOT / compiler)
    if len(rows) != 1 or rows[0].get('compileFailed') or rows[0]['relocations']:
        raise ValueError(('863 synthetic compiler failed', rows))
    row = rows[0]
    directory = WORK / label / 'canonical'
    try:
        comparison = validate(row, qualified_bindings(row), directory)
    except ValueError as error:
        if not error.args or not isinstance(error.args[0], dict):
            raise
        comparison = error.args[0]
    proof, image = link_private(row, qualified_bindings(row), directory, WORK / label / 'private', ENTRY)
    return dict(compilation=row, canonicalBorrowedIdentityComparison=comparison, privateLink=proof, sourceCredit=0), image


def execute_c(image, x, y):
    u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    u.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address in [ENTRY, SP - 0x1000, STOP]:
        u.mem_map(address, 0x1000)
    u.mem_write(ENTRY, image)
    u.reg_write(R.UC_ARM_REG_CPSR, 0xD3)
    for index, reg in enumerate(R.REGS):
        u.reg_write(reg, 0x7A7A0000 + index * 0x101)
    saved = [u.reg_read(reg) for reg in R.REGS[4:12]]
    u.reg_write(R.REGS[0], x)
    u.reg_write(R.REGS[1], y)
    u.reg_write(R.UC_ARM_REG_SP, SP)
    u.reg_write(R.UC_ARM_REG_LR, STOP)
    u.emu_start(ENTRY, STOP, count=100)
    if u.reg_read(R.UC_ARM_REG_PC) != STOP or u.reg_read(R.UC_ARM_REG_SP) != SP or [u.reg_read(reg) for reg in R.REGS[4:12]] != saved:
        raise ValueError('863 actual C probe return/ABI missing')
    return u.reg_read(R.REGS[0])


def native_site(image):
    engine = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    engine.detail = True
    address = 0x021DA5E4
    for ins in engine.disasm(image[address - 0x021D7240:address - 0x021D7240 + 2080], address):
        if ins.mnemonic == 'adds' and len(ins.operands) == 3 and all(op.type == ARM_OP_REG and op.shift.value == 0 for op in ins.operands):
            names = [ins.reg_name(op.reg) for op in ins.operands]
            aliases = {'sb': 9, 'sl': 10, 'fp': 11, 'ip': 12}
            indices = [aliases[name] if name in aliases else int(name[1:]) for name in names]
            if all(index < 13 for index in indices) and indices[1] != indices[2]:
                return dict(address=ins.address, bytesHex=bytes(ins.bytes).hex(), disassembly=ins.mnemonic + ' ' + ins.op_str, registers=indices)
    raise ValueError('863 no independently bounded register-register ADDS site')


def execute_native(site, x, y, carry):
    u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    u.ctl_set_cpu_model(UC_CPU_ARM_946)
    address = site['address']
    u.mem_map(address & ~0xFFF, 0x1000)
    u.mem_write(address, bytes.fromhex(site['bytesHex']))
    u.reg_write(R.UC_ARM_REG_CPSR, 0xD3 | (carry << 29))
    dst, left, right = site['registers']
    u.reg_write(R.REGS[left], x)
    u.reg_write(R.REGS[right], y)
    u.emu_start(address, address + 4, count=1)
    flags = u.reg_read(R.UC_ARM_REG_CPSR)
    result = u.reg_read(R.REGS[dst])
    if u.reg_read(R.UC_ARM_REG_PC) != address + 4 or result != (x + y) & 0xFFFFFFFF or ((flags >> 29) & 1) != (x + y > 0xFFFFFFFF):
        raise ValueError('863 native ADDS flag/result mismatch')
    return (flags >> 29) & 1


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('863 pinned runtime differs')
    source = BASE / 'positive/source.c'
    wrong = BASE / 'wrong/source.c'
    positiveText = 'typedef unsigned long u32;\ntypedef unsigned long long u64;\nu32 native_main_0201b248(u32 left, u32 right) {\n    return (u32) (((u64) left + (u64) right) >> 32);\n}\n'
    wrongText = positiveText.replace('(u32) (((u64) left + (u64) right) >> 32)', '((left + right) >> 31)')
    for path, text in [(source, positiveText), (wrong, wrongText)]:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_text() != text:
            raise ValueError('863 frozen synthetic source changed')
        path.write_text(text)
    moduleInfo, image, unused = measured_module('ov000')
    site = native_site(image)
    inputs = cases()
    native = [execute_native(site, x, y, initial) for x, y in inputs for initial in [0, 1]]
    targets = []
    for compiler, expected in sorted(C.COMPILER_PINS.items()):
        if sha256(ROOT / compiler) != expected:
            raise ValueError('863 compiler pin differs')
        proof, body = compile_probe(source, compiler, expected[:12])
        outputs = [execute_c(body, x, y) for x, y in inputs]
        if outputs != [int(x + y > 0xFFFFFFFF) for x, y in inputs]:
            raise ValueError('863 unsigned C expression mismatch')
        targets.append(dict(compiler=compiler, proof=proof, bodyBytes=len(body), actuallyReturningExecutions=len(outputs), outputSha256=hashlib.sha256(struct.pack('<' + 'I' * len(outputs), *outputs)).hexdigest()))
    wrongProof, wrongBody = compile_probe(wrong, sorted(C.COMPILER_PINS)[0], 'wrong-top-bit')
    wrongOutputs = [execute_c(wrongBody, x, y) for x, y in inputs]
    rejects = sum(value != int(x + y > 0xFFFFFFFF) for value, (x, y) in zip(wrongOutputs, inputs))
    if not rejects:
        raise ValueError('863 returning wrong-C rejection missing')
    report = dict(schemaVersion=1, sourceCredit=0, nativeGameFunctionCredit=0, nativeModule='ov000', nativeModuleSha256=moduleInfo['sha256'], nativeInstruction=site, nativeSingleInstructionProbes=len(native), nativeProbeFunctionReturns=0, nativeProbeEndPcChecked=True, cases=inputs, targets=targets, actualPositiveCProbeReturns=sum(row['actuallyReturningExecutions'] for row in targets), negativeEvidence=dict(proof=wrongProof, actualTopReturns=len(wrongOutputs), rejected=rejects, positive=len(wrongOutputs) - rejects), allPassed=True, limits=['Tool-qualification unsigned-add carry expression only; borrowed main0201B248 symbol is not a reconstruction or byte match and remains zero credit.', 'One original ov000 ADDS instruction is single-stepped with explicit operand registers and both initial C states; these are not native function returns.', 'Ghidra INT_CARRY has two equal-sized operands and unsigned-add overflow semantics; this result does not qualify M2C_CARRY(result), shift carry, ADC composed carry, signed overflow, unknown widths or an entire Ghidra-exported function.', 'All four pinned ARM946 compiler bodies execute genuine private-linked code and properly return with isolated state and callee-saved/SP checks; no host/device or game semantics claim.'])
    write_json(ROOT / 'evidence/verification/ghidra-carry863-unsigned-add-20261102.json', report)
    print(dict(cases=len(inputs), nativeSingleInstructionProbes=len(native), actualCProbeReturns=report['actualPositiveCProbeReturns'], wrongReturns=len(wrongOutputs), wrongRejects=rejects, sourceCredit=0))


if __name__ == '__main__':
    execute()
