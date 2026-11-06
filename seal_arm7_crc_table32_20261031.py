import hashlib
import io
import json
from pathlib import Path
import tokenize

ROOT = Path(__file__).resolve().parent
FILES = ['src/utility/lane_20261031_crc_table32/native_crc_table32.c', 'derive_arm7_crc_table32_20261031.py',
    'arm7_crc_table32_scope_20261031.py', 'arm7_crc_table32_native_20261031.py',
    'match_arm7_crc_table32_20261031.py', 'validate_arm7_crc_table32_20261031.py', 'seal_arm7_crc_table32_20261031.py',
    'nonmatching/arm7-bulk/20261031/lane-child-crc-table32-final/generator-pins.json',
    'evidence/data/arm7-child-crc-table32-20261031.json', 'evidence/verification/arm7-crc-table32-controls-20261031.json',
    'evidence/verification/arm7-crc-table32-replay-receipt-20261031.json',
    'evidence/attempts/arm7-crc-table32-mwld-sidecar-format-20261031.json',
    'evidence/attempts/arm7-crc-table32-before-input-closure-20261031.json',
    'provenance/arm7-crc-table32-before-input-closure-20261031/match_arm7_crc_table32_20261031.py',
    'docs/2026-10-31-arm7-child-crc-mathematical-table32.md']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    report, controls = [json.loads((ROOT / name).read_text()) for name in FILES[8:10]]
    if sha(ROOT / FILES[8]) != '96640684f1f66a5e0f431df6219991fe239fffb3b424730fb704a99598236942' or sha(ROOT / FILES[9]) != '4bb746e7a7e44f942bc59840a3c8c8f3c9c98755c475d88d1781d4643e12d758':
        raise ValueError('Complete mathematical source-data/control replay differs')
    if report['generatorSha256'] != sha(ROOT / FILES[4]) or controls['generatorSha256'] != sha(ROOT / FILES[5]) or len(controls['controls']) != 32 or not controls['allPassed']:
        raise ValueError('Current complete producer/control source not replayed')
    if report['ordinaryFunctionCredit'] or report['ordinaryCCodeBytes'] or report['sourceDataBytesFromNativeInput'] or report['initializedDataBytes'] != 32:
        raise ValueError('Table data/code/generation scope differs')
    if report['nativeOriginalConsumers']['actualOriginalConsumerReturns'] != 576 or controls['mutantOriginalConsumerReturns'] != 128:
        raise ValueError('Actual original-consumer return counts differ')
    row = report['dataMatches'][0]
    if row['source'] != FILES[0] or row['sourceSha256'] != sha(ROOT / FILES[0]) or not row['exactAfterRealMwLink'] or row['sourceSymbolType'] != 'STT_OBJECT':
        raise ValueError('Whole non-executable source object or genuine linker proof differs')
    if (row['program'], row['processor'], row['module'], row['mode'], row['address'], row['bytes']) != ('dwc/utility.bin/move/child.srl', 'arm7', 'utility-child-arm7-main', 'data', '0x27f7f74', 32):
        raise ValueError('Qualified initialized-data identity differs')
    historical = json.loads((ROOT / FILES[12]).read_text())
    if historical['generatorSha256'] != sha(ROOT / FILES[13]):
        raise ValueError('Historical pre-closure generator archive differs')
    required = {item['path']: item['sha256'] for item in report['generatorSources'] if item['path'] not in FILES}
    required.update({row['compiler']: row['compilerSha256'], row['inputModule']: row['inputModuleSha256'],
        'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe': row['linkerSha256'], 'inputs/game.nds': report['romSha256']})
    for name, expected in required.items():
        if sha(ROOT / name) != expected:
            raise ValueError('Required existing tool/source/input differs: ' + name)
    files = []
    for name in FILES:
        path = ROOT / name
        if not path.is_file() or name.startswith(('work/', 'inputs/', 'tools/')):
            raise ValueError('Absent/generated transport path')
        if path.suffix == '.py':
            text = path.read_text()
            if len(text.splitlines()) > 500 or any(token.type == tokenize.COMMENT for token in tokenize.generate_tokens(io.StringIO(text).readline)):
                raise ValueError('Authored source policy differs')
        files.append({'path': name, 'sha256': sha(path), 'bytes': path.stat().st_size})
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': sha(Path(__file__)), 'files': files,
        'requiredExistingFiles': [{'path': name, 'sha256': value} for name, value in sorted(required.items())],
        'qualifiedData': {key: row[key] for key in ('program', 'processor', 'module', 'mode', 'address', 'bytes')},
        'sourceDataObjectsReady': 1, 'sourceInitializedDataBytesReady': 32, 'ordinarySourceFunctionsOrInstructionBytesReady': 0,
        'acceptedSourceCreditBeforeIntegrator': 0, 'originalTotalObjectExtentClaimed': False,
        'cachedGeneratedProductsTransported': False, 'sharedRegistryConfigLedgerPreferenceOrBoundaryEdits': False,
        'reproduce': ['match_arm7_crc_table32_20261031.py'], 'controlsReproduce': ['validate_arm7_crc_table32_20261031.py'], 'allPassed': True}
    output = ROOT / 'provenance/arm7-crc-table32-handoff-20261031.json'
    output.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'manifest': output.relative_to(ROOT).as_posix(), 'sha256': sha(output), 'files': len(files), 'existingInputs': len(required)}), flush=True)


if __name__ == '__main__':
    main()
