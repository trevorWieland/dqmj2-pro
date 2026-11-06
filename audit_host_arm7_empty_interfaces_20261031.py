import hashlib
import json
from pathlib import Path
import re
import match_runtime
import audit_arm7_bulk_20261030 as inventory
import arm7_predicate_abi_20261030_v3 as predicates
import capstone.arm as arm
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from project import write_json

ROOT = Path(__file__).resolve().parent
SNAPSHOT = ROOT / 'evidence/verification/accepted-cohort92-identities-v2-20261031.json'
REPORT = ROOT / 'evidence/research/host-arm7-empty-interface-candidates-20261031.json'
SCOPE = ROOT / 'provenance/host-arm7-empty-interface-scope-20261031.json'
SCOPE_SHA = 'e1f4e2348002074713d6895afd92cbe2b97a518ea48123123b8196184fad8b28'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def operand_reads(row):
    reads, writes = predicates.access_names(row)
    shifts = {row.reg_name(operand.shift.value) for operand in row.operands
        if operand.shift.type in (arm.ARM_SFT_ASR_REG, arm.ARM_SFT_LSL_REG, arm.ARM_SFT_LSR_REG, arm.ARM_SFT_ROR_REG, arm.ARM_SFT_RRX_REG)}
    return reads | shifts, writes, shifts


def prefixes(spec, summaries):
    instructions = {row.address: row for row in spec['instructions']}
    queue, seen, observations, stops = [(spec['address'], 0, flags) for flags in range(16)], set(), {}, set()
    while queue:
        pc, defined, flags = queue.pop()
        if (pc, defined, flags) in seen:
            continue
        seen.add((pc, defined, flags))
        if len(seen) > 20000:
            stops.add('prefix-state-cap')
            break
        if pc not in instructions:
            stops.add('outside-decoded-instruction-scope')
            continue
        row = instructions[pc]
        following = pc + row.size
        reads, writes, shift_reads = operand_reads(row)
        if row.mnemonic.startswith(('push', 'stm')):
            reads -= set(predicates.REGISTERS)
        conditional = row.cc not in (0, 15)
        if not predicates.predicate(row.cc, flags):
            queue.append((following, defined, flags))
            continue
        mask = sum(predicates.REGISTERS[name] for name in reads & predicates.REGISTERS.keys()) & ~defined
        if mask:
            key = pc, 'explicit-native-operand', mask
            observations[key] = {'pc': hex(pc), 'instruction': row.mnemonic + ' ' + row.op_str,
                'liveInMask': mask, 'class': key[1], 'conditionalPathFeasibilityUnproved': conditional}
            observations[key]['explicitRegisterShiftLiveInMask'] = sum(predicates.REGISTERS[name] for name in shift_reads & predicates.REGISTERS.keys()) & ~defined
        target = row.operands[0].imm & ~1 if row.operands and row.operands[0].type == 2 else None
        if row.group(CS_GRP_CALL):
            summary = summaries.get(target)
            if summary:
                needed = summary['registerInputMask'] & ~defined
                if needed:
                    key = pc, 'qualified-leaf-callee-input', needed
                    observations[key] = {'pc': hex(pc), 'instruction': row.mnemonic + ' ' + row.op_str,
                        'liveInMask': needed, 'class': key[1], 'callee': hex(target), 'calleeSummary': summary}
            stops.add('stop-at-call-no-output-or-CPSR-assumption')
            continue
        defined |= sum(predicates.REGISTERS[name] for name in writes & predicates.REGISTERS.keys())
        if predicates.conventional_return(row):
            stops.add('return-register-residue-excluded')
            continue
        if row.group(CS_GRP_JUMP) or 'pc' in writes:
            if target in instructions:
                queue.append((target, defined, flags))
            elif target in summaries:
                needed = summaries[target]['registerInputMask'] & ~defined
                if needed:
                    key = pc, 'qualified-leaf-tail-input', needed
                    observations[key] = {'pc': hex(pc), 'instruction': row.mnemonic + ' ' + row.op_str,
                        'liveInMask': needed, 'class': key[1], 'callee': hex(target), 'calleeSummary': summaries[target]}
                stops.add('tail-entry-not-followed')
            else:
                stops.add('opaque-or-outside-branch')
            continue
        if row.mnemonic.startswith(('mrs', 'msr')):
            stops.add('explicit-CPSR-state-operation-not-followed')
        elif row.update_flags or 'cpsr' in writes:
            may, unused = predicates.flag_update(row, spec['mode'])
            queue.extend((following, defined, new_flags) for new_flags in range(16) if not (new_flags ^ flags) & (15 & ~may))
        else:
            queue.append((following, defined, flags))
    return {'candidates': sorted(observations.values(), key=lambda row: (int(row['pc'], 0), row['class'])),
        'prefixStates': len(seen), 'stops': sorted(stops), 'noReturnProjectionUsed': True,
        'conservativeMayReadOnly': True, 'instructionPredicateFlagsEnumerated': True, 'operandValueFactsNotSolved': True}


