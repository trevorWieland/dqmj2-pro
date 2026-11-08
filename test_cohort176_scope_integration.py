import ast
import builtins
import copy
from contextlib import contextmanager, redirect_stderr
import io
import hashlib
import importlib.util
import json
from pathlib import Path
import symtable
import sys
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
SECOND = HERE.parent / 'successor-v2'
for path in (BASE, SECOND):
    if path.is_dir():
        sys.path.insert(0, str(path))
import cohort176_scope_acceptance_v1 as scope
import cohort176_committed_context_v3 as context
import cohort176_epoch_v1 as core
ROOT = next(p for p in (HERE, *HERE.parents) if (p / 'recovery.json').is_file())
NATIVE3 = ROOT / 'work/goal-resume-20261107/cohort176-external-workspace-delta-native3/qualifier-authoring-v1'
CONTRACT = ROOT / 'provenance/cohort176-main-matching-workspace-contract-v1-20261108.json'
if not CONTRACT.is_file():
    CONTRACT = NATIVE3 / 'cohort176-main-matching-workspace-contract-final.json'
BUILDER = ROOT / 'cohort176_scope_state.py'
if not BUILDER.is_file():
    BUILDER = NATIVE3.parent / 'qualifier-authoring-v2/cohort176_scope_state.py'
QUALIFIER = ROOT / 'cohort176_main_matching_workspace_scope.py'
if not QUALIFIER.is_file():
    QUALIFIER = NATIVE3 / 'main_matching_workspace_scope.py'


class ScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT.read_bytes())
        cls.contract['jsonPins']['plan'] = copy.deepcopy(scope.PENDING)
        cls.contract['membershipPins'] = [copy.deepcopy(scope.PENDING) if p['path'] == scope.PLAN else p for p in cls.contract['membershipPins']]
        cls.bundle = {name: json.loads((ROOT / pin['path']).read_bytes()) for name, pin in cls.contract['jsonPins'].items()}
        selected = BUILDER
        spec = importlib.util.spec_from_file_location('selected_pure_shared_builder', selected)
        cls.builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.builder)
        cls.refs = dict(contract=cls.builder.pin('scope-contract.json', cls.builder.encode(cls.contract)))
        cls.proof = dict(cohort=176, sourceReconstructionComplete=False, qualificationCompletedUtc='2026-11-08T01:00:00+00:00', MainMatchingWorkspaceScopePassed=True, contractSha256=cls.refs['contract']['sha256'], historicalOriginalGateExitCode=1,
            preservedSuccessfulGates=15, sourceCreditAddedByScopeRepair=0, sourceRegistrySha256=core.NEW,
            sourcePreferenceSha256=core.PREFS, sourceMatchedFunctions=11660, sourceLinkedBytes=1267058,
            moduleComparisonsExact=20, currentAuthoredFiles=43638 + len(cls.contract['extraSupportPins']),
            unacceptedCandidateFiles=2, extraSupportFiles=len(cls.contract['extraSupportPins']),
            checksumVectors=36, checksumActualReturns=144, getterComparisons=5117,
            missingCachePins=cls.contract['missingCachePins'])
        cls.proof.update({name: False for name in scope.FALSE_FIELDS})
        cls.refs['preproof'] = cls.builder.pin('scope-preproof.json', cls.builder.encode(cls.proof))
        state = scope.Acceptance(cls.refs, cls.contract, cls.bundle, cls.proof, cls.builder)
        cls.driver_pin = cls.builder.pin(scope.SCOPED_DRIVER, cls.builder.encode(state.driver()))

    def state(self, contract=None, bundle=None, proof=None, refs=None):
        return scope.Acceptance(refs or self.refs, contract or self.contract, bundle or self.bundle, proof or self.proof, self.builder)

    def test_truthful_receipt_uses_standard_path_without_old_failure_projection(self):
        original = copy.deepcopy(self.bundle)
        state = self.state()
        result = state.receipt(self.driver_pin, '2026-11-08T01:00:00+00:00')
        self.assertEqual(result['acceptanceScope'], 'current-main-matching-inputs')
        self.assertFalse(result['linksPending'])
        self.assertEqual(result['originalPendingPlan'], scope.PENDING)
        self.assertEqual(result['sourceMatchedFunctions'], 11660)
        self.assertEqual(result['sourceLinkedBytes'], 1267058)
        self.assertEqual(result['migrationReports'], [])
        self.assertEqual(self.bundle, original)
        self.assertEqual(self.bundle['driver']['state'], 'failed')
        self.assertTrue(self.bundle['plan']['linksPending'])
        for name in scope.FALSE_FIELDS:
            self.assertIs(result[name], False)

    def test_scoped_driver_preserves_actual_fifteen_and_original_failed_step(self):
        state = self.state()
        driver = state.driver()
        self.assertEqual(driver['state'], 'QUALIFIED_CURRENT_MAIN_MATCHING_INPUTS')
        self.assertEqual(driver['reusedPassedSteps'], self.bundle['driver']['steps'][:15])
        self.assertEqual(self.bundle['driver']['steps'][15]['exitCode'], 1)
        self.assertEqual(driver['originalGateExitCode'], 1)
        self.assertNotIn('steps', driver)

    def test_all_historical_false_to_true_changes_refused(self):
        for name in scope.FALSE_FIELDS:
            with self.subTest(name=name):
                proof = copy.deepcopy(self.proof)
                proof[name] = True
                with self.assertRaises(ValueError):
                    self.state(proof=proof)

    def test_both_pending_snapshot_pin_positions_are_mandatory(self):
        for which in ('json', 'membership'):
            contract = copy.deepcopy(self.contract)
            if which == 'json':
                contract['jsonPins']['plan']['path'] = scope.PLAN
            else:
                next(p for p in contract['membershipPins'] if p['path'] == scope.PENDING['path'])['path'] = scope.PLAN
            with self.assertRaises(ValueError):
                self.state(contract=contract)

    def test_failed_driver_or_workspace_identity_cannot_be_substituted(self):
        for name in ('driver', 'workspace'):
            contract = copy.deepcopy(self.contract)
            contract['jsonPins'][name]['sha256'] = '0' * 64
            with self.assertRaises(ValueError):
                self.state(contract=contract)

    def test_wrong_counts_namespace_epoch_or_credits_refused(self):
        for name, value in [('sourceMatchedFunctions', 11652), ('sourceLinkedBytes', 1265646), ('sourceRegistrySha256', core.OLD), ('sourcePreferenceSha256', '0' * 64), ('moduleComparisonsExact', 19), ('sourceCreditAddedByScopeRepair', 1), ('extraSupportFiles', 99)]:
            with self.subTest(field=name):
                proof = copy.deepcopy(self.proof)
                proof[name] = value
                with self.assertRaises(ValueError):
                    self.state(proof=proof)

    def test_extra_reference_or_json_role_refused(self):
        refs = dict(self.refs, unexpected=dict(path='unknown', sha256='0' * 64))
        with self.assertRaises(ValueError):
            self.state(refs=refs)
        contract = copy.deepcopy(self.contract)
        contract['jsonPins']['unexpected'] = scope.PENDING
        with self.assertRaises(ValueError):
            self.state(contract=contract)

    def test_original_failed_driver_cannot_be_used_as_scoped_driver(self):
        with self.assertRaises(ValueError):
            self.state().receipt(scope.FAILED_PIN, '2026-11-08T01:00:00+00:00')

    def test_old_gate_exit_cannot_be_silently_fixed(self):
        bundle = copy.deepcopy(self.bundle)
        bundle['driver']['steps'][15]['exitCode'] = 0
        with self.assertRaises(ValueError):
            self.state(bundle=bundle)

    def test_zero_migration_scope_cannot_be_widened(self):
        bundle = copy.deepcopy(self.bundle)
        bundle['plan']['duplicateMigrationFunctions'] = 1
        with self.assertRaises(ValueError):
            self.state(bundle=bundle)

    def test_timestamp_requires_timezone(self):
        with self.assertRaises(ValueError):
            self.state().receipt(self.driver_pin, '2026-11-08T01:00:00')

    def test_checked_actual_pending_snapshot_and_wrong_pin(self):
        raw = scope.checked(ROOT, scope.PENDING)
        self.assertEqual(core.sha(raw), scope.PENDING['sha256'])
        with self.assertRaises(ValueError):
            scope.checked(ROOT, dict(scope.PENDING, sha256='0' * 64))
        with self.assertRaises(ValueError):
            scope.checked(ROOT, dict(scope.PENDING, extra=True))

    def test_committed_qualifier_rejects_uncommitted_input_and_stale_receipt(self):
        state = self.state()
        receipt = state.receipt(self.driver_pin, '2026-11-08T01:00:00+00:00')
        data = {scope.PLAN: json.dumps(receipt).encode(), scope.FAILED: b'failed', scope.WORKSPACE: b'false',
            scope.PENDING['path']: b'pending', self.driver_pin['path']: json.dumps(state.driver()).encode(),
            self.refs['contract']['path']: b'contract', self.refs['preproof']['path']: b'proof'}
        data.update({pin['path']: (ROOT / pin['path']).read_bytes() for pin in self.contract['extraSupportPins']})
        epoch = SimpleNamespace(committed_revision='a' * 40, ensure=lambda: None, read_current=data.__getitem__, read_committed=data.__getitem__)
        with patch.object(scope, 'live_state', return_value=state), patch.object(scope, 'checked', return_value=data[self.driver_pin['path']]):
            result = scope.committed(epoch, ROOT, self.refs, self.driver_pin)
            self.assertEqual(result['commit'], 'a' * 40)
            self.assertNotIn('qualificationCompletedUtc', result['liveScopeProof'])
            self.assertEqual(result['acceptanceQualificationCompletedUtc'], self.proof['qualificationCompletedUtc'])
            epoch.read_committed = lambda name: b'stale' if name == scope.PLAN else data[name]
            with self.assertRaises(ValueError):
                scope.committed(epoch, ROOT, self.refs, self.driver_pin)
            epoch.read_committed = data.__getitem__
            receipt['baselineAndInputsUnchanged'] = True
            data[scope.PLAN] = json.dumps(receipt).encode()
            with self.assertRaises(ValueError):
                scope.committed(epoch, ROOT, self.refs, self.driver_pin)

    def test_precommit_and_committed_phases_do_not_reuse_passed_boolean_only(self):
        state = self.state()
        receipt = state.receipt(self.driver_pin, self.proof['qualificationCompletedUtc'])
        def raw(root, pin):
            return self.builder.encode(receipt if pin['path'] == scope.PLAN else state.driver())
        with patch.object(scope, 'live_state', return_value=state) as live, patch.object(scope, 'checked', side_effect=raw):
            result = scope.precommit(ROOT, self.refs, self.driver_pin, '2026-11-08T01:00:00+00:00')
            self.assertEqual(live.call_count, 1)
            self.assertEqual(result['sourceCreditAddedByScopeRepair'], 0)
        with self.assertRaises(ValueError):
            scope.committed(SimpleNamespace(committed_revision=None), ROOT, self.refs, self.driver_pin)

    def test_precommit_rejects_tampered_canonical_receipt_before_finisher(self):
        state = self.state()
        receipt = state.receipt(self.driver_pin, self.proof['qualificationCompletedUtc'])
        receipt['baselineAndInputsUnchanged'] = True
        def raw(root, pin):
            return self.builder.encode(receipt if pin['path'] == scope.PLAN else state.driver())
        with patch.object(scope, 'live_state', return_value=state), patch.object(scope, 'checked', side_effect=raw):
            with self.assertRaisesRegex(ValueError, 'before finisher'):
                scope.precommit(ROOT, self.refs, self.driver_pin, self.proof['qualificationCompletedUtc'])

    def test_context_never_calls_old_full_driver_route_or_read_masks(self):
        text = (HERE / 'cohort176_committed_context_v3.py').read_text()
        self.assertNotIn('original.validation_route(', text)
        self.assertNotIn('bindings.validation_route(', text)
        self.assertNotIn("patch.object(original, 'read_json'", text)
        self.assertIn('original.extend_contract(', text)
        self.assertIn('original.qualify(adjusted', text)
        self.assertIn('ten.route(', text)
        self.assertIn('child.route(', text)
        self.assertIn('registered.validation_route(', text)

    def test_all_new_deferred_globals_resolve(self):
        if (HERE / 'recovery.json').is_file():
            for module in (scope, context, core):
                self.assertEqual(Path(module.__file__).resolve().parent, HERE)
        for name in ('cohort176_scope_acceptance_v1.py', 'cohort176_committed_context_v3.py'):
            table = symtable.symtable((HERE / name).read_text(), name, 'exec')
            bound = {s.get_name() for s in table.get_symbols() if s.is_imported() or s.is_assigned() or s.is_namespace()}
            bad = []
            def visit(node):
                for s in node.get_symbols():
                    if s.is_global() and s.is_referenced() and s.get_name() not in bound and not hasattr(builtins, s.get_name()) and s.get_name() not in ('__file__', '__name__'):
                        bad.append((node.get_name(), s.get_name()))
                for child in node.get_children():
                    visit(child)
            visit(table)
            self.assertEqual(bad, [])

    def test_explicit_context_enters_scope_factory_without_old_driver_route(self):
        class Boundary(RuntimeError):
            pass
        modules = {}
        names = ['source_packet_committed_context', 'qualify_arm9_overlay_reference_inputs_20261105',
            'qualify_ten_consumers_v2', 'qualify_child_snd_reference_v1_20261107', 'registered_input_path_context_v1_20261107']
        for name in names:
            module = ModuleType(name)
            module.__file__, module.ROOT = str(ROOT / (name + '.py')), ROOT
            modules[name] = module
        def boundary():
            raise Boundary('No native or old-context work may start')
        modules[names[0]].load_contract = boundary
        modules[names[0]].validation_route = lambda *args: self.fail('Forbidden old driver route')
        epoch = SimpleNamespace(contract=dict(registrySha256=core.NEW), committed_revision='a' * 40,
            current_hashes={name + '.py': core.sha((ROOT / (name + '.py')).read_bytes()) for name in names})
        receipt = self.state().receipt(self.driver_pin, '2026-11-08T01:00:00+00:00')
        with patch.dict(sys.modules, modules), patch.object(scope, 'committed', return_value=dict(receipt=receipt)) as gated:
            with self.assertRaises(Boundary):
                with context.validation_route(epoch, ROOT, ROOT / 'work/cohort176-scope-tests-never-context-output', self.refs, self.driver_pin):
                    self.fail('Unreachable')
            self.assertEqual(gated.call_count, 1)
        self.assertFalse((ROOT / 'work/cohort176-scope-tests-never-context-output').exists())

    def test_live_scope_backend_must_run_and_match_preproof(self):
        serialized = {pin['path']: json.dumps(self.bundle[name]).encode() for name, pin in self.contract['jsonPins'].items()}
        serialized[scope.PENDING['path']] = (ROOT / scope.PENDING['path']).read_bytes()
        serialized[self.refs['contract']['path']] = json.dumps(self.contract).encode()
        serialized[self.refs['preproof']['path']] = json.dumps(self.proof).encode()
        helper = QUALIFIER.read_bytes()
        self.assertEqual(core.sha(helper), scope.HELPER_SHA)
        observed = {k: v for k, v in self.proof.items() if k != 'qualificationCompletedUtc'}
        fake = SimpleNamespace(__file__=str(ROOT / 'cohort176_main_matching_workspace_scope.py'), qualify=lambda *args: copy.deepcopy(observed))
        builder = SimpleNamespace(__file__=str(ROOT / 'cohort176_scope_state.py'), build_records=self.builder.build_records, encode=self.builder.encode, pin=self.builder.pin)
        builder_raw = BUILDER.read_bytes()
        original_read = Path.read_bytes
        def read(path):
            if path == ROOT / 'cohort176_main_matching_workspace_scope.py':
                return helper
            return builder_raw if path == ROOT / 'cohort176_scope_state.py' else original_read(path)
        with patch.object(scope, 'checked', side_effect=lambda root, pin: serialized[pin['path']]), patch.object(scope.importlib, 'import_module', side_effect=lambda name: builder if name == 'cohort176_scope_state' else fake), patch.object(Path, 'read_bytes', read):
            state = scope.live_state(ROOT, self.refs)
            self.assertEqual(state.proof, self.proof)
            fake.qualify = lambda *args: dict(observed, sourceLinkedBytes=0)
            with self.assertRaises(ValueError):
                scope.live_state(ROOT, self.refs)

    def test_shared_builder_exact_byte_roundtrip_and_acyclic_driver_pin(self):
        self.assertEqual(core.sha(BUILDER.read_bytes()), scope.BUILDER_SHA)
        state = self.state()
        created = self.proof['qualificationCompletedUtc']
        driver, receipt = self.builder.build_records(self.bundle['plan'], self.proof, self.bundle['driver'], state.record_references(), created)
        self.assertEqual(self.builder.encode(state.driver()), self.builder.encode(driver))
        self.assertEqual(self.builder.encode(state.receipt(self.driver_pin, created)), self.builder.encode(receipt))
        self.assertEqual(receipt['scopedDriver'], self.builder.pin(scope.SCOPED_DRIVER, self.builder.encode(driver)))
        self.assertNotIn('scopedDriver', driver)
        self.assertEqual(driver['scopeSummary'], self.proof)

    def test_manifest_alignment_remains_distinct_from_typed_source_totals(self):
        state = self.state()
        receipt = state.receipt(self.driver_pin, self.proof['qualificationCompletedUtc'])
        self.assertEqual(receipt['sourceFunctionBytesIncludingPools'], 1157550)
        self.assertEqual(receipt['sourceDataBytes'], 109484)
        self.assertEqual(receipt['sourceLinkedBytes'] - receipt['sourceFunctionBytesIncludingPools'] - receipt['sourceDataBytes'], 24)
        self.assertEqual(receipt['initializedModuleByteDenominator'], 2512636)

    def test_driver_format_or_captured_proof_pin_drift_refused(self):
        state = self.state()
        compact = json.dumps(state.driver(), separators=(',', ':')).encode()
        with self.assertRaises(ValueError):
            state.receipt(self.builder.pin(scope.SCOPED_DRIVER, compact), self.proof['qualificationCompletedUtc'])
        refs = copy.deepcopy(self.refs)
        refs['preproof']['sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            self.state(refs=refs).driver()

    def test_acceptance_timestamp_cannot_be_replaced_by_later_audit_time(self):
        with self.assertRaises(ValueError):
            self.state().receipt(self.driver_pin, '2026-11-08T01:00:01+00:00')

    def test_extra_support_files_must_belong_to_actual_support_commit(self):
        contract, proof, refs = map(copy.deepcopy, (self.contract, self.proof, self.refs))
        support = dict(path='cohort176_scope_acceptance_v1.py', sha256=core.sha(b'support'), bytes=7)
        contract['extraSupportPins'] = [support]
        refs['contract'] = self.builder.pin('scope-contract.json', self.builder.encode(contract))
        proof.update(contractSha256=refs['contract']['sha256'], currentAuthoredFiles=43639, extraSupportFiles=1)
        refs['preproof'] = self.builder.pin('scope-preproof.json', self.builder.encode(proof))
        state = self.state(contract=contract, proof=proof, refs=refs)
        driver_raw = self.builder.encode(state.driver())
        driver_pin = self.builder.pin(scope.SCOPED_DRIVER, driver_raw)
        receipt = state.receipt(driver_pin, proof['qualificationCompletedUtc'])
        data = {scope.PLAN: self.builder.encode(receipt), scope.FAILED: b'failed', scope.WORKSPACE: b'false',
            scope.PENDING['path']: b'pending', driver_pin['path']: driver_raw,
            refs['contract']['path']: b'contract', refs['preproof']['path']: b'proof', support['path']: b'support'}
        epoch = SimpleNamespace(committed_revision='a' * 40, ensure=lambda: None,
            read_current=data.__getitem__, read_committed=data.__getitem__)
        with patch.object(scope, 'live_state', return_value=state), patch.object(scope, 'checked', return_value=driver_raw):
            snapshot = scope.committed(epoch, ROOT, refs, driver_pin)
            self.assertIn(support['path'], [p['path'] for p in snapshot['definingRecordPins']])
            epoch.read_committed = lambda name: b'uncommitted' if name == support['path'] else data[name]
            with self.assertRaises(ValueError):
                scope.committed(epoch, ROOT, refs, driver_pin)
            with self.assertRaises(ValueError):
                scope.ensure_committed(epoch, snapshot)

    def test_cli_inherited_v9_exact_argv_report_commit_and_exception_restoration(self):
        name = 'verify_committed_source_inputs_context_v9_20261106'
        module = ModuleType(name)
        module.__file__, module.ROOT = str(ROOT / (name + '.py')), ROOT
        observed = []
        module.main = lambda: observed.append(list(sys.argv))
        epoch = SimpleNamespace(committed_revision='a' * 40, ensure=lambda: observed.append('checked'),
            current_hashes={name + '.py': core.sha((ROOT / (name + '.py')).read_bytes())})
        @contextmanager
        def route(*args):
            yield dict(MainMatchingWorkspaceScope=dict(commit='a' * 40))
        argv = sys.argv
        with patch.dict(sys.modules, {name: module}), patch.object(context, 'validation_route', route):
            report = context.run_inherited(epoch, ROOT, HERE / 'never-native-output', self.refs, self.driver_pin)
            self.assertIs(sys.argv, argv)
            self.assertEqual(observed[0], [module.__file__, '--cohort', '176'])
            self.assertEqual(report['commit'], 'a' * 40)
            self.assertFalse(report['originalFullDriverPassed'])
            self.assertFalse(report['originalHistoricalWorkspacePassed'])
            self.assertEqual(report['sourceCredit'], 0)
            class Boundary(RuntimeError):
                pass
            def failure():
                raise Boundary('Synthetic V9 failure')
            module.main = failure
            with self.assertRaises(Boundary):
                context.run_inherited(epoch, ROOT, HERE / 'never-native-output', self.refs, self.driver_pin)
            self.assertIs(sys.argv, argv)
        self.assertFalse((HERE / 'never-native-output').exists())

    def test_cli_refuses_other_cohort_before_input_or_native_work(self):
        with patch.object(sys, 'argv', ['audit', '--cohort', '175']), redirect_stderr(io.StringIO()), patch.object(scope, 'checked', side_effect=AssertionError('No reads admitted')):
            with self.assertRaises(SystemExit) as result:
                context.main()
            self.assertEqual(result.exception.code, 2)

    def test_epoch_contract_json_must_remain_exact_committed_raw_bytes(self):
        raw = b'{"epoch":176}\n'
        pin = self.builder.pin(context.EPOCH_CONTRACT, raw)
        data = {pin['path']: raw}
        epoch = SimpleNamespace(read_current=data.__getitem__, read_committed=lambda name: raw)
        context.ensure_epoch_contract(epoch, pin)
        data[pin['path']] = b'{"epoch":175}\n'
        with self.assertRaises(ValueError):
            context.ensure_epoch_contract(epoch, pin)
        data[pin['path']] = raw
        epoch.read_committed = lambda name: b'uncommitted'
        with self.assertRaises(ValueError):
            context.ensure_epoch_contract(epoch, pin)

    def test_scope_records_are_rechecked_after_namespace_audits(self):
        data = {'scope-preproof.json': b'qualified'}
        epoch = SimpleNamespace(committed_revision='a' * 40, ensure=lambda: None,
            read_current=data.__getitem__, read_committed=lambda name: b'qualified')
        snapshot = dict(commit='a' * 40, definingRecordPins=[dict(path='scope-preproof.json', sha256=core.sha(b'qualified'))])
        scope.ensure_committed(epoch, snapshot)
        data['scope-preproof.json'] = b'changed'
        with self.assertRaises(ValueError):
            scope.ensure_committed(epoch, snapshot)


if __name__ == '__main__':
    unittest.main()
