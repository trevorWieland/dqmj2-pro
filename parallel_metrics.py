import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
DISPATCH = 'evidence/lanes/parallel-wave20261102/dispatch.json'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class Committed:
    def __init__(self, root, revision):
        self.root = root
        self.revision = subprocess.run(['git', 'rev-parse', revision + '^{commit}'], cwd=root,
            capture_output=True, text=True, check=True).stdout.strip()
        self.cache = {}

    def read(self, name, revision=None):
        key = revision or self.revision, name
        if key not in self.cache:
            process = subprocess.run(['git', 'show', key[0] + ':' + name], cwd=self.root, capture_output=True)
            self.cache[key] = process.stdout if process.returncode == 0 else None
        return self.cache[key]

    def paths(self):
        return subprocess.run(['git', 'ls-tree', '-r', '--name-only', self.revision, '--', 'evidence/verification'],
            cwd=self.root, capture_output=True, text=True, check=True).stdout.splitlines()

    def ancestor(self, revision):
        return subprocess.run(['git', 'merge-base', '--is-ancestor', revision, self.revision],
            cwd=self.root, capture_output=True).returncode == 0


def parse(raw):
    return json.loads(raw) if raw is not None else None


def seconds(start, finish):
    try:
        first = datetime.fromisoformat(start.replace('Z', '+00:00'))
        last = datetime.fromisoformat(finish.replace('Z', '+00:00'))
        if first.utcoffset() is None or last.utcoffset() is None or last < first:
            return None
        return (last - first).total_seconds()
    except (TypeError, ValueError, AttributeError):
        return None


def accepted_history(committed, first=146):
    cohorts = sorted(int(match[1]) for name in committed.paths()
        if (match := re.fullmatch(r'evidence/verification/cohort-2026-10-29-(\d+)\.json', name)) and int(match[1]) >= first)
    history, excluded = [], []
    for cohort in cohorts:
        receipt_path = f'evidence/verification/cohort-2026-10-29-{cohort}.json'
        closure_path = f'evidence/verification/cohort{cohort}-expanded-source-closure-20261101.json'
        try:
            raw, closed = committed.read(receipt_path), committed.read(closure_path)
            receipt, closure = parse(raw), parse(closed)
            if not closure or closure.get('passed') is not True or closure.get('cohort') != cohort:
                raise ValueError('No committed passed closure')
            source = closure['sourceCommit']
            if not committed.ancestor(source) or committed.read(receipt_path, source) != raw:
                raise ValueError('Closure does not bind this committed finalized receipt')
            if not (receipt.get('linksPending') is False and receipt.get('acceptedBuildCreatedUtc') and
                receipt.get('sourceMatchedFunctions') == receipt.get('expectedSourceMatchedFunctions') and
                receipt.get('sourceLinkedBytes') == receipt.get('expectedSourceLinkedBytes') and
                receipt.get('moduleComparisonsExact') == 20 and receipt.get('negativeAcceptanceChecksPassed') is True and
                receipt.get('sourcePolicyPassed') is True):
                raise ValueError('Receipt is not finalized')
            if not closure.get('reports'):
                raise ValueError('Closure has no immutable component proofs')
            for pin in closure['reports']:
                component_raw = committed.read(pin['path'])
                if component_raw is None or digest(component_raw) != pin['sha256']:
                    raise ValueError('Committed closure component missing or changed')
                component = parse(component_raw)
                proof = component.get('committedVerification', component)
                if proof.get('passed') is not True or proof.get('commit') != source:
                    raise ValueError('Closure component is unpassed or names another source commit')
                if component.get('capturedClosure'):
                    captured = committed.read(component['capturedClosure'])
                    if captured is None or digest(captured) != component['capturedClosureSha256'] or component.get('currentContentHashesRechecked') is not True:
                        raise ValueError('Captured oracle closure is not bound and rechecked')
            manifest_raw = committed.read('manifest.json', source)
            manifest = parse(manifest_raw)
            if manifest_raw is None or digest(manifest_raw) != receipt['manifestSha256'] or manifest['functionMatched'] != receipt['sourceMatchedFunctions'] or manifest['sourceLinkedBytes'] != receipt['sourceLinkedBytes']:
                raise ValueError('Finalized source manifest does not match receipt')
            if history and (receipt['previousAcceptedCohort'] != history[-1]['cohort'] or receipt['previousAcceptedBytes'] != history[-1]['bytes']):
                raise ValueError('Finalized predecessor is unavailable or inconsistent')
            driver_path = f'evidence/verification/cohort{cohort}-validation-driver.json'
            driver = parse(committed.read(driver_path, source)) or {}
            timing = None
            if driver.get('state') == 'build-and-regression-checks-passed' and driver.get('sourceLinkedBytes') == receipt['sourceLinkedBytes'] and driver.get('sourceMatchedFunctions') == receipt['sourceMatchedFunctions']:
                timing = seconds(driver.get('createdUtc'), driver.get('finishedUtc'))
            history.append(dict(cohort=cohort, functions=receipt['sourceMatchedFunctions'], bytes=receipt['sourceLinkedBytes'],
                sourceCommit=source, receipt=receipt_path, receiptSha256=digest(raw), closure=closure_path, closureSha256=digest(closed),
                acceptedBuildCreatedUtc=receipt['acceptedBuildCreatedUtc'], validationStartedUtc=driver.get('createdUtc'),
                validationFinishedUtc=driver.get('finishedUtc'), validationDurationSeconds=timing,
                driverRecordedNonzeroExitSteps=sum(1 for row in driver.get('steps', []) if row.get('exitCode')),
                initializedModuleByteDenominator=receipt['initializedModuleByteDenominator'],
                romSha256=manifest['rom']['sha256'],
                initializedModuleSourcePercentage=receipt['sourceLinkedBytes'] * 100 / receipt['initializedModuleByteDenominator'],
                sourceOnlyRomProven=receipt.get('sourceOnlyRomProven', False)))
        except (ValueError, KeyError, TypeError) as error:
            excluded.append(dict(cohort=cohort, reason=str(error)))
    if not history or history[0]['cohort'] != first:
        raise ValueError('Committed finalized baseline is unavailable')
    baseline = history[0]['bytes']
    for row in history:
        row['acceptedByteDeltaFromBaseline'] = row['bytes'] - baseline
    return history, excluded


