import shutil
import subprocess
import sys
import uuid
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure


def main():
    producer = 'match_http_explicit_interfaces_20261106.py'
    layout_name = 'evidence/lanes/parallel-wave20261106/http-explicit-interfaces/source-layout.json'
    report_name = 'evidence/matches/http-explicit-interfaces-20261106.json'
    layout = read_json(ROOT / layout_name)
    original = read_json(ROOT / report_name)
    files = set(code_closure([producer, *['wave20261105_dwc_http_next_' + p + '_build.py' for p in ['fifth', 'sixth', 'seventh']]]))
    files.update([layout_name, layout['ownershipClaim'], layout['debtReceipt'], layout['qualifiedPrototypeProbe']])
    for packet in ['fifth', 'sixth', 'seventh']:
        inputs = read_json(ROOT / f'evidence/lanes/parallel-wave20261105/dwc-http-next/{packet}/inputs.json')
        for pin in inputs['files']:
            assert sha256(ROOT / pin['path']) == pin['sha256']
            files.add(pin['path'])
    for row in layout['sources']:
        files.add(row['source'])
        files.add(row['oldSource']['path'])
        files.update(pin['path'] for pin in row['headers'] + row['oldHeaders'])
    assert not any(name.startswith('inputs/') or name.endswith(('.o', '.elf')) for name in files)
    directory = ROOT / 'work/w6hi-copy' / uuid.uuid4().hex[:10]
    directory.mkdir(parents=True)
    pins = []
    for name in sorted(files):
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
        assert sha256(target) == sha256(ROOT / name)
        pins.append(dict(path=name, sha256=sha256(target)))
    config = read_json(directory / 'project.json')
    config.update(rom='inputs/missing.nds', save='inputs/missing.sav', deps='deps/native',
                  compiler='tools/mwccarm/mwccarm/2.0/base/mwccarm.exe',
                  linker='tools/mwccarm/mwccarm/2.0/base/mwldarm.exe', license='tools/mwccarm/mwccarm/license.dat')
    write_json(directory / 'project.json', config)
    assert not (directory / 'work').exists() and not (directory / report_name).exists()
    run = subprocess.run([sys.executable, str(directory / producer)], cwd=directory, capture_output=True, timeout=180)
    (directory / 'copied-root-output.txt').write_bytes(run.stdout + run.stderr)
    assert run.returncode == 0, (run.stdout + run.stderr)[-3000:]
    copied = read_json(directory / report_name)
    assert copied['allPassed'] and copied['newByteCredit'] == copied['newFunctionCredit'] == 0
    assert len(copied['matches']) == 5
    for before, after in zip(original['matches'], copied['matches']):
        assert before['sourceSha256'] == after['sourceSha256'] and before['targetSha256'] == after['targetSha256']
        assert before['objectSha256'] != after['objectSha256']
        assert sha256(directory / after['object']) == after['objectSha256']
    expected_objects = {p.relative_to(directory).as_posix(): sha256(p) for p in directory.rglob('*.o')}
    source = directory / layout['sources'][0]['headers'][0]['path']
    raw = source.read_bytes()
    controls = []
    for label in ['missing-canonical-header', 'same-size-canonical-header-edit']:
        if label.startswith('missing'):
            source.unlink()
        else:
            source.write_bytes(bytes([raw[0] ^ 1]) + raw[1:])
        failure = subprocess.run([sys.executable, str(directory / producer)], cwd=directory, capture_output=True, timeout=180)
        assert failure.returncode != 0
        assert expected_objects == {p.relative_to(directory).as_posix(): sha256(p) for p in directory.rglob('*.o')}
        source.write_bytes(raw)
        controls.append(dict(control=label, rejectedBeforeObjectOverwrite=True))
    write_json(ROOT / 'evidence/lanes/parallel-wave20261106/http-explicit-interfaces/copied-root-controls.json',
        dict(passed=True, sourceCredit=0, newByteCredit=0, freshMigratedCallers=5,
             copiedRoot=directory.relative_to(ROOT).as_posix(), originalReportSha256=sha256(ROOT / report_name),
             noRomSaveOrCachedObjectsCopied=True, originalViewsAndExplicitViewsBothFreshlyCompiled=True,
             projectPathRebindingDisclosed=True, copiedInputs=pins, controls=controls,
             generatorSha256=sha256(__file__)))
    print(dict(passed=True, freshMigratedCallers=5, controls=len(controls), newByteCredit=0))


if __name__ == '__main__':
    main()
