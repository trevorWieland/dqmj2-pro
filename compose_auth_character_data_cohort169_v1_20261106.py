import hashlib
import json
from project import ROOT, read_json, write_json, sha256
from qualify_child_message_data_additions_20261106 import identity


def plan(cfg, spec, package):
    assert cfg['cohort'] == spec['cohort'] == package['cohort'] == 169
    assert cfg['previousAcceptedCohort'] == spec['previousAcceptedCohort'] == 168
    assert cfg['membershipFrozen'] and not spec['migrations'] and not spec.get('expectedDataAdditions')
    functions = len(spec['expectedAdditions'])
    function_bytes = sum(r['bytes'] for r in spec['expectedAdditions'])
    assert functions and functions == cfg['frozenOrdinaryMembership']['functions']
    assert function_bytes == cfg['frozenOrdinaryMembership']['ordinaryCBytes']
    membership = hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest()
    assert membership == cfg['frozenOrdinaryMembership']['membershipSha256']
    ready_name = 'evidence/lanes/parallel-wave20261106/auth-character-data/ready.json'
    assert sha256(ROOT / ready_name) == '68efcd298eb48e69b59b9a82131d9f20dd465e4a07cc6f7a41b64149838912ec'
    ready = read_json(ROOT / ready_name)
    assert ready['dataObjects'] == ready['freshCopiedRootObjects'] == 102 and ready['initializedBytes'] == 1431
    assert ready['actualFreshSourceGenerationCompilationAndGenuineLinkReplay'] and ready['noOldWorkObjectsRequired']
    assert ready['configuredCallerPointerWitnessesVerifiedForAll102Objects']
    assert ready['privateIntegrationNegativeControls'] == 14 and ready['copiedRootTamperControls'] == 5
    for pin in [ready['canonicalDescriptor'], ready['additionalQualifierSourceManifest'], *ready['files']]:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    assert sha256(ROOT / ready['sourceManifest']) == ready['sourceManifestSha256']
    claim_name = 'evidence/lanes/parallel-wave20261106/auth-character-data/data-claim.json'
    assert sha256(ROOT / claim_name) == '02be137cee4d5da3d0311cd4c62335d1192d29f1ed1fd672d481eb892b001ed4'
    claim = {identity(r): r for r in read_json(ROOT / claim_name)['claimedStorage']}
    report = read_json(ROOT / ready['report'])
    assert report['functionMatched'] == 0 and report['functionMatches'] == []
    assert report['allObjectsFreshlyGeneratedCompiledAndGenuinelyLinked'] and report['noOldObjectsOrLinksRequired']
    assert report['allConfiguredCallerPointerWitnessesVerified'] and report['deferredUrlsExcluded']
    rows = report['dataMatches']
    assert len(rows) == len(claim) == 102 and report['dataMatchedBytes'] == 1431
    assert {identity(r) for r in rows} == set(claim)
    occupied = [((r.get('program') or '', r['processor'], r['module']), int(r['address'], 0),
                 int(r['address'], 0) + r['bytes']) for r in spec['expectedAdditions']]
    expected = []
    for row in rows:
        key = identity(row)
        assert key[:4] == ('', 'arm9', 'main', 'data') and row['mode'] == 'data' and row['exactBytes']
        assert row['bytes'] == claim[key]['bytes'] and row['targetSha256'] == row['outputSha256'] == claim[key]['targetSha256']
        assert row['semanticSource'] == claim[key]['semanticSource']
        assert row['semanticSourceSha256'] == claim[key]['semanticSourceSha256']
        assert all(row[k] == 0 for k in ['ordinaryFunctionCredit', 'executableSectionBytes', 'allocatedZeroFillBytes', 'encodedAssetBytes', 'measuredZeroAlignmentBytes'])
        for label in ['source', 'object']:
            assert sha256(ROOT / row[label]) == row[label + 'Sha256']
        assert not any(scope == key[:3] and max(key[4], a) < min(key[4] + row['bytes'], b) for scope, a, b in occupied)
        occupied.append((key[:3], key[4], key[4] + row['bytes']))
        expected.append({k: row[k] for k in ['program', 'processor', 'module', 'mode', 'kind', 'address', 'bytes']})
    spec['expectedDataAdditions'] = expected
    spec['dataOnlyCohort'] = False
    spec['packets'].append(dict(report=ready['report'], producer=ready['producer'], directProducer=False))
    receipt = 'evidence/verification/cohort169-auth-data-composition-20261106.json'
    extras = [ready_name, claim_name, ready['sourceManifest'], ready['canonicalDescriptor']['path'],
              ready['additionalQualifierSourceManifest']['path'], receipt,
              'compose_auth_character_data_cohort169_v1_20261106.py', *[p['path'] for p in ready['files']]]
    package['manifests'] = list(dict.fromkeys([*package['manifests'], ready['sourceManifest'], ready['additionalQualifierSourceManifest']['path']]))
    package['extra'] = list(dict.fromkeys([*package['extra'], *extras]))
    cfg['composedInitializedDataReady'] = dict(path=ready_name, sha256=sha256(ROOT / ready_name), objects=102, bytes=1431)
    assert hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest() == membership
    return dict(passed=True, sourceCredit=0, functions=functions, functionBytes=function_bytes,
        initializedDataObjects=102, initializedDataBytes=1431, totalCandidateBytes=function_bytes + 1431,
        ordinaryMembershipSha256=membership, allOriginalFunctionAndTypedDataGuardsRequired=True,
        fullFreshSourceReplayProducerRequired=True, generatorSha256=sha256(__file__))


def main():
    names = ['provenance/parallel-wave20261105-n-packets.json',
             'cohort169-parallel-wave20261105-n-specification.json', 'cohort169-parallel-wave20261105-n-package.json']
    cfg, spec, package = [read_json(ROOT / n) for n in names]
    unchanged = {n: sha256(ROOT / n) for n in ['recovery.json', 'source-preferences.json']}
    result = plan(cfg, spec, package)
    archive = 'evidence/attempts/cohort169-auth-data-composition-20261106/verbatim-inputs.json'
    assert not (ROOT / archive).exists()
    write_json(ROOT / archive, dict(sourceCredit=0, files=[dict(path=n, sha256=sha256(ROOT / n),
        text=(ROOT / n).read_text(encoding='utf-8')) for n in names]))
    package['extra'].append(archive)
    assert all(sha256(ROOT / n) == h for n, h in unchanged.items())
    for name, document in zip(names, [cfg, spec, package]):
        write_json(ROOT / name, document)
    write_json(ROOT / 'evidence/verification/cohort169-auth-data-composition-20261106.json', result)
    print(result)


if __name__ == '__main__':
    main()
