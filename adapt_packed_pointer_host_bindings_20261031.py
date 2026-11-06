import argparse
import copy
import subprocess
import sys
import match_mechanics_save_20261031_lane_packed_pointer_abi
import match_mechanics_save_20261031_lane_packed_classify
from project import ROOT, read_json, write_json, sha256, configuration
from link_runtime_unit import measured_module
from native_bindings import main_thumb_targets, scoped_bindings, merge_target

RAW = 'evidence/matches/mechanics-save-20261031-lane-packed-pointer-abi.json'
OUTPUT = 'evidence/matches/mechanics-save-20261031-lane-packed-pointer-abi-host-bindings.json'
LEGACY = 'evidence/matches/main-thumb-runtime02.json'
ADDRESSES = {0x02096CE8, 0x02096CF8, 0x02096D04, 0x02096D24, 0x02096D4C, 0x02096D6C, 0x02096D9C}
CLASSIFY = 'evidence/matches/mechanics-save-20261031-lane-packed-classify.json'
CLASSIFY_OUTPUT = 'evidence/matches/mechanics-save-20261031-lane-packed-classify-host-bindings.json'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--existing', action='store_true')
    args = parser.parse_args()
    if not args.existing:
        subprocess.run([sys.executable, str(ROOT / 'match_mechanics_save_20261031_lane_packed_pointer_abi.py')], cwd=ROOT, check=True)
        subprocess.run([sys.executable, str(ROOT / 'match_mechanics_save_20261031_lane_packed_classify.py')], cwd=ROOT, check=True)
    raw = read_json(ROOT / RAW)
    assert raw['romSha256'] == configuration()['romSha256']
    module, binary, unused = measured_module('main')
    assert raw['arm9Sha256'] == module['sha256']
    assert raw['migrationOnly'] and len(raw['matches']) == 6
    assert sum(row['bytes'] for row in raw['matches']) == 140
    entries = raw['nativeSymbolEntries']
    assert set(entries) == set(raw['nativeSymbols']) == set(raw['nativeSymbolModules'])
    before = scoped_bindings([ROOT / LEGACY, ROOT / RAW])
    name = before[ROOT / RAW]['native_fn_02096cf8']
    assert name.startswith('__binding_main_')
    bindings = {}
    merge_target(bindings, name, '0x2096cf8')
    try:
        merge_target(bindings, name, '0x2096cf9')
    except ValueError:
        rejected = True
    else:
        raise ValueError('Original scoped alias no longer reproduces the failure')
    changed = set()
    for input_path, output_path, functions, size in [(RAW, OUTPUT, 6, 140), (CLASSIFY, CLASSIFY_OUTPUT, 1, 112)]:
        original = read_json(ROOT / input_path)
        assert original['romSha256'] == raw['romSha256'] and original['arm9Sha256'] == module['sha256']
        assert len(original['matches']) == functions and sum(row['bytes'] for row in original['matches']) == size
        document = copy.deepcopy(original)
        removed = {}
        for symbol, scope in original['nativeSymbolModules'].items():
            if not symbol.startswith('native_fn_'):
                continue
            address = int(original['nativeSymbols'][symbol], 0)
            if address not in ADDRESSES:
                continue
            entry = original['nativeSymbolEntries'][symbol]
            assert address in main_thumb_targets() and symbol.endswith(f'{address:08x}')
            assert entry['module'] == scope == 'main' and entry['mode'] == 'thumb' and entry['kind'] == 'function'
            removed[symbol] = scope
            del document['nativeSymbolModules'][symbol]
            changed.add(symbol)
        document['integrationBindingScopeRepair'] = dict(
            rawReport=input_path, rawReportSha256=sha256(ROOT / input_path), legacyReport=LEGACY,
            legacyReportSha256=sha256(ROOT / LEGACY), explicitMainEvidenceRetained='nativeSymbolEntries',
            removedRedundantMainScopes=removed, originalFailureReproduced=rejected,
            originalObjectsAndTargetsUnchanged=True, frameworkModified=False, sourceCredit=0)
        document['generator'] = 'adapt_packed_pointer_host_bindings_20261031.py'
        document['generatorSha256'] = sha256(__file__)
        assert document['matches'] == original['matches'] and document['nativeSymbols'] == original['nativeSymbols']
        write_json(ROOT / output_path, document)
    assert changed == {f'native_fn_{address:08x}' for address in ADDRESSES}
    after = scoped_bindings([ROOT / LEGACY, ROOT / OUTPUT, ROOT / CLASSIFY_OUTPUT])
    assert 'native_fn_02096cf8' not in after[ROOT / OUTPUT]
    bindings = {}
    merge_target(bindings, 'native_fn_02096cf8', '0x2096cf8')
    merge_target(bindings, 'native_fn_02096cf8', '0x2096cf9')
    assert bindings['native_fn_02096cf8'] == '0x2096cf8'
    assert not any(symbol in aliases for aliases in after.values() for symbol in changed)
    print(dict(frozenFrameworksUnchanged=True, bindingScopesAligned=len(changed), unchangedFunctions=7, sourceCredit=0))


if __name__ == '__main__':
    main()
