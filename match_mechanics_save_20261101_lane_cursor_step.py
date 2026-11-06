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

REPORTS = ['evidence/application/save-core-cursor292-20261101.json',
    'evidence/application/save-core-cursor293-controls-20261101.json',
    'evidence/application/save-core-cursor294-consumer-20261101.json',
    'evidence/application/save-core-cursor295-consumer-controls-20261101.json']
PRODUCERS = ['evidence/application/save_core_cursor292_fixtures_20261101.py',
    'evidence/application/save_core_cursor293_controls_20261101.py',
    'evidence/application/save_core_cursor294_consumer_20261101.py',
    'evidence/application/save_core_cursor295_consumer_controls_20261101.py']
CASES = ['b9818fa287a792f93b4dc0cf24c21406d50ac24721709aafab0be1aadf4caea2',
    '93d94e3e064de6191edf4af1882c96618f9175d2b034eedae01e7caa2700ad8f',
    '7ac314d27f69cc2f72e5898a69493bb184ad3ba49a4305151feea14a91ee85e7',
    '10a8e249b5cd7795e0c9d01457086420170b3227bf8ed20dc0b5e7a8445ab811']
SOURCES = {0x0206238C: '6bc108eb86c7b3bb7ca08f9bdb02a11e027dabc48b305d5d4fbb0d31fdc22015',
    0x0206F79C: 'f6fcc519fe86ee733e6a1745a479f8a34bc6ede242bf7c3c63b3ea429bec4a66'}
PRESERVED_CONSUMER = dict(source='src/mechanics_save/20261030_lane_menu_refresh/native_main_0206eaa0.c',
    sha256='5e06d09e97ac10fbfb4fbe1e5e4ae3a2b3f4d4a302e15592284bde73e063f183')


