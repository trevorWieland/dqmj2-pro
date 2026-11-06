import hashlib
import io
import json
from pathlib import Path
import tokenize

ROOT = Path(__file__).resolve().parent
FILES = ['src/utility/lane_20261031_halfword_bytes76/native_utility_child_arm7_main_027e94c8.c',
    'src/utility/lane_20261031_halfword_bytes76/native_utility_child_arm7_main_027e94e8.c',
    'arm7_lane_halfword_bytes76_native_20261031.py', 'arm7_lane_halfword_bytes76_boundaries_20261031.py',
    'match_arm7_lane_child_halfword_bytes76_20261031.py', 'validate_arm7_lane_child_halfword_bytes76_20261031.py',
    'seal_arm7_child_halfword_bytes76_20261031.py',
    'nonmatching/arm7-bulk/20261031/lane-child-halfword-bytes76-final/closure.json',
    'nonmatching/arm7-bulk/20261031/lane-child-halfword-bytes76-final/generator-pins.json',
    'evidence/matches/arm7-lane-child-halfword-bytes76-20261031.json',
    'evidence/verification/arm7-lane-child-halfword-bytes76-controls-20261031.json',
    'evidence/verification/arm7-halfword-bytes76-replay-receipt-20261031.json',
    'evidence/attempts/arm7-child-codec-breadth91-summary-20261031.json',
    'docs/2026-10-31-arm7-child-halfword-byte-helpers76.md']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    report = json.loads((ROOT / FILES[9]).read_text())
    controls = json.loads((ROOT / FILES[10]).read_text())
    if sha(ROOT / FILES[9]) != 'c824a3988a43c78e9d38991a48285118e6ce407a333c49f5111864aebe2c0fb0' or sha(ROOT / FILES[10]) != '3db5b88ede9fa264026ff87d78c2910d7c609b2c5792b0555d00e0a1a9b787c8':
        raise ValueError('Final exact source/native/control replay differs')
    if report['generatorSha256'] != sha(ROOT / FILES[4]) or controls['generatorSha256'] != sha(ROOT / FILES[5]) or len(controls['controls']) != 33 or not controls['allPassed']:
        raise ValueError('Current producer/control source was not fully replayed')
    if (report['actualNativeAndCompiledReturns'], report['matchedInitializedBytes'], report['matchedInstructionBytes'], report['generatedLiteralBytes']) != (5232, 76, 76, 0):
        raise ValueError('Measured exact source/return scope differs')
    if len(report['matches']) != 2 or report['originalDataSourceCredit'] or report['calleeSourceCredit']:
        raise ValueError('Invented source/function/data credit')
    required = {item['path']: item['sha256'] for item in report['generatorSources'] if item['path'] not in FILES}
    required['inputs/game.nds'] = report['romSha256']
    for index, row in enumerate(report['matches']):
        if row['source'] != FILES[index] or row['sourceSha256'] != sha(ROOT / FILES[index]) or not row['realArm7Link']['exactLinkedBytes']:
            raise ValueError('Frozen ordinary C/genuine full-byte link differs')
        required.update({row['compiler']: row['compilerSha256'], row['binary']: row['inputModuleSha256']})
        required[Path(row['realArm7Link']['linkCommand'][0]).relative_to(ROOT).as_posix()] = row['realArm7Link']['linkerSha256']
    for name, expected in required.items():
        if sha(ROOT / name) != expected:
            raise ValueError('Required existing source/tool/input changed: ' + name)
    files = []
    for name in FILES:
        path = ROOT / name
        if not path.is_file() or name.startswith(('work/', 'inputs/', 'tools/')):
            raise ValueError('Absent/generated transport path')
        if path.suffix == '.py':
            text = path.read_text()
            if len(text.splitlines()) > 500 or any(token.type == tokenize.COMMENT for token in tokenize.generate_tokens(io.StringIO(text).readline)):
                raise ValueError('Authored source policy differs')
        files.append({'path': name, 'sha256': sha(path), 'bytes': path.stat().st_size})
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': sha(Path(__file__)), 'files': files,
        'requiredExistingFiles': [{'path': name, 'sha256': value} for name, value in sorted(required.items())],
        'qualifiedCallers': [{key: row[key] for key in ('program', 'processor', 'module', 'mode', 'address', 'bytes')} for row in report['matches']],
        'sourceFunctionsReady': 2, 'sourceInitializedBytesReady': 76, 'sourceInstructionBytesReady': 76,
        'generatedLiteralBytes': 0, 'originalDataOrCalleeSourceCredit': 0, 'acceptedSourceCreditBeforeIntegrator': 0,
        'cachedGeneratedProductsTransported': False, 'sharedRegistryConfigLedgerPreferenceEdits': False,
        'reproduce': ['match_arm7_lane_child_halfword_bytes76_20261031.py'],
        'controlsReproduce': ['validate_arm7_lane_child_halfword_bytes76_20261031.py'], 'allPassed': True}
    output = ROOT / 'provenance/arm7-child-halfword-bytes76-handoff-20261031.json'
    output.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'manifest': output.relative_to(ROOT).as_posix(), 'sha256': sha(output), 'files': len(files), 'existingInputs': len(required)}), flush=True)


if __name__ == '__main__':
    main()
