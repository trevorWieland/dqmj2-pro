import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'evidence/application'), str(ROOT / 'deps/native')]
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, ROM_SHA, SAVE_SHA, MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry, unpack
from match_mechanics_save_20261029_item_use import data_entry
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
from source_dependencies import dependencies_current
from save_core_cleanup_words_fixtures_20261031 import code_bytes
import save_core_slot_kind141_machine_20261101 as M

PROFILE = 'evidence/lanes/save-core/slot-kind141-profile-20261101.json'
ORACLE = 'evidence/application/save-core-slot-kind141-source-20261101.json'
CONTROLS = 'evidence/lanes/save-core/slot-kind141-controls-20261101.json'
PROFILE_SHA = '42cdc46d37a132ec8fd0f97d59bd880f878c25a455d37edb91aa767518c654b1'
CASE_SHA = '7a9f6797ea29517ecef562880645a67bd4a998261cc9bfb30f63916da1f2daec'
CONTROL_SHA = 'e220f9f1a223c0ee8d8e5742cadf25a33796154258432cb6dd07490d52dc0b34'


def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    assert sha((ROOT / PROFILE).read_bytes()) == PROFILE_SHA
    producers = ['evidence/application/save_core_slot_kind141_fixtures_20261101.py',
                 'evidence/application/save_core_slot_kind141_controls_20261101.py']
    for producer in producers:
        process = subprocess.run([sys.executable, str(ROOT / producer)], capture_output=True, text=True,
                                 timeout=240, creationflags=subprocess.CREATE_NO_WINDOW)
        assert process.returncode == 0, process.stdout + process.stderr
    oracle = json.loads((ROOT / ORACLE).read_text())
    controls = json.loads((ROOT / CONTROLS).read_text())
    vectors = unpack(oracle['vectorSidecar'], CASE_SHA)
    wrong = unpack(controls['vectorSidecar'], CONTROL_SHA)
    assert len(vectors) == 2464 and all(v['native']['actualReturn'] and v['compiledIdentical'] for v in vectors)
    assert oracle['counts'] == dict(contexts=2464, actualEntryReturns=4928, actualHelperReturns=0, suppliedCalls=2756)
    assert len(wrong) == 6 and sum(v['independentRejected'] for v in wrong) == 3
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in wrong)
    assert controls['counts'] == dict(contexts=6, actualEntryReturns=12, independentRejections=3, positiveControls=3)
    assert len(oracle['unsupported']) == 1 and not oracle['unsupported'][0]['actualReturn']
    assert oracle['unsupported'][0]['errorType'] == 'LogicalWriteBoundary' and not oracle['unsupported'][0]['postFaultCredit']
    cache, entries = {}, {}
    row = dict(oracle['matches'][0])
    row.update(row['realLinkSnapshot'])
    assert int(row['address'], 0) == M.ENTRY and row['compiledBytes'] == row['bytes'] == M.LENGTH
    assert row['exactByteEqual'] and dependencies_current(row)
    for key, digest in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                        ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                        ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        assert sha((ROOT / row[key]).read_bytes()) == row[digest]
    own = native_entry('main', M.ENTRY, cache)
    metadata, binary, _ = cache['main']
    start = M.ENTRY - int(metadata['base'], 0)
    native = binary[start:start + M.LENGTH]
    linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
    validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
    assert native == linked and validation['exactCallerBytes'] and code_bytes(row) == 216
    assert validation['sourceSha256'] == row['sourceSha256'] and validation['sourceObjectSha256'] == row['objectSha256']
    assert validation['nativeSpanSha256'] == sha(native) and validation['linkedCallerSha256'] == sha(linked)
    assert validation['linkerSha256'] == 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
    assert validation['linkerAttempt']['exitCode'] == 0
    assert set(oracle['ownInstructionOffsets']) == set(range(0, 216, 4))
    sites = {0x020451D4: 0xE1A06002, 0x020451DC: 0xE1A08000, 0x020451E0: 0xE1A07001,
             0x020451E4: 0xE1A05003, 0x02045284: 0x15957000, 0x020452A0: 0x15857000}
    for address, word in sites.items():
        offset = address - int(metadata['base'], 0)
        assert int.from_bytes(binary[offset:offset + 4], 'little') == word
    row.update(exactBytes=M.LENGTH, exactAfterDeclaredRelocation=True, exactAfterRealMwLink=True,
               linked=False, outputSha256=sha(linked),
               oracle=dict(supported=True, cases=len(vectors), actualReturns=4928, report=ORACLE,
                           reportSha256=sha((ROOT / ORACLE).read_bytes()), limits=oracle['limitations']),
               returnContract=dict(sourceReturnType='u32', physicalR0Compared=True,
                                   sourceFieldOffset=8, apiReturnProven=False, callerConsumptionComplete=False))
    entries[row['name']] = own
    for relocation in row['relocations']:
        entries[relocation['symbol']] = (data_entry if relocation['kind'] == 'data' else native_entry)(
            'main', int(relocation['target'], 0), cache)
    deps = runtime_files() | set(producers) | {PROFILE, ORACLE, CONTROLS,
        oracle['vectorSidecar']['path'], controls['vectorSidecar']['path'],
        'match_mechanics_save_20261101_lane_slot_kind.py', 'provenance/seed-manifest.json'}
    for item in [*oracle['runtimeDependencies'], *controls['runtimeDependencies']]:
        assert sha((ROOT / item['path']).read_bytes()) == item['sha256']
        deps.add(item['path'])
    for candidate in [row, *controls['candidates']]:
        deps.add(candidate['source'])
        deps.update(d['path'] for d in candidate.get('sourceDependencies', []))
    deps.update(value[0]['symbolsFile'] for value in cache.values())
    verify_inputs()
    output = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA,
        matches=[row], matchedFunctions=1, matchedBytes=M.LENGTH,
        nativeSymbolEntries=entries, nativeSymbols={name: value['address'] for name, value in entries.items()},
        nativeSymbolModules={}, sourceDependencies=[], replayDependencies=[file_identity(Path(p).as_posix()) for p in sorted(deps)],
        replayRequires=[], oracle=dict(cases=2464, actualReturns=4928, nativeCaseDigest=CASE_SHA,
                                       counts=oracle['counts'], report=ORACLE),
        negativeControls=dict(report=CONTROLS, sha256=sha((ROOT / CONTROLS).read_bytes()),
                              nativeCaseDigest=CONTROL_SHA, counts=controls['counts']),
        helperAbiEvidence=dict(address=hex(M.HELPER), bytes=360, sites={hex(a): hex(w) for a, w in sites.items()},
            actualHelperReturns=0, qualification='Original saves all four inputs; fourth-word pointer is conditionally read and written. Full helper is supplied in these executions; original formal declaration and file behavior remain unproved.'),
        wholeLinkedRebuild=False, registrationPerformedByThisScript=False, inputsUnchanged=True,
        limitations=oracle['limitations'])
    path = ROOT / 'evidence/matches/mechanics-save-20261101-lane-slot-kind.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(dict(functions=1, bytes=236, actualEntryReturns=4928, wrongCActualReturns=12,
               reportSha256=sha(path.read_bytes())))


if __name__ == '__main__':
    main()
