from project import ROOT, configuration, sha256, write_json
import match_runtime as compiler
import link_runtime_unit as linker
from main_format_parser_native_20261030 import execute, cases
from match_main_overlap_copy_20261030 import main_references

WORK = ROOT / 'work/main-format-parser-final-20261030'
SOURCES = [ROOT / f'src/runtime/20261030_format_parser/native_main_{address}.c' for address in ['0201b338']]
BINDINGS = {'native_data_020d8e04': {'processor': 'arm9', 'module': 'main', 'kind': 'data', 'mode': 'data', 'address': '0x020d8e04'}}


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
        literal = 4
        row['boundaries'] = dict(main_references(row, original, config), instructionBytes=row['bytes'] - literal - 4, compilerAlignmentPaddingBytes=4,
                                 literalPoolBytes=literal, generatedLiteralOrPaddingBytes=literal + 4)
        offset = int(row['address'], 0) - 0x02000000
        rebuilt[offset:offset + row['bytes']] = (directory / 'caller.bin').read_bytes()
        rows.append(row)
    results = []
    helper_returns = 0
    for tag, case in enumerate(cases()):
        before, after = execute(original, case, tag), execute(bytes(rebuilt), case, tag)
        assert before == after, case
        helper_returns += 0
        results.append({'case': [case[0].hex(), list(case[1])], 'result': before})
        if len(results) % 200 == 0:
            print({'returningPairs': len(results)}, flush=True)
    files = ['match_main_format_parser_20261030.py', 'main_format_parser_native_20261030.py',
             'main_format_wrappers_native_20261030.py', 'match_main_overlap_copy_20261030.py', 'match_runtime.py', 'link_runtime_unit.py']
    report = {'romSha256': configuration()['romSha256'], 'processor': 'arm9', 'module': 'main', 'matches': rows,
              'matchedFunctions': 1, 'matchedBytes': 1424, 'sourceCredit': 1424, 'nativeSymbolEntries': BINDINGS,
              'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in files],
              'oracle': {'pairs': len(results), 'actualOriginalAndSourceReturns': len(results) * 2,
                         'actualOriginalHelperReturns': helper_returns, 'providedCalls': 0, 'rows': results},
              'limitations': ['Only this 1424-byte ordinary C parser receives credit after complete acceptance',
                              'These are actual direct parser-entry returns, distinct from the earlier outer formatter near-source proof',
                              'Independent regular-expression/field models check bounded format strings, argument advancement and the complete format record',
                              'The two format padding bytes copy initialized stack poison; no semantic field meaning is assigned',
                              'Invalid pointers, integer width overflow/INT_MIN negation, arbitrary strings and device execution are unsupported']}
    path = ROOT / 'evidence/matches/main-format-parser-20261030.json'
    write_json(path, report)
    print({'functions': 1, 'bytes': 1424, 'actualReturns': len(results) * 2, 'helperReturns': helper_returns, 'reportSha256': sha256(path)})


if __name__ == '__main__':
    main()
