import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'evidence/application'), str(ROOT / 'deps/native')]
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, ROM_SHA, SAVE_SHA, MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry, unpack
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_descriptor_inputs_fixtures_20261101 as P
import save_core_descriptor_inputs_controls_20261101 as C
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
ORACLE = 'evidence/application/save-core-descriptor-inputs133-source-20261101.json'
CONTROLS = 'evidence/application/save-core-descriptor-inputs133-controls-20261101.json'
PROFILE = 'evidence/lanes/save-core/descriptor-inputs133-profile-20261101.json'
CASE = '54e55d48b949cb9c86c45168faba7496253a8ebd9eb535272a03a42db526b458'
CONTROL_CASE = 'e3096bc3230de7377c9485daa3fef6237434e940ed92a56b1868baf427538c0a'
PROFILE_SHA = '3a729e215c63a71285ab5ab4eca4d9cbafb9fde4fa1a80b0b8b32e5c26910829'

def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    assert sha((ROOT / PROFILE).read_bytes()) == PROFILE_SHA
    producers = ['evidence/application/save_core_descriptor_inputs_fixtures_20261101.py', 'evidence/application/save_core_descriptor_inputs_controls_20261101.py']
    for producer in producers:
        process = subprocess.run([sys.executable, str(ROOT / producer)], capture_output=True, text=True, timeout=300)
        assert process.returncode == 0, process.stdout + process.stderr
    oracle = json.loads((ROOT / ORACLE).read_text())
    controls = json.loads((ROOT / CONTROLS).read_text())
    vectors = unpack(oracle['vectorSidecar'], CASE)
    negatives = unpack(controls['vectorSidecar'], CONTROL_CASE)
    assert len(vectors) == 1872 and all(v['actualReturn'] for v in vectors)
    assert oracle['counts']['actualTopReturns']==3744 and oracle['counts']['physicalNativeHelperReturns']==5436 and oracle['counts']['providedServiceCalls']==1504
    assert len(negatives)==36 and sum(v['independentRejection'] for v in negatives)==13
    assert all(v['actualOriginalReturn'] and v['actualPositiveReturn'] and v['actualWrongReturn'] for v in negatives)
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
        assert set.union(*(set(v['functionInstructionOffsets'][str(address)]) for v in vectors if v['entry']==address)) == {i.address - address for i in Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(linked[:84], address)}
        row.update(outputSha256=sha(linked), linked=False, exactBytes=length, exactAfterDeclaredRelocation=True, exactAfterRealMwLink=True, oracle=dict(supported=True, cases=oracle['counts']['perEntryCases'][str(address)], actualReturns=2*oracle['counts']['perEntryCases'][str(address)], report=ORACLE, reportSha256=sha((ROOT / ORACLE).read_bytes()), limits=oracle['limitations']))
        row['returnContract'] = dict(sourceReturnType='u32', physicalR0Compared=True, apiReturnProven=False, callerConsumptionComplete=False)
        entries[row['name']] = own
        for rel in row['relocations']:
            entries[rel['symbol']] = (data_entry if rel['kind'] == 'data' else native_entry)('main', int(rel['target'], 0), cache)
        matches.append(row)
    assert len(matches) == 2 and sum((r['bytes'] for r in matches)) == 180
    deps = runtime_files() | set(producers) | {ORACLE, CONTROLS, PROFILE, oracle['vectorSidecar']['path'], controls['vectorSidecar']['path'], 'provenance/seed-manifest.json', 'match_mechanics_save_20261101_lane_descriptor_inputs.py'}
    rows = matches + [v['match'] for v in controls['controls']]
    deps.update((r['source'] for r in rows))
    for row in rows:
        deps.update((p['path'] for p in row.get('sourceDependencies', [])))
    for address in [P.M.GATE, P.M.SLOT, *P.M.HELPERS, *P.M.PROVIDERS]:
        entries[f'qualified_native_{address:08x}'] = native_entry('main', address, cache)
    deps.update((v[0]['symbolsFile'] for v in cache.values()))
    verify_inputs()
    out = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA, matches=matches, matchedFunctions=2, matchedBytes=180, reusedAcceptedBytes=0, reusedNewCredit=0, nativeSymbolEntries=entries, nativeSymbols={n: v['address'] for n, v in entries.items()}, nativeSymbolModules={}, sourceDependencies=[], replayDependencies=[file_identity(Path(p).as_posix()) for p in sorted(deps)], replayRequires=[], oracle=dict(cases=1872, actualReturns=3744, nativeCaseDigest=CASE, report=ORACLE, counts=oracle['counts']), negativeControls=dict(report=CONTROLS, sha256=sha((ROOT / CONTROLS).read_bytes()), counts=controls['counts'], nativeCaseDigest=CONTROL_CASE), wholeLinkedRebuild=False, registrationPerformedByThisScript=False, inputsUnchanged=True, limitations=oracle['limitations'])
    target = ROOT / 'evidence/matches/mechanics-save-20261101-lane-descriptor-inputs.json'
    target.write_text(json.dumps(out, indent=2) + '\n')
    print(dict(functions=2, bytes=180, actualReturns=3744, wrongReturns=36, reportSha256=sha(target.read_bytes())))
if __name__ == '__main__':
    main()
