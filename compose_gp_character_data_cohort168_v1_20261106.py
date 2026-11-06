import hashlib
import json
from project import ROOT, read_json, write_json, sha256
from qualify_child_message_data_additions_20261106 import identity


def main():
    cfg_name = 'provenance/parallel-wave20261105-m-packets.json'
    spec_name = 'cohort168-parallel-wave20261105-m-specification.json'
    package_name = 'cohort168-parallel-wave20261105-m-package.json'
    cfg, spec, package = [read_json(ROOT / n) for n in [cfg_name, spec_name, package_name]]
    assert cfg['membershipFrozen'] and cfg['cohort'] == spec['cohort'] == 168
    assert cfg['previousAcceptedCohort'] == spec['previousAcceptedCohort'] == 167
    assert not spec['migrations'] and not spec.get('expectedDataAdditions')
    assert len(spec['expectedAdditions']) == 92 and sum(r['bytes'] for r in spec['expectedAdditions']) == 13150
    membership = hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest()
    assert cfg['frozenOrdinaryMembership']['membershipSha256'] == membership
    ready_name = 'evidence/lanes/parallel-wave20261106/gamespy-gp-character-data/full-replay/ready.json'
    assert sha256(ROOT / ready_name) == '0d2d83eff45e976f4fae51a913cdd5ec6fcbffc3cca87e55a520adc1dca14264'
    ready = read_json(ROOT / ready_name)
    assert ready['dataObjects'] == ready['freshCopiedRootObjects'] == 259 and ready['initializedBytes'] == 3696
    assert ready['functionCount'] == ready['executableBytes'] == ready['bssBytes'] == ready['gapBytes'] == 0
    assert ready['actualCompleteSourceGenerationCompilationAndGenuineLinkReplay'] and ready['noOriginalWorkObjectsNeeded']
    assert ready['wholeOriginalAndAdditiveFrozenInputsPreserved'] == 1983
    descriptor = ready['canonicalDescriptor']
    assert sha256(ROOT / descriptor['path']) == descriptor['sha256']
    assert sha256(ROOT / ready['sourceManifest']) == ready['sourceManifestSha256']
    for pin in ready['files']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    claim_name = 'evidence/lanes/parallel-wave20261106/gamespy-gp-character-data/data-claim.json'
    assert sha256(ROOT / claim_name) == '9d9fb10cf08ed3cc5a0fd44b61a40267dbb2e2f5e07b5a02a21c8a32c7b990a6'
    claim = {identity(r): r for r in read_json(ROOT / claim_name)['claimedStorage']}
    report = read_json(ROOT / ready['report'])
    rows = report['dataMatches']
    assert report['functionMatched'] == 0 and report['functionMatches'] == []
    assert len(rows) == len(claim) == 259 and report['dataMatchedBytes'] == 3696
    assert report['gpCharacterFullSourceReplay']['objectsFreshlyCompiledAndGenuinelyLinked'] == 259
    assert report['gpCharacterFullSourceReplay']['noOldObjectOrLinkRequired']
    assert {identity(r) for r in rows} == set(claim)
    occupied = []
    for r in spec['expectedAdditions']:
        occupied.append(((r.get('program') or '', r['processor'], r['module']), int(r['address'], 0), int(r['address'], 0) + r['bytes']))
    expected = []
    for row in rows:
        key = identity(row)
        assert key[:4] == ('', 'arm9', 'main', 'data')
        assert row['mode'] == 'data' and row['exactBytes'] and row['bytes'] == claim[key]['bytes']
        assert row['targetSha256'] == row['outputSha256'] == claim[key]['targetSha256']
        assert row['semanticSource'] == claim[key]['semanticSource']
        assert row['semanticSourceSha256'] == claim[key]['semanticSourceSha256']
        assert all(row[k] == 0 for k in ['ordinaryFunctionCredit', 'executableSectionBytes', 'allocatedZeroFillBytes', 'encodedAssetBytes', 'measuredZeroAlignmentBytes'])
        for label in ['source', 'object']:
            assert sha256(ROOT / row[label]) == row[label + 'Sha256']
        assert not any(scope == key[:3] and max(key[4], a) < min(key[4] + row['bytes'], b) for scope, a, b in occupied)
        occupied.append((key[:3], key[4], key[4] + row['bytes']))
        expected.append({k: row[k] for k in ['program', 'processor', 'module', 'mode', 'kind', 'address', 'bytes']})
    unchanged = {n: sha256(ROOT / n) for n in ['recovery.json', 'source-preferences.json']}
    archive = 'evidence/attempts/cohort168-gp-data-composition-20261106/verbatim-inputs.json'
    assert not (ROOT / archive).exists()
    write_json(ROOT / archive, dict(sourceCredit=0, files=[dict(path=n, sha256=sha256(ROOT / n),
        text=(ROOT / n).read_text(encoding='utf-8')) for n in [cfg_name, spec_name, package_name]]))
    spec['expectedDataAdditions'] = expected
    spec['dataOnlyCohort'] = False
    spec['packets'].append(dict(report=ready['report'], producer=ready['producer'], directProducer=False))
    receipt = 'evidence/verification/cohort168-gp-data-composition-20261106.json'
    extras = [ready_name, claim_name, descriptor['path'], ready['sourceManifest'], archive, receipt,
              'compose_gp_character_data_cohort168_v1_20261106.py', *[p['path'] for p in ready['files']]]
    package['manifests'] = list(dict.fromkeys([*package['manifests'], ready['sourceManifest']]))
    package['extra'] = list(dict.fromkeys([*package['extra'], *extras]))
    cfg['composedInitializedDataReady'] = dict(path=ready_name, sha256=sha256(ROOT / ready_name), objects=259, bytes=3696)
    assert hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest() == membership
    assert all(sha256(ROOT / n) == h for n, h in unchanged.items())
    write_json(ROOT / cfg_name, cfg)
    write_json(ROOT / spec_name, spec)
    write_json(ROOT / package_name, package)
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, functions=92, functionBytes=13150,
        initializedDataObjects=259, initializedDataBytes=3696, totalCandidateBytes=16846,
        originalOrdinaryMembershipSha256=membership, allOriginalFunctionGuardsAndTypedDataQualificationRequired=True,
        fullFreshSourceReplayProducerRequired=True, copiedRootAndWrongDataControlsPassed=True,
        sourceRegistryAndPreferencesUnchanged=True, ready=dict(path=ready_name, sha256=sha256(ROOT / ready_name)),
        specificationSha256=sha256(ROOT / spec_name), packageSha256=sha256(ROOT / package_name),
        generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=92, dataObjects=259, candidateBytes=16846, sourceCredit=0))


if __name__ == '__main__':
    main()
