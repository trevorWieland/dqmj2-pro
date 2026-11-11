"""Pinned regression tests for the relocation patcher's branch-mode selection.

The compiler always leaves a Thumb ``BL`` placeholder plus an
``R_ARM_THM_CALL`` relocation, including when the callee is ARM. The measured
image decides: an ARM callee is a ``BLX`` immediate. ``form_search.relocate``
therefore has to resolve the target from project evidence, never from the
placeholder halfword.

The three rows are the ones that exposed the bug:

* ``0x021FB384`` (24 B) -- one call to ARM ``0x02002480``; the image word at
  ``+0xA`` is ``07 F6 78 E8``.
* ``0x021FF02C`` (48 B) -- one call to ARM ``0x0200616C``; the image word at
  ``+0x1A`` is ``07 F6 92 E8``.
* ``0x02203EBC`` (48 B) -- a Thumb target that must stay a ``BL``; it is the
  negative control for "BLX everywhere".

    python ops/test_form_search.py
"""
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import form_search  # noqa: E402
from thumb_branch import encode  # noqa: E402


def object_with(offset, first, second, length=64):
    """A fake compiled object: zero bytes with a BL placeholder at ``offset``."""
    text = bytearray(length)
    struct.pack_into('<HH', text, offset, first, second)
    return bytes(text)


class RelocateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modes = form_search.TargetModes(form_search.ROOT)

    def patch(self, site, offset, target, placeholder, addend=-4, modes=None, arm=None):
        text = object_with(offset, *placeholder)
        relocations = [(offset, 10, f'native_fn_{target:08x}', addend)]
        return form_search.relocate(text, site, relocations, {}, modes=modes, arm=arm)

    def test_021fb384_blx_site(self):
        # Object says BL (0xF877); the ledger says the callee is ARM, so the
        # patched word must be the image's BLX (07 F6 78 E8).
        patched = self.patch(0x021FB384, 0xA, 0x02002480, (0xF607, 0xF877),
                             modes=self.modes)
        self.assertEqual(patched[0xA:0xE].hex(), '07f678e8')

    def test_021ff02c_blx_site(self):
        patched = self.patch(0x021FF02C, 0x1A, 0x0200616C, (0xF607, 0xF8A7),
                             modes=self.modes)
        self.assertEqual(patched[0x1A:0x1E].hex(), '07f692e8')

    def test_02203ebc_thumb_target_stays_bl(self):
        # 0x02203EBC is a Thumb row; a call to it must remain a BL.
        mode, evidence = self.modes.resolve(0x02203EBC)
        self.assertEqual((mode, evidence), ('thumb', 'ledger-address'))
        patched = self.patch(0x021F7B9C, 0x4, 0x02203EBC, (0xF00C, 0xF98C),
                             modes=self.modes)
        self.assertEqual(patched[0x4:0x8].hex(), '0cf08cf9')
        second = int.from_bytes(patched[0x6:0x8], 'little')
        self.assertEqual(second & 0xF800, 0xF800)  # BL marker bit 12 set

    def test_negative_control_bl_does_not_match(self):
        # Without target evidence the old placeholder rule yields a BL; it must
        # not reproduce the ARM site, which is exactly the bug being fixed.
        patched = self.patch(0x021FB384, 0xA, 0x02002480, (0xF607, 0xF877),
                             modes=None)
        self.assertEqual(patched[0xA:0xE].hex(), '07f677f8')
        self.assertNotEqual(patched[0xA:0xE].hex(), '07f678e8')

    def test_explicit_arm_override_wins(self):
        # The caller hint survives for callers that already know the target.
        patched = self.patch(0x021FB384, 0xA, 0x02002480, (0xF607, 0xF877),
                             modes=self.modes, arm=True)
        self.assertEqual(patched[0xA:0xE].hex(), '07f678e8')
        patched = self.patch(0x021FB384, 0xA, 0x02002480, (0xF607, 0xF877),
                             modes=self.modes, arm=False)
        self.assertEqual(patched[0xA:0xE].hex(), '07f677f8')

    def test_ledger_evidence_order(self):
        self.assertEqual(self.modes.resolve(0x02002480)[0], 'arm')
        self.assertEqual(self.modes.resolve(0x02002480, 'func_02002480')[0], 'arm')
        # A target inside a measured ARM extent inherits that row's mode.
        self.assertEqual(self.modes.resolve(0x020260E8),
                         ('arm', 'ledger-extent'))
        # itcm has only ARM rows in the ledger; a target in an uncovered gap
        # still resolves through the module-level rule.
        self.assertEqual(self.modes.resolve(0x01FFBB10), ('arm', 'module-mode'))

    def test_unknown_target_falls_back_to_bl(self):
        # No ledger, no module match, no accepted source: BL is the safe default.
        with tempfile.TemporaryDirectory() as directory:
            modes = form_search.TargetModes(directory)
            patched = self.patch(0x021FB384, 0xA, 0x02FFFFFF, (0xF607, 0xF877),
                                 modes=modes)
        first, second = encode(0x021FB38E, 0x02FFFFFF, -4, arm=False)
        self.assertEqual(patched[0xA:0xE], struct.pack('<HH', first, second))


class EncodeTests(unittest.TestCase):
    def test_blx_aligned_base(self):
        self.assertEqual(encode(0x021FB38E, 0x02002480, -4, arm=True),
                         (0xF607, 0xE878))
        self.assertEqual(encode(0x021FB38E, 0x02002480, -4, arm=False),
                         (0xF607, 0xF877))

    def test_marker_override(self):
        self.assertEqual(encode(0x021FB38E, 0x02002480, -4, mode='arm'),
                         (0xF607, 0xE878))
        self.assertEqual(encode(0x021FB38E, 0x02002480, -4, mode='thumb'),
                         (0xF607, 0xF877))


if __name__ == '__main__':
    unittest.main()
