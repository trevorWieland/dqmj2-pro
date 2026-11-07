import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest import mock


sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import utility_child_snd_alias_v1_20261106 as p
import link_utility


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.row = copy.deepcopy(p.EXPECTED)
        self.plan = ([self.row], {'existing_native_name': '0x2000000'}, [], [{'preserved': True}])
        self.qualified = {'aliases': copy.deepcopy(p.EXPECTED['nativeSymbolEntries'])}

    def test_exact_projection_preserves_all_source_and_metadata_objects(self):
        result = p.project(self.plan, self.qualified, p.PROGRAM, 'arm9')
        self.assertIs(result[0], self.plan[0])
        self.assertIs(result[3], self.plan[3])
        self.assertEqual(len(result[1]), 9)
        self.assertEqual(len(result[2]), 8)
        self.assertEqual(result[1]['existing_native_name'], '0x2000000')
        self.assertEqual(self.plan[1], {'existing_native_name': '0x2000000'})
        self.assertEqual(self.plan[2], [])

    def test_other_plan_and_processor_preserve_exact_original_plan(self):
        other = ([], {}, [], [])
        self.assertIs(p.project(other, self.qualified, 'host', 'arm7'), other)

    def test_wrong_exact_target_context_rejected(self):
        for program, cpu in [('host', 'arm9'), (p.PROGRAM, 'arm7'), (p.PROGRAM, None)]:
            with self.subTest(program=program, cpu=cpu), self.assertRaises(ValueError):
                p.project(self.plan, self.qualified, program, cpu)

    def test_every_namespace_mode_kind_address_and_unknown_alias_rejected(self):
        first = next(iter(self.row['nativeSymbolEntries']))
        for key, value in [('program', 'host'), ('processor', 'arm7'), ('module', 'main'), ('mode', 'thumb'), ('kind', 'data'), ('address', '0x2005888')]:
            wrong = copy.deepcopy(self.row)
            wrong['nativeSymbolEntries'][first][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                p.validate_entry(wrong)
        for remove in [True, False]:
            wrong = copy.deepcopy(self.row)
            if remove:
                del wrong['nativeSymbolEntries'][first]
            else:
                wrong['nativeSymbolEntries']['foreign_alias'] = copy.deepcopy(wrong['nativeSymbolEntries'][first])
            with self.assertRaises(ValueError):
                p.validate_entry(wrong)

    def test_changed_source_object_compiler_flags_extent_rejected(self):
        for key, value in [('sourceSha256', '0' * 64), ('objectSha256', '0' * 64), ('bytes', 192), ('compilerFlags', ['-O0']), ('name', 'foreign')]:
            wrong = copy.deepcopy(self.row)
            wrong[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                p.validate_entry(wrong)

    def test_changed_raw_relocation_contract_rejected(self):
        for key, value in [('offset', 32), ('targetMode', 'thumb'), ('type', 2), ('addend', 0), ('symbol', 'host_alias')]:
            wrong = copy.deepcopy(self.row)
            wrong['relocations'][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                p.validate_entry(wrong)

    def test_duplicate_exact_and_conflicting_existing_aliases(self):
        once = p.project(self.plan, self.qualified, p.PROGRAM, 'arm9')
        twice = p.project(once, self.qualified, p.PROGRAM, 'arm9')
        self.assertEqual(once, twice)
        name = next(iter(self.qualified['aliases']))
        wrong = copy.deepcopy(self.plan)
        wrong[1][name] = '0x2000000'
        with self.assertRaises(ValueError):
            p.project(wrong, self.qualified, p.PROGRAM, 'arm9')
        wrong = copy.deepcopy(once)
        wrong[2][0]['program'] = 'host'
        with self.assertRaises(ValueError):
            p.project(wrong, self.qualified, p.PROGRAM, 'arm9')

    def test_receipt_boolean_cannot_supply_aliases(self):
        with self.assertRaises(KeyError):
            p.project(self.plan, {'passed': True}, p.PROGRAM, 'arm9')
        with self.assertRaises(TypeError):
            with p.factory(link_utility, qualifier=lambda: self.qualified):
                pass

    def test_duplicate_target_row_rejected(self):
        wrong = ([self.row, copy.deepcopy(self.row)], {}, [], [])
        with self.assertRaises(ValueError):
            p.project(wrong, self.qualified, p.PROGRAM, 'arm9')


class ActualFactoryProjectionTests(unittest.TestCase):
    setUp = ProjectionTests.setUp

    def test_work_executable_paths_are_rejected(self):
        for name in ['work/fake/mwccarm.exe', str(p.ROOT / p.EXPECTED['compiler']), 'work/fake/helper.py']:
            with self.subTest(name=name), self.assertRaises(ValueError):
                p.executable(name)

    def test_work_factory_module_is_rejected_before_qualification(self):
        with mock.patch.object(link_utility, '__file__', str(p.ROOT / 'work/fake/link_utility.py')), mock.patch.object(p, 'qualify') as qualify:
            with self.assertRaises(ValueError):
                with p.factory(link_utility):
                    self.fail('Untrusted work module was admitted')
            qualify.assert_not_called()
    def test_actual_module_restores_previous_factory_and_order(self):
        original = link_utility.accepted
        calls = []
        def previous(program, processor=None):
            calls.append(('legacy', program, processor))
            return self.plan
        with mock.patch.object(link_utility, 'accepted', previous), mock.patch.object(p, 'qualify', side_effect=lambda: calls.append(('live-proof-required',)) or self.qualified):
            with p.factory(link_utility):
                result = link_utility.accepted(p.PROGRAM, 'arm9')
                self.assertEqual(len(result[2]), 8)
            self.assertIs(link_utility.accepted, previous)
        self.assertIs(link_utility.accepted, original)
        self.assertEqual(calls, [('live-proof-required',), ('legacy', p.PROGRAM, 'arm9')])

    def test_nested_actual_module_factories_delegate_and_restore(self):
        original = link_utility.accepted
        with mock.patch.object(link_utility, 'accepted', return_value=self.plan) as previous, mock.patch.object(p, 'qualify', return_value=self.qualified) as proof:
            with p.factory(link_utility):
                outer = link_utility.accepted
                with p.factory(link_utility):
                    self.assertEqual(len(link_utility.accepted(p.PROGRAM, 'arm9')[2]), 8)
                self.assertIs(link_utility.accepted, outer)
            self.assertIs(link_utility.accepted, previous)
            self.assertEqual(proof.call_count, 2)
            self.assertEqual(previous.call_count, 1)
        self.assertIs(link_utility.accepted, original)

    def test_qualification_exception_never_installs_factory(self):
        original = link_utility.accepted
        with mock.patch.object(p, 'qualify', side_effect=ValueError('required fresh proof failed')):
            with self.assertRaises(ValueError):
                with p.factory(link_utility):
                    self.fail('Unqualified context was entered')
        self.assertIs(link_utility.accepted, original)

    def test_legacy_exception_restores_actual_previous_factory(self):
        original = link_utility.accepted
        with mock.patch.object(link_utility, 'accepted', side_effect=ValueError('legacy invariant rejected')) as previous, mock.patch.object(p, 'qualify', return_value=self.qualified):
            with self.assertRaises(ValueError):
                with p.factory(link_utility):
                    link_utility.accepted(p.PROGRAM, 'arm9')
            self.assertIs(link_utility.accepted, previous)
        self.assertIs(link_utility.accepted, original)


if __name__ == '__main__':
    unittest.main(verbosity=2)
