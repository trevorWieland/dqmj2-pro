import hashlib
import io
import json
from pathlib import Path
import tokenize

ROOT = Path(__file__).resolve().parent
FILES = ['src/utility/lane_20261031_record_check172/native_utility_child_arm7_main_027f5b10.c',
    'nonmatching/arm7-bulk/20261031/lane-child-record-check172-v4/native_utility_child_arm7_main_027f5b10.c',
    'arm7_lane_record_check172_native_20261031.py', 'arm7_lane_record_check172_boundaries_20261031.py',
    'link_arm7_child_record_check172_20261031.py', 'match_arm7_lane_child_record_check172_20261031.py',
    'validate_arm7_lane_child_record_check172_20261031.py', 'seal_arm7_child_record_check172_20261031.py',
    'nonmatching/arm7-bulk/20261031/lane-child-record-check172-final/closure.json',
    'nonmatching/arm7-bulk/20261031/lane-child-record-check172-final/generator-pins.json',
    'evidence/matches/arm7-lane-child-record-check172-20261031.json',
    'evidence/verification/arm7-lane-child-record-check172-controls-20261031.json',
    'evidence/verification/arm7-record-check172-replay-receipt-20261031.json',
    'evidence/attempts/arm7-record-check172-declaration-closure-20261031.json',
    'evidence/attempts/arm7-record-check172-ip-scratch-fixture-correction-20261031.json',
    'evidence/attempts/arm7-child-record-check172-original-link-refusal-20261031.json',
    'docs/2026-10-31-arm7-child-record-check172.md']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    report = json.loads((ROOT / FILES[10]).read_text())
    controls = json.loads((ROOT / FILES[11]).read_text())
    if sha(ROOT / FILES[10]) != 'd5f96592ec2d5839a7d2d0659178e2f62835a5a2b2e282c798caa5bc7f3802cd' or sha(ROOT / FILES[11]) != '6a183e66ce04c8dd4f575d910dd07ace92c98ea84702c7c6aa47a87d5ad683f3':
        raise ValueError('Frozen actual source/native/control replay differs')
    if report['generatorSha256'] != sha(ROOT / FILES[5]) or controls['generatorSha256'] != sha(ROOT / FILES[6]):
        raise ValueError('Current producer/control was not replayed')
    if len(controls['controls']) != 50 or not controls['allPassed']:
        raise ValueError('Required standalone controls missing')
    row = report['matches'][0]
    if (row['program'], row['processor'], row['module'], row['address'], row['mode'], row['bytes']) != ('dwc/utility.bin/move/child.srl', 'arm7', 'utility-child-arm7-main', '0x27f5b10', 'arm', 172):
        raise ValueError('Full qualified source identity differs')
    if row['source'] != FILES[0] or row['sourceSha256'] != sha(ROOT / FILES[0]) or not row['realArm7Link']['exactLinkedBytes']:
        raise ValueError('Complete source-only genuine linkage differs')
    if (report['actualNativeAndCompiledReturns'], report['actualSeparatelyObservedNestedReturns'], report['calleeSourceCredit'], report['originalDataSourceCredit']) != (256, 81152, 0, 0):
        raise ValueError('Own/nested native return scope or zero-credit dependencies differ')
    dependencies = {item['path']: item['sha256'] for item in report['generatorSources'] if item['path'] not in FILES}
    dependencies.update({row['compiler']: row['compilerSha256'], row['binary']: row['inputModuleSha256'], 'inputs/game.nds': report['romSha256']})
    dependencies[Path(row['realArm7Link']['linkCommand'][0]).relative_to(ROOT).as_posix()] = row['realArm7Link']['linkerSha256']
    pointer = json.loads((ROOT / 'evidence/arm7/lane-halfword-runtime-pointer-20261031.json').read_text())
    for namespace in pointer['namespaceInputs']:
        for kind in ('main', 'wram'):
            dependencies[namespace[kind]] = namespace[kind + 'Sha256']
    for name, expected in dependencies.items():
        if sha(ROOT / name) != expected:
            raise ValueError('Required existing source/tool/input changed: ' + name)
    files = []
    for name in FILES:
        path = ROOT / name
        if name.startswith(('work/', 'tools/', 'inputs/')) or not path.is_file():
            raise ValueError('Generated or absent source transport path')
        if path.suffix == '.py':
            text = path.read_text()
            if len(text.splitlines()) > 500 or any(token.type == tokenize.COMMENT for token in tokenize.generate_tokens(io.StringIO(text).readline)):
                raise ValueError('Authored source policy differs')
        files.append({'path': name, 'sha256': sha(path), 'bytes': path.stat().st_size})
    manifest = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': sha(Path(__file__)), 'files': files,
        'requiredExistingFiles': [{'path': name, 'sha256': value} for name, value in sorted(dependencies.items())],
        'qualifiedCaller': {key: row[key] for key in ('program', 'processor', 'module', 'address', 'mode', 'bytes')},
        'sourceFunctionsReady': 1, 'sourceInitializedBytesReady': 172, 'sourceInstructionBytesReady': 164,
        'generatedLiteralBytes': 8, 'originalCalleeSourceCredit': 0, 'externalWordOrTableDataSourceCredit': 0,
        'acceptedSourceCreditBeforeIntegrator': 0, 'cachedGeneratedProductsTransported': False,
        'sharedRegistryConfigLedgerPreferenceEdits': False, 'reproduce': ['match_arm7_lane_child_record_check172_20261031.py'],
        'controlsReproduce': ['validate_arm7_lane_child_record_check172_20261031.py'], 'allPassed': True}
    output = ROOT / 'provenance/arm7-child-record-check172-handoff-20261031.json'
    output.write_text(json.dumps(manifest, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'manifest': output.relative_to(ROOT).as_posix(), 'sha256': sha(output), 'files': len(files), 'existingInputs': len(dependencies)}), flush=True)


if __name__ == '__main__':
    main()
