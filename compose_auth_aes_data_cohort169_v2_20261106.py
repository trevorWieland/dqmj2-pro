import hashlib
import json
from project import ROOT, read_json, write_json, sha256
from qualify_child_message_data_additions_20261106 import identity
from compose_auth_character_data_cohort169_v1_20261106 import plan as auth_plan


def plan(cfg, spec, package):
    auth_result = auth_plan(cfg, spec, package)
    membership = hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest()
    ready_name = 'evidence/lanes/parallel-wave20261106/aes-table-data/ready.json'
    assert sha256(ROOT / ready_name) == '80871400de636018370444022f2e7bc3f4adf6d4d890905631559033d8be2d8c'
    ready = read_json(ROOT / ready_name)
    assert ready['functionCount'] == 0 and ready['dataObjects'] == ready['freshCopiedRootObjects'] == 10
    assert ready['initializedBytes'] == ready['typedConstantDataBytes'] == 10240
    assert ready['actualFreshSourceGenerationCompilationAndGenuineLinkReplay'] and ready['noOldWorkObjectsRequired']
    assert ready['all13ExistingNativeAliasesPreserved'] and ready['ambiguousQualifiersAndMainPluralReferencesUnchanged']
    assert ready['genuineWrongCObjects'] == 8 and ready['copiedRootTamperControls'] == 7
    assert ready['semanticMathSchemaControls'] == 50 and ready['namespaceTypeExtentControls'] == 8
    assert ready['threeInteriorViewControls'] == 15 and ready['actualWrongWidthHeaderCompileRejected']
    assert ready['privateIntegrationNegativeControls'] == 16 and ready['privateEarlierSelectedFunctionsPreserved'] == 11247
    for field in ['executableBytes', 'bssBytes', 'gapBytes', 'interiorViewExtraBytes', 'interiorViewExtraObjects']:
        assert ready[field] == 0
    for pin in [ready['canonicalDescriptor'], ready['additionalQualifierSourceManifest'], ready['dataAdditionQualifier'], *ready['files']]:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    assert sha256(ROOT / ready['sourceManifest']) == ready['sourceManifestSha256']
    claim_name = 'evidence/lanes/parallel-wave20261106/aes-table-data/data-claim.json'
    assert sha256(ROOT / claim_name) == '366bfb04f9d8b3e92ae1e2d54b90c3699d13fb57d57654d4e596cb71803a2694'
    claim = {identity(row): row for row in read_json(ROOT / claim_name)['claimedStorage']}
    report = read_json(ROOT / ready['report'])
    assert report['functionMatched'] == 0 and report['functionMatches'] == []
    assert report['allWholeTablesFreshlyGeneratedCompiledAndGenuinelyLinked'] and report['noOldWorkObjectsOrLinksRequired']
    assert report['allClosedCompilerInputGuardsPassed'] and report['allOriginalAmbiguousQualifiersAndPluralOverlayReferencesUnchanged']
    assert report['compilerSourceSection'] == report['nativePlacementSection'] == '.rodata' and not report['sectionRetargetingRequired']
    assert report['interiorViewExtraBytes'] == report['interiorViewExtraObjects'] == 0
    clarification = read_json(ROOT / 'evidence/lanes/parallel-wave20261106/structured-table-read-only/aes-interior-views-and-placement.json')
    assert {name: int(address, 0) for name, address in report['dataAliases'].items()} == {
        row['name']: row['address'] for row in clarification['allNormalAndAmbiguousRecordsInWholeTableUnion']}
    rows = report['dataMatches']
    assert len(rows) == len(claim) == 10 and report['dataMatchedBytes'] == 10240
    assert {identity(row) for row in rows} == set(claim)
    occupied = [((row.get('program') or '', row['processor'], row['module']), int(row['address'], 0),
        int(row['address'], 0) + row['bytes']) for row in [*spec['expectedAdditions'], *spec['expectedDataAdditions']]]
    for row in rows:
        key = identity(row)
        assert key[:4] == ('', 'arm9', 'ov006', 'data') and row['mode'] == 'data' and row['exactBytes']
        assert row['bytes'] == claim[key]['bytes'] == row['initializedBytes'] == 1024
        assert row['elementType'] == 'u32' and row['elementCount'] == 256
        assert row['targetSha256'] == row['outputSha256'] == claim[key]['targetSha256']
        assert row['semanticSource'] == claim[key]['semanticSource']
        assert row['semanticSourceSha256'] == claim[key]['semanticSourceSha256']
        assert row['section'] == row['targetSection'] == '.rodata'
        assert all(row[field] == 0 for field in ['ordinaryFunctionCredit', 'executableSectionBytes',
            'allocatedZeroFillBytes', 'encodedAssetBytes', 'measuredZeroAlignmentBytes', 'interiorViewExtraBytes'])
        assert all(sha256(ROOT / row[field]) == row[field + 'Sha256'] for field in ['source', 'object'])
        assert not any(scope == key[:3] and max(key[4], a) < min(key[4] + row['bytes'], b) for scope, a, b in occupied)
        occupied.append((key[:3], key[4], key[4] + row['bytes']))
        spec['expectedDataAdditions'].append({field: row[field] for field in ['program', 'processor', 'module', 'mode', 'kind', 'address', 'bytes']})
    assert len(spec['expectedDataAdditions']) == 112 and sum(row['bytes'] for row in spec['expectedDataAdditions']) == 11671
    spec['packets'].append(dict(report=ready['report'], producer=ready['producer'], directProducer=False))
    extras = [ready_name, claim_name, ready['sourceManifest'], ready['canonicalDescriptor']['path'],
        ready['additionalQualifierSourceManifest']['path'], 'compose_auth_aes_data_cohort169_v2_20261106.py',
        'qualify_auth_aes_data_additions_v1_20261106.py', 'qualify_auth_aes_data_composition_v1_20261106.py',
        'prepare_source_data_cohort_v12_20261106.py', 'audit_character_storage_all_symbol_qualifiers_v1_20261106.py',
        'evidence/verification/cohort169-auth-aes-data-composition-20261106.json',
        'evidence/verification/cohort169-auth-aes-data-composition-qualification-v1-20261106.json',
        'evidence/verification/auth-aes-data-preparer-v12-routing-qualification-20261106.json',
        'evidence/verification/character-storage-all-symbol-qualifiers-audit-20261106.json',
        *[pin['path'] for pin in ready['files']]]
    package['manifests'] = list(dict.fromkeys([*package['manifests'], ready['sourceManifest'], ready['additionalQualifierSourceManifest']['path']]))
    package['extra'] = list(dict.fromkeys([*package['extra'], *extras]))
    cfg['composedInitializedDataReadys'] = [cfg.pop('composedInitializedDataReady'),
        dict(path=ready_name, sha256=sha256(ROOT / ready_name), objects=10, bytes=10240)]
    assert hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest() == membership
    return auth_result, dict(passed=True, sourceCredit=0, functions=auth_result['functions'],
        functionBytes=auth_result['functionBytes'], initializedDataObjects=112, initializedDataBytes=11671,
        totalCandidateBytes=auth_result['functionBytes'] + 11671, ordinaryMembershipSha256=membership,
        originalAuthCompositionGuardsUnchanged=True, bothFullFreshProducersRequired=True,
        interiorViewExtraBytes=0, unresolvedPluralOverlayReferencesPreserved=True, generatorSha256=sha256(__file__))


def main():
    names = ['provenance/parallel-wave20261105-n-packets.json', 'cohort169-parallel-wave20261105-n-specification.json',
             'cohort169-parallel-wave20261105-n-package.json']
    documents = [read_json(ROOT / name) for name in names]
    baseline = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json']}
    auth_result, result = plan(*documents)
    archive = 'evidence/attempts/cohort169-auth-aes-data-composition-20261106/verbatim-inputs.json'
    assert not (ROOT / archive).exists()
    write_json(ROOT / archive, dict(sourceCredit=0, files=[dict(path=name, sha256=sha256(ROOT / name),
        text=(ROOT / name).read_text(encoding='utf-8')) for name in names]))
    documents[2]['extra'].append(archive)
    assert all(sha256(ROOT / name) == digest for name, digest in baseline.items())
    for name, document in zip(names, documents):
        write_json(ROOT / name, document)
    write_json(ROOT / 'evidence/verification/cohort169-auth-data-composition-20261106.json', auth_result)
    write_json(ROOT / 'evidence/verification/cohort169-auth-aes-data-composition-20261106.json', result)
    print(result)


if __name__ == '__main__':
    main()
