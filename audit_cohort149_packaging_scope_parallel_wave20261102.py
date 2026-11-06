from pathlib import Path
import hashlib
import json
import subprocess
from project import ROOT, read_json, write_json, sha256


def main():
    package_path = ROOT / 'cohort149-parallel-wave20261102-next-package.json'
    package = read_json(package_path)
    opaque = {'evidence/verification/parallel-wave20261102/research-placement-dependency-audit.json',
        'evidence/attempts/cohort149-source-policy-research-placement-20261102/evidence/verification/workspace.json',
        'evidence/lanes/parallel-wave20261102/generated-research-placement/relocation-receipt.json'}
    assert set(package['traces']) == opaque and not opaque.intersection(package['extra'])
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    helpers = ['stage_declared_source_package_v7_20261102.py', 'stage_verified_cohort.py', 'oracle_source_closure_20261031.py']
    for name in helpers:
        committed = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
        assert hashlib.sha256(committed).hexdigest() == sha256(ROOT / name)
    stage = (ROOT / helpers[0]).read_text()
    assert "staged_paths = sorted(declared | set(configuration.get('traces', [])))" in stage
    assert "*configuration['extra']" in stage and "extra.extend([*declared, dependency_path, diagnostic_path])" in stage
    registry_path = ROOT / 'recovery.json'
    registry_sha = sha256(registry_path)
    registry = read_json(registry_path)
    receipt = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-149.json')
    assert registry_sha == receipt['sourceRegistrySha256']
    pins = {}
    references = 0
    for batch in registry['batches']:
        for name, digest in batch['sourceHashes'].items():
            assert name not in pins or pins[name] == digest
            pins[name] = digest
            references += 1
    assert all(sha256(ROOT / name) == digest for name, digest in pins.items())
    audit = read_json(ROOT / 'evidence/verification/parallel-wave20261102/research-placement-dependency-audit.json')
    original = read_json(ROOT / 'evidence/verification/parallel-wave20261102/research-relocation-root-verification.json')
    before = {row['path']: row for row in audit['eligibleResearchFiles']}
    assert audit['relocationEligible'] and original['passed'] and not original['matchedSourceInputsChanged']
    moved = {}
    for row in original['moves']:
        assert row['old'] in before and row['sha256'] == before[row['old']]['sha256']
        assert row['old'] not in pins and row['new'] not in pins
        assert not (ROOT / row['old']).exists() and sha256(ROOT / row['new']) == row['sha256']
        assert len((ROOT / row['new']).read_bytes()) == row['bytes']
        moved[row['old']] = row
    assert all(row['path'] in moved for row in audit['sourcePolicyFailurePaths'])
    archived = next(name for name in opaque if name.endswith('/workspace.json'))
    assert sha256(ROOT / archived) == audit['originalFailedWorkspaceSha256']
    assert sha256(registry_path) == registry_sha
    result = dict(passed=True, sourceCredit=0, packageSha256=sha256(package_path), helperCommit=revision,
        opaqueDiagnostics=[dict(artifact=name, sha256=sha256(ROOT / name), role='diagnostic-only opaque JSON; no recursive source dependency interpretation') for name in sorted(opaque)],
        onlyThreeOpaqueDiagnosticArtifacts=True, diagnosticArtifactsAbsentFromRecursiveExtras=True,
        unchangedStagingHelperHashes={name: sha256(ROOT / name) for name in helpers},
        frozenRegistrySha256=registry_sha, registeredBatches=len(registry['batches']),
        actualSourcePinReferencesVerified=references, uniqueActualSourcePinHashesVerified=len(pins),
        nativeProducerInputsUnchanged=True, bytePreservedResearchMoves=len(moved),
        all38FailedHeadersPreservedUnderGenerated=True, broadUnselectedResearchNeededForRuntime=False,
        inputClosureEvidence='Existing independent fourth/fifth copied roots contain no research trees and genuinely replayed all44 objects and full linked callers; dependency audit records physical hashes',
        indexMutations=0, stagerInvocations=0, registryMutations=0,
        generatorSha256=sha256(Path(__file__)))
    output = ROOT / 'evidence/verification/parallel-wave20261102/cohort149-packaging-scope-audit.json'
    assert not output.exists()
    write_json(output, result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
