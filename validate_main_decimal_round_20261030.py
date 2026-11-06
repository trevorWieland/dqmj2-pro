import os
import subprocess
from project import ROOT, read_json, sha256, write_json
import link_runtime_unit as linker
from main_decimal_round_native_20261030 import execute
from elftools.elf.elffile import ELFFile


def main():
    positive_path = ROOT / 'evidence/matches/main-decimal-round-20261030.json'
    report = read_json(positive_path)
    positive = report['matches'][0]
    source_path = ROOT / positive['source']
    original_hash = sha256(source_path)
    source = source_path.read_text()
    start = source.index('{', source.index('void native_main_0201c2ec'))
    variants = [('wrong-tie-parity', source.replace('p[-1] & 1', '0'), ('15', 1, 0, False)),
                ('wrong-exponent-carry', source.replace('dec->exp += 1;', 'dec->exp -= 1;'), ('99', 1, 32767, True)),
                ('wrong-zero-digit', source.replace("*dec->sig.text = '0';", "*dec->sig.text = '1';"), ('5', -1, 0, False)),
                ('nonreturning-loop', source[:start + 1] + '\n    for (;;) {}\n}\n', ('5', 0, 0, True))]
    metadata, native, config = linker.measured_module('main')
    results = []
    for label, text, case in variants:
        assert text != source
        folder = ROOT / 'work/main-decimal-round-controls-20261030' / label
        folder.mkdir(parents=True, exist_ok=True)
        path = ROOT / 'nonmatching/main-runtime/20261030/decimal-round-controls' / (label + '.c')
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
        assert len(payload) == size and size <= 292
        candidate = bytearray(native)
        candidate[0x1C2EC:0x1C2EC + size] = payload
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
    files = ['validate_main_decimal_round_20261030.py', 'main_decimal_round_native_20261030.py']
    write_json(ROOT / 'evidence/verification/main-decimal-round-controls-20261030.json',
        {'status': 'passed', 'controls': len(results), 'sourceCredit': 0, 'positiveSourceUnchanged': True,
         'positiveReportSha256': sha256(positive_path), 'results': results,
         'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in files]})
    print({'controls': len(results), 'allRejected': True, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
