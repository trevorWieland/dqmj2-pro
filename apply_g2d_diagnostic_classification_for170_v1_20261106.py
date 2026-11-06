from project import ROOT, read_json, write_json, sha256
from prepare_parallel_packet_wave import mandatory_inputs


def main():
    name = 'evidence/lanes/parallel-wave20261106/g2d-canvas-next/first-diagnostic-classification-v1.json'
    assert sha256(ROOT / name) == '740217b394d12cac55eacaf9cd3d129106d5d97ddd17a5254a59d828ebf7fb68'
    classification = read_json(ROOT / name)
    assert classification['sourceCredit'] == 0 and len(classification['mandatoryParsedFiles']) == 7
    opaque = {row['path']: row['sha256'] for row in classification['opaqueTraceFiles']}
    assert len(opaque) == 6 and all(path.endswith('.json') for path in opaque)
    ready_name = 'evidence/lanes/parallel-wave20261106/g2d-canvas-next/first/ready.json'
    assert sha256(ROOT / ready_name) == '40fe4c487062d0ac63236a63e68e66f9946909964fd0851d1d9e3eb19ab8165f'
    ready = read_json(ROOT / ready_name); descriptor = ready['canonicalDescriptor']
    assert sha256(ROOT / descriptor['path']) == descriptor['sha256']
    mandatory = {pin['path']: pin['sha256'] for pin in mandatory_inputs(read_json(ROOT / descriptor['path'])['frozenInputs'])}
    for pin in read_json(ROOT / 'evidence/lanes/parallel-wave20261106/g2d-canvas-next/first/inputs.json')['files']:
        assert pin['path'] not in mandatory or mandatory[pin['path']] == pin['sha256']
        mandatory[pin['path']] = pin['sha256']
    mandatory.update({ready_name: sha256(ROOT / ready_name), descriptor['path']: descriptor['sha256']})
    mandatory.update({pin['path']: pin['sha256'] for pin in classification['mandatoryParsedFiles']})
    assert not mandatory.keys() & opaque.keys()
    for path, expected in {**mandatory, **opaque}.items():
        assert sha256(ROOT / path) == expected
    cfg_name = 'provenance/parallel-wave20261105-o-packets.json'
    package_name = 'cohort170-parallel-wave20261105-o-package.json'
    cfg, package = read_json(ROOT / cfg_name), read_json(ROOT / package_name)
    assert not cfg['membershipFrozen']
    prior = sorted(set(cfg['opaqueMetadata']) & mandatory.keys())
    archive = 'evidence/attempts/cohort170-g2d-source-expansion-policy-v1-20261106/verbatim-inputs.json'
    if not (ROOT / archive).exists():
        write_json(ROOT / archive, dict(sourceCredit=0, files=[dict(path=n, sha256=sha256(ROOT / n),
            text=(ROOT / n).read_text(encoding='utf-8')) for n in [cfg_name, package_name]]))
    cfg['opaqueMetadata'] = sorted((set(cfg['opaqueMetadata']) | opaque.keys()) - mandatory.keys())
    assert not set(cfg['opaqueMetadata']) & mandatory.keys()
    receipt = 'evidence/verification/g2d-diagnostic-classification-v1-independent-20261106.json'
    extras = [name, receipt, archive, 'apply_g2d_diagnostic_classification_for170_v1_20261106.py',
        'admit_g2d_canvas_scope_v1_20261106.py',
        'evidence/attempts/auth-ready-output-role-path-set-correction-20261106/previous-audit.json']
    cfg['extra'] = list(dict.fromkeys([*cfg['extra'], *extras]))
    package['extra'] = list(dict.fromkeys([*package['extra'], *extras]))
    write_json(ROOT / cfg_name, cfg); write_json(ROOT / package_name, package)
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, actualRuntimeJsonAndAdmissionInputsFullyParsed=True,
        mandatoryFullyParsed=[dict(path=p, sha256=h) for p, h in sorted(mandatory.items())],
        opaqueDiagnosticsOnly=[dict(path=p, sha256=h) for p, h in sorted(opaque.items())],
        restoredFullyParsedDefaultAdmissionMetadata=prior, allFrozenWorkerInputsUnchanged=True,
        generatorSha256=sha256(__file__)))
    print(dict(passed=True, opaqueDiagnostics=6, mandatoryInputs=len(mandatory), sourceCredit=0))


if __name__ == '__main__':
    main()
