import copy
import json
from pathlib import Path
import time
import parallel_metrics as metrics


ROOT = Path(__file__).resolve().parent


def raw(value):
    return json.dumps(value, sort_keys=True).encode()


class Fixture:
    def __init__(self):
        self.files = {}
        self.revision = 'f' * 40

    def read(self, name, revision=None):
        return self.files.get((revision or self.revision, name))

    def paths(self):
        return [name for revision, name in self.files if revision == self.revision]

    def ancestor(self, revision):
        return revision in {'a' * 40, 'b' * 40}

    def add(self, cohort, source, functions, size, previous, previous_bytes):
        receipt_path = f'evidence/verification/cohort-2026-10-29-{cohort}.json'
        closure_path = f'evidence/verification/cohort{cohort}-expanded-source-closure-20261101.json'
        manifest = raw(dict(functionMatched=functions, sourceLinkedBytes=size, rom=dict(sha256='0' * 64)))
        receipt = raw(dict(linksPending=False, acceptedBuildCreatedUtc='2026-11-02T00:02:00+00:00',
            sourceMatchedFunctions=functions, expectedSourceMatchedFunctions=functions,
            sourceLinkedBytes=size, expectedSourceLinkedBytes=size, moduleComparisonsExact=20,
            negativeAcceptanceChecksPassed=True, sourcePolicyPassed=True,
            manifestSha256=metrics.digest(manifest), previousAcceptedCohort=previous,
            previousAcceptedBytes=previous_bytes, initializedModuleByteDenominator=1000))
        component_path = f'evidence/verification/fixture-component-{cohort}.json'
        component = raw(dict(passed=True, commit=source))
        self.files[self.revision, receipt_path] = self.files[source, receipt_path] = receipt
        self.files[source, 'manifest.json'] = manifest
        self.files[self.revision, component_path] = component
        self.files[self.revision, closure_path] = raw(dict(cohort=cohort, sourceCommit=source, passed=True,
            reports=[dict(path=component_path, sha256=metrics.digest(component))]))
        self.files[source, f'evidence/verification/cohort{cohort}-validation-driver.json'] = raw(dict(
            state='build-and-regression-checks-passed', sourceLinkedBytes=size, sourceMatchedFunctions=functions,
            createdUtc='2026-11-02T00:00:00+00:00', finishedUtc='2026-11-02T00:02:00+00:00', steps=[dict(exitCode=0)]))


