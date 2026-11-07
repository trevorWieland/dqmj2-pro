import argparse
import copy
import importlib.util
import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, sha256


ORIGINAL = 'finish_source_package_v25_20261106.py'
PINS = {
    ORIGINAL: '34ff772e6f515c198baf5934b18edeafe2f597802fa15fab840be85904b9be75',
    'verify_committed_source_inputs_context_v10_20261106.py': 'de8ce1bb0e569aeb436bde3e0cb507ad3b7e0e5933818a943be16a42f99db1eb',
}
run_command = subprocess.run


def verify():
    for name, digest in PINS.items():
        if sha256(ROOT / name) != digest:
            raise ValueError('Pinned source finisher context changed: ' + name)


class Context:
    def __init__(self, module, cohort):
        if cohort != 174:
            raise ValueError('Only the qualified cohort174 context is supported')
        self.module = module
        self.cohort = cohort
        self.previous_run = module.run
        self.previous_write = module.write_json
        self.previous_process = module.subprocess
        self.reports = [f'evidence/verification/cohort{cohort}-committed-source-inputs-v14-20261105.json',
                        f'evidence/verification/cohort{cohort}-captured-oracle-closure-verification-20261031.json']
        self.extra = f'evidence/verification/cohort{cohort}-overlay-reference-context-v10-20261106.json'
        self.closure = f'evidence/verification/cohort{cohort}-expanded-source-closure-20261101.json'
        self.audit_complete = False
        self.closure_written = False
        self.extra_staged = False

    def __getattr__(self, name):
        return getattr(self.previous_process, name)

    def audit(self, command, log):
        expected = [sys.executable, str(ROOT / 'verify_committed_source_inputs_context_v9_20261106.py'),
                    '--cohort', str(self.cohort)]
        if command != expected:
            return self.previous_run(command, log)
        if self.audit_complete:
            raise ValueError('Duplicate committed-source context dispatch')
        actual = [sys.executable, str(ROOT / 'verify_committed_source_inputs_context_v10_20261106.py'),
                  '--cohort', str(self.cohort)]
        result = self.previous_run(actual, log)
        self.audit_complete = True
        return result

    def write(self, path, value):
        if Path(path) != ROOT / self.closure:
            return self.previous_write(path, value)
        if not self.audit_complete or self.closure_written:
            raise ValueError('Fresh committed-source audit is required exactly once')
        if (value.get('cohort'), value.get('passed'), value.get('sourceCredit'),
                value.get('fullCleanReplayProven')) != (self.cohort, True, 0, False):
            raise ValueError('Original closure scope or success predicates changed')
        if [row['path'] for row in value['reports']] != self.reports:
            raise ValueError('Original committed-source and captured-oracle components changed')
        if any(row['sha256'] != sha256(ROOT / row['path']) for row in value['reports']):
            raise ValueError('Original closure component bytes changed')
        proof = read_json(ROOT / self.extra)
        if proof.get('sourceCredit') != 0:
            raise ValueError('Namespace qualification cannot add source credit')
        if not all(proof.get(key) is True for key in ['passed',
                'allOriginalContextV9AndUnderlyingCommittedGlobalAuditsCompleted',
                'sourceRegistryAndFrozen174MembershipUnchanged']):
            raise ValueError('Namespaced overlay context did not complete its inherited audits')
        result = copy.deepcopy(value)
        result['reports'].append(dict(path=self.extra, sha256=sha256(ROOT / self.extra)))
        result['finisherContext'] = dict(originalFinisher=ORIGINAL, pinnedEntrypoints=PINS,
                                         underlyingFinisherGuardsUnchanged=True, sourceCredit=0)
        written = self.previous_write(path, result)
        self.closure_written = True
        return written

    def run(self, command, *args, **kwargs):
        expected = ['git', 'add', '--', *self.reports, self.closure]
        if command == expected:
            if not self.closure_written or self.extra_staged:
                raise ValueError('Explicit namespace closure component must be staged exactly once')
            command = ['git', 'add', '--', *self.reports, self.extra, self.closure]
            result = run_command(command, *args, **kwargs)
            self.extra_staged = True
            return result
        return run_command(command, *args, **kwargs)

    def complete(self):
        if not all([self.audit_complete, self.closure_written, self.extra_staged]):
            raise ValueError('Source finisher context did not complete every required action')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True, choices=[174])
    parser.add_argument('--stage', required=True)
    parser.add_argument('--document', required=True)
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    if (options.stage, options.document) != ('stage_parallel_packet_wave174_v2_20261106.py',
                                           'docs/2026-11-06-parallel-wave-s-acceptance.md'):
        raise ValueError('The qualified cohort174 stage/document route changed')
    verify()
    spec = importlib.util.spec_from_file_location('pinned_source_package_finisher', ROOT / ORIGINAL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    context = Context(module, options.cohort)
    module.run, module.write_json, module.subprocess = context.audit, context.write, context
    try:
        module.main()
        context.complete()
    finally:
        module.run, module.write_json, module.subprocess = context.previous_run, context.previous_write, context.previous_process
        verify()


if __name__ == '__main__':
    main()
