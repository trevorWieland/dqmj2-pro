import copy
import contextlib
import io
import json
from types import SimpleNamespace
import unittest
from unittest import mock
import run_source_cohort_v6_20261106 as v6


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.source = v6.read_json(v6.ROOT / v6.TEMPLATE)
        self.before = copy.deepcopy(self.source)
        self.backend = SimpleNamespace(run=mock.Mock(return_value=SimpleNamespace(returncode=0)), STDOUT=-2)
        self.dispatch = v6.Dispatch(self.backend)

    def test_exact_sixteen_commands_and_actual_wrapper_log(self):
        commands = v6.expected_commands()
        self.assertEqual(len(commands), 16)
        self.assertEqual(commands[4], v6.WRAPPER)
        self.assertEqual(commands[5], ['integrate_context_v4_20261106.py', '--clean'])
        self.assertEqual(commands[14], ['validate_evidence_ash_cache_20261031.py'])
        self.assertEqual(commands.count(['make_manifest.py']), 2)
        stream = io.StringIO()
        for command in commands:
            self.dispatch.run([v6.sys.executable, str(v6.ROOT / command[0]), *command[1:]], cwd=v6.ROOT, stdout=stream)
        self.dispatch.complete()
        self.assertEqual(self.backend.run.call_count, 16)
        logged = json.loads(stream.getvalue())
        self.assertEqual(logged['actualDelegatedCommand'][1:], [str(v6.ROOT / v6.WRAPPER[0]), '--clean'])
        self.assertEqual(logged['originalCommand'], v6.TARGET)

    def test_source_list_is_never_mutated(self):
        result = v6.rewrite_steps(self.source)
        self.assertEqual(self.source, self.before)
        self.assertIsNot(result['steps'], self.source['steps'])
        self.assertEqual(result['steps'][3]['command'], v6.WRAPPER)
        self.assertEqual(result['steps'][4]['command'], ['integrate.py', '--clean'])
        self.assertEqual(result['steps'][13]['command'], ['validate_evidence.py'])
        for index, item in enumerate(result['steps']):
            if index != 3:
                self.assertEqual(item, self.before['steps'][index])

    def test_duplicate_missing_wrongargs_and_reordered_template_rejected(self):
        mutations = []
        missing = copy.deepcopy(self.source)
        missing['steps'].pop(3)
        mutations.append(missing)
        duplicate = copy.deepcopy(self.source)
        duplicate['steps'].insert(4, copy.deepcopy(duplicate['steps'][3]))
        mutations.append(duplicate)
        wrong = copy.deepcopy(self.source)
        wrong['steps'][3]['command'] = ['link_utility.py']
        mutations.append(wrong)
        reordered = copy.deepcopy(self.source)
        reordered['steps'][0], reordered['steps'][1] = reordered['steps'][1], reordered['steps'][0]
        mutations.append(reordered)
        for value in mutations:
            with self.assertRaises(ValueError):
                v6.rewrite_steps(value)
        self.assertEqual(self.source, self.before)

    def test_wrong_actual_command_and_arguments_rejected_before_process(self):
        for command in [[v6.sys.executable, str(v6.ROOT / 'link_utility.py'), '--clean'], [v6.sys.executable, str(v6.ROOT / 'verify_source_selection_v2_20261106.py'), '--extra']]:
            with self.assertRaises(ValueError):
                self.dispatch.run(command, cwd=v6.ROOT, stdout=io.StringIO())
        self.backend.run.assert_not_called()

    def test_missing_stage_and_duplicate_dispatch_rejected(self):
        with self.assertRaises(ValueError):
            self.dispatch.complete()
        for command in v6.expected_commands():
            self.dispatch.run([v6.sys.executable, str(v6.ROOT / command[0]), *command[1:]], cwd=v6.ROOT, stdout=io.StringIO())
        with self.assertRaises(ValueError):
            self.dispatch.run([v6.sys.executable, str(v6.ROOT / v6.WRAPPER[0]), '--clean'], cwd=v6.ROOT, stdout=io.StringIO())

    def test_additive_provenance_does_not_mutate_original_result(self):
        captured = []
        original = SimpleNamespace(read_json=lambda path: self.source, write_json=lambda path, value: captured.append(value), subprocess=self.backend)
        result = dict(cohort=174, state='running', steps=[])
        v6.delegate(original)
        rewritten = original.read_json(v6.ROOT / v6.TEMPLATE)
        original.write_json(v6.ROOT / 'evidence/verification/cohort174-validation-driver.json', result)
        self.assertNotIn('utilityAliasLinkDelegation', result)
        self.assertEqual(captured[0]['utilityAliasLinkDelegation']['actualCommand'], v6.WRAPPER)
        self.assertEqual(rewritten['steps'][3]['command'], v6.WRAPPER)
        self.assertEqual(self.source, self.before)

    def test_wrong_cohort_and_premature_success_rejected(self):
        writer = mock.Mock()
        original = SimpleNamespace(read_json=lambda path: self.source, write_json=writer, subprocess=self.backend)
        v6.delegate(original)
        for value in [dict(cohort=173, state='running'), dict(cohort=174, state='build-and-regression-checks-passed')]:
            with self.assertRaises(ValueError):
                original.write_json(v6.ROOT / 'evidence/verification/cohort174-validation-driver.json', value)
        writer.assert_not_called()

    def test_unmodified_v5_main_dispatches_all_sixteen_with_in_memory_backends(self):
        original = v6.load_original()
        written = []
        plan = dict(sourceRegistrySha256='registry', expectedSourceMatchedFunctions=42, expectedSourceLinkedBytes=555)
        manifest = dict(functionMatched=42, sourceLinkedBytes=555, exactContainerMatchWithScaffolding=True, rejectedMatchEvidence=[])
        def read(path):
            if path == v6.ROOT / v6.TEMPLATE:
                return self.source
            if path == v6.ROOT / 'manifest.json':
                return manifest
            if path == v6.ROOT / 'evidence/verification/cohort-2026-10-29-174.json':
                return plan
            raise ValueError('Unexpected V5 input read')
        original.read_json = read
        original.write_json = lambda path, value: written.append(copy.deepcopy(value))
        original.sha256 = lambda path: 'registry' if path == v6.ROOT / 'recovery.json' else 'fixture-log'
        original.subprocess = self.backend
        real_open = v6.Path.open
        def memory_log(path, *args, **kwargs):
            if path.parent == v6.ROOT / 'logs/integration' and args[:1] == ('w',):
                return io.StringIO()
            return real_open(path, *args, **kwargs)
        previous = v6.delegate(original)
        try:
            with mock.patch.object(original, 'verify_sources') as source_guard, mock.patch.object(original, 'verify_selection_delegate', return_value={'retained': True}) as selection_guard, mock.patch('qualified_context_builder_entrypoint_v4_20261106.verify', return_value={'retained': True}) as context_guard, mock.patch.object(v6.sys, 'argv', ['run_source_cohort_v6_20261106.py', '--cohort', '174']), mock.patch.object(v6.Path, 'open', memory_log), contextlib.redirect_stdout(io.StringIO()):
                original.main()
            source_guard.assert_called_once()
            selection_guard.assert_called_once()
            context_guard.assert_called_once()
            previous[3].complete()
        finally:
            original.read_json, original.write_json, original.subprocess = previous[:3]
        final = written[-1]
        self.assertEqual(final['state'], 'build-and-regression-checks-passed')
        self.assertEqual([row['command'] for row in final['steps']], v6.expected_commands())
        self.assertEqual(final['contextIntegrationDelegation'], {'retained': True})
        self.assertEqual(final['sourceSelectionDelegation'], {'retained': True})
        self.assertEqual(final['utilityAliasLinkDelegation']['wrapperDispatches'], 1)
        self.assertEqual(self.backend.run.call_count, 16)
        self.assertEqual(self.source, self.before)


if __name__ == '__main__':
    unittest.main(verbosity=2)
