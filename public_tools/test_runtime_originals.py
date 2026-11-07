import copy
import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from runtime_originals import digest, materialize, safe_binary


class RuntimeOriginalsTests(unittest.TestCase):
    def setUp(self):
        workspace = Path(__file__).resolve().parents[1] / 'work/runtime-originals-tests'
        workspace.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=workspace)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.image = bytes(range(12))
        self.write('extract/arm7/arm7.bin', self.image)
        self.write('extract/files/dwc/utility.bin', b'owned utility archive')
        self.write('arm7_runtime.py', b'original frozen ARM7 source')
        self.write('utility_runtime.py', b'original frozen utility source')
        self.arm7 = dict(modules=[], imageSha256=hashlib.sha256(self.image).hexdigest(), imageBytes=len(self.image))
        self.utility = dict(modules=[], runtimeMappingCanonical=True,
            inputSha256=digest(self.root / 'extract/files/dwc/utility.bin'), inputBytes=21)
        self.utility_files, self.inventory = {}, []
        for index in range(9):
            family = 'arm7' if index < 3 else 'utility'
            name = f'extract/{family}/runtime/module-{index}.bin'
            content = self.image[index * 4:index * 4 + 4] if index < 3 else bytes([index]) * 4
            module = dict(name=f'module-{index}', binary=name, bytes=4, sha256=hashlib.sha256(content).hexdigest())
            self.inventory.append(module)
            if index < 3:
                self.arm7['modules'].append(dict(module, inputFileOffset=index * 4, inputBytes=4))
            else:
                self.utility['modules'].append(module)
                self.utility_files[self.root / name] = bytearray(content) if index == 8 else content
        self.utility_files[self.root / 'extract/utility/child.srl'] = b'owned child program'
        self.host = []
        for index in range(11):
            name = f'extract/arm9/module-{index}.bin'
            content = bytes([index]) * 4
            self.write(name, content)
            self.host.append(dict(name=f'host-{index}', binary=name, bytes=4, sha256=hashlib.sha256(content).hexdigest()))
        self.rom = b'owned ROM'
        self.write('inputs/game.nds', self.rom)
        self.write('tools/dsd.exe', b'pinned DSD tool')
        self.write('project.json', json.dumps(dict(rom='inputs/game.nds', dsd='tools/dsd.exe',
            romSha256=hashlib.sha256(self.rom).hexdigest())).encode())
        self.dsd = patch('runtime_originals.DSD_SHA256', digest(self.root / 'tools/dsd.exe'))
        self.dsd.start()
        self.addCleanup(self.dsd.stop)
        self.write('evidence/arm7/runtime-layout.json', json.dumps(self.arm7).encode())
        self.write('evidence/utility/runtime-layout.json', json.dumps(self.utility).encode())
        self.write('ledger/modules.json', json.dumps(dict(buildSha256=hashlib.sha256(self.rom).hexdigest(),
            modules=self.inventory + self.host)).encode())
        modules = (SimpleNamespace(derive=lambda image: copy.deepcopy(self.arm7)),
                   SimpleNamespace(derive=lambda: (copy.deepcopy(self.utility), dict(self.utility_files))))
        self.loader = patch('runtime_originals.load_modules', return_value=modules)
        self.loader.start()
        self.addCleanup(self.loader.stop)
        self.layouts = {path: digest(path) for path in self.root.glob('evidence/*/runtime-layout.json')}

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def test_missing_runtime_originals_are_materialized_without_rewriting_layouts(self):
        result = materialize(self.root)
        self.assertEqual(result['createdOriginalFiles'], 10)
        self.assertEqual(result['derivedRuntimeModules'], 9)
        self.assertEqual(result['verifiedNativeModules'], 20)
        self.assertEqual(result['sourceCredit'], 0)
        for row in self.inventory:
            self.assertEqual(digest(self.root / row['binary']), row['sha256'])
        self.assertEqual({path: digest(path) for path in self.layouts}, self.layouts)

    def test_identical_existing_files_are_reused_without_writes(self):
        materialize(self.root)
        original = self.root / self.inventory[0]['binary']
        timestamp = original.stat().st_mtime_ns
        result = materialize(self.root)
        self.assertEqual(result['createdOriginalFiles'], 0)
        self.assertEqual(result['reusedOriginalFiles'], 10)
        self.assertEqual(original.stat().st_mtime_ns, timestamp)

    def test_conflicting_original_fails_before_creating_any_new_runtime_file(self):
        conflict = self.inventory[-1]['binary']
        self.write(conflict, b'bad!')
        with self.assertRaisesRegex(ValueError, 'Existing original runtime file differs'):
            materialize(self.root)
        self.assertEqual((self.root / conflict).read_bytes(), b'bad!')
        self.assertFalse((self.root / self.inventory[0]['binary']).exists())

    def test_derived_layout_must_match_the_frozen_metadata(self):
        self.utility['runtimeMappingCanonical'] = False
        with self.assertRaisesRegex(ValueError, 'frozen proof'):
            materialize(self.root)

    def test_real_module_bytes_must_match_the_frozen_ledger(self):
        self.utility_files[self.root / self.inventory[-1]['binary']] = b'bad!'
        with self.assertRaisesRegex(ValueError, 'measured identity'):
            materialize(self.root)

    def test_omitting_a_measured_runtime_module_fails(self):
        del self.utility_files[self.root / self.inventory[-1]['binary']]
        with self.assertRaisesRegex(ValueError, 'omitted measured'):
            materialize(self.root)

    def test_returned_original_cannot_escape_extract_or_supply_source(self):
        for name in ('../outside.bin', 'extract/../outside.bin', 'src/secret.c', 'extract/fake.c'):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'repository-local binary'):
                safe_binary(self.root, name)

    def test_absolute_path_outside_checkout_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'escapes its checkout'):
            safe_binary(self.root, self.root.parent / 'outside.bin')

    def test_output_directory_symlink_is_rejected(self):
        outside = self.root / 'external-binaries'
        outside.mkdir()
        link = self.root / 'extract/utility/runtime'
        link.parent.mkdir(parents=True, exist_ok=True)
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest(str(error))
        try:
            with self.assertRaisesRegex(ValueError, 'symlink or junction'):
                materialize(self.root)
        finally:
            link.unlink()

    @unittest.skipUnless(os.name == 'nt', 'Windows junction test')
    def test_output_directory_junction_is_rejected(self):
        outside = self.root / 'external-binaries'
        outside.mkdir()
        link = self.root / 'extract/utility/runtime'
        link.parent.mkdir(parents=True, exist_ok=True)
        process = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(outside)], capture_output=True)
        if process.returncode:
            self.skipTest('Cannot create a junction')
        try:
            with self.assertRaisesRegex(ValueError, 'symlink or junction'):
                materialize(self.root)
        finally:
            os.rmdir(link)

    def test_output_file_symlink_is_rejected_even_for_identical_bytes(self):
        target = self.root / 'external.bin'
        target.write_bytes(self.image[:4])
        link = self.root / self.inventory[0]['binary']
        link.parent.mkdir(parents=True, exist_ok=True)
        try:
            link.symlink_to(target)
        except OSError as error:
            self.skipTest(str(error))
        try:
            with self.assertRaisesRegex(ValueError, 'symlink or junction'):
                materialize(self.root)
        finally:
            link.unlink()

    def runner(self, command, **options):
        output = Path(command[command.index('--output-path') + 1])
        for row in self.host:
            path = output / Path(row['binary']).relative_to('extract')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(bytes([int(row['name'].split('-')[1])]) * 4)
        for name, content in [('arm7/arm7.bin', self.image), ('files/dwc/utility.bin', b'owned utility archive')]:
            path = output / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        (output / 'config.yaml').write_text('disposable generated DSD configuration')
        return SimpleNamespace(returncode=0, stdout=b'tool log', stderr=b'')

    def test_missing_host_originals_are_staged_without_overwriting_config(self):
        missing = self.root / self.host[0]['binary']
        missing.unlink()
        self.write('extract/config.yaml', b'frozen public config')
        result = materialize(self.root, runner=self.runner)
        self.assertEqual(result['stagedDsdOriginalFiles'], 1)
        self.assertEqual(digest(missing), self.host[0]['sha256'])
        self.assertEqual((self.root / 'extract/config.yaml').read_bytes(), b'frozen public config')
        stages = list((self.root / 'work').glob('runtime-originals-dsd-*'))
        self.assertEqual(len(stages), 1)
        self.assertTrue((stages[0] / 'extraction-receipt.json').is_file())
        self.assertTrue((stages[0] / 'dsd-extract.log').is_file())
        self.assertFalse((stages[0] / 'extract').exists())

    def test_missing_physical_parent_is_derived_before_runtime_modules(self):
        parent = self.root / 'extract/arm7/arm7.bin'
        parent.unlink()
        result = materialize(self.root, runner=self.runner)
        self.assertEqual(result['stagedDsdOriginalFiles'], 1)
        self.assertEqual(parent.read_bytes(), self.image)
        self.assertEqual(result['verifiedNativeModules'], 20)

    def test_staged_original_hash_mismatch_is_rejected_before_installing(self):
        missing = self.root / self.host[0]['binary']
        missing.unlink()
        def corrupt(command, **options):
            result = self.runner(command, **options)
            output = Path(command[command.index('--output-path') + 1])
            (output / Path(self.host[0]['binary']).relative_to('extract')).write_bytes(b'bad!')
            return result
        with self.assertRaisesRegex(ValueError, 'Staged original image differs'):
            materialize(self.root, runner=corrupt)
        self.assertFalse(missing.exists())

    def test_wrong_rom_is_rejected_before_dsd_execution(self):
        (self.root / self.host[0]['binary']).unlink()
        self.write('inputs/game.nds', b'wrong ROM')
        with self.assertRaisesRegex(ValueError, 'Pinned original ROM'):
            materialize(self.root, runner=lambda *args, **kwargs: self.fail('DSD must not run'))


if __name__ == '__main__':
    unittest.main()
