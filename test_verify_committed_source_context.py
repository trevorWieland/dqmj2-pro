from types import SimpleNamespace
import unittest
from unittest import mock
import verify_committed_source_context as subject


class ScopedProjectionControls(unittest.TestCase):
    def setUp(self):
        self.proof = dict(freshObject='work/fresh-child.o', freshObjectSha256='1' * 64)
        self.inputs = [dict(report='canonical-child', sourceHashes={'archive': 'a', 'module': 'b', 'source': 'c'})]
        self.removed = [dict(path='archive', sha256='a'), dict(path='module', sha256='b')]
        self.projected = [dict(report='canonical-child', sourceHashes={'source': 'c'})]
        self.events = []
        self.live = SimpleNamespace(proof=self.proof)
        self.qualification = SimpleNamespace(
            load_contract=lambda expected: {'derivedEvidence': self.removed},
            qualify=lambda expected: self.live,
            comparison_projection=self.project,
            verify_pins=lambda contract: self.events.append('scope-rechecked'))
        self.prior = mock.Mock(return_value=('inherited-result', 'inherited-proof'))
        for name, value in [('promotion', lambda: {'pinned': True}),
                            ('qualification_module', lambda: self.qualification),
                            ('sha256', lambda path: self.proof['freshObjectSha256'])]:
            patcher = mock.patch.object(subject, name, side_effect=value)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = mock.patch.object(subject.overlay, 'project_batches', self.prior)
        patcher.start()
        self.addCleanup(patcher.stop)

    def project(self, actual, contract, capability):
        self.assertIs(capability, self.live)
        self.assertIs(actual, self.inputs)
        self.events.append('live-projection')
        return self.projected, self.removed

    def test_exact_live_projection_delegates_and_restores_inherited_callback(self):
        with subject.validation_route() as proof:
            result = subject.overlay.project_batches(self.inputs, 'report', 'declaration')
            self.assertEqual(result, ('inherited-result', 'inherited-proof'))
        self.prior.assert_called_once_with(self.projected, 'report', 'declaration')
        self.assertIs(subject.overlay.project_batches, self.prior)
        self.assertEqual(proof['comparisonProjectionInvocations'], [self.removed])
        self.assertEqual(self.events, ['live-projection', 'scope-rechecked'])

    def test_inherited_failure_is_preserved_and_callback_restored(self):
        self.prior.side_effect = RuntimeError('original projector rejected')
        with self.assertRaisesRegex(RuntimeError, 'original projector rejected'):
            with subject.validation_route() as proof:
                subject.overlay.project_batches(self.inputs, 'report', 'declaration')
        self.assertIs(subject.overlay.project_batches, self.prior)
        self.assertEqual(proof['comparisonProjectionInvocations'], [])
        self.assertIn('scope-rechecked', self.events)

    def test_changed_live_object_rejects_scope_exit(self):
        with mock.patch.object(subject, 'sha256', return_value='2' * 64):
            with self.assertRaisesRegex(ValueError, 'Live child compilation changed'):
                with subject.validation_route():
                    pass
        self.assertIs(subject.overlay.project_batches, self.prior)

    def test_changed_promotion_rejects_scope_exit(self):
        with mock.patch.object(subject, 'promotion', side_effect=[{'pinned': True}, {'pinned': False}]):
            with self.assertRaisesRegex(ValueError, 'exact inherited callback/promotion'):
                with subject.validation_route():
                    pass
        self.assertIs(subject.overlay.project_batches, self.prior)


if __name__ == '__main__':
    unittest.main()
