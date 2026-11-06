import argparse
import re
from project import ROOT, read_json, write_json, sha256
from prepare_parallel_packet_wave import mandatory_inputs


def validate_partition(opaque, mandatory):
    assert all(path.endswith(('.json', '.txt', '.md', '.csv')) for path in opaque)
    assert not opaque.keys() & mandatory.keys()
    for path, expected in {**mandatory, **opaque}.items():
        assert sha256(ROOT / path) == expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configuration'); parser.add_argument('--ready', required=True)
    parser.add_argument('--sha256', required=True); parser.add_argument('--classification', required=True)
    parser.add_argument('--classification-sha256', required=True); parser.add_argument('--label', required=True)
    options = parser.parse_args(); assert re.fullmatch('[a-z0-9-]+', options.label)
    cfg = read_json(ROOT / options.configuration); assert not cfg['membershipFrozen']
    assert sha256(ROOT / options.ready) == options.sha256
    assert sha256(ROOT / options.classification) == options.classification_sha256
    classification = read_json(ROOT / options.classification); assert classification['sourceCredit'] == 0
    keys = [key for key in ['sourceExpansionOpaque', 'opaqueTraceFiles'] if key in classification]
    assert len(keys) == 1; opaque = {pin['path']: pin['sha256'] for pin in classification[keys[0]]}
    mandatory = {}
    for name in dict.fromkeys([*cfg['readyPackets'], options.ready]):
        ready = read_json(ROOT / name); descriptor = ready['canonicalDescriptor']
        assert sha256(ROOT / descriptor['path']) == descriptor['sha256']
        frozen = read_json(ROOT / descriptor['path'])['frozenInputs']; pins = mandatory_inputs(frozen)
        for pin in frozen:
            value = read_json(ROOT / pin['path']) if pin['path'].endswith('.json') else None
            if isinstance(value, dict):
                pins += value.get('files', [])
        pins += [dict(path=name, sha256=sha256(ROOT / name)), descriptor]
        for pin in pins:
            assert pin['path'] not in mandatory or mandatory[pin['path']] == pin['sha256']
            mandatory[pin['path']] = pin['sha256']
    for key in ['mandatoryParsed', 'mandatoryParsedFiles']:
        for pin in classification.get(key, []):
            assert pin['path'] not in mandatory or mandatory[pin['path']] == pin['sha256']
            mandatory[pin['path']] = pin['sha256']
    validate_partition(opaque, mandatory)
    actual_json = next(name for name in mandatory if name.endswith('/inputs.json'))
    try:
        validate_partition({**opaque, actual_json: mandatory[actual_json]}, mandatory)
    except AssertionError:
        pass
    else:
        raise AssertionError('Actual runtime input was admitted as opaque metadata')
    cohort = cfg['cohort']; package_name = cfg['name'] + '-package.json'
    archive = f'evidence/attempts/cohort{cohort}-{options.label}-diagnostics-v1-20261106/verbatim-inputs.json'
    assert not (ROOT / archive).exists()
    write_json(ROOT / archive, dict(sourceCredit=0, files=[dict(path=name, sha256=sha256(ROOT / name),
        verbatimUtf8=(ROOT / name).read_bytes().decode('utf-8')) for name in [options.configuration, package_name]]))
    unchanged = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json', options.ready]}
    cfg['opaqueMetadata'] = sorted((set(cfg['opaqueMetadata']) | opaque.keys()) - mandatory.keys())
    receipt = f'evidence/verification/cohort{cohort}-{options.label}-diagnostics-v1-20261106.json'
    cfg['extra'] = list(dict.fromkeys([*cfg['extra'], options.classification, archive, receipt,
        'apply_function_packet_diagnostics_v1_20261106.py']))
    write_json(ROOT / options.configuration, cfg)
    assert unchanged == {name: sha256(ROOT / name) for name in unchanged}
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, mandatoryFullyParsed=len(mandatory),
        opaqueDiagnosticsOnly=opaque, actualRuntimeJsonAsOpaqueRejected=True,
        frozenSourcesReadysAndInputsUnchanged=True, sharedRegistryAndPreferencesUnchanged=unchanged,
        generatorSha256=sha256(__file__)))
    print(dict(passed=True, opaqueDiagnostics=len(opaque), mandatoryInputs=len(mandatory), sourceCredit=0))


if __name__ == '__main__':
    main()
