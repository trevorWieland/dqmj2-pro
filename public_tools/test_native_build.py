import copy
import json
import struct
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from bytematch_project import DENOMINATOR, digest, elf_object, write
from native_build import attributes, original_modules, rebuild, verify_results
from native_objects import FreshObjects, object_contract, safe_flags


class NativeBuildTests(unittest.TestCase):
    def setUp(self):
        container = Path(__file__).resolve().parent.parent / 'work/native-build-tests'
        container.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=container)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        (self.root / 'src').mkdir()
        (self.root / 'src/value.c').write_text('int value(void){return 7;}\n')
        (self.root / 'src/table.c').write_text('const int table = 7;\n')
        compiler = self.root / 'tools/compiler.exe'
        compiler.parent.mkdir()
        compiler.write_bytes(b'isolated fixture compiler')
        self.compiler_hash = digest(compiler)
        self.old = self.root / 'work/original/value.o'
        self.current = self.root / 'build/fresh/value.o'
        self.old_data = self.root / 'work/original/table.o'
        elf_object(self.old, bytes.fromhex('0700a0e3'), [('value', 0, 4, 'arm')])
        elf_object(self.current, bytes.fromhex('0700a0e3'), [('value', 0, 4, 'arm')])
        with self.current.open('ab') as stream:
            stream.write(b'new debug container identity')
        elf_object(self.old_data, bytes.fromhex('07000000'), [('table', 0, 4, 'data')], False)
        self.function = dict(id='accepted', buildSha256='a' * 64, processor='arm9', program=None, module='m00',
                             address='0x2000000', mode='arm', symbol='func_02000000', bytes=4,
                             sourceUnit='src/value.c', sourceSha256=digest(self.root / 'src/value.c'),
                             sourceDependencies=[], compilerSha256=self.compiler_hash, compilerFlags=['-O2', '-proc', 'arm946e'],
                             states=dict(functionMatched=True, moduleLinked=True))
        self.manifest = dict(schemaVersion=1, revision='closed', romSha256='a' * 64,
                             initializedDenominatorBytes=DENOMINATOR, functions=[self.function])
        write(self.root / 'public/accepted-functions.json', self.manifest)
        self.data = dict(module='m00', address='0x2000004', bytes=4, storedBytes=4, kind='data',
                         source='src/table.c', sourceSha256=digest(self.root / 'src/table.c'),
                         compilerSha256=self.compiler_hash, compilerFlags=['-O2', '-proc', 'arm946e', '-DSAVED_TABLE'])
        write(self.root / 'public/accepted-data.json', dict(records=[self.data]))
        self.compilation = self.root / 'build/compilation.json'
        write(self.compilation, dict(status='source-compilation-passed', fullManifestCompiled=True,
              manifestSha256=digest(self.root / 'public/accepted-functions.json'), results=[
                  dict(source='src/value.c', compilerSha256=self.compiler_hash, compilerFlags=self.function['compilerFlags'],
                       status='compiled', object=str(self.current), objectSha256=digest(self.current))]))
        self.unit = dict(module='m00', kind='function', function='value', start='0x2000000', end='0x2000004',
                         source='src/value.c', sourceSha256=self.function['sourceSha256'], sourceDependencies=[],
                         object=self.old.relative_to(self.root).as_posix(), sha256=digest(self.old))
        self.data_unit = dict(module='m00', kind='data', symbol='table', start='0x2000004', end='0x2000008',
                              source='src/table.c', sourceSha256=self.data['sourceSha256'], sourceDependencies=[],
                              object=self.old_data.relative_to(self.root).as_posix(), sha256=digest(self.old_data))
        self.calls = []
        def compile_fixture(command, **options):
            self.calls.append((command, options))
            output = Path(command[-1])
            output.write_bytes(self.old_data.read_bytes() + b'new data debug container')
            return SimpleNamespace(returncode=0, stdout=b'', stderr=b'')
        self.runner = compile_fixture

    def objects(self, runner=None):
        return FreshObjects(self.root, self.compilation, self.root / 'work/native/fresh', self.root / 'tools',
                            self.root / 'tools/license.dat', runner or self.runner)

    def test_fresh_function_replaces_cached_container_without_mutating_metadata(self):
        fresh = self.objects()
        before = copy.deepcopy(self.unit)
        result = fresh.unit(self.unit)
        self.assertEqual(self.unit, before)
        self.assertEqual(result['object'], self.current.relative_to(self.root).as_posix())
        self.assertEqual(result['sha256'], digest(self.current))
        self.assertNotEqual(result['sha256'], before['sha256'])
        self.assertEqual(result['originalObjectSha256'], before['sha256'])
        self.assertTrue(result['freshCompilationVerified'])
        self.assertFalse(self.calls)

    def test_auxiliary_data_is_actually_compiled_with_pinned_flags(self):
        fresh = self.objects()
        result = fresh.unit(self.data_unit)
        self.assertEqual(len(self.calls), 1)
        command, options = self.calls[0]
        self.assertIn('-DSAVED_TABLE', command)
        self.assertIn('-c', command)
        self.assertEqual(options['env']['LM_LICENSE_FILE'], str(self.root / 'tools/license.dat'))
        self.assertTrue((self.root / result['object']).is_relative_to(self.root / 'work'))
        self.assertEqual(object_contract(self.root / result['object']), object_contract(self.old_data))
        self.assertEqual(fresh.finish()['auxiliaryFreshCompilationUnits'], 1)

    def test_auxiliary_wrong_data_is_rejected_even_when_compiler_succeeds(self):
        def wrong(command, **options):
            raw = bytearray(self.old_data.read_bytes())
            raw[52] ^= 1
            Path(command[-1]).write_bytes(raw)
            return SimpleNamespace(returncode=0, stdout=b'', stderr=b'')
        with self.assertRaisesRegex(ValueError, 'Fresh allocated source sections'):
            self.objects(wrong).unit(self.data_unit)

    def test_fresh_compiler_artifacts_remain_hash_bound_until_finish(self):
        fresh = self.objects()
        fresh.unit(self.unit)
        with self.current.open('ab') as stream:
            stream.write(b'changed after source-object verification')
        with self.assertRaisesRegex(ValueError, 'Frozen inputs changed'):
            fresh.finish()

    def test_missing_closed_profile_cannot_gain_source_credit(self):
        unit = dict(self.unit, start='0x2000008', end='0x200000c')
        with self.assertRaisesRegex(ValueError, 'outside the closed function snapshot'):
            self.objects().unit(unit)

    def test_allocated_symbol_binding_changes_are_not_debug_only(self):
        raw = bytearray(self.current.read_bytes())
        section_table = struct.unpack_from('<I', raw, 32)[0]
        symtab = struct.unpack_from('<IIIIIIIIII', raw, section_table + 80)
        raw[symtab[4] + 32 + 12] = 0x22
        path = self.root / 'build/weak.o'
        path.write_bytes(raw)
        self.assertNotEqual(object_contract(path), object_contract(self.old))

    def test_frozen_veneer_remains_imported_with_zero_source_credit(self):
        item = dict(kind='linkage', ordinaryFunctionCredit=0, object=self.old.relative_to(self.root).as_posix(),
                    objectSha256=digest(self.old))
        result = self.objects().entry(item)
        self.assertTrue(result['importedFrozenLinkage'])
        self.assertNotIn('freshCompilationVerified', result)
        self.assertEqual(result['object'], item['object'])
        with self.assertRaisesRegex(ValueError, 'zero source function credit'):
            self.objects().entry(dict(item, ordinaryFunctionCredit=1))

    def test_macro_flags_preserve_order_and_private_include_paths_are_rejected(self):
        options = ['-O2', '-DSAVED_TABLE', '-proc', 'arm946e']
        self.assertEqual(safe_flags(self.root, options), options)
        with self.assertRaises(ValueError):
            safe_flags(self.root, ['-i', 'inputs'])

    def test_native_outputs_require_new_work_directory(self):
        with self.assertRaisesRegex(ValueError, 'new dedicated native build directory'):
            rebuild(self.root, self.compilation, self.root / 'build/native')
        output = self.root / 'work/existing'
        output.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, 'new dedicated native build directory'):
            rebuild(self.root, self.compilation, output)

    def test_runtime_attribute_redirects_are_restored_on_failure(self):
        target = SimpleNamespace(WORK='original', write_json='original-writer')
        with self.assertRaises(RuntimeError):
            with attributes(target, WORK='isolated', write_json='isolated-writer'):
                self.assertEqual(target.WORK, 'isolated')
                raise RuntimeError('fixture failure')
        self.assertEqual(target.WORK, 'original')
        self.assertEqual(target.write_json, 'original-writer')

    def test_ci_build_cannot_reuse_a_predating_source_compile_report(self):
        with self.assertRaisesRegex(ValueError, 'predates this CI build'):
            rebuild(self.root, self.compilation, self.root / 'work/too-old', compilation_not_before_ns=time.time_ns() + 1000000000)

    def scope_fixture(self):
        modules, outputs = [], []
        work = self.root / 'work/scope'
        for index in range(20):
            payload = bytes(DENOMINATOR - 19 * 8 if index == 0 else 8)
            original = self.root / f'extract/m{index:02}.bin'
            output = work / f'm{index:02}.bin'
            original.parent.mkdir(exist_ok=True)
            output.parent.mkdir(parents=True, exist_ok=True)
            original.write_bytes(payload)
            output.write_bytes(payload)
            module = dict(name=f'm{index:02}', program=None, processor='arm9', base='0x2000000',
                          bytes=len(payload), binary=original.relative_to(self.root).as_posix(), sha256=digest(original))
            modules.append(module)
            outputs.append(dict(module=module['name'], inputSha256=module['sha256'], output=str(output),
                                outputSha256=digest(output), exactBytes=True))
        write(self.root / 'ledger/modules.json', dict(buildSha256='a' * 64, modules=modules))
        reports = [dict(allModuleBytesExact=True, symbolCheckPassed=True, modules=outputs, sourceUnits=[self.unit])]
        return work, modules, reports

    def test_all_twenty_original_module_hashes_and_source_coverage_are_required(self):
        work, modules, reports = self.scope_fixture()
        self.assertEqual(len(original_modules(self.root, self.manifest)), 20)
        self.assertEqual(verify_results(self.root, work, modules, reports, self.manifest)['acceptedFunctionsLinked'], 1)
        reports[0]['sourceUnits'] = []
        with self.assertRaisesRegex(ValueError, 'omitted original modules or accepted source functions'):
            verify_results(self.root, work, modules, reports, self.manifest)

    def test_previous_link_output_outside_new_work_directory_is_rejected(self):
        work, modules, reports = self.scope_fixture()
        reports[0]['modules'][0]['output'] = str(self.current)
        with self.assertRaisesRegex(ValueError, 'freshly created beneath this work directory'):
            verify_results(self.root, work, modules, reports, self.manifest)


if __name__ == '__main__':
    unittest.main()
