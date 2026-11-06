import hashlib
import io
import json
from pathlib import Path
import tokenize

ROOT = Path(__file__).resolve().parent
SCOPE = ['arm7_lane_wordpair124_native_20261031.py', 'prove_arm7_child_divide_scope_20261031.py',
    'validate_arm7_child_divide_scope_20261031.py', 'evidence/arm7/lane-child-divide-wordpair-scope-20261031.json',
    'evidence/verification/arm7-child-divide-scope-controls-20261031.json']
CALLER = ['src/utility/lane_20261031_wordpair124/native_utility_child_arm7_main_027f6a48.c',
    'nonmatching/arm7-bulk/20261031/lane-child-wordpair124-v1/native_utility_child_arm7_main_027f6a48.c',
    'arm7_lane_wordpair124_boundaries_20261031.py', 'match_arm7_lane_child_wordpair124_20261031.py',
    'validate_arm7_lane_child_wordpair124_20261031.py', 'seal_arm7_child_wordpair124_20261031.py',
    'nonmatching/arm7-bulk/20261031/lane-child-wordpair124-final/closure.json',
    'nonmatching/arm7-bulk/20261031/lane-child-wordpair124-final/generator-pins.json',
    'evidence/attempts/arm7-wordpair124-declaration-closure-20261031.json',
    'evidence/attempts/arm7-wordpair124-boundary-address-normalization-20261031.json',
    'evidence/matches/arm7-lane-child-wordpair124-20261031.json',
    'evidence/verification/arm7-lane-child-wordpair124-controls-20261031.json',
    'evidence/verification/arm7-wordpair124-replay-receipt-20261031.json',
    'docs/2026-10-31-arm7-child-wordpair124.md']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(names):
    result = []
    for name in names:
        path = ROOT / name
        if name.startswith(('work/', 'tools/', 'inputs/')) or not path.is_file():
            raise ValueError('Non-source transport item')
        if path.suffix == '.py':
            text = path.read_text()
            if len(text.splitlines()) > 500 or any(token.type == tokenize.COMMENT for token in tokenize.generate_tokens(io.StringIO(text).readline)):
                raise ValueError('Authored Python source policy differs')
        result.append({'path': name, 'sha256': sha(path), 'bytes': path.stat().st_size})
    return result


