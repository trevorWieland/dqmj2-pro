import hashlib
from project import ROOT, read_json, sha256, write_json
import match_runtime as compiler
import link_runtime_unit as linker
import match_main_format_core_20261030 as producer
from main_format_core_native_20261030 import execute


def main():
    report = read_json(ROOT / 'evidence/matches/main-format-core-20261030.json')
    entry = report['matches'][0]
    source = (ROOT / entry['source']).read_text()
    assert sha256(ROOT / entry['source']) == entry['sourceSha256']
    metadata, native, config = linker.measured_module('main')
    work = ROOT / 'work/main-format-core-controls-20261030'
    work.mkdir(parents=True, exist_ok=True)
    failure, unused = producer.failure_callback()
    variants = [('wrong-initial-count', source.replace('chars_written = 0;', 'chars_written = 1;'), b'literal', [], b'literal', None),
                ('wrong-total-update', source.replace('chars_written += field_width;', 'chars_written -= field_width;'), b'%d', [17], b'17', None),
                ('wrong-writer-failure-result', source.replace('return -1;', 'return 0;'), b'literal', [], b'', failure)]
    start = source.index('{', source.index('int native_main_0201cb74'))
    variants.append(('nonreturning-loop', source[:start + 1] + '\n    for (;;) {}\n}\n', b'', [], b'', None))
    results = []
    for label, text, fmt, arguments, expected, callback in variants:
        assert text != source
        path = ROOT / 'nonmatching/main-runtime/20261030/format-core-controls' / (label + '.c')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        compiler.WORK = work / label / 'compile'
        rows, unused = compiler.compare(path, 'main', '3', 'off', True)
        assert len(rows) == 1 and not rows[0]['exactAfterDeclaredRelocation']
        row = rows[0]
        directory = work / label / 'real-link'
        try:
            linker.validate(row, producer.BINDINGS, directory)
        except ValueError as error:
            link_error = str(error)
            assert 'matchingBytes' in link_error, link_error
        else:
            raise AssertionError('WrongSourceAcceptedByLinkerComparison')
        payload = (directory / 'caller.bin').read_bytes()
        assert len(payload) <= 2084
        candidate = bytearray(native)
        candidate[0x1CB74:0x1CB74 + len(payload)] = payload
        try:
            execute(bytes(candidate), fmt, arguments, expected, 64, 0, 1, callback)
        except AssertionError:
            rejected = True
        else:
            raise AssertionError('WrongSourcePassedIndependentNativeContract')
        results.append({'control': label, 'source': path.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(path),
                        'compiledBytes': len(payload), 'objectSha256': row['objectSha256'],
                        'linkedPayloadSha256': hashlib.sha256(payload).hexdigest(),
                        'realLinkComparisonRejected': True, 'nativeContractRejected': rejected,
                        'sourceCredit': 0, 'linkFailure': link_error})
    assert sha256(ROOT / entry['source']) == entry['sourceSha256']
    path = ROOT / 'evidence/verification/main-format-core-controls-20261030.json'
    write_json(path, {'status': 'passed', 'controls': len(results), 'sourceCredit': 0,
                     'positiveSourceUnchanged': True, 'positiveReportSha256': sha256(ROOT / 'evidence/matches/main-format-core-20261030.json'),
                     'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in
                        ['validate_main_format_core_20261030.py', 'main_format_core_native_20261030.py']], 'results': results})
    print({'controls': len(results), 'allRejected': True, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
