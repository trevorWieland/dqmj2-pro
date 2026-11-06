from project import ROOT, read_json, write_json, sha256


def main():
    name = 'evidence/lanes/parallel-wave20261105/wcm-manager-next/diagnostic-classification-v2.json'
    classification = read_json(ROOT / name)
    assert classification['sourceCredit'] == 0 and classification['runtimeInputsRemainFullyParsed']
    opaque = {r['path']: r['sha256'] for r in classification['sourceExpansionOpaque']}
    assert len(opaque) == 9 and all(path.endswith('.json') for path in opaque)
    mandatory = {}
    for folder in ['first', 'second']:
        ready_name = f'evidence/lanes/parallel-wave20261105/wcm-manager-next/{folder}/ready.json'
        ready = read_json(ROOT / ready_name)
        mandatory[ready_name] = sha256(ROOT / ready_name)
        descriptor = ready['canonicalDescriptor']
        mandatory[descriptor['path']] = descriptor['sha256']
        for manifest in read_json(ROOT / descriptor['path'])['frozenInputs']:
            mandatory[manifest['path']] = manifest['sha256']
            for item in read_json(ROOT / manifest['path'])['files']:
                if item['path'].endswith('.json'):
                    assert item['path'] not in opaque
                    mandatory[item['path']] = item['sha256']
    assert not mandatory.keys() & opaque.keys()
    for path, expected in {**mandatory, **opaque}.items():
        assert sha256(ROOT / path) == expected
    cfg_name = 'provenance/parallel-wave20261105-m-packets.json'
    package_name = 'cohort168-parallel-wave20261105-m-package.json'
    cfg, package = read_json(ROOT / cfg_name), read_json(ROOT / package_name)
    assert not cfg['membershipFrozen']
    prior = sorted(set(cfg['opaqueMetadata']) & mandatory.keys())
    archive = 'evidence/attempts/cohort168-wcm-source-expansion-policy-v2-20261106/verbatim-inputs.json'
    assert not (ROOT / archive).exists()
    write_json(ROOT / archive, dict(sourceCredit=0, files=[dict(path=n, sha256=sha256(ROOT / n),
        text=(ROOT / n).read_text(encoding='utf-8')) for n in [cfg_name, package_name]]))
    cfg['opaqueMetadata'] = sorted((set(cfg['opaqueMetadata']) | opaque.keys()) - mandatory.keys())
    assert not set(cfg['opaqueMetadata']) & mandatory.keys()
    receipt = 'evidence/verification/wcm-diagnostic-classification-v2-independent-20261106.json'
    extras = [name, receipt, archive, 'apply_wcm_diagnostic_classification_v2_20261106.py']
    cfg['extra'] = list(dict.fromkeys([*cfg['extra'], *extras]))
    package['extra'] = list(dict.fromkeys([*package['extra'], *extras]))
    write_json(ROOT / cfg_name, cfg)
    write_json(ROOT / package_name, package)
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, actualRuntimeJsonAndAdmissionInputsFullyParsed=True,
        mandatoryFullyParsed=[dict(path=p, sha256=h) for p, h in sorted(mandatory.items())],
        opaqueDiagnosticsOnly=[dict(path=p, sha256=h) for p, h in sorted(opaque.items())],
        restoredFullyParsedDefaultAdmissionMetadata=prior, allFrozenWorkerInputsUnchanged=True,
        generatorSha256=sha256(ROOT / 'apply_wcm_diagnostic_classification_v2_20261106.py')))
    print(dict(passed=True, opaqueDiagnostics=9, mandatoryInputs=len(mandatory), sourceCredit=0))


if __name__ == '__main__':
    main()
