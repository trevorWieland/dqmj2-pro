"""Tests for ops/ram_capture.py refusals and the --rehearse path."""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ram_capture

ROOT = Path(__file__).resolve().parent.parent


class RehearsalTest(unittest.TestCase):
    def setUp(self):
        self.manifest = ram_capture.load_manifest(ROOT)
        self.dump = Path(tempfile.mkdtemp(dir=ROOT / 'work'))
        self.spec = ram_capture.rehearsal_spec(self.manifest, f'work/{self.dump.name}/dump.bin')
        (self.dump / 'dump.bin').write_bytes(b'\0' * (1 << 20))

    def tearDown(self):
        shutil.rmtree(self.dump, ignore_errors=True)

    def test_missing_provenance_is_refused(self):
        broken = dict(self.spec)
        broken['provenance'] = dict(self.spec['provenance'])
        del broken['provenance']['tool']
        problems = ram_capture.validate_spec(ROOT, broken, self.manifest)
        self.assertTrue(any('tool' in problem for problem in problems))

    def test_capture_outside_module_is_refused(self):
        broken = dict(self.spec)
        broken['captures'] = [{'name': 'bad', 'address': '0x01000000', 'bytes': 16}]
        problems = ram_capture.validate_spec(ROOT, broken, self.manifest)
        self.assertTrue(any('outside' in problem for problem in problems))

    def test_rehearse_emits_a_module_entry(self):
        scratch = ROOT / 'work' / 'test-ram-rehearsal'
        shutil.rmtree(scratch, ignore_errors=True)
        code = ram_capture.main(['--rehearse', '--root', str(ROOT), '--scratch', str(scratch)])
        self.assertEqual(code, 0)
        fragment = json.loads((scratch / 'manifest-modules.json').read_text())
        self.assertEqual(len(fragment['modules']), 1)
        entry = fragment['modules'][0]
        self.assertEqual(entry['name'], 'ram-roster')
        self.assertEqual(entry['bytes'], 360)
        self.assertTrue((ROOT / entry['binary']).is_file())
        shutil.rmtree(scratch, ignore_errors=True)

    def test_manifest_destination_refused(self):
        with self.assertRaises(SystemExit):
            ram_capture.guard_manifest_destination(ROOT, ROOT / 'manifest.json')


if __name__ == '__main__':
    unittest.main()
