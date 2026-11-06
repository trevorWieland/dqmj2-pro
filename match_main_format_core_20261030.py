import hashlib
import os
import subprocess
from project import ROOT, configuration, native_dependencies, sha256, write_json
native_dependencies(configuration())
import match_runtime as compiler
import link_runtime_unit as linker
from main_format_core_native_20261030 import execute, vectors
from match_main_overlap_copy_20261030 import main_references
from elftools.elf.elffile import ELFFile

WORK = ROOT / 'work/main-format-core-final-20261030'
SOURCE = ROOT / 'src/runtime/20261030_format_core/native_main_0201cb74.c'
FUNCTIONS = [0x0201D948, 0x0201D69C, 0x0201B338, 0x0201BB14, 0x0201B8C8,
             0x0201C410, 0x0201BE10, 0x0201B124, 0x0201B21C]
BINDINGS = {f'native_fn_{value:08x}': {'processor': 'arm9', 'module': 'main', 'kind': 'function',
              'mode': 'arm', 'address': hex(value)} for value in FUNCTIONS}
BINDINGS.update({f'native_data_{value:08x}': {'processor': 'arm9', 'module': 'main', 'kind': 'data',
                'mode': 'data', 'address': hex(value)} for value in [0x020DD11C, 0x020DD120]})


def failure_callback():
    source = ROOT / 'evidence/fixtures/formatter_write_failure_20261030.c'
    obj = WORK / 'failure-callback.o'
    command = [str(compiler.COMPILER), *compiler.FLAGS, '-c', str(source), '-o', str(obj)]
    result = subprocess.run(command, capture_output=True, text=True, timeout=60,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    assert result.returncode == 0, result.stdout + result.stderr
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = elf.get_section_by_name('.symtab').get_symbol_by_name('formatter_write_failure')[0]
        assert not linker.relocation_rows(obj, 'formatter_write_failure')
        body = elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']]
    return body, {'source': source.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(source),
                  'objectSha256': sha256(obj), 'bytes': len(body), 'nativeSourceCredit': 0,
                  'actualCompiledCExecution': True, 'syntheticRegisterOrReturnInjection': False}


def main():
    assert sha256(compiler.COMPILER) == compiler.COMPILER_PINS[compiler.COMPILER.relative_to(ROOT).as_posix()]
    assert sha256(SOURCE) == '12d8864dd33e734415987823d96866c15058dfc7bd886e487f9f79429ba015c9'
    metadata, binary, config = linker.measured_module('main')
    assert binary[0xDD11C:0xDD11E] == bytes(2) and binary[0xDD120:0xDD121] == bytes(1)
    compiler.WORK = WORK / 'compile'
    rows, unused = compiler.compare(SOURCE, 'main', '3', 'off', True)
    assert len(rows) == 1 and rows[0]['compiledBytes'] == 2084 and rows[0]['exactAfterDeclaredRelocation']
    entry = rows[0]
    entry.update(originalObjectScaffolding=False, sourceLanguage='C', ordinaryFunctionCredit=1, nativeSymbolEntries=BINDINGS)
    directory = WORK / 'real-link'
    directory.mkdir(parents=True, exist_ok=True)
    for filename in ['caller.bin', 'linked.elf']:
        path = directory / filename
        if path.exists():
            path.unlink()
    proof = linker.validate(entry, BINDINGS, directory)
    entry['realMainLink'] = proof
    entry['relocations'] = [{**row, 'target': row['symbol'], 'targetAddress': BINDINGS[row['symbol']]['address'],
                             'targetMode': BINDINGS[row['symbol']]['mode'], 'targetModule': 'main',
                             'addend': row['explicitAddend']} for row in proof['originalRelocations']]
    entry['boundaries'] = dict(main_references(entry, binary, config), generatedLiteralOrPaddingBytes=8,
                               instructionBytes=2076, literalPoolBytes=8)
    rebuilt = bytearray(binary)
    rebuilt[0x1CB74:0x1D398] = (directory / 'caller.bin').read_bytes()
    failure_code, failure = failure_callback()
    results = []
    for tag, case in enumerate(vectors()):
        args = (case['format'], case['arguments'], case['expected'], case['capacity'], case['alignment'], tag,
                failure_code if case['failure'] else None)
        original = execute(binary, *args)
        source = execute(bytes(rebuilt), *args)
        assert original == source, case
        results.append({'case': case['case'], 'formatHex': case['format'].hex(), 'capacity': case['capacity'],
                        'alignment': case['alignment'], 'writerFailure': case['failure'],
                        'independentTextModel': case['expected'] is not None, 'result': original})
    limitations = ['Only this2084-byte caller receives new native source credit',
                   'Nine original helper bodies, original writer, two original empty-string regions and fixture callback receive zero credit',
                   'Four-byte va-list and struct layout are target-specific and guarded at compilation',
                   'No arbitrary format widths, malformed active pointers, overlapping output or percent-hhn claims',
                   'Hex-float rows compare original and source without an independent text oracle',
                   'Whole-module and whole-ROM acceptance remain separate gates']
    files = ['match_main_format_core_20261030.py', 'main_format_core_native_20261030.py',
             'main_format_wrappers_native_20261030.py', 'match_main_overlap_copy_20261030.py',
             'link_runtime_unit.py', 'match_runtime.py', 'evidence/fixtures/formatter_write_failure_20261030.c']
    report = {'romSha256': configuration()['romSha256'], 'processor': 'arm9', 'module': 'main',
              'matches': [entry], 'matchedFunctions': 1, 'matchedBytes': 2084, 'nativeSymbolEntries': BINDINGS,
              'nativeSymbols': {name: row['address'] for name, row in BINDINGS.items()},
              'nativeSymbolModules': {name: row['module'] for name, row in BINDINGS.items()},
              'generatorSources': [{'path': path, 'sha256': sha256(ROOT / path)} for path in files],
              'originalHelperCodeAndSourceCredit': 0,
              'oracle': {'pairs': len(results), 'actualOriginalAndSourceReturns': len(results) * 2,
                         'knownActualDependencyReturns': 2 * sum(row['result']['actualKnownDependencyReturns'] for row in results),
                         'registerRamStackAndOrderedWritesEqual': True, 'failureCallback': failure,
                         'instructionBudgetPerRun': 1000000, 'microsecondBudgetPerRun': 2000000, 'rows': results},
              'limitations': limitations}
    path = ROOT / 'evidence/matches/main-format-core-20261030.json'
    write_json(path, report)
    print({'functions': 1, 'bytes': 2084, 'actualReturns': len(results) * 2, 'reportSha256': sha256(path)})


if __name__ == '__main__':
    main()
