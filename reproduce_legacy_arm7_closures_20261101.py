import argparse
import copy
import importlib
from pathlib import Path
from unittest.mock import patch
from seal_recovery_evidence_20261031 import code_closure
from project import ROOT, read_json, write_json, sha256


FAMILIES = {
    'driver-leaves': ('driver_leaves', '20261030'),
    'timing': ('timing', '20261031'),
    'setting': ('setting', '20261031'),
    'initializer': ('initializer', '20261031'),
    'alarm-selector': ('alarm_selector', '20261031'),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', choices=sorted(FAMILIES), required=True)
    parser.add_argument('--prepare', action='store_true')
    options = parser.parse_args()
    family = options.family
    stem, date = FAMILIES[family]
    matcher = importlib.import_module('match_arm7_lane_' + stem + '_' + date)
    validator = importlib.import_module('validate_arm7_lane_' + stem + '_' + date)
    REPORT = ROOT / f'evidence/matches/arm7-lane-{family}-{date}.json'
    CONTROL = ROOT / f'evidence/verification/arm7-lane-{family}-controls-{date}.json'
    WORK = ROOT / f'work/legacy-arm7-closure-compatibility-20261101/{family}' 
    assert sha256(ROOT / 'seal_recovery_evidence_20261031.py') == 'bc0eea9a76eb54bdbe5818027c2dfdf19742e9741759a90f14f1c1ca8e282b9c'
    assert sha256(matcher.__file__) == validator.GENERATOR_SHA
    original_report, original_control = REPORT.read_bytes(), CONTROL.read_bytes()
    previous = read_json(REPORT)
    WORK.mkdir(parents=True, exist_ok=True)
    raw_path, normalized_path, control_path = [WORK / name for name in ['raw-generator.json', 'normalized-report.json', 'normalized-controls.json']]
    captured = []

    def producer_output(path, document):
        if Path(path).resolve() != REPORT.resolve() or captured:
            raise ValueError('Unexpected matcher output namespace')
        captured.append(copy.deepcopy(document))
        write_json(raw_path, document)

    with patch.object(matcher, 'write_json', producer_output):
        matcher.main()
    assert len(captured) == 1
    document = captured[0]
    pins = read_json(matcher.PIN_FILE)['files']
    required = {Path(matcher.__file__).name, matcher.PROFILE.relative_to(ROOT).as_posix(),
                matcher.PIN_FILE.relative_to(ROOT).as_posix()} | {row['path'] for row in pins}
    sources = document['generatorSources']
    assert len(sources) == len(required) and {row['path'] for row in sources} == required
    for item in sources:
        assert sha256(ROOT / item['path']) == item['sha256']
    assert len(previous['matches']) == len(document['matches'])
    object_rebuilds = []
    for before, after in zip(previous['matches'], document['matches']):
        assert all(before[field] == after[field] for field in ['address', 'bytes', 'source', 'sourceSha256', 'targetSha256'])
        unchanged = before['objectSha256'] == after['objectSha256']
        if options.prepare:
            assert unchanged
        object_rebuilds.append(dict(address=after['address'], previousObjectSha256=before['objectSha256'],
            currentObjectSha256=after['objectSha256'], unchanged=unchanged))
    scripts = code_closure([Path(__file__).name, 'seal_recovery_evidence_20261031.py', Path(matcher.__file__).name, Path(validator.__file__).name])
    supplemental = [dict(path=name, sha256=sha256(ROOT / name)) for name in scripts if name not in required]
    assert {Path(__file__).name, 'seal_recovery_evidence_20261031.py', Path(validator.__file__).name} <= {row['path'] for row in supplemental}
    assert all(row['path'].endswith('.py') and (ROOT / row['path']).resolve().is_relative_to(ROOT) for row in supplemental)
    document['supplementalReplaySources'] = supplemental
    document['replayCodeSeal'] = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        producerCommand=[Path(matcher.__file__).name], originalGeneratorDocumentSha256=sha256(raw_path),
        scope='Original generator closure retained exactly; supplemental replay and validation code pinned separately', sourceOrNativeByteCredit=0)
    write_json(normalized_path, document)
    validator._FRESH.clear()
    outputs = []

    def validator_output(path, result):
        if Path(path).resolve() != CONTROL.resolve() or outputs:
            raise ValueError('Unexpected validator output namespace')
        assert result['allPassed'] and result['reportSha256'] == sha256(normalized_path)
        assert result['report'] == normalized_path.relative_to(ROOT).as_posix()
        result = copy.deepcopy(result)
        result['report'] = REPORT.relative_to(ROOT).as_posix()
        outputs.append(result)
        write_json(control_path, result)

    with patch.object(validator, 'REPORT', normalized_path), patch.object(validator, 'write_json', validator_output):
        validator.main()
    assert len(outputs) == 1 and all(row['rejected'] for row in outputs[0]['controls'])
    assert REPORT.read_bytes() == original_report and CONTROL.read_bytes() == original_control
    if not options.prepare:
        try:
            REPORT.write_bytes(normalized_path.read_bytes())
            CONTROL.write_bytes(control_path.read_bytes())
        except BaseException:
            REPORT.write_bytes(original_report)
            CONTROL.write_bytes(original_control)
            raise
    receipt = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), preparedOnly=options.prepare, family=family,
        originalReportSha256=matcher.digest(original_report), report=normalized_path.relative_to(ROOT).as_posix(),
        reportSha256=sha256(normalized_path), controls=control_path.relative_to(ROOT).as_posix(), controlsSha256=sha256(control_path),
        originalGeneratorClosureEntries=len(required), supplementalReplaySources=supplemental,
        unchangedOriginalValidator=True, allOriginalControlsPassed=True, negativeControls=len(outputs[0]['controls']),
        originalSourceAndObjectIdentitiesPreserved=all(row['unchanged'] for row in object_rebuilds), originalSourceAndTargetIdentitiesPreserved=True, rebuiltObjectMetadata=object_rebuilds, newSourceBytes=0,
        currentReportsPreservedDuringPreparation=options.prepare, namespaceRestored=True,
        limitations=['The frozen matcher prints the existing canonical report hash after its diverted write; that printed hash is not the diagnostic output identity',
            'Only report publication is diverted; the original full validator, fresh builds, native vectors and every negative control execute unchanged',
            'This repairs incompatible sealing metadata and does not establish a complete fresh checkout'])
    write_json(ROOT / f'evidence/verification/legacy-arm7-{family}-closure-compatibility-20261101.json', receipt)
    print(dict(preparedOnly=options.prepare, family=family, originalClosureEntries=len(required), supplemental=len(supplemental),
               controls=receipt['negativeControls'], newSourceBytes=0), flush=True)


if __name__ == '__main__':
    main()
