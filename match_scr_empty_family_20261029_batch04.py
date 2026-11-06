import hashlib
import json
import shutil
import struct
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/script-source/20261029/batch04/empty-family'
OUTPUT = ROOT / 'evidence/matches/scripts-20261029-empty-family.json'
PINS = {
    'audit_scr_v3_20261029_batch04.py': '08297094d1ce29abec0874dcf1028ba5d71cc519f992c057828fe5a03d2ab824',
    'build_scr_empty_family_20261029.py': '5b2ae9eaa9e576924b2f6c661d10309b8777c906d6811f08f196bf2b9a0ea4ea',
    'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
    'scr_c_compiler_20261029_v2.py': 'e88ddd56f388e97852293942d7f49cc8fab2f89c8bd4d19683c33811de565f2e',
    'scr_c_compiler_20261029_v3.py': '6b26e8a8639ff9cb1b43a37606577dcf80ec0b43aee2d636739c9ee7f6e30c9f',
    'src/scripts/20261029/batch02/before_primary_flag_reset.c': 'c6e2d8d816a96553043687a44c00d98f3c9c3c7d98db68a290c4e8a590e86d6d',
    'src/scripts/20261029/batch02/scr_flags.h': '8f0e2b3942eb2760b8fff0031849b4738c5e16c96cfd27e2e4a269bbddc9f7fe',
    'src/scripts/20261029/batch03/scr_decision.h': '476823583e462d2fc5a90d2d43abc25301a73f4a284550012b9aa3f9bca097c1',
    'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
    'nonmatching/script-source/20261029/native_scr_empty_20261029.py': '6702658043b2fe03e85170a5f5ebfbb8c65b9618a68d3e8fedbe5985e288a30e',
    'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
    'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
}
for path, expected in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
import script_assets_20261029 as assets
import native_scr_empty_20261029 as fixtures
import audit_scr_v3_20261029_batch04 as auditor


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()),
            'bytes': path.stat().st_size}


