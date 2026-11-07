import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('child_reference_under_test', HERE / 'qualify_child_snd_reference_v1_20261107.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
ROOT = helper.ROOT
CONTRACT = helper.read(HERE / 'child-snd-reference-contract-v1.json')
REGISTRY = helper.read(ROOT / 'recovery.json')['batches']
REPORT = helper.read(ROOT / helper.REPORT)


class ContractTests(unittest.TestCase):
    def test_exact_scope(self):
        row = helper.validate(CONTRACT, REGISTRY, REPORT)
        self.assertEqual(row['bytes'], 196)
        self.assertEqual(len(row['nativeSymbolEntries']), 8)

    def mutate(self, field, value):
        report = copy.deepcopy(REPORT)
        report['matches'][0][field] = value
        with self.assertRaises(ValueError):
            helper.validate(CONTRACT, REGISTRY, report)

    def test_wrong_program(self):
        self.mutate('program', '')

    def test_wrong_cpu(self):
        self.mutate('processor', 'arm7')

    def test_wrong_module(self):
        self.mutate('module', 'main')

    def test_wrong_mode(self):
        self.mutate('mode', 'thumb')

    def test_wrong_address(self):
        self.mutate('address', '0x2006ebc')

    def test_wrong_extent(self):
        self.mutate('bytes', 192)

    def test_wrong_body(self):
        self.mutate('targetSha256', '0' * 64)

    def test_wrong_source(self):
        self.mutate('sourceSha256', '0' * 64)

    def test_wrong_header(self):
        headers = copy.deepcopy(CONTRACT['row']['sourceDependencies'])
        headers[0]['sha256'] = '0' * 64
        self.mutate('sourceDependencies', headers)

    def test_wrong_compiler(self):
        self.mutate('compilerSha256', '0' * 64)

    def test_wrong_profile(self):
        flags = CONTRACT['row']['compilerFlags'].copy()
        flags[flags.index('-O4,p')] = '-O0'
        self.mutate('compilerFlags', flags)

    def test_all_binding_namespace_fields(self):
        for field, value in [('program', ''), ('processor', 'arm7'), ('module', 'main'), ('mode', 'thumb'), ('address', '0x2000000')]:
            with self.subTest(field=field):
                bindings = copy.deepcopy(CONTRACT['bindings'])
                next(iter(bindings.values()))[field] = value
                self.mutate('nativeSymbolEntries', bindings)

    def test_missing_binding(self):
        bindings = copy.deepcopy(CONTRACT['bindings'])
        bindings.pop(next(iter(bindings)))
        self.mutate('nativeSymbolEntries', bindings)

    def test_wrong_reference_hash(self):
        contract = copy.deepcopy(CONTRACT)
        contract['referencePins'][next(iter(contract['referencePins']))] = '0' * 64
        with self.assertRaises(ValueError):
            helper.validate(contract, REGISTRY, REPORT)

    def test_changed_or_duplicate_batch(self):
        for duplicate in [False, True]:
            registry = copy.deepcopy(REGISTRY)
            selected = next(b for b in registry if b['report'] == helper.REPORT)
            if duplicate:
                registry.append(copy.deepcopy(selected))
            else:
                selected['sourceHashes'][next(iter(helper.REFS))] = '0' * 64
            with self.subTest(duplicate=duplicate), self.assertRaises(ValueError):
                helper.validate(CONTRACT, registry, REPORT)

    def test_closed_actual_source_headers(self):
        inputs = helper.compiler_inputs(CONTRACT['row'])
        self.assertFalse(inputs['originalCodeCompilerInput'])
        self.assertEqual(len(inputs['includes']), 1)

    def test_actual_serialized_first_fresh_object_resumption(self):
        receipt = ROOT / 'work/goal-resume-20261107/child-snd-reference-qualifier-source1/host-backend-stop.json'
        positive = helper.resumed_positive(receipt, CONTRACT['row'])
        self.assertTrue(positive['freshPositiveCompiledByFirstAttemptNotThisInvocation'])
        self.assertEqual(positive['objectSha256'], CONTRACT['row']['objectSha256'])

    def test_boolean_or_unqualified_receipt_cannot_activate_resume(self):
        with self.assertRaises(ValueError):
            helper.resumed_positive(ROOT / 'project.json', CONTRACT['row'])


class CompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import host_arm9_overlay_reference_v1_20261106 as old
        import qualify_ten_consumers_v2 as ten
        cls.old = old
        cls.ten = ten
        cls.old_contract = helper.read(ROOT / 'provenance/host-arm9-overlay-reference-v1-20261106-contract.json')
        cls.ten_contract = helper.read(ROOT / 'ten-consumer-contract-v2.json')

    def prior_projection(self, actual):
        old, unused = self.old._comparison_projection(actual, self.old_contract)
        return self.ten.project_batches(old, self.ten_contract)[0]

    def test_existing39_and_ten_membership(self):
        self.assertEqual(sum(len(c['rows']) for c in self.old_contract['consumers']), 39)
        self.assertEqual(len(self.ten_contract['consumers']), 10)
        self.assertEqual(sum(c['row']['bytes'] for c in self.ten_contract['consumers']), 2100)

    def test_only_two_fields_one_batch_after_existing_routes(self):
        original = copy.deepcopy(REGISTRY)
        prior = self.prior_projection(REGISTRY)
        result, event = helper.project_batches(prior, CONTRACT)
        self.assertEqual(REGISTRY, original)
        self.assertEqual(set(event['removed']), set(helper.REFS))
        self.assertEqual(sum(a != b for a, b in zip(prior, result)), 1)
        before = next(b for b in prior if b['report'] == helper.REPORT)
        after = next(b for b in result if b['report'] == helper.REPORT)
        expected = copy.deepcopy(before)
        for key in helper.REFS:
            del expected['sourceHashes'][key]
        self.assertEqual(after, expected)

    def test_changed_shadow_ref_or_extra_input_rejects(self):
        for extra in [False, True]:
            registry = copy.deepcopy(REGISTRY)
            batch = next(b for b in registry if b['report'] == helper.REPORT)
            batch['sourceHashes']['extract/unapproved.bin' if extra else next(iter(helper.REFS))] = '0' * 64
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                helper.project_batches(registry, CONTRACT)

    def test_hook_preserves_original_gate_order_and_restores(self):
        import qualify_arm9_overlay_reference_inputs_20261105 as overlay
        prior = self.prior_projection(REGISTRY)
        proof = dict(contractCanonicalSha256=helper.canonical(CONTRACT), inputHashes={})
        seen = []
        def gate(actual, report, declared):
            self.assertEqual(actual, REGISTRY)
            self.assertEqual(next(b for b in actual if b['report'] == helper.REPORT), CONTRACT['batch'])
            seen.append('unchanged-canonical-gate-and-existing-projections')
            return prior, ['existing39+10-fixture']
        with patch.object(overlay, 'project_batches', gate), patch.object(helper, 'qualify', return_value=proof) as live:
            with helper.route(CONTRACT, HERE / 'not-executed-fixture') as routed:
                projected, previous = overlay.project_batches(REGISTRY, None, None)
                self.assertEqual(previous, ['existing39+10-fixture'])
                self.assertEqual(len(routed['childProjectionEvents']), 1)
                self.assertEqual(sum(a != b for a, b in zip(prior, projected)), 1)
            self.assertIs(overlay.project_batches, gate)
            live.assert_called_once()
        self.assertEqual(seen, ['unchanged-canonical-gate-and-existing-projections'])

    def test_hook_restores_on_exception(self):
        import qualify_arm9_overlay_reference_inputs_20261105 as overlay
        previous = overlay.project_batches
        proof = dict(contractCanonicalSha256=helper.canonical(CONTRACT), inputHashes={})
        with patch.object(helper, 'qualify', return_value=proof):
            with self.assertRaisesRegex(RuntimeError, 'fixture-stop'):
                with helper.route(CONTRACT, HERE / 'not-executed-fixture'):
                    raise RuntimeError('fixture-stop')
        self.assertIs(overlay.project_batches, previous)


if __name__ == '__main__':
    unittest.main(verbosity=2)
