import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'evidence/application'), str(ROOT / 'deps/native')]
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, ROM_SHA, SAVE_SHA, MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import unpack
from match_mechanics_save_20261029_item_use import data_entry
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
from source_dependencies import dependencies_current
from link_runtime_unit import measured_module
from save_core_cleanup_words_fixtures_20261031 import code_bytes
import save_core_save_widget_exit142_machine_20261101 as M

PROFILE = 'evidence/lanes/save-core/save-widget-exit142-profile-20261101.json'
ORACLE = 'evidence/application/save-core-save-widget-exit142-source-20261101.json'
CONTROLS = 'evidence/lanes/save-core/save-widget-exit142-controls-20261101.json'
PROFILE_SHA = 'e756f267ed741766288b29c7efc53adbcd9ad9148127468415c35a62bc3d8ede'
CASE_SHA = '85d2cff0cdfbe78e6c733955dfc64b5260be75c4ed06b9e18bfa43fe49e0e7fa'
CYCLE_SHA = '21d76d62747ec497625d92a2e2946d67548e03a4667872e02f4f97675327764a'
CONTROL_SHA = 'ec754a09216a9ea2631007c582fa6519807f7cc609c2326efe0e72611e79a122'


def entry(module, address, cache):
    if module not in cache:
        cache[module] = measured_module(module)
    metadata, binary, config = cache[module]
    match = re.search(r'^(\S+) kind:function\((arm|thumb),size=0x([0-9a-f]+)\) addr:0x' + f'{address:08x}' + '$', config, re.M)
    assert match
    alias, mode, length = match[1], match[2], int(match[3], 16)
    start = address - int(metadata['base'], 0)
    native = binary[start:start + length]
    assert len(native) == length and sha(binary) == metadata['sha256']
    return dict(module=module, processor='arm9', address=hex(address), mode=mode, bytes=length,
                kind='function', nativeAlias=alias, nativeSpanSha256=sha(native),
                nativeModuleSha256=metadata['sha256'], verification='Measured qualified module/config/span identity')


