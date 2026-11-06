import hashlib
import io
import json
from pathlib import Path
import tokenize

ROOT = Path(__file__).resolve().parent
FILES = [
    'src/arm7/lane_20261031_mmio_poll44/native_arm7_wram_037fb300.c',
    'arm7_lane_mmio_poll44_native_20261031.py',
    'arm7_lane_mmio_poll44_boundaries_20261031.py',
    'match_arm7_lane_mmio_poll44_20261031.py',
    'validate_arm7_lane_mmio_poll44_20261031.py',
    'seal_arm7_mmio_poll44_20261031.py',
    'nonmatching/arm7-bulk/20261031/lane-mmio-poll44-final/closure.json',
    'nonmatching/arm7-bulk/20261031/lane-mmio-poll44-final/generator-pins.json',
    'evidence/matches/arm7-lane-mmio-poll44-20261031.json',
    'evidence/verification/arm7-lane-mmio-poll44-controls-20261031.json',
    'evidence/verification/arm7-mmio-poll44-replay-receipt-20261031.json',
    'evidence/attempts/arm7-mmio-poll44-caller-suffix-pin-correction-20261031.json',
    'docs/2026-10-31-arm7-mmio-poll44.md',
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    report = json.loads((ROOT / FILES[8]).read_text())
    controls = json.loads((ROOT / FILES[9]).read_text())
    receipt = json.loads((ROOT / FILES[10]).read_text())
    if sha(ROOT / FILES[8]) != receipt['canonicalReportSha256'] or sha(ROOT / FILES[9]) != receipt['controlsReportSha256']:
        raise ValueError('Final independent-CWD receipts differ')
    if report['generatorSha256'] != sha(ROOT / FILES[3]) or controls['generatorSha256'] != sha(ROOT / FILES[4]):
        raise ValueError('Current matcher/validator differs from replayed source')
    if len(controls['controls']) != 41 or not controls['allPassed'] or len(report['matches']) != 1:
        raise ValueError('Complete poll controls/unit missing')
    row = report['matches'][0]
    if row['source'] != FILES[0] or row['sourceSha256'] != sha(ROOT / FILES[0]) or not row['realArm7Link']['exactLinkedBytes']:
        raise ValueError('Source-only genuine link proof differs')
    if (row['program'], row['processor'], row['module'], row['mode'], row['address'], row['bytes']) != ('', 'arm7', 'arm7-wram', 'arm', '0x37fb300', 44):
        raise ValueError('Qualified poll identity differs')
    if report['actualNativeAndCompiledReturns'] != 228 or report['actualSeparatelyObservedNestedReturns'] != 38 or report['actualSeparatelyObservedNativeCallerSuffixReturns'] != 38:
        raise ValueError('Own and distinct caller/nested returns changed')
    if report['physicalHardwareExecutionCredit'] != 0 or row['oracle']['providerFreeReturnCredit'] != 0:
        raise ValueError('Synthetic MMIO path overclaimed')
    inputs = {item['path']: item['sha256'] for item in report['generatorSources'] if item['path'] not in FILES}
    inputs.update({row['compiler']: row['compilerSha256'], row['binary']: row['inputModuleSha256'], 'inputs/game.nds': report['romSha256']})
    linker = Path(row['realArm7Link']['linkCommand'][0]).relative_to(ROOT).as_posix()
    inputs[linker] = row['realArm7Link']['linkerSha256']
    for name, expected in inputs.items():
        if sha(ROOT / name) != expected:
            raise ValueError('Existing tool/runtime/input changed: ' + name)
    for name in FILES:
        path = ROOT / name
        if name.startswith(('work/', 'tools/', 'inputs/')) or len(path.read_bytes()) == 0:
            raise ValueError('Invalid source-only transport item')
        if path.suffix == '.py':
            text = path.read_text()
            if len(text.splitlines()) > 500 or any(row.type == tokenize.COMMENT for row in tokenize.generate_tokens(io.StringIO(text).readline)):
                raise ValueError('Authored Python source policy differs')
    manifest = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': sha(Path(__file__)),
        'files': [{'path': name, 'sha256': sha(ROOT / name), 'bytes': (ROOT / name).stat().st_size} for name in FILES],
        'requiredExistingFiles': [{'path': name, 'sha256': value} for name, value in sorted(inputs.items())],
        'qualifiedFunction': {key: row[key] for key in ('program', 'processor', 'module', 'mode', 'address', 'bytes')},
        'reproduce': ['match_arm7_lane_mmio_poll44_20261031.py'], 'controlsReproduce': ['validate_arm7_lane_mmio_poll44_20261031.py'],
        'declaredGeneratedOutputRoot': 'work/arm7-bulk-20261030/lane-mmio-poll44-final', 'cachedOutputsTransported': False,
        'sourceFunctionsReady': 1, 'sourceInitializedBytesReady': 44, 'acceptedSourceCreditBeforeIntegrator': 0,
        'sharedRegistryOrConfigEdits': False, 'allPassed': True}
    output = ROOT / 'provenance/arm7-mmio-poll44-handoff-20261031.json'
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'manifest': output.relative_to(ROOT).as_posix(), 'sha256': sha(output), 'files': len(FILES), 'existingInputs': len(inputs), 'allPassed': True}), flush=True)


if __name__ == '__main__':
    main()
