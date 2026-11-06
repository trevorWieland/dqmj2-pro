import gzip
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'evidence/application'), str(ROOT / 'deps/native')]
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, ROM_SHA, SAVE_SHA, MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
from source_dependencies import dependencies_current

ORACLE = 'evidence/application/save-core-skill-byteview266-20261101.json'
PORT = 'evidence/ports/save-core-skill-bytes-windows267-20261101.json'
SOURCE_SHA = '17e7ed3a6fc9dde613d14d5e3ba1fd092ce17106f0af88b25fdd4909dc8452d3'
PREVIOUS_SHA = '80266c7022b2d082aa4dc2f963819ba7353642848c2efd0b8582398df84c4b56'
CASE = '82ecfbac325b4a467cd72cf87bef712130b07b7955571517579ddfe8ccf9f505'
CONTROL = 'c17000ecfddd3f5ac0545728d50633bd5addec58a4b6fdc05c5963e2c891e8e8'
WINDOWS_CASE = '83e722b1b6a5b8e2470b6c67a9692e47014c3ad6f4d6dda1734c50de3083a555'


def main():
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    producers = ['evidence/application/save_core_skill_byteview266_fixtures_20261101.py',
                 'check_save_core_skill_bytes_windows267_20261101.py']
    for producer in producers:
        process = subprocess.run([sys.executable, str(ROOT / producer)], cwd=ROOT, capture_output=True, text=True, timeout=600)
        assert process.returncode == 0, process.stdout + process.stderr
    oracle = json.loads((ROOT / ORACLE).read_text())
    port = json.loads((ROOT / PORT).read_text())
    assert oracle['caseSha256'] == CASE and oracle['controls']['caseSha256'] == CONTROL
    assert oracle['cases'] == 16125 and oracle['totalActualReturns'] == 32250
    assert oracle['subobjectCrossingCases'] == 3325 and oracle['providers'] == oracle['dataWrites'] == 0
    assert oracle['codeCoverage'] == list(range(0, 24, 4))
    assert len(oracle['unsupported']) == 6 and all(not item['actualReturn'] for item in oracle['unsupported'])
    assert oracle['controls']['actualReturns'] == 6 and oracle['controls']['rejectedCases'] == 2
    assert oracle['controls']['positiveCases'] == 1 and oracle['signatureChanged'] is False
    for sidecar, expected in [(oracle['sidecar'], CASE), (oracle['controls']['sidecar'], CONTROL)]:
        raw = (ROOT / sidecar['path']).read_bytes()
        assert sha(raw) == sidecar['sha256'] and sha(gzip.decompress(raw)) == expected
    row = dict(oracle['candidate'])
    row.update(row['realLinkSnapshot'])
    previous = oracle['previousSource']
    assert row['sourceSha256'] == SOURCE_SHA and previous['sha256'] == PREVIOUS_SHA
    assert sha((ROOT / previous['path']).read_bytes()) == PREVIOUS_SHA
    assert row['bytes'] == row['compiledBytes'] == 24 and row['exactByteEqual'] and dependencies_current(row)
    assert row['relocations'] == []
    for path, digest in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                         ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                         ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        assert sha((ROOT / row[path]).read_bytes()) == row[digest]
    cache = {}
    own = native_entry('main', 0x0207AD98, cache)
    metadata, binary, config = cache['main']
    offset = 0x0207AD98 - int(metadata['base'], 0)
    native = binary[offset:offset + 24]
    linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
    validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
    assert native == linked and validation['exactCallerBytes'] and validation['sourceSha256'] == SOURCE_SHA
    assert validation['sourceObjectSha256'] == row['objectSha256']
    assert validation['nativeSpanSha256'] == validation['linkedCallerSha256'] == sha(native)
    assert validation['linkerSha256'] == 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
    assert validation['linkerAttempt']['exitCode'] == 0
    assert port['source']['sourceSha256'] == SOURCE_SHA and port['nativeCaseSha256'] == CASE
    assert port['actualPublicCalls'] == 16125 and port['totalActualPublicCalls'] == 16131
    assert port['windowsCaseSha256'] == WINDOWS_CASE and sum(v['rejected'] for v in port['controls']) == 2
    row.update(outputSha256=sha(linked), linked=False, exactBytes=24, exactAfterDeclaredRelocation=True,
        exactAfterRealMwLink=True, netNewFunctions=0, netNewBytes=0, primaryReplacementCandidate=True,
        oldSource=previous['path'], oldSourceSha256=PREVIOUS_SHA,
        oracle=dict(supported=True, cases=16125, actualReturns=32250, report=ORACLE,
            reportSha256=sha((ROOT / ORACLE).read_bytes()), limits=oracle['limitations']),
        returnContract=dict(sourceReturnType='int', physicalR0Compared=True, apiReturnProven=True,
            qualifiedReturnRange=[0, 255], signatureUnchanged=True))
    deps = runtime_files() | set(producers) | {ORACLE, PORT, row['source'], previous['path'],
        oracle['controls']['candidate']['source'], oracle['sidecar']['path'], oracle['controls']['sidecar']['path'],
        'nonmatching/save-core/20261101-skill-record-byteview264/whole_record_views.c',
        'evidence/application/save_core_skill_byteview265_machine_20261101.py',
        'evidence/application/save_core_historical_link_20261031.py',
        'provenance/seed-manifest.json', 'match_mechanics_save_20261101_lane_skill_record_bytes.py'}
    deps.update(v[0]['symbolsFile'] for v in cache.values())
    verify_inputs()
    entries = {row['name']: own}
    output = dict(schemaVersion=1, romSha256=ROM_SHA, saveSha256=SAVE_SHA, arm9Sha256=MAIN_SHA,
        matches=[row], matchedFunctions=1, matchedBytes=24, netNewFunctions=0, netNewBytes=0,
        primaryReplacementCandidate=True, sourceInterfaceChanged=False,
        nativeSymbolEntries=entries, nativeSymbols={key: value['address'] for key, value in entries.items()},
        nativeSymbolModules={}, sourceDependencies=[], replayDependencies=[file_identity(p) for p in sorted(deps)],
        replayRequires=[], oracle=dict(cases=16125, actualReturns=32250, nativeCaseDigest=CASE,
            report=ORACLE, providers=0, writes=0, unsupportedStops=6),
        negativeControls=dict(actualReturns=6, rejectedCases=2, positiveCases=1, nativeCaseDigest=CONTROL),
        portableValidation=dict(report=PORT, sha256=sha((ROOT / PORT).read_bytes()),
            actualWindowsReturns=16125, actualControlReturns=6, nativeCaseDigest=CASE, windowsCaseDigest=WINDOWS_CASE),
        wholeLinkedRebuild=False, registrationPerformedByThisScript=False, inputsUnchanged=True,
        limitations=oracle['limitations'])
    target = ROOT / 'evidence/matches/mechanics-save-20261101-lane-skill-record-bytes.json'
    target.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(dict(functions=1, bytes=24, netNewBytes=0, actualReturns=32250,
        windowsReturns=16131, reportSha256=sha(target.read_bytes()))))


if __name__ == '__main__':
    main()
