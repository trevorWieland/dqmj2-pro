"""Checks for the whole-image link gate that need no private inputs.

The link and the byte diff themselves require the extracted module image and the address
ledger, which arrive only through the pinned private-input bundle; CI runs those when the
bundle is available.  Everything here runs on a public checkout: the section table, the
linker-command-file renderer, the alignment rule, the diagnostic parser and the diff
attribution logic (on synthetic bytes).
"""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import whole_image_link as W

ROOT = Path(__file__).resolve().parent.parent


class LayoutTest(unittest.TestCase):
    def test_section_table_derives_the_declared_image_size(self):
        layout = W.load_layout(ROOT)
        report = W.layout_report(ROOT)
        self.assertEqual(report['base'], '0x02000000')
        self.assertEqual(report['imageBytes'], 930560)
        self.assertEqual(report['textBytes'], 868320)
        self.assertEqual(report['bssBytes'], 999232)
        # The initialised image ends where .bss starts.
        self.assertEqual(layout['byName']['data']['end'], layout['byName']['bss']['start'])
        self.assertEqual(layout['byName']['ctor']['start'], layout['byName']['ctor']['end'])

    def test_overlapping_sections_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'config' / 'arm9'
            path.mkdir(parents=True)
            (path / 'delinks.txt').write_text(
                '    .text       start:0x02000000 end:0x02000100 kind:code align:32\n'
                '    .rodata     start:0x02000080 end:0x02000200 kind:rodata align:4\n'
                '    .ctor       start:0x02000200 end:0x02000200 kind:rodata align:4\n'
                '    .data       start:0x02000200 end:0x02000300 kind:data align:32\n'
                '    .bss        start:0x02000300 end:0x02000400 kind:bss align:32\n',
                encoding='utf-8')
            with self.assertRaises(W.WholeImageError):
                W.load_layout(folder)

    def test_missing_section_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'config' / 'arm9'
            path.mkdir(parents=True)
            (path / 'delinks.txt').write_text(
                '    .text       start:0x02000000 end:0x02000100 kind:code align:32\n',
                encoding='utf-8')
            with self.assertRaises(W.WholeImageError):
                W.load_layout(folder)


class LcfTest(unittest.TestCase):
    def layout(self):
        return dict(sections=[
            dict(name='text', start=0x02000000, end=0x02000100, kind='code', align=32),
            dict(name='rodata', start=0x02000100, end=0x02000180, kind='rodata', align=4),
            dict(name='ctor', start=0x02000180, end=0x02000180, kind='rodata', align=4),
            dict(name='data', start=0x02000180, end=0x02000200, kind='data', align=32),
            dict(name='bss', start=0x02000200, end=0x02000300, kind='bss', align=32),
        ], byName={name: dict(name=name, start=start, end=end, kind=kind, align=align)
                   for name, start, end, kind, align in (
                       ('text', 0x02000000, 0x02000100, 'code', 32),
                       ('rodata', 0x02000100, 0x02000180, 'rodata', 4),
                       ('ctor', 0x02000180, 0x02000180, 'rodata', 4),
                       ('data', 0x02000180, 0x02000200, 'data', 32),
                       ('bss', 0x02000200, 0x02000300, 'bss', 32))})

    def test_every_region_and_boundary_is_rendered(self):
        text = W.render_lcf(self.layout(), [
            dict(address=0x02000000, object='aaaaaaaaaa.o', symbol='first', size=4, mode='arm'),
            dict(address=0x020000f6, object='bbbbbbbbbb.o', symbol='second', size=4, mode='thumb'),
        ], 'arm9.bin', dict(delinksSha256='0' * 64))
        self.assertIn('ARM9 : ORIGIN = 0x02000000 > arm9.bin', text)
        self.assertIn('BSS  : ORIGIN = 0x02000200', text)
        self.assertIn('ALIGNALL(2);', text)
        self.assertIn('. = 0x02000000; aaaaaaaaaa.o (.text)', text)
        self.assertIn('. = 0x020000f6; bbbbbbbbbb.o (.text)', text)
        self.assertIn('. = 0x02000100;', text)
        self.assertIn('ARM9_TEXT_START = .;', text)
        self.assertIn('ARM9_TEXT_END = .;', text)
        self.assertIn('ARM9_RODATA_START = .;', text)
        self.assertIn('ARM9_CTOR_START = .;', text)
        self.assertIn('ARM9_DATA_START = .;', text)
        self.assertIn('ARM9_BSS_END = .;', text)
        self.assertIn('* (.rodata)', text)
        self.assertIn('* (.data)', text)
        self.assertIn('* (.bss)', text)
        # The written length is fixed by the .data end assignment, not by a length option.
        self.assertIn('. = 0x02000200;', text)

    def test_provenance_names_every_source(self):
        text = W.render_lcf(self.layout(), [], 'arm9.bin', dict(delinksSha256='a' * 64))
        for token in (W.DELINKS_PATH, W.HEADER_PATH, W.LEDGER_PATH, W.SYMBOLS_PATH,
                      'GENERATED FILE', 'dsd lcf'):
            self.assertIn(token, text)

    def test_alignment_rule(self):
        self.assertEqual(W.natural_alignment(0x02000000), 4)
        self.assertEqual(W.natural_alignment(0x020000f6), 2)
        self.assertEqual(W.natural_alignment(0x0200000c), 4)
        self.assertEqual(W.natural_alignment(0x02000003), 1)


