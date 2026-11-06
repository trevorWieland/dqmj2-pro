import argparse
import subprocess
import sys
import time
from project import ROOT, read_json, write_json, sha256, now


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--specification', required=True)
    parser.add_argument('--transport-receipt', action='append', default=[])
    parser.add_argument('--stage', required=True)
    parser.add_argument('--document', required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--resume-prepared', action='store_true')
    options = parser.parse_args()
    specification = read_json(ROOT / options.specification)
    cohort, previous = specification['cohort'], specification['previousAcceptedCohort']
    assert cohort == previous + 1
    prerequisite = f'evidence/verification/cohort{previous}-expanded-source-closure-20261101.json'
    output = ROOT / f'evidence/verification/cohort{cohort}-continuation-driver-v20-20261105.json'
    result = dict(cohort=cohort, startedUtc=now(), generator=__file__.split('\\')[-1],
        generatorSha256=sha256(__file__), state='waiting-for-prior-committed-package', steps=[])
    write_json(output, result)
    while True:
        path = ROOT / prerequisite
        blob = subprocess.run(['git', 'show', 'HEAD:' + prerequisite], cwd=ROOT, capture_output=True)
        if path.is_file() and blob.returncode == 0 and blob.stdout == path.read_bytes():
            assert read_json(path)['passed']
            break
        time.sleep(5)
    assert not read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{previous}.json')['linksPending']
    has_migrations = bool(specification['migrations'])
    preparer = 'prepare_source_cohort_migrations_20261101.py' if has_migrations else 'prepare_source_cohort_v4_20261102.py'
    publisher = 'publish_prepared_source_migrations_v6_20261101.py' if has_migrations else 'publish_source_cohort_v7_20261105.py'
    commands = [[preparer, options.specification]]
    if options.transport_receipt:
        commands.append(['pin_prepared_replay_transports_20261101.py', '--cohort', str(cohort),
            *[part for name in options.transport_receipt for part in ['--receipt', name]]])
    commands += [[publisher, '--cohort', str(cohort)],
        ['run_source_cohort_20261101.py', '--cohort', str(cohort)],
        ['finalize_source_cohort_20261101.py', '--cohort', str(cohort)],
        ['finish_source_package_v15_20261105.py', '--cohort', str(cohort), '--stage', options.stage,
         '--document', options.document, '--label', options.label]]
    if options.resume_prepared:
        assert not options.transport_receipt and commands[0][0] == preparer
        commands = commands[1:]
        result['preparedTransactionResumedWithoutRecompilationOrRegistryRewrite'] = True
    result['state'] = 'running'
    for index, command in enumerate(commands):
        log = ROOT / f'logs/integration/cohort{cohort}-expanded-v20-continuation-{index:02}-20261101.txt'
        result['currentCommand'] = command
        write_json(output, result)
        with log.open('w', encoding='utf-8') as stream:
            run = subprocess.run([sys.executable, str(ROOT / command[0]), *command[1:]], cwd=ROOT,
                stdout=stream, stderr=subprocess.STDOUT)
        result['steps'].append(dict(command=command, exitCode=run.returncode,
            log=log.relative_to(ROOT).as_posix(), logSha256=sha256(log)))
        if run.returncode:
            result.update(state='failed', finishedUtc=now())
            write_json(output, result)
            raise SystemExit(run.returncode)
    result.update(state='packaged', finishedUtc=now())
    result.pop('currentCommand', None)
    write_json(output, result)
    atlas = [sys.executable, str(ROOT / 'export_reconstruction_atlas.py'), '--revision', 'HEAD']
    pending = list(ROOT.glob(f'cohort{cohort + 1}-*-specification.json'))
    if len(pending) == 1:
        atlas.extend(['--pending', pending[0].name])
    log = ROOT / f'logs/integration/cohort{cohort}-accepted-atlas-20261105.txt'
    with log.open('w', encoding='utf-8') as stream:
        subprocess.run(atlas, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=True)
    result.update(acceptedAtlasRefreshed=True, atlasLog=log.relative_to(ROOT).as_posix(), atlasLogSha256=sha256(log))
    write_json(output, result)


if __name__ == '__main__':
    main()
