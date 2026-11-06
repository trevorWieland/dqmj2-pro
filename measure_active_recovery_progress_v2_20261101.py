import json
import subprocess
from pathlib import Path
from project import ROOT, now, sha256, write_json


def main():
    accepted = []
    for path in (ROOT / 'evidence/verification').glob('cohort-2026-10-29-*.json'):
        try:
            number = int(path.stem.rsplit('-', 1)[1])
        except ValueError:
            continue
        closure = ROOT / f'evidence/verification/cohort{number}-expanded-source-closure-20261101.json'
        if not closure.is_file():
            continue
        relative = closure.relative_to(ROOT).as_posix()
        committed = subprocess.run(['git', 'show', 'HEAD:' + relative], cwd=ROOT, capture_output=True)
        if committed.returncode or committed.stdout != closure.read_bytes():
            continue
        record = json.loads(path.read_bytes())
        if not record.get('linksPending', True) and json.loads(closure.read_bytes())['passed']:
            accepted.append((number, path, record))
    number, path, current = max(accepted, key=lambda row: row[0])
    histories = sorted((ROOT / 'evidence/attempts').glob('main-*breadth*-20261101.json'))
    identities = {}
    for history in histories:
        document = json.loads(history.read_bytes())
        for row in document.get('results', []):
            if not isinstance(row, dict) or 'address' not in row:
                continue
            address = int(row['address'], 0) if isinstance(row['address'], str) else row['address']
            key = (row.get('mode', 'arm'), address)
            state = identities.setdefault(key, dict(drafted=False, compiled=False, bytes=row.get('bytes', 0)))
            state['drafted'] |= bool(row.get('attempts'))
            state['compiled'] |= bool(row.get('compilable'))
    result = dict(createdUtc=now(), generator=Path(__file__).name, generatorSha256=sha256(__file__),
        acceptedCohort=number, acceptedEvidence=dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)),
        sourceMatchedFunctions=current['sourceMatchedFunctions'], sourceLinkedInitializedBytes=current['sourceLinkedBytes'],
        initializedModuleByteDenominator=current['initializedModuleByteDenominator'],
        sourceInitializedBytePercentage=current['sourceCoveragePercentage'], overallGamePercentage=None,
        executableOnlyDenominatorProven=current['executableOnlyDenominatorProven'],
        unresolvedInitializedModuleBytes=current['unresolvedInitializedModuleBytes'],
        exactSourceOnlyRom=current['sourceOnlyRomProven'], fullWindowsGame=current['fullWindowsGameFromSourceProven'],
        androidDeviceExecutions=current['androidDeviceExecutionCount'],
        bulkUniqueResultIdentities=len(identities), bulkDraftedFunctions=sum(row['drafted'] for row in identities.values()),
        bulkCompilableFunctions=sum(row['compiled'] for row in identities.values()),
        bulkCompilableNativeBytes=sum(row['bytes'] for row in identities.values() if row['compiled']),
        bulkCredit=0, bulkReports=[dict(path=file.relative_to(ROOT).as_posix(), sha256=sha256(file)) for file in histories],
        limitations=['Initialized module bytes include literal pools and data',
            'Bulk results are generated hypotheses and may overlap subsequently accepted sources',
            'Compilation and native component tests do not prove a complete game port'])
    write_json(ROOT / 'evidence/verification/active-recovery-progress-v2-20261101.json', result)
    print({key: value for key, value in result.items() if key not in ['bulkReports', 'limitations']})


if __name__ == '__main__':
    main()
