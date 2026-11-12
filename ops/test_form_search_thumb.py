"""Tests for ops/form_search_thumb.py's three idiom dimensions.

Every dimension must be able to produce an observable machine-code difference,
because that is the only evidence that a form search can move a row at all.
Each positive test compiles two forms of the same function and pins the
instruction the image idiom is about:

* ``WRITEBACK`` -- a store whose destination pointer stays live becomes
  ``stm`` in mwcc, an ordinary indexed store stays ``str``.
* ``HOIST`` -- a third live argument keeps the literal-pool load after the
  store; a two-argument call hoists the load above it.
* ``LOOP`` -- the countdown ``do``/``while`` is shorter and has no pre-test
  branch, the ``for`` form has one.

The control is the other half of the contract: a spec with no dimension, or a
dimension whose alternatives are equivalent source spellings, must produce
byte-identical code.  That is what stops a "difference" from being noise.

The tests compile with the lane's real p032/2.0-base toolchain and skip when
the private toolchain is unavailable, like the other ops/ tests.
"""
import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import form_search_thumb  # noqa: E402

COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'


def thumb_words(text):
    return list(struct.unpack(f'<{len(text) // 2}H', text[:len(text) // 2 * 2]))


def has_writeback_stm(text):
    """True when the text contains a Thumb ``stm base!, {list}`` form."""
    for halfword in thumb_words(text):
        if halfword & 0xF800 == 0xC000 and halfword & 0x00FF:
            return True
    return False


def first_index(text, predicate):
    for offset in range(0, len(text) - 1, 2):
        halfword = struct.unpack_from('<H', text, offset)[0]
        if predicate(halfword):
            return offset
    return None


def is_pc_load(halfword):
    # 01001 RRRR iiii iiii : LDR (literal)
    return halfword & 0xF800 == 0x4800


def is_byte_store(halfword):
    # 0111 0 RRRR RRR iii : STRB (register offset outside this small range is
    # encoded with 0x5?00; the immediate form used here is 0x7000).
    return halfword & 0xF800 == 0x7000


class CompileMixin:
    @classmethod
    def setUpClass(cls):
        if not COMPILER.is_file():
            raise unittest.SkipTest('pinned mwccarm 2.0/base is unavailable')
        cls.work = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.work.cleanup)

    def compile(self, source, tag='unit'):
        work = Path(self.work.name)
        path = work / f'{tag}.c'
        obj = work / f'{tag}.o'
        path.write_text(source, encoding='utf-8')
        result = form_search.compile_source(COMPILER, path, obj, ROOT,
                                           flags=form_search.FLAGS)
        self.assertEqual(result.returncode, 0,
                         (result.stdout or result.stderr)[-600:])
        text, _defined, _relocations = form_search.read_object(obj)
        return text


class WritebackDimensionTest(CompileMixin, unittest.TestCase):
    """``stm`` only appears when the advanced pointer stays live."""

    def test_live_pointer_walk_emits_stm_but_array_indices_do_not(self):
        forms = dict(form_search_thumb.writeback_forms(
            ['v'], base='p', live_tail='return p;'))
        self.assertIn('array', forms)
        self.assertIn('ptr_walk_live', forms)
        template = ('typedef unsigned int u32;\n'
                    'unsigned *f(unsigned *p, unsigned v) {\n%s\n}\n')
        indexed = self.compile(template % forms['array'], 'wb_array')
        walked = self.compile(template % forms['ptr_walk_live'], 'wb_live')
        self.assertFalse(has_writeback_stm(indexed),
                         'indexed stores must stay plain str')
        self.assertTrue(has_writeback_stm(walked),
                        'a live advanced pointer must let mwcc emit stm')
        self.assertNotEqual(indexed, walked)

    def test_struct_assignment_emits_stm_even_without_a_pointer_walk(self):
        # Two words stay in registers; three words make mwcc copy the local
        # struct through the stack, which is the ldm/stm pair.
        forms = dict(form_search_thumb.writeback_forms(['v', 'w', 'x'], base='p'))
        self.assertIn('struct_fields', forms)
        source = ('typedef unsigned int u32;\n'
                  'void f(unsigned *p, unsigned v, unsigned w, unsigned x) {\n%s\n}\n'
                  % forms['struct_fields'])
        text = self.compile(source, 'wb_struct')
        self.assertTrue(has_writeback_stm(text),
                        'a three-word struct assignment must use ldm/stm')


class HoistDimensionTest(CompileMixin, unittest.TestCase):
    """A live third argument delays the pool load past the store."""

    DECL = ('extern void hook();\n'
            'void f(int a, char *p, int c) {\n%s\n}\n')

    def test_live_argument_moves_the_pool_load_after_the_store(self):
        direct = 'p[2] = 0x67; hook(a, (int)p);'
        live = 'p[2] = 0x67; hook(a, (int)p, c);'
        direct_text = self.compile(self.DECL % direct, 'ho_direct')
        live_text = self.compile(self.DECL % live, 'ho_live')
        direct_load = first_index(direct_text, is_pc_load)
        direct_store = first_index(direct_text, is_byte_store)
        live_load = first_index(live_text, is_pc_load)
        live_store = first_index(live_text, is_byte_store)
        self.assertIsNotNone(direct_load)
        self.assertIsNotNone(live_load)
        self.assertLess(direct_load, direct_store,
                        'the two-argument call should hoist the pool load')
        self.assertLess(live_store, live_load,
                        'the live third argument should delay the pool load')
        self.assertNotEqual(direct_text, live_text)

    def test_hoist_library_lists_both_orderings(self):
        names = [name for name, _body in form_search_thumb.hoist_forms(
            'p[2] = 0x67;', 'hook(a, (int)p);')]
        self.assertEqual(names[0], 'direct')
        self.assertIn('comma', names)


class LoopDimensionTest(CompileMixin, unittest.TestCase):
    """The countdown ``do`` form has no pre-test branch."""

    def test_do_and_for_spell_the_same_loop_differently(self):
        forms = dict(form_search_thumb.loop_forms(body='*p++ = n;', count='n'))
        self.assertEqual(set(forms), {'for', 'while', 'do', 'goto'})
        template = 'void f(int *p, int n) {\n    int i;\n%s\n}\n'
        loop_for = self.compile(template % forms['for'], 'loop_for')
        loop_do = self.compile(template % forms['do'], 'loop_do')
        self.assertNotEqual(loop_for, loop_do)
        self.assertLess(len(loop_do), len(loop_for),
                        'the rotated loop should not carry the pre-test branch')
        # The pre-test spelling is a branch over the body; the rotated one
        # starts with the body.
        self.assertTrue(any((word & 0xF800) == 0xE000 for word in thumb_words(loop_for)),
                        'the pre-tested form needs an unconditional branch')
        self.assertFalse(any((word & 0xF800) == 0xE000 for word in thumb_words(loop_do)),
                         'the rotated form must not need a pre-test branch')


class ControlTest(CompileMixin, unittest.TestCase):
    """A dimension must not change code when its forms are equivalent."""

    def write_spec(self, template, dimensions):
        directory = Path(self.work.name)
        template_path = directory / 'control.c'
        template_path.write_text(template, encoding='utf-8')
        spec_path = directory / 'control.json'
        spec_path.write_text(json.dumps({
            'address': '0x02000000', 'bytes': 8, 'module': 'main',
            'template': 'control.c', 'dimensions': dimensions,
        }), encoding='utf-8')
        return form_search_thumb.load_spec(spec_path)

    def test_absent_dimension_is_a_byte_identical_control(self):
        template = 'int f(int x) { return x + 1; }\n'
        spec = self.write_spec(template, {})
        candidates = form_search_thumb.expand(spec)
        self.assertEqual(len(candidates), 1)
        choices, source = candidates[0]
        self.assertEqual(choices, {})
        self.assertEqual(source, template)
        self.assertEqual(self.compile(source, 'ctl_a'),
                         self.compile(template, 'ctl_b'))

    def test_equivalent_forms_must_not_change_the_object(self):
        template = 'int f(void) {\n$HOIST\n}\n'
        spec = self.write_spec(template, {'HOIST': ['    return 1;', '    return 1u;']})
        candidates = form_search_thumb.expand(spec)
        self.assertEqual(len(candidates), 2)
        first = self.compile(candidates[0][1], 'ctl_c')
        second = self.compile(candidates[1][1], 'ctl_d')
        self.assertEqual(first, second,
                         'equivalent spellings must not look like a dimension win')

    def test_library_control_none_is_the_unsubstituted_template(self):
        # Every library's first form is the plain spelling; the no-dimension
        # expansion is what the row spec falls back to.
        names = [name for name, _text in form_search_thumb.writeback_forms(
            ['v'], base='p')]
        self.assertEqual(names[0], 'array')
        self.assertEqual(form_search_thumb.dimension_alternatives(
            {'dimensions': {}}, 'WRITEBACK'), [('none', '')])


class SpecTest(unittest.TestCase):
    def test_unknown_dimension_is_rejected(self):
        with self.assertRaises(form_search_thumb.SpecError):
            form_search_thumb.dimension_alternatives(
                {'dimensions': {'BOGUS': ['x']}}, 'BOGUS')

    def test_missing_template_is_rejected(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / 'spec.json'
        path.write_text(json.dumps({'address': '0x0', 'bytes': 4,
                                    'template': 'absent.c'}), encoding='utf-8')
        with self.assertRaises(form_search_thumb.SpecError):
            form_search_thumb.load_spec(path)


class RankTest(unittest.TestCase):
    """Ranking must be size-first, then idiom-bearing rows."""

    def test_rank_prefers_small_rows_and_flags_idioms(self):
        batch_one = (0x0208ba68, 0x020a3d9c, 0x0208ed2c, 0x020a8bc4)
        ranked = form_search_thumb.rank_targets(ROOT, exclude=batch_one)
        if not ranked:
            raise unittest.SkipTest('private ledger is unavailable')
        sizes = [row['bytes'] for row in ranked]
        self.assertEqual(sizes, sorted(sizes))
        self.assertTrue(all('address' in row and 'idioms' in row for row in ranked))
        # The documented batch-1 population: 201 unopened rows minus the four
        # already authored in src/main/t1_main_thumb.
        self.assertEqual(len(ranked), 197,
                         'the unmatched main/Thumb population must stay at 197')


if __name__ == '__main__':
    unittest.main()