def compile_all(targets):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [
        ('build_scr_empty_family_20261029.py', 'build_scr_empty_family_20261029.py'),
        ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029.py'),
        ('scr_c_compiler_20261029_v3.py', 'scr_c_compiler_20261029_v3.py'),
        ('src/scripts/20261029/batch02/before_primary_flag_reset.c', 'before_primary_flag_reset.c'),
        ('src/scripts/20261029/batch03/scr_decision.h', 'scr_flags.h'),
    ]
    for source, name in files:
        shutil.copyfile(ROOT / source, directory / name)
    layout = directory / 'targets.json'
    layout.write_text(json.dumps([{'scriptSha256': row['scriptSha256'], 'startPc': row['startPc']}
                                 for row in targets], indent=2) + '\n')
    command = [sys.executable, str(directory / 'build_scr_empty_family_20261029.py'),
               '--source', 'before_primary_flag_reset.c', '--targets', 'targets.json', '--output', 'generated.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=90, check=True)
    compiled = json.loads((directory / 'generated.json').read_text())
    assert compiled['sourceClosure']['sourceSha256'] == PINS['src/scripts/20261029/batch02/before_primary_flag_reset.c']
    assert compiled['sourceClosure']['includeSha256'] == PINS['src/scripts/20261029/batch03/scr_decision.h']
    assert compiled['sourceClosure']['compilerSha256'] == PINS['scr_c_compiler_20261029_v3.py']
    assert compiled['newAuthoredImplementationFamilies'] == 0
    bodies = {(row['scriptSha256'], row['startPc']): bytes.fromhex(row['bodyHex'])
              for row in compiled['compiledInstances']}
    assert len(bodies) == len(targets) == 1109
    closure_id = digest(json.dumps(compiled['sourceClosure'], sort_keys=True, separators=(',', ':')).encode())
    return bodies, {'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
                    'stdout': result.stdout.strip(), 'targets': artifact(layout),
                    'inputClosure': [artifact(directory / name) for unused, name in files],
                    'generatedArtifact': artifact(directory / 'generated.json'), 'build': compiled['sourceClosure'],
                    'sourceClosureId': closure_id,
                    'includeAlias': {'requestedName': 'scr_flags.h',
                        'contentSource': 'src/scripts/20261029/batch03/scr_decision.h',
                        'sha256': PINS['src/scripts/20261029/batch03/scr_decision.h'],
                        'effect': 'Adds an unused getter declaration while preserving Boolean and setter declarations; empty C bytes unchanged'},
                    'originalBytecodeCompilerInput': False}


def main():
    for image, expected in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH),
                            (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH),
                            (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(image) == expected
    WORK.mkdir(parents=True, exist_ok=True)
    audit = auditor.audit()
    assert audit['additionalNonemptyCandidates'] == 0
    targets = audit['newEmptyFunctionInstances']
    bodies, build = compile_all(targets)
    grouped = defaultdict(list)
    for target in targets:
        grouped[target['asset']].append(target)
    total_calls, total_cases, ordinal = 0, 0, 0
    modules, hashes = [], set()
    rom, files = assets.original_files()
    for asset, rows in sorted(grouped.items()):
        data = assets.load(ROOT / asset)
        assert data['scriptSha256'] == rows[0]['scriptSha256']
        raw = (ROOT / asset).read_bytes()
        members = []
        for index in range(assets.u32(raw, 4)):
            offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
            stored = raw[offset:offset + length]
            assert assets.ash(stored) == data['script']
            members.append({'index': index, 'storedOffset': offset, 'storedBytes': length,
                            'storedSha256': digest(stored), 'scriptSha256': digest(data['script'])})
        rebuilt = bytearray(data['script'])
        starts = {row['pc'] for row in data['instructions']}
        cases, ranges = [], []
        for target in sorted(rows, key=lambda value: value['startPc']):
            base = target['startPc']
            body = bodies[(data['scriptSha256'], base)]
            assert base in starts and base + 16 in starts
            assert body == data['code'][base:base + 16]
            assert struct.unpack('<4I', body) == (1036, 12, base + 12, 1026)
            rebuilt[4100 + base:4100 + base + 16] = body
            hashes.add(digest(body))
            ranges.append({'startPc': base, 'endExclusivePc': base + 16, 'bytes': 16, 'sha256': digest(body),
                           'mode': 'SCR', 'vmHostProcessor': 'ARM9', 'scriptSha256': data['scriptSha256'],
                           'sourceClosureId': build['sourceClosureId'], 'emittedBodyHex': body.hex(),
                           'entryAliases': target['entryAliases'], 'externalInteriorEntries': 0,
                           'sharedReturnTailDetected': False, 'sourceImplementationFamily': 'empty-void-SCR-entry',
                           'adjacentUnexecutedBytesSha256': digest(data['code'][base + 16:base + 24]),
                           'adjacentUnexecutedBytesSourceCredit': 0})
        assert bytes(rebuilt) == data['script']
        for target in sorted(rows, key=lambda value: value['startPc']):
            ordinal += 1
            thread, seed = ordinal % 4, 2026103020000 + ordinal
            original = fixtures.execute(data['script'], target, thread, seed)
            recompiled = fixtures.execute(bytes(rebuilt), target, thread, seed)
            assert original == recompiled
            total_calls += original['actualReturningCalls']
            total_cases += 1
            cases.append(original)
        for index, (source_range, case) in enumerate(zip(ranges, cases)):
            assert source_range['startPc'] == case['startPc']
            evidence_hash = digest(json.dumps(case, sort_keys=True, separators=(',', ':')).encode())
            source_range['nativeReturnEvidence'] = {'moduleCaseIndex': index, 'seed': case['seed'],
                'thread': case['thread'], 'actualReturningCalls': case['actualReturningCalls'],
                'originalObservationSha256': evidence_hash, 'rebuiltObservationSha256': evidence_hash,
                'comparisonRequiresAllObservedRegistersStoresAndStates': True}
        fs_name = Path(asset).name
        modules.append({'asset': asset, 'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'],
                        'codeSha256': digest(data['code']), 'entryTableSha256': digest(data['script'][4:4100]),
                        'romFileRange': list(files[fs_name]), 'members': members, 'matchedRanges': ranges,
                        'matchedBytes': len(rows) * 16, 'sourceDefinitionFamily': 'empty-void-SCR-entry',
                        'originalScaffoldingBytes': len(rebuilt) - len(rows) * 16, 'scaffoldingSourceCredit': 0,
                        'rebuiltDecodedImageEqualsOriginal': True, 'wholeImageReconstructed': False,
                        'nativeDifferentialCases': cases})
    assert total_cases == 1109 and len(modules) == 113
    report = {'schemaVersion': 1, 'evidenceClass': 'reused-empty-C-family-source-rebuild-and-native-execution',
              'generator': Path(__file__).relative_to(ROOT).as_posix(), 'generatorSha256': digest(Path(__file__).read_bytes()),
              'reproductionCommand': 'python match_scr_empty_family_20261029_batch04.py', 'romSha256': assets.ROM_HASH,
              'sourceClosure': [{'path': path, 'sha256': expected} for path, expected in PINS.items()],
              'frozenV3ExhaustionAudit': audit, 'sourceOnlyBuild': build, 'modules': modules,
              'sourceDefinitionUsed': 'src/scripts/20261029/batch02/before_primary_flag_reset.c',
              'sourceDefinitionSha256': PINS['src/scripts/20261029/batch02/before_primary_flag_reset.c'],
              'sourceImplementationFamily': 'empty-void-SCR-entry', 'newAuthoredDefinitions': 0,
              'newImplementationFamilies': 0, 'newSubstantiveDecisionLogicBytes': 0,
              'completeFunctionInstances': total_cases, 'qualifiedScriptRangeBytes': total_cases * 16,
              'uniqueImagesWithRecoveredRanges': len(modules), 'distinctEmittedBodyHashes': len(hashes),
              'previouslyAcceptedEmptyInstancesExcluded': 2, 'memberAliasesGiveNoDuplicateCredit': True,
              'actualReturningCallsPerImplementation': total_calls, 'actualReturningCallsTotal': total_calls * 2,
              'freshMachinesPerImplementation': total_cases, 'nativeFunctionStubs': 0,
              'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True,
              'completeImagesRecovered': 0, 'ordinaryNativeExecutableByteCredit': 0, 'postFaultStateUsedForProof': False,
              'wholeRomSourceMatch': False,
              'limitations': ['This reuses one already recovered empty implementation and adds no authored-definition or substantive-logic novelty',
                  'Physical range/instance credit is separate from implementation families and meaningful decisions',
                  'Every new qualified instance executes completely on one rotating selected thread; the shared family was already checked on all four threads and through CALL/RET in batch02',
                  'Known entry/direct-call/fork roots and decoded direct interiors are audited; opaque or computed outside entries remain incomplete',
                  'Adjacent metadata, image headers, other script code, native executables and archive compression remain zero-credit scaffolding',
                  'Only depth-zero per-instance completion is claimed; generic depth-one family behavior is prior separately versioned evidence',
                  'No whole image, scene, story/quest progress, access predicate or encounter renewability is established']}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'report': OUTPUT.relative_to(ROOT).as_posix(), 'instances': total_cases,
                      'qualifiedBytes': total_cases * 16, 'images': len(modules), 'newDefinitions': 0,
                      'actualReturns': total_calls * 2, 'freshMachinesPerImplementation': total_cases}))


if __name__ == '__main__':
    main()