def main():
    results = []
    source = Fixture()
    source.add(146, 'a' * 40, 10, 100, 145, 80)
    source.add(147, 'b' * 40, 12, 120, 146, 100)
    history, excluded = metrics.accepted_history(source)
    assert not excluded and history[-1]['acceptedByteDeltaFromBaseline'] == 20 and history[-1]['validationDurationSeconds'] == 120
    results.append('Only committed finalized receipt and matching passed closure grant history credit')
    for label, mutate in [
        ('transient-acceptance-before-closure', lambda fixture: fixture.files.pop((fixture.revision, 'evidence/verification/cohort147-expanded-source-closure-20261101.json'))),
        ('failed-component', lambda fixture: fixture.files.__setitem__((fixture.revision, 'evidence/verification/fixture-component-147.json'), raw(dict(passed=False, commit='b' * 40)))),
        ('receipt-changed-after-source-commit', lambda fixture: fixture.files.__setitem__((fixture.revision, 'evidence/verification/cohort-2026-10-29-147.json'), raw(dict(linksPending=False)))),
        ('source-manifest-tampered', lambda fixture: fixture.files.__setitem__(('b' * 40, 'manifest.json'), raw(dict(functionMatched=999, sourceLinkedBytes=999))))]:
        altered = copy.deepcopy(source)
        mutate(altered)
        history, ignored = metrics.accepted_history(altered)
        assert history[-1]['cohort'] == 146 and ignored[0]['cohort'] == 147
        results.append(label + ' safely falls back to finalized predecessor')
    altered = copy.deepcopy(source)
    altered.files['b' * 40, 'evidence/verification/cohort147-validation-driver.json'] = raw(dict(state='build-and-regression-checks-passed', sourceLinkedBytes=120, sourceMatchedFunctions=12, steps=[dict(exitCode=0)]))
    assert metrics.accepted_history(altered)[0][-1]['validationDurationSeconds'] is None
    assert metrics.seconds('2026-11-02T00:02:00+00:00', '2026-11-02T00:00:00+00:00') is None
    assert metrics.seconds('2026-11-02T00:00:00', '2026-11-02T00:02:00') is None
    results.append('Missing UTC fields, backwards time and naive timestamps never invent durations')
    driver_path = 'b' * 40, 'evidence/verification/cohort147-validation-driver.json'
    altered = copy.deepcopy(source)
    qualified_driver = json.loads(altered.files[driver_path])
    qualified_driver['steps'].append(dict(exitCode=1, externalApplicationSnapshotDifferences=True))
    altered.files[driver_path] = raw(qualified_driver)
    timed = metrics.accepted_history(altered)[0][-1]
    assert timed['validationDurationSeconds'] == 120 and timed['driverRecordedNonzeroExitSteps'] == 1
    results.append('Finalized passed driver interval preserves qualified nonzero command observations')
    qualified_driver['sourceLinkedBytes'] = 999
    altered.files[driver_path] = raw(qualified_driver)
    assert metrics.accepted_history(altered)[0][-1]['validationDurationSeconds'] is None
    results.append('A driver for another accepted byte scope supplies no duration')
    work = ROOT / 'work/parallel-metrics-parallel-wave20261102' / str(time.time_ns())
    lane = work / 'evidence/lanes/parallel-wave20261102/lane'
    lane.mkdir(parents=True)
    (work / 'evidence/verification').mkdir(parents=True)
    accepted = dict(processor='arm9', program='', module='main', mode='arm', address='0x2000000', bytes=16)
    pending = dict(accepted, address='0x2000020')
    unique = dict(accepted, address='0x2000040')
    other_program = dict(unique, program='dwc/utility.bin/move/child.srl')
    source.files['b' * 40, 'ledger/functions.jsonl'] = raw(dict(accepted, states=dict(functionMatched=True))) + b'\n'
    board = dict(pendingSpecifications={'148': 'pending.json'})
    (work / 'evidence/lanes/parallel-wave20261102/dispatch.json').write_bytes(raw(board))
    (work / 'pending.json').write_bytes(raw(dict(cohort=148, expectedAdditions=[pending, pending])))
    (lane / 'ready.json').write_bytes(raw(dict(status='ready-for-coordinator-acceptance', romSha256='0' * 64, functions=5,
        bytes=80, identities=[accepted, pending, unique, unique, other_program])))
    latest = dict(cohort=147, sourceCommit='b' * 40, romSha256='0' * 64)
    queue = metrics.queue_snapshot(work, source, latest)
    assert queue['pending']['functions'] == 1 and queue['pending']['bytes'] == 16
    assert queue['ready']['functions'] == 2 and queue['ready']['bytes'] == 32
    assert queue['ready']['exclusions'] == dict(accepted=1, pending=1, duplicate=1, conflict=0)
    results.append('Ready queue excludes accepted and pending duplicates, preserves distinct program namespaces')
    overlapping = dict(unique, address='0x2000008')
    selected, counts = metrics.select_unique([overlapping], [metrics.extent(accepted)])
    assert not selected and counts['conflict'] == 1
    results.append('Partial byte overlap is a conflict rather than fractional ready credit')
    wrong_rom = json.loads((lane / 'ready.json').read_bytes())
    wrong_rom['romSha256'] = '1' * 64
    (lane / 'ready.json').write_bytes(raw(wrong_rom))
    assert metrics.queue_snapshot(work, source, latest)['ready']['functions'] == 0
    results.append('A different ROM handoff contributes no ready identities')
    (lane / 'ready.json').write_bytes(raw(dict(status='ready-for-coordinator-acceptance', romSha256='0' * 64,
        functions=1, bytes=16, identities=[dict(unique, address='0x2000030')])))
    (work / 'pending.json').write_bytes(raw(dict(cohort=148, expectedAdditions=[pending, dict(pending, address='0x2000028')])))
    ambiguous = metrics.queue_snapshot(work, source, latest)
    assert ambiguous['pending']['bytes'] is None and ambiguous['ready']['functions'] == 0
    results.append('All conflicting pending extents remain reserved and union totals become unknown')
    driver = dict(cohort=148, state='running', pid=123, createdUtc='2026-11-02T00:03:00+00:00', steps=[dict(command=['first.py'], exitCode=0)])
    (work / 'evidence/verification/cohort148-validation-driver.json').write_bytes(raw(driver))
    status = metrics.driver_state(work, 147)
    assert status['reportedState'] == 'running' and status['lastCompletedCommand'] == ['first.py'] and 'activeCommand' not in status
    results.append('Driver reports only recorded state and completed command, without fabricated liveness or active step')
    (work / 'evidence/verification/cohort149-validation-driver.json').write_bytes(raw(dict(driver,
        cohort=149, createdUtc='2026-11-02T00:01:00+00:00')))
    assert metrics.driver_state(work, 147)['cohort'] == 148
    results.append('A newer UTC retry outranks a stale higher-cohort driver without mtime')
    code = (ROOT / 'parallel_metrics.py').read_text()
    assert '.stat(' not in code and 'mtime' not in code.replace('no file mtime', '')
    results.append('No filesystem modification time is queried for history, duration or driver proof')
    report = dict(passed=True, fixtureControls=len(results), controls=results, sourceCredit=0,
        metricsSha256=metrics.digest((ROOT / 'parallel_metrics.py').read_bytes()),
        generatorSha256=metrics.digest(Path(__file__).read_bytes()), fixtures=str(work.relative_to(ROOT)))
    output = ROOT / 'evidence/verification/parallel-wave20261102/parallel-metrics-controls.json'
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
