import copy
import json
from pathlib import Path
import prove_arm7_child_divide_scope_20261031 as producer
import arm7_lane_wordpair124_native_20261031 as native
from project import ROOT, sha256, write_json


def validate(report):
    if report['generator'] != Path(producer.__file__).name or report['generatorSha256'] != sha256(producer.__file__):
        raise ValueError('Code-role producer differs')
    if report['nativeGenerator'] != Path(native.__file__).name or report['nativeGeneratorSha256'] != sha256(native.__file__):
        raise ValueError('Actual native ABI generator differs')
    expected = {'program': 'dwc/utility.bin/move/child.srl', 'processor': 'arm7', 'module': 'utility-child-arm7-wram', 'mode': 'arm',
        'nativeEntry': '0x3805184', 'inputModule': native.WRAM, 'inputModuleSha256': native.WRAM_SHA,
        'configuredEntryBytesUnchanged': 8, 'actualExecutedCodeBytes': 480, 'newlyConfirmedCodeBytesOutsideConfiguredEntry': 472,
        'actualStandaloneOriginalReturns': 294, 'actualSeparateZeroDivisorCharacterizationReturns': 3,
        'sourceOrFunctionBoundaryOrDenominatorCredit': 0, 'sharedInventoryConfigModified': False, 'supportedDivisors': [1, 5, 7, 100, 400]}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('Qualified code/return/credit scope differs')
    raw = (ROOT / native.WRAM).read_bytes()
    span = raw[native.HELPER - native.WRAM_BASE:native.HELPER_END - native.WRAM_BASE]
    wanted = {'start': hex(native.HELPER), 'endExclusive': hex(native.HELPER_END), 'bytes': 484, 'sha256': native.digest(span)}
    if report['decodedSpan'] != wanted or sha256(ROOT / native.WRAM) != native.WRAM_SHA:
        raise ValueError('Measured full decoded range differs')
    if report['skippedNop'] != {'address': hex(native.SKIPPED), 'bytes': 4, 'word': '0xe1a00000', 'actualExecutionCredit': 0}:
        raise ValueError('Skipped instruction gained execution/padding credit')
    ranges = [{'start': hex(native.HELPER), 'endExclusive': hex(native.SKIPPED), 'bytes': native.SKIPPED - native.HELPER},
        {'start': hex(native.SKIPPED + 4), 'endExclusive': hex(native.HELPER_END), 'bytes': native.HELPER_END - native.SKIPPED - 4}]
    if report['executedArmInstructionRanges'] != ranges:
        raise ValueError('Disjoint actual ARM ranges differ')
    if report['unsupportedBudget']['returnCredit'] != 0 or report['unsupportedBudget']['state']['actualReturn']:
        raise ValueError('Budget exhaustion counted as native return')
    if len(report['records']) != 294 or len(report['zeroDivisorCharacterization']) != 3:
        raise ValueError('Actual return evidence absent')
    visited, targets = set(), set()
    for row in report['records']:
        state = row['state']
        if not state['actualReturn'] or state['writes'] or state['r0'] != row['numerator'] // row['divisor'] or state['r1'] != row['numerator'] % row['divisor']:
            raise ValueError('Native quotient/remainder word evidence invalid')
        if state['packedU64'] != state['r0'] | state['r1'] << 32:
            raise ValueError('Low/high ABI packing differs')
        for transfer in state['computedTransfers']:
            selector = transfer['selector']
            if transfer['pc'] != '0x38051d8' or selector not in range(0, 85, 12) or transfer['actualTarget'] != hex(0x038051E0 + (selector << 2)):
                raise ValueError('Native computed transfer qualification differs')
            targets.add(transfer['actualTarget'])
        visited.update(state['visited'])
    required = set(range(native.HELPER, native.HELPER_END, 4)) - {native.SKIPPED}
    if visited != required:
        raise ValueError('Original exercised executable code coverage differs')
    if report['computedTransferTargets'] != sorted(targets):
        raise ValueError('Published computed target set differs')
    for row in report['zeroDivisorCharacterization']:
        if row['callerContractCredit'] != 0 or not row['state']['actualReturn'] or row['state']['r0'] != row['numerator'] or row['state']['r1'] != 0:
            raise ValueError('Zero-divisor characterization or caller-domain exclusion differs')
    return True


def main():
    producer.main()
    report = json.loads(producer.REPORT.read_text())
    validate(report)
    controls = []
    changes = (
        ('wrong-program', ('program',), ''), ('wrong-processor', ('processor',), 'arm9'), ('wrong-mode', ('mode',), 'thumb'),
        ('wrong-entry', ('nativeEntry',), '0x380518c'), ('wrong-module', ('module',), 'arm7-wram'),
        ('wrong-module-hash', ('inputModuleSha256',), '0' * 64), ('wrong-decoded-end', ('decodedSpan', 'endExclusive'), '0x380536c'),
        ('skipped-nop-called-executed', ('skippedNop', 'actualExecutionCredit'), 4),
        ('denominator-or-source-double-credit', ('sourceOrFunctionBoundaryOrDenominatorCredit',), 472),
        ('frozen-config-edited', ('sharedInventoryConfigModified',), True),
        ('helper-returns-inflated', ('actualStandaloneOriginalReturns',), 297),
        ('budget-return-credit', ('unsupportedBudget', 'returnCredit'), 1),
        ('packed-abi-words-reversed', ('records', 7, 'state', 'packedU64'), 0),
        ('skipped-nop-merged-into-code-range', ('executedArmInstructionRanges', 0, 'endExclusive'), '0x38051e0'),
        ('computed-targets-invented', ('computedTransferTargets',), ['0x38051dc']),
        ('zero-divisor-as-caller-contract', ('zeroDivisorCharacterization', 0, 'callerContractCredit'), 1),
    )
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        cursor = changed
        for key in keys[:-1]:
            cursor = cursor[key]
        cursor[keys[-1]] = value
        try:
            validate(changed)
        except Exception as error:
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('Invalid original code-role proof accepted: ' + name)
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': sha256(__file__),
        'report': producer.REPORT.relative_to(ROOT).as_posix(), 'reportSha256': sha256(producer.REPORT),
        'controls': controls, 'allPassed': True, 'sourceCredit': 0, 'originalInventoryConfigChanged': False}
    output = ROOT / 'evidence/verification/arm7-child-divide-scope-controls-20261031.json'
    write_json(output, result)
    print(json.dumps({'report': output.relative_to(ROOT).as_posix(), 'sha256': sha256(output), 'controls': len(controls), 'allPassed': True}), flush=True)


if __name__ == '__main__':
    main()
