from project import ROOT, configuration, sha256, write_json
import match_runtime as compiler
import link_runtime_unit as linker
from main_byte_to_wide_native_20261030 import execute, cases
from match_main_overlap_copy_20261030 import main_references

WORK = ROOT / 'work/main-byte-to-wide-final-20261030'
SOURCES = [ROOT / f'src/runtime/20261030_byte_to_wide/native_main_{address}.c' for address in ['0201b09c']]
BINDINGS = {f'native_fn_{address}': {'processor': 'arm9', 'module': 'main', 'kind': 'function', 'mode': 'arm', 'address': '0x'+address}
            for address in ['0201b018', '0201d69c']}


def main():
    compiler.WORK = WORK / 'compile'
    metadata, original, config = linker.measured_module('main')
    rebuilt = bytearray(original)
    rows = []
    for source in SOURCES:
        found, unused = compiler.compare(source, 'main', '3', 'off', True)
        assert len(found) == 1
        row = found[0]
        assert row['exactAfterDeclaredRelocation']
        row.update(ordinaryFunctionCredit=1, sourceLanguage='C', originalObjectScaffolding=False)
        directory = WORK / row['name']
        proof = linker.validate(row, BINDINGS, directory)
        row['realMainLink'] = proof
        row['relocations'] = [{**r, 'target': r['symbol'], 'targetAddress': BINDINGS[r['symbol']]['address'],
                               'targetMode': BINDINGS[r['symbol']]['mode'], 'targetModule': 'main', 'addend': r['explicitAddend']}
                              for r in proof['originalRelocations']]
        literal = 0
        row['boundaries'] = dict(main_references(row, original, config), instructionBytes=row['bytes'] - literal,
                                 literalPoolBytes=literal, generatedLiteralOrPaddingBytes=literal)
        offset = int(row['address'], 0) - 0x02000000
        rebuilt[offset:offset + row['bytes']] = (directory / 'caller.bin').read_bytes()
        rows.append(row)
    results = []
    helper_returns = 0
    for tag, case in enumerate(cases()):
        before, after = execute(original, case, tag), execute(bytes(rebuilt), case, tag)
        assert before == after, case
        helper_returns += len(before['helperReturns']) * 2
        results.append({'case': list(case), 'result': before})
        if len(results) % 200 == 0:
            print({'returningPairs': len(results)}, flush=True)
    files = ['match_main_byte_to_wide_20261030.py', 'main_byte_to_wide_native_20261030.py',
             'main_format_wrappers_native_20261030.py', 'match_main_overlap_copy_20261030.py', 'match_runtime.py', 'link_runtime_unit.py']
    report = {'romSha256': configuration()['romSha256'], 'processor': 'arm9', 'module': 'main', 'matches': rows,
              'matchedFunctions': 1, 'matchedBytes': 136, 'sourceCredit': 136, 'nativeSymbolEntries': BINDINGS,
              'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in files],
              'oracle': {'pairs': len(results), 'actualOriginalAndSourceReturns': len(results) * 2,
                         'actualOriginalHelperReturns': helper_returns, 'providedCalls': 0, 'rows': results},
              'limitations': ['Only this 136-byte ordinary C caller receives new credit after full acceptance',
                              'Actual native strlen and default locale byte widening execute without providers',
                              'All 256 input bytes, bounded limits and null output are checked against an independent halfword-store/count model',
                              'The initial native strlen executes even when output is null; null input is unsupported',
                              'No arbitrary locale replacement/backend error, save-label encoding or device execution is claimed']}
    path = ROOT / 'evidence/matches/main-byte-to-wide-20261030.json'
    write_json(path, report)
    print({'functions': 1, 'bytes': 136, 'actualReturns': len(results) * 2, 'helperReturns': helper_returns, 'reportSha256': sha256(path)})


if __name__ == '__main__':
    main()
