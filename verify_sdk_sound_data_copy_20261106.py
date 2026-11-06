import json
import shutil
import subprocess
import sys
import uuid
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure


def main():
    producer = 'match_sdk_sound_data_20261106.py'
    report_name = 'evidence/data/sdk-sound-data-20261106.json'
    layout_name = 'src/runtime/parallel_wave20261106/sdk-sound-data/layout.json'
    original = read_json(ROOT / report_name)
    layout = read_json(ROOT / layout_name)
    directory = ROOT / 'work/w5ss' / uuid.uuid4().hex[:10]
    directory.mkdir(parents=True)
    files = set(code_closure([producer])) | {layout_name, 'project.json'}
    for row in layout['assets']:
        files.update([row['semanticSource'], row['binary']])
    files.update(path.relative_to(ROOT).as_posix() for path in (ROOT / 'deps/native/elftools').rglob('*.py'))
    files.update(['tools/mwccarm/mwccarm/2.0/base/mwccarm.exe', 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe',
                  'tools/mwccarm/mwccarm/license.dat'])
    files.update(path.relative_to(ROOT).as_posix() for path in (ROOT / 'tools/mwccarm/mwccarm/2.0/base').glob('*.dll'))
    inputs = []
    for name in sorted(files):
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
        assert sha256(target) == sha256(ROOT / name)
        inputs.append(dict(path=name, sha256=sha256(target)))
    config = read_json(directory / 'project.json')
    config.update(rom='inputs/original.nds', save='inputs/original.sav', deps='deps/native',
                  compiler='tools/mwccarm/mwccarm/2.0/base/mwccarm.exe',
                  linker='tools/mwccarm/mwccarm/2.0/base/mwldarm.exe', license='tools/mwccarm/mwccarm/license.dat')
    write_json(directory / 'project.json', config)
    assert not list(directory.rglob('*.o')) and not list(directory.rglob('*.elf'))
    stale = directory / 'generated/sdk-sound-data/stale.c'
    stale.parent.mkdir(parents=True)
    stale.write_text('stale unselected generated output', encoding='utf-8')
    output = directory / report_name
    write_json(output, dict(staleReport=True))
    result = subprocess.run([sys.executable, str(directory / producer)], cwd=directory, capture_output=True, timeout=120)
    (directory / 'positive-output.txt').write_bytes(result.stdout + result.stderr)
    assert result.returncode == 0, (result.stdout + result.stderr)[-2000:]
    copied = read_json(output)
    assert copied['functionMatched'] == 0 and copied['dataMatchedBytes'] == 3752
    assert len(copied['dataMatches']) == len(original['dataMatches']) == 6
    assert all(a['targetSha256'] == b['targetSha256'] and a['sourceSha256'] == b['sourceSha256'] and
               a['objectSha256'] != b['objectSha256'] for a, b in zip(original['dataMatches'], copied['dataMatches']))
    expected_objects = {path.relative_to(directory).as_posix(): sha256(path) for path in directory.rglob('*.o')}
    controls = []
    original_layout = (directory / layout_name).read_bytes()
    first_source = layout['assets'][0]['semanticSource']
    original_semantic = (directory / first_source).read_bytes()
    for label in ['semantic-tamper', 'missing-semantic', 'wrong-processor', 'wrong-program', 'wrong-module-hash']:
        (directory / layout_name).write_bytes(original_layout)
        (directory / first_source).write_bytes(original_semantic)
        modified = json.loads(original_layout)
        if label == 'semantic-tamper':
            doc = json.loads(original_semantic)
            doc['elements'][0] ^= 1
            write_json(directory / first_source, doc)
            modified['assets'][0]['semanticSourceSha256'] = sha256(directory / first_source)
        elif label == 'missing-semantic':
            (directory / first_source).unlink()
        elif label == 'wrong-processor':
            modified['assets'][0]['processor'] = 'arm7'
        elif label == 'wrong-program':
            modified['assets'][0]['program'] = 'foreign-program'
        else:
            modified['assets'][0]['inputModuleSha256'] = '0' * 64
        write_json(directory / layout_name, modified)
        rejected = subprocess.run([sys.executable, str(directory / producer)], cwd=directory, capture_output=True, timeout=120)
        assert rejected.returncode != 0
        assert expected_objects == {path.relative_to(directory).as_posix(): sha256(path) for path in directory.rglob('*.o')}
        controls.append(dict(control=label, rejectedBeforeObjectOverwrite=True))
    (directory / layout_name).write_bytes(original_layout)
    (directory / first_source).write_bytes(original_semantic)
    write_json(ROOT / 'evidence/lanes/parallel-wave20261106/sdk-sound-data/copied-root-controls.json',
        dict(passed=True, sourceCredit=0, copiedRoot=directory.relative_to(ROOT).as_posix(), freshObjects=6,
             initializedBytes=3752, originalReportSha256=sha256(ROOT / report_name), controls=controls,
             noRomSdkSourcesAdmissionArtifactsOrCachedObjectsCopied=True, copiedInputs=inputs,
             projectPathRebindingDisclosed=True, generatorSha256=sha256(__file__)))
    print(dict(passed=True, freshObjects=6, controls=len(controls), initializedBytes=3752, sourceCredit=0))


if __name__ == '__main__':
    main()
