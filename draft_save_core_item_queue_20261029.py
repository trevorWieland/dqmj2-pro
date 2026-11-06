import ast
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps/native'))
import ndspy.rom
from ledger_state import collect_matches
import save_core_item_queue_build_20261029 as build
from save_core_item_queue_oracle_20261029 import validate


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    rom = (ROOT / 'inputs/game.nds').read_bytes()
    save = (ROOT / 'inputs/save.sav').read_bytes()
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    namespace = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
    if sha(rom) != namespace or sha(save) != '169d65a4c6ffcb0fe996d652f73a01f70d594a08ad2385098f628abbe1c4b8f0':
        raise AssertionError('Queue hypothesis input namespace changed')
    if sha(arm) != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':
        raise AssertionError('Queue hypothesis main module changed')
    if sha((ROOT / build.COMPILER).read_bytes()) != build.COMPILER_HASH:
        raise AssertionError('Queue hypothesis compiler pin changed')
    accepted, rejected = collect_matches(namespace)
    overlaps = [row for row in accepted.values() if row['module'] == 'main'
                and row['address'] < 0x02063A74 and 0x02063A0C < row['address'] + row['size']]
    if overlaps:
        raise AssertionError('This hypothesis now overlaps accepted source; preserve it and refresh ownership')
    rows, exact = build.compile_and_link(arm, 2, 'space')
    row = rows[0]
    if exact:
        binary = ROOT / next(iter(exact.values()))[0]['isolatedCallerBinary']
    else:
        failure = ast.literal_eval(row['failure'])
        binary = Path(failure['directory']) / 'caller.bin'
    compiled = binary.read_bytes()
    target = arm[0x63A0C:0x63A74]
    same = sum(left == right for left, right in zip(compiled, target))
    real_table = bytes(ndspy.rom.NintendoDSRom(rom).getFileByName('ItemTbl.bin'))
    oracle = validate(arm, compiled, save, real_table[8:])
    source = ROOT / build.SOURCE
    attempts = ROOT / 'work/mechanics-save/20261029-item-recent-find'
    records = [{'path': str(path.relative_to(ROOT)), 'sha256': sha(path.read_bytes())}
               for path in sorted(attempts.glob('candidate*.c'))]
    counterexample_path = ROOT / 'nonmatching/save-core/20261029-item-queue/legacy-counterexample.json'
    counterexample = json.loads(counterexample_path.read_text())
    if sha((ROOT / counterexample['preservedLegacyCopy']).read_bytes()) != counterexample['legacySourceSha256']:
        raise AssertionError('Legacy source no longer has the rejected sentinel/ABI identity')
    report = {
        'schemaVersion': 1, 'romSha256': namespace, 'saveSha256': sha(save),
        'arm9Sha256': sha(arm), 'stage': 'compileable-C-hypothesis-with-native-effect-fixtures',
        'notForRecoveryRegistry': True, 'netNewMatchedFunctions': 0, 'netNewMatchedBytes': 0,
        'preferredNonmatchingImplementation': True,
        'preferenceReason': 'Explicit typed ABI and native sentinel/effect fixtures pass; exact bytes still fail.',
        'knownIncorrectAlternatives': [{
            'source': counterexample['legacySource'],
            'sourceSha256': counterexample['legacySourceSha256'],
            'preservedSource': counterexample['preservedLegacyCopy'],
            'classification': counterexample['classification'],
            'reasons': counterexample['reasons'],
            'counterexample': str(counterexample_path.relative_to(ROOT)),
            'counterexampleSha256': sha(counterexample_path.read_bytes())
        }],
        'uniqueUnmatchedDraftFunctions': 1, 'uniqueUnmatchedNativeDraftBytes': 104,
        'source': build.SOURCE, 'sourceSha256': sha(source.read_bytes()),
        'compiler': build.COMPILER, 'compilerSha256': build.COMPILER_HASH,
        'hypothesis': row, 'realMwLinkedBinary': str(binary.relative_to(ROOT)),
        'realMwLinkedBinarySha256': sha(compiled), 'nativeBytes': len(target),
        'compiledBytes': len(compiled), 'sameOffsetBytes': same,
        'sameOffsetBytePercent': same * 100 / max(len(target), len(compiled)),
        'exactByteEqual': compiled == target,
        'itemTable': {'bytes': len(real_table), 'sha256': sha(real_table), 'recordStride': 88,
                      'providerEntry': 'main:arm:0x02065d88', 'categoryByteOffset': 44},
        'serializedQueueBytes': ['0x37D8..0x37E2', '0x37E4..0x37EE'],
        'queuePaddingBytes': ['0x37E2..0x37E4', '0x37EE..0x37F0'],
        'oracle': oracle, 'earlierSourceHypotheses': records,
        'generator': 'draft_save_core_item_queue_20261029.py',
        'generatorSha256': sha(Path(__file__).read_bytes()),
        'buildDriver': 'save_core_item_queue_build_20261029.py',
        'buildDriverSha256': sha((ROOT / 'save_core_item_queue_build_20261029.py').read_bytes()),
        'oracleSource': 'save_core_item_queue_oracle_20261029.py',
        'oracleSourceSha256': sha((ROOT / 'save_core_item_queue_oracle_20261029.py').read_bytes()),
        'linker': 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe',
        'linkerSha256': sha((ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe').read_bytes()),
        'failedExperiments': [
            {'source': 'candidate00.c', 'compiledBytes': 108, 'classification': 'size-mismatch'},
            {'source': 'candidate01.c', 'compiledBytes': 104, 'sameOffsetBytes': 85},
            {'source': 'candidate02.c', 'compiledBytes': 104, 'sameOffsetBytes': 92},
            {'source': 'candidate03.c', 'compiledBytes': 104, 'sameOffsetBytes': 98},
            {'source': 'candidate04.c', 'compiledBytes': 104, 'sameOffsetBytes': 98},
            {'classification': 'oracle-harness-ABI-assumption',
             'failure': 'Initial harness required LR unchanged after an ordinary nested call.',
             'resolution': 'Require return PC and SP; compare architectural LR across native/compiled engines.'}
        ],
        'limitations': [
            'The current real-linked C body differs in four register-encoding instructions. '
            'Semantic fixture success never counts as an exact source match.',
            'R2 is caller-saved and differs after the function; all relevant return, '
            'preserved-register, flags, stack and source-memory effects are checked.',
            'Synthetic u8 item IDs and every category byte are bounded model probes, not '
            'proof of valid gameplay IDs, queue freshness or ownership.',
            'The original24-byte item-record provider remains an explicit native dependency; '
            'it adds zero source credit. No normal gameplay function is stubbed.',
            'Negative/full-width out-of-table IDs, concurrent mutation and malformed table pointers '
            'remain unsupported. No story, encounter access or renewability meaning is assigned.'
        ]
    }
    if sha((ROOT / 'inputs/game.nds').read_bytes()) != namespace or sha((ROOT / 'inputs/save.sav').read_bytes()) != report['saveSha256']:
        raise AssertionError('Immutable input changed during queue hypothesis audit')
    output = ROOT / 'nonmatching/save-core/20261029-item-queue/report.json'
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'report': str(output), 'sameOffsetBytes': same, 'nativeBytes': 104,
                      'fixtureCases': oracle['cases'], 'actualReturns': oracle['nativeAndCompiledActualReturns'],
                      'differingCallerSavedRegisters': oracle['differingCallerSavedRegisterIndices'],
                      'netNewMatchedBytes': 0}))


if __name__ == '__main__':
    main()
