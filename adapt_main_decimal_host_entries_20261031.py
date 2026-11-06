import argparse
import copy
import subprocess
import sys
import match_main_decimal_pow2_20261031
import match_main_decimal_from_double_20261031
from project import ROOT, configuration, read_json, sha256, write_json
from recover_linked_runtime import qualified_bindings


UNITS = {
    'pow2': ('main-decimal-pow2-20261031', 'match_main_decimal_pow2_20261031.py', 0x02022D80, 900),
    'from-double': ('main-decimal-from-double-20261031', 'match_main_decimal_from_double_20261031.py', 0x02023568, 384),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('unit', choices=UNITS)
    parser.add_argument('--existing', action='store_true')
    options = parser.parse_args()
    name, producer, address, size = UNITS[options.unit]
    if not options.existing:
        subprocess.run([sys.executable, str(ROOT / producer)], cwd=ROOT, check=True)
    relative = 'evidence/matches/' + name + '.json'
    raw = read_json(ROOT / relative)
    assert raw['romSha256'] == configuration()['romSha256']
    assert len(raw['matches']) == 1 and isinstance(raw['nativeSymbolEntries'], list)
    row = raw['matches'][0]
    assert row['processor'] == 'arm9' and row['module'] == 'main' and row['mode'] == 'arm'
    assert int(row['address'], 0) == address and row['bytes'] == size and row['compiledBytes'] == size
    assert row['exactAfterDeclaredRelocation'] and row['exactAfterRealMwLink']
    for key in ['source', 'object']:
        assert sha256(ROOT / row[key]) == row[key + 'Sha256']
    entries = {}
    for item in raw['nativeSymbolEntries']:
        assert item['name'] not in entries
        entries[item['name']] = {key: value for key, value in item.items() if key != 'name'}
    assert entries == qualified_bindings(row)
    assert raw['nativeSymbols'] == {name: binding['address'] for name, binding in entries.items()}
    report = copy.deepcopy(raw)
    report['nativeSymbolEntries'] = entries
    report['hostEntryMetadataAdapter'] = dict(path='adapt_main_decimal_host_entries_20261031.py',
        sha256=sha256(__file__), rawReport=relative, rawReportSha256=sha256(ROOT / relative),
        change='Represent existing verified named entries in the frozen linker map schema',
        sourceChanges=0, objectChanges=0, targetChanges=0, sourceCoverageChanges=0)
    output = 'evidence/matches/' + name + '-host-bindings.json'
    write_json(ROOT / output, report)
    print(dict(report=output, typedEntries=len(entries), sourceAndObjectUnchanged=True))


if __name__ == '__main__':
    main()