def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    for producer in PRODUCERS:
        process = subprocess.run([sys.executable, str(ROOT / producer)], cwd=ROOT, capture_output=True, text=True, timeout=600)
        assert process.returncode == 0, process.stdout + process.stderr
    reports = [json.loads((ROOT / path).read_text()) for path in REPORTS]
    for path, report, digest in zip(REPORTS, reports, CASES):
        assert report['nativeCaseSha256'] == digest
        packed = (ROOT / report['sidecar']['path']).read_bytes()
        assert sha(packed) == report['sidecar']['sha256'] and sha(gzip.decompress(packed)) == digest
    direct, wrong_direct, caller, wrong_caller = reports
    assert (direct['pairs'], direct['actualTopReturns'], direct['actualNativeHelperReturns'], direct['suppliedNotifications']) == (10819, 21638, 142058, 9480)
    assert direct['aliasedPointerPairs'] == 96 and direct['blockedGatePairs'] == 1045
    assert direct['codeCoverage'] == list(range(0, 248, 4))
    assert len(direct['unsupported']) == 2 and all(not row['actualReturn'] and not row['postFaultStateClaimed'] for row in direct['unsupported'])
    assert (caller['pairs'], caller['actualTopReturns'], caller['actualNativeHelperReturns'], caller['actualCursorReturns'], caller['suppliedNotifications']) == (8227, 16454, 143852, 16454, 8192)
    assert caller['codeCoverage'] == list(range(0, 84, 4))
    assert (wrong_direct['pairs'], wrong_direct['actualReturns'], wrong_direct['rejectedCases'], wrong_direct['positiveCases']) == (36, 72, 9, 27)
    assert (wrong_caller['pairs'], wrong_caller['actualReturns'], wrong_caller['rejectedCases'], wrong_caller['positiveCases']) == (18, 36, 11, 7)
    assert sha((ROOT / PRESERVED_CONSUMER['source']).read_bytes()) == PRESERVED_CONSUMER['sha256']
    previous = caller['oldSource']
    assert sha((ROOT / previous['source']).read_bytes()) == previous['sha256']
    matches, entries, cache = [], {}, {}
    for report, path in ((direct, REPORTS[0]), (caller, REPORTS[2])):
        row = dict(report['candidate'])
        row.update(row['realLinkSnapshot'])
        address = int(row['address'], 0)
        assert row['sourceSha256'] == SOURCES[address]
        assert row['compiledBytes'] == row['bytes'] and row['exactByteEqual'] and dependencies_current(row)
        for key, digest in [('source', 'sourceSha256'), ('object', 'objectSha256'),
            ('isolatedCallerBinary', 'isolatedCallerBinarySha256'), ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT / row[key]).read_bytes()) == row[digest]
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
        replacement = address == 0x0206F79C
        row.update(outputSha256=sha(linked), linked=False, exactBytes=row['bytes'], exactAfterDeclaredRelocation=True,
            exactAfterRealMwLink=True, primaryReplacementCandidate=replacement,
            netNewFunctions=0 if replacement else 1, netNewBytes=0 if replacement else row['bytes'],
            oracle=dict(supported=True, cases=report['pairs'], actualReturns=report['actualTopReturns'],
                report=path, reportSha256=sha((ROOT / path).read_bytes()), limits=report['limits']),
            returnContract=dict(sourceReturnType='void' if replacement else 'u32', physicalR0Compared=True,
                apiReturnProven=not replacement, qualifiedReturn='incidental physical R0 only' if replacement else 'raw word FFFFFFFF,0,1 representing signed step -1,0,+1'))
        if replacement:
            row.update(oldSource=previous['source'], oldSourceSha256=previous['sha256'])
        matches.append(row)
    assert sum(row['bytes'] for row in matches) == 344 and sum(row['netNewBytes'] for row in matches) == 252
    deps = runtime_files() | set(PRODUCERS) | set(REPORTS) | {
        'evidence/application/save_core_cursor288_machine_20261101.py',
        'evidence/application/save_core_roster_initializer250_machine_20261101.py',
        'evidence/application/save_core_measured_inputs140_machine_20261101.py',
        'evidence/application/save_core_historical_link_20261031.py', 'provenance/seed-manifest.json',
        'match_mechanics_save_20261101_lane_cursor_step.py', previous['source'], PRESERVED_CONSUMER['source']}
    deps.update(report['sidecar']['path'] for report in reports)
    deps.update(row['source'] for row in matches + wrong_direct['candidates'] + wrong_caller['candidates'])
    deps.update(value[0]['symbolsFile'] for value in cache.values())
    verify_inputs()
    output = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA,
        matches=matches, matchedFunctions=2, matchedBytes=344, netNewFunctions=1, netNewBytes=252,
        nativeSymbolEntries=entries, nativeSymbols={name: row['address'] for name, row in entries.items()}, nativeSymbolModules={},
        sourceDependencies=[], replayDependencies=[file_identity(path) for path in sorted(deps)], replayRequires=[],
        jointPrimarySelectionRequired=[dict(module='main', address='0x0206F79C', source=matches[1]['source'], sourceSha256=matches[1]['sourceSha256'])],
        preservedExistingConsumer=PRESERVED_CONSUMER,
        oracle=dict(directPairs=10819, directActualReturns=21638, callerPairs=8227, callerActualReturns=16454,
            actualOriginalHelperReturns=285910, actualCursorNestedReturns=16454, suppliedMutedNotifications=17672,
            cases=CASES, reports=REPORTS),
        negativeControls=dict(actualReturns=108, rejectedCases=20, positiveCases=34),
        wholeLinkedRebuild=False, registrationPerformedByThisScript=False, inputsUnchanged=True,
        limitations=direct['limits'] + caller['limits'] + ['The two source definitions form a u32(s8*,s32,s32) input-helper/typed-pointer consumer closure. The existing 396-byte u32 consumer is preserved.',
            'Changing the 396-byte consumer return declaration to s8 compiled only392bytes, so no narrow-return primary was selected. Original declaration text is not recovered from that experiment.',
            'There are no actual Windows or Android executions in this packet and no ordinary scene or saved-state semantics are inferred.'])
    path = ROOT / 'evidence/matches/mechanics-save-20261101-lane-cursor-step.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(dict(matchedFunctions=2, matchedBytes=344, newFunctions=1, newBytes=252,
        nativeSourceActualReturns=38092, negativeActualReturns=108, reportSha256=sha(path.read_bytes()))))


if __name__ == '__main__':
    main()
