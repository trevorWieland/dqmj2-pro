import argparse
import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, sha256, write_json
import finish_source_package_context as original_context


AUDIT = 'verify_committed_source_context.py'
ORIGINAL_CONTEXT_SHA = 'd714b405bae27f640cdbe9f8dad362d993ecfd300643db2f40c57c4b16c12aa4'


def git(*arguments):
    return subprocess.check_output(['git', '--literal-pathspecs', *arguments], cwd=ROOT)


class AdditionalQualification:
    def __init__(self, context, source_commit, run=None):
        self.context = context
        self.source_commit = source_commit
        self.original_run = context.previous_run
        self.original_write = context.previous_write
        self.command = run or subprocess.run
        self.extra = f'evidence/verification/cohort{context.cohort}-child-arm9-reference-context-20261107.json'
        self.audit_done = False
        self.written_hash = None
        self.closure_hash = None
        self.staged = False

    def audit(self, command, log):
        expected = [sys.executable, str(ROOT / 'verify_committed_source_inputs_context_v10_20261106.py'),
                    '--cohort', str(self.context.cohort)]
        if command == expected:
            if self.audit_done:
                raise ValueError('Additional committed-input audit must run exactly once')
            command = [sys.executable, str(ROOT / AUDIT), '--cohort', str(self.context.cohort)]
            result = self.original_run(command, log)
            self.audit_done = True
            return result
        return self.original_run(command, log)

    def write(self, path, value):
        if Path(path) != ROOT / self.context.closure:
            return self.original_write(path, value)
        if not self.audit_done or self.written_hash is not None:
            raise ValueError('Fresh additional audit must precede closure exactly once')
        expected = [*self.context.reports, self.context.extra]
        if [row['path'] for row in value['reports']] != expected:
            raise ValueError('Inherited three closure components changed')
        if value['sourceCommit'] != self.source_commit:
            raise ValueError('The original source commit changed')
        if any(row['sha256'] != sha256(ROOT / row['path']) for row in value['reports']):
            raise ValueError('Inherited closure bytes changed')
        proof = read_json(ROOT / self.extra)
        if proof.get('sourceCredit') != 0 or not all(proof.get(key) is True for key in [
                'passed', 'allOriginalContextV10AuditsCompleted',
                'canonicalSourceRegistryUnchanged', 'frozenCohortMembershipUnchanged']):
            raise ValueError('Fresh child ARM9 qualification did not complete inherited audits')
        result = copy.deepcopy(value)
        self.written_hash = sha256(ROOT / self.extra)
        result['reports'].append(dict(path=self.extra, sha256=self.written_hash))
        result['committedPackageContinuation'] = dict(generator=Path(__file__).name,
            generatorSha256=sha256(__file__), originalSourceCommit=self.source_commit,
            originalContextSha256=ORIGINAL_CONTEXT_SHA, sourceCredit=0)
        written = self.original_write(path, result)
        self.closure_hash = sha256(ROOT / self.context.closure)
        return written

    def validate_closure(self):
        document = read_json(ROOT / self.context.closure)
        paths = [*self.context.reports, self.context.extra, self.extra]
        if (self.closure_hash is None or sha256(ROOT / self.context.closure) != self.closure_hash
                or [row['path'] for row in document['reports']] != paths
                or document['sourceCommit'] != self.source_commit
                or any(row['sha256'] != sha256(ROOT / row['path']) for row in document['reports'])):
            raise ValueError('Expanded continuation closure changed before publication')
        return paths

    def run(self, command, *args, **kwargs):
        expected = ['git', 'add', '--', *self.context.reports, self.context.extra, self.context.closure]
        if command == expected:
            if self.written_hash is None or self.staged or sha256(ROOT / self.extra) != self.written_hash:
                raise ValueError('Additional closure must be unchanged and staged exactly once')
            paths = self.validate_closure()
            command = ['git', 'add', '--', *paths, self.context.closure]
            result = self.command(command, *args, **kwargs)
            self.staged = True
            return result
        if command[:2] == ['git', 'commit']:
            paths = [*self.context.reports, self.context.extra, self.extra, self.context.closure]
            expected = ['git', 'commit', '--only', '-m',
                        f'Verify cohort {self.context.cohort} committed source and oracle closure', '--', *paths]
            if command != expected or not self.staged:
                raise ValueError('Only the explicitly staged closure transaction may be committed')
            self.validate_closure()
        return self.command(command, *args, **kwargs)

    def complete(self):
        self.context.complete()
        if not self.audit_done or self.written_hash is None or not self.staged:
            raise ValueError('Additional qualification did not complete every action')


