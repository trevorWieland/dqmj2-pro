import hashlib
import struct
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as C
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_REG, ARM_SFT_ASR
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_CPU_ARM_946
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module
import probe_ghidra_carry863_20261102 as P
import ov001_action822_machine_20261102 as R

BASE = ROOT / 'nonmatching/overlay-lane/20261102-flags869'


def signed(value):
    return value - 0x100000000 if value & 0x80000000 else value


def indices(ins):
    aliases = {'sb': 9, 'sl': 10, 'fp': 11, 'ip': 12}
    result = []
    for operand in ins.operands:
        if operand.type != ARM_OP_REG:
            raise ValueError('869 non-register native flag operand')
        name = ins.reg_name(operand.reg)
        result.append(aliases[name] if name in aliases else int(name[1:]))
    if max(result) >= 13 or result[1] == result[2]:
        raise ValueError('869 unsupported flag register alias')
    return result


def execute_compare(image, x, y, borrow):
    u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    u.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address in [P.ENTRY, P.SP - 0x1000, P.STOP]:
        u.mem_map(address, 0x1000)
    u.mem_write(P.ENTRY, image)
    u.reg_write(R.UC_ARM_REG_CPSR, 0xD3)
    for index, reg in enumerate(R.REGS):
        u.reg_write(reg, 0x82820000 + index * 257)
    saved = [u.reg_read(reg) for reg in R.REGS[4:12]]
    for reg, value in zip(R.REGS[:3], [x, y, borrow]):
        u.reg_write(reg, value)
    u.reg_write(R.UC_ARM_REG_SP, P.SP)
    u.reg_write(R.UC_ARM_REG_LR, P.STOP)
    u.emu_start(P.ENTRY, P.STOP, count=100)
    if u.reg_read(R.UC_ARM_REG_PC) != P.STOP or u.reg_read(R.UC_ARM_REG_SP) != P.SP or [u.reg_read(reg) for reg in R.REGS[4:12]] != saved:
        raise ValueError('869 comparator proper return/ABI missing')
    return u.reg_read(R.REGS[0])


def native_subtract(ins, x, y, borrow):
    u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    u.ctl_set_cpu_model(UC_CPU_ARM_946)
    u.mem_map(ins.address & ~0xFFF, 0x1000)
    u.mem_write(ins.address, bytes(ins.bytes))
    u.reg_write(R.UC_ARM_REG_CPSR, 0xD3 | ((1 - borrow) << 29))
    dst, left, right = indices(ins)
    u.reg_write(R.REGS[left], x)
    u.reg_write(R.REGS[right], y)
    shift = ins.operands[2].shift
    effective = signed(y)
    if shift.value:
        if shift.type != ARM_SFT_ASR:
            raise ValueError('869 unsupported native subtract shift')
        effective >>= shift.value
    u.emu_start(ins.address, ins.address + 4, count=1)
    flags = u.reg_read(R.UC_ARM_REG_CPSR)
    result = ((flags >> 31) & 1) != ((flags >> 28) & 1)
    expected = (effective - signed(x) - borrow < 0) if ins.mnemonic == 'rscs' else (signed(x) - effective - borrow < 0)
    if u.reg_read(R.UC_ARM_REG_PC) != ins.address + 4 or result != expected:
        raise ValueError('869 native SBCS signed comparison mismatch')
    return int(result)


