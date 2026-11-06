import os
import subprocess
from project import ROOT, read_json, sha256, write_json
import link_runtime_unit as linker
from main_memory_primitives_native_20261030 import execute
from elftools.elf.elffile import ELFFile


def main():
    positive_path = ROOT / 'evidence/matches/main-memory-primitives-20261030.json'
    report = read_json(positive_path)
    metadata, native, config = linker.measured_module('main')
    variants = [('search-wrong-predicate', '0x201b21c', '== target', '!= target', ('search', 65, 31, 0, 2)),
                ('compare-reversed-order', '0x201b248', '? -1 : 1', '? 1 : -1', ('compare', 65, 64, 0, 1)),
                ('fill-missing-word', '0x201b288', 'words[7] = fill', 'words[6] = fill', ('fill', 255, 64, 0, 0)),
                ('nonreturning-search', '0x201b21c', None, None, ('search', 65, 31, 0, 2))]
    results = []
    for label, address, old, new, case in variants:
        positive = next(row for row in report['matches'] if row['address'] == address)
        source_path = ROOT / positive['source']
        original_hash = sha256(source_path)
        source = source_path.read_text()
        if old is None:
            text = source[:source.index('{')] + '{\n    for (;;) {}\n}\n'
        else:
            assert old in source
            text = source.replace(old, new)
        assert text != source
        folder = ROOT / 'work/main-memory-primitives-controls-20261030' / label
        folder.mkdir(parents=True, exist_ok=True)
        path = ROOT / 'nonmatching/main-runtime/20261030/memory-primitives-controls' / (label + '.c')
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
            linker.validate(row, {}, directory)
        except ValueError as error:
            failure = str(error)
            assert 'matchingBytes' in failure
        else:
            raise AssertionError('IncorrectSourceAccepted')
        payload = (directory / 'caller.bin').read_bytes()
        assert len(payload) == size and size <= positive['bytes']
        candidate = bytearray(native)
        start = int(address, 0) - 0x02000000
        candidate[start:start + size] = payload
        try:
            execute(bytes(candidate), case, 0)
        except AssertionError:
            rejected = True
        else:
            raise AssertionError('IncorrectSourcePassedIndependentModel')
        assert sha256(source_path) == original_hash
        results.append({'control': label, 'source': path.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(path),
                        'objectSha256': sha256(obj), 'linkedBytes': size, 'realLinkComparisonRejected': True,
                        'independentContractRejected': rejected, 'linkFailure': failure, 'sourceCredit': 0})
    files = ['validate_main_memory_primitives_20261030.py', 'main_memory_primitives_native_20261030.py']
    write_json(ROOT / 'evidence/verification/main-memory-primitives-controls-20261030.json',
               {'status': 'passed', 'controls': len(results), 'sourceCredit': 0, 'positiveSourcesUnchanged': True,
                'positiveReportSha256': sha256(positive_path), 'results': results,
                'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in files]})
    print({'controls': len(results), 'allRejected': True, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
