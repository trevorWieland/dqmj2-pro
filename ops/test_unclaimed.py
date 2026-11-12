"""Tests for ops/unclaimed.py — source-first screening of ledger rows."""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import unclaimed


def row(address, module='ov000', size=16, mode='arm', matched=False, symbol=None):
    return {
        'id': f'{module}/{address}',
        'address': address,
        'module': module,
        'mode': mode,
        'bytes': size,
        'symbol': symbol or f'func_{module}_{address[2:]}',
        'states': {'functionMatched': matched},
    }


class Fixture:
    def __init__(self, rows, files):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / 'src').mkdir()
        (self.root / 'ledger').mkdir()
        for relative, text in files.items():
            path = self.root / 'src' / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        with (self.root / 'ledger/functions.jsonl').open('w', encoding='utf-8') as stream:
            for item in rows:
                stream.write(json.dumps(item) + '\n')

    def close(self):
        self._tmp.cleanup()


class UnclaimedTest(unittest.TestCase):
    def fixture(self, rows, files):
        fixture = Fixture(rows, files)
        self.addCleanup(fixture.close)
        return fixture.root

    def status(self, root, address, module='ov000', include_inverse=False):
        records, summary = unclaimed.classify(root)
        shown = unclaimed.displayed(records, include_inverse)
        return {(record['key'], record['module']): record for record in shown}, summary

    def test_symbol_definition_claims_row(self):
        root = self.fixture(
            [row('0x021e0478')],
            {'ov000/native_ov000_021e0478.c': 'void native_ov000_021e0478(void)\n{\n}\n'})
        shown, summary = self.status(root, '0x021e0478')
        self.assertEqual(summary['claimed'], 1)
        self.assertEqual(shown, {})

    def test_address_named_file_with_semantic_symbol_claims_row(self):
        # The shape the ledger-only screen missed: the file names the address, the
        # symbol carries only a semantic name.
        root = self.fixture(
            [row('0x020685bc', module='main', size=12)],
            {'main/r1/native_main_020685bc.c':
             'void saved_identity_profile_pointer(void) { return; }\n'})
        shown, summary = self.status(root, '0x020685bc', module='main')
        self.assertEqual(summary['claimed'], 1)
        self.assertEqual(shown, {})

    def test_wrapped_header_is_a_definition(self):
        root = self.fixture(
            [row('0x021e02b0')],
            {'ov000/native_ov000_021e02b0.c':
             's32 native_ov000_021e02b0(Actor *actor, ParameterBlock *first,\n'
             '                          ParameterBlock *second)\n'
             '{\n    return 1;\n}\n'})
        _, summary = self.status(root, '0x021e02b0')
        self.assertEqual(summary['claimed'], 1)

    def test_extern_declaration_is_not_a_claim(self):
        root = self.fixture(
            [row('0x021e0478')],
            {'ov000/context.h': 'extern void native_ov000_021e0478(void);\n'})
        shown, summary = self.status(root, '0x021e0478')
        self.assertEqual(summary['claimed'], 0)
        self.assertEqual(shown[('021e0478', 'ov000')]['status'], 'unclaimed')
        self.assertEqual(shown[('021e0478', 'ov000')]['confidence'], 'medium')

    def test_prototype_is_not_a_claim(self):
        root = self.fixture(
            [row('0x021e0478')],
            {'ov000/header.c': 'void native_ov000_021e0478(void);\n'})
        _, summary = self.status(root, '0x021e0478')
        self.assertEqual(summary['claimed'], 0)

    def test_comment_mention_is_not_a_claim_but_lowers_confidence(self):
        root = self.fixture(
            [row('0x021e0478')],
            {'ov000/caller.c': '/* calls 0x021e0478 later */\nint caller(void) { return 0; }\n'})
        shown, _ = self.status(root, '0x021e0478')
        self.assertEqual(shown[('021e0478', 'ov000')]['mentions'], 1)
        self.assertEqual(shown[('021e0478', 'ov000')]['confidence'], 'medium')

    def test_unmentioned_row_is_high_confidence(self):
        root = self.fixture([row('0x021e9999')], {'ov000/notes.c': 'int unrelated(void)\n{\n}\n'})
        shown, _ = self.status(root, '0x021e9999')
        self.assertEqual(shown[('021e9999', 'ov000')]['confidence'], 'high')

    def test_asm_global_label_claims_row(self):
        root = self.fixture(
            [row('0x01ff8000', module='itcm')],
            {'itcm/hardware/native_itcm_01ff8000.s':
             '\t.global native_itcm_01ff8000\n'
             'native_itcm_01ff8000:\n\tbx lr\n'})
        _, summary = self.status(root, '0x01ff8000', module='itcm')
        self.assertEqual(summary['claimed'], 1)

    def test_module_scope_keeps_other_overlay_unclaimed(self):
        # Every overlay loads at 0x021d7240: src/ov000 must not claim an ov004 row.
        root = self.fixture(
            [row('0x021d813c', module='ov000', size=420),
             row('0x021d813c', module='ov004', size=44)],
            {'ov000/native_ov000_021d813c.c': 'void native_ov000_021d813c(void)\n{\n}\n'})
        records, _ = unclaimed.classify(root)
        by_module = {record['module']: record['status'] for record in records}
        self.assertEqual(by_module['ov000'], 'claimed')
        self.assertEqual(by_module['ov004'], 'unclaimed')

    def test_data_definition_is_reported_separately(self):
        root = self.fixture(
            [row('0x0224536c', size=4)],
            {'ov000/data.c': 's32 native_data_ov000_0224536c = 0;\n'})
        _, summary = self.status(root, '0x0224536c')
        self.assertEqual(summary['dataClaimed'], 1)
        self.assertEqual(summary['claimed'], 0)

    def test_matched_without_claim_is_inverse_not_unclaimed(self):
        root = self.fixture([row('0x021e0478', matched=True)],
                            {'ov000/unrelated.c': 'int unrelated(void)\n{\n}\n'})
        shown, summary = self.status(root, '0x021e0478')
        self.assertEqual(summary['inverse'], 1)
        self.assertEqual(summary['unclaimed'], 0)
        self.assertEqual(shown, {})
        shown_inverse, _ = self.status(root, '0x021e0478', include_inverse=True)
        self.assertEqual(shown_inverse[('021e0478', 'ov000')]['confidence'], 'low')

    def test_summary_counts_bytes(self):
        root = self.fixture(
            [row('0x021e0478', size=32), row('0x021e0479', size=12)],
            {'ov000/native_ov000_021e0478.c': 'void native_ov000_021e0478(void)\n{\n}\n'})
        _, summary = self.status(root, '0x021e0478')
        self.assertEqual(summary['claimed'], 1)
        self.assertEqual(summary['unclaimed'], 1)
        self.assertEqual(summary['unclaimedBytes'], 12)

    def test_check_addresses_exit_status(self):
        root = self.fixture(
            [row('0x021e0478')],
            {'ov000/native_ov000_021e0478.c': 'void native_ov000_021e0478(void)\n{\n}\n'})
        with redirect_stdout(io.StringIO()):
            blocked = unclaimed.main(['--root', str(root), '--check-addresses',
                                      'ov000:0x021e0478'])
        with redirect_stdout(io.StringIO()):
            clear = unclaimed.main(['--root', str(root), '--check-addresses',
                                    'ov000:0x021e9999'])
        self.assertEqual(blocked, 1)
        self.assertEqual(clear, 0)

    def test_check_addresses_batch_file(self):
        root = self.fixture(
            [row('0x021e0478')],
            {'ov000/native_ov000_021e0478.c': 'void native_ov000_021e0478(void)\n{\n}\n'})
        batch = root / 'batch.txt'
        batch.write_text('# lane ov000\nov000:0x021e0478\nov000:0x021e9999\n', encoding='utf-8')
        with redirect_stdout(io.StringIO()):
            status = unclaimed.main(['--root', str(root), '--address-file', str(batch),
                                     '--check-addresses'])
        self.assertEqual(status, 1)

    def test_parse_target(self):
        self.assertEqual(unclaimed.parse_target('0x021E0478'), (None, '021e0478'))
        self.assertEqual(unclaimed.parse_target('main:0x020685bc'), ('main', '020685bc'))
        self.assertEqual(unclaimed.parse_target('# comment'), (None, None))
        with self.assertRaises(ValueError):
            unclaimed.parse_target('main:not-an-address')
        with self.assertRaises(ValueError):
            unclaimed.parse_target('nonsense:0x021e0478')


if __name__ == '__main__':
    unittest.main()
