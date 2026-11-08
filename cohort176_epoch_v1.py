import copy
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess


OLD = 'f792a31d3bbe574aeced9f6146576999e4d0e28bc5517111ada5b5b8dda82629'
NEW = '8c09a25ee61fa3b684cc0d8204f94919b363476c0b1433da30f39f4467bf1d34'
PREFS = 'c7697573f1cdbb32f4d5f89665c2ec176ba49e6817466fd42edcce31d848c2ef'
SOURCE = '217601b0b0c11a5941c7b42d65228f6edf9c0b25'
EXPECTED = {('', 'arm9', 'ov001', 'arm', 0x222595c): 592,
    ('', 'arm9', 'ov001', 'arm', 0x2226598): 168,
    ('', 'arm9', 'ov001', 'arm', 0x2226290): 128,
    ('', 'arm9', 'ov001', 'arm', 0x2225854): 132,
    ('', 'arm9', 'ov001', 'arm', 0x22258d8): 132,
    ('', 'arm9', 'ov006', 'thumb', 0x2202f98): 32,
    ('dwc/utility.bin/move/child.srl', 'arm7', 'utility-child-arm7-wram', 'arm', 0x37fd448): 60,
    ('dwc/utility.bin/move/child.srl', 'arm7', 'utility-child-arm7-wram', 'arm', 0x37fd3a0): 168}
ACCOUNTING = dict(rawLogicalAliasCount=21538, canonicalPathCount=21537,
    removedDuplicateKeys=1, canonicalSourceQueries=1, explicitCopiedDependencyPaths=983, sourceCredit=0)


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def identity(row):
    return (row.get('program') or '', row['processor'], row['module'], row['mode'], int(row['address'], 0))


def safe(name):
    path = PurePosixPath(name)
    require(isinstance(name, str) and name == path.as_posix() and not path.is_absolute()
        and '..' not in path.parts and not any(c in name for c in '\\:\n\r\0') and name not in ('', '.'), 'Unsafe input path')
    return name


def registry_delta(baseline, current, added):
    require({k: v for k, v in baseline.items() if k != 'batches'} == {k: v for k, v in current.items() if k != 'batches'}, 'Registry metadata changed')
    old = {b['report']: b for b in baseline['batches']}
    require(len(old) == len(baseline['batches']) == 1375 and len(current['batches']) == 1382, 'Registry membership count differs')
    require(len({b['report'] for b in current['batches']}) == 1382, 'Duplicate report')
    require([b for b in current['batches'] if b['report'] in old] == baseline['batches'], 'Historical record or relative order changed')
    additions = [b for b in current['batches'] if b['report'] not in old]
    require(len(additions) == 7 and {b['report']: canonical(b) for b in additions} == added, 'Unknown changed or missing addition')
    return additions


