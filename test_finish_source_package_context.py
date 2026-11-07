import copy
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest import mock
import finish_source_package_context as subject


class ContextControls(unittest.TestCase):
    def setUp(self):
        self.events = []
        self.module = SimpleNamespace(
            run=lambda command, log: self.events.append(('audit', command, log)),
            write_json=lambda path, value: self.events.append(('write', path, value)),
            subprocess=subprocess)
        self.context = subject.Context(self.module, 174)
        self.digest = '1' * 64
        self.value = dict(cohort=174, passed=True, sourceCredit=0, fullCleanReplayProven=False,
                          sourceCommit='2' * 40,
                          reports=[dict(path=p, sha256=self.digest) for p in self.context.reports])
        self.proof = dict(passed=True, sourceCredit=0,
                          allOriginalContextV9AndUnderlyingCommittedGlobalAuditsCompleted=True,
                          sourceRegistryAndFrozen174MembershipUnchanged=True)
        self.audit_command = [sys.executable, str(subject.ROOT / 'verify_committed_source_inputs_context_v9_20261106.py'),
                              '--cohort', '174']
        self.add_command = ['git', 'add', '--', *self.context.reports, self.context.closure]

    def write(self):
        with mock.patch.object(subject, 'read_json', return_value=self.proof), \
                mock.patch.object(subject, 'sha256', return_value=self.digest):
            self.context.write(subject.ROOT / self.context.closure, self.value)

    def test_only_qualified_cohort_and_exact_audit_are_adapted(self):
        with self.assertRaises(ValueError):
            subject.Context(self.module, 175)
        other = [sys.executable, 'some-other-check.py']
        self.context.audit(other, 'other.log')
        self.assertEqual(self.events[0][1], other)
        self.assertFalse(self.context.audit_complete)
        self.context.audit(self.audit_command, 'audit.log')
        self.assertEqual(self.events[1][1][1], str(subject.ROOT / 'verify_committed_source_inputs_context_v10_20261106.py'))
        with self.assertRaises(ValueError):
            self.context.audit(self.audit_command, 'again.log')

    def test_failed_actual_audit_cannot_enable_closure(self):
        self.context.previous_run = mock.Mock(side_effect=RuntimeError('audit failed'))
        with self.assertRaises(RuntimeError):
            self.context.audit(self.audit_command, 'audit.log')
        with self.assertRaises(ValueError):
            self.write()
        self.assertFalse(self.context.audit_complete)

    def test_failed_missing_or_credit_bearing_context_proof_rejected(self):
        self.context.audit(self.audit_command, 'audit.log')
        original = copy.deepcopy(self.proof)
        for key in ['passed', 'allOriginalContextV9AndUnderlyingCommittedGlobalAuditsCompleted',
                    'sourceRegistryAndFrozen174MembershipUnchanged']:
            self.proof = dict(original, **{key: False})
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.write()
        self.proof = dict(original, sourceCredit=1)
        with self.assertRaises(ValueError):
            self.write()
        self.assertFalse(self.context.closure_written)

    def test_original_report_removal_reordering_and_changed_bytes_rejected(self):
        self.context.audit(self.audit_command, 'audit.log')
        original = copy.deepcopy(self.value)
        for reports in [[], list(reversed(original['reports'])),
                        [dict(original['reports'][0], sha256='0' * 64), original['reports'][1]]]:
            self.value = dict(original, reports=reports)
            with self.subTest(reports=reports), self.assertRaises(ValueError):
                self.write()
        self.assertFalse(self.context.closure_written)

    def test_namespace_component_is_additive_and_staged_before_complete(self):
        before = copy.deepcopy(self.value)
        self.context.audit(self.audit_command, 'audit.log')
        self.write()
        self.assertEqual(self.value, before)
        written = self.events[-1][2]
        self.assertEqual(written['reports'][:2], before['reports'])
        self.assertEqual(written['reports'][2], dict(path=self.context.extra, sha256=self.digest))
        with self.assertRaises(ValueError):
            self.context.complete()
        original_run = subprocess.run
        with mock.patch.object(subject, 'run_command', return_value=SimpleNamespace(returncode=0)) as run:
            self.context.run(self.add_command, cwd=subject.ROOT, check=True)
            self.assertEqual(run.call_args.args[0], ['git', 'add', '--', *self.context.reports,
                                                   self.context.extra, self.context.closure])
            with self.assertRaises(ValueError):
                self.context.run(self.add_command, cwd=subject.ROOT, check=True)
        self.context.complete()
        self.assertIs(subprocess.run, original_run)

    def test_early_staging_and_duplicate_closure_are_rejected(self):
        with self.assertRaises(ValueError):
            self.context.run(self.add_command)
        self.context.audit(self.audit_command, 'audit.log')
        self.write()
        with self.assertRaises(ValueError):
            self.write()


if __name__ == '__main__':
    unittest.main()
