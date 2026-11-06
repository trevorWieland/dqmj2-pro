import argparse
import copy

from project import ROOT, read_json, write_json, sha256
from replay_parallel_packet_typed_arm9 import adapt, verified_bindings
from host_bindings import apply_typed_bindings


def rejected(callback, label):
    try:
        callback()
    except ValueError as error:
        return dict(control=label, rejected=True, reason=str(error))
    raise ValueError('Negative control was accepted: ' + label)


def verify(report, fixture):
    descriptor = report['canonicalPacketDescriptor']
    first = adapt(report, descriptor)
    second = adapt(first, descriptor)
    if first != second:
        raise ValueError('Typed ARM9 metadata adapter is not idempotent')
    row = next(value for value in report['matches'] if value['name'] == fixture['caller'])
    bindings = verified_bindings(row)
    name = fixture['binding']
    controls = []
    mutations = [('mode', 'thumb'), ('module', 'ov000'), ('processor', 'arm7'), ('program', 'move/child.srl'), ('address', '0x2008be4')]
    for field, value in mutations:
        wrong = copy.deepcopy(row)
        next(probe for probe in wrong['realLink']['bindingOnlyProbes'] if probe['name'] == name)[field] = value
        controls.append(rejected(lambda: verified_bindings(wrong), 'genuine-mode-probe-' + field))
    for field in ['nativeSymbolEntries', 'qualifiedDependencies']:
        wrong = copy.deepcopy(row)
        wrong[field] = copy.deepcopy(bindings)
        wrong[field][name]['mode'] = 'thumb'
        controls.append(rejected(lambda: verified_bindings(wrong), 'existing-metadata-conflict-' + field))

    def units():
        result = copy.deepcopy(fixture['units'])
        result.append(dict(module=row['module'], symbols={row['nativeAlias']: row['name']}, typedNativeBindings=copy.deepcopy(bindings), typedBindingRelocations=copy.deepcopy(row['relocations'])))
        return result

    normalized = apply_typed_bindings(units())[-1]
    if normalized['relocationAliases'] != fixture['expectedAliases']:
        raise ValueError('Host binding path changed the measured global relocation aliases')
    for field, value in mutations:
        wrong = units()
        wrong[-1]['typedNativeBindings'][name][field] = value
        controls.append(rejected(lambda: apply_typed_bindings(wrong), 'host-binding-' + field))
    return dict(schemaVersion=1, passed=True, sourceCredit=0, functions=len(report['matches']), adapterIdempotent=True, existingRowContractsUnchanged=True, aliasMapping=normalized['relocationAliases'], typedFunctionBindings=normalized['typedFunctionBindings'], negativeControls=controls)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('report')
    parser.add_argument('fixture')
    parser.add_argument('--output', required=True)
    options = parser.parse_args()
    result = verify(read_json(ROOT / options.report), read_json(ROOT / options.fixture))
    result.update(wrapperSha256=sha256(ROOT / 'replay_parallel_packet_typed_arm9.py'), verifierSha256=sha256(__file__), inputReport=dict(path=options.report, sha256=sha256(ROOT / options.report)), fixture=dict(path=options.fixture, sha256=sha256(ROOT / options.fixture)))
    write_json(ROOT / options.output, result)
    print(dict(passed=True, functions=result['functions'], idempotent=True, rejectedControls=len(result['negativeControls']), output=options.output))


if __name__ == '__main__':
    main()
