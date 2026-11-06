import argparse
import subprocess
import sys
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256, configuration, native_dependencies


def binding_identity(value):
    return value.get('program') or '', value['processor'], value['module'], value['kind'], value['mode'], int(value['address'], 0)


def qualify_report(report, scope):
    native_dependencies(configuration())
    import link_arm7_bulk_20261030 as original
    original_namespace = original.namespace
    symbols, bindings, proofs = dict(report.get('nativeSymbols', {})), {}, []
    for entry in report['matches']:
        assert (entry.get('program') or '', entry['processor'], entry['module'], entry['mode']) == ('', 'arm7', 'arm7-main', 'arm')
        assert entry['realLink']['exactCallerBytes'] and entry['exactAfterDeclaredRelocation']
        qualified = []
        if (int(entry['address'], 0), entry['bytes']) == (0x027e0898, 4464):
            assert entry['targetSha256'] == 'acb3b83aa6853d01ac2efc2a06b7dc16b8c9b49935bf1886ede49c0d7c55f30c'
            from wave20261105_arm7_boundary_next_source_callables import qualified as qualify_callables
            qualified = list(qualify_callables().values())
            assert len(qualified) == 2 and {int(row['address'], 0) for row in qualified} == {0x027e1ad4, 0x027e1c00}
        def namespace(program):
            modules, functions = original_namespace(program)
            for row in qualified:
                address = int(row['address'], 0)
                assert address not in functions and program == ''
                functions[address] = row
            return modules, functions
        directory = original.WORK / 'complete-binding-metadata-20261106' / scope / entry['address'][2:]
        with patch.object(original, 'namespace', side_effect=namespace):
            proof = original.validate(entry, directory)
        derived = proof['bindings']
        declared = entry['nativeSymbolEntries']
        assert set(derived) == set(declared)
        assert all(binding_identity(derived[name]) == binding_identity(declared[name]) for name in derived)
        assert all(row['initializedCodeBytes'] == row['calleeSourceCredit'] == 0 for row in entry['realLink']['zeroCodeAnchors'])
        for name, value in derived.items():
            assert value['processor'] == 'arm7' and not value.get('program')
            if name in bindings:
                assert binding_identity(bindings[name]) == binding_identity(value)
            address = value['address']
            if name in symbols:
                assert int(symbols[name], 0) == int(address, 0)
            symbols[name] = address
            bindings[name] = value
        proofs.append(dict(address=entry['address'], bytes=entry['bytes'], objectSha256=entry['objectSha256'],
                           originalCoreGenuineLink=proof, declaredNativeBindings=len(derived)))
    report['nativeSymbols'] = symbols
    report['nativeSymbolBindings'] = [dict(name=name, **value) for name, value in sorted(bindings.items())]
    report['completeArm7BindingQualification'] = dict(passed=True, sourceCredit=0, calleeSourceCredit=0,
        originalNativeWordsAndCompilerObjectsUnchanged=True, originalCoreVerifierUnchanged=True, proofs=proofs)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('descriptor')
    args = parser.parse_args()
    descriptor = read_json(ROOT / args.descriptor)
    assert all((row.get('program') or '', row['processor'], row['module'], row['mode']) == ('', 'arm7', 'arm7-main', 'arm')
               for row in descriptor['identities'])
    subprocess.run([sys.executable, str(ROOT / 'replay_parallel_packet.py'), args.descriptor], cwd=ROOT, check=True)
    path = ROOT / descriptor['canonicalReport']
    report = read_json(path)
    before = [(row['sourceSha256'], row['objectSha256'], row['targetSha256']) for row in report['matches']]
    result = qualify_report(report, path.stem)
    assert before == [(row['sourceSha256'], row['objectSha256'], row['targetSha256']) for row in result['matches']]
    sources = {pin['path']: pin['sha256'] for pin in result['generatorSources']}
    sources[__file__.split('\\')[-1]] = sha256(__file__)
    result['generatorSources'] = [dict(path=name, sha256=digest) for name, digest in sorted(sources.items())]
    write_json(path, result)
    print(dict(functions=len(result['matches']), completeNativeSymbols=len(result['nativeSymbols']),
               originalSourceAndObjectBytesPreserved=True, sourceCredit=0))


if __name__ == '__main__':
    main()
