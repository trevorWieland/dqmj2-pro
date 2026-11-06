import argparse
import copy
import hashlib
import json
from pathlib import Path
import validate_main_sdk_lock_pair_20261101 as locks
import validate_main_sdk_thread_remove124_20261101 as threads
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure

FAMILIES = {'lock-pair': locks, 'thread-remove124': threads}


def convert(document, to_text):
    result = copy.deepcopy(document)
    changes = []
    for label, row in [('top', result), *[(item['address'], item) for item in result['matches']]]:
        for name, value in row.get('nativeSymbols', {}).items():
            if to_text:
                assert isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 0xFFFFFFFF
                row['nativeSymbols'][name] = hex(value)
                changes.append(dict(row=label, symbol=name, value=value, text=hex(value)))
            else:
                assert isinstance(value, str) and value == hex(int(value, 0))
                row['nativeSymbols'][name] = int(value, 0)
    return result, changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', choices=FAMILIES, required=True)
    parser.add_argument('--prepare', action='store_true')
    options = parser.parse_args()
    validator = FAMILIES[options.family]
    report_path, control_path = validator.REPORT, validator.CONTROLS
    before_report, before_controls = report_path.read_bytes(), control_path.read_bytes()
    if not options.prepare:
        validator._FRESH = None
        validator.main()
    raw_bytes = report_path.read_bytes()
    raw, controls = read_json(report_path), read_json(control_path)
    assert controls['allPassed'] and all(row['rejected'] for row in controls['controls'])
    assert controls['reportSha256'] == sha256(report_path)
    assert controls['report'] == report_path.relative_to(ROOT).as_posix()
    assert sha256(validator.matcher.__file__) == validator.MATCHER_SHA
    normalized, changes = convert(raw, True)
    restored, unused = convert(normalized, False)
    assert restored == raw and changes
    digest = hashlib.sha256(raw_bytes).hexdigest()
    archive = ROOT / 'evidence/attempts/sdk-symbol-transport-20261101' / (options.family + '-' + digest + '.json')
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        assert archive.read_bytes() == raw_bytes
    else:
        archive.write_bytes(raw_bytes)
    raw_control_digest = sha256(control_path)
    raw_control = archive.with_name(options.family + '-controls-' + raw_control_digest + '.json')
    if raw_control.exists():
        assert raw_control.read_bytes() == control_path.read_bytes()
    else:
        raw_control.write_bytes(control_path.read_bytes())
    published_controls = copy.deepcopy(controls)
    published_controls['report'] = archive.relative_to(ROOT).as_posix()
    published_controls['publicationTransport'] = dict(generator=Path(__file__).name,
        generatorSha256=sha256(__file__), originalControlReport=raw_control.relative_to(ROOT).as_posix(),
        originalControlReportSha256=raw_control_digest, originalValidatorUnmodified=True,
        scope='Original controls refer to their byte-identical archived raw report; integration view changes only address serialization')
    work = ROOT / 'work/sdk-symbol-transport-20261101' / options.family
    work.mkdir(parents=True, exist_ok=True)
    candidate, candidate_controls = work / 'report.json', work / 'controls.json'
    write_json(candidate, normalized)
    write_json(candidate_controls, published_controls)
    supplemental = [dict(path=name, sha256=sha256(ROOT / name)) for name in code_closure([Path(__file__).name])]
    receipt = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), family=options.family,
        preparedOnly=options.prepare, report=report_path.relative_to(ROOT).as_posix(),
        controls=control_path.relative_to(ROOT).as_posix(), previousReportSha256=hashlib.sha256(before_report).hexdigest(),
        previousControlsSha256=hashlib.sha256(before_controls).hexdigest(), normalizedReport=candidate.relative_to(ROOT).as_posix(),
        normalizedReportSha256=sha256(candidate), normalizedControls=candidate_controls.relative_to(ROOT).as_posix(),
        normalizedControlsSha256=sha256(candidate_controls), rawReport=archive.relative_to(ROOT).as_posix(), rawReportSha256=digest,
        rawControls=raw_control.relative_to(ROOT).as_posix(), rawControlsSha256=raw_control_digest,
        changedAddressValues=changes, roundTripExact=True, sourceAndObjectIdentitiesPreserved=True,
        allOriginalControlsPassed=True, originalControls=len(controls['controls']),
        supplementalReplaySources=supplemental, newFunctionCredit=0, newByteCredit=0)
    if options.prepare:
        assert report_path.read_bytes() == before_report and control_path.read_bytes() == before_controls
    else:
        try:
            report_path.write_bytes(candidate.read_bytes())
            control_path.write_bytes(candidate_controls.read_bytes())
        except BaseException:
            report_path.write_bytes(before_report)
            control_path.write_bytes(before_controls)
            raise
    write_json(ROOT / f'evidence/verification/sdk-{options.family}-symbol-transport-20261101.json', receipt)
    print(dict(family=options.family, preparedOnly=options.prepare, changedAddressValues=len(changes),
        originalControls=receipt['originalControls'], roundTripExact=True, newByteCredit=0))


if __name__ == '__main__':
    main()
