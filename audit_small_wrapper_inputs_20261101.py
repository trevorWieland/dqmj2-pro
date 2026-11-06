import re
import match_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_JUMP, CS_GRP_CALL, CS_GRP_RET
from capstone.arm import ARM_REG_R0, ARM_REG_R1, ARM_REG_R2, ARM_REG_R3, ARM_REG_PC
from project import ROOT, read_json, sha256, write_json


def formal_count(text, address):
    match = re.search(r'\bnative_\w+_' + f'{address:08x}' + r'\s*\(([^()]*)\)\s*\{', text)
    if not match:
        return None
    arguments = match[1].strip()
    if arguments in ['', 'void']:
        return 0
    return len(arguments.split(','))


def prefix_inputs(code, address, mode):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if mode == 'thumb' else CS_MODE_ARM)
    decoder.detail = True
    registers = [ARM_REG_R0, ARM_REG_R1, ARM_REG_R2, ARM_REG_R3]
    written, required, instructions = set(), set(), []
    for instruction in decoder.disasm(code, address):
        if any(instruction.group(group) for group in [CS_GRP_JUMP, CS_GRP_CALL, CS_GRP_RET]):
            break
        reads, writes = instruction.regs_access()
        if ARM_REG_PC in writes:
            break
        if instruction.mnemonic not in ['push', 'pop', 'stmdb', 'stmfd']:
            required.update(registers.index(r) for r in reads if r in registers and r not in written)
        written.update(writes)
        instructions.append(dict(address=hex(instruction.address), mnemonic=instruction.mnemonic, operands=instruction.op_str))
    return sorted(required), instructions


def tail_preserved(code, address, mode):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if mode == 'thumb' else CS_MODE_ARM)
    decoder.detail = True
    registers = [ARM_REG_R0, ARM_REG_R1, ARM_REG_R2, ARM_REG_R3]
    written = set()
    for instruction in decoder.disasm(code, address):
        if instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_RET):
            return []
        if instruction.group(CS_GRP_JUMP):
            if instruction.mnemonic not in ['b', 'bx'] or instruction.op_str == 'lr':
                return []
            return [index for index, register in enumerate(registers) if register not in written]
        reads, writes = instruction.regs_access()
        if ARM_REG_PC in writes:
            return []
        written.update(writes)
    return []


