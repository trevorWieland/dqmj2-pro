from project import ROOT, configuration, native_dependencies, sha256, write_json
native_dependencies(configuration())
import match_runtime as compiler
import link_runtime_unit as linker
from main_integer_formatter_native_20261030 import execute, vectors
from match_main_overlap_copy_20261030 import main_references

WORK = ROOT / 'work/main-integer-formatter-final-20261030'
SOURCE = ROOT / 'src/runtime/20261030_integer_formatter/native_main_0201b8c8.c'
BINDINGS = {'_u32_div_f': {'processor': 'arm9', 'module': 'main', 'kind': 'function', 'mode': 'arm', 'address': '0x02026350'}}


def main():
    assert sha256(compiler.COMPILER) == compiler.COMPILER_PINS[compiler.COMPILER.relative_to(ROOT).as_posix()]
    compiler.WORK = WORK / 'compile'
    rows, unused = compiler.compare(SOURCE, 'main', '4', 'off', True)
    assert len(rows) == 1 and rows[0]['compiledBytes'] == 588 and rows[0]['exactAfterDeclaredRelocation']
    entry = rows[0]
    entry.update(sourceLanguage='C', ordinaryFunctionCredit=1, originalObjectScaffolding=False, nativeSymbolEntries=BINDINGS)
    directory = WORK / 'real-link'
    directory.mkdir(parents=True, exist_ok=True)
    for filename in ['caller.bin', 'linked.elf']:
        path = directory / filename
        if path.exists():
            path.unlink()
    proof = linker.validate(entry, BINDINGS, directory)
    entry['realMainLink'] = proof
    entry['relocations'] = [{**row, 'target': row['symbol'], 'targetAddress': BINDINGS[row['symbol']]['address'],
                             'targetMode': 'arm', 'targetModule': 'main', 'addend': row['explicitAddend']}
                            for row in proof['originalRelocations']]
    metadata, original, config = linker.measured_module('main')
    entry['boundaries'] = dict(main_references(entry, original, config), generatedLiteralOrPaddingBytes=4,
                               instructionBytes=584, literalPoolBytes=4)
    rebuilt = bytearray(original)
    rebuilt[0x1B8C8:0x1BB14] = (directory / 'caller.bin').read_bytes()
    results = []
    helper_returns = 0
    for tag, case in enumerate(vectors()):
        before, after = execute(original, case, tag), execute(bytes(rebuilt), case, tag)
        assert before == after, case
        helper_returns += before['actualDivisionHelperReturns'] * 2
        results.append({'case': list(case), 'result': before})
        if len(results) % 500 == 0:
            print({'returningPairs': len(results)}, flush=True)
    files = ['match_main_integer_formatter_20261030.py', 'main_integer_formatter_native_20261030.py',
             'main_format_wrappers_native_20261030.py', 'match_main_overlap_copy_20261030.py', 'link_runtime_unit.py', 'match_runtime.py']
    report = {'romSha256': configuration()['romSha256'], 'processor': 'arm9', 'module': 'main',
              'matches': [entry], 'matchedFunctions': 1, 'matchedBytes': 588, 'nativeSymbolEntries': BINDINGS,
              'nativeSymbols': {'_u32_div_f': '0x02026350'}, 'nativeSymbolModules': {'_u32_div_f': 'main'},
              'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in files],
              'oracle': {'pairs': len(results), 'actualOriginalAndSourceReturns': len(results) * 2,
                         'actualOriginalDivisionHelperReturns': helper_returns, 'originalDivisionHelperSourceCredit': 0,
                         'unsignedDivisionR0QuotientR1RemainderChecked': True, 'independentOrderedByteStoreModel': True,
                         'instructionBudgetPerRun': 200000, 'microsecondBudgetPerRun': 1000000,
                         'rows': results},
              'limitations': ['Only this588-byte caller receives native source credit',
                              'Original unsigned divide helper/data context receives zero new credit',
                              'Only six valid integer conversion selectors are modeled; unknown selectors leave base uninitialized',
                              'Arbitrary invalid buffers, pointer aliases and signed precision/width overflow are not claimed',
                              'A null return may follow partial output writes',
                              'Whole-module/ROM acceptance and portable host execution remain separate']}
    path = ROOT / 'evidence/matches/main-integer-formatter-20261030.json'
    write_json(path, report)
    print({'functions': 1, 'bytes': 588, 'actualTopReturns': len(results) * 2, 'actualDivisionReturns': helper_returns,
           'reportSha256': sha256(path)})


if __name__ == '__main__':
    main()