class DiagnosticsTest(unittest.TestCase):
    def test_undefined_symbols_are_read_from_linker_text(self):
        text = ('### mwldarm.exe Linker Error:\n'
                '#   Undefined : "__startup"\n'
                '#   Undefined : native_fn_02097488\n'
                '#   Undefined : native_fn_02097488\n')
        self.assertEqual(W.undefined_symbols(text),
                         ['__startup', 'native_fn_02097488'])

    def test_address_suffix_rule(self):
        match = W.ADDRESS_SUFFIX.search('native_fn_02097488')
        self.assertEqual(int(match.group(1), 16), 0x02097488)
        self.assertEqual(W.ADDRESS_SUFFIX.search('native_data_main_020dd680').group(1), '020dd680')
        self.assertIsNone(W.ADDRESS_SUFFIX.search('strncmp'))


class DiffTest(unittest.TestCase):
    """Attribution is exercised on synthetic bytes so no module image is needed."""

    def layout(self):
        def section(name, start, end, kind):
            return dict(name=name, start=start, end=end, kind=kind, align=4)
        sections = [section('text', 0x02000000, 0x02000010, 'code'),
                    section('rodata', 0x02000010, 0x02000010, 'rodata'),
                    section('ctor', 0x02000010, 0x02000010, 'rodata'),
                    section('data', 0x02000010, 0x02000020, 'data'),
                    section('bss', 0x02000020, 0x02000030, 'bss')]
        return dict(sections=sections, byName={item['name']: item for item in sections})

    def test_differences_are_attributed_to_the_right_owner(self):
        layout = self.layout()
        spans = [dict(address=0x02000000, extent=4, symbol='matched', mode='arm', size=4,
                      source='src/a.c'),
                 dict(address=0x0200000c, extent=2, symbol='second', mode='thumb', size=2,
                      source='src/b.c')]
        ledger = [dict(address=0x02000000, size=4, symbol='matched', mode='arm', source='src/a.c'),
                  dict(address=0x02000004, size=4, symbol='stubbed', mode='arm', source=''),
                  dict(address=0x02000008, size=4, symbol='other', mode='arm', source=''),
                  dict(address=0x0200000c, size=2, symbol='second', mode='thumb', source='src/b.c')]
        original = bytearray(0x20)
        produced = bytearray(0x20)
        # reconstructed span differs -> gate failure, attributed to "matched"
        produced[0] = 1
        # stub row differs -> reported, not a failure
        produced[4] = 2
        # text hole (0x0e..0x10) differs -> reported as a hole
        produced[0x0e] = 3
        # data window differs -> reported separately
        produced[0x18] = 4
        result = W.diff_image(bytes(produced), bytes(original), layout, spans, ledger)
        self.assertEqual(result['reconstructedDifferingBytes'], 1)
        self.assertEqual(result['stubDifferingBytes'], 1)
        self.assertEqual(result['gapDifferingBytes'], 1)
        self.assertEqual(result['dataWindowDifferingBytes'], 1)
        self.assertEqual(result['mismatchedFunctions'], 1)
        self.assertEqual(result['mismatched'][0]['symbol'], 'matched')
        self.assertEqual(result['mismatched'][0]['differing'], 1)
        self.assertEqual(result['differingBytes'], 4)

    def test_identical_images_have_no_differences(self):
        layout = self.layout()
        original = bytes(range(0x20))
        result = W.diff_image(original, original, layout, [], [])
        self.assertEqual(result['differingBytes'], 0)
        self.assertEqual(result['reconstructedDifferingBytes'], 0)

    def test_size_mismatch_is_rejected(self):
        with self.assertRaises(W.WholeImageError):
            W.diff_image(b'\x00' * 8, b'\x00' * 16, self.layout(), [], [])


class InputGateTest(unittest.TestCase):
    def test_missing_inputs_are_reported_not_raised(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertFalse(W.inputs_present(folder))
            self.assertEqual(W.install_inputs(folder, 'private-inputs')['status'], 'absent')
            self.assertEqual(W.install_inputs(folder, None)['status'], 'not-requested')

    def test_cli_check_layout_runs_on_a_public_checkout(self):
        process = subprocess.run([os.sys.executable, str(Path(W.__file__)),
                                  '--root', str(ROOT), '--check-layout'],
                                 capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr[-2000:])
        report = json.loads(process.stdout)
        self.assertEqual(report['status'], 'layout-ok')
        self.assertEqual(report['imageBytes'], 930560)


if __name__ == '__main__':
    unittest.main()
