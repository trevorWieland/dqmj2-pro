from pathlib import Path
import json
import re
import subprocess
from project import ROOT, read_json, write_json, sha256


def main():
    lane = ROOT / 'evidence/lanes/parallel-wave20261102/main-sdk-third'
    ready_name = (lane / 'ready.json').relative_to(ROOT).as_posix()
    ready = read_json(lane / 'ready.json')
    inputs = read_json(lane / 'inputs.json')
    report = read_json(lane / 'match.json')
    mapping_name = 'evidence/verification/parallel-wave20261102/unselected-sdk-header-packaging.json'
    mapping = read_json(ROOT / mapping_name)
    manifest_name = 'provenance/cohort149-parallel-wave20261102-next-source-files.json'
    manifest = read_json(ROOT / manifest_name)
    package = read_json(ROOT / 'cohort149-parallel-wave20261102-next-package.json')
    spec = read_json(ROOT / 'cohort149-parallel-wave20261102-next-specification.json')
    registry = read_json(ROOT / 'recovery.json')
    captured = read_json(ROOT / 'evidence/verification/cohort149-captured-oracle-closure-20261031.json')
    registered = {name: digest for batch in registry['batches'] for name, digest in batch['sourceHashes'].items()}
    closure = captured['sourceAndEvidenceHashes']
    assert manifest_name not in registered and manifest_name not in closure
    assert sha256(lane / 'ready.json') == mapping['originalReadySha256'] == next(pin['sha256'] for pin in spec['readyPacketInputs'] if pin['path'] == ready_name)
    assert ready_name in package['traces'] and ready_name not in package['extra']
    pins = {pin['path']: pin['sha256'] for pin in ready['files']}
    staged = {pin['path']: pin['sha256'] for pin in manifest['files']}
    assert ready_name not in staged and len(mapping['copies']) == 7
    for row in mapping['copies']:
        assert row['old'].startswith('evidence/lanes/parallel-wave20261102/main-sdk-third/exploration-headers/')
        assert row['new'].startswith('generated/parallel-wave20261102/main-sdk-third-exploration-headers/')
        assert sha256(ROOT / row['old']) == sha256(ROOT / row['new']) == row['sha256'] == pins[row['old']] == staged[row['new']]
        assert row['old'] not in registered and row['old'] not in closure and row['old'] not in staged
    actual = set()
    for entry in inputs['entries']:
        assert not entry.get('explorationHeaderPins')
        actual.add(entry['source'])
        actual.update(pin['path'] for pin in entry['sourceDependencies'])
        assert 'exploration' not in json.dumps(entry.get('compilerFlags', []))
    assert all('exploration' not in json.dumps(entry['compilerFlags']) for entry in report['matches'])
    for name in actual:
        text = (ROOT / name).read_text()
        assert not re.search(r'^\s*#\s*include\s*<', text, re.M)
        assert 'g2d_config.h' not in text and 'exploration-headers' not in text
    assert all(row['old'] not in actual for row in mapping['copies'])
    assert all(sha256(ROOT / name) == digest for name, digest in registered.items())
    receipt = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-149.json')
    assert sha256(ROOT / 'recovery.json') == receipt['sourceRegistrySha256']
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    helpers = ['stage_declared_source_package_v7_20261102.py', 'stage_verified_cohort.py', 'finish_source_package_v14_20261102.py']
    import hashlib
    assert all(hashlib.sha256(subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)).hexdigest() == sha256(ROOT / name) for name in helpers)
    assert "path.startswith('generated/')" in (ROOT / helpers[-1]).read_text()
    result = dict(passed=True, sourceCredit=0, originalReadySha256=sha256(lane / 'ready.json'),
        originalReadyStillPinnedByNativeSpecification=True, originalReadyOpaqueHistoricalLineage=True,
        stagingSourceFilesManifestSha256=sha256(ROOT / manifest_name), stagingManifestIsNotNativeProducerInput=True,
        nativeRegistrySha256=sha256(ROOT / 'recovery.json'), uniqueActualNativeSourcePinsVerified=len(registered),
        immutableThirdSdkCompilerEntries=len(inputs['entries']), actualSourceAndIncludeFiles=len(actual),
        actualCompilerExplorationHeaderInputs=0, diagnosticHeaderCopies=len(mapping['copies']),
        byteIdentityOfOriginalAndGeneratedCopiesVerified=True, capturedClosureRequiresOriginalHeaders=False,
        unchangedStagerAndFinisherCommit=revision, newPolicyOrBypassAdded=False,
        mappingReceipt=mapping_name, mappingReceiptSha256=sha256(ROOT / mapping_name),
        indexMutations=0, stagerOrFinisherInvocations=0, registryMutations=0,
        generatorSha256=sha256(Path(__file__)))
    output = ROOT / 'evidence/verification/parallel-wave20261102/unselected-header-packaging-independent-audit.json'
    assert not output.exists()
    write_json(output, result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
