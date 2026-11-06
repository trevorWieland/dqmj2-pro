import argparse
import copy
from pathlib import Path
from unittest.mock import patch
import match_arm7_channel_parameters_20261030_67 as matcher
import validate_arm7_channel_parameters_20261030_67 as validator
from seal_recovery_evidence_20261031 import code_closure
from project import ROOT, read_json, write_json, sha256


REPORT = ROOT / 'evidence/matches/arm7-channel-parameters-20261030-67.json'
CONTROL = ROOT / 'evidence/verification/arm7-channel-parameters-controls-20261030-67.json'
WORK = ROOT / 'work/channel67-closure-v2-compatibility-20261101'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    options = parser.parse_args()
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
    scripts = code_closure([Path(__file__).name, 'seal_recovery_evidence_20261031.py', Path(validator.__file__).name])
    supplemental = [dict(path=name, sha256=sha256(ROOT / name)) for name in scripts if name not in required]
    assert {row['path'] for row in supplemental} == {Path(__file__).name,
        'seal_recovery_evidence_20261031.py', Path(validator.__file__).name}
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
    receipt = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), preparedOnly=options.prepare,
        originalReportSha256=matcher.digest(original_report), report=normalized_path.relative_to(ROOT).as_posix(),
        reportSha256=sha256(normalized_path), controls=control_path.relative_to(ROOT).as_posix(), controlsSha256=sha256(control_path),
        originalGeneratorClosureEntries=len(required), supplementalReplaySources=supplemental,
        unchangedOriginalValidator=True, allOriginalControlsPassed=True, negativeControls=len(outputs[0]['controls']),
        originalSourceAndObjectIdentitiesPreserved=all(row['unchanged'] for row in object_rebuilds), originalSourceAndTargetIdentitiesPreserved=True, rebuiltObjectMetadata=object_rebuilds, newSourceBytes=0,
        currentReportsPreservedDuringPreparation=options.prepare, namespaceRestored=True,
        limitations=['The frozen matcher prints the existing canonical report hash after its diverted write; that printed hash is not the diagnostic output identity',
            'Only report publication is diverted; the original full validator, fresh builds, native vectors and every negative control execute unchanged',
            'This repairs incompatible sealing metadata and does not establish a complete fresh checkout'])
    write_json(ROOT / 'evidence/verification/channel67-closure-v2-compatibility-20261101.json', receipt)
    print(dict(preparedOnly=options.prepare, originalClosureEntries=len(required), supplemental=len(supplemental),
               controls=receipt['negativeControls'], newSourceBytes=0), flush=True)


if __name__ == '__main__':
    main()
