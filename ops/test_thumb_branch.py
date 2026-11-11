"""Pinned regression cases for ops/thumb_branch.py.

Each case is a real call site from the measured ov006 image: the site address, the
callee the original linker resolved, the relocation addend, and the two image
halfwords. Three BLX-immediate sites and two BL sites, so both branch bases and
both markers are covered.

    python ops/test_thumb_branch.py
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from thumb_branch import encode, marker_mode  # noqa: E402


class ThumbBranchTests(unittest.TestCase):
    def check(self, site, target, arm, first, second, addend=-4):
        got = encode(site, target, addend, arm=arm)
        self.assertEqual((hex(got[0]), hex(got[1])), (hex(first), hex(second)),
                         f'site {site:#010x} -> {target:#010x} (arm={arm})')

    def test_blx_immediate_sites(self):
        # Three measured BLX-immediate sites: the second halfword carries 0xE800.
        self.check(0x021EDA60, 0x02026144, True, 0xF638, 0xEB70)
        self.check(0x021EDB3E, 0x02006B7C, True, 0xF619, 0xE81E)
        self.check(0x021EDCFE, 0x0200F48C, True, 0xF621, 0xEBC6)

    def test_bl_sites(self):
        # Two measured BL sites (Thumb callee): the marker stays 0xF800.
        self.check(0x021F7212, 0x021F52CC, False, 0xF7FE, 0xF85B)
        self.check(0x02091C52, 0x02093824, False, 0xF001, 0xFDE7)

    def test_marker_is_second_halfword(self):
        # A BLX site read from its image bytes must report 'arm'; reading the first
        # halfword instead would always report 'thumb'.
        blx = bytes.fromhex('38f670eb')
        bl = bytes.fromhex('fef75bf8')
        self.assertEqual(marker_mode(blx, 0), 'arm')
        self.assertEqual(marker_mode(bl, 0), 'thumb')

    def test_blx_marker_with_j1_clear(self):
        # BLX clears bit 12; J1 is free. 0xC8xx is a valid BLX with J1 == 0 and
        # the old (second & 0xF800) == 0xE800 test misclassified it as BL.
        self.assertEqual(marker_mode(bytes.fromhex('38f600c8'), 0), 'arm')
        first, second = encode(0x021FB38E, 0x02002480, -4, mode='arm')
        self.assertEqual(second & 0xD000, 0xC000)

    def test_mode_override_matches_arm_flag(self):
        self.assertEqual(encode(0x021FB38E, 0x02002480, -4, mode='arm'),
                         encode(0x021FB38E, 0x02002480, -4, arm=True))
        self.assertEqual(encode(0x021FB38E, 0x02002480, -4, mode='thumb'),
                         encode(0x021FB38E, 0x02002480, -4, arm=False))
        with self.assertRaises(ValueError):
            encode(0x021FB38E, 0x02002480, -4, mode='arm7')

    def test_blx_base_is_aligned(self):
        # BLX relative to Align(PC+4,4): the same inputs must not encode as a BL.
        arm_words = encode(0x021EDA60, 0x02026144, -4, arm=True)
        thumb_words = encode(0x021EDA60, 0x02026144, -4, arm=False)
        self.assertEqual(arm_words, (0xF638, 0xEB70))
        self.assertNotEqual(thumb_words, arm_words)
        self.assertEqual(thumb_words[1] & 0xF800, 0xF800)


if __name__ == '__main__':
    unittest.main()
