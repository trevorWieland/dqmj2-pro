import ast
import match_runtime as compiler
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_heap_search_fixture_20261031 import execute


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    results = []
    for entry, optimization, speed in [(0x0202B044, 2, False), (0x0202B0F8, 3, True)]:
        source = ROOT / f'src/runtime/20261031_heap_block_search/native_main_{entry:08x}.c'
        text = source.read_text()
        variants = [
            ('always-first', 'heap_mode(heap) == 0', '1'),
            ('last-equal-fit', 'smallest > block->bytes', 'smallest >= block->bytes'),
            ('wrong-direction', f', {int(entry == 0x0202B0F8)});', f', {int(entry != 0x0202B0F8)});'),
            ('wrong-request', ', start, bytes,', ', start, bytes + 4,')]
        for label, previous, replacement in variants:
            assert text.count(previous) == 1
            path = ROOT / f'generated/heap-search-negative-20261101/{entry:08x}/{label}/candidate.c'
            path.parent.mkdir(parents=True, exist_ok=True)
            content = text.replace(previous, replacement)
            (path.parent / 'heap_views.h').write_bytes((source.parent / 'heap_views.h').read_bytes())
            path.write_text(content, encoding='utf-8')
            work = ROOT / f'work/heap-search-negative-20261101/{entry:08x}/{label}'
            compiler.WORK = work / 'compile'
            rows, unused = compiler.compare(path, 'main', optimization, 'on', speed=speed)
            row = rows[0]
            assert not row.get('compileFailed'), row
            try:
                validate(row, qualified_bindings(row), work / 'link')
            except ValueError as error:
                mismatch = ast.literal_eval(str(error))
            else:
                raise AssertionError('Wrong body unexpectedly matches original bytes')
            code = (work / 'link/caller.bin').read_bytes()
            failures, positives = [], 0
            for index in range(980):
                result = execute(original, code, entry, index)
                assert result['actualReturns'] == 1
                if result['modelPassed']:
                    positives += 1
                else:
                    failures.append(dict(index=index, result=result))
            assert failures and positives, (hex(entry), label)
            results.append(dict(address=hex(entry), negative=label, source=row['source'],
                sourceSha256=row['sourceSha256'], compilerResult=row, linkMismatch=mismatch,
                actualReturns=980, independentRejections=len(failures), positiveCases=positives,
                failures=failures, acceptedSourceCredit=0))
    positive = ROOT / 'evidence/attempts/main-heap-search-behavior-qualified-drafts-20261031.json'
    assert read_positive(positive)
    write_json(ROOT / 'evidence/attempts/main-heap-search-negative-controls-20261101.json', dict(
        romSha256=config['romSha256'], positiveReport=positive.relative_to(ROOT).as_posix(),
        positiveReportSha256=sha256(positive), results=results, actualReturns=sum(r['actualReturns'] for r in results),
        independentRejections=sum(r['independentRejections'] for r in results),
        sourceFunctionMatch=False, acceptedSourceCredit=0,
        limitations=['Only stable bounded lists and the supplied commit contract are tested',
            'Wrong-body rejection does not establish exact compiled bytes, real heap effects, or game scene feasibility']))
    print(dict(wrongBodies=len(results), actualReturns=sum(r['actualReturns'] for r in results),
               independentRejections=sum(r['independentRejections'] for r in results), sourceCredit=0))


def read_positive(path):
    from project import read_json
    report = read_json(path)
    return report['actualReturns'] == 3920 and report['acceptedSourceCredit'] == 0


if __name__ == '__main__':
    main()
