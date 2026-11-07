import copy
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest import mock
import finish_source_package_context as inherited
import finish_committed_source_package as subject


class ContinuationControls(unittest.TestCase):
    def setUp(self):
        self.events = []
        self.document = None
        self.digest = '1' * 64
        self.hashes = {}
        self.source_commit = '2' * 40
        module = SimpleNamespace(run=lambda command, log: self.events.append(('audit', command, log)),
                                 write_json=self.capture, subprocess=subprocess)
        self.context = inherited.Context(module, 174)
        self.additional = subject.AdditionalQualification(self.context, self.source_commit,
            run=lambda command, *args, **kwargs: self.events.append(('command', command)))
        self.context.previous_run = self.additional.audit
        self.context.previous_write = self.additional.write
        self.overlay = dict(passed=True, sourceCredit=0,
            allOriginalContextV9AndUnderlyingCommittedGlobalAuditsCompleted=True,
            sourceRegistryAndFrozen174MembershipUnchanged=True)
        self.child = dict(passed=True, sourceCredit=0, allOriginalContextV10AuditsCompleted=True,
                          canonicalSourceRegistryUnchanged=True, frozenCohortMembershipUnchanged=True)
        self.value = dict(cohort=174, sourceCommit=self.source_commit, passed=True, sourceCredit=0,
            fullCleanReplayProven=False, reports=[dict(path=p, sha256=self.digest) for p in self.context.reports])
        for module in [inherited, subject]:
            for name, replacement in [('read_json', self.read), ('sha256', self.hash)]:
                patcher = mock.patch.object(module, name, side_effect=replacement)
                patcher.start()
                self.addCleanup(patcher.stop)
        patcher = mock.patch.object(inherited, 'run_command', side_effect=self.additional.run)
        patcher.start()
        self.addCleanup(patcher.stop)

    def capture(self, path, value):
        self.document = copy.deepcopy(value)
        self.events.append(('write', path, value))

    def read(self, path):
        if path == subject.ROOT / self.context.extra:
            return self.overlay
        if path == subject.ROOT / self.additional.extra:
            return self.child
        if path == subject.ROOT / self.context.closure:
            return self.document
        raise AssertionError(path)

    def hash(self, path):
        return self.hashes.get(str(path), self.digest)

    def audit(self):
        self.context.audit([sys.executable,
            str(subject.ROOT / 'verify_committed_source_inputs_context_v9_20261106.py'),
            '--cohort', '174'], 'fresh-resume.log')

    def write(self):
        self.context.write(subject.ROOT / self.context.closure, self.value)

    def stage(self):
        self.context.run(['git', 'add', '--', *self.context.reports, self.context.closure])

    def commit(self):
        self.context.run(['git', 'commit', '--only', '-m',
            'Verify cohort 174 committed source and oracle closure', '--',
            *self.context.reports, self.context.extra, self.additional.extra, self.context.closure])

    def test_success_preserves_three_components_and_adds_exact_fourth(self):
        original = copy.deepcopy(self.value)
        original_subprocess = subprocess.run
        self.audit()
        self.assertEqual(self.events[-1][1][1], str(subject.ROOT / subject.AUDIT))
        self.write()
        self.assertEqual(self.value, original)
        self.assertEqual([r['path'] for r in self.document['reports']],
                         [*self.context.reports, self.context.extra, self.additional.extra])
        self.stage()
        self.commit()
        self.additional.complete()
        self.assertIs(subprocess.run, original_subprocess)
        with self.assertRaises(ValueError):
            self.stage()
        with self.assertRaises(ValueError):
            self.audit()

    def test_failed_actual_audit_never_enables_closure(self):
        self.additional.original_run = mock.Mock(side_effect=RuntimeError('failed actual audit'))
        with self.assertRaises(RuntimeError):
            self.audit()
        with self.assertRaises(ValueError):
            self.write()
        with self.assertRaises(ValueError):
            self.stage()
        self.assertFalse(self.context.audit_complete)
        self.assertFalse(self.additional.audit_done)

    def test_each_failed_or_missing_child_scope_flag_is_rejected(self):
        self.audit()
        original = dict(self.child)
        for key in ['passed', 'allOriginalContextV10AuditsCompleted',
                    'canonicalSourceRegistryUnchanged', 'frozenCohortMembershipUnchanged']:
            for missing in [False, True]:
                self.child = dict(original)
                if missing:
                    del self.child[key]
                else:
                    self.child[key] = False
                with self.subTest(key=key, missing=missing), self.assertRaises(ValueError):
                    self.write()
        self.child = dict(original, sourceCredit=1)
        with self.assertRaises(ValueError):
            self.write()
        self.assertFalse(self.context.closure_written)

    def test_source_commit_and_inherited_report_identity_cannot_change(self):
        self.audit()
        self.value['sourceCommit'] = '3' * 40
        with self.assertRaises(ValueError):
            self.write()
        self.value['sourceCommit'] = self.source_commit
        self.value['reports'].reverse()
        with self.assertRaises(ValueError):
            self.write()

    def test_changed_child_proof_cannot_be_staged(self):
        self.audit()
        self.write()
        self.hashes[str(subject.ROOT / self.additional.extra)] = '4' * 64
        with self.assertRaises(ValueError):
            self.stage()
        self.assertFalse(self.additional.staged)

    def test_changed_closure_bytes_cannot_be_staged(self):
        self.audit()
        self.write()
        self.hashes[str(subject.ROOT / self.context.closure)] = '5' * 64
        with self.assertRaises(ValueError):
            self.stage()

    def test_changed_inherited_component_after_staging_cannot_commit(self):
        self.audit()
        self.write()
        self.stage()
        self.hashes[str(subject.ROOT / self.context.reports[0])] = '6' * 64
        with self.assertRaises(ValueError):
            self.commit()

    def test_early_or_nonisolated_commits_are_rejected(self):
        with self.assertRaises(ValueError):
            self.commit()
        self.audit()
        self.write()
        self.stage()
        with self.assertRaises(ValueError):
            self.context.run(['git', 'commit', '-m', 'include unrelated staged work'])


if __name__ == '__main__':
    unittest.main()