def extent(row):
    module = row['module']
    cpu = row.get('processor') or ('arm7' if 'arm7' in module else 'arm9')
    program = row.get('program') or ('dwc/utility.bin/move/child.srl' if module.startswith('utility-child-') else '')
    address = int(row['address'], 0) if isinstance(row['address'], str) else row['address']
    size = int(row['bytes'], 0) if isinstance(row['bytes'], str) else row['bytes']
    mode = row['mode']
    if size <= 0 or mode not in ('arm', 'thumb') or address % (4 if mode == 'arm' else 2):
        raise ValueError('Invalid function extent')
    return (program, cpu, module), address, address + size, mode


def overlap(left, right):
    return left[0] == right[0] and left[1] < right[2] and right[1] < left[2]


def select_unique(rows, accepted, reserved=()):
    selected, counts = [], dict(accepted=0, pending=0, duplicate=0, conflict=0)
    for row in rows:
        value = extent(row)
        hits = [other for other in accepted if overlap(value, other)]
        category = 'accepted'
        if not hits:
            hits = [other for other in reserved if overlap(value, other)]
            category = 'pending'
        if not hits:
            hits = [other for previous, other in selected if overlap(value, other)]
            category = 'duplicate'
        if hits:
            counts[category if value in hits else 'conflict'] += 1
        else:
            selected.append((row, value))
    return selected, counts


def working_json(root, name):
    try:
        return json.loads((root / name).read_text(encoding='utf-8-sig'))
    except (OSError, ValueError):
        return None


