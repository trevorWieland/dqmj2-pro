"""Regression tests for the Thumb BL/BLX immediate encoder.

Each case is a real call site from the measured image: the site address, the callee the original
linker resolved, the relocation addend the compiler emits for that kind, and the two image
halfwords.  A wrong delta formula shifts every BL by four bytes and these cases fail.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from repo_build import encode_thumb_branch


class ThumbBranchTests(unittest.TestCase):
    def check(self, absolute, target, addend, arm, first, second):
        got_first, got_second = encode_thumb_branch(absolute, target, addend, arm)
        word = (got_second << 16) | got_first
        expected = (second << 16) | first
        self.assertEqual(hex(word), hex(expected),
                         'site 0x%08x -> 0x%08x must encode as 0x%08x, got 0x%08x'
                         % (absolute, target, expected, word))

    def test_ov006_counter_call(self):
        # R_ARM_THM_CALL, addend -4, Thumb callee; image word at 0x021F7212 is 0xF85BF7FE.
        self.check(0x021F7212, 0x021F52CC, -4, False, 0xF7FE, 0xF85B)

    def test_main_thumb_call(self):
        self.check(0x02091C52, 0x02093824, -4, False, 0xF001, 0xFDE7)

    def test_accepted_ov006_units(self):
        # 0x021F7B9C and 0x021FBEA8 were accepted before the encoder rewrite; their real call
        # sites must keep encoding to the image words below.
        self.check(0x021F7BA0, 0x02203EBC, -4, False, 0xF00C, 0xF98C)
        self.check(0x021FBEAC, 0x02203EBC, -4, False, 0xF008, 0xF806)
        self.check(0x021F7BAA, 0x021F23A0, -4, False, 0xF7FA, 0xFBF9)
        self.check(0x021FBEB6, 0x021F23A0, -4, False, 0xF7F6, 0xFA73)

    def test_arm_blx(self):
        # R_ARM_THM_CALL to an ARM callee uses the BLX form with the 0xE800 marker;
        # image word at 0x0208B722 is 0xE900F77B.
        self.check(0x0208B722, 0x02006924, -4, True, 0xF77B, 0xE900)

    def test_ov006_blx_immediate_sites(self):
        # Three real R_ARM_THM_CALL sites whose callee is ARM: the original linker
        # expanded each to the BLX form (0xE800 marker in the second halfword).  The
        # callee mode is measured, not assumed -- the image word itself says ARM.
        self.check(0x021EDA60, 0x02026144, -4, True, 0xF638, 0xEB70)
        self.check(0x021EDB3E, 0x02006B7C, -4, True, 0xF619, 0xE81E)
        self.check(0x021EDCFE, 0x0200F48C, -4, True, 0xF621, 0xEBC6)

    def test_three_blx_rows(self):
        # The three rows that exposed the pipeline bug. Each call site's image word
        # is BLX because the callee is ARM (ledger mode 'arm').
        # 0x021FB384 + 0xA -> 0x02002480; image word 0xE878F607 (07 F6 78 E8).
        self.check(0x021FB38E, 0x02002480, -4, True, 0xF607, 0xE878)
        # 0x021FF02C + 0x1A -> 0x0200616C; image word 0xE892F607 (07 F6 92 E8).
        self.check(0x021FF046, 0x0200616C, -4, True, 0xF607, 0xE892)
        # 0x02203EBC is a Thumb target and must stay BL (existing accepted row).
        self.check(0x021F7BA0, 0x02203EBC, -4, False, 0xF00C, 0xF98C)

    def test_row_negative_control(self):
        # The same 0x021FB384 site encoded from the compiler's BL placeholder
        # (arm=False) must not reproduce the image's BLX word.
        first, second = encode_thumb_branch(0x021FB38E, 0x02002480, -4, False)
        self.assertEqual((first, second), (0xF607, 0xF877))
        self.assertNotEqual((first, second), (0xF607, 0xE878))
        self.assertEqual(second & 0xD000, 0xD000)  # BL keeps bit 12 set

    def test_ov006_blx_marker_is_arm_only(self):
        # The same site encoded as Thumb (BL) must not produce the image word: the
        # expansion has to follow the measured callee mode, not a default.
        first, second = encode_thumb_branch(0x021EDA60, 0x02026144, -4, False)
        self.assertNotEqual((first, second), (0xF638, 0xEB70),
                            'a Thumb expansion must not reproduce an ARM-word site')
        self.assertEqual(second & 0xF800, 0xF800)

    def test_bias_is_not_applied_twice(self):
        # A +4 error is the regression this guards: the same inputs must not produce
        # a word that decodes four bytes short.
        first, second = encode_thumb_branch(0x021F7212, 0x021F52CC, -4, False)
        self.assertEqual((first, second), (0xF7FE, 0xF85B))
        wrong_first, wrong_second = encode_thumb_branch(0x021F7212, 0x021F52C8, -4, False)
        self.assertNotEqual(((first, second)), ((wrong_first, wrong_second)),
                            'a target four bytes lower must encode differently')


if __name__ == '__main__':
    unittest.main()