class Epoch:
    def __init__(self, contract, trusted_hash, baseline_raw, current_raw, preferences_raw, read_current, read_committed):
        require(canonical(contract) == trusted_hash, 'Untrusted epoch contract')
        require(contract['schemaVersion'] == 1 and contract['cohort'] == 176 and contract['sourceCredit'] == 0, 'Wrong epoch scope')
        require(contract['baselineSourceCommit'] == SOURCE and contract['baselineRegistrySha256'] == OLD
            and contract['registrySha256'] == NEW and contract['preferencesSha256'] == PREFS, 'Unapproved epoch boundary')
        require(sha(baseline_raw) == OLD and sha(current_raw) == NEW and sha(preferences_raw) == PREFS, 'Wrong registry or preferences')
        require(read_committed('recovery.json') == current_raw and read_committed('source-preferences.json') == preferences_raw, 'Current epoch is not exact committed bytes')
        baseline, current = json.loads(baseline_raw), json.loads(current_raw)
        additions = registry_delta(baseline, current, contract['addedBatches'])
        require(set(contract['reports']) == {b['report'] for b in additions}, 'Unbound report contract')
        rows, reports = {}, {}
        for batch in additions:
            name = safe(batch['report'])
            raw = read_current(name)
            require(raw == read_committed(name) and sha(raw) == contract['reports'][name]['sha256'], 'Uncommitted or changed report')
            report = json.loads(raw)
            require(report.get('allPassed') is True and report['romSha256'] == contract['romSha256'], 'Failed report or wrong ROM')
            require(canonical(report['matches']) == contract['reports'][name]['rowsSha256'] and len(report['matches']) == batch['entries'], 'Complete source object profile or row set changed')
            refs = {p: h for p, h in batch['sourceHashes'].items() if p.startswith('extract/')}
            require(refs == contract['reports'][name]['referencePins'], 'Unknown original reference')
            for row in report['matches']:
                key = identity(row)
                require(key not in rows and EXPECTED.get(key) == row['bytes'] == row['compiledBytes'], 'Wrong full function namespace or extent')
                rows[key] = row
            reports[name] = report
        require({k: r['bytes'] for k, r in rows.items()} == EXPECTED, 'Exact eight-function union differs')
        require(sum(len(v['referencePins']) for v in contract['reports'].values()) == 9, 'Nine-field comparison boundary differs')
        require(contract['accounting'] == ACCOUNTING, 'Unapproved path accounting')
        self.contract = copy.deepcopy(contract)
        self.contract_hash = trusted_hash
        self.raw = current_raw
        self.registry = current
        self.registry_hash = canonical(current)
        self.reports = reports
        self.rows = rows
        self.read_current = read_current
        self.read_committed = read_committed
        self.current_hashes = {'recovery.json': NEW, 'source-preferences.json': PREFS}
        self.committed_revision = None
        self.current_hashes.update({p: value['sha256'] for p, value in contract['reports'].items()})
        for pin in [*contract['supportPins'], *contract['implementationPins']]:
            name = safe(pin['path'])
            require(sha(read_current(name)) == pin['sha256'] and read_current(name) == read_committed(name), 'Changed or uncommitted support')
            self.current_hashes[name] = pin['sha256']
        self.ensure()

    @classmethod
    def committed(cls, root, contract, trusted_hash, revision):
        root = Path(root).resolve()
        require(len(revision) == 40 and all(c in '0123456789abcdef' for c in revision), 'Resolved commit required')
        def blob(name, commit=revision):
            return subprocess.check_output(['git', 'show', commit + ':' + safe(name)], cwd=root)
        resolved = subprocess.check_output(['git', 'rev-parse', revision + '^{commit}'], cwd=root, text=True).strip()
        head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
        require(resolved == head == revision, 'Commit binding changed')
        subprocess.run(['git', 'merge-base', '--is-ancestor', SOURCE, revision], cwd=root, check=True, capture_output=True)
        def read(name):
            path = root / safe(name)
            require(path.resolve() == path.absolute() and path.resolve().is_relative_to(root) and not path.is_symlink(), 'Escaping committed input')
            return path.read_bytes()
        result = cls(contract, trusted_hash, blob('recovery.json', SOURCE), read('recovery.json'), read('source-preferences.json'), read, blob)
        result.committed_revision = revision
        result.check_commit = lambda: subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
        result.ensure()
        return result

    def ensure(self):
        require(canonical(self.contract) == self.contract_hash, 'Epoch contract changed')
        require(canonical(self.registry) == self.registry_hash, 'In-memory canonical registry changed')
        require(self.committed_revision is None or self.check_commit() == self.committed_revision, 'Committed audit epoch moved')
        for name, expected in self.current_hashes.items():
            raw = self.read_current(name)
            require(sha(raw) == expected and raw == self.read_committed(name), 'Epoch input changed: ' + name)
            if name in self.reports:
                require(json.loads(raw) == self.reports[name], 'In-memory canonical report changed')

    def check_canonical(self, actual):
        self.ensure()
        require(actual == self.registry['batches'], 'Projection did not receive full canonical registry')

    def project(self, actual, live):
        from cohort176_native_reference_v1 import LiveReferences
        self.check_canonical(actual)
        require(isinstance(live, LiveReferences), 'A receipt cannot authorize projection')
        live.ensure(self)
        require(live.identities == {k for k in EXPECTED if k[1] == 'arm9'}, 'Wrong live reference union')
        result, events = copy.deepcopy(actual), []
        for batch in result:
            declared = self.contract['reports'].get(batch['report'])
            if declared is None:
                continue
            for name, expected in declared['referencePins'].items():
                require(batch['sourceHashes'].pop(name) == expected, 'Comparison field changed')
                events.append(dict(report=batch['report'], path=name, sha256=expected))
        require(len(events) == 9, 'Wrong comparison projection count')
        restored = copy.deepcopy(result)
        for event in events:
            next(b for b in restored if b['report'] == event['report'])['sourceHashes'][event['path']] = event['sha256']
        require(restored == actual, 'Projection changed noncomparison fields')
        return result, events


@contextmanager
def installed_projection(module, epoch, live):
    original = module.project_batches
    events = []
    def projected(actual, report, declared):
        copies, removed = epoch.project(actual, live)
        events.append(removed)
        return original(copies, report, declared)
    module.project_batches = projected
    try:
        yield events
    finally:
        changed = module.project_batches is not projected
        module.project_batches = original
        require(not changed, 'Projection binding unexpectedly changed')
        epoch.ensure()


def accounting(document):
    require(document.get('passed') is True and document.get('sourceCredit') == 0, 'Underlying V8 did not pass')
    require(document['registeredRepositoryPathsChecked'] == 21537 and document['explicitCopiedDependencyPaths'] == 983, 'Actual V8 path accounting differs')
    return copy.deepcopy(ACCOUNTING)
