from pathlib import Path
import json
from project import ROOT, read_json, sha256, write_json


PREFIXES = ['src/utility/parallel_wave20261102/' + lane + '/reference-research' for lane in ['fourth', 'fifth']]


def research(name):
    return isinstance(name, str) and any(name.startswith(prefix) for prefix in PREFIXES)


def main():
    workspace_path = ROOT / 'evidence/verification/workspace.json'
    workspace = read_json(workspace_path)
    failures = workspace['sourcePolicy']['failures']
    assert failures and all(research(row['path']) and row['physicalLines'] > 500 and not row['hasComments'] for row in failures)
    assert all(sha256(ROOT / row['path']) == row['sha256'] for row in failures)
    registry = read_json(ROOT / 'recovery.json')
    registered = [dict(report=batch['report'], path=name) for batch in registry['batches'] for name in batch['sourceHashes'] if research(name)]
    frozen, compiler_inputs, metadata, watched, descriptors = [], [], [], {}, []
    lane_root = ROOT / 'evidence/lanes/parallel-wave20261102'
    for path in lane_root.glob('*/ready.json'):
        document = read_json(path)
        watched[path.relative_to(ROOT).as_posix()] = sha256(path)
        frozen.extend(dict(manifest=path.relative_to(ROOT).as_posix(), path=pin['path']) for pin in document.get('files', []) if research(pin['path']))
    for path in lane_root.glob('*/packet-ready-inputs.json'):
        document = read_json(path)
        watched[path.relative_to(ROOT).as_posix()] = sha256(path)
        for pin in document.get('generatorSources', []) + document.get('mandatoryExternalInputs', []):
            if research(pin['path']):
                frozen.append(dict(manifest=path.relative_to(ROOT).as_posix(), path=pin['path']))
        for entry in document.get('entries', []):
            actual = [entry['source']] + [pin['path'] for pin in entry.get('sourceDependencies', [])]
            compiler_inputs.extend(dict(manifest=path.relative_to(ROOT).as_posix(), path=name) for name in actual if research(name))
            metadata.extend(dict(manifest=path.relative_to(ROOT).as_posix(), field='sourceReuseProvenance', **pin) for pin in entry.get('sourceReuseProvenance', []) if research(pin['source']))
    descriptor_paths = list((ROOT / 'provenance').glob('*parallel-wave20261102*.json')) + list(lane_root.glob('*/canonical-packet.json'))
    for path in descriptor_paths:
        document = read_json(path)
        for pin in document.get('frozenInputs', []) if isinstance(document, dict) else []:
            if research(pin['path']):
                descriptors.append(dict(descriptor=path.relative_to(ROOT).as_posix(), path=pin['path']))
    copies = []
    for lane in ['utility-child-fourth', 'utility-child-fifth']:
        proof_path = lane_root / lane / 'copied-root-canonical-bridge-proof.json'
        proof = read_json(proof_path)
        copied = Path(proof['copiedRoot'])
        assert proof['exitCode'] == 0 and proof['canonicalReportFresh'] and proof['sourceAndNativeContractsIdentical'] and proof['staleWorkerAndCanonicalReportsReplaced']
        absent = [str(path) for prefix in PREFIXES for path in (copied / Path(prefix).parent).glob(Path(prefix).name + '*')]
        assert not absent
        descriptor = read_json(lane_root / lane / 'canonical-packet.json')
        canonical_path = copied / descriptor['canonicalReport']
        assert sha256(canonical_path) == proof['canonicalReportSha256']
        canonical = read_json(canonical_path)
        objects = 0
        for row in canonical['matches']:
            assert sha256(copied / row['source']) == row['sourceSha256']
            assert sha256(copied / row['object']) == row['objectSha256']
            actual = row['realLink']
            assert sha256(copied / actual['linkedElf']) == actual['linkedElfSha256'] and sha256(copied / actual['lcf']) == actual['lcfSha256']
            assert sha256((copied / actual['lcf']).parent / 'caller.bin') == row['targetSha256']
            objects += 1
        copies.append(dict(proof=proof_path.relative_to(ROOT).as_posix(), proofSha256=sha256(proof_path),
            copiedRoot=str(copied), functions=objects, originalResearchDirectoriesPresent=False,
            actualFreshObjectAndWholeLinkedCallerHashesVerified=True))
    trees = []
    for prefix in PREFIXES:
        trees.extend(path for path in (ROOT / Path(prefix).parent).glob(Path(prefix).name + '*') if path.is_dir())
    files = [dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path), bytes=len(path.read_bytes()))
        for tree in trees for path in tree.rglob('*') if path.is_file()]
    unchanged = all(sha256(ROOT / name) == digest for name, digest in watched.items())
    passed = not registered and not frozen and not compiler_inputs and not descriptors and unchanged
    result = dict(passed=passed, sourceCredit=0, relocationEligible=passed,
        scope='Read-only generated research placement and runtime dependency audit; no relocation performed',
        originalFailedWorkspaceSha256=sha256(workspace_path), sourcePolicyFailurePaths=failures,
        currentRegistrySha256=sha256(ROOT / 'recovery.json'), registeredBatchesChecked=len(registry['batches']),
        registeredResearchSourcePins=registered, frozenReadyResearchPins=frozen,
        runtimeCompilerResearchInputs=compiler_inputs, frozenDescriptorResearchInputs=descriptors,
        immutableHandoffHashes=watched, immutableHandoffsUnchanged=unchanged,
        historicalMetadataReferences=metadata, historicalReferenceCount=len(metadata),
        historicalPathsMustRemainUnedited=True,
        runtimeReadClosureEvidence=copies,
        producerReadAnalysis='Frozen --verify reads final promoted source/include/compiler/native inputs; researchEvidence and sourceReuseProvenance are copied metadata, and selected/promote research branches are not executed',
        relocationRequirements=['Byte-preserving move only these unregistered generated research trees',
            'Record every original path, new generated path, size and content hash',
            'Retain failed workspace receipt/log and immutable historical provenance JSON bytes',
            'Do not move final promoted source/includes or edit frozen producers/registries',
            'Re-run failed workspace gate and preserve all prior passed gate hashes'],
        eligibleResearchFiles=files, researchFiles=len(files), generatorSha256=sha256(Path(__file__)))
    output = ROOT / 'evidence/verification/parallel-wave20261102/research-placement-dependency-audit.json'
    assert not output.exists()
    write_json(output, result)
    print(json.dumps(dict(passed=passed, failurePaths=len(failures), registeredPins=len(registered), readyPins=len(frozen),
        compilerInputs=len(compiler_inputs), descriptorPins=len(descriptors), historicalReferences=len(metadata),
        researchFiles=len(files), copiedRootVerifiedFunctions=sum(row['functions'] for row in copies), sourceCredit=0)))
    if not passed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
