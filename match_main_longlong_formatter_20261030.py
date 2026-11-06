from project import ROOT, configuration, native_dependencies, read_json, sha256, write_json
native_dependencies(configuration())
import match_runtime as compiler
import link_runtime_unit as linker
import native_alternate_entries as entry_policy
from main_longlong_formatter_native_20261030 import execute, vectors
from match_main_overlap_copy_20261030 import main_references

WORK = ROOT / 'work/main-longlong-formatter-final-20261030'
SOURCE = ROOT / 'src/runtime/20261030_longlong_formatter/native_main_0201bb14.c'
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p6/mwccarm.exe'


def main():
    assert sha256(COMPILER) == compiler.COMPILER_PINS[COMPILER.relative_to(ROOT).as_posix()]
    qualifier = entry_policy.binding('main', 0x020260E8)
    if qualifier is None:
        raise ValueError('Unsigned64 alternate entry is not activated')
    bindings = {'native_fn_020260e8': qualifier,
                'native_fn_020260dc': {'processor': 'arm9', 'module': 'main', 'mode': 'arm', 'kind': 'function', 'address': '0x020260dc'}}
    compiler.WORK = WORK / 'compile'
    rows, unused = compiler.compare(SOURCE, 'main', '4', 'off', True, compiler=COMPILER)
    assert len(rows) == 1 and rows[0]['compiledBytes'] == 764 and rows[0]['exactAfterDeclaredRelocation']
    row = rows[0]
    row.update(ordinaryFunctionCredit=1, sourceLanguage='C', originalObjectScaffolding=False,
               sourceCreditWithheldPendingBindingActivation=False, nativeSymbolEntries=bindings)
    directory = WORK / 'real-link'
    directory.mkdir(parents=True, exist_ok=True)
    for filename in ['caller.bin', 'linked.elf']:
        path = directory / filename
        if path.exists():
            path.unlink()
    original_table = entry_policy.TABLE
    table_hash = sha256(original_table)
    proof = linker.validate(row, bindings, directory)
    assert sha256(original_table) == table_hash
    row['realMainLink'] = proof
    row['relocations'] = [{**r, 'target': r['symbol'], 'targetAddress': bindings[r['symbol']]['address'],
                           'targetMode': 'arm', 'targetModule': 'main', 'addend': r['explicitAddend']}
                          for r in proof['originalRelocations']]
    metadata, original, config = linker.measured_module('main')
    row['boundaries'] = dict(main_references(row, original, config), generatedLiteralOrPaddingBytes=4, instructionBytes=760, literalPoolBytes=4)
    rebuilt = bytearray(original)
    rebuilt[0x1BB14:0x1BE10] = (directory / 'caller.bin').read_bytes()
    results, helper_returns = [], 0
    for tag, case in enumerate(vectors()):
        before, after = execute(original, case, tag), execute(bytes(rebuilt), case, tag)
        assert before == after, case
        helper_returns += 2 * before['actualArithmeticHelperReturns']
        results.append({'case': list(case), 'result': before})
        if len(results) % 500 == 0:
            print({'returningPairs': len(results)}, flush=True)
    files = ['match_main_longlong_formatter_20261030.py', 'main_longlong_formatter_native_20261030.py',
             'main_format_wrappers_native_20261030.py', 'match_main_overlap_copy_20261030.py', 'match_runtime.py',
             'link_runtime_unit.py', 'native_alternate_entries.py', 'verify_main_unsigned64_entry_20261030.py',
             'prove_main_unsigned64_entries_20261030.py',
             'evidence/entrypoints/main-unsigned64-entry-20261030.json']
    report = {'romSha256': configuration()['romSha256'], 'processor': 'arm9', 'module': 'main', 'matches': [row],
              'sourceCredit': 764, 'ordinaryFunctionCredit': 1, 'bindingActivated': True, 'matchedFunctions': 1, 'matchedBytes': 764, 'originalTableUnchanged': True,
              'initializedSourceBytes': 764, 'nativeSymbolEntries': bindings,
              'nativeSymbols': {name: value['address'] for name, value in bindings.items()},
              'nativeSymbolModules': {name: value['module'] for name, value in bindings.items()},
              'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in files],
              'oracle': {'pairs': len(results), 'actualOriginalAndSourceReturns': len(results) * 2,
                         'actualOriginalArithmeticHelperReturns': helper_returns, 'rows': results},
              'limitations': ['Typed alternate binding is activated and checked against its exact native ABI evidence',
                              'Only six valid selectors and bounded arithmetic/buffer states are modeled',
                              'Null result can follow partial writes; invalid pointers and aliases are not claimed',
                              'Original arithmetic helpers and data receive zero new credit',
                              'Full module/ROM gates and host game execution remain separate']}
    path = ROOT / 'evidence/matches/main-longlong-formatter-20261030.json'
    write_json(path, report)
    print({'bytes': 764, 'sourceCredit': 764, 'actualTopReturns': len(results) * 2, 'actualHelperReturns': helper_returns, 'reportSha256': sha256(path)})


if __name__ == '__main__':
    main()
