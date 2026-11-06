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

ORACLE = 'evidence/application/save-core-page-count282-20261101.json'
PORT = 'evidence/ports/save-core-page-count-windows283-20261101.json'
CASE = 'e08143aa3f2c3fa53d8674bb78fefa6491ffd0badfcb1fa733f2e3abeea91dc8'
CONTROL = 'fb16567e273cebc686f538bf258e92aa02917acc2638f26f9aa21bc514f6d06b'
WINDOWS_CASE = 'dfc091397eca48eb6bc17751006af17446ebb3ef222220a4b508ac67bb1c2c6f'
SOURCES = {0x0206E634: '6e67d18fab52aaad83209668b631a20c63bee31b88c610e3bcf866025c6cb329',
           0x0206E644: '35ff9601a3b19289cd5b30780824f7cc28242f2e7105f5676499328c21d5cce3'}


def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    producers = ['evidence/application/save_core_page_count282_fixtures_20261101.py',
                 'check_save_core_page_count_windows283_20261101.py']
    for producer in producers:
        process = subprocess.run([sys.executable, str(ROOT / producer)], cwd=ROOT, capture_output=True, text=True, timeout=600)
        assert process.returncode == 0, process.stdout + process.stderr
    oracle = json.loads((ROOT / ORACLE).read_text())
    port = json.loads((ROOT / PORT).read_text())
    assert oracle['nativeCaseSha256'] == CASE and oracle['controls']['nativeCaseSha256'] == CONTROL
    assert oracle['pairs'] == 3486 and oracle['actualTopReturns'] == 6972
    assert oracle['actualSetterHelperReturns'] == 3486 and oracle['suppliedServiceCalls'] == 10458
    assert oracle['controls']['actualReturns'] == 48 and oracle['controls']['rejectedCases'] == 15
    assert oracle['controls']['positiveCases'] == 9
    assert oracle['codeCoverage'] == {'0x206e634': [0, 4, 8], '0x206e644': list(range(0, 92, 4))}
    for sidecar, expected in [(oracle['sidecar'], CASE), (oracle['controls']['sidecar'], CONTROL)]:
        raw = (ROOT / sidecar['path']).read_bytes()
        assert sha(raw) == sidecar['sha256'] and sha(gzip.decompress(raw)) == expected
    assert port['nativeCaseSha256'] == CASE and port['windowsCaseSha256'] == WINDOWS_CASE
    assert port['actualPublicCalls'] == 3486 and port['totalActualPublicCalls'] == 3582
    assert port['actualGoodControlCalls'] == port['actualWrongControlCalls'] == 48
    assert sum(row['rejected'] for row in port['controls']) == 30
    for variant in [port['source'], *port['wrongSources']]:
        for source in variant['objects']:
            assert sha((ROOT / source['source']).read_bytes()) == source['sourceSha256']
            assert sha((ROOT / source['object']).read_bytes()) == source['objectSha256']
            assert source['objectTimeDateStamp'] == 0
    matches, entries, cache = [], {}, {}
    for raw_row, previous in zip(oracle['matches'], oracle['previousSources']):
        row = dict(raw_row)
        row.update(row['realLinkSnapshot'])
        address = int(row['address'], 0)
        assert row['sourceSha256'] == SOURCES[address]
        assert sha((ROOT / previous['source']).read_bytes()) == previous['sha256']
        assert row['compiledBytes'] == row['bytes'] and row['exactByteEqual'] and dependencies_current(row)
        for path, digest in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                             ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                             ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
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
            target = int(relocation['target'], 0)
            entries[relocation['symbol']] = (data_entry if relocation['kind'] == 'data' else native_entry)('main', target, cache)
        row.update(outputSha256=sha(linked), linked=False, exactBytes=row['bytes'], exactAfterDeclaredRelocation=True,
            exactAfterRealMwLink=True, netNewFunctions=0, netNewBytes=0, primaryReplacementCandidate=True,
            oldSource=previous['source'], oldSourceSha256=previous['sha256'],
            oracle=dict(supported=True, cases=1743, actualReturns=3486, report=ORACLE,
                reportSha256=sha((ROOT / ORACLE).read_bytes()), limits=oracle['limits']),
            returnContract=dict(sourceReturnType='u32', physicalR0Compared=True, apiReturnProven=True,
                qualifiedInput='raw32bit word', qualifiedReturn='unchanged incomingword', additionalProviderLimits=address == 0x0206E644))
        matches.append(row)
    assert len(matches) == 2 and sum(row['bytes'] for row in matches) == 108
    deps = runtime_files() | set(producers) | {ORACLE, PORT, oracle['sidecar']['path'], oracle['controls']['sidecar']['path'],
        'evidence/application/save_core_page_count280_build_20261101.py',
        'evidence/application/save_core_page_count281_machine_20261101.py',
        'evidence/application/save_core_roster_initializer250_machine_20261101.py',
        'evidence/application/save_core_measured_inputs140_machine_20261101.py',
        'evidence/application/save_core_historical_link_20261031.py',
        'ports/windows-native/page_count283_services.c', 'match_mechanics_save_20261101_lane_page_count_word.py',
        'provenance/seed-manifest.json'}
    deps.update(row['source'] for row in matches + oracle['controls']['rows'] + oracle['previousSources'])
    deps.update(v[0]['symbolsFile'] for v in cache.values())
    verify_inputs()
    output = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA,
        matches=matches, matchedFunctions=2, matchedBytes=108, netNewFunctions=0, netNewBytes=0,
        primaryReplacementCandidate=True, jointOverlayDeclarationRequired='ov000:ARM02204DEC',
        nativeSymbolEntries=entries, nativeSymbols={name: row['address'] for name, row in entries.items()},
        nativeSymbolModules={}, sourceDependencies=[], replayDependencies=[file_identity(path) for path in sorted(deps)],
        replayRequires=[], oracle=dict(pairs=3486, actualReturns=6972, actualSetterHelperReturns=3486,
            suppliedServiceCalls=10458, nativeCaseDigest=CASE, report=ORACLE),
        negativeControls=dict(actualReturns=48, rejectedCases=15, positiveCases=9, nativeCaseDigest=CONTROL),
        portableValidation=dict(report=PORT, sha256=sha((ROOT / PORT).read_bytes()),
            actualWindowsReturns=3486, actualGoodControlReturns=48, actualWrongControlReturns=48,
            nativeCaseDigest=CASE, windowsCaseDigest=WINDOWS_CASE),
        wholeLinkedRebuild=False, registrationPerformedByThisScript=False, inputsUnchanged=True, limitations=oracle['limits'])
    target = ROOT / 'evidence/matches/mechanics-save-20261101-lane-page-count-word.json'
    target.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(dict(functions=2, matchedBytes=108, netNewBytes=0, actualReturns=6972,
        windowsReturns=3582, reportSha256=sha(target.read_bytes()))))


if __name__ == '__main__':
    main()
