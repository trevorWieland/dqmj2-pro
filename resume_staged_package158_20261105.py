import hashlib
import subprocess
from concurrent.futures import ThreadPoolExecutor
from project import ROOT, read_json, write_json, sha256


def main():
    folder = ROOT / 'evidence/attempts/cohort158-tooling-eof-20261105'
    repair = read_json(folder / 'repair.json')
    captured_name = 'evidence/verification/cohort158-captured-oracle-closure-20261031.json'
    assert repair['passed'] and repair['pythonAstUnchanged'] and repair['ownedUnfrozenToolingOnly']
    assert sha256(ROOT / captured_name) == repair['originalCapturedClosureSha256']
    assert sha256(folder / 'cohort158-stage-20261101.txt') == repair['originalStageLogSha256']
    assert sha256(ROOT / 'evidence/verification/cohort158-validation-driver.json') == repair['originalValidationDriverSha256']
    driver = read_json(ROOT / 'evidence/verification/cohort158-validation-driver.json')
    assert driver['state'] == 'build-and-regression-checks-passed'
    assert len(driver['steps']) == 16 and all(r['exitCode'] == 0 or r.get('externalApplicationSnapshotDifferences') is True for r in driver['steps'])
    assert sha256(ROOT / repair['path']) == repair['newSha256']
    captured = read_json(ROOT / captured_name)
    assert not captured['missingRequiredPaths'] and repair['path'] not in captured['sourceAndEvidenceHashes']
    assert sha256(ROOT / 'recovery.json') == captured['registrySha256'] == driver['sourceRegistrySha256']

    def current(item):
        name, digest = item
        assert sha256(ROOT / name) == digest, name
        return name

    with ThreadPoolExecutor(max_workers=8) as executor:
        checked = list(executor.map(current, captured['sourceAndEvidenceHashes'].items()))
    names = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'], cwd=ROOT).decode().split('\0')
    names = sorted(n for n in names if n)
    query = ''.join(':' + name + '\n' for name in names).encode()
    output = subprocess.run(['git', 'cat-file', '--batch'], cwd=ROOT, input=query, capture_output=True, check=True).stdout
    cursor = 0
    for name in names:
        end = output.index(b'\n', cursor)
        header = output[cursor:end].decode().split()
        assert len(header) == 3 and header[1] == 'blob', name
        length, cursor = int(header[2]), end + 1
        body, cursor = output[cursor:cursor + length], cursor + length + 1
        assert body == (ROOT / name).read_bytes(), name
    assert cursor == len(output)
    receipt = 'evidence/verification/cohort158-staged-package-resume-20261105.json'
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, unchangedCapturedPaths=len(checked),
        unchangedStagedFiles=len(names), originalStageTraversalRetained=True, allSixteenOriginalStagesRetained=True,
        onlyChange=repair, originalCaptureSha256=repair['originalCapturedClosureSha256'],
        originalStageLogSha256=repair['originalStageLogSha256'], generatorSha256=sha256(__file__),
        stagedPathListSha256=hashlib.sha256('\0'.join(names).encode()).hexdigest()))
    extras = [receipt, 'resume_staged_package158_20261105.py', *[p.relative_to(ROOT).as_posix() for p in folder.iterdir() if p.name != 'cohort158-whitespace-20261101.txt']]
    subprocess.run(['git', 'add', '--', *extras], cwd=ROOT, check=True)
    print(dict(passed=True, capturedPaths=len(checked), stagedFiles=len(names), originalTraversalRetained=True))


if __name__ == '__main__':
    main()
