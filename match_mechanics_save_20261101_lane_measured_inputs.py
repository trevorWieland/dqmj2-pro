import gzip
import hashlib
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
import save_core_measured_inputs140_machine_20261101 as M

PROFILE = 'evidence/lanes/save-core/measured-inputs140-exact-profile-20261101.json'
ORACLE = 'evidence/application/save-core-measured-inputs140-source-20261101.json'
CONTROLS = 'evidence/lanes/save-core/measured-inputs140-controls-20261101.json'
PROFILE_SHA = '7e37e54ecfc3e23afb356d6de5cf1bc10f9331b527b18289c6bdbf186e12204d'
CASE_SHA = '92d23934f2e5c6760eba30c3a711f0cbf27e8a13222433e7fd65074f1e5687cc'
CONTROL_SHA = '5a0b81685304d6f9eea3c097e4bfee973dc2c85bc2fd198298e2a8f8055ebf48'


def check_large_sidecar(sidecar, expected):
    path = ROOT / sidecar['path']
    assert sha(path.read_bytes()) == sidecar['sha256'] and path.stat().st_size == sidecar['compressedBytes']
    digest, count = hashlib.sha256(), 0
    with gzip.open(path, 'rb') as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
            count += len(chunk)
    assert digest.hexdigest() == sidecar['uncompressedSha256'] == expected
    assert count == sidecar['uncompressedBytes'] and sidecar['contexts'] == 5292


def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    assert sha((ROOT / PROFILE).read_bytes()) == PROFILE_SHA
    producers = ['evidence/application/save_core_measured_inputs140_fixtures_20261101.py',
                 'evidence/application/save_core_measured_inputs140_controls_20261101.py']
    for producer in producers:
        process = subprocess.run([sys.executable, str(ROOT / producer)], capture_output=True, text=True,
                                 timeout=300, creationflags=subprocess.CREATE_NO_WINDOW)
        assert process.returncode == 0, process.stdout + process.stderr
    oracle = json.loads((ROOT / ORACLE).read_text())
    controls = json.loads((ROOT / CONTROLS).read_text())
    assert oracle['actualEntryReturns'] == 10584 and oracle['actualHelperReturns'] == 118928
    assert oracle['suppliedCalls'] == 16768 and len(oracle['matches']) == 3
    assert len(oracle['unsupported']) == 2
    assert all(not value['actualReturn'] and not value['postFaultCredit'] and value['errorType'] == 'UcError'
               and 'UC_ERR_READ_UNMAPPED' in value['reason'] for value in oracle['unsupported'])
    assert sum(value['contexts'] for value in oracle['counts'].values()) == 5292
    assert oracle['counts'][str(0x0205F920)]['suppliedCalls'] == oracle['counts'][str(0x02048E14)]['suppliedCalls'] == 0
    check_large_sidecar(oracle['vectorSidecar'], CASE_SHA)
    negatives = unpack(controls['vectorSidecar'], CONTROL_SHA)
    assert len(negatives) == 12 and sum(value['independentRejected'] for value in negatives) == 6
    assert all(value['native']['actualReturn'] and value['compiledWrongC']['actualReturn'] for value in negatives)
    assert controls['counts'] == dict(contexts=12, actualEntryReturns=24, independentRejections=6, positiveControls=6)
    cache, entries, matches = {}, {}, []
    for raw in oracle['matches']:
        row = dict(raw)
        row.update(row['realLinkSnapshot'])
        address, length = int(row['address'], 0), row['bytes']
        assert row['exactByteEqual'] and row['compiledBytes'] == length and dependencies_current(row)
        for key, digest in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                            ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                            ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT / row[key]).read_bytes()) == row[digest]
        own = native_entry('main', address, cache)
        metadata, binary, _ = cache['main']
        start = address - int(metadata['base'], 0)
        native = binary[start:start + length]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        assert own['bytes'] == length and native == linked and validation['exactCallerBytes']
        assert validation['sourceSha256'] == row['sourceSha256'] and validation['sourceObjectSha256'] == row['objectSha256']
        assert validation['nativeSpanSha256'] == sha(native) and validation['linkedCallerSha256'] == sha(linked)
        assert validation['linkerSha256'] == 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        assert validation['linkerAttempt']['exitCode'] == 0
        assert set(oracle['ownInstructionOffsets'][str(address)]) == set(range(0, code_bytes(row), 4))
        counts = oracle['counts'][str(address)]
        row.update(exactBytes=length, exactAfterDeclaredRelocation=True, exactAfterRealMwLink=True,
                   linked=False, outputSha256=sha(linked),
                   oracle=dict(supported=True, cases=counts['contexts'], actualReturns=counts['actualEntryReturns'],
                               report=ORACLE, reportSha256=sha((ROOT / ORACLE).read_bytes()), limits=oracle['limitations']),
                   returnContract=dict(sourceReturnType='void' if address == 0x0205F920 else 'u32',
                       physicalR0Compared=True, apiReturnProven=False, callerConsumptionComplete=False))
        entries[row['name']] = own
        for relocation in row['relocations']:
            entries[relocation['symbol']] = (data_entry if relocation['kind'] == 'data' else native_entry)(
                'main', int(relocation['target'], 0), cache)
        matches.append(row)
    assert sum(row['bytes'] for row in matches) == 520
    for address in [*M.HELPERS, *M.PROVIDERS]:
        entries[f'qualified_native_{address:08x}'] = native_entry('main', address, cache)
    deps = runtime_files() | set(producers) | {PROFILE, ORACLE, CONTROLS,
        oracle['vectorSidecar']['path'], controls['vectorSidecar']['path'],
        'match_mechanics_save_20261101_lane_measured_inputs.py', 'provenance/seed-manifest.json'}
    for item in [*oracle['runtimeDependencies'], *controls['runtimeDependencies']]:
        assert sha((ROOT / item['path']).read_bytes()) == item['sha256']
        deps.add(item['path'])
    for row in [*matches, *controls['candidates']]:
        deps.add(row['source'])
        deps.update(value['path'] for value in row.get('sourceDependencies', []))
    deps.update(value[0]['symbolsFile'] for value in cache.values())
    verify_inputs()
    output = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA,
        matches=matches, matchedFunctions=len(matches), matchedBytes=sum(row['bytes'] for row in matches),
        nativeSymbolEntries=entries, nativeSymbols={name: value['address'] for name, value in entries.items()},
        nativeSymbolModules={}, sourceDependencies=[], replayDependencies=[file_identity(Path(path).as_posix()) for path in sorted(deps)],
        replayRequires=[], oracle=dict(cases=5292, actualReturns=oracle['actualEntryReturns'],
            actualHelperReturns=oracle['actualHelperReturns'], providedCalls=oracle['suppliedCalls'],
            nativeCaseDigest=CASE_SHA, report=ORACLE, counts=oracle['counts']),
        negativeControls=dict(report=CONTROLS, sha256=sha((ROOT / CONTROLS).read_bytes()),
            nativeCaseDigest=CONTROL_SHA, counts=controls['counts']),
        wholeLinkedRebuild=False, registrationPerformedByThisScript=False, inputsUnchanged=True,
        limitations=oracle['limitations'])
    target = ROOT / 'evidence/matches/mechanics-save-20261101-lane-measured-inputs.json'
    target.write_text(json.dumps(output, indent=2) + '\n')
    print(dict(functions=len(matches), bytes=output['matchedBytes'], actualEntryReturns=oracle['actualEntryReturns'],
               wrongCActualReturns=controls['counts']['actualEntryReturns'], reportSha256=sha(target.read_bytes())))


if __name__ == '__main__':
    main()
