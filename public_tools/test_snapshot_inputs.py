import hashlib
import json
import unittest
from build_bytematch import BundleError, install_bundle
import test_private_inputs as fixtures


class SnapshotInputTests(unittest.TestCase):
    setUp = fixtures.PrivateInputTests.setUp
    pack = fixtures.PrivateInputTests.pack

    def snapshot(self, name, body, previous=None):
        sha = hashlib.sha256(body).hexdigest()
        directory = self.bundle / 'snapshot-files'
        directory.mkdir(exist_ok=True)
        (directory / sha).write_bytes(body)
        path = self.bundle / 'manifest.json'
        manifest = json.loads(path.read_text())
        entry = dict(path=name, sha256=sha, bytes=len(body))
        if previous is not None:
            entry['replacesSha256'] = hashlib.sha256(previous).hexdigest()
        manifest.setdefault('snapshotFiles', []).append(entry)
        path.write_text(json.dumps(manifest), encoding='utf-8')
        return sha

    def rejected(self):
        with self.assertRaises(BundleError):
            install_bundle(self.root, self.bundle)
        self.assertFalse((self.root / 'inputs/game.nds').exists())

    def test_metadata_transition_and_new_descriptor_reuse_original_archive(self):
        self.pack([('inputs/game.nds', b'original'), ('recovery.json', b'old')])
        part = self.bundle / 'inputs.tar.gz.part0'
        archive = part.read_bytes()
        self.snapshot('recovery.json', b'new', previous=b'old')
        self.snapshot('src/new/unit.json', b'new descriptor')
        result = install_bundle(self.root, self.bundle)
        self.assertEqual(result['installedFiles'], 3)
        self.assertEqual(result['snapshotFiles'], 2)
        self.assertEqual((self.root / 'recovery.json').read_bytes(), b'new')
        self.assertEqual((self.root / 'inputs/game.nds').read_bytes(), b'original')
        self.assertEqual(part.read_bytes(), archive)
        reused = install_bundle(self.root, self.bundle)
        self.assertEqual(reused['installedFiles'], 0)
        self.assertEqual(reused['identicalExistingFiles'], 3)

    def test_wrong_predecessor_rejected_before_installation(self):
        self.pack([('inputs/game.nds', b'original'), ('recovery.json', b'old')])
        self.snapshot('recovery.json', b'new', previous=b'wrong')
        self.rejected()

    def test_rom_cannot_be_replaced_even_with_matching_predecessor(self):
        self.pack([('inputs/game.nds', b'original')])
        self.snapshot('inputs/game.nds', b'changed', previous=b'original')
        self.rejected()

    def test_compiler_cannot_be_replaced(self):
        self.pack([('inputs/game.nds', b'original'), ('tools/compiler.exe', b'compiler')])
        self.snapshot('tools/compiler.exe', b'changed', previous=b'compiler')
        self.rejected()

    def test_public_source_cannot_be_added(self):
        self.pack([('inputs/game.nds', b'original')])
        self.snapshot('src/public.c', b'forbidden')
        self.rejected()

    def test_duplicate_snapshot_paths_rejected(self):
        self.pack([('inputs/game.nds', b'original')])
        self.snapshot('ledger/new.json', b'one')
        self.snapshot('ledger/new.json', b'two')
        self.rejected()

    def test_case_colliding_snapshot_paths_rejected(self):
        self.pack([('inputs/game.nds', b'original')])
        self.snapshot('ledger/new.json', b'one')
        self.snapshot('ledger/NEW.json', b'two')
        self.rejected()

    def test_case_colliding_base_member_rejected(self):
        self.pack([('inputs/game.nds', b'original'), ('ledger/new.json', b'one')])
        self.snapshot('ledger/NEW.json', b'two')
        self.rejected()

    def test_addition_cannot_silently_replace_archive_metadata(self):
        self.pack([('inputs/game.nds', b'original'), ('recovery.json', b'old')])
        self.snapshot('recovery.json', b'new')
        self.rejected()

    def test_replacement_requires_an_existing_base_member(self):
        self.pack([('inputs/game.nds', b'original')])
        self.snapshot('recovery.json', b'new', previous=b'absent')
        self.rejected()

    def test_changed_payload_rejected_before_any_installation(self):
        self.pack([('inputs/game.nds', b'original')])
        sha = self.snapshot('ledger/new.json', b'one')
        (self.bundle / 'snapshot-files' / sha).write_bytes(b'two')
        self.rejected()

    def test_existing_private_file_is_preserved_on_conflict(self):
        self.pack([('inputs/game.nds', b'original'), ('recovery.json', b'old')])
        self.snapshot('recovery.json', b'new', previous=b'old')
        (self.root / 'recovery.json').write_bytes(b'existing')
        self.rejected()
        self.assertEqual((self.root / 'recovery.json').read_bytes(), b'existing')

    def test_snapshot_traversal_is_rejected(self):
        self.pack([('inputs/game.nds', b'original')])
        self.snapshot('../outside.json', b'forbidden')
        self.rejected()

    def test_incomplete_snapshot_identity_is_rejected(self):
        self.pack([('inputs/game.nds', b'original')])
        self.snapshot('ledger/new.json', b'one')
        path = self.bundle / 'manifest.json'
        manifest = json.loads(path.read_text())
        manifest['snapshotFiles'][0]['bytes'] = True
        path.write_text(json.dumps(manifest), encoding='utf-8')
        self.rejected()


if __name__ == '__main__':
    unittest.main()