def execute():
    exportPath = ROOT / 'evidence/generated/ghidra868/ov000/export.json'
    export = read_json(exportPath)
    moduleInfo, image, unused = measured_module('ov000')
    if export['moduleSha256'] != moduleInfo['sha256']:
        raise ValueError('869 export/module mismatch')
    engine = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    engine.detail = True
    inputs = P.cases()
    carrySites = []
    borrowSites = []
    for row in export['functions']:
        address = int(row['address'], 0)
        for operation in row['unsignedAdditionCarryOperations']:
            pc = int(operation['instruction'], 16)
            ins = next(engine.disasm(image[pc - 0x021D7240:pc - 0x021D7240 + 4], pc))
            if ins.mnemonic != 'adds' or operation['outputBytes'] != 1 or [x['bytes'] for x in operation['inputs']] != [4, 4] or any(x['highType'] != 'uint' or x['highTypeBytes'] != 4 for x in operation['inputs']):
                raise ValueError('869 carry node/native width/operator mismatch')
            site = dict(address=pc, bytesHex=bytes(ins.bytes).hex(), disassembly=ins.mnemonic + ' ' + ins.op_str, registers=indices(ins))
            outputs = [P.execute_native(site, x, y, carry) for x, y in inputs for carry in [0, 1]]
            carrySites.append(dict(function=row['address'], operation=operation, native=site, singleInstructionProbes=len(outputs), outputSha256=hashlib.sha256(bytes(outputs)).hexdigest()))
        body = image[address - 0x021D7240:address - 0x021D7240 + row['nativeBytes']]
        for ins in engine.disasm(body, address):
            if ins.mnemonic not in ['sbcs', 'rscs']:
                continue
            values = [native_subtract(ins, x, y, borrow) for x, y in inputs for borrow in [0, 1]]
            borrowSites.append(dict(function=row['address'], address=hex(ins.address), bytesHex=bytes(ins.bytes).hex(), disassembly=ins.mnemonic + ' ' + ins.op_str, singleInstructionProbes=len(values), outputSha256=hashlib.sha256(bytes(values)).hexdigest()))
    source = BASE / 'positive/source.c'
    wrong = BASE / 'wrong/source.c'
    text = 'typedef unsigned long u32;\ntypedef signed long s32;\ntypedef signed long long s64;\nu32 native_main_0201b248(s32 left, s32 right, u32 borrow) {\n    return (s64) left - (s64) right - (s64) borrow < 0;\n}\n'
    for path, data in [(source, text), (wrong, text.replace('(s64) left - (s64) right - (s64) borrow < 0', '(u32) left < (u32) right'))]:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_text() != data:
            raise ValueError('869 frozen synthetic source changed')
        path.write_text(data)
    targets = []
    for compiler in sorted(C.COMPILER_PINS):
        proof, body = P.compile_probe(source, compiler, '869-' + sha256(ROOT / compiler)[:12])
        values = [execute_compare(body, x, y, borrow) for x, y in inputs for borrow in [0, 1]]
        if values != [int(signed(x) - signed(y) - borrow < 0) for x, y in inputs for borrow in [0, 1]]:
            raise ValueError('869 C signed33-bit comparison failed')
        targets.append(dict(compiler=compiler, proof=proof, actualTopReturns=len(values), resultSha256=hashlib.sha256(bytes(values)).hexdigest()))
    proof, body = P.compile_probe(wrong, sorted(C.COMPILER_PINS)[0], '869-wrong-unsigned')
    values = [execute_compare(body, x, y, borrow) for x, y in inputs for borrow in [0, 1]]
    rejected = sum(value != int(signed(x) - signed(y) - borrow < 0) for value, (x, y, borrow) in zip(values, [(x, y, borrow) for x, y in inputs for borrow in [0, 1]]))
    if not rejected or len(carrySites) != 26 or len(borrowSites) != 5:
        raise ValueError('869 flag coverage/control incomplete')
    report = dict(schemaVersion=1, sourceCredit=0, nativeGameFunctionCredit=0, allPassed=True, module='ov000', moduleSha256=moduleInfo['sha256'], export=dict(path=exportPath.relative_to(ROOT).as_posix(), sha256=sha256(exportPath)), unsignedCarrySites=carrySites, signedBorrowComparisonSites=borrowSites, nativeSingleInstructionProbes=sum(row['singleInstructionProbes'] for row in carrySites + borrowSites), nativeProbeFunctionReturns=0, signedComparisonCProbes=targets, actualPositiveCProbeReturns=sum(row['actualTopReturns'] for row in targets), negativeEvidence=dict(proof=proof, actualTopReturns=len(values), rejected=rejected, positive=len(values) - rejected), limits=['Tool qualification only; no game function/source/module credit.', 'Each explicit Ghidra CARRY4 site has named 4-byte unsigned operands mapped to original ADDS, separate from ambiguous M2C_CARRY result placeholders.', 'Original SBCS/RSCS sites preserve ordinary/reversed operand order and actual ASR12/31 shifted-input domains; both borrow states are independently exercised.', 'The C signed64 intermediate computes a signed33-bit difference without signed32 overflow, with borrow restricted to0/1. This supports those whole comparisons, not a generic SBORROW/SCARRY/shift-carry macro.', 'Borrowed main0201B248 synthetic symbol, private links and single-step probes remain explicitly zero credit; single-step native probes are not function returns.'])
    write_json(ROOT / 'evidence/verification/ghidra-flags869-sites-20261102.json', report)
    print(dict(carrySites=len(carrySites), borrowSites=len(borrowSites), nativeSingleInstructionProbes=report['nativeSingleInstructionProbes'], actualCProbeReturns=report['actualPositiveCProbeReturns'], wrongReturns=len(values), wrongRejects=rejected, sourceCredit=0))


if __name__ == '__main__':
    execute()
