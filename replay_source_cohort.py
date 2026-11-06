import argparse
import subprocess
import sys
from project import ROOT, now, read_json, sha256, write_json
from recovery_registry import entries


def projection(report):
    keys = ('name', 'module', 'processor', 'mode', 'address', 'bytes', 'size', 'source',
            'sourceSha256', 'targetSha256', 'compilerSha256', 'flags', 'compilerFlags')
    return [{key: row[key] for key in keys if key in row} for row in entries(report)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--lane', required=True)
    args = parser.parse_args()
    plan = read_json(ROOT / f'evidence/verification/cohort{args.cohort}-replay-plan.json')
    output = ROOT / f'evidence/verification/cohort{args.cohort}-{args.lane}-replays.json'
    result = {'createdUtc': now(), 'cohort': args.cohort, 'lane': args.lane, 'passed': False, 'steps': []}
    for index, job in enumerate(plan['lanes'][args.lane]):
        for relative, expected in job['sourceHashes'].items():
            if sha256(ROOT / relative) != expected:
                raise ValueError('Pending source/dependency changed: ' + relative)
        log = ROOT / f'logs/integration/cohort{args.cohort}-{args.lane}-{index:02d}.txt'
        log.parent.mkdir(parents=True, exist_ok=True)
        before = sha256(ROOT / job['report'])
        with log.open('w', encoding='utf-8') as stream:
            process = subprocess.run([sys.executable, str(ROOT / job['script'])], cwd=ROOT.parent,
                                     stdout=stream, stderr=subprocess.STDOUT)
        after = read_json(ROOT / job['report'])
        unchanged = all(sha256(ROOT / path) == pin for path, pin in job['sourceHashes'].items())
        step = {'script': job['script'], 'report': job['report'], 'exitCode': process.returncode,
                'sourceClosureUnchanged': unchanged, 'sourceIdentityUnchanged': projection(after) == job['identities'],
                'beforeReportSha256': before, 'afterReportSha256': sha256(ROOT / job['report']),
                'log': log.relative_to(ROOT).as_posix(), 'logSha256': sha256(log)}
        result['steps'].append(step)
        write_json(output, result)
        print(step, flush=True)
        if process.returncode or not unchanged or not step['sourceIdentityUnchanged']:
            raise ValueError('Pending source replay failed: ' + job['script'])
    result['passed'] = True
    write_json(output, result)


if __name__ == '__main__':
    main()
