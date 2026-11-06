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
import save_core_table_leaves147_fixtures_20261101 as F

ORACLE = 'evidence/application/save-core-table-leaves147-source-20261101.json'
CONTROLS = 'evidence/lanes/save-core/table-leaves147-controls-20261101.json'
CASE_SHA = 'a684755c6d930556b2349273b1b5ef81c46cc58c01c460711fbdfe81d6d9336f'
CONTROL_SHA = 'e983b831b39e21bb224d40d3264ed0de22171dfdceed1d9bfc951e004ac8bce0'


def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    producers = ['evidence/application/save_core_table_leaves147_fixtures_20261101.py',
                 'evidence/application/save_core_table_leaves147_controls_20261101.py']
    for producer in producers:
        process = subprocess.run([sys.executable, str(ROOT / producer)], capture_output=True, text=True,
            timeout=240, creationflags=subprocess.CREATE_NO_WINDOW)
        assert process.returncode == 0, process.stdout + process.stderr
    oracle, controls = [json.loads((ROOT / p).read_text()) for p in [ORACLE, CONTROLS]]
    vectors, wrong = unpack(oracle['vectorSidecar'], CASE_SHA), unpack(controls['vectorSidecar'], CONTROL_SHA)
    assert len(vectors) == 1325 and all(v['native']['actualReturn'] and v['compiledIdentical'] for v in vectors)
    assert oracle['counts'] == dict(contexts=1325, actualEntryReturns=2650, actualHelperReturns=0, suppliedCalls=0)
    assert len(wrong) == 8 and sum(v['independentRejected'] for v in wrong) == 4
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in wrong)
    assert controls['counts'] == dict(contexts=8, actualEntryReturns=16, independentRejections=4, positiveControls=4)
    cache, entries, matches = {}, {}, []
    for original in oracle['matches']:
        row = dict(original)
        row.update(row['realLinkSnapshot'])
        entry = int(row['address'], 0)
        assert row['compiledBytes'] == row['bytes'] == 40 and row['exactByteEqual'] and dependencies_current(row)
        for key, digest in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT / row[key]).read_bytes()) == row[digest]
        own = native_entry('main', entry, cache)
        metadata, binary, _ = cache['main']
        start = entry - int(metadata['base'], 0)
        native = binary[start:start + 40]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        code = 36 if entry == F.MASK else 40
        assert linked == native and code_bytes(row) == code and validation['exactCallerBytes']
        assert validation['sourceSha256'] == row['sourceSha256'] and validation['sourceObjectSha256'] == row['objectSha256']
        assert validation['nativeSpanSha256'] == sha(native) and validation['linkedCallerSha256'] == sha(linked)
        assert validation['linkerSha256'] == 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        assert validation['linkerAttempt']['exitCode'] == 0
        assert set(oracle['ownInstructionOffsets'][str(entry)]) == set(range(0, code, 4))
        cases = sum(v['native']['entry'] == entry for v in vectors)
        row.update(exactBytes=40, exactAfterDeclaredRelocation=True, exactAfterRealMwLink=True,
            linked=False, outputSha256=sha(linked), oracle=dict(supported=True, cases=cases,
                actualReturns=cases * 2, report=ORACLE, reportSha256=sha((ROOT / ORACLE).read_bytes()), limits=oracle['limitations']))
        entries[row['name']] = own
        for relocation in row['relocations']:
            entries[relocation['symbol']] = (data_entry if relocation['kind'] == 'data' else native_entry)(
                'main', int(relocation['target'], 0), cache)
        matches.append(row)
    deps = runtime_files() | set(producers) | {F.PROFILE, ORACLE, CONTROLS,
        oracle['vectorSidecar']['path'], controls['vectorSidecar']['path'],
        'match_mechanics_save_20261101_lane_table_leaves.py', 'provenance/seed-manifest.json'}
    for item in [*oracle['runtimeDependencies'], *controls['runtimeDependencies']]:
        assert sha((ROOT / item['path']).read_bytes()) == item['sha256']
        deps.add(item['path'])
    for row in [*matches, *controls['candidates']]:
        deps.add(row['source'])
        deps.update(d['path'] for d in row.get('sourceDependencies', []))
    deps.update(value[0]['symbolsFile'] for value in cache.values())
    verify_inputs()
    output = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA,
        matches=matches, matchedFunctions=2, matchedBytes=80, nativeSymbolEntries=entries,
        nativeSymbols={name:value['address'] for name,value in entries.items()}, nativeSymbolModules={},
        sourceDependencies=[], replayDependencies=[file_identity(Path(p).as_posix()) for p in sorted(deps)], replayRequires=[],
        oracle=dict(cases=1325, actualReturns=2650, nativeCaseDigest=CASE_SHA, counts=oracle['counts'], report=ORACLE),
        negativeControls=dict(report=CONTROLS, sha256=sha((ROOT / CONTROLS).read_bytes()),
            nativeCaseDigest=CONTROL_SHA, counts=controls['counts']),
        wholeLinkedRebuild=False, registrationPerformedByThisScript=False, inputsUnchanged=True,
        limitations=oracle['limitations'])
    path = ROOT / 'evidence/matches/mechanics-save-20261101-lane-table-leaves.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(dict(functions=2, bytes=80, actualEntryReturns=2650, wrongCActualReturns=16, reportSha256=sha(path.read_bytes())))


if __name__ == '__main__':
    main()
