import gzip
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'evidence/application'), str(ROOT / 'deps/native')]
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, native_entry, ROM_SHA, SAVE_SHA, MAIN_SHA
from match_mechanics_save_20261029_item_use import data_entry
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
from source_dependencies import dependencies_current
from save_core_cleanup_words_fixtures_20261031 import code_bytes
import save_core_roster_initializer251_fixtures_20261101 as F

PRODUCER = 'evidence/application/save_core_roster_initializer251_fixtures_20261101.py'
ORACLE = 'evidence/application/save-core-roster-initializer251-20261101.json'
CONTROL_PRODUCER = 'evidence/application/save_core_roster_initializer252_controls_20261101.py'
CONTROLS = 'evidence/application/save-core-roster-initializer252-controls-20261101.json'
CASE_SHA = '6cb7cd92e994bbe022e8bf2a655cfbc309fc883244a9f5a8ba1cad2a5f0de866'
CONTROL_SHA = 'd886203387911ea238e0b9069f070394ad8ebd8382a32dd150652a39a5c6cd1a'
SOURCES = {0x020C5B00: '007a3f371e28b9fae3ea5deabf3a16c0894c0972835f4a46e09c1cdfec9592b1',
           0x0206C140: '2b62c8a8a847dc7ea3e8eab1cc5750c75c0c605ba628b5a91ec019f17b6efc0d'}


def run(path):
    process = subprocess.run([sys.executable, str(ROOT / path)], capture_output=True, text=True,
                             timeout=1800, creationflags=subprocess.CREATE_NO_WINDOW)
    assert process.returncode == 0, process.stdout + process.stderr


