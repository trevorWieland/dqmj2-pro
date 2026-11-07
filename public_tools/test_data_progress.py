import copy
import json
import os
import shutil
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from build_receipts import DENOMINATOR, REPORTS, digest
from bytematch_project import elf_object
from data_progress import check_public_data_sources, load_data_spans


class DataProgressTests(unittest.TestCase):
    def setUp(self):
        workspace = Path(__file__).resolve().parents[1] / 'work/data-progress-tests'
        workspace.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=workspace)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.clock = time.time_ns()
        self.started = self.clock - 20_000_000_000
        self.native_started = self.clock - 10_000_000_000
        self.native_parent = self.root / 'work/native-unique'
        self.build_hash = 'a' * 64
        self.compiler_hash = 'b' * 64
        self.flags = ['-O2', '-proc', 'arm946e']
        self.manifest = self.root / 'public/accepted-functions.json'
        self.write(self.manifest, dict(romSha256=self.build_hash))
        self.rows, self.source_units, self.compiler_records = [], [], []
        for index, source in enumerate(('src/table.c', 'generated/assets/tile.c')):
            symbol = 'table' if index == 0 else 'tile'
            path = self.root / source
            path.parent.mkdir(parents=True)
            path.write_text(f'const int {symbol} = {7 + index * 2};\n', encoding='utf-8')
            obj = self.root / ('build/public-source-compile/table.o' if index == 0 else 'work/native-unique/fresh-auxiliary/tile/fresh.o')
            elf_object(obj, (7 + index * 2).to_bytes(4, 'little'), [(symbol, 0, 4, 'data')], False)
            stamp = self.clock - (15_000_000_000 if index == 0 else 9_000_000_000)
            os.utime(obj, ns=(stamp, stamp))
            row = dict(id=f'data-{index}', buildSha256=self.build_hash, kind='data', module='m00',
                       address=hex(0x02000000 + 4 * index), bytes=4, storedBytes=4,
                       source=source, sourceSha256=digest(path), sourceDependencies=[],
                       compilerSha256=self.compiler_hash, compilerFlags=self.flags,
                       states=dict(dataMatched=True, moduleLinked=True))
            self.rows.append(row)
            self.source_units.append(dict(module='m00', kind='data', start=row['address'], end=hex(int(row['address'], 0) + 4),
                source=source, sourceSha256=row['sourceSha256'], sourceDependencies=[], symbol=symbol,
                object=obj.relative_to(self.root).as_posix(), sha256=digest(obj), compiledBytes=4))
            self.compiler_records.append(dict(source=source, compilerSha256=self.compiler_hash,
                compilerFlags=self.flags, object=obj.relative_to(self.root).as_posix(), objectSha256=digest(obj),
                status='compiled' if index == 0 else 'freshly-compiled'))
        metadata = self.root / 'src/data/asset-model.json'
        self.write(metadata, dict(width=1))
        self.rows[1]['sourceDependencies'] = [dict(path=metadata.relative_to(self.root).as_posix(), sha256=digest(metadata))]
        self.data = dict(schemaVersion=1, buildSha256=self.build_hash, records=self.rows)
        self.compilation = self.root / 'build/public-source-compile/report.json'
        self.public_compilation = dict(status='source-compilation-passed', fullManifestCompiled=True,
            manifestSha256=digest(self.manifest), results=[self.compiler_records[0]])
        self.modules, self.linked_modules = [], []
        for index in range(20):
            size = 8 if index == 0 else DENOMINATOR - 8 - 18 if index == 19 else 1
            payload = bytes.fromhex('0700000009000000') if index == 0 else bytes(size)
            original = self.root / f'extract/m{index:02}.bin'
            output = self.native_parent / f'modules/m{index:02}.bin'
            for path in (original, output):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(payload)
                os.utime(path, ns=(self.clock - 8_000_000_000, self.clock - 8_000_000_000))
            module = dict(name=f'm{index:02}', bytes=size, base=hex(0x02000000 + index * 0x1000),
                          binary=original.relative_to(self.root).as_posix(), sha256=digest(original))
            self.modules.append(module)
            self.linked_modules.append(dict(module=module['name'], inputSha256=module['sha256'],
                outputSha256=module['sha256'], exactBytes=True, output=output.relative_to(self.root).as_posix()))
        self.write(self.root / 'ledger/modules.json', dict(buildSha256=self.build_hash, modules=self.modules))
        self.report_paths = {name: self.native_parent / 'evidence/linking' / name for name in REPORTS}
        self.reports = {}
        for name, begin, end in zip(REPORTS, (0, 11, 14), (11, 14, 20)):
            self.reports[name] = dict(buildNamespace=self.build_hash, allModuleBytesExact=True, symbolCheckPassed=True,
                modules=self.linked_modules[begin:end], sourceUnits=self.source_units if begin == 0 else [])
        self.native_path = self.native_parent / 'native-build-receipt.json'
        self.native = dict(nativeBuildPassed=True, allModuleBytesExact=True, allSymbolChecksPassed=True,
            acceptedManifestSha256=digest(self.manifest), startedTimeNs=self.native_started,
            freshCompilation=dict(results=[self.compiler_records[1]]))
        self.outer = dict(startedTimeNs=self.started)
        self.sync()

    def write(self, path, value, modified=None):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) + '\n', encoding='utf-8')
        if modified is not None:
            os.utime(path, ns=(modified, modified))

    def pin(self, path):
        return dict(path=path.relative_to(self.root).as_posix(), sha256=digest(path), modifiedTimeNs=path.stat().st_mtime_ns)

    def sync(self):
        self.write(self.root / 'public/accepted-data.json', self.data)
        self.write(self.compilation, self.public_compilation, self.clock - 15_000_000_000)
        self.outer['publicSourceCompileReport'] = self.pin(self.compilation)
        self.native['publicSourceCompileReport'] = copy.deepcopy(self.outer['publicSourceCompileReport'])
        pins = {}
        for name, path in self.report_paths.items():
            self.write(path, self.reports[name], self.clock - 7_000_000_000)
            pin = self.pin(path)
            pins[pin.pop('path')] = pin
        self.outer['reports'] = pins
        self.write(self.native_path, self.native, self.clock - 5_000_000_000)
        self.outer['nativeBuildReceipt'] = self.pin(self.native_path)
        self.verified = dict(buildScope='native-modules', nativeReceipt=self.native,
            receipt=self.outer, compilation=self.compilation, reports=self.report_paths)

    def load(self):
        with patch('data_progress.DATA_RECORDS', 2), patch('data_progress.DATA_BYTES', 8):
            return load_data_spans(self.root, self.root, self.verified)

    def test_public_and_private_actual_c_inputs_receive_only_data_spans(self):
        result = self.load()
        self.assertEqual(len(result['m00']), 2)
        self.assertEqual(sum(row['end'] - row['start'] for row in result['m00']), 8)
        self.assertEqual(result['m00'][1]['source'], 'generated/assets/tile.c')
        self.assertEqual(result['m00'][1]['symbol'], 'tile')
        self.assertTrue(all(set(row) <= {'start', 'end', 'source', 'sourceSha256', 'symbol'} for row in result['m00']))

    def test_legacy_and_diagnostic_modes_explicitly_receive_no_data_credit(self):
        for build in (None, {}, dict(buildScope='full-replay'), dict(buildScope='diagnostic')):
            self.assertEqual(load_data_spans(self.root, self.root, build), {})

    def test_closed_data_count_and_byte_denominator_are_not_silently_reduced(self):
        with self.assertRaisesRegex(ValueError, 'complete closed typed-data snapshot'):
            load_data_spans(self.root, self.root, self.verified)

    def test_unmatched_or_unlinked_data_is_rejected(self):
        for key in ('dataMatched', 'moduleLinked'):
            self.rows[0]['states'][key] = False
            self.sync()
            with self.assertRaisesRegex(ValueError, 'unqualified initialized source'):
                self.load()
            self.rows[0]['states'][key] = True

    def test_source_and_semantic_dependency_hashes_are_checked(self):
        source = self.root / self.rows[1]['source']
        source.write_text('const int tile = 100;\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'identity differs'):
            self.load()
        source.write_text('const int tile = 9;\n', encoding='utf-8')
        (self.root / 'src/data/asset-model.json').write_text('{}\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'identity differs'):
            self.load()

    def test_tampered_fresh_data_object_is_rejected(self):
        obj = self.root / self.compiler_records[1]['object']
        raw = bytearray(obj.read_bytes())
        raw[52] ^= 1
        obj.write_bytes(raw)
        with self.assertRaisesRegex(ValueError, 'identity differs'):
            self.load()

    def test_old_cached_object_cannot_masquerade_as_the_fresh_linker_input(self):
        cached = self.root / 'work/old-cache/tile.o'
        cached.parent.mkdir(parents=True)
        shutil.copy2(self.root / self.compiler_records[1]['object'], cached)
        self.source_units[1]['object'] = cached.relative_to(self.root).as_posix()
        self.sync()
        with self.assertRaisesRegex(ValueError, 'old or different compiler object'):
            self.load()

    def test_auxiliary_object_must_have_been_compiled_during_native_build(self):
        obj = self.root / self.compiler_records[1]['object']
        old = self.native_started - 1_000_000_000
        os.utime(obj, ns=(old, old))
        with self.assertRaisesRegex(ValueError, 'predates or escapes'):
            self.load()

    def test_failed_or_missing_compiler_provenance_prevents_data_credit(self):
        self.native['freshCompilation']['results'][0]['status'] = 'compile-failed'
        self.sync()
        with self.assertRaisesRegex(ValueError, 'compiler did not succeed'):
            self.load()
        self.native['freshCompilation']['results'] = []
        self.sync()
        with self.assertRaisesRegex(ValueError, 'lacks fresh compiler provenance'):
            self.load()

    def test_exact_canonical_linked_interval_is_required(self):
        self.source_units[1]['end'] = hex(int(self.source_units[1]['end'], 0) + 4)
        self.sync()
        with self.assertRaisesRegex(ValueError, 'exact canonical fresh linked source unit'):
            self.load()

    def test_native_module_bytes_must_still_match_original_hashes(self):
        output = self.root / self.linked_modules[0]['output']
        output.write_bytes(b'changed!')
        with self.assertRaisesRegex(ValueError, 'identity differs'):
            self.load()

    def test_data_symbol_cannot_be_a_fabricated_function(self):
        obj = self.root / self.compiler_records[1]['object']
        elf_object(obj, bytes.fromhex('09000000'), [('tile', 0, 4, 'arm')], True)
        self.compiler_records[1]['objectSha256'] = digest(obj)
        self.source_units[1]['sha256'] = digest(obj)
        self.sync()
        with self.assertRaisesRegex(ValueError, 'not the complete initialized object'):
            self.load()

    def test_a_public_generator_cannot_replace_the_actual_c_source_path(self):
        source = self.root / 'src/encoder.py'
        source.write_text('def encode(value):\n    return value\n', encoding='utf-8')
        self.rows[1]['source'] = self.source_units[1]['source'] = self.compiler_records[1]['source'] = 'src/encoder.py'
        self.rows[1]['sourceSha256'] = self.source_units[1]['sourceSha256'] = digest(source)
        self.sync()
        with self.assertRaisesRegex(ValueError, 'actual frozen C compiler input'):
            self.load()

    def test_bss_and_unqualified_alignment_do_not_gain_initialized_data_credit(self):
        self.data['records'] = self.rows + [dict(kind='bss', bytes=4096, storedBytes=4096)]
        self.sync()
        self.assertEqual(sum(row['end'] - row['start'] for row in self.load()['m00']), 8)


class PublicDataVisibilityTests(unittest.TestCase):
    def setUp(self):
        workspace = Path(__file__).resolve().parents[1] / 'work/data-progress-tests'
        workspace.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=workspace)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.write('src/table.c', '#include "table.h"\nconst unsigned int table = TABLE_VALUE;\n')
        self.write('src/table.h', '#define TABLE_VALUE 7\n')
        self.write('generated/math/table.c', 'const unsigned int cosine = 1;\n')
        self.write('derive_math.py', 'def derive():\n    return 1\n')
        self.rows = []
        for index, source in enumerate(('src/table.c', 'generated/math/table.c', 'generated/assets/tile.c')):
            self.rows.append(dict(id=str(index), module='main', address=hex(0x2000000 + index * 4),
                source=source, sourceSha256=digest(self.root / source) if index != 2 else 'a' * 64,
                kind='data', bytes=4, states=dict(dataMatched=True, moduleLinked=True), compilerFlags=[]))
        self.rows[0]['sourceDependencies'] = [dict(path='src/table.h', sha256=digest(self.root / 'src/table.h'))]
        self.data = dict(schemaVersion=1, buildSha256='f' * 64, records=self.rows)
        self.functions = dict(revision='b' * 40, romSha256='f' * 64,
            functions=[dict(module='main', processor='arm9', program=None)])
        self.visibility = dict(schemaVersion=1, snapshotRevision=self.functions['revision'], sources=[],
            generators=dict(math=[dict(path='derive_math.py', sha256=digest(self.root / 'derive_math.py'))]))
        for index, state in ((1, 'public'), (2, 'private-asset')):
            row = self.rows[index]
            self.visibility['sources'].append(dict(**{key: row[key] for key in ('id', 'module', 'address', 'source', 'sourceSha256')},
                processor='arm9', program='', sourceTextBytes=(self.root / row['source']).stat().st_size if index == 1 else 100,
                initializedBytes=4, visibility=state, classification='mathematical-table' if index == 1 else 'complete-encoded-game-asset',
                generatorFamily='math', cIncludeDependencies=[]))
        self.counts = patch('data_progress.GENERATED_VISIBILITY_COUNTS', {'public': 1, 'private-asset': 1})
        self.counts.start()
        self.addCleanup(self.counts.stop)
        self.sync()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def sync(self):
        self.write('public/accepted-data.json', json.dumps(self.data))
        self.write('public/accepted-functions.json', json.dumps(self.functions))
        self.visibility['acceptedDataManifestSha256'] = digest(self.root / 'public/accepted-data.json')
        self.write('public/data-source-visibility.json', json.dumps(self.visibility))

    def check(self):
        return check_public_data_sources(self.root)

    def test_rom_free_check_accepts_absent_private_assets_and_grants_no_credit(self):
        self.assertFalse((self.root / 'generated/assets/tile.c').exists())
        result = self.check()
        self.assertEqual(result['publicDataRecordsVerified'], 2)
        self.assertEqual(result['publicInitializedBytes'], 8)
        self.assertEqual(result['publicSemanticGeneratorsVerified'], 1)
        self.assertFalse(result['privateAssetSourcesRequired'])
        self.assertFalse(result['matchingCreditGranted'])

    def test_curated_public_c_bytes_must_match_the_frozen_source(self):
        self.write('generated/math/table.c', 'const unsigned int cosine = 2;\n')
        with self.assertRaisesRegex(ValueError, 'source hash differs'):
            self.check()

    def test_public_header_closure_is_required_even_without_private_assets(self):
        (self.root / 'src/table.h').unlink()
        with self.assertRaisesRegex(ValueError, 'missing or escapes'):
            self.check()

    def test_stale_visibility_manifest_hash_is_rejected(self):
        self.write('public/accepted-data.json', json.dumps(self.data) + '\n')
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.check()

    def test_wrong_snapshot_revision_is_rejected(self):
        self.visibility['snapshotRevision'] = 'c' * 40
        self.sync()
        with self.assertRaisesRegex(ValueError, 'wrong snapshot'):
            self.check()

    def test_wrong_child_cpu_or_program_cannot_default_to_host_arm9(self):
        self.visibility['sources'][1]['processor'] = 'arm7'
        self.sync()
        with self.assertRaisesRegex(ValueError, 'source identity'):
            self.check()

    def test_private_asset_visibility_cannot_be_omitted(self):
        self.visibility['sources'].pop()
        self.sync()
        with self.assertRaisesRegex(ValueError, 'inventory is incomplete'):
            self.check()

    def test_semantic_generator_is_checked_as_provenance_not_used_as_the_source(self):
        self.write('derive_math.py', 'def derive():\n    return 2\n')
        with self.assertRaisesRegex(ValueError, 'source hash differs'):
            self.check()

    def test_unqualified_data_does_not_pass_public_visibility_verification(self):
        self.rows[0]['states']['dataMatched'] = False
        self.sync()
        with self.assertRaisesRegex(ValueError, 'unqualified'):
            self.check()


if __name__ == '__main__':
    unittest.main()
