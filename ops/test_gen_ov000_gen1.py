"""Unit tests for the ov000 generation-1 spelling and decoding rules.

Run with ``python ops/test_gen_ov000_gen1.py``.  The heavy end-to-end gate is
``ops/verify_ov000_gen1.py``; these tests pin the small rules that cost several
compile attempts in the first pass.
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'public_tools'))

import gen_ov000_gen1 as generator  # noqa: E402


class SpineTests(unittest.TestCase):
    def test_condition_is_split_after_the_width(self):
        self.assertEqual(generator.split_condition('ldrsbeq'), ('ldrsb', 'eq'))
        self.assertEqual(generator.split_condition('ldrbeq'), ('ldrb', 'eq'))
        self.assertEqual(generator.split_condition('strhne'), ('strh', 'ne'))
        self.assertEqual(generator.split_condition('moveq'), ('mov', 'eq'))
        self.assertEqual(generator.split_condition('movs'), ('movs', ''))

    def test_width_condition_is_reordered_before_the_width(self):
        self.assertEqual(generator.reorder_width('ldrbeq'), 'ldreqb')
        self.assertEqual(generator.reorder_width('ldrsbne'), 'ldrnesb')
        self.assertEqual(generator.reorder_width('ldrshle'), 'ldrlesh')
        self.assertEqual(generator.reorder_width('strhge'), 'strgeh')
        self.assertEqual(generator.reorder_width('ldreq'), 'ldreq')
        self.assertIsNone(generator.reorder_width('ldrb'))

    def test_ldm_condition_is_reordered_before_the_mode(self):
        self.assertEqual(generator.reorder_ldm('ldm'), 'ldmia')
        self.assertEqual(generator.reorder_ldm('ldmne'), 'ldmneia')
        self.assertEqual(generator.reorder_ldm('ldmiane'), 'ldmneia')
        self.assertEqual(generator.reorder_ldm('stmdbne'), 'stmnedb')
        self.assertEqual(generator.reorder_ldm('stmdb'), 'stmdb')
        self.assertIsNone(generator.reorder_ldm('ldrb'))

    def test_pool_words_choose_module_scoped_symbols(self):
        # ov000 code address -> function symbol; ov000 storage -> data symbol.
        self.assertEqual(generator.pool_expression(0x021D7EF8, 0x021D7240),
                         'native_fn_021d7ef8')
        self.assertEqual(generator.pool_expression(0x02236AC8, 0x021D7240),
                         'native_data_02236ac8')
        # main-RAM storage below the overlay base.
        self.assertEqual(generator.pool_expression(0x020DE2D8, 0x021D7240),
                         'native_data_020de2d8')
        # A float constant is not an address.
        self.assertEqual(generator.pool_expression(0x3F800000, 0x021D7240), '0x3f800000')

    def test_rotated_arm_immediate_is_decoded_not_read_as_a_byte(self):
        # mov r0, #0x04000000 is imm8=1, rotate=3; a generator that copies the low
        # byte emits 1 and differs by two bytes.  Capstone is the decoder here.
        word = 0xE3A00301
        [insn] = list(generator.MD.disasm(word.to_bytes(4, 'little'), 0))
        self.assertIn('#0x4000000', insn.op_str)


class EmitterTests(unittest.TestCase):
    def row(self, address):
        return generator.LEDGER[address]

    def test_asm_row_keeps_the_pool_out_of_the_body(self):
        text = generator.emit_asm(self.row(0x021DFD80))
        # The pool word 0x0222ebd8 is a symbol, not an eoreq instruction.
        self.assertIn('ldr r0, =native_data_0222ebd8', text)
        self.assertNotIn('eoreq', text)
        self.assertIn('ldmia sp!, {r4, pc}', text)
        self.assertIn('bl native_fn_02042fec', text)

    def test_asm_row_rewrites_conditional_width_and_block_transfers(self):
        self.assertIn('ldreqb', generator.emit_asm(self.row(0x021F95C8)))
        self.assertIn('ldmneia', generator.emit_asm(self.row(0x021FB8A8)))

    def test_f4_template_uses_signed_casts(self):
        text = generator.render_f4(self.row(0x0221221C))
        self.assertIn('native_fn_02211104((s16)a, (s16)b)', text)
        self.assertIn('native_fn_02211644(t, c)', text)

    def test_f7_template_decodes_offsets_and_the_four_argument_variant(self):
        three = generator.render_f7(self.row(0x02213E7C))
        self.assertIn('native_data_02243e3c + index * 0x10c', three)
        self.assertIn('e[0x103] = *(u32 *)(p + 0x9c + (slot << 3))', three)
        self.assertIn('native_fn_02041474(u8 *, u8 *, u32)', three)
        four = generator.render_f7(self.row(0x02213E10))
        self.assertIn('native_fn_02041268(e, p + 0x60 + (slot << 4), 0, 0)', four)
        self.assertIn('e[0x102]', four)

    def test_f2_and_f1_templates_decode_the_row_parameters(self):
        f2 = generator.render_f2(self.row(0x021EB654))
        self.assertIn('native_data_0222ee18', f2)
        self.assertIn('n = 8;', f2)
        self.assertIn('native_fn_02045680(2);', f2)
        f1 = generator.render_f1(self.row(0x021EBD88))
        self.assertIn('native_data_020de2d8', f1)
        self.assertIn('native_data_02236ac8', f1)
        self.assertIn('while (++i < 0x15)', f1)
        self.assertIn('stride += 3;', f1)


if __name__ == '__main__':
    unittest.main()
