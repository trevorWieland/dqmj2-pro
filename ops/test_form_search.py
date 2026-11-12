"""Regression tests for ops/form_search.py relocation patching.

The patcher is the project's measurement path: `ops/compiler_matrix.py`, `ops/permuter.py`
targets and `ops/verify_permuter.py` all go through `form_search.relocate`. These tests pin
the decisions that are easy to get wrong and expensive to notice:

* a Thumb branch's instruction set comes from the measured image at the call site,
  and falls back to *module-scoped* ledger evidence -- never a global address table
  (``docs/authoring/2026-11-11-scanner-module-mode.md``);
* an ``R_ARM_ABS32`` to a Thumb *function* carries the ARM ELF Thumb bit;
* ``R_ARM_PC24``, ``R_ARM_MOVW_ABS_NC`` / ``R_ARM_MOVT_ABS`` and the Thumb MOVW/MOVT
  kinds are encoded rather than silently skipped, and an unknown kind is reported.

The ten accepted ``utility-child-arm7-wram`` rows are an end-to-end check: they
share a base with ``arm7-wram``, so a module-blind lookup encoded BLX where the
child image has BL.
"""
import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import form_search  # noqa: E402


class FakeModes:
    """Stand-in for TargetModes: resolve(target, symbol) -> (mode, evidence)."""

    def __init__(self, modes):
        self.modes = modes

    def resolve(self, target, symbol=None):
        return self.modes.get(target, None), 'test'


def patch(text, relocations, defined=None, modes=None, skip_counts=None):
    return form_search.relocate(bytes(text), 0x02000000, relocations, defined or {},
                                modes=modes, skip_counts=skip_counts)


def make_root(directory, modules):
    """Write a synthetic manifest, module images and ledger under ``directory``."""
    root = Path(directory)
    (root / 'ledger').mkdir(parents=True)
    document = {'modules': []}
    for name, base, image in modules:
        binary = f'extract/{name}.bin'
        path = root / binary
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(image)
        document['modules'].append(dict(name=name, base=hex(base), bytes=len(image),
                                        binary=binary))
    (root / 'manifest.json').write_text(json.dumps(document), encoding='utf-8')
    return root


def write_rows(root, rows):
    with (root / 'ledger/functions.jsonl').open('w', encoding='utf-8') as stream:
        for row in rows:
            stream.write(json.dumps(row) + '\n')


