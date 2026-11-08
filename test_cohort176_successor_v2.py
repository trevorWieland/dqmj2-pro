import copy
from contextlib import contextmanager
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
BASE = Path(__file__).resolve().parent.parent / 'successor-v1'
if BASE.is_dir():
    sys.path.insert(0, str(BASE))
import cohort176_epoch_v1 as core
import cohort176_native_reference_v1 as native
import cohort176_registered_paths_v1 as paths
import cohort176_legacy_live_v2 as legacy_live
import cohort176_committed_context_v2 as context


HERE = Path(__file__).resolve().parent
ROOT = next(p for p in (HERE, *HERE.parents) if (p / 'recovery.json').is_file())


class SuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads((HERE / 'cohort176-epoch-contract-v2.json').read_bytes())
        cls.old_raw = subprocess.check_output(['git', 'show', core.SOURCE + ':recovery.json'], cwd=ROOT)
        cls.current_raw = (ROOT / 'recovery.json').read_bytes()
        cls.preferences = (ROOT / 'source-preferences.json').read_bytes()
        cls.old = json.loads(cls.old_raw)
        cls.current = json.loads(cls.current_raw)
        cls.cached = {'recovery.json': cls.current_raw, 'source-preferences.json': cls.preferences}
        for pin in cls.contract['implementationPins']:
            cls.cached[pin['path']] = ((HERE / pin['path']) if (HERE / pin['path']).is_file() else (BASE / pin['path'])).read_bytes()
        for pin in cls.contract['supportPins']:
            cls.cached[pin['path']] = (ROOT / pin['path']).read_bytes()
        for name in cls.contract['reports']:
            cls.cached[name] = (ROOT / name).read_bytes()
        spec = importlib.util.spec_from_file_location('pure_frozen175_paths', ROOT / 'registered_input_path_context_v1_20261107.py')
        cls.frozen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.frozen)
        cls.path_contract = json.loads((ROOT / cls.frozen.CONTRACT).read_bytes())

    def setUp(self):
        self.data = dict(self.cached)

    def read(self, name):
        if name not in self.data:
            self.data[name] = (ROOT / name).read_bytes()
        return self.data[name]

    def epoch(self, contract=None, committed=None):
        value = self.contract if contract is None else contract
        return core.Epoch(value, core.canonical(value), self.old_raw, self.current_raw, self.preferences, self.read, committed or self.read)

    def pure_live(self, epoch):
        proof = native.LiveReferences.__new__(native.LiveReferences)
        proof.identities = {k for k in core.EXPECTED if k[1] == 'arm9'}
        proof.ensure = lambda actual: core.require(actual is epoch, 'Wrong fake epoch')
        return proof

    def test_authentic_exact1375_plus7_in_memory_fixture(self):
        epoch = self.epoch()
        self.assertEqual(len(epoch.rows), 8)
        self.assertEqual(sum(r['bytes'] for r in epoch.rows.values()), 1412)
        self.assertIsNone(epoch.committed_revision)

    def test_structural_old_record_change_refused(self):
        current = copy.deepcopy(self.current)
        current['batches'][0]['entries'] += 1
        with self.assertRaises(ValueError):
            core.registry_delta(self.old, current, self.contract['addedBatches'])

    def test_structural_old_relative_order_refused(self):
        current = copy.deepcopy(self.current)
        current['batches'][0], current['batches'][1] = current['batches'][1], current['batches'][0]
        with self.assertRaises(ValueError):
            core.registry_delta(self.old, current, self.contract['addedBatches'])

    def test_structural_registry_metadata_refused(self):
        current = copy.deepcopy(self.current)
        current['unexpected'] = True
        with self.assertRaises(ValueError):
            core.registry_delta(self.old, current, self.contract['addedBatches'])

    def test_structural_eighth_unknown_report_refused(self):
        current = copy.deepcopy(self.current)
        current['batches'].append(copy.deepcopy(current['batches'][0]))
        with self.assertRaises(ValueError):
            core.registry_delta(self.old, current, self.contract['addedBatches'])

    def test_structural_new_source_or_profile_pin_refused(self):
        current = copy.deepcopy(self.current)
        next(b for b in current['batches'] if b['report'] in self.contract['addedBatches'])['sourceHashes']['unexpected.c'] = '0' * 64
        with self.assertRaises(ValueError):
            core.registry_delta(self.old, current, self.contract['addedBatches'])

    def test_wrong_registry_epoch_refused(self):
        with self.assertRaises(ValueError):
            core.Epoch(self.contract, core.canonical(self.contract), self.old_raw, self.old_raw, self.preferences, self.read, self.read)

    def test_untrusted_contract_hash_refused(self):
        with self.assertRaises(ValueError):
            core.Epoch(self.contract, '0' * 64, self.old_raw, self.current_raw, self.preferences, self.read, self.read)

    def test_wrong_preferences_refused(self):
        with self.assertRaises(ValueError):
            core.Epoch(self.contract, core.canonical(self.contract), self.old_raw, self.current_raw, b'{}', self.read, self.read)

    def test_current_uncommitted_registry_refused(self):
        with self.assertRaises(ValueError):
            self.epoch(committed=lambda p: self.old_raw if p == 'recovery.json' else self.read(p))

    def test_unbound_contract_report_refused(self):
        contract = copy.deepcopy(self.contract)
        contract['reports']['unknown.json'] = {}
        with self.assertRaises(ValueError):
            self.epoch(contract)

    def test_changed_full_namespace_profile_or_source_report_refused(self):
        name = next(iter(self.contract['reports']))
        for key, value in [('program', 'wrong'), ('processor', 'arm7'), ('module', 'main'), ('mode', 'thumb'), ('sourceSha256', '0' * 64), ('compilerFlags', ['-O0'])]:
            with self.subTest(field=key):
                report = json.loads(self.cached[name])
                report['matches'][0][key] = value
                self.data[name] = json.dumps(report).encode()
                with self.assertRaises(ValueError):
                    self.epoch()
        self.data[name] = self.cached[name]

    def test_memory_report_mutation_refused(self):
        epoch = self.epoch()
        next(iter(epoch.reports.values()))['matches'][0]['sourceSha256'] = '0' * 64
        with self.assertRaises(ValueError):
            epoch.ensure()

    def test_memory_registry_mutation_refused(self):
        epoch = self.epoch()
        epoch.registry['batches'][0]['entries'] += 1
        with self.assertRaises(ValueError):
            epoch.ensure()

    def test_exact_nine_projection_old_batches_and_child_unchanged(self):
        epoch = self.epoch()
        result, events = epoch.project(self.current['batches'], self.pure_live(epoch))
        self.assertEqual(len(events), 9)
        old_names = {b['report'] for b in self.old['batches']}
        self.assertEqual([b for b in result if b['report'] in old_names], self.old['batches'])
        for b in result:
            if 'heap-' in b['report'] and b['report'] in self.contract['reports']:
                self.assertEqual(b, next(c for c in self.current['batches'] if c['report'] == b['report']))

    def test_partial_or_projected_registry_never_canonical(self):
        epoch = self.epoch()
        projected, unused = epoch.project(self.current['batches'], self.pure_live(epoch))
        for actual in (self.current['batches'][1:], projected, self.old['batches']):
            with self.assertRaises(ValueError):
                epoch.project(actual, self.pure_live(epoch))

    def test_receipt_boolean_cannot_authorize_projection(self):
        epoch = self.epoch()
        with self.assertRaises(ValueError):
            epoch.project(self.current['batches'], dict(passed=True, functions=6))

    def test_wrong_live_identity_union_refused(self):
        epoch = self.epoch()
        live = self.pure_live(epoch)
        live.identities = set()
        with self.assertRaises(ValueError):
            epoch.project(self.current['batches'], live)

    def test_projection_forwards_after_full_gate_and_restores(self):
        epoch, calls = self.epoch(), []
        def previous(actual, report, declared):
            calls.append((actual, report, declared))
            return actual, ['old-routes']
        module = SimpleNamespace(project_batches=previous)
        with core.installed_projection(module, epoch, self.pure_live(epoch)) as events:
            result = module.project_batches(self.current['batches'], 'report', 'declared')
        self.assertIs(module.project_batches, previous)
        self.assertEqual(result[1], ['old-routes'])
        self.assertEqual(len(events[0]), 9)
        self.assertEqual(calls[0][1:], ('report', 'declared'))

    def test_downstream_projection_exception_restores_hook(self):
        epoch = self.epoch()
        def previous(*args):
            raise RuntimeError('expected')
        module = SimpleNamespace(project_batches=previous)
        with self.assertRaises(RuntimeError):
            with core.installed_projection(module, epoch, self.pure_live(epoch)):
                module.project_batches(self.current['batches'], None, None)
        self.assertIs(module.project_batches, previous)

    def test_actual_v8_accounting_all_paths_and_copied_files(self):
        document = dict(passed=True, sourceCredit=0, registeredRepositoryPathsChecked=21537, explicitCopiedDependencyPaths=983)
        self.assertEqual(core.accounting(document), core.ACCOUNTING)
        for key, value in [('registeredRepositoryPathsChecked', 21438), ('explicitCopiedDependencyPaths', 980), ('sourceCredit', 1), ('passed', False)]:
            with self.assertRaises(ValueError):
                core.accounting(dict(document, **{key: value}))

    def test_exact_seven_views_and_eleven_origins_prepare(self):
        result = paths.prepare(self.epoch(), self.frozen, self.path_contract)
        self.assertEqual(len(result['documents']), 7)
        self.assertEqual(result['report']['historicalProofInputs'], 11)

    def fake_verifier(self, prepared, fail=False):
        original_documents = copy.deepcopy(prepared['documents'])
        def read(path):
            return copy.deepcopy(original_documents[Path(path).relative_to(ROOT).as_posix()])
        module = SimpleNamespace(read_json=read)
        def main():
            for number, name in enumerate(original_documents):
                self.assertEqual(module.read_json(ROOT / name)['previous']['source'], self.frozen.CANON)
                if fail and number == 2:
                    raise RuntimeError('expected')
        module.main = main
        return module, main, read

    def test_seven_views_forward_original_v8_and_restore(self):
        epoch = self.epoch()
        prepared = paths.prepare(epoch, self.frozen, self.path_contract)
        module, main, reader = self.fake_verifier(prepared)
        with paths.installed(module, self.frozen, epoch, prepared, ROOT) as proof:
            module.main()
        self.assertTrue(proof['passed'])
        self.assertEqual(len(proof['events']), 7)
        self.assertIs(module.main, main)
        self.assertIs(module.read_json, reader)

    def test_v8_failure_restores_original_hooks(self):
        epoch = self.epoch()
        prepared = paths.prepare(epoch, self.frozen, self.path_contract)
        module, main, reader = self.fake_verifier(prepared, True)
        with self.assertRaises(RuntimeError):
            with paths.installed(module, self.frozen, epoch, prepared, ROOT):
                module.main()
        self.assertIs(module.main, main)
        self.assertIs(module.read_json, reader)

    def test_v8_missing_actual_dispatch_refused(self):
        epoch = self.epoch()
        prepared = paths.prepare(epoch, self.frozen, self.path_contract)
        module, unused, reader = self.fake_verifier(prepared)
        with self.assertRaises(ValueError):
            with paths.installed(module, self.frozen, epoch, prepared, ROOT):
                pass

    def test_legacy_bindings_forward_only_new_epoch_and_restore_on_error(self):
        epoch = self.epoch()
        one, two = lambda *a: 1, lambda *a: 2
        ten, child = SimpleNamespace(live_qualify=one), SimpleNamespace(qualify=two)
        with patch.object(legacy_live, 'ten_live', return_value='ten') as t, patch.object(legacy_live, 'child_live', return_value='child') as c:
            with self.assertRaises(RuntimeError):
                with legacy_live.installed(epoch, ten, child):
                    self.assertEqual(ten.live_qualify('contract', 'output'), 'ten')
                    self.assertEqual(child.qualify('contract', 'output'), 'child')
                    with self.assertRaises(ValueError):
                        child.qualify('contract', 'output', resume_positive='old')
                    raise RuntimeError('expected')
            self.assertEqual(t.call_args.args, (epoch, 'contract', 'output'))
            self.assertEqual(c.call_args.args, (epoch, 'contract', 'output'))
        self.assertIs(ten.live_qualify, one)
        self.assertIs(child.qualify, two)

    def test_uncommitted_fixture_cannot_start_any_native_entry(self):
        epoch = self.epoch()
        before = set(sys.modules)
        for callback in (lambda: native.qualify(epoch, ROOT, HERE / 'never-output'), lambda: legacy_live.ten_live(epoch, {}, 'never'), lambda: legacy_live.child_live(epoch, {}, 'never')):
            with self.assertRaises(ValueError):
                callback()
        self.assertEqual(set(sys.modules), before)
        self.assertFalse((HERE / 'never-output').exists())

    def test_actual_pinned_six_source_graphs_and_profiles_readonly(self):
        epoch = self.epoch()
        rows = [r for r in epoch.rows.values() if r['processor'] == 'arm9']
        self.assertEqual(len(rows), 6)
        for row in rows:
            graph = native.source_graph(ROOT, row)
            self.assertFalse(graph['originalCodeCompilerInput'])

    def test_hidden_compiler_file_and_language_changes_refused(self):
        row = copy.deepcopy(next(r for r in self.epoch().rows.values() if r['module'] == 'ov001'))
        for flags in (row['compilerFlags'] + ['-Ihidden'], row['compilerFlags'] + ['-include', 'original.bin'], ['-proc', 'arm7tdmi'], row['compilerFlags'] + ['-thumb']):
            wrong = dict(row, compilerFlags=flags)
            with self.assertRaises(ValueError):
                native.source_graph(ROOT, wrong)

    def test_context_has_no_namespace_ledger_append(self):
        source = (HERE / 'cohort176_committed_context_v2.py').read_text()
        self.assertNotIn("['consumers'].append", source)
        self.assertIn('originalMainLedgerFileConsumers=26', source)
        self.assertIn('unchangedMainComparisonViewConsumers=36', source)

    def test_failed_workspace_driver_cannot_activate_context(self):
        revision = 'a' * 40
        docs = {'evidence/verification/cohort-2026-10-29-176.json': dict(sourceRegistrySha256=core.NEW, previousAcceptedCohort=175, linksPending=False, moduleComparisonsExact=20),
            'evidence/verification/cohort176-validation-driver.json': dict(state='failed', steps=[{} for unused in range(16)])}
        read = lambda name: json.dumps(docs[name]).encode()
        epoch = SimpleNamespace(contract=dict(registrySha256=core.NEW), read_current=read, read_committed=read, committed_revision=revision)
        with self.assertRaises(ValueError):
            context.committed_state(epoch, ROOT, revision)
        docs['evidence/verification/cohort176-validation-driver.json']['state'] = 'build-and-regression-checks-passed'
        self.assertEqual(context.committed_state(epoch, ROOT, revision)['commit'], revision)
        with self.assertRaises(ValueError):
            context.committed_state(epoch, ROOT, 'b' * 40)

    def test_reader_source_origin_exact_and_external_fallback_denied(self):
        name = 'parallel_packet_native_unit_identity_v1.py'
        pins = {name: core.sha((ROOT / name).read_bytes())}
        result = native.imported_origins(ROOT, pins, {name[:-3]: SimpleNamespace(__file__=ROOT / name)})
        self.assertEqual(len(result), 1)
        for wrong in (ROOT.parent / 'external-elftools.py', ROOT / 'deps/native/elftools/__pycache__/elf.cpython-313.pyc'):
            with self.assertRaises(ValueError):
                native.imported_origins(ROOT, pins, {'elftools.elf.elffile': SimpleNamespace(__file__=wrong)})

    def test_projection_never_mutates_process_argv(self):
        epoch = self.epoch()
        previous = lambda *args: None
        module = SimpleNamespace(project_batches=previous)
        before = sys.argv[:]
        with core.installed_projection(module, epoch, self.pure_live(epoch)):
            module.project_batches(self.current['batches'], None, None)
        self.assertEqual(sys.argv, before)

    def test_bound_accounting_rejects_stale_report_commit(self):
        epoch = self.epoch()
        epoch.committed_revision = 'a' * 40
        epoch.check_commit = lambda: 'a' * 40
        ten = SimpleNamespace(live_qualify=lambda *args: None)
        child = SimpleNamespace(qualify=lambda *args: None)
        registered = SimpleNamespace(validation_route=lambda *args: None, validate_accounting=lambda *args: None, validate_contract=lambda contract: None)
        document = dict(cohort=176, commit='b' * 40, passed=True, sourceCredit=0, registeredRepositoryPathsChecked=21537, explicitCopiedDependencyPaths=983)
        with context.bindings(epoch, ROOT, ten, child, registered):
            with self.assertRaises(ValueError):
                registered.validate_accounting(document, {})
            document['commit'] = 'a' * 40
            self.assertEqual(registered.validate_accounting(document, {})['canonicalPathCount'], 21537)


if __name__ == '__main__':
    unittest.main()
