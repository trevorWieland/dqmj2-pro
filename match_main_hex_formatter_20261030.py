import os
import subprocess
from project import ROOT, configuration, native_dependencies, sha256, write_json
native_dependencies(configuration())
from elftools.elf.elffile import ELFFile
import match_runtime as compiler
import link_runtime_unit as linker
from main_hex_formatter_native_20261030 import execute, vectors
from match_main_overlap_copy_20261030 import main_references

SOURCE = ROOT / 'src/runtime/20261030_hex_formatter/native_main_0201be10.c'
WORK = ROOT / 'work/main-hex-formatter-final-20261030'
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p6/mwccarm.exe'
FUNCTIONS = {'native_fn_020236e8': 0x020236E8, 'native_fn_02022664': 0x02022664, 'native_fn_0201b8c8': 0x0201B8C8, '_deq': 0x02025208}
DATA = [0x020DD0E4, 0x020DD0EC, 0x020DD0F4, 0x020DD0FC, 0x020DD100, 0x020DD104, 0x020DD10C, 0x020DD114, 0x020DD118]
BINDINGS = {name: {'processor': 'arm9', 'module': 'main', 'kind': 'function', 'mode': 'arm', 'address': hex(address)} for name, address in FUNCTIONS.items()}
BINDINGS.update({f'native_data_{address:08x}': {'processor': 'arm9', 'module': 'main', 'kind': 'data', 'mode': 'data', 'address': hex(address)} for address in DATA})


def main():
    assert sha256(COMPILER) == compiler.COMPILER_PINS[COMPILER.relative_to(ROOT).as_posix()]
    WORK.mkdir(parents=True, exist_ok=True)
    flags = compiler.FLAGS[:]
    flags[0] = '-O4'
    flags[flags.index('-inline') + 1] = 'all'
    flags += ['-opt', 'speed']
    obj = WORK / 'source.o'
    process = subprocess.run([str(COMPILER), *flags, '-c', str(SOURCE), '-o', str(obj)], cwd=ROOT,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')),
        capture_output=True, text=True, timeout=60)
    assert process.returncode == 0, process.stdout + process.stderr
    immutable = WORK / 'objects' / (sha256(obj) + '.o')
    immutable.parent.mkdir(parents=True, exist_ok=True)
    if not immutable.exists():
        immutable.write_bytes(obj.read_bytes())
    with immutable.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = elf.get_section_by_name('.symtab').get_symbol_by_name('native_main_0201be10')[0]
        assert symbol['st_size'] == 1244
        section_index, section_offset = symbol['st_shndx'], symbol['st_value']
    metadata, original, config = linker.measured_module('main')
    native = original[0x1BE10:0x1C2EC]
    row = {'name': 'native_main_0201be10', 'nativeAlias': 'func_0201be10', 'processor': 'arm9', 'module': 'main',
           'mode': 'arm', 'address': '0x0201be10', 'bytes': 1244, 'compiledBytes': 1244,
           'source': SOURCE.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(SOURCE),
           'object': immutable.relative_to(ROOT).as_posix(), 'objectSha256': sha256(immutable),
           'compilerPath': COMPILER.relative_to(ROOT).as_posix(), 'compilerSha256': sha256(COMPILER), 'compilerFlags': flags,
           'targetSha256': compiler.sha(native), 'sectionIndex': section_index, 'sectionOffset': section_offset,
           'ordinaryFunctionCredit': 1, 'sourceLanguage': 'C', 'originalObjectScaffolding': False}
    directory = WORK / 'real-link'
    proof = linker.validate(row, BINDINGS, directory)
    row.update(realMainLink=proof, matchingBytes=1244, exactAfterDeclaredRelocation=True, outputSha256=sha256(directory / 'caller.bin'))
    row['relocations'] = [{**r, 'target': r['symbol'], 'targetAddress': BINDINGS[r['symbol']]['address'],
                           'targetMode': BINDINGS[r['symbol']]['mode'], 'targetModule': 'main', 'addend': r['explicitAddend']}
                          for r in proof['originalRelocations']]
    row['boundaries'] = dict(main_references(row, original, config), instructionBytes=1200,
                             literalPoolBytes=44, generatedLiteralOrPaddingBytes=44)
    rebuilt = bytearray(original)
    rebuilt[0x1BE10:0x1C2EC] = (directory / 'caller.bin').read_bytes()
    results = []
    helper_returns = 0
    for tag, case in enumerate(vectors()):
        before, after = execute(original, case, tag), execute(bytes(rebuilt), case, tag)
        assert before == after, case
        helper_returns += len(before['nativeHelperReturns']) * 2
        results.append({'case': list(case), 'result': before})
        if len(results) % 100 == 0:
            print({'returningPairs': len(results)}, flush=True)
    files = ['match_main_hex_formatter_20261030.py', 'main_hex_formatter_native_20261030.py',
             'main_format_wrappers_native_20261030.py', 'match_main_overlap_copy_20261030.py', 'match_runtime.py', 'link_runtime_unit.py']
    report = {'romSha256': configuration()['romSha256'], 'processor': 'arm9', 'module': 'main', 'matches': [row],
              'matchedFunctions': 1, 'matchedBytes': 1244, 'sourceCredit': 1244, 'nativeSymbolEntries': BINDINGS,
              'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in files],
              'oracle': {'pairs': len(results), 'actualOriginalAndSourceReturns': len(results) * 2,
                         'actualOriginalHelperReturns': helper_returns, 'providedCalls': 0,
                         'independentExpectedTextAndOrderedStores': True, 'rows': results},
              'limitations': ['Only this1244-byte caller earns source credit after the complete acceptance gate',
                              'Original decimal conversion/comparison/rounding helpers and readonly text/type data receive zero new credit',
                              'Raw-bit normal/subnormal hex extraction is truncation and padding, not IEEE decimal rounding',
                              'Negative precision, invalid selectors/pointers, arbitrary aliases and unsafe signed maximum-width buffers remain unsupported',
                              'Zero ignores case, sign and precision and produces0x0p0; nonzero subnormals use implicit1 and exponent-1023 as measured',
                              'No source-only ROM, playable host game or device execution is claimed']}
    path = ROOT / 'evidence/matches/main-hex-formatter-20261030.json'
    write_json(path, report)
    print({'bytes': 1244, 'actualReturns': len(results) * 2, 'actualHelperReturns': helper_returns, 'reportSha256': sha256(path)})


if __name__ == '__main__':
    main()
