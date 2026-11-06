import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'evidence/application'), str(ROOT / 'deps/native')]
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, ROM_SHA, SAVE_SHA, MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry, unpack
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_prefix_setup_fixtures_20261101 as P
import save_core_prefix_setup_controls_20261101 as C
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
ORACLE = 'evidence/application/save-core-prefix-setup131-source-20261101.json'
CONTROLS = 'evidence/application/save-core-prefix-setup131-controls-20261101.json'
PROFILE = 'evidence/lanes/save-core/prefix-setup131-profile-20261101.json'
CASE = '8996410731c9bb571444a2c4065b7f86012bfabcff0212b0f2b7a1f6b1155f66'
CONTROL_CASE = 'd61499dc00e2cbfe1bc5d0c3235e48f870bb15fab2ea4fbe4409177f43def470'
PROFILE_SHA = '43728390d135cfc567e18d135b540b734d863ff4c82b6ba137251f283866da80'

def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    assert sha((ROOT / PROFILE).read_bytes()) == PROFILE_SHA
    producers = ['evidence/application/save_core_prefix_setup_fixtures_20261101.py', 'evidence/application/save_core_prefix_setup_controls_20261101.py']
    for producer in producers:
        process = subprocess.run([sys.executable, str(ROOT / producer)], capture_output=True, text=True, timeout=300)
        assert process.returncode == 0, process.stdout + process.stderr
    oracle = json.loads((ROOT / ORACLE).read_text())
    controls = json.loads((ROOT / CONTROLS).read_text())
    vectors = unpack(oracle['vectorSidecar'], CASE)
    negatives = unpack(controls['vectorSidecar'], CONTROL_CASE)
    parents=vectors['parent'];direct=vectors['direct'];allvectors=parents+direct
    assert len(parents)==838 and len(direct)==97 and all(v['actualReturn'] for v in allvectors)
    assert oracle['counts']['parentActualReturns']==1676 and oracle['counts']['directHelperActualReturns']==194 and oracle['counts']['nestedCleanupActualReturns']==256 and oracle['counts']['allCleanupActualReturns']==450 and oracle['counts']['otherNativeCompareReturns']==1080 and oracle['counts']['providedServiceCalls']==2692
    assert len(negatives)==37 and sum(v['independentRejection'] for v in negatives)==14 and all(v['actualOriginalReturn'] and v['actualWrongReturn'] for v in negatives)
    assert len(oracle['unsupportedBoundaries'])==3 and all(not v['actualReturn'] and not v['postfaultStateCredited'] for v in oracle['unsupportedBoundaries'])
    profiles = json.loads((ROOT / PROFILE).read_text())['rows']
    cache = {}
    matches = []
    entries = {}
    for raw in oracle['matches']:
        row = dict(raw)
        row.update(row['realLinkSnapshot'])
        address = int(row['address'], 0)
        p = next((p for p in profiles if int(p['address'], 0) == address))
        length = p['bytes']
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
        code=148 if address==P.M.ENTRY else 14
        assert set.union(*(set(v['functionInstructionOffsets'][str(address)]) for v in allvectors))=={i.address-address for i in Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(linked[:code],address)}
        cases,returns=(838,1676) if address==P.M.ENTRY else (225,450)
        row.update(outputSha256=sha(linked), linked=False, exactBytes=length, exactAfterDeclaredRelocation=True, exactAfterRealMwLink=True, oracle=dict(supported=True, cases=cases, actualReturns=returns, report=ORACLE, reportSha256=sha((ROOT / ORACLE).read_bytes()), limits=oracle['limitations']))
        row['returnContract'] = dict(sourceReturnType='u32', physicalR0Compared=True, apiReturnProven=False, callerConsumptionComplete=False)
        entries[row['name']] = own
        for rel in row['relocations']:
            entries[rel['symbol']] = (data_entry if rel['kind'] == 'data' else native_entry)('main', int(rel['target'], 0), cache)
        matches.append(row)
    assert len(matches) == 2 and sum((r['bytes'] for r in matches)) == 168
    deps = runtime_files() | set(producers) | {ORACLE, CONTROLS, PROFILE, oracle['vectorSidecar']['path'], controls['vectorSidecar']['path'], 'provenance/seed-manifest.json', 'match_mechanics_save_20261101_lane_prefix_setup.py'}
    rows = matches + [v['match'] for v in controls['controls']]
    deps.update((r['source'] for r in rows))
    for row in rows:
        deps.update((p['path'] for p in row.get('sourceDependencies', [])))
    for address in [P.M.ENTRY,*P.M.HELPERS,0x020B4634,0x020B3A58,0x020B557C]:
        entries[f'qualified_native_{address:08x}'] = native_entry('main', address, cache)
    deps.update((v[0]['symbolsFile'] for v in cache.values()))
    verify_inputs()
    out = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA, matches=matches, matchedFunctions=2, matchedBytes=168, reusedAcceptedBytes=0, reusedNewCredit=0, nativeSymbolEntries=entries, nativeSymbols={n: v['address'] for n, v in entries.items()}, nativeSymbolModules={}, sourceDependencies=[], replayDependencies=[file_identity(Path(p).as_posix()) for p in sorted(deps)], replayRequires=[], oracle=dict(parentCases=838,directHelperCases=97,actualTopReturns=1870,actualCleanupReturns=450, nativeCaseDigest=CASE, report=ORACLE, counts=oracle['counts']), negativeControls=dict(report=CONTROLS, sha256=sha((ROOT / CONTROLS).read_bytes()), counts=controls['counts'], nativeCaseDigest=CONTROL_CASE), wholeLinkedRebuild=False, registrationPerformedByThisScript=False, inputsUnchanged=True, limitations=oracle['limitations'])
    target = ROOT / 'evidence/matches/mechanics-save-20261101-lane-prefix-setup.json'
    target.write_text(json.dumps(out, indent=2) + '\n')
    print(dict(functions=2,bytes=168,parentActualReturns=1676,directHelperReturns=194,nestedCleanupReturns=256,wrongReturns=37, reportSha256=sha(target.read_bytes())))
if __name__ == '__main__':
    main()