def controls():
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True

    def spec(words):
        body = b''.join(word.to_bytes(4, 'little') for word in words)
        return {'address': 0x1000, 'mode': 'arm', 'instructions': list(decoder.disasm(body, 0x1000))}

    cases = [('save-restore-not-input', [0xE92D4001, 0xE8BD4001, 0xE12FFF1E], {}, False),
        ('bare-return-not-input', [0xE12FFF1E], {}, False),
        ('pointer-consumed-before-definition', [0xE1A04000, 0xE5940000, 0xE12FFF1E], {}, True),
        ('word-defined-first', [0xE3A00001, 0xE12FFF1E], {}, False),
        ('required-callee-input', [0xEB0003FE, 0xE12FFF1E], {0x2000: {'registerInputMask': 1}}, True),
        ('required-callee-input-defined', [0xE3A00001, 0xEB0003FD, 0xE12FFF1E], {0x2000: {'registerInputMask': 1}}, False),
        ('opaque-call-output-not-guessed', [0xEB0003FE, 0xE5910000, 0xE12FFF1E], {}, False),
        ('register-controlled-shift-count-is-input', [0xE3A02001, 0xE3A03000, 0xE1830012, 0xE12FFF1E], {}, True),
        ('defined-register-shift-count-not-input', [0xE3A00001, 0xE3A02001, 0xE3A03000, 0xE1830012, 0xE12FFF1E], {}, False),
        ('immediate-shift-is-not-register-input', [0xE3A02001, 0xE3A03000, 0xE1830082, 0xE12FFF1E], {}, False)]
    results = []
    for name, words, summaries, expected in cases:
        proof = prefixes(spec(words), summaries)
        if bool(proof['candidates']) != expected:
            raise ValueError('Empty-interface audit negative control failed: ' + name)
        results.append({'name': name, 'passed': True, 'expectedCandidate': expected, 'analysis': proof})
    for name, mode, body, expected in [('arm-register-shift-operand', CS_MODE_ARM, bytes.fromhex('120083e1'), {'r0', 'r2', 'r3'}),
        ('arm-immediate-shift-operand', CS_MODE_ARM, bytes.fromhex('820083e1'), {'r2', 'r3'}),
        ('thumb-register-shift-operand-only', CS_MODE_THUMB, bytes.fromhex('8840'), {'r0', 'r1'}),
        ('thumb-immediate-shift-operand-only', CS_MODE_THUMB, bytes.fromhex('4800'), {'r1'})]:
        decode = Cs(CS_ARCH_ARM, mode)
        decode.detail = True
        instruction = next(decode.disasm(body, 0x1000))
        reads, unused, shifts = operand_reads(instruction)
        actual = reads & set(predicates.REGISTERS)
        if actual != expected:
            raise ValueError('Register-shift operand control failed: ' + name)
        results.append({'name': name, 'passed': True, 'instruction': instruction.mnemonic + ' ' + instruction.op_str,
            'bytes': body.hex(), 'actualInputOperands': sorted(actual), 'explicitShiftRegisterOperands': sorted(shifts),
            'wholeThumbCfgAuditClaimed': False})
    return results


def empty_externals(text, spec, summaries):
    results = []
    for match in re.finditer(r'extern\s+[^;{}]*?\b(\w+_([0-9a-fA-F]{8}))\s*\(\s*(void)?\s*\)\s*;', text):
        name, target = match.group(1), int(match.group(2), 16)
        summary = summaries.get(target)
        calls = list(re.finditer(r'\b' + re.escape(name) + r'\s*\(\s*\)\s*;', text))
        sites = [] if spec is None else [hex(instruction.address) for instruction in spec['instructions']
            if instruction.group(CS_GRP_CALL) and instruction.operands and instruction.operands[0].type == 2 and instruction.operands[0].imm & ~1 == target]
        if summary and calls and sites:
            results.append({'declaredCallee': name, 'qualifiedCalleeSummary': summary, 'matchingDirectNativeCallSites': sites,
                'cEmptyCallOffsets': [item.start() for item in calls], 'declarationExplicitVoid': bool(match.group(3)),
                'contextSpecificArgumentVacuityNotExcluded': True})
    return results


