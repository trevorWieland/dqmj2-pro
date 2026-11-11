"""Regression tests for ops/form_search.py relocation patching.

The patcher is the project's measurement path: `ops/compiler_matrix.py`, `ops/permuter.py`
targets and `ops/verify_permuter.py` all go through `form_search.relocate`. These tests pin
the two decisions that are easy to get wrong and expensive to notice:

* a Thumb branch target's instruction set comes from the target, not from the placeholder
  halfword the compiler leaves in the object (``docs/authoring/2026-11-11-blx-mode-fix.md``);
* an ``R_ARM_ABS32`` to a Thumb *function* carries the ARM ELF Thumb bit. mwccarm cannot
  encode the callee's mode in a relocatable object, so the patcher has to set it the way the
  linker would; without it a literal function pointer reads back one byte low.
"""
import struct
import sys
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


def patch(text, relocations, defined=None, modes=None):
    return form_search.relocate(bytes(text), 0x02000000, relocations, defined or {}, modes=modes)


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


class UnsupportedTest(unittest.TestCase):
    def test_unknown_relocation_kind_is_rejected(self):
        with self.assertRaises(ValueError):
            patch([0] * 8, [(0, 7, 'native_fn_02001000', 0)])


if __name__ == '__main__':
    unittest.main()
