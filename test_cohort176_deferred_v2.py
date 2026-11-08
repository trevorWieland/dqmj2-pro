import ast
import builtins
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import symtable
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
if '--fixture-root' in sys.argv:
    index = sys.argv.index('--fixture-root')
    fixture = Path(sys.argv[index + 1]).resolve()
    actual = next(p for p in (HERE, *HERE.parents) if (p / 'recovery.json').is_file())
    if fixture != actual:
        raise ValueError('Canonical fixtureRoot must be this repository')
    HERE = fixture
    del sys.argv[index:index + 2]
sys.path.insert(0, str(HERE))
BASE = HERE.parent / 'successor-v1'
if BASE.is_dir():
    sys.path.insert(0, str(BASE))
import cohort176_legacy_live_v2 as live
import cohort176_epoch_v1 as core
ROOT = next(p for p in (HERE, *HERE.parents) if (p / 'recovery.json').is_file())
SANDBOX_PARENT = ROOT / 'work'


class ToolBoundary(RuntimeError):
    pass


def unresolved(path):
    table = symtable.symtable(Path(path).read_text(), str(path), 'exec')
    bound = {s.get_name() for s in table.get_symbols() if s.is_assigned() or s.is_imported() or s.is_namespace()}
    result = []
    def visit(node):
        for symbol in node.get_symbols():
            if symbol.is_global() and symbol.is_referenced() and symbol.get_name() not in bound and not hasattr(builtins, symbol.get_name()) and symbol.get_name() not in ('__file__', '__name__'):
                result.append((node.get_name(), symbol.get_name()))
        for child in node.get_children():
            visit(child)
    visit(table)
    return sorted(set(result))


