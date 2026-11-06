import gzip
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'evidence/application'), str(ROOT / 'deps/native')]
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, ROM_SHA, SAVE_SHA, MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry
from match_mechanics_save_20261029_item_use import data_entry
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
from source_dependencies import dependencies_current

REPORT = 'evidence/application/save-core-latch309-20261101.json'
CONTROL = 'evidence/application/save-core-latch311-controls-20261101.json'
WINDOWS = 'evidence/ports/save-core-latch-windows310-20261101.json'
LEAF_CASE = '22864949c7b813aea9c9c3dd5d93eceee69838e656f8de8c51a9ffbda98bef28'
MENU_CASE = '82519c9ccf1b85a9e35b0c0b92a9e3f3a943c654fd3b59131a6433f75e539234'
CONTROL_CASE = '201402a5d2ffd8f74e0ec3287a3a58cead3176c69781d2d7f4189f1f95ad41b0'
WINDOWS_CASE = '131af7476e4dad03d2e89322513b4e438086e8c3c74f657be5a9be5fc4d77245'
SOURCE_PINS = {0x02062358: 'f7817dc161c0b161bb143f31dedcc7be189e3333af92152164416cf6e007ea33'}
PREVIOUS = {0x02062358: ('src/runtime/runtime07/native_main_02062358.c', 'afbab4707188657071a07b87ab9a96460134db6f769f2ae3bf8142ab40dec30c'),
    0x0206EAA0: ('src/mechanics_save/20261030_lane_menu_refresh/native_main_0206eaa0.c', '5e06d09e97ac10fbfb4fbe1e5e4ae3a2b3f4d4a302e15592284bde73e063f183')}


def packed(sidecar, digest):
    raw = (ROOT / sidecar['path']).read_bytes()
    assert sha(raw) == sidecar['sha256'] and sha(gzip.decompress(raw)) == digest