def preflight(cohort, source_commit):
    original_context.verify()
    if sha256(ROOT / 'finish_source_package_context.py') != ORIGINAL_CONTEXT_SHA:
        raise ValueError('Original stable finisher context changed')
    for name in [Path(__file__).name, AUDIT]:
        if git('show', 'HEAD:' + name) != (ROOT / name).read_bytes():
            raise ValueError('Continuation support must be committed before activation: ' + name)
    git('merge-base', '--is-ancestor', source_commit, 'HEAD')
    import run_source_cohort_v6_20261106 as runner
    runner.verify()
    driver_name = f'evidence/verification/cohort{cohort}-validation-driver.json'
    plan_name = f'evidence/verification/cohort-2026-10-29-{cohort}.json'
    driver, plan = read_json(ROOT / driver_name), read_json(ROOT / plan_name)
    if (driver['state'] != 'build-and-regression-checks-passed' or len(driver['steps']) != 16
            or [row['command'] for row in driver['steps']] != runner.expected_commands()):
        raise ValueError('The original sixteen qualified stages are required')
    for row in driver['steps']:
        if sha256(ROOT / row['log']) != row['logSha256']:
            raise ValueError('An original stage log changed')
        if row['exitCode'] and not (row['exitCode'] == 1 and row.get('externalApplicationSnapshotDifferences') is True):
            raise ValueError('An original stage did not pass')
    if plan['linksPending'] or (plan['sourceMatchedFunctions'], plan['sourceLinkedBytes']) != (11640, 1262114):
        raise ValueError('The finalized cohort174 source frontier changed')
    names = [driver_name, plan_name, 'recovery.json', 'source-preferences.json', 'manifest.json',
             'ledger/functions.jsonl', plan['specification'], 'verify_captured_oracle_closure_20261031.py',
             f'evidence/verification/accepted-cohort{cohort}-identities-v2-20261101.json',
             f'evidence/verification/cohort{cohort}-captured-oracle-closure-20261031.json']
    for name in names:
        if git('show', source_commit + ':' + name) != (ROOT / name).read_bytes():
            raise ValueError('The original committed source frontier changed: ' + name)
    return plan


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True, choices=[174])
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--index-state', type=Path, required=True)
    options = parser.parse_args()
    source_commit = git('rev-parse', options.source_commit + '^{commit}').decode().strip()
    plan = preflight(options.cohort, source_commit)
    output = options.output.resolve()
    if not output.is_relative_to(ROOT / 'work') or output.exists():
        raise ValueError('Continuation needs a new dedicated work output directory')
    protected = sorted(set(read_json(options.index_state)['restoredExcludedIndexPaths']))
    index_before = git('ls-files', '--stage', '-z', '--', *protected)
    working_before = {name: sha256(ROOT / name) for name in protected}
    output.mkdir(parents=True)
    (output / 'protected.index').write_bytes(index_before)
    spec = importlib.util.spec_from_file_location('unchanged_source_finisher', ROOT / original_context.ORIGINAL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    context = original_context.Context(module, options.cohort)
    additional = AdditionalQualification(context, source_commit)
    context.previous_run, context.previous_write = additional.audit, additional.write
    previous_command = original_context.run_command
    original_context.run_command = additional.run
    state = dict(status='running', sourceCommit=source_commit, sourceCredit=0,
                 protectedIndexPaths=protected, protectedWorkingHashes=working_before)
    write_json(output / 'state.json', state)
    try:
        audit_log = f'logs/integration/cohort{options.cohort}-source-input-resume-20261107.txt'
        captured_log = f'logs/integration/cohort{options.cohort}-captured-closure-resume-20261107.txt'
        outputs = [audit_log, captured_log, context.closure, *context.reports, context.extra, additional.extra]
        if any((ROOT / name).exists() for name in outputs):
            raise ValueError('Preserve existing continuation outputs before retrying')
        context.audit([sys.executable, str(ROOT / 'verify_committed_source_inputs_context_v9_20261106.py'),
                       '--cohort', str(options.cohort)], audit_log)
        additional.original_run([sys.executable, str(ROOT / 'verify_captured_oracle_closure_20261031.py'),
                                 '--cohort', str(options.cohort)], captured_log)
        if (not read_json(ROOT / context.reports[0])['passed']
                or not read_json(ROOT / context.reports[1])['committedVerification']['passed']):
            raise ValueError('The original committed-source and captured-oracle audits must pass')
        context.write(ROOT / context.closure, dict(cohort=options.cohort, sourceCommit=source_commit,
            passed=True, sourceCredit=0, fullCleanReplayProven=False,
            reports=[dict(path=name, sha256=sha256(ROOT / name)) for name in context.reports]))
        context.run(['git', 'add', '--', *context.reports, context.closure], cwd=ROOT, check=True)
        paths = [*context.reports, context.extra, additional.extra, context.closure]
        context.run(['git', 'commit', '--only', '-m', f'Verify cohort {options.cohort} committed source and oracle closure',
                     '--', *paths], cwd=ROOT, check=True)
        additional.complete()
        sys.path.insert(0, str(ROOT / 'work/goal-resume-20261106'))
        from cohort_sealing_guard import verify_committed_closure
        verification = verify_committed_closure(ROOT, 'HEAD', context.closure)
        if verification['reportsVerified'] != 4:
            raise ValueError('Every explicit namespace qualification must be committed')
        state.update(status='packaged', finalCommit=git('rev-parse', 'HEAD').decode().strip(),
                     committedClosureVerification=verification, acceptedFunctions=plan['sourceMatchedFunctions'],
                     acceptedInitializedBytes=plan['sourceLinkedBytes'])
    except BaseException as error:
        state.update(status='failed', errorType=type(error).__name__, error=str(error))
        raise
    finally:
        original_context.run_command = previous_command
        index_after = git('ls-files', '--stage', '-z', '--', *protected)
        state['protectedIndexUnchanged'] = index_after == index_before
        state['protectedWorkingBytesUnchanged'] = all(sha256(ROOT / name) == digest for name, digest in working_before.items())
        write_json(output / 'state.json', state)
        if not state['protectedIndexUnchanged'] or not state['protectedWorkingBytesUnchanged']:
            raise ValueError('Continuation changed unrelated staged or working bytes')
    print(json.dumps(state))


if __name__ == '__main__':
    main()
