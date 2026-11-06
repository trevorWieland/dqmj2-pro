import uuid
from project import ROOT, write_json
from validate_clean_checkout import archive_previous_checks, current_checks


def run():
    work = ROOT / 'work/clean-report-output-controls-20261030' / uuid.uuid4().hex
    results = []
    def fixture(name, report):
        target = work / name
        logs = target / 'logs/clean-checkout'
        logs.mkdir(parents=True)
        path = target / 'evidence/verification/checks.json'
        write_json(path, report)
        return target, logs, path
    green = {'allChecksPassed': True, 'buildAndOracleChecksPassed': True}
    target, logs, path = fixture('stale-green-process-interrupted', green)
    archived = archive_previous_checks(target, logs)
    assert archived and not path.exists()
    try:
        current_checks(target, -1)
    except (FileNotFoundError, ValueError):
        results.append('Archived historical green cannot certify an interrupted run')
    else:
        raise AssertionError('Stale report accepted')
    target, logs, path = fixture('fresh-green', green)
    assert current_checks(target, 0) == green
    results.append('Fresh complete green with status0 accepted')
    audit_only = {'allChecksPassed': False, 'buildAndOracleChecksPassed': True}
    target, logs, path = fixture('fresh-isolation-only-failure', audit_only)
    assert current_checks(target, 1) == audit_only
    results.append('Fresh build success retains separate strict isolation failure')
    for label, status, data in [('killed-with-green', -1, green), ('status-one-with-green', 1, green), ('status-zero-with-failure', 0, audit_only)]:
        target, logs, path = fixture(label, data)
        try:
            current_checks(target, status)
        except ValueError:
            results.append(label + ' rejected')
        else:
            raise AssertionError(label)
    write_json(ROOT / 'evidence/verification/clean-report-output-controls-20261030.json',
        {'sourceCredit': 0, 'controls': len(results), 'passed': True, 'results': results,
         'limitations': ['Synthetic runner-result controls; they add no successful full clean build or native credit']})
    print({'controls': len(results), 'passed': True, 'sourceCredit': 0})


if __name__ == '__main__':
    run()
