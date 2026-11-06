import os
import subprocess
from project import ROOT, read_json, sha256, write_json
import link_runtime_unit as linker
from main_decimal_formatter_native_20261030 import execute
from elftools.elf.elffile import ELFFile


def main():
    positive_path = ROOT / 'evidence/matches/main-decimal-formatter-20261030.json'
    report = read_json(positive_path)
    positive = report['matches'][0]
    source_path = ROOT / positive['source']
    original_hash = sha256(source_path)
    source = source_path.read_text()
    start = source.index('{', source.index('char* native_main_0201c410'))
    normal = (0x3FF8000000000000, 'f', 6, 0, 0, False)
    variants = [('wrong-radix', source.replace("radix_marker = '.';", "radix_marker = ',';"), normal),
                ('wrong-negative-sign', source.replace('if (dec.sign)', 'if (0)'), (0xC002000000000000, 'f', 6, 0, 0, True)),
                ('wrong-result-pointer', source.replace('return p;', 'return 0;'), normal),
                ('wrong-infinity-case', source.replace('native_data_020dd0ec', 'native_data_020dd0f4'), (0xFFF0000000000000, 'F', 6, 0, 0, False)),
                ('nonreturning-loop', source[:start + 1] + '\n    for (;;) {}\n}\n', normal)]
    metadata, native, config = linker.measured_module('main')
    results = []
    for label, text, case in variants:
        assert text != source
        folder = ROOT / 'work/main-decimal-formatter-controls-20261030' / label
        folder.mkdir(parents=True, exist_ok=True)
        path = ROOT / 'nonmatching/main-runtime/20261030/decimal-formatter-controls' / (label + '.c')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        obj = folder / 'source.o'
        process = subprocess.run([str(ROOT / positive['compilerPath']), *positive['compilerFlags'], '-c', str(path), '-o', str(obj)],
            capture_output=True, text=True, timeout=60,
            env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
        assert process.returncode == 0, process.stdout + process.stderr
        with obj.open('rb') as stream:
            elf = ELFFile(stream)
            symbol = elf.get_section_by_name('.symtab').get_symbol_by_name(positive['name'])[0]
            size = symbol['st_size']
        row = dict(positive, source=path.relative_to(ROOT).as_posix(), sourceSha256=sha256(path),
                   object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj), ordinaryFunctionCredit=0)
        directory = folder / 'real-link'
        try:
            linker.validate(row, report['nativeSymbolEntries'], directory)
        except ValueError as error:
            failure = str(error)
            assert 'matchingBytes' in failure
        else:
            raise AssertionError('IncorrectSourceAccepted')
        payload = (directory / 'caller.bin').read_bytes()
        assert len(payload) == size and size <= 1892
        candidate = bytearray(native)
        candidate[0x1C410:0x1C410 + size] = payload
        try:
            execute(bytes(candidate), case, 0)
        except AssertionError:
            rejected = True
        else:
            raise AssertionError('IncorrectSourcePassedIndependentModel')
        results.append({'control': label, 'source': path.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(path),
                        'objectSha256': sha256(obj), 'linkedBytes': size, 'realLinkComparisonRejected': True,
                        'independentContractRejected': rejected, 'linkFailure': failure, 'sourceCredit': 0})
    assert sha256(source_path) == original_hash
    files = ['validate_main_decimal_formatter_20261030.py', 'main_decimal_formatter_native_20261030.py']
    write_json(ROOT / 'evidence/verification/main-decimal-formatter-controls-20261030.json',
        {'status': 'passed', 'controls': len(results), 'sourceCredit': 0, 'positiveSourceUnchanged': True,
         'positiveReportSha256': sha256(positive_path), 'results': results,
         'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in files]})
    print({'controls': len(results), 'allRejected': True, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
