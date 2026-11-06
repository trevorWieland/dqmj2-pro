import os
import subprocess
from project import ROOT, read_json, sha256, write_json
import link_runtime_unit as linker
from main_format_parser_native_20261030 import execute
from elftools.elf.elffile import ELFFile


def main():
    positive_path = ROOT / 'evidence/matches/main-format-parser-20261030.json'
    report = read_json(positive_path)
    positive = report['matches'][0]
    assert positive['boundaries']['instructionBytes'] == 1416
    assert positive['boundaries']['compilerAlignmentPaddingBytes'] == 4
    assert positive['boundaries']['literalPoolBytes'] == 4
    seen = {pc for row in report['oracle']['rows'] for pc in row['result']['pcs']}
    assert seen == set(range(0x0201B338, 0x0201B338 + 1416, 4))
    with (ROOT / positive['object']).open('rb') as stream:
        elf = ELFFile(stream)
        table = elf.get_section_by_name('.symtab')
        symbol = table.get_symbol_by_name(positive['name'])[0]
        mapping = [(row.name, row['st_value']) for row in table.iter_symbols()
                   if row.name.startswith('$') and row['st_shndx'] == symbol['st_shndx']]
        assert mapping == [('$a', 0), ('$d', 1416)]
        payload = elf.get_section(symbol['st_shndx']).data()
        assert payload[1416:1420] == bytes(4)
    metadata, native, config = linker.measured_module('main')
    variants = [('wrong-width-cap', '0x201b338', 'f.field_width > 509', 'f.field_width > 508', (b'%509dZ', ())),
                ('wrong-sign-priority', '0x201b338', 'f.sign_options != sign_always', 'f.sign_options == sign_always', (b'%+ dZ', ())),
                ('wrong-wide-character-kind', '0x201b338', 'f.argument_options = wchar_argument;', 'f.argument_options = normal_argument;', (b'%lcZ', ())),
                ('nonreturning-parser', '0x201b338', None, None, (b'%dZ', ()))]
    results = []
    for label, address, old, new, case in variants:
        positive = next(row for row in report['matches'] if row['address'] == address)
        source_path = ROOT / positive['source']
        original_hash = sha256(source_path)
        source = source_path.read_text()
        if old is None:
            text = source[:source.index('{', source.index(positive['name']))] + '{\n    for (;;) {}\n}\n'
        else:
            assert old in source
            text = source.replace(old, new)
        assert text != source
        folder = ROOT / 'work/main-format-parser-controls-20261030' / label
        folder.mkdir(parents=True, exist_ok=True)
        path = ROOT / 'nonmatching/main-runtime/20261030/format-parser-controls' / (label + '.c')
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
    files = ['validate_main_format_parser_20261030.py', 'main_format_parser_native_20261030.py']
    write_json(ROOT / 'evidence/verification/main-format-parser-controls-20261030.json',
               {'status': 'passed', 'controls': len(results), 'sourceCredit': 0, 'positiveSourcesUnchanged': True,
                'positiveReportSha256': sha256(positive_path), 'results': results,
                'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in files]})
    print({'controls': len(results), 'allRejected': True, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