def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    producers = ['evidence/application/save_core_latch309_fixtures_20261101.py',
        'evidence/application/save_core_latch311_controls_20261101.py', 'check_save_core_latch_windows310_20261101.py']
    for producer in producers:
        process = subprocess.run([sys.executable, str(ROOT / producer)], cwd=ROOT, capture_output=True, text=True, timeout=600)
        assert process.returncode == 0, process.stdout + process.stderr
    oracle, controls, port = [json.loads((ROOT / path).read_text()) for path in (REPORT, CONTROL, WINDOWS)]
    assert oracle['leafCaseSha256'] == LEAF_CASE and oracle['menuCaseSha256'] == MENU_CASE
    assert (oracle['leafPairs'], oracle['actualLeafReturns'], oracle['menuPairs'], oracle['actualMenuReturns']) == (1536, 3072, 672, 1344)
    assert oracle['actualMenuNativeHelperReturns'] == 36776 and oracle['suppliedMenuCalls'] == 13552
    assert controls['nativeCaseSha256'] == CONTROL_CASE
    assert (controls['actualReturns'], controls['rejectedCases'], controls['positiveCases']) == (54, 16, 11)
    packed(oracle['leafSidecar'], LEAF_CASE)
    packed(oracle['menuSidecar'], MENU_CASE)
    packed(controls['sidecar'], CONTROL_CASE)
    assert port['nativeCaseSha256'] == LEAF_CASE and port['windowsCaseSha256'] == WINDOWS_CASE
    assert (port['actualPublicCalls'], port['actualGoodControlCalls'], port['actualWrongControlCalls']) == (1536, 27, 27)
    assert sum(row['rejected'] for row in port['controls']) == 16
    for item in [port['source'], *port['wrongSources']]:
        for row in item['objects']:
            assert sha((ROOT / row['source']).read_bytes()) == row['sourceSha256']
            assert sha((ROOT / row['object']).read_bytes()) == row['objectSha256'] and row['objectTimeDateStamp'] == 0
    matches, entries, cache = [], {}, {}
    for candidate in oracle['matches']:
        row = dict(candidate)
        row.update(row['realLinkSnapshot'])
        address = int(row['address'], 0)
        if address in SOURCE_PINS:
            assert row['sourceSha256'] == SOURCE_PINS[address]
        else:
            before = (ROOT / PREVIOUS[address][0]).read_text()
            expected = before.replace('extern void native_fn_02062358(u32 value);', 'extern u32 native_fn_02062358(u32 value);')
            assert (ROOT / row['source']).read_text() == expected and expected != before
        assert sha((ROOT / PREVIOUS[address][0]).read_bytes()) == PREVIOUS[address][1]
        assert row['compiledBytes'] == row['bytes'] and row['exactByteEqual'] and dependencies_current(row)
        for path, digest in [('source', 'sourceSha256'), ('object', 'objectSha256'),
            ('isolatedCallerBinary', 'isolatedCallerBinarySha256'), ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT / row[path]).read_bytes()) == row[digest]
        entries[row['name']] = native_entry('main', address, cache)
        metadata, binary, config = cache['main']
        offset = address - int(metadata['base'], 0)
        native = binary[offset:offset + row['bytes']]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        assert linked == native and validation['exactCallerBytes'] and validation['sourceSha256'] == row['sourceSha256']
        assert validation['sourceObjectSha256'] == row['objectSha256']
        assert validation['linkedCallerSha256'] == validation['nativeSpanSha256'] == sha(native)
        assert validation['linkerSha256'] == 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        assert validation['linkerAttempt']['exitCode'] == 0
        for relocation in row['relocations']:
            entries[relocation['symbol']] = (data_entry if relocation['kind'] == 'data' else native_entry)('main', int(relocation['target'], 0), cache)
        row.update(outputSha256=sha(linked), linked=False, exactBytes=row['bytes'], exactAfterDeclaredRelocation=True,
            exactAfterRealMwLink=True, primaryReplacementCandidate=True, netNewFunctions=0, netNewBytes=0,
            oldSource=PREVIOUS[address][0], oldSourceSha256=PREVIOUS[address][1],
            oracle=dict(supported=True, cases=1536 if address == 0x02062358 else 672,
                actualReturns=3072 if address == 0x02062358 else 1344, report=REPORT,
                reportSha256=sha((ROOT / REPORT).read_bytes()), limits=oracle['limits']),
            returnContract=dict(sourceReturnType='u32', physicalR0Compared=True, apiReturnProven=True,
                qualifiedReturn='unchanged incoming raw word' if address == 0x02062358 else 'retained qualified controller word'))
        matches.append(row)
    assert sum(row['bytes'] for row in matches) == 412
    deps = runtime_files() | set(producers) | {REPORT, CONTROL, WINDOWS,
        'evidence/application/save_core_latch307_build_20261101.py',
        'evidence/application/save_core_measured_inputs140_machine_20261101.py',
        'evidence/application/save_core_roster_initializer250_machine_20261101.py',
        'evidence/application/save_core_historical_link_20261031.py',
        'evidence/application/save_core_menu_fixtures_20261030.py', 'evidence/application/save_core_menu_build_20261030.py',
        'evidence/application/save_core_menu_machine_20261030.py', 'ports/windows-native/latch310_storage.c',
        'match_mechanics_save_20261101_lane_latch_word.py', 'provenance/seed-manifest.json'}
    deps.update(row['source'] for row in matches + controls['rows'])
    deps.update(value[0] for value in PREVIOUS.values())
    deps.update(value[0]['symbolsFile'] for value in cache.values())
    deps.update(sidecar['path'] for sidecar in (oracle['leafSidecar'], oracle['menuSidecar'], controls['sidecar']))
    verify_inputs()
    output = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA,
        matches=matches, matchedFunctions=2, matchedBytes=412, netNewFunctions=0, netNewBytes=0,
        primaryReplacementCandidate=True, jointOverlayHeaderRequired='ov000:ARM0221B070 birth395 context.h declaration62358',
        nativeSymbolEntries=entries, nativeSymbols={name: row['address'] for name, row in entries.items()}, nativeSymbolModules={},
        sourceDependencies=[], replayDependencies=[file_identity(path) for path in sorted(deps)], replayRequires=[],
        oracle=dict(actualLeafReturns=3072, actualMenuReturns=1344, actualNativeMenuHelperReturns=36776,
            suppliedMenuCalls=13552, leafCaseDigest=LEAF_CASE, menuCaseDigest=MENU_CASE),
        negativeControls=dict(actualReturns=54, rejectedCases=16, positiveCases=11, nativeCaseDigest=CONTROL_CASE),
        portableValidation=dict(report=WINDOWS, sha256=sha((ROOT / WINDOWS).read_bytes()), actualPublicCalls=1536,
            goodControlCalls=27, wrongControlCalls=27, nativeCaseDigest=LEAF_CASE, windowsCaseDigest=WINDOWS_CASE),
        wholeLinkedRebuild=False, registrationPerformedByThisScript=False, inputsUnchanged=True, limitations=oracle['limits'])
    path = ROOT / 'evidence/matches/mechanics-save-20261101-lane-latch-word.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(dict(matchedBytes=412, netNewBytes=0, actualSourceNativeReturns=4416,
        negativeReturns=54, windowsReturns=1590, reportSha256=sha(path.read_bytes()))))


if __name__ == '__main__':
    main()
