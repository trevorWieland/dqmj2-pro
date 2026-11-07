import unittest
from native_build import APPROVED_CHECKPOINTS, approved_checkpoint
from bytematch_project import DENOMINATOR


class CheckpointGuardTests(unittest.TestCase):
    def manifest(self, record):
        return dict(revision=record[1], acceptedFunctions=record[2], acceptedInitializedBytes=record[3],
                    initializedDenominatorBytes=DENOMINATOR,
                    romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6')

    def test_both_closed_checkpoints_are_approved(self):
        for sha, record in APPROVED_CHECKPOINTS.items():
            with self.subTest(cohort=record[0]):
                self.assertEqual(approved_checkpoint(self.manifest(record), sha), record[0])

    def test_same_count_with_unknown_manifest_hash_is_rejected(self):
        record = next(iter(APPROVED_CHECKPOINTS.values()))
        with self.assertRaises(ValueError):
            approved_checkpoint(self.manifest(record), '0' * 64)

    def test_changed_snapshot_counts_or_input_are_rejected(self):
        sha, record = list(APPROVED_CHECKPOINTS.items())[-1]
        for key, value in [('revision', '0' * 40), ('acceptedFunctions', 11482),
                           ('acceptedInitializedBytes', 1236781), ('initializedDenominatorBytes', DENOMINATOR + 1),
                           ('romSha256', '0' * 64)]:
            with self.subTest(field=key):
                manifest = self.manifest(record)
                manifest[key] = value
                with self.assertRaises(ValueError):
                    approved_checkpoint(manifest, sha)


if __name__ == '__main__':
    unittest.main()
