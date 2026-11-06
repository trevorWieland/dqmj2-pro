from project import ROOT, configuration, sha256, write_json
import match_runtime as compiler
import link_runtime_unit as linker
from main_text_conversion_native_20261030 import execute, cases
from match_main_overlap_copy_20261030 import main_references

WORK = ROOT / 'work/main-text-conversion-final-20261030'
SOURCES = [ROOT / f'src/runtime/20261030_text_conversion/native_main_{address}.c' for address in ['0201b018', '0201b080', '0201b124']]
BINDINGS = {'native_data_020dcf1c': {'processor': 'arm9', 'module': 'main', 'kind': 'data', 'mode': 'data', 'address': '0x020dcf1c'},
            'native_fn_0201b080': {'processor': 'arm9', 'module': 'main', 'kind': 'function', 'mode': 'arm', 'address': '0x0201b080'},
            'native_fn_0201d780': {'processor': 'arm9', 'module': 'main', 'kind': 'function', 'mode': 'arm', 'address': '0x0201d780'}}


def main():
    compiler.WORK = WORK / 'compile'
    metadata, original, config = linker.measured_module('main')
    rebuilt = bytearray(original)
    rows = []
    for source in SOURCES:
        found, unused = compiler.compare(source, 'main', '2', 'off', True)
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
        literal = 4 if row['bytes'] == 28 else 0
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
    files = ['match_main_text_conversion_20261030.py', 'main_text_conversion_native_20261030.py',
             'main_format_wrappers_native_20261030.py', 'match_main_overlap_copy_20261030.py', 'match_runtime.py', 'link_runtime_unit.py']
    report = {'romSha256': configuration()['romSha256'], 'processor': 'arm9', 'module': 'main', 'matches': rows,
              'matchedFunctions': 3, 'matchedBytes': 176, 'sourceCredit': 176, 'nativeSymbolEntries': BINDINGS,
              'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in files],
              'oracle': {'pairs': len(results), 'actualOriginalAndSourceReturns': len(results) * 2,
                         'actualOriginalHelperReturns': helper_returns, 'providedCalls': 0, 'rows': results},
              'limitations': ['Only these three176 bytes of ordinary C receive credit after full acceptance',
                              'The current native locale table dispatches to byte-widening/truncating backends; no UTF8/ShiftJIS or save-label encoding is inferred',
                              'All256 byte values and selected full words/wide units, null outputs and bounded limits are checked',
                              'No arbitrary locale replacement, invalid input pointers or unsupported backend sizes/errors are claimed',
                              'A terminator may be written at the requested count boundary; this is measured behavior, not a standard sizing promise',
                              'Existing backend/copy helpers receive zero new credit; no scene/UI/persistence/device behavior is established']}
    path = ROOT / 'evidence/matches/main-text-conversion-20261030.json'
    write_json(path, report)
    print({'functions': 3, 'bytes': 176, 'actualReturns': len(results) * 2, 'helperReturns': helper_returns, 'reportSha256': sha256(path)})


if __name__ == '__main__':
    main()