class DeferredTests(unittest.TestCase):
    def fixture(self, root):
        def put(name, data):
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data if isinstance(data, bytes) else json.dumps(data).encode())
            return path
        sha = lambda path: core.sha(Path(path).read_bytes())
        source = put('src/unit.c', b'unsigned int unit(void){return 1;}\n')
        obj = put('old.o', b'fake-comparison-object')
        compiler = put('tools/compiler.exe', b'not-an-executable')
        producer = put('producer.py', b'pass\n')
        helper = put('fake-helper.py', b'pass\n')
        rom = put('rom.bin', b'fake-model-input')
        put('main.bin', b'four')
        put('ov.bin', b'four')
        put('provenance/seed-manifest.json', {})
        put('ledger.json', {})
        dependency = put('dependency.py', b'pass\n')
        report = 'evidence/matches/cohort175-packet-06.json'
        row = dict(name='unit', source='src/unit.c', sourceSha256=sha(source), sourceDependencies=[], object='old.o', objectSha256=sha(obj), compiler='tools/compiler.exe', compilerSha256=sha(compiler), compilerFlags=['-O2', '-lang', 'c99', '-O4,p'], address='0x2000000', bytes=4, nativeSymbolEntries={})
        put(report, dict(matches=[row]))
        batch = dict(report=report, sourceHashes={}, entries=1, kind='functions')
        raw_registry = dict(batches=[batch])
        put('recovery.json', raw_registry)
        (root / 'work').mkdir()
        calls = []
        epoch = SimpleNamespace(committed_revision='a' * 40, ensure=lambda: calls.append('epoch'), check_canonical=lambda actual: self.assertEqual(actual, raw_registry['batches']))
        return SimpleNamespace(root=root, put=put, sha=sha, row=row, report=report, batch=batch, helper=helper, producer=producer, compiler=compiler, rom=rom, dependency=dependency, epoch=epoch, calls=calls)

    def test_all_five_active_deferred_modules_have_no_unresolved_globals(self):
        contract = json.loads((HERE / 'cohort176-epoch-contract-v2.json').read_bytes())
        for pin in contract['implementationPins']:
            path = HERE / pin['path']
            if not path.is_file():
                path = BASE / pin['path']
            with self.subTest(module=pin['path']):
                self.assertEqual(unresolved(path), [])

    def test_original_regression_detects_both_preserved_v1_misses(self):
        if not BASE.is_dir():
            self.skipTest('Historical authoring predecessor is audit-only after promotion')
        self.assertEqual(unresolved(BASE / 'cohort176_legacy_live_v1.py'), [('ten_live', 'producer_view'), ('ten_live', 'validate_contract')])

    def test_committed_ten_body_resolves_both_qualified_calls_before_tool_boundary(self):
        with tempfile.TemporaryDirectory(prefix='pure-ten-', dir=SANDBOX_PARENT) as temporary:
            root = Path(temporary).resolve()
            self.assertTrue(root.is_relative_to(SANDBOX_PARENT))
            f = self.fixture(root)
            contract = dict(dependencies=[], inventoryDependencies=[], remainingMainConsumerInventory=dict(path='inventory.json', sha256='unused'), consumers=[dict(report=f.report, generator='producer.py', batchSha256=core.canonical(f.batch), row=f.row)])
            f.put('inventory.json', {})
            legacy = ModuleType('qualify_ten_consumers_v2')
            exports = dict(ROOT=root, canonical=core.canonical, blob=lambda name: (root / name).read_bytes(), digest=core.sha, LEDGER='ledger.json', sha256=f.sha, SOURCE=core.SOURCE, source_path=lambda name: (name, root / name), read_json=lambda p: json.loads(Path(p).read_bytes()), validate_report=lambda raw, item: (json.loads(raw), f.row), closed_graph=lambda row: {}, object_contract=lambda p, row: dict(fake=True), configuration=lambda: dict(rom=f.rom), ROM=f.sha(f.rom), derive_main=lambda: b'four', overlay=SimpleNamespace(derive=lambda *args: dict(fake=True)), OV='ov.bin', MAIN='main.bin', main_packets=SimpleNamespace(read_json=lambda p: json.loads(Path(p).read_bytes())), linker=SimpleNamespace(validate=lambda *a: self.fail('Unexpected link')))
            for name, value in exports.items():
                setattr(legacy, name, value)
            legacy.__file__ = str(f.helper)
            legacy.load_contract = lambda: contract
            legacy.validate_contract = lambda actual: f.calls.append(('validate_contract', actual))
            legacy.producer_view = lambda report, item: (f.calls.append(('producer_view', report, item)) or (copy.deepcopy(report), []))
            def boundary(*args):
                f.calls.append('fake-compiler-boundary')
                raise ToolBoundary('No real compiler or linker may launch')
            legacy.qualify_report = boundary
            with patch.dict(sys.modules, {'qualify_ten_consumers_v2': legacy}), patch.object(live.subprocess, 'run', side_effect=AssertionError('Real subprocess forbidden')):
                with self.assertRaises(ToolBoundary):
                    live.ten_live(f.epoch, contract, root / 'work/output')
            self.assertEqual(sum(isinstance(x, tuple) and x[0] == 'validate_contract' for x in f.calls), 1)
            self.assertEqual(sum(isinstance(x, tuple) and x[0] == 'producer_view' for x in f.calls), 1)
            self.assertEqual(f.calls.count('fake-compiler-boundary'), 1)
            self.assertFalse((root / 'work/output/wrong-O0.o').exists())

    def test_committed_child_body_resolves_until_first_intercepted_compiler_boundary(self):
        with tempfile.TemporaryDirectory(prefix='pure-child-', dir=SANDBOX_PARENT) as temporary:
            root = Path(temporary).resolve()
            self.assertTrue(root.is_relative_to(SANDBOX_PARENT))
            f = self.fixture(root)
            archive, child = f.put('archive.bin', b'archive'), f.put('child.bin', b'child')
            refs = {'archive.bin': f.sha(archive), 'child.bin': f.sha(child)}
            contract = dict(helperSha256=f.sha(f.helper), producer='producer.py', dependencies={'dependency.py': f.sha(f.dependency)})
            path = f.put('contract.json', contract)
            legacy = ModuleType('qualify_child_snd_reference_v1_20261107')
            def local(name):
                result = root / name
                self.assertTrue(result.is_file())
                return result
            exports = dict(ROOT=root, sha=f.sha, read=lambda p: json.loads(Path(p).read_bytes()), local=local, ROM_SHA=f.sha(f.rom), REPORT=f.report, REPORT_SHA=f.sha(root / f.report), validate=lambda c, registry, report: f.row, compiler_inputs=lambda row: {}, REFS=refs, object_contract=lambda p, row: dict(fake=True), child_link=lambda *a: self.fail('Unexpected child linker'), resumed_positive=lambda *a: self.fail('Old resumption forbidden'), derive_originals=lambda p: ({}, b'x' * 256), ensure=lambda *a: None, canonical=core.canonical, committed=lambda name: (root / name).read_bytes(), CONTRACT=path)
            for name, value in exports.items():
                setattr(legacy, name, value)
            legacy.__file__ = str(f.helper)
            linker = ModuleType('link_runtime_unit')
            project = ModuleType('project')
            project.configuration = lambda: dict(rom=f.rom)
            def boundary(*args, **kwargs):
                f.calls.append(('fake-native-boundary', args, kwargs))
                raise ToolBoundary('Native subprocess intercepted before dispatch')
            with patch.dict(sys.modules, {'qualify_child_snd_reference_v1_20261107': legacy, 'link_runtime_unit': linker, 'project': project}), patch.object(live.subprocess, 'run', side_effect=boundary):
                with self.assertRaises(ToolBoundary):
                    live.child_live(f.epoch, contract, root / 'work/output')
            commands = [x for x in f.calls if isinstance(x, tuple) and x[0] == 'fake-native-boundary']
            self.assertEqual(len(commands), 1)
            self.assertEqual(commands[0][1][0], [str(f.compiler), *f.row['compilerFlags'], '-c', str(root / f.row['source']), '-o', str(root / 'work/output/explicit-c99.o')])
            self.assertFalse((root / 'work/output/explicit-c99.o').exists())

    def test_exact_v1_to_v2_legacy_fix_is_only_two_qualified_names(self):
        if not BASE.is_dir():
            self.skipTest('Historical authoring predecessor is audit-only after promotion')
        restored = (HERE / 'cohort176_legacy_live_v2.py').read_text().replace('    legacy.validate_contract(contract)', '    validate_contract(contract)').replace('view, aliases = legacy.producer_view(', 'view, aliases = producer_view(')
        self.assertEqual(restored, (BASE / 'cohort176_legacy_live_v1.py').read_text())

    def test_context_successor_changes_only_legacy_import(self):
        if not BASE.is_dir():
            self.skipTest('Historical authoring predecessor is audit-only after promotion')
        restored = (HERE / 'cohort176_committed_context_v2.py').read_text().replace('import cohort176_legacy_live_v2 as legacy_live', 'import cohort176_legacy_live_v1 as legacy_live')
        self.assertEqual(restored, (BASE / 'cohort176_committed_context_v1.py').read_text())


if __name__ == '__main__':
    unittest.main()