def main():
    checks = controls()
    if digest(SCOPE.read_bytes()) != SCOPE_SHA:
        raise ValueError('Explicit selected-source audit scope differs')
    scope = json.loads(SCOPE.read_text())
    if digest(SNAPSHOT.read_bytes()) != scope['snapshotSha256']:
        raise ValueError('Selected snapshot differs')
    allowed = {row['path']: row['sha256'] for row in scope['sourceInputs']}
    for name, expected in allowed.items():
        if digest((ROOT / name).read_bytes()) != expected:
            raise ValueError('Frozen selected-source audit input differs: ' + name)
    specs = [row for row in inventory.specs() if row['program'] == '' and row['mode'] == 'arm']
    by = {(row['module'], row['address']): row for row in specs}
    summaries = {}
    for row in specs:
        if any(instruction.group(CS_GRP_CALL) for instruction in row['instructions']) or len(row['instructions']) > 80:
            continue
        analysis = predicates.analyze(row, return_live_mask=0)
        semantic_mask, shift_mask = 0, 0
        for observed in prefixes(row, {})['candidates']:
            semantic_mask |= observed['liveInMask']
            shift_mask |= observed.get('explicitRegisterShiftLiveInMask', 0)
        mask = (analysis['registerInputMask'] | shift_mask) & semantic_mask
        if analysis['prototypeHintUsable'] and mask:
            summaries[row['address']] = {'module': row['module'], 'nativeEntry': hex(row['address']), 'mode': 'arm',
                'inputModuleSha256': row['inputModuleSha256'], 'registerInputMask': mask,
                'calleeSaveOnlyInputsExcluded': True,
                'registerShiftLiveInMaskAddedToFrozenAnalysis': shift_mask & ~analysis['registerInputMask'],
                'returnProjectionMask': 0, 'analysis': analysis, 'argumentTypesProven': False}
    rows, external, skipped, checked, local = [], [], [], 0, 0
    for selected in json.loads(SNAPSHOT.read_text())['functions']:
        if selected.get('processor') != 'arm7' or selected.get('program') or selected.get('mode') != 'arm':
            continue
        source = ROOT / selected.get('source', '')
        if selected.get('source', '') not in allowed:
            skipped.append({'identity': selected, 'reason': 'selected-source-not-local-C'})
            continue
        text = source.read_text()
        if digest(source.read_bytes()) != selected['sourceSha256']:
            raise ValueError('Selected frozen C hash differs')
        local += 1
        address = selected['address']
        address = int(address, 0) if isinstance(address, str) else address
        spec = by.get((selected['module'], address))
        external.extend(dict(item, callerIdentity=selected, source=source.relative_to(ROOT).as_posix(), sourceSha256=digest(source.read_bytes()))
            for item in empty_externals(text, spec, summaries))
        definitions = re.findall(r'\b([A-Za-z_]\w*)\s*\(\s*(void)?\s*\)\s*\{', text)
        if len(definitions) != 1:
            continue
        if spec is None:
            skipped.append({'identity': selected, 'reason': 'no-legacy-canonical-decoded-scope'})
            continue
        checked += 1
        proof = prefixes(spec, summaries)
        if proof['candidates']:
            rows.append({'identity': selected, 'source': source.relative_to(ROOT).as_posix(), 'sourceSha256': digest(source.read_bytes()),
                'functionDefinition': definitions[0][0], 'explicitVoidParameters': bool(definitions[0][1]), 'analysis': proof})
    calibration = "extern u32 native_host_arm7_arm_037fd10c(void);\nvoid old_initialization(void) { native_host_arm7_arm_037fd10c(); }\n"
    positive = empty_externals(calibration, by[('arm7-wram', 0x037FD34C)], summaries)
    fixed = calibration.replace('037fd10c(void)', '037fd10c(u32)').replace('037fd10c();', '037fd10c(1);')
    if len(positive) != 1 or positive[0]['qualifiedCalleeSummary']['registerInputMask'] != 1 or positive[0]['matchingDirectNativeCallSites'] != ['0x37fd368'] or empty_externals(fixed, by[('arm7-wram', 0x037FD34C)], summaries):
        raise ValueError('Real D34C/D10C erased-argument calibration failed')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'scope': SCOPE.relative_to(ROOT).as_posix(), 'scopeSha256': SCOPE_SHA,
        'snapshot': SNAPSHOT.relative_to(ROOT).as_posix(), 'snapshotSha256': digest(SNAPSHOT.read_bytes()),
        'selectedLocalHostCInputsChecked': local, 'selectedNoInputDefinitionsAudited': checked, 'candidateDefinitions': len(rows),
        'emptyExternCallCandidates': external, 'emptyExternCallCandidateCount': len(external), 'qualifiedLeafInputSummaries': len(summaries),
        'candidates': rows, 'skipped': skipped, 'controls': checks, 'sourceCredit': 0, 'sourceSignatureOrSharedFileEdits': False,
        'knownCaseCalibration': {'unacceptedHostD34cToD10c': {'sourceInterfacePattern': calibration,
            'sourcePatternSha256': digest(calibration.encode()), 'matches': positive, 'explicitWordArgumentRejectedAsCandidate': True},
            'mainArm9Cd5bcAndCab98To49ad0': {'included': False, 'reason': 'ARM9 processor/main namespace is outside this host ARM7-only audit; excluded known cases are not negative findings'}},
        'limitations': ['Candidates require independent native ABI/caller/effect review; this audit never changes signatures',
            'Instruction predicate flags are enumerated; unmodeled operand-value relationships can yield mutually infeasible may paths',
            'Analysis stops at every call and makes no unknown call output, CPSR, transitive cycle or tail-execution assumption',
            'Push/STM saving alone and undefined return-register residue are excluded; stack-restored argument dependencies can be missed',
            'Leaf summaries use unchanged bounded v3 predicate analysis with return mask zero; no argument-type or language-signature proof']}
    write_json(REPORT, result)
    print(json.dumps({'report': REPORT.relative_to(ROOT).as_posix(), 'sha256': digest(REPORT.read_bytes()),
        'audited': checked, 'candidateDefinitions': len(rows), 'externCallCandidates': len(external), 'controls': len(checks), 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
