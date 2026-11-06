import json
from pathlib import Path
import arm7_lane_wordpair124_native_20261031 as native
import audit_arm7_bulk_20261030 as inventory
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from project import ROOT, sha256, write_json

REPORT = ROOT / 'evidence/arm7/lane-child-divide-wordpair-scope-20261031.json'


def main():
    raw = (ROOT / native.WRAM).read_bytes()
    if sha256(ROOT / native.WRAM) != native.WRAM_SHA:
        raise ValueError('Measured original child WRAM differs')
    entry = next(row for row in inventory.specs() if row['program'] and row['module'] == 'utility-child-arm7-wram' and row['address'] == native.HELPER)
    if entry['bytes'] != 8 or entry['mode'] != 'arm':
        raise ValueError('Frozen configured entry already differs; independent review required')
    first, last = native.HELPER - native.WRAM_BASE, native.HELPER_END - native.WRAM_BASE
    span = raw[first:last]
    decoded = list(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(span, native.HELPER))
    if len(decoded) * 4 != len(span) or len(span) != 484:
        raise ValueError('Computed divide range includes undecoded bytes')
    skipped = next(row for row in decoded if row.address == native.SKIPPED)
    if skipped.mnemonic != 'mov' or skipped.op_str != 'r0, r0' or decoded[-1].mnemonic != 'bx' or decoded[-1].op_str != 'lr':
        raise ValueError('Skipped NOP or actual final helper return differs')
    records, visited, targets = [], set(), set()
    for seed, (numerator, divisor) in enumerate(native.helper_cases()):
        state = native.helper_run(numerator, divisor, seed)
        if not state['actualReturn']:
            raise ValueError('Original divide ABI input failed actual return')
        visited.update(state['visited'])
        targets.update(row['actualTarget'] for row in state['computedTransfers'])
        records.append({'numerator': numerator, 'divisor': divisor, 'state': state})
    required = set(range(native.HELPER, native.HELPER_END, 4)) - {native.SKIPPED}
    if visited != required:
        raise ValueError('Original divide code role not completely exercised: ' + repr(sorted(required - visited)))
    zero = []
    for seed, numerator in enumerate((0, 1, 0xFFFFFFFF)):
        state = native.helper_run(numerator, 0, seed)
        if not state['actualReturn'] or [state['r0'], state['r1']] != [numerator, 0]:
            raise ValueError('Original zero-divisor characterization differs')
        zero.append({'numerator': numerator, 'state': state, 'callerContractCredit': 0})
    short = native.helper_run(0xFFFFFFFF, 7, 0, budget=1)
    if short['actualReturn']:
        raise ValueError('Division budget stop received return credit')
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': sha256(__file__),
        'nativeGenerator': Path(native.__file__).name, 'nativeGeneratorSha256': sha256(native.__file__),
        'program': 'dwc/utility.bin/move/child.srl', 'processor': 'arm7', 'module': 'utility-child-arm7-wram', 'mode': 'arm',
        'inputModule': native.WRAM, 'inputModuleSha256': native.WRAM_SHA, 'nativeEntry': hex(native.HELPER),
        'configuredEntryBytesUnchanged': 8, 'decodedSpan': {'start': hex(native.HELPER), 'endExclusive': hex(native.HELPER_END), 'bytes': 484, 'sha256': native.digest(span)},
        'executedArmInstructionRanges': [{'start': hex(native.HELPER), 'endExclusive': hex(native.SKIPPED), 'bytes': native.SKIPPED - native.HELPER},
            {'start': hex(native.SKIPPED + 4), 'endExclusive': hex(native.HELPER_END), 'bytes': native.HELPER_END - native.SKIPPED - 4}],
        'skippedNop': {'address': hex(native.SKIPPED), 'bytes': 4, 'word': '0xe1a00000', 'actualExecutionCredit': 0},
        'actualExecutedCodeBytes': len(visited) * 4, 'newlyConfirmedCodeBytesOutsideConfiguredEntry': len(visited) * 4 - 8,
        'computedTransferTargets': sorted(targets), 'actualStandaloneOriginalReturns': len(records),
        'actualSeparateZeroDivisorCharacterizationReturns': len(zero), 'supportedDivisors': [1, 5, 7, 100, 400],
        'abiContract': 'R0 unsigned32 quotient and R1 unsigned32 remainder for every measured nonzero supported divisor; C u64 is a low/high ABI-word view only',
        'records': records, 'zeroDivisorCharacterization': zero, 'unsupportedBudget': {'state': short, 'returnCredit': 0},
        'sourceOrFunctionBoundaryOrDenominatorCredit': 0, 'sharedInventoryConfigModified': False,
        'limitations': ['Code/data role and direct ABI are measured; this does not enlarge a canonical ordinary-function boundary or reconstruct the divide source',
            'Opaque outside interior references/shared-tail ownership are not globally reconciled by this code-scope proof',
            'No all-divisor, signed64 division, device, caller-scene or C portability meaning is claimed']}
    write_json(REPORT, report)
    print(json.dumps({'report': REPORT.relative_to(ROOT).as_posix(), 'sha256': sha256(REPORT),
        'returns': len(records), 'separateZeroDivisorReturns': len(zero), 'executedBytes': len(visited) * 4, 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
