import argparse
import copy
import subprocess
import sys
import match_ov001_recruit373_20261031
from project import ROOT, read_json, write_json, sha256, configuration
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--existing', action='store_true')
    options = parser.parse_args()
    if not options.existing:
        subprocess.run([sys.executable, str(ROOT / 'match_ov001_recruit373_20261031.py')], cwd=ROOT, check=True)
    raw_path = 'evidence/matches/ov001-20261031-recruit373.json'
    raw = read_json(ROOT / raw_path)
    old_path = 'evidence/matches/ov001-20261031-recruit364.json'
    old = read_json(ROOT / old_path)
    assert raw['romSha256'] == old['romSha256'] == configuration()['romSha256']
    item = raw['zeroCreditCallerInterface']
    assert item['bytes'] == 1092 and item['sourceCredit'] == 0 and not item['preferredSourceChanged']
    row = copy.deepcopy(item['compilation'])
    assert row['module'] == 'ov001' and row['mode'] == 'arm' and int(row['address'], 0) == 0x02209CC0
    assert row['bytes'] == row['compiledBytes'] == row['matchingBytes'] == 1092
    assert row['exactAfterDeclaredRelocation']
    prior = next(value for value in old['matches'] if int(value['address'], 0) == 0x02209CC0)
    assert row['targetSha256'] == prior['targetSha256'] and row['relocations'] == prior['relocations']
    for key in ['source', 'object']:
        assert sha256(ROOT / row[key]) == row[key + 'Sha256']
    proof = validate(row, qualified_bindings(row), ROOT / 'work/ov001-refresh-void-caller-adoption-20261031')
    row.update(freeze_link(proof))
    row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, newFunctionCredit=0, newByteCredit=0)
    output = {key: copy.deepcopy(old[key]) for key in ['romSha256', 'nativeSymbols', 'nativeSymbolModules', 'nativeSymbolEntries'] if key in old}
    output.update(matches=[row], generator='adopt_ov001_refresh_void_caller_20261031.py', generatorSha256=sha256(__file__),
        rawReport=raw_path, rawReportSha256=sha256(ROOT / raw_path), previousReport=old_path,
        previousReportSha256=sha256(ROOT / old_path), zeroCreditSourceInterface=dict(bytes=1092, newCoverage=0),
        evidenceScope=item['scope'], limitations=[
            'Only the actor-refresh return declaration changes tovoid; caller bytes and required inputs unchanged',
            'Connected original/fresh-C native arrangements and explicit UI providers are in the frozen raw373 report',
            'No source or helper coverage beyond the previously matched1092 bytes; no whole-scene or game proof'])
    write_json(ROOT / 'evidence/matches/ov001-refresh-void-caller-20261031.json', output)
    print(dict(replacementBytes=1092, newCoverage=0, originalSourcePreserved=True))


if __name__ == '__main__':
    main()
