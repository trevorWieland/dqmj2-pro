"""Tests for public_tools/scr_asm.py against the matched opcode table."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scr_asm
import scr_disasm

ROOT = Path(__file__).resolve().parent.parent
DECODER = ROOT / scr_disasm.DECODER_SOURCE


@unittest.skipUnless(DECODER.is_file(), 'matched decoder source not present')
class AssembleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.table = scr_disasm.parse_table(DECODER)
        cls.mnemonics = scr_asm.build_mnemonics(cls.table)

    def assemble(self, text):
        entries = scr_asm.parse_listing(text)
        return scr_asm.assemble(entries, self.mnemonics)

    def test_directives_and_opcodes(self):
        walk = next(name for name in self.mnemonics if name.startswith('walk_0'))
        text_opcode = next(name for name in self.mnemonics if name.startswith('text_'))
        data, undecoded, errors = self.assemble(
            '0x00000000  %02x           %s\n'
            '0x00000001  e3 1c 05     .escape_skip 0x05\n'
            '0x00000004  e3 1b        .block_end\n' % (self.mnemonics[walk], walk))
        self.assertEqual(errors, [])
        self.assertEqual(undecoded, [])
        self.assertEqual(data.hex(), '%02xe31c05e31b' % self.mnemonics[walk])

    def test_refuses_undecoded(self):
        data, undecoded, errors = self.assemble('0x00000000  ff           .byte 0xff   ; unknown opcode\n')
        self.assertEqual(data, b'\xff')
        self.assertEqual(undecoded, [0])

    def test_refuses_unknown_statement(self):
        data, undecoded, errors = self.assemble('0x00000000  00           not_a_statement\n')
        self.assertTrue(errors)
        self.assertIn('unknown statement', errors[0])

    def test_rejects_byte_column_mismatch(self):
        text_opcode = next(name for name in self.mnemonics if name.startswith('text_'))
        data, undecoded, errors = self.assemble(
            '0x00000000  %02x           %s\n' % ((self.mnemonics[text_opcode] + 1) & 0xff, text_opcode))
        self.assertTrue(errors)
        self.assertIn('listed bytes', errors[0])

    def test_ignores_coverage_comment(self):
        data, undecoded, errors = self.assemble(
            '0x00000000  00           .end\n'
            '# coverage: 1 byte(s) read, decoded 1 (100.0%), undecoded 0\n')
        self.assertEqual(data, b'\x00')
        self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main()