def queue_snapshot(root, committed, latest, extra_pending=()):
    ledger = committed.read('ledger/functions.jsonl', latest['sourceCommit'])
    accepted = [extent(row) for line in ledger.splitlines() if (row := json.loads(line))['states']['functionMatched']]
    board = working_json(root, DISPATCH) or {}
    paths = list(extra_pending) + [path for cohort, path in board.get('pendingSpecifications', {}).items() if int(cohort) > latest['cohort']]
    for path in (root / 'evidence/verification').glob('cohort-2026-10-29-*.json'):
        receipt = working_json(root, path.relative_to(root))
        if receipt and receipt.get('specification') and (match := re.search(r'-(\d+)\.json$', path.name)) and int(match[1]) > latest['cohort']:
            raw = (root / receipt['specification']).read_bytes() if (root / receipt['specification']).is_file() else None
            if raw and digest(raw) == receipt.get('specificationSha256'):
                paths.append(receipt['specification'])
    pending_rows, pending_inputs, unavailable = [], [], []
    for name in dict.fromkeys(paths):
        spec = working_json(root, name)
        if not spec or spec.get('cohort', 0) <= latest['cohort']:
            unavailable.append(str(name))
            continue
        pending_rows.extend(spec.get('expectedAdditions', []))
        pending_inputs.append(dict(path=str(name), sha256=digest((root / name).read_bytes()), cohort=spec['cohort']))
    pending, pending_counts = select_unique(pending_rows, accepted)
    reserved = [extent(row) for row in pending_rows]
    ready_rows, packets, invalid = [], [], []
    ready_paths = [path for wave in (root / 'evidence/lanes').glob('parallel-wave*')
                   if wave.is_dir() for path in wave.rglob('*ready*.json')]
    for path in sorted(ready_paths):
        ready = working_json(root, path.relative_to(root))
        if not ready or ready.get('status') != 'ready-for-coordinator-acceptance':
            continue
        rows = ready.get('identities', [])
        if ready.get('romSha256') != latest['romSha256'] or len(rows) != ready.get('functions') or sum(row['bytes'] for row in rows) != ready.get('bytes'):
            invalid.append(path.relative_to(root).as_posix())
            continue
        name = path.relative_to(root).as_posix()
        packets.append(dict(path=name, functions=len(rows), bytes=ready['bytes']))
        ready_rows.extend(dict(row, packet=name) for row in rows)
    unique, counts = select_unique(ready_rows, accepted, reserved)
    identities = [dict(program=value[0][0], processor=value[0][1], module=value[0][2], address=hex(value[1]),
        mode=value[3], bytes=value[2]-value[1], packet=row['packet']) for row, value in unique]
    return dict(scope='Observed working-tree handoffs; zero accepted credit',
        pending=dict(functions=None if pending_counts['conflict'] else len(pending),
            bytes=None if pending_counts['conflict'] else sum(value[2]-value[1] for row, value in pending), inputs=pending_inputs, exclusions=pending_counts),
        ready=dict(functions=len(unique), bytes=sum(row['bytes'] for row in identities), identities=identities, exclusions=counts, packets=packets),
        unavailablePendingInputs=unavailable, invalidReadyPackets=invalid)


def driver_state(root, accepted_cohort):
    drivers = []
    for path in (root / 'evidence/verification').glob('cohort*-validation-driver.json'):
        data = working_json(root, path.relative_to(root))
        if data and data.get('cohort', 0) > accepted_cohort:
            drivers.append((data.get('cohort', 0), data.get('createdUtc') or '', path, data))
    if not drivers:
        return None
    def stamp(row):
        try:
            value = datetime.fromisoformat(row[1].replace('Z', '+00:00'))
            return value.timestamp() if value.utcoffset() is not None else float('-inf')
        except (ValueError, TypeError, OverflowError):
            return float('-inf')
    cohort, started, path, data = max(drivers, key=lambda row: (stamp(row), row[0]))
    steps = data.get('steps', [])
    return dict(scope='Observed working-tree driver report; process liveness unverified', cohort=cohort,
        reportedState=data.get('state'), reportedPid=data.get('pid'), startedUtc=data.get('createdUtc'),
        finishedUtc=data.get('finishedUtc'), completedSteps=len(steps), lastCompletedCommand=steps[-1].get('command') if steps else None,
        failedCommands=[row.get('command') for row in steps if row.get('exitCode')], report=path.relative_to(root).as_posix())


def snapshot(root=ROOT, revision='HEAD', first=146, pending=()):
    committed = Committed(root, revision)
    history, excluded = accepted_history(committed, first)
    latest = history[-1]
    return dict(schemaVersion=1, committedRevision=committed.revision, accepted=latest, acceptedHistory=history,
        unfinalizedCommittedCohorts=excluded, queue=queue_snapshot(root, committed, latest, pending),
        currentDriver=driver_state(root, latest['cohort']),
        timingScope='Only immutable successful-driver UTC start/finish; no file mtime, prior-attempt total or productivity score',
        overallGameCompletionPercentage=None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--pretty', action='store_true')
    parser.add_argument('--revision', default='HEAD')
    parser.add_argument('--pending', action='append', default=[])
    options = parser.parse_args()
    result = snapshot(revision=options.revision, pending=options.pending)
    if options.json or options.pretty:
        print(json.dumps(result, indent=2 if options.pretty else None, separators=None if options.pretty else (',', ':')))
    else:
        row = result['accepted']
        print(f"Accepted{row['cohort']}: {row['functions']:,} functions / {row['bytes']:,} initialized bytes; +{row['acceptedByteDeltaFromBaseline']:,} bytes since146")
        print('Ready unique: {functions} functions / {bytes} bytes'.format(**result['queue']['ready']))
        print('Pending union: {functions} functions / {bytes} bytes'.format(**result['queue']['pending']))
        if result['currentDriver']:
            print('Driver{cohort}: {reportedState}; {completedSteps} completed steps'.format(**result['currentDriver']))


if __name__ == '__main__':
    main()
