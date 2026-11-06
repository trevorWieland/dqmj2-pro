import json
import time
from project import ROOT, read_json, write_json, sha256
from linked_source_range_index_20261105 import LinkedSourceRanges, original_contains


def main():
    names = ['ledger/functions.jsonl', 'evidence/linking/latest.json',
        'evidence/linking/arm7-latest.json', 'evidence/linking/utility-latest.json']
    before = {name: sha256(ROOT / name) for name in names}
    rows = [json.loads(line) for line in (ROOT / names[0]).read_text(encoding='utf-8').splitlines()]
    units = [unit for name in names[1:] for unit in read_json(ROOT / name).get('sourceUnits', [])]
    queries = [(r['module'], int(r['address'], 0), r['bytes'], r['objectSha256'])
        for r in rows if r['states']['functionMatched']]
    started = time.perf_counter()
    expected = [original_contains(units, *q) for q in queries]
    original_seconds = time.perf_counter() - started
    started = time.perf_counter()
    index = LinkedSourceRanges(units)
    actual = [index.contains(*q) for q in queries]
    indexed_seconds = time.perf_counter() - started
    assert expected == actual
    fixtures = [dict(module='main', sha256='a', start='0x2000000', end='0x2000010'),
        dict(module='utility-child-arm9-main', sha256='a', start='0x2000000', end='0x2000020'),
        dict(module='main', sha256='b', start='0x2000000', end='0x2000010'),
        dict(module='main', sha256='a', start='0x2000008', end='0x2000018')]
    fixture_index = LinkedSourceRanges(fixtures)
    checked = 0
    for module in ['main', 'utility-child-arm9-main', 'ov000', 'arm7-main']:
        for digest in ['a', 'b', 'missing']:
            for address in [0x1fffffe, 0x2000000, 0x2000008, 0x200000e, 0x2000010, 0x2000018, 0x2000020]:
                for size in [0, 2, 4, 8, 16, 24, 32]:
                    q = module, address, size, digest
                    assert original_contains(fixtures, *q) == fixture_index.contains(*q)
                    checked += 1
    assert before == {name: sha256(ROOT / name) for name in names}, 'Inputs changed during read-only comparison'
    write_json(ROOT / 'evidence/verification/linked-source-range-index-20261105.json', dict(
        passed=True, sourceCredit=0, productionAdopted=False, actualQueries=len(queries),
        actualUnits=len(units), actualPredicatesIdentical=True, boundaryNamespaceHashControls=checked,
        originalSeconds=original_seconds, indexedSecondsIncludingConstruction=indexed_seconds,
        exactPredicate='module equality, original start/end containment, exact object SHA', inputHashes=before,
        helperSha256=sha256(ROOT / 'linked_source_range_index_20261105.py'),
        originalLedgerImplementationUnmodified=True, fullOriginalAcceptanceSuiteStillRequired=True))
    print(dict(passed=True, queries=len(queries), controls=checked,
        originalSeconds=original_seconds, indexedSeconds=indexed_seconds, productionAdopted=False))


if __name__ == '__main__':
    main()
