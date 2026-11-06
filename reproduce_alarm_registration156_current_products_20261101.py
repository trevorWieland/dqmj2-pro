import argparse
import sys
from pathlib import Path
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256
import reproduce_legacy_arm7_closures_20261101 as compatibility


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-root', required=True)
    options = parser.parse_args()
    assert Path(options.expected_root).resolve() == ROOT.resolve()
    scripts = ['match_arm7_lane_alarm_registration_20261031.py', 'validate_arm7_lane_alarm_registration_20261031.py']
    before = {name: sha256(ROOT / name) for name in scripts}
    arguments = [compatibility.__file__, '--family', 'alarm-registration156']
    with patch.dict(compatibility.FAMILIES, {'alarm-registration156': ('alarm_registration', '20261031')}), patch.object(sys, 'argv', arguments):
        compatibility.main()
    assert all(sha256(ROOT / name) == digest for name, digest in before.items())
    report = ROOT / 'evidence/verification/arm7-lane-alarm-registration156-controls-20261031.json'
    result = read_json(report)
    assert result['allPassed'] and all(row['rejected'] for row in result['controls'])
    write_json(ROOT / 'evidence/verification/alarm-registration156-current-products-20261101.json',
        dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), sourceCredit=0,
            fullOriginalValidatorPassed=True, originalScripts=before, controls=len(result['controls']),
            canonicalControlReport=report.relative_to(ROOT).as_posix(), canonicalControlReportSha256=sha256(report),
            freshOriginalMatcherAndAllControlsExecuted=True,
            limitations=['Rebuilds an unselected historical oracle prerequisite omitted from the selected source build order',
                'Original frozen source, validator and closure conditions remain unchanged',
                'This targeted replay does not establish a complete clean checkout']))
    print(dict(controls=len(result['controls']), allPassed=True, sourceCredit=0))


if __name__ == '__main__':
    main()