def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    assert sha((ROOT / PROFILE).read_bytes()) == PROFILE_SHA
    producers = ['evidence/application/save_core_save_widget_exit142_fixtures_20261101.py',
                 'evidence/application/save_core_save_widget_exit142_controls_20261101.py']
    for producer in producers:
        process = subprocess.run([sys.executable, str(ROOT / producer)], capture_output=True, text=True,
                                 timeout=240, creationflags=subprocess.CREATE_NO_WINDOW)
        assert process.returncode == 0, process.stdout + process.stderr
    oracle = json.loads((ROOT / ORACLE).read_text())
    controls = json.loads((ROOT / CONTROLS).read_text())
    vectors = unpack(oracle['vectorSidecar'], CASE_SHA)
    cycles = unpack(oracle['cycleSidecar'], CYCLE_SHA)
    wrong = unpack(controls['vectorSidecar'], CONTROL_SHA)
    assert len(vectors) == 1536 and all(v['native']['actualReturn'] and v['compiledIdentical'] for v in vectors)
    assert oracle['counts'] == dict(contexts=1536, actualEntryReturns=3072, actualHelperReturns=256,
        suppliedCalls=14720, nonreturningCycleContexts=3, cycleActualReturns=0)
    assert len(cycles) == 3 and all(not v['actualReturn'] and not v['postStopCredit']
        and v['witness']['period'] == 256 and v['witness']['memoryInvariant'] for v in cycles)
    assert len(wrong) == 4 and sum(v['independentRejected'] for v in wrong) == 2
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in wrong)
    assert controls['counts'] == dict(contexts=4, actualEntryReturns=8, independentRejections=2, positiveControls=2)
    cache, entries = {}, {}
    row = dict(oracle['matches'][0])
    row.update(row['realLinkSnapshot'])
    assert int(row['address'], 0) == M.ENTRY and row['compiledBytes'] == row['bytes'] == 36
    assert row['exactByteEqual'] and dependencies_current(row)
    for key, digest in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                        ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                        ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        assert sha((ROOT / row[key]).read_bytes()) == row[digest]
    own = entry('main', M.ENTRY, cache)
    metadata, binary, _ = cache['main']
    start = M.ENTRY - int(metadata['base'], 0)
    native = binary[start:start + 36]
    linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
    validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
    assert native == linked and validation['exactCallerBytes'] and code_bytes(row) == 32
    assert validation['sourceSha256'] == row['sourceSha256'] and validation['sourceObjectSha256'] == row['objectSha256']
    assert validation['nativeSpanSha256'] == sha(native) and validation['linkedCallerSha256'] == sha(linked)
    assert validation['linkerSha256'] == 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
    assert validation['linkerAttempt']['exitCode'] == 0
    assert set(oracle['ownInstructionOffsets']) == set(range(0, 32, 4))
    assert set(oracle['helperInstructionOffsets']) == set(range(0, 88, 4))
    row.update(exactBytes=36, exactAfterDeclaredRelocation=True, exactAfterRealMwLink=True, linked=False,
        outputSha256=sha(linked), oracle=dict(supported=True, cases=1536, actualReturns=3072,
            report=ORACLE, reportSha256=sha((ROOT / ORACLE).read_bytes()), limits=oracle['limitations']),
        returnContract=dict(sourceReturnType='u32', physicalR0Compared=True, apiReturnProven=False,
                            callerConsumptionComplete=False))
    entries[row['name']] = own
    for relocation in row['relocations']:
        module = relocation['targetModule']
        address = int(relocation['target'], 0)
        entries[relocation['symbol']] = data_entry('main', address, cache) if relocation['kind'] == 'data' else entry(module, address, cache)
    for module, address in [('ov000', M.HELPER), ('main', 0x02049AD0), ('ov000', 0x022162C0), ('ov000', 0x022172DC)]:
        entries[f'qualified_{module}_{address:08x}'] = entry(module, address, cache)
    deps = runtime_files() | set(producers) | {PROFILE, ORACLE, CONTROLS,
        oracle['vectorSidecar']['path'], oracle['cycleSidecar']['path'], controls['vectorSidecar']['path'],
        'match_mechanics_save_20261101_lane_save_widget_exit.py', 'provenance/seed-manifest.json'}
    for item in [*oracle['runtimeDependencies'], *controls['runtimeDependencies']]:
        assert sha((ROOT / item['path']).read_bytes()) == item['sha256']
        deps.add(item['path'])
    for candidate in [row, *controls['candidates']]:
        deps.add(candidate['source'])
        deps.update(d['path'] for d in candidate.get('sourceDependencies', []))
    deps.update(value[0]['symbolsFile'] for value in cache.values())
    verify_inputs()
    output = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA,
        matches=[row], matchedFunctions=1, matchedBytes=36, nativeSymbolEntries=entries,
        nativeSymbols={name: value['address'] for name, value in entries.items()},
        nativeSymbolModules={name: value['module'] for name, value in entries.items() if value['module'] != 'main'},
        sourceDependencies=[], replayDependencies=[file_identity(Path(p).as_posix()) for p in sorted(deps)], replayRequires=[],
        oracle=dict(cases=1536, actualReturns=3072, actualHelperReturns=256, suppliedCalls=14720,
                    nativeCaseDigest=CASE_SHA, counts=oracle['counts'], report=ORACLE),
        negativeControls=dict(report=CONTROLS, sha256=sha((ROOT / CONTROLS).read_bytes()),
                              nativeCaseDigest=CONTROL_SHA, counts=controls['counts']),
        nonreturningEvidence=dict(contexts=3, actualReturns=0, sidecar=oracle['cycleSidecar'], nativeCaseDigest=CYCLE_SHA),
        wholeLinkedRebuild=False, registrationPerformedByThisScript=False, inputsUnchanged=True, limitations=oracle['limitations'])
    path = ROOT / 'evidence/matches/mechanics-save-20261101-lane-save-widget-exit.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(dict(functions=1, bytes=36, actualEntryReturns=3072, wrongCActualReturns=8,
               nonreturningCycleReturns=0, reportSha256=sha(path.read_bytes())))


if __name__ == '__main__':
    main()
