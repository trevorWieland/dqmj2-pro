import re
from project import ROOT, read_json, write_json, sha256


def main():
    symbol_name = 'config/arm9/symbols.txt'
    symbols = (ROOT / symbol_name).read_text(encoding='utf-8').splitlines()
    measured = []
    for line in symbols:
        match = re.search(r' addr:(0x[0-9a-fA-F]+)(?:\s|$)', line)
        assert match
        measured.append((int(match[1], 0), line))
    results = []
    for lane, expected_count, expected_bytes, expected_sha in [
        ('gamespy-gp-character-data', 259, 3696, '9d9fb10cf08ed3cc5a0fd44b61a40267dbb2e2f5e07b5a02a21c8a32c7b990a6'),
        ('auth-character-data', 102, 1431, '02be137cee4d5da3d0311cd4c62335d1192d29f1ed1fd672d481eb892b001ed4')]:
        name = f'evidence/lanes/parallel-wave20261106/{lane}/data-claim.json'
        assert sha256(ROOT / name) == expected_sha
        rows = read_json(ROOT / name)['claimedStorage']
        assert len(rows) == expected_count and sum(row['bytes'] for row in rows) == expected_bytes
        reviews = []
        for row in rows:
            start = int(row['address'], 0)
            assert (row['program'], row['processor'], row['module']) == ('', 'arm9', 'main')
            starts = [line for at, line in measured if at == start]
            assert len(starts) == 1
            assert not any(start < at < start + row['bytes'] for at, line in measured)
            reviews.append(dict(address=row['address'], bytes=row['bytes'], exactStartRecord=starts[0],
                allNormalAndTrailingQualifiedInteriorRecords=[]))
        results.append(dict(claim=dict(path=name, sha256=expected_sha), objects=len(rows), bytes=expected_bytes,
            allNormalAndTrailingQualifiedSymbolsScanned=True, interiorRecords=0, reviews=reviews))
    write_json(ROOT / 'evidence/verification/character-storage-all-symbol-qualifiers-audit-20261106.json',
        dict(passed=True, sourceCredit=0, originalAdmittersClaimsSourcesReadysUnchanged=True,
            originalSymbols=dict(path=symbol_name, sha256=sha256(ROOT / symbol_name)), results=results,
            generatorSha256=sha256(__file__)))
    print(dict(passed=True, objects=361, initializedCandidateBytes=5127, sourceCredit=0))


if __name__ == '__main__':
    main()
