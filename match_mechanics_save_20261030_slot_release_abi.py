from pathlib import Path
import subprocess
import sys
from project import ROOT, configuration, read_json, sha256, verify_inputs, write_json

SOURCE = 'src/mechanics_save/20261030_slot_release_abi/native_main_0207f1ec.c'
SOURCE_SHA = 'f9868912879cb190b4f9195359506658295be0cee859435d58fd1450ee5853d1'
FIXTURE = 'evidence/application/slot_release_abi_20261030.py'
PROOF = 'evidence/abi/slot-release-main-0207f1ec-20261030.json'
REPORT = 'evidence/matches/mechanics-save-20261030-slot-release-abi.json'


def main():
    inputs = verify_inputs(configuration())
    if sha256(ROOT / SOURCE) != SOURCE_SHA:
        raise ValueError('Frozen explicit-index release source changed')
    subprocess.run([sys.executable, str(ROOT / FIXTURE)], check=True, cwd=ROOT, timeout=180)
    proof = read_json(ROOT / PROOF)
    row = proof['unit'].copy()
    if not proof['exactFreshSourceCompileAndRealLink'] or proof['providerCount'] != 0 or proof['actualNativeAndSourceTopReturns'] != 640:
        raise ValueError('Bounded explicit-index ABI proof changed')
    expected = [(False, True), (True, False), (False, False), (True, True)]
    if [(x['argumentSupplied'], x['accepted']) for x in proof['declarationControls']] != expected:
        raise ValueError('Old/new C call-contract controls differ')
    row.update(row['realLinkSnapshot'])
    for key, digest in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                        ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                        ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        if sha256(ROOT / row[key]) != row[digest]:
            raise ValueError('Current source/object/real-link input differs')
    validation = read_json(ROOT / row['isolatedCallerLinkValidation'])
    if not validation['exactCallerBytes'] or validation['sourceSha256'] != SOURCE_SHA or validation['sourceObjectSha256'] != row['objectSha256']:
        raise ValueError('Current source-selected real-link proof differs')
    row.update({'exactBytes': True, 'outputSha256': row['linkedBinarySha256'],
                'compilerPath': 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe',
                'linked': False, 'oracle': {'report': PROOF, 'reportSha256': sha256(ROOT / PROOF),
                    'actualReturns': 640, 'freshMachines': True, 'providerCount': 0,
                    'supportedDomain': 'Direct indexed entry, empty resource and null nested resource',
                    'unsupportedNonNullResourceReturns': 0}})
    sys.path.insert(0, str(ROOT / 'evidence/application'))
    import predicate_abi_build_20261030 as builder
    builder.ENTRY, builder.LENGTH, builder.NAME = 0x0207F1EC, 104, 'native_main_0207f1ec'
    builder.SOURCE = SOURCE
    bindings = builder.item_bindings()
    deps = [FIXTURE, Path(__file__).name, 'evidence/application/predicate_abi_build_20261030.py',
            'preparation_build_20261029.py', 'link_runtime_unit.py', 'save_link_snapshots.py',
            'config/arm9/symbols.txt', 'src/runtime/main-null01/native_main_0207f1ec.c']
    if verify_inputs(configuration()) != inputs:
        raise ValueError('Original inputs changed during release ABI replay')
    report = {'schemaVersion': 1, 'romSha256': configuration()['romSha256'],
              'matches': [row], 'matchedFunctions': 1, 'matchedBytes': 104,
              'netNewFunctions': 0, 'netNewBytes': 0,
              'nativeSymbols': {k: v['address'] for k, v in bindings.items()},
              'nativeSymbolEntries': bindings,
              'nativeSymbolModules': {k: v['module'] for k, v in bindings.items()},
              'replayDependencies': [{'path': p, 'sha256': sha256(ROOT / p)} for p in deps],
              'replayRequires': ['evidence/matches/main-main-null01.json'],
              'oracle': {'report': PROOF, 'reportSha256': sha256(ROOT / PROOF), 'actualReturns': 640},
              'inputsUnchanged': True, 'wholeLinkedRebuild': False,
              'registrationPerformedByThisScript': False, 'limitations': proof['limitations']}
    write_json(ROOT / REPORT, report)
    print({'matchedBytes': 104, 'newSourceCredit': 0, 'actualReturns': 640})


if __name__ == '__main__':
    main()
