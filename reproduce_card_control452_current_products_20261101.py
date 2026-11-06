import argparse
import importlib
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
    expected = 'bc0eea9a76eb54bdbe5818027c2dfdf19742e9741759a90f14f1c1ca8e282b9c'
    assert sha256(ROOT / 'seal_recovery_evidence_20261031.py') == expected
    control = ROOT / 'evidence/verification/arm7-lane-card-control452-controls-20261031.json'
    positive = ROOT / 'evidence/matches/arm7-lane-card-control452-20261031.json'
    negative = ROOT / 'prove_arm7_card_control452_negative_returns_20261031.py'
    validator = ROOT / 'validate_arm7_lane_card_control_20261031.py'
    frozen = {path.name: sha256(path) for path in [negative, validator, ROOT / 'match_arm7_lane_card_control_20261031.py']}
    archive = ROOT / 'evidence/attempts/card-control452-current-products-20261101'
    archive.mkdir(parents=True, exist_ok=True)
    previous = []
    for path in [positive, control]:
        digest = sha256(path)
        saved = archive / (digest + '.json')
        if saved.exists():
            assert saved.read_bytes() == path.read_bytes()
        else:
            saved.write_bytes(path.read_bytes())
        previous.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=digest,
            archived=saved.relative_to(ROOT).as_posix()))
    arguments = [compatibility.__file__, '--family', 'card-control452']
    with patch.dict(compatibility.FAMILIES, {'card-control452': ('card_control', '20261031')}), patch.object(sys, 'argv', arguments):
        compatibility.main()
    current = read_json(control)
    assert current['allPassed'] and len(current['controls']) == 44
    for record in current['negativeRuntimeLinks']:
        directory = Path(record['cwd']).resolve()
        assert directory.is_relative_to(ROOT / 'work')
        assert sha256(directory / 'caller.bin') == record['linkedSha256']
    proof = importlib.import_module('prove_arm7_card_control452_negative_returns_20261031')
    proof.main()
    for name, digest in frozen.items():
        assert sha256(ROOT / name) == digest
    report = read_json(ROOT / 'evidence/verification/arm7-card-control452-negative-returns-20261031.json')
    assert report['allPassed'] and report['actualWrongCompiledSourceReturns'] == report['modelRejections'] == 4
    receipt = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), sourceCredit=0,
        expectedRoot=str(ROOT), originalFrozenImplementations=frozen, staleReports=previous,
        fullOriginalControls=44, actualWrongSourceReturns=4, independentRejections=4,
        negativeProductsFreshlyCompiledAndLinked=True, originalPathGuardsUnchanged=True,
        currentReportsRebasedByOriginalProducer=True,
        limitations=['Repairs a missing fresh-product prerequisite before the frozen negative-return proof',
            'Uses the existing separately sealed closure compatibility mechanism without editing its implementation',
            'Changes generated reports/products only; no source, validator, path guard or acceptance condition is weakened',
            'This targeted replay is not a complete clean build; remaining commands must still run'])
    write_json(ROOT / 'evidence/verification/card-control452-current-products-20261101.json', receipt)
    print(dict(fullControls=44, actualWrongReturns=4, independentRejections=4, sourceCredit=0))


if __name__ == '__main__':
    main()
