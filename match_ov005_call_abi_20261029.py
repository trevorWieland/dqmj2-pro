from pathlib import Path
from project import ROOT, configuration, read_json, sha256, verify_inputs, write_json
import match_runtime as compiler
from recover_linked_runtime import qualified_bindings
from link_runtime_unit import measured_module, validate, verify_binding
from save_link_snapshots import freeze_link
from ov005_call_abi_fixture_20261029 import execute, vectors

SPECS = [(0x021D761C, 288, 'src/overlays/ov005_021d761c_20261029_call_abi.c'),
         (0x021D7E58, 136, 'src/overlays/ov005_021d7e58_20261029_call_abi.c')]


def main():
    before = verify_inputs(configuration())
    metadata, native, config = measured_module('ov005')
    main_metadata, main, unused = measured_module('main')
    matches = []
    for entry, size, relative in SPECS:
        source = ROOT / relative
        rows, exact = compiler.compare(source, 'ov005', 2, 'off')
        name = 'native_ov005_' + format(entry, '08x')
        if name not in exact:
            raise ValueError('Complete source byte/relocation match failed')
        row = exact[name][0]
        if row['bytes'] != size or row['compiledBytes'] != size:
            raise ValueError('Complete configured caller boundary changed')
        self_relocations = [rel for rel in row['relocations'] if rel['symbol'] == name]
        bindings = qualified_bindings({**row, 'relocations': [rel for rel in row['relocations'] if rel['symbol'] != name]})
        if self_relocations:
            own = {'processor': 'arm9', 'module': 'ov005', 'kind': 'function', 'mode': 'arm', 'address': hex(entry)}
            verify_binding(name, own)
            bindings[name] = own
        directory = ROOT / 'work/ov005-call-abi/20261029' / name
        proof = validate(row, bindings, directory)
        code = (directory / 'caller.bin').read_bytes()
        target = native[entry - 0x021D7240:entry - 0x021D7240 + size]
        cases = []
        for ordinal, case in enumerate(vectors(entry)):
            original = execute(main, native, entry, target, case, ordinal)
            rebuilt = execute(main, native, entry, code, case, ordinal)
            if original != rebuilt:
                raise AssertionError(('Native/compiled caller state differs', hex(entry), ordinal))
            cases.append({'input': case, 'actualReturns': 2, 'result': original})
        matches.append({**row, 'sourceLanguage': 'C', 'ordinaryCOnly': True,
                        'nativeSymbolEntries': bindings, 'qualifiedDependencies': bindings,
                        'isolatedCallerRealLink': proof, **freeze_link(proof), 'calleeCodeOrSourceCredit': 0,
                        'oracle': {'supported': True, 'supportedReturningVectors': len(cases),
                                   'actualReturningCalls': len(cases) * 2, 'cases': cases,
                                   'independentCompleteDataRamAndCallModel': True,
                                   'allGeneralRegistersCpsrStackStoresAndPcTracesCompared': True,
                                   'explicitCalleeReturnOnlyProviders': True, 'nativeCalleesExecute': False,
                                   'limitations': ['Callees use declared return-only boundaries; SDK networking/UI behavior is not certified',
                                                  'Only the caller ranges and their qualified call-word contracts receive source credit']},
                        'linked': False, 'sourceReconstructionComplete': False})
    if before != verify_inputs(configuration()):
        raise AssertionError('Original private inputs changed')
    report = {'schemaVersion': 1, 'romSha256': configuration()['romSha256'], 'module': 'ov005',
              'moduleInputSha256': metadata['sha256'], 'mainInputSha256': main_metadata['sha256'],
              'matches': matches, 'matchedFunctions': len(matches), 'matchedBytes': sum(row['bytes'] for row in matches),
              'nativeSymbols': {rel['symbol']: rel['target'] for row in matches for rel in row['relocations']},
              'replayDependencies': [{'path': name, 'sha256': sha256(ROOT / name)} for name in
                                     ('match_ov005_call_abi_20261029.py', 'ov005_call_abi_fixture_20261029.py')],
              'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    write_json(ROOT / 'evidence/matches/ov005-20261029-call-abi.json', report)
    print({'functions': len(matches), 'bytes': report['matchedBytes'],
           'cases': sum(row['oracle']['supportedReturningVectors'] for row in matches),
           'actualReturns': sum(row['oracle']['actualReturningCalls'] for row in matches)})


if __name__ == '__main__':
    main()
