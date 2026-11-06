import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'evidence/application'), str(ROOT / 'deps/native')]
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, ROM_SHA, SAVE_SHA, MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry, unpack
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_cleanup_abi_pair_fixtures_20261101 as P
import save_core_cleanup_abi_pair_controls_20261101 as C
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
ORACLE = 'evidence/application/save-core-cleanup-abi-pair132-source-20261101.json'
CONTROLS = 'evidence/application/save-core-cleanup-abi-pair132-controls-20261101.json'
PROFILE = 'evidence/lanes/save-core/cleanup-abi-pair132-profile-20261101.json'
CASE = '24684e10a4dfdede89a76dfd7f12eb48b08b3e0e5a983d7ca12b06675382bca3'
CONTROL_CASE = '0be71a03a992cc664257b4a3a0b19a0b1e55529adcbd1574b6c6e97677207b8d'
PROFILE_SHA = '93bd591029f391f599447edb8db79751ddb3baca41de2cb26c7517d3e2cec6d2'

def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    assert sha((ROOT / PROFILE).read_bytes()) == PROFILE_SHA
    producers = ['evidence/application/save_core_cleanup_abi_pair_fixtures_20261101.py', 'evidence/application/save_core_cleanup_abi_pair_controls_20261101.py', 'check_save_core_cleanup_abi_pair_windows32_20261101.py']
    for producer in producers:
        process = subprocess.run([sys.executable, str(ROOT / producer)], capture_output=True, text=True, timeout=300)
        assert process.returncode == 0, process.stdout + process.stderr
    oracle = json.loads((ROOT / ORACLE).read_text())
    controls = json.loads((ROOT / CONTROLS).read_text())
    vectors = unpack(oracle['vectorSidecar'], CASE)
    negatives = unpack(controls['vectorSidecar'], CONTROL_CASE)
    assert len(vectors) == 320 and all((v['actualReturn'] for v in vectors)) and (oracle['counts']['actualMatchedReturns'] == 640) and (oracle['counts']['physicalOtherNativeReturns'] == 2944) and (oracle['counts']['providedServiceCalls'] == 960)
    assert len(negatives) == 16 and sum((v['independentRejection'] for v in negatives)) == 8 and all((v['actualOriginalReturn'] and v['actualPositiveReturn'] and v['actualWrongReturn'] for v in negatives))
    spec = json.loads((ROOT / PROFILE).read_text())
    profiles = spec['rows']
    portpath = 'evidence/portability/save-core-cleanup-abi-pair132-windows32-20261101.json'
    port = json.loads((ROOT / portpath).read_text())
    assert port['actualWindowsTypedReturns'] == port['typedPass'] == 512 and port['retainedCallerPointerRejects'] == 512 and (port['wrongCallerPointerRejects'] == port['wrongZeroHandlePositives'] == 256)
    for item in port['inputSources']:
        assert sha((ROOT / item['path']).read_bytes()) == item['sha256']
    cache = {}
    matches = []
    entries = {}
    for raw in oracle['matches']:
        row = dict(raw)
        row.update(row['realLinkSnapshot'])
        address = int(row['address'], 0)
        p = next((p for p in profiles if int(p['address'], 0) == address))
        length = p['bytes']
        old = next((r for r in oracle['historicalMatches'] if int(r['address'], 0) == address))
        assert old['exactByteEqual'] and old['source'] == p['oldSource'] and (old['sourceSha256'] == p['oldSourceSha256'])
        assert row['sourceSha256'] == p['sourceSha256'] and row['compiledBytes'] == row['bytes'] == length and row['exactByteEqual'] and dependencies_current(row)
        for path, digest in [('source', 'sourceSha256'), ('object', 'objectSha256'), ('isolatedCallerBinary', 'isolatedCallerBinarySha256'), ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT / row[path]).read_bytes()) == row[digest]
        own = native_entry('main', address, cache)
        metadata, binary, config = cache['main']
        offset = address - int(metadata['base'], 0)
        native = binary[offset:offset + length]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        assert native == linked and validation['exactCallerBytes'] and (validation['sourceSha256'] == row['sourceSha256'])
        assert validation['sourceObjectSha256'] == row['objectSha256'] and validation['nativeSpanSha256'] == sha(native) and (validation['linkedCallerSha256'] == sha(linked)) and (validation['linkerSha256'] == 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74') and (validation['linkerAttempt']['exitCode'] == 0)
        assert set.union(*(set(v['ownInstructionOffsets']) for v in vectors if v['entry'] == address)) == {i.address - address for i in Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(linked[:length], address)}
        row.update(outputSha256=sha(linked), linked=False, exactBytes=length, exactAfterDeclaredRelocation=True, exactAfterRealMwLink=True, oracle=dict(supported=True, cases=sum((v['entry'] == address for v in vectors)), actualReturns=2 * sum((v['entry'] == address for v in vectors)), report=ORACLE, reportSha256=sha((ROOT / ORACLE).read_bytes()), limits=oracle['limitations']))
        row.update(netNewFunctions=0, netNewBytes=0, primaryReplacementCandidate=True, oldSource=p['oldSource'], oldSourceSha256=p['oldSourceSha256'])
        row['returnContract'] = dict(sourceReturnType='u32', physicalR0Compared=True, apiReturnProven=False, callerConsumptionComplete=False)
        entries[row['name']] = own
        for rel in row['relocations']:
            entries[rel['symbol']] = (data_entry if rel['kind'] == 'data' else native_entry)('main', int(rel['target'], 0), cache)
        matches.append(row)
    assert len(matches) == 2 and sum((r['bytes'] for r in matches)) == 140
    deps = runtime_files() | set(producers) | {ORACLE, CONTROLS, PROFILE, portpath, 'ports/windows-native/cleanup_abi_pair132_runner.c', *(r['oldSource'] for r in profiles), oracle['vectorSidecar']['path'], controls['vectorSidecar']['path'], 'provenance/seed-manifest.json', 'match_mechanics_save_20261101_lane_cleanup_abi_pair.py'}
    rows = matches + [v['match'] for v in controls['controls']]
    deps.update((r['source'] for r in rows))
    for row in rows:
        deps.update((p['path'] for p in row.get('sourceDependencies', [])))
    for address in [P.M.FIRST, P.M.SECOND, 34099360, 34111044, 34099888, 34099824, 34106132, 33845476]:
        entries[f'qualified_native_{address:08x}'] = native_entry('main', address, cache)
    deps.update((v[0]['symbolsFile'] for v in cache.values()))
    verify_inputs()
    out = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA, matches=matches, matchedFunctions=2, matchedBytes=140, netNewFunctions=0, netNewBytes=0, primaryReplacementCandidate=True, reusedAcceptedBytes=0, reusedNewCredit=0, nativeSymbolEntries=entries, nativeSymbols={n: v['address'] for n, v in entries.items()}, nativeSymbolModules={}, sourceDependencies=[], replayDependencies=[file_identity(Path(p).as_posix()) for p in sorted(deps)], replayRequires=[], oracle=dict(cases=len(vectors), actualReturns=2 * len(vectors), nativeCaseDigest=CASE, report=ORACLE, counts=oracle['counts']), negativeControls=dict(report=CONTROLS, sha256=sha((ROOT / CONTROLS).read_bytes()), counts=controls['counts'], nativeCaseDigest=CONTROL_CASE), portableValidation=dict(report=portpath, sha256=sha((ROOT / portpath).read_bytes()), perProcessTypedReturns=port['actualWindowsTypedReturns'], perProcessHistoricalReturns=port['actualWindowsRetainedReturns'], historicalRejects=port['retainedCallerPointerRejects'], perProcessWrongReturns=port['actualWindowsWrongReturns'], wrongRejects=port['wrongCallerPointerRejects'], wrongPositives=port['wrongZeroHandlePositives'], scope=port['limitations']), wholeLinkedRebuild=False, registrationPerformedByThisScript=False, inputsUnchanged=True, limitations=oracle['limitations'])
    target = ROOT / 'evidence/matches/mechanics-save-20261101-lane-cleanup-abi-pair.json'
    target.write_text(json.dumps(out, indent=2) + '\n')
    print(dict(functions=2, bytes=140, netNewBytes=0, actualMatchedReturns=640, wrongMatchedReturns=16, windowsTypedReturns=512, reportSha256=sha(target.read_bytes())))
if __name__ == '__main__':
    main()