def main():
    report = json.loads((ROOT / CALLER[10]).read_text())
    controls = json.loads((ROOT / CALLER[11]).read_text())
    role = json.loads((ROOT / SCOPE[3]).read_text())
    role_controls = json.loads((ROOT / SCOPE[4]).read_text())
    if sha(ROOT / CALLER[10]) != '5ba35c4897ec05f61a4eb80c77d5e8c60a6558b8fe03f33b83223c574b493698' or sha(ROOT / CALLER[11]) != 'a333e0c0c2b59452ec4f04610c334a3a2dbcc6677e59b2d52656b91115ab2c97':
        raise ValueError('Final complete-caller replay differs')
    if report['generatorSha256'] != sha(ROOT / CALLER[3]) or controls['generatorSha256'] != sha(ROOT / CALLER[4]):
        raise ValueError('Current matcher/control source was not replayed')
    if len(controls['controls']) != 40 or not controls['allPassed'] or len(role_controls['controls']) != 16 or not role_controls['allPassed']:
        raise ValueError('Required caller or zero-credit code-scope guards absent')
    if sha(ROOT / SCOPE[3]) != '9d1951d47676c59ea4b5c8cdae84150f6d169fbbfda92f3c5467435ebf536e7c' or role['sourceOrFunctionBoundaryOrDenominatorCredit'] != 0:
        raise ValueError('Independent original-code role scope or zero credit differs')
    row = report['matches'][0]
    if row['source'] != CALLER[0] or row['sourceSha256'] != sha(ROOT / CALLER[0]) or not row['realArm7Link']['exactLinkedBytes']:
        raise ValueError('Actual source-only genuine complete link differs')
    if (row['program'], row['processor'], row['module'], row['mode'], row['address'], row['bytes']) != ('dwc/utility.bin/move/child.srl', 'arm7', 'utility-child-arm7-main', 'arm', '0x27f6a48', 124):
        raise ValueError('Caller identity differs')
    if report['actualNativeAndCompiledReturns'] != 896 or report['actualSeparatelyObservedNestedReturns'] != 3584 or report['calleeSourceCredit'] != 0:
        raise ValueError('Actual caller versus original-dependency returns/credit differ')
    history = json.loads((ROOT / CALLER[8]).read_text())
    old = history['unchangedAcceptedLowWordConsumer']
    if sha(ROOT / old['path']) != old['sha256']:
        raise ValueError('Accepted pre-existing C declaration changed')
    all_names = set(SCOPE + CALLER)
    required = {item['path']: item['sha256'] for item in report['generatorSources'] if item['path'] not in all_names}
    required.update({row['compiler']: row['compilerSha256'], row['binary']: row['inputModuleSha256'],
        role['inputModule']: role['inputModuleSha256'], 'inputs/game.nds': report['romSha256']})
    required[Path(row['realArm7Link']['linkCommand'][0]).relative_to(ROOT).as_posix()] = row['realArm7Link']['linkerSha256']
    for name, expected in required.items():
        if sha(ROOT / name) != expected:
            raise ValueError('Existing baseline tool/source/input changed: ' + name)
    scope_manifest = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': sha(Path(__file__)),
        'files': files(SCOPE), 'program': row['program'], 'processor': 'arm7', 'module': 'utility-child-arm7-wram',
        'mode': 'arm', 'entry': '0x03805184', 'configuredEntryBytesUnchanged': 8, 'decodedSpanBytes': 484,
        'executedInstructionBytes': 480, 'skippedInstructionBytes': 4, 'newlyConfirmedCodeBytes': 472,
        'sourceCredit': 0, 'functionBoundaryCredit': 0, 'initializedCoverageDenominatorIncrease': 0,
        'reproduce': ['validate_arm7_child_divide_scope_20261031.py'], 'sharedConfigEdits': False, 'allPassed': True}
    scope_path = ROOT / 'provenance/arm7-child-divide-scope-handoff-20261031.json'
    scope_path.write_text(json.dumps(scope_manifest, indent=2, sort_keys=True) + '\n')
    manifest = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': sha(Path(__file__)),
        'files': files(CALLER + SCOPE) + [{'path': scope_path.relative_to(ROOT).as_posix(), 'sha256': sha(scope_path), 'bytes': scope_path.stat().st_size}],
        'requiredExistingFiles': [{'path': name, 'sha256': value} for name, value in sorted(required.items())],
        'separateZeroSourceCreditCodeScopeManifest': {'path': scope_path.relative_to(ROOT).as_posix(), 'sha256': sha(scope_path)},
        'qualifiedCaller': {key: row[key] for key in ('program', 'processor', 'module', 'mode', 'address', 'bytes')},
        'sourceFunctionsReady': 1, 'sourceInitializedBytesReady': 124, 'originalHelperSourceCredit': 0,
        'acceptedSourceCreditBeforeIntegrator': 0, 'cachedGeneratedProductsTransported': False,
        'sharedRegistryConfigLedgerPreferenceEdits': False, 'reproduce': ['match_arm7_lane_child_wordpair124_20261031.py'],
        'controlsReproduce': ['validate_arm7_lane_child_wordpair124_20261031.py'], 'allPassed': True}
    output = ROOT / 'provenance/arm7-child-wordpair124-handoff-20261031.json'
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'callerManifest': output.relative_to(ROOT).as_posix(), 'callerSha256': sha(output),
        'separateScopeManifest': scope_path.relative_to(ROOT).as_posix(), 'scopeSha256': sha(scope_path),
        'files': len(manifest['files']), 'existingInputs': len(required), 'allPassed': True}), flush=True)


if __name__ == '__main__':
    main()