def main():
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-98.json')
    assert not plan['linksPending']
    ledger_path = ROOT / 'generated/audits/wrapper-input-ledger98-20261101.json'
    assert sha256(ledger_path) == 'faf63e57491c7e00cbb31111de9dd165c934491519a77052088ac7224a649ccf'
    captured = read_json(ledger_path)
    revision, ledger_sha = captured['sourceCommit'], captured['sourceLedgerSha256']
    snapshot = read_json(ROOT / 'evidence/verification/accepted-cohort98-identities-v2-20261101.json')
    assert ledger_sha == snapshot['ledgerSha256']
    rows = captured['rows']
    lookup = {(r['module'], int(r['address'], 0)): r for r in rows if r['processor'] == 'arm9'}
    binaries, reviewed, findings = {}, 0, []
    for caller in rows:
        if caller['processor'] != 'arm9' or not caller['states']['functionMatched'] or caller['bytes'] > 64:
            continue
        if caller['module'] != 'main' and not re.fullmatch(r'ov\d{3}', caller['module']):
            continue
        source = ROOT / caller['sourceUnit']
        if source.suffix != '.c':
            continue
        assert sha256(source) == caller['sourceSha256']
        count = formal_count(source.read_text(), int(caller['address'], 0))
        if count is None:
            continue
        formal = re.search(r'\bnative_\w+_' + f'{int(caller["address"], 0):08x}' + r'\s*\(([^()]*)\)\s*\{', source.read_text())[1]
        if re.search(r'\b(?:u64|s64|double|f64|long|struct)\b', formal):
            continue
        caller_module = caller['module']
        if caller_module not in binaries:
            relative = f'extract/arm9_overlays/{caller_module}.bin' if caller_module.startswith('ov') else 'extract/arm9/arm9.bin'
            binaries[caller_module] = (relative, (ROOT / relative).read_bytes())
        offset = caller['binaryOffset']
        preserved = tail_preserved(binaries[caller_module][1][offset:offset + caller['bytes']], int(caller['address'], 0), caller['mode'])
        if not preserved:
            continue
        reviewed += 1
        for dependency in caller['dependencies']:
            symbol = dependency.get('symbol', '')
            if '_data_' in symbol or not re.search(r'_[0-9a-f]{8}$', symbol):
                continue
            value = dependency.get('target')
            if isinstance(value, str) and not value.startswith('0x'):
                continue
            address = (int(value, 0) if isinstance(value, str) else int(value)) & ~1
            module = caller['module'] if caller['module'].startswith('ov') and address >= 0x021D7240 else 'main'
            target = lookup.get((module, address))
            if not target:
                continue
            if module not in binaries:
                relative = f'extract/arm9_overlays/{module}.bin' if module.startswith('ov') else 'extract/arm9/arm9.bin'
                binaries[module] = (relative, (ROOT / relative).read_bytes())
            relative, binary = binaries[module]
            offset = target['binaryOffset']
            inputs, instructions = prefix_inputs(binary[offset:offset + min(target['bytes'], 128)], address, target['mode'])
            omitted = [index for index in inputs if index >= count and index in preserved]
            if omitted:
                findings.append(dict(callerModule=caller['module'], callerMode=caller['mode'], callerAddress=caller['address'],
                    callerBytes=caller['bytes'], source=caller['sourceUnit'], sourceSha256=caller['sourceSha256'],
                    declaredFormals=count, targetModule=module, targetMode=target['mode'], targetAddress=hex(address),
                    callerTailPreservedIncomingRegisters=preserved,
                    targetBytes=target['bytes'], targetInputModule=relative, targetInputModuleSha256=sha256(ROOT / relative),
                    targetPrefixIncomingRegisters=inputs, potentiallyUnrepresentedIncomingRegisters=omitted,
                    instructions=instructions, relocation=dependency, evidenceClass='static-review-candidate', sourceCredit=0))
    old = ROOT / 'src/runtime/runtime06/native_main_020380e4.c'
    new = ROOT / 'src/runtime/20261101_resource_word_forwarding/native_main_020380e4.c'
    assert formal_count(old.read_text(), 0x020380E4) == 1
    assert formal_count(new.read_text(), 0x020380E4) == 2
    assert any(r['callerAddress'] == '0x20380e4' and 1 in r['potentiallyUnrepresentedIncomingRegisters'] for r in findings)
    write_json(ROOT / 'evidence/attempts/small-wrapper-input-audit-20261101.json', dict(
        generator='audit_small_wrapper_inputs_20261101.py', generatorSha256=sha256(__file__),
        ledgerSha256=ledger_sha, ledgerSourceCommit=revision, acceptedCohort=98,
        capturedMetadata=ledger_path.relative_to(ROOT).as_posix(), capturedMetadataSha256=sha256(ledger_path),
        acceptedEvidenceSha256=sha256(ROOT / 'evidence/verification/cohort-2026-10-29-98.json'),
        reviewedSmallCWrappers=reviewed, findings=findings, sourceCredit=0,
        controls=dict(oldOneInputPrototypeDetected=True, explicitTwoInputPrototypeCounted=True), limitations=[
            'Conservative prefix read-before-write analysis stops at the first branch and excludes stack-save spacer reads',
            'Register liveness does not establish semantic arguments, forwarding, caller reachability or a source defect',
            'Every finding requires independent caller/target execution and source-interface review before migration',
            'No source, registry, preferences or accepted byte counts are changed']))
    print(dict(reviewed=reviewed, reviewCandidates=len(findings), sourceCredit=0))


if __name__ == '__main__':
    main()