class ImageFirstBranchModeTest(unittest.TestCase):
    """The measured call-site marker, then module-scoped ledger evidence."""

    def fixture(self, child_image, rows):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = make_root(temporary.name, [
            ('host', 0x1000, bytes(0x200)),
            ('child', 0x1000, bytes(child_image)),
        ])
        write_rows(root, rows)
        return root

    @staticmethod
    def rows():
        return [dict(module='host', address='0x00001044', bytes=0x40, mode='arm'),
                dict(module='child', address='0x00001000', bytes=0x10, mode='thumb')]

    def test_image_bl_selects_thumb_despite_host_arm_extent(self):
        child = bytearray(0x80)
        struct.pack_into('<HH', child, 4, 0xF000, 0xF800)
        root = self.fixture(child, self.rows())
        modes = form_search.TargetModes(root, 'child')
        self.assertEqual(modes.site_mode(0x1004), 'thumb')
        self.assertEqual(modes.resolve_site(0x1004, 0x1044), ('thumb', 'image-branch'))
        out = form_search.relocate(bytes(0x20), 0x1000, [(4, 10, 'target', -4)],
                                   {'target': 0x1044}, modes=modes)
        first, second = struct.unpack_from('<HH', out, 4)
        self.assertEqual(first & 0xF800, 0xF000)
        self.assertNotEqual(second & 0xD000, 0xC000,
                            'host arm extent must not turn a measured BL into BLX')

    def test_image_blx_selects_arm_despite_child_thumb_ledger(self):
        child = bytearray(0x80)
        struct.pack_into('<HH', child, 4, 0xF000, 0xE800)
        rows = self.rows()
        rows.append(dict(module='child', address='0x00001044', bytes=4, mode='thumb'))
        root = self.fixture(child, rows)
        modes = form_search.TargetModes(root, 'child')
        self.assertEqual(modes.site_mode(0x1004), 'arm')
        out = form_search.relocate(bytes(0x20), 0x1000, [(4, 10, 'target', -4)],
                                   {'target': 0x1044}, modes=modes)
        _first, second = struct.unpack_from('<HH', out, 4)
        self.assertEqual(second & 0xD000, 0xC000,
                         'the image marker must win over a conflicting ledger row')

    def test_base_collision_never_borrows_the_other_modules_extent(self):
        # The child caller owns 0x1044; the host row covering it is a different
        # image at the same base. With no child evidence the answer is unknown,
        # not the host's ARM extent.
        rows = [dict(module='host', address='0x00001000', bytes=0x100, mode='arm'),
                dict(module='child', address='0x00001000', bytes=0x10, mode='thumb'),
                dict(module='child', address='0x00001020', bytes=0x10, mode='arm')]
        root = self.fixture(bytearray(0x80), rows)
        modes = form_search.TargetModes(root, 'child')
        self.assertEqual(modes.resolve(0x1044), (None, 'fallback'))

    def test_abs32_uses_the_measured_word_over_a_colliding_symbol(self):
        child = bytearray(0x80)
        struct.pack_into('<I', child, 8, 0x1044)  # original pointer, even
        rows = [dict(module='child', address='0x00001044', bytes=4, mode='thumb')]
        root = self.fixture(child, rows)
        modes = form_search.TargetModes(root, 'child')
        self.assertEqual(modes.resolve(0x1044)[0], 'thumb')
        out = form_search.relocate(bytes(0x20), 0x1000, [(8, 2, 'target', 0)],
                                   {'target': 0x1044}, modes=modes)
        self.assertEqual(struct.unpack_from('<I', out, 8)[0], 0x1044,
                         'the image word, not the colliding ledger mode, is the pointer')

    def test_external_target_uses_the_module_that_contains_it(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = make_root(temporary.name, [
            ('host', 0x1000, bytes(0x300)),
            ('child', 0x1000, bytes(0x80)),
        ])
        write_rows(root, [dict(module='host', address='0x00001200', bytes=0x20, mode='arm'),
                          dict(module='child', address='0x00001000', bytes=0x10, mode='thumb')])
        modes = form_search.TargetModes(root, 'child')
        self.assertEqual(modes.resolve(0x1200), ('arm', 'ledger-address'))


class MovwMovtEncodingTest(unittest.TestCase):
    """MOVW/MOVT keep the ``imm4:imm12`` split and the instruction's other fields."""

    def arm(self, kind, target, mode, placeholder, addend=0):
        out = patch(struct.pack('<I', placeholder) + bytes(4),
                    [(0, kind, 'target', addend)], {'target': target},
                    modes=FakeModes({target: mode}))
        return struct.unpack_from('<I', out, 0)[0]

    def thumb(self, kind, target, mode, first, second, addend=0):
        out = patch(struct.pack('<HH', first, second) + bytes(4),
                    [(0, kind, 'target', addend)], {'target': target},
                    modes=FakeModes({target: mode}))
        return struct.unpack_from('<HH', out, 0)

    @staticmethod
    def arm_immediate(word):
        return (((word >> 16) & 0xF) << 12) | (word & 0xFFF)

    @staticmethod
    def thumb_immediate(first, second):
        return (((first & 0xF) << 12) | (((first >> 10) & 1) << 11)
                | (((second >> 12) & 7) << 8) | (second & 0xFF))

    def test_arm_movw(self):
        word = self.arm(43, 0x12345678, 'arm', 0xE3000000)
        self.assertEqual(word, 0xE3050678)
        self.assertEqual(self.arm_immediate(word), 0x5678)

    def test_arm_movt(self):
        word = self.arm(44, 0x12345678, 'arm', 0xE3400000)
        self.assertEqual(word, 0xE3410234)
        self.assertEqual(self.arm_immediate(word), 0x1234)

    def test_thumb_movw_sets_the_thumb_bit(self):
        first, second = self.thumb(47, 0x12345678, 'thumb', 0xF240, 0x0000)
        self.assertEqual((first, second), (0xF245, 0x6079))
        self.assertEqual(self.thumb_immediate(first, second), 0x5679)

    def test_thumb_movt_does_not_set_the_thumb_bit(self):
        first, second = self.thumb(48, 0x12345679, 'thumb', 0xF2C0, 0x0000)
        self.assertEqual((first, second), (0xF2C1, 0x2034))
        self.assertEqual(self.thumb_immediate(first, second), 0x1234)

    def test_addend_is_applied_before_the_split(self):
        first, second = self.thumb(47, 0x12345678, 'arm', 0xF240, 0x0000, addend=4)
        self.assertEqual(self.thumb_immediate(first, second), 0x567C)

    def test_prel_movw_kind_is_reported_not_encoded(self):
        skips = {}
        with self.assertRaises(form_search.UnsupportedRelocation):
            patch(bytes(8), [(0, 45, 'target', 0)], {'target': 0x12345678},
                  skip_counts=skips)
        self.assertEqual(skips, {45: 1})


ROOT = Path(__file__).resolve().parent.parent


class TenUtilityChildRowsTest(unittest.TestCase):
    """End-to-end: the ten accepted rows that exposed the base collision."""

    ROWS = (0x038029F4, 0x037FF3A8, 0x03802AC0, 0x037FF6E4, 0x037FF454,
            0x03801BF8, 0x03802B88, 0x038018E0, 0x03802BD0, 0x03804C8C)

    @classmethod
    def setUpClass(cls):
        cls.ledger = ROOT / 'ledger/functions.jsonl'
        cls.compiler = ROOT / 'tools/mwccarm/mwccarm/1.2/base/mwccarm.exe'
        if not cls.ledger.is_file() or not cls.compiler.is_file():
            raise unittest.SkipTest('private ledger or pinned mwccarm is unavailable')

    def test_ten_rows_score_exact_through_form_search(self):
        sys.path.insert(0, str(ROOT / 'public_tools'))
        import permuter  # noqa: E402
        import source_units  # noqa: E402

        rows = {}
        for line in self.ledger.read_text(encoding='utf-8').splitlines():
            if line.strip():
                row = json.loads(line)
                if row.get('module') == 'utility-child-arm7-wram':
                    rows[int(row['address'], 0)] = row
        config = source_units.load_config(ROOT)
        modes = form_search.TargetModes(ROOT, 'utility-child-arm7-wram')
        image, _, base = form_search.module_image(ROOT, 'utility-child-arm7-wram')
        work = ROOT / 'work/form_search_ten'
        work.mkdir(parents=True, exist_ok=True)
        for address in self.ROWS:
            row = rows[address]
            rule = source_units.resolve(config, row['sourceUnit'])
            flags = [flag for flag in rule['compilerFlags'] if flag != '-thumb']
            thumb = '-thumb' in rule['compilerFlags']
            obj = work / f'{address:08x}.o'
            built = permuter.compile_object(ROOT, ROOT / row['sourceUnit'], obj, flags,
                                            thumb, compiler=ROOT / rule['compilerPath'],
                                            timeout=60)
            self.assertEqual(built.returncode, 0,
                             f'{address:#010x}: {(built.stderr or built.stdout)[-500:]}')
            text, defined, relocations = form_search.read_object(obj)
            actual = form_search.relocate(text, address, relocations, defined, modes=modes)
            wanted = image[address - base:address - base + row['bytes']]
            self.assertEqual(form_search.score(actual, wanted), (0, 0),
                             f'{address:#010x} must reproduce the child image')


class Abs32ThumbBitTest(unittest.TestCase):
    def test_abs32_to_thumb_function_sets_bit_zero(self):
        modes = FakeModes({0x020902F0: 'thumb'})
        out = patch([0] * 12, [(8, 2, 'native_fn_020902f0', 0)], modes=modes)
        self.assertEqual(struct.unpack_from('<I', out, 8)[0], 0x020902F1)

    def test_abs32_to_arm_function_stays_even(self):
        modes = FakeModes({0x020902F0: 'arm'})
        out = patch([0] * 12, [(8, 2, 'native_fn_020902f0', 0)], modes=modes)
        self.assertEqual(struct.unpack_from('<I', out, 8)[0], 0x020902F0)

    def test_abs32_to_data_symbol_never_sets_the_bit(self):
        modes = FakeModes({0x027FFFA8: 'thumb'})
        out = patch([0] * 12, [(8, 2, 'native_data_027fffa8', 0)], modes=modes)
        self.assertEqual(struct.unpack_from('<I', out, 8)[0], 0x027FFFA8)

    def test_unknown_target_mode_is_left_alone(self):
        modes = FakeModes({})
        out = patch([0] * 12, [(8, 2, 'native_fn_020902f0', 0)], modes=modes)
        self.assertEqual(struct.unpack_from('<I', out, 8)[0], 0x020902F0)

    def test_addend_is_applied_before_the_thumb_bit(self):
        modes = FakeModes({0x020902F0: 'thumb'})
        out = patch([0] * 12, [(8, 2, 'native_fn_020902f0', 4)], modes=modes)
        self.assertEqual(struct.unpack_from('<I', out, 8)[0], 0x020902F5)

    def test_no_modes_keeps_the_historical_behaviour(self):
        out = patch([0] * 12, [(8, 2, 'native_fn_020902f0', 0)])
        self.assertEqual(struct.unpack_from('<I', out, 8)[0], 0x020902F0)


class BranchModeTest(unittest.TestCase):
    """kind 10 is one relocation for both BL and BLX; the target decides.

    Thumb-2 encoding: the second halfword is ``11111 J1 J2`` for BL and ``11101 J1 J2``
    for BLX, so bits 15..11 are ``11111`` vs ``11101`` -- that is the marker the
    historical patcher looked for.
    """

    def test_thumb_target_encodes_bl(self):
        modes = FakeModes({0x02001000: 'thumb'})
        out = patch([0] * 8, [(0, 10, 'native_fn_02001000', -4)], modes=modes)
        _first, second = struct.unpack_from('<HH', out, 0)
        self.assertEqual(second & 0xF800, 0xF800, 'BL marker missing for a Thumb target')

    def test_arm_target_encodes_blx(self):
        modes = FakeModes({0x02001000: 'arm'})
        out = patch([0] * 8, [(0, 10, 'native_fn_02001000', -4)], modes=modes)
        _first, second = struct.unpack_from('<HH', out, 0)
        self.assertEqual(second & 0xF800, 0xE800, 'BLX marker missing for an ARM target')

    def test_explicit_arm_hint_wins_over_the_target(self):
        modes = FakeModes({0x02001000: 'thumb'})
        out = patch([0] * 8, [(0, 10, 'native_fn_02001000', -4)], modes=modes)
        hinted = form_search.relocate(bytes(8), 0x02000000,
                                      [(0, 10, 'native_fn_02001000', -4)], {}, arm=True)
        self.assertNotEqual(out, hinted)


class ArmPc24Test(unittest.TestCase):
    def test_arm_bl_uses_pc_bias_from_the_addend(self):
        out = patch(struct.pack('<I', 0xEB000000) + bytes(4),
                    [(0, 1, 'target', -8)], {'target': 0x02000100})
        self.assertEqual(struct.unpack_from('<I', out, 0)[0], 0xEB00003E)

    def test_arm_pc24_keeps_the_condition_field(self):
        out = patch(struct.pack('<I', 0x1A000000) + bytes(4),
                    [(0, 1, 'target', -8)], {'target': 0x02000100})
        self.assertEqual(struct.unpack_from('<I', out, 0)[0], 0x1A00003E)


class UnsupportedTest(unittest.TestCase):
    def test_unknown_relocation_kind_is_rejected(self):
        with self.assertRaises(ValueError):
            patch([0] * 8, [(0, 7, 'native_fn_02001000', 0)])

    def test_unknown_relocation_kind_is_counted(self):
        skips = {}
        with self.assertRaises(form_search.UnsupportedRelocation):
            patch([0] * 8, [(0, 7, 'native_fn_02001000', 0)], skip_counts=skips)
        self.assertEqual(skips, {7: 1})


if __name__ == '__main__':
    unittest.main()
