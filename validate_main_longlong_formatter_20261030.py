import os
import subprocess
from project import ROOT, configuration, native_dependencies, read_json, sha256, write_json
native_dependencies(configuration())
import match_runtime as compiler
import link_runtime_unit as linker
from main_longlong_formatter_native_20261030 import execute
from elftools.elf.elffile import ELFFile


def main():
    report = read_json(ROOT / 'evidence/matches/main-longlong-formatter-20261030.json')
    positive = report['matches'][0]
    source = (ROOT / positive['source']).read_text()
    original_hash = sha256(ROOT / positive['source'])
    metadata, native, config = linker.measured_module('main')
    start = source.index('{', source.index('char* native_main_0201bb14'))
    variants = [('wrong-digits', source.replace("n += '0';", "n += '1';"), (17, 'd', 1, 0, 0, 1, 0, 0)),
                ('wrong-precision-limit', source.replace('> 509)', '> 508)'), (17, 'd', 1, 0, 0, 506, 0, 0)),
                ('wrong-result-pointer', source.replace('return p;', 'return 0;'), (17, 'x', 1, 0, 0, 1, 0, 0)),
                ('nonreturning-loop', source[:start + 1] + '\n    for (;;) {}\n}\n', (0, 'd', 1, 0, 0, 0, 0, 0))]
    results = []
    for label, text, case in variants:
        assert text != source
        folder = ROOT / 'work/main-longlong-formatter-controls-20261030' / label
        folder.mkdir(parents=True, exist_ok=True)
        path = ROOT / 'nonmatching/main-runtime/20261030/longlong-formatter-controls' / (label + '.c')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        obj = folder / 'source.o'
        command = [str(ROOT / positive['compilerPath']), *positive['compilerFlags'], '-c', str(path), '-o', str(obj)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=60,
            env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
        assert result.returncode == 0, result.stdout + result.stderr
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
        assert len(payload) == size and len(payload) <= 764
        candidate = bytearray(native)
        candidate[0x1BB14:0x1BB14 + size] = payload
        try:
            execute(bytes(candidate), case, 0)
        except AssertionError:
            rejected = True
        else:
            raise AssertionError('IncorrectSourcePassedIndependentModel')
        results.append({'control': label, 'source': path.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(path),
                        'objectSha256': sha256(obj), 'linkedBytes': size, 'linkedPayloadSha256': sha256(directory / 'caller.bin'),
                        'realLinkComparisonRejected': True, 'independentContractRejected': rejected, 'sourceCredit': 0,
                        'linkFailure': failure})
    assert sha256(ROOT / positive['source']) == original_hash
    destination = ROOT / 'evidence/verification/main-longlong-formatter-controls-20261030.json'
    write_json(destination, {'status': 'passed', 'controls': len(results), 'sourceCredit': 0, 'positiveSourceUnchanged': True,
                            'positiveReportSha256': sha256(ROOT / 'evidence/matches/main-longlong-formatter-20261030.json'),
                            'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in
                                ['validate_main_longlong_formatter_20261030.py', 'main_longlong_formatter_native_20261030.py']],
                            'results': results})
    print({'controls': len(results), 'allRejected': True, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
