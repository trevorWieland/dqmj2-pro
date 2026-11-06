import subprocess
import sys
from project import ROOT, read_json, sha256


def main():
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-100.json')
    assert plan['linksPending'] and len(plan['replayMetadataMigrations']) == 1
    reference = plan['replayMetadataMigrations'][0]
    assert sha256(ROOT / reference['path']) == reference['sha256']
    migration = read_json(ROOT / reference['path'])
    receipt = read_json(ROOT / migration['preparationReceipt'])
    assert sha256(ROOT / migration['preparationReceipt']) == migration['preparationReceiptSha256']
    assert sha256(ROOT / receipt['generator']) == receipt['generatorSha256']
    report, control = ROOT / migration['report'], ROOT / migration['controlReport']
    assert sha256(report) == migration['previousReportSha256']
    assert sha256(control) == migration['previousControlsSha256']
    prepared_report, prepared_control = ROOT / migration['normalizedReport'], ROOT / migration['normalizedControls']
    assert sha256(prepared_report) == migration['normalizedReportSha256']
    assert sha256(prepared_control) == migration['normalizedControlsSha256']
    registry = ROOT / 'recovery.json'
    old_report, old_control, old_registry = report.read_bytes(), control.read_bytes(), registry.read_bytes()
    try:
        report.write_bytes(prepared_report.read_bytes())
        control.write_bytes(prepared_control.read_bytes())
        subprocess.run([sys.executable, str(ROOT / 'publish_source_cohort_20261101.py'), '--cohort', '100'], cwd=ROOT, check=True)
        assert sha256(registry) == plan['sourceRegistrySha256']
    except BaseException:
        report.write_bytes(old_report)
        control.write_bytes(old_control)
        registry.write_bytes(old_registry)
        raise
    print(dict(published=True, cohort=100, replayMetadataCompatibility=True, originalSourceAndObjectsPreserved=True))


if __name__ == '__main__':
    main()
