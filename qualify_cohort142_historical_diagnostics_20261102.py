import ast
import hashlib
import subprocess
from project import ROOT, read_json, write_json, sha256


def main():
    log = ROOT / 'logs/integration/cohort142-expanded-v17-continuation-04-20261101.txt'
    findings = ast.literal_eval(log.read_text().rsplit('AssertionError: ', 1)[1].strip())
    failed = [row for row in findings if not row['classified']]
    expected = {
        'nonmatching/save-core/20261031-progression-controller-rejected-locals/native_main_020c61a4.c',
        'nonmatching/save-core/20261031-progression-dependencies/native_main_020698f4.c',
        'nonmatching/save-core/20261031-progression-dependencies/native_main_020c7170.c',
    }
    assert {row['path'] for row in failed} == expected
    commit = '8092f1bd7ce2d5e9ad986afce878c273d12fc937'
    rows = []
    for row in failed:
        path = ROOT / row['path']
        blob = subprocess.run(['git', 'show', commit + ':' + row['path']], cwd=ROOT,
            capture_output=True, check=True).stdout
        assert blob == path.read_bytes()
        assert hashlib.sha256(blob).hexdigest() == row['sha256'] == sha256(path)
        rows.append(dict(path=row['path'], sha256=row['sha256']))
    manifest = 'provenance/save-core-large406-historical-diagnostics-supplement-20261102.json'
    write_json(ROOT / manifest, dict(sourceCredit=0, newFunctions=0, newBytes=0,
        workerCommit=commit, parentManifest='evidence/lanes/save-core/large406-ready-20261102.json',
        parentManifestSha256=sha256(ROOT / 'evidence/lanes/save-core/large406-ready-20261102.json'),
        reason='Three unchanged worker Git inputs required by archived research; no reconstructed-source adoption',
        files=rows, originalWorkerBlobsIndependentlyVerified=True))
    configuration = ROOT / 'cohort142-arm7-mlme-and-descriptor-migrations-package-20261102.json'
    old_hash = sha256(configuration)
    package = read_json(configuration)
    assert manifest not in package['manifests']
    package['manifests'].append(manifest)
    receipt = 'evidence/attempts/cohort142-historical-diagnostics-packaging-refusal-20261102.json'
    package['extra'].extend([__file__.split('\\')[-1], receipt,
        'docs/2026-11-02-cohort142-historical-diagnostics-packaging.md'])
    write_json(configuration, package)
    write_json(ROOT / receipt, dict(sourceCredit=0, refusalLog=log.relative_to(ROOT).as_posix(),
        refusalLogSha256=sha256(log), originalPackageSha256=old_hash,
        supplementedPackageSha256=sha256(configuration), findings=failed,
        fullBuildAndRegressionsPassedBeforePackaging=True,
        sourceRegistryOrPreferredSourceChanges=False, frozenWorkerInputsModified=False,
        supplementation='Exact existing three worker Git blobs explicitly declared as zero-credit nonmatching diagnostics'))
    print(dict(verifiedHistoricalDiagnostics=len(rows), sourceCredit=0, registryMutated=False))


if __name__ == '__main__':
    main()
