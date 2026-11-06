import hashlib
import subprocess
from project import ROOT, read_json, write_json, sha256


def main():
    path = 'evidence/application/save_core_record_expand436_fixtures_20261102.py'
    worker = 'adf4d2f49662781db762fb4173edd90d18f4a0df'
    original = 'evidence/lanes/save-core/record-expand438-ready-20261102.json'
    expected = next(r['sha256'] for r in read_json(ROOT / original)['files'] if r['path'] == path)
    blob = subprocess.run(['git', 'show', worker + ':' + path], cwd=ROOT, capture_output=True, check=True).stdout
    assert blob == (ROOT / path).read_bytes() and b'\r\r\n' in blob
    assert hashlib.sha256(blob).hexdigest() == expected == sha256(ROOT / path)
    manifest = 'provenance/save-core-record438-frozen-proof-fixture-20261102.json'
    write_json(ROOT / manifest, dict(sourceCredit=0, newFunctions=0, newBytes=0,
        classification='Immutable Python proof fixture; zero compiled ARM source credit',
        workerCommit=worker, parentManifest=original, parentManifestSha256=sha256(ROOT / original),
        originalWorkerGitBlobVerified=True, normalizationPerformed=False,
        files=[dict(path=path, sha256=expected)]))
    package = ROOT / 'cohort144-textures-record-lookup-and-arm7-20261102-package.json'
    cfg = read_json(package)
    assert manifest not in cfg['manifests']
    cfg['manifests'].append(manifest)
    cfg['preservedResearchReplayInputs'] = [dict(path=path, sha256=expected, pinManifest=manifest,
        workerCommit=worker, sourceCredit=0, reason='unchanged-worker-CRCRLF-research-input')]
    cfg['extra'].append(__file__.split('\\')[-1])
    write_json(package, cfg)
    print(dict(verifiedImmutablePythonFixtures=1, sourceCredit=0, frozenBytesModified=False))


if __name__ == '__main__':
    main()
