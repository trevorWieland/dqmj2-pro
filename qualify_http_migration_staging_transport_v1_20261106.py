import copy
from project import ROOT, read_json, write_json, sha256

PINS = {
    'http-explicit-interfaces': 'fbbae4eac9a2d3ef7f25fa00b91f7a6fc7acc9711bb09a337b360a71b2357b71',
    'http-explicit-strncpy': 'db856f3b7ce80b967ec2e7af43e92903840a20176fd7574311f746b94b983eb5',
}
NATIVE = dict(path='extract/arm9/arm9.bin', sha256='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f')
EXCLUDED = {'extract', 'work', 'build', 'logs', '.git', 'asm'}


def authored_projection(document):
    assert document['sourceCredit'] == 0
    rows = document['files']
    assert len({r['path'] for r in rows}) == len(rows)
    native = [r for r in rows if r['path'].split('/')[0] in EXCLUDED]
    assert native == [NATIVE]
    result = copy.deepcopy(document)
    result['files'] = [r for r in rows if r['path'] != NATIVE['path']]
    result['derivedReferenceInputs'] = [dict(**NATIVE, sourceCredit=0,
        classification='measured-ROM-derived-comparison-image', committedAsAuthoredSource=False)]
    result['noOriginalRomSaveOrCachedObjectsNeeded'] = False
    result['fullCleanSourceOnlyReplayProven'] = False
    assert result['files'] == [r for r in rows if r != NATIVE]
    return result


def main():
    package_name = 'cohort167-parallel-wave20261105-l-package.json'
    cfg_name = 'provenance/parallel-wave20261105-l-packets.json'
    spec_name = 'cohort167-parallel-wave20261105-l-specification.json'
    package, cfg = read_json(ROOT / package_name), read_json(ROOT / cfg_name)
    assert package['cohort'] == cfg['cohort'] == 167
    baseline = {n: sha256(ROOT / n) for n in ['recovery.json', 'source-preferences.json', spec_name]}
    mixed_name = 'evidence/verification/cohort167-mixed-reference-inputs-20261105.json'
    assert read_json(ROOT / mixed_name)['passed']
    assert sha256(ROOT / NATIVE['path']) == NATIVE['sha256']
    archive = 'evidence/attempts/cohort167-native-reference-manifest-staging-20261106/verbatim-inputs.json'
    assert not (ROOT / archive).exists()
    names = [package_name, cfg_name, 'logs/integration/cohort167-stage-20261101.txt',
             'logs/integration/cohort167-expanded-v35-continuation-03-20261101.txt',
             'evidence/verification/cohort167-continuation-driver-v35-20261105.json']
    write_json(ROOT / archive, dict(sourceCredit=0, files=[dict(path=n, sha256=sha256(ROOT / n),
        text=(ROOT / n).read_text(encoding='utf-8')) for n in names]))
    replacements, records, controls = {}, [], []
    for family, expected in PINS.items():
        name = f'evidence/lanes/parallel-wave20261106/{family}/source-files.json'
        assert sha256(ROOT / name) == expected and name in package['manifests']
        original = read_json(ROOT / name)
        assert all(sha256(ROOT / r['path']) == r['sha256'] for r in original['files'])
        normalized = authored_projection(original)
        mutations = []
        m = copy.deepcopy(original); m['files'] = [r for r in m['files'] if r != NATIVE]; mutations.append(('missing-native', m))
        m = copy.deepcopy(original); m['files'].append(NATIVE); mutations.append(('duplicate-native', m))
        m = copy.deepcopy(original); next(r for r in m['files'] if r == NATIVE)['sha256'] = '0' * 64; mutations.append(('wrong-native-sha', m))
        m = copy.deepcopy(original); next(r for r in m['files'] if r == NATIVE)['path'] = 'build/other.bin'; mutations.append(('wrong-native-path', m))
        m = copy.deepcopy(original); m['files'].append(dict(path='work/unapproved.json', sha256='0' * 64)); mutations.append(('extra-excluded-input', m))
        m = copy.deepcopy(original); m['sourceCredit'] = 1; mutations.append(('positive-credit', m))
        for label, mutation in mutations:
            try:
                authored_projection(mutation)
            except AssertionError:
                controls.append(f'{family}:{label}')
            else:
                raise AssertionError(label)
        output = f'evidence/verification/cohort167-{family}-authored-staging-inputs-v1-20261106.json'
        assert not (ROOT / output).exists()
        normalized['originalImmutableManifest'] = dict(path=name, sha256=expected)
        write_json(ROOT / output, normalized)
        replacements[name] = output
        records.append(dict(original=dict(path=name, sha256=expected),
            transport=dict(path=output, sha256=sha256(ROOT / output)),
            originalFiles=len(original['files']), authoredAndDependencyFiles=len(normalized['files']),
            allOtherFileEntriesByteForByteUnchanged=True, derivedReferenceInput=NATIVE))
    package['manifests'] = [replacements.get(n, n) for n in package['manifests']]
    receipt = 'evidence/verification/cohort167-http-migration-staging-transport-v1-qualification-20261106.json'
    extras = [*replacements, *replacements.values(), archive, receipt,
              'qualify_http_migration_staging_transport_v1_20261106.py']
    package['extra'] = list(dict.fromkeys([*package['extra'], *extras]))
    cfg['extra'] = list(dict.fromkeys([*cfg['extra'], *extras]))
    assert all(sha256(ROOT / n) == h for n, h in baseline.items())
    write_json(ROOT / package_name, package)
    write_json(ROOT / cfg_name, cfg)
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, cohort=167, records=records,
        rejectedControls=controls, allOriginalManifestsUnchanged=True,
        sourceRegistryPreferencesSpecificationAndAllRegisteredBytesUnchanged=True,
        unchangedOriginalStagerAndFinisherRequired=True, nativeImageNeverStagedAsSource=True,
        mixedReferenceQualification=dict(path=mixed_name, sha256=sha256(ROOT / mixed_name)),
        unchangedInputs=baseline, generatorSha256=sha256(ROOT / __file__)))
    print(dict(passed=True, manifests=2, rejectedControls=len(controls), sourceCredit=0))


if __name__ == '__main__':
    main()
