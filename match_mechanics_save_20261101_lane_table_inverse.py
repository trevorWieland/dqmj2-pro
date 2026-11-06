import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'evidence/application'), str(ROOT / 'deps/native')]
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, ROM_SHA, SAVE_SHA, MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry, unpack
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
from source_dependencies import dependencies_current
from save_core_cleanup_words_fixtures_20261031 import code_bytes
import save_core_table_inverse146_machine_20261101 as M

PROFILE = 'evidence/lanes/save-core/table-inverse146-profile-20261101.json'
ORACLE = 'evidence/application/save-core-table-inverse146-source-20261101.json'
CONTROLS = 'evidence/lanes/save-core/table-inverse146-controls-20261101.json'
CASE_SHA = 'e9ac2548d71c1ec36507c89523533d5b2ca4c11580078c724111c82b171deb68'
CONTROL_SHA = '3790e87fcf7a88909cf76ba78e94a24d833208586254dce87d3abf41662046a2'


def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    producers = ['evidence/application/save_core_table_inverse146_fixtures_20261101.py',
                 'evidence/application/save_core_table_inverse146_controls_20261101.py']
    for producer in producers:
        process = subprocess.run([sys.executable, str(ROOT / producer)], capture_output=True, text=True,
            timeout=900, creationflags=subprocess.CREATE_NO_WINDOW)
        assert process.returncode == 0, process.stdout + process.stderr
    oracle, controls = [json.loads((ROOT / p).read_text()) for p in [ORACLE, CONTROLS]]
    vectors, wrong = unpack(oracle['vectorSidecar'], CASE_SHA), unpack(controls['vectorSidecar'], CONTROL_SHA)
    assert len(vectors) == 351 and all(v['native']['actualReturn'] and v['compiledIdentical'] for v in vectors)
    assert oracle['counts'] == dict(contexts=351, actualEntryReturns=702, actualHelperReturns=163830, suppliedCalls=0)
    assert len(wrong) == 4 and sum(v['independentRejected'] for v in wrong) == 2
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in wrong)
    assert controls['counts'] == dict(contexts=4, actualEntryReturns=8, independentRejections=2, positiveControls=2)
    assert len(oracle['unsupported']) == 1 and oracle['unsupported'][0]['errorType'] == 'LogicalReadBoundary'
    assert not oracle['unsupported'][0]['actualReturn'] and not oracle['unsupported'][0]['postFaultCredit']
    cache, entries = {}, {}
    row = dict(oracle['matches'][0])
    row.update(row['realLinkSnapshot'])
    assert row['compiledBytes'] == row['bytes'] == 60 and row['exactByteEqual'] and dependencies_current(row)
    for key, digest in [('source', 'sourceSha256'), ('object', 'objectSha256'),
            ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
            ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        assert sha((ROOT / row[key]).read_bytes()) == row[digest]
    own = native_entry('main', M.ENTRY, cache)
    metadata, binary, _ = cache['main']
    start = M.ENTRY - int(metadata['base'], 0)
    native, linked = binary[start:start + 60], (ROOT / row['isolatedCallerBinary']).read_bytes()
    validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
    assert linked == native and code_bytes(row) == 60 and validation['exactCallerBytes']
    assert validation['sourceSha256'] == row['sourceSha256'] and validation['sourceObjectSha256'] == row['objectSha256']
    assert validation['nativeSpanSha256'] == sha(native) and validation['linkedCallerSha256'] == sha(linked)
    assert validation['linkerSha256'] == 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
    assert validation['linkerAttempt']['exitCode'] == 0
    assert set(oracle['ownInstructionOffsets']) == set(range(0, 60, 4))
    assert set(oracle['helperInstructionOffsets']) == set(range(0, 76, 4))
    row.update(exactBytes=60, exactAfterDeclaredRelocation=True, exactAfterRealMwLink=True,
        linked=False, outputSha256=sha(linked), oracle=dict(supported=True, cases=351,
            actualReturns=702, report=ORACLE, reportSha256=sha((ROOT / ORACLE).read_bytes()), limits=oracle['limitations']))
    entries[row['name']] = own
    for relocation in row['relocations']:
        entries[relocation['symbol']] = native_entry('main', int(relocation['target'], 0), cache)
    deps = runtime_files() | set(producers) | {PROFILE, ORACLE, CONTROLS,
        oracle['vectorSidecar']['path'], controls['vectorSidecar']['path'],
        'match_mechanics_save_20261101_lane_table_inverse.py', 'provenance/seed-manifest.json',
        'evidence/application/save_core_table_inverse146_build_20261101.py',
        'evidence/application/save_core_table_inverse146_machine_20261101.py'}
    for item in [*oracle['runtimeDependencies'], *controls['runtimeDependencies']]:
        assert sha((ROOT / item['path']).read_bytes()) == item['sha256']
        deps.add(item['path'])
    for candidate in [row, *controls['candidates']]:
        deps.add(candidate['source'])
        deps.update(d['path'] for d in candidate.get('sourceDependencies', []))
    deps.update(value[0]['symbolsFile'] for value in cache.values())
    verify_inputs()
    output = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA,
        matches=[row], matchedFunctions=1, matchedBytes=60, nativeSymbolEntries=entries,
        nativeSymbols={name:value['address'] for name,value in entries.items()}, nativeSymbolModules={},
        sourceDependencies=[], replayDependencies=[file_identity(Path(p).as_posix()) for p in sorted(deps)], replayRequires=[],
        oracle=dict(cases=351, actualReturns=702, nativeCaseDigest=CASE_SHA, counts=oracle['counts'], report=ORACLE),
        negativeControls=dict(report=CONTROLS, sha256=sha((ROOT / CONTROLS).read_bytes()),
            nativeCaseDigest=CONTROL_SHA, counts=controls['counts']),
        wholeLinkedRebuild=False, registrationPerformedByThisScript=False, inputsUnchanged=True,
        limitations=oracle['limitations'])
    path = ROOT / 'evidence/matches/mechanics-save-20261101-lane-table-inverse.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(dict(functions=1, bytes=60, actualEntryReturns=702, actualHelperReturns=163830,
        wrongCActualReturns=8, reportSha256=sha(path.read_bytes())))


if __name__ == '__main__':
    main()