def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    run(PRODUCER)
    run(CONTROL_PRODUCER)
    oracle, controls = json.loads((ROOT / ORACLE).read_text()), json.loads((ROOT / CONTROLS).read_text())
    assert oracle['caseSha256'] == CASE_SHA and oracle['mainSha256'] == MAIN_SHA
    assert (oracle['independentPairs'], oracle['actualTopReturns'], oracle['actualNestedReturns'], oracle['providerInvocations']) == (2288, 4576, 152092, 53156)
    assert oracle['actualTopReturnsByEntry'] == {'0x20c5b00': 4380, '0x20bf518': 132, '0x206c140': 64}
    sidecar = ROOT / oracle['sidecar']['path']
    assert sha(sidecar.read_bytes()) == oracle['sidecar']['sha256']
    digest, counts = hashlib.sha256(), {}
    coverage = {at: {'native': set(), 'source': set()} for at in SOURCES}
    interleavings = 0
    with gzip.open(sidecar, 'rb') as stream:
        for line in stream:
            digest.update(line)
            value = json.loads(line)
            entry = value['entry']
            counts[entry] = counts.get(entry, 0) + 1
            interleavings += value['profile'].get('modeOverride') is not None
            assert value['native']['actualReturn'] and value['source']['actualReturn']
            for at in coverage:
                for implementation in coverage[at]:
                    coverage[at][implementation].update(value[implementation]['coverage'][str(at)])
    assert digest.hexdigest() == CASE_SHA and sum(counts.values()) == 2288 and interleavings == 8
    assert controls['caseSha256'] == CONTROL_SHA and (controls['totalActualReturns'], controls['rejectedCases'], controls['positiveCases']) == (12, 3, 3)
    raw = gzip.decompress((ROOT / controls['sidecar']['path']).read_bytes())
    assert sha(raw) == CONTROL_SHA
    wrong = json.loads(raw)
    assert len(wrong) == 6 and all(v['native']['actualReturn'] and v['wrong']['actualReturn'] for v in wrong)
    assert sum(v['rejected'] for v in wrong) == 3
    assert len(controls['unsupported']) == 4 and all(not v['actualReturn'] and not v['postFaultStateClaimed'] for v in controls['unsupported'])
    selected_path = 'src/runtime/runtime07/native_main_0206c140.c'
    selected_sha = 'd1515ab8e85e357acb8b8e8c678c645498ae89bd44c31e66b0c560f679452a46'
    assert sha((ROOT / selected_path).read_bytes()) == selected_sha
    assert re.search(r'\bu32\s+native_main_0206c140\(void\)\s*\{', (ROOT / selected_path).read_text())
    assert 'extern u32 native_fn_0206c140(void);' in (ROOT / oracle['functionalDraft']['source']).read_text()
    from link_runtime_unit import measured_module
    original_arm = measured_module('main')[1]
    reused, reused_body = F.build(original_arm, F.M.CLEAR, selected_path, 'actually-selected-clear-v2')
    assert reused['sourceSha256'] == selected_sha and reused['exactByteEqual'] and reused['compiledBytes'] == 20
    cache, entries, matches = {}, {}, []
    for candidate in oracle['matches']:
        row = dict(candidate)
        row.update(row['realLinkSnapshot'])
        address = int(row['address'], 0)
        assert row['sourceSha256'] == SOURCES[address] and row['exactByteEqual'] and dependencies_current(row)
        assert row['compiledBytes'] == row['bytes'] == {F.M.ENTRY: 708, F.M.CLEAR: 20}[address]
        for key, digest_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                                ('isolatedCallerBinary', 'isolatedCallerBinarySha256'), ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT / row[key]).read_bytes()) == row[digest_key]
        own = native_entry('main', address, cache)
        metadata, body, _ = cache['main']
        native = body[address - int(metadata['base'], 0):address - int(metadata['base'], 0) + row['bytes']]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        assert linked == native and validation['exactCallerBytes']
        assert validation['sourceSha256'] == row['sourceSha256'] and validation['sourceObjectSha256'] == row['objectSha256']
        assert validation['nativeSpanSha256'] == sha(native) and validation['linkedCallerSha256'] == sha(linked)
        assert validation['linkerSha256'] == 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode'] == 0
        code = {F.M.ENTRY: 696, F.M.CLEAR: 16}[address]
        assert code_bytes(row) == code and all(seen == set(range(0, code, 4)) for seen in coverage[address].values())
        row.update(exactBytes=row['bytes'], exactAfterDeclaredRelocation=True, exactAfterRealMwLink=True, linked=False,
            outputSha256=sha(linked), oracle=dict(supported=True, cases=counts[address], actualReturns=2 * counts[address],
                report=ORACLE, reportSha256=sha((ROOT / ORACLE).read_bytes()), limits=oracle['limitations']))
        if address != F.M.CLEAR:
            matches.append(row)
        else:
            assert linked == reused_body
        entries[row['name']] = own
        for relocation in row['relocations']:
            loader = data_entry if relocation['symbol'].startswith('native_data_') else native_entry
            entries[relocation['symbol']] = loader(relocation.get('targetModule') or 'main', int(relocation['target'], 0), cache)
    for address in [*F.M.DETAILS, *F.M.PROVIDERS]:
        module = 'ov000' if address in (0x021F0764, 0x021F27D0) else 'main'
        name = 'native_fn_' + (module + '_' if module != 'main' else '') + f'{address:08x}'
        entries[name] = native_entry(module, address, cache)
    deps = runtime_files() | {PRODUCER, ORACLE, CONTROL_PRODUCER, CONTROLS,
        'match_mechanics_save_20261101_lane_roster_initializer_v2.py', selected_path,
        'evidence/application/save_core_roster_initializer250_machine_20261101.py',
        'evidence/application/save_core_measured_inputs140_machine_20261101.py',
        'evidence/application/save_core_historical_link_20261031.py',
        oracle['sidecar']['path'], controls['sidecar']['path'], 'provenance/seed-manifest.json'}
    for row in [*matches, oracle['functionalDraft'], *controls['candidates']]:
        deps.add(row['source'])
        deps.update(value['path'] for value in row.get('sourceDependencies', []))
    deps.update(F.ORIGINS.values())
    deps.update(item[0]['symbolsFile'] for item in cache.values())
    verify_inputs()
    output = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA,
        matches=matches, matchedFunctions=1, matchedBytes=708, nativeSymbolEntries=entries,
        nativeSymbols={name: value['address'] for name, value in entries.items()},
        nativeSymbolModules={name: value['module'] for name, value in entries.items() if value['module'] != 'main'},
        reusedDependencyBinding=dict(module='main',processor='arm9',mode='arm',address=hex(F.M.CLEAR),
            selectedSource=selected_path,selectedSourceSha256=selected_sha,selectedCPrototype='u32 native_main_0206c140(void)',
            callerPrototype='extern u32 native_fn_0206c140(void);',inputViewCompatible=True,
            newCoverageBytes=0,newFunctionCredit=0,preferredSourceChangeRequested=False,
            freshObjectSha256=reused['objectSha256'],freshLinkedBodySha256=sha(reused_body),
            exactlyEqualsNativeAndFrozenRegressionBody=True),
        sourceDependencies=[], replayDependencies=[file_identity(Path(p).as_posix()) for p in sorted(deps)], replayRequires=[],
        oracle=dict(cases=2288, actualReturns=4576, actualReturnsByEntry=oracle['actualTopReturnsByEntry'],
            nativeCaseDigest=CASE_SHA, actualHelperReturns=152092, suppliedCalls=53156, report=ORACLE,
            functionalDraftBytes=132, functionalDraftExactCredit=0, explicitSyntheticInterleavingPairs=8),
        negativeControls=dict(report=CONTROLS, nativeCaseDigest=CONTROL_SHA, actualReturns=12, rejects=3, positives=3, unsupportedStops=4),
        registrationPerformedByThisScript=False, wholeLinkedRebuild=False, inputsUnchanged=True, limitations=oracle['limitations'])
    path = ROOT / 'evidence/matches/mechanics-save-20261101-lane-roster-initializer-v2.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(dict(functions=1, bytes=708, actualTopReturns=4576, actualNestedReturns=152092, reportSha256=sha(path.read_bytes())))


if __name__ == '__main__':
    main()
