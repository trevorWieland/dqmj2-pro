"""Regression tests for the jump-table carrier lane and its data directives.

The lane exists because mwccarm's inline assembler has no general data
directive. These tests pin what it does accept and what it rejects, so a future
lane does not re-learn the limit by trial:

* ``dcd <32-bit value>`` is the only data spelling a mwccarm ``asm`` body
  accepts; ``.word``, ``.long``, ``.4byte``, ``.byte``, ``.hword``, ``.short``,
  ``dc32``, ``dc.b``, ``dc.w`` and ``dc.l`` are each rejected;
* mwasmarm accepts ``.word``, ``.hword``, ``.short`` and ``.byte`` (with section
  padding after the symbol), and rejects ``dc.*``, ``dcd``;
* the committed lane has exactly one address-named file per plan row, the plan's
  rows are ledger rows whose form matches their instruction set, and every plan
  table extent is reproduced by the scanner.

    python -m unittest ops.test_jumptable_carrier
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import transcribe_data_rows  # noqa: E402

CC = ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'
AS = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe'
PLAN = ROOT / 'ops/jumptable_carrier_plan.json'
LANE = ROOT / 'src/verified_assembly/20261112_jumptable_carrier'
LEDGER = ROOT / 'ledger/functions.jsonl'
IMAGE = ROOT / 'extract/arm9_overlays/ov006.bin'
MAIN_IMAGE = ROOT / 'extract/arm9/arm9.bin'
FLAGS = ['-O2', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc',
         'arm946e', '-gccext,on', '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions',
         'off', '-RTTI', 'off', '-interworking', '-w', 'off', '-sym', 'on',
         '-gccinc', '-nolink', '-msgstyle', 'gcc', '-opt', 'speed']


def have_compilers():
    return CC.is_file() and AS.is_file()


def compile_asm(body, work):
    source = work / 'probe.c'
    obj = work / 'probe.o'
    source.write_text('asm int probe(void)\n{\n%s\n    bx lr\n}\n' % body,
                      encoding='ascii')
    env = {key: value for key, value in os.environ.items() if key != 'LM_LICENSE_FILE'}
    return subprocess.run([str(CC), *FLAGS, '-c', str(source), '-o', str(obj)],
                          capture_output=True, text=True, env=env), obj


def assemble(text, work):
    source = work / 'probe.s'
    obj = work / 'probe.o'
    source.write_text(text, encoding='ascii')
    env = {key: value for key, value in os.environ.items() if key != 'LM_LICENSE_FILE'}
    return subprocess.run([str(AS), '-proc', 'arm5TE', str(source), '-o', str(obj)],
                          capture_output=True, text=True, env=env), obj


def diagnostics(process):
    return (process.stdout + process.stderr).strip()


class AsmDataDirectiveTests(unittest.TestCase):
    def setUp(self):
        if not have_compilers():
            self.skipTest('the pinned compilers are not present')
        self._directory = tempfile.TemporaryDirectory(prefix='carrier-test-')
        self.work = Path(self._directory.name)

    def tearDown(self):
        self._directory.cleanup()

    def test_dcd_is_the_accepted_asm_data_directive(self):
        process, obj = compile_asm('    dcd 0x12345678', self.work)
        self.assertEqual(process.returncode, 0, diagnostics(process))
        text, unused_defined, relocations = form_search.read_object(obj)
        self.assertEqual(text[:4], bytes.fromhex('78563412'))
        self.assertEqual(relocations, [])

    def test_dcd_carries_a_relocatable_address(self):
        source = self.work / 'reloc.c'
        obj = self.work / 'reloc.o'
        source.write_text(
            'extern unsigned char native_data_0202562c[];\n'
            'asm int probe(void)\n{\n    dcd native_data_0202562c\n    bx lr\n}\n',
            encoding='ascii')
        env = {key: value for key, value in os.environ.items() if key != 'LM_LICENSE_FILE'}
        process = subprocess.run([str(CC), *FLAGS, '-c', str(source), '-o', str(obj)],
                                 capture_output=True, text=True, env=env)
        self.assertEqual(process.returncode, 0, diagnostics(process))
        text, unused_defined, relocations = form_search.read_object(obj)
        self.assertEqual(text[:4], b'\x00\x00\x00\x00')
        self.assertEqual(relocations, [(0, 2, 'native_data_0202562c', 0)])

    def test_every_other_asm_data_spelling_is_rejected(self):
        rejected = {
            '.word 0x12345678': 'unknown assembler instruction mnemonic',
            '.long 0x12345678': 'unknown assembler instruction mnemonic',
            '.4byte 0x12345678': 'invalid floating-point constant',
            '.byte 0x12': 'unknown assembler instruction mnemonic',
            '.hword 0x1234': 'unknown assembler instruction mnemonic',
            '.short 0x1234': 'unknown assembler instruction mnemonic',
            'dc32 0x12345678': 'unknown assembler instruction mnemonic',
            'dc.b 0x12': 'unknown assembler instruction mnemonic',
            'dc.w 0x1234': 'unknown assembler instruction mnemonic',
            'dc.l 0x12345678': 'unknown assembler instruction mnemonic',
        }
        for body, needle in rejected.items():
            with self.subTest(spelling=body.split()[0]):
                process, unused_obj = compile_asm('    ' + body, self.work)
                self.assertNotEqual(process.returncode, 0, body)
                self.assertIn(needle, diagnostics(process), body)


class MwasmDataDirectiveTests(unittest.TestCase):
    def setUp(self):
        if not have_compilers():
            self.skipTest('the pinned compilers are not present')
        self._directory = tempfile.TemporaryDirectory(prefix='carrier-test-')
        self.work = Path(self._directory.name)

    def tearDown(self):
        self._directory.cleanup()

    def test_halfword_byte_and_word_data_are_emitted(self):
        process, obj = assemble(
            '.section .text\n.thumb\n.global probe\n.type probe, @function\n'
            'probe:\n    add pc, r0\n    .hword 0x003e\n    .hword 0x002e\n'
            '    .byte 0x7f\n    .word 0x11223344\n.size probe, .-probe\n',
            self.work)
        self.assertEqual(process.returncode, 0, diagnostics(process))
        text, unused_defined, unused_relocations = form_search.read_object(obj)
        self.assertEqual(text[:8], bytes.fromhex('87443e002e007f00'))
        self.assertEqual(text[8:12], bytes.fromhex('44332211'))

    def test_dc_spellings_are_rejected_by_mwasmarm(self):
        for spelling in ('dc.w 0x1234', 'dc.b 0x12', 'dcd 0x11223344'):
            with self.subTest(spelling=spelling.split()[0]):
                process, unused_obj = assemble(
                    '.section .text\n.thumb\nprobe:\n    %s\n' % spelling, self.work)
                self.assertNotEqual(process.returncode, 0, spelling)
                self.assertIn('Undefined macro or opcode', diagnostics(process))


@unittest.skipUnless(LEDGER.is_file() and IMAGE.is_file() and MAIN_IMAGE.is_file(),
                     'the measured inputs are not present')
class LaneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads(PLAN.read_text())['rows']
        cls.rows = {}
        with LEDGER.open(encoding='utf-8') as stream:
            for line in stream:
                if not line.strip():
                    continue
                row = json.loads(line)
                cls.rows[(row['module'], int(row['address'], 16))] = row

    def test_plan_rows_are_ledger_rows_and_their_form_matches_the_mode(self):
        for entry in self.plan:
            key = (entry['module'], int(entry['address'], 16))
            self.assertIn(key, self.rows)
            row = self.rows[key]
            self.assertEqual(entry['form'], 'c' if row['mode'] == 'arm' else 's', key)

    def test_table_extents_lie_inside_the_row_and_are_aligned(self):
        for entry in self.plan:
            row = self.rows[(entry['module'], int(entry['address'], 16))]
            address, size = int(row['address'], 16), int(row['bytes'])
            width = 4 if row['mode'] == 'arm' else 2
            for value in ','.join(entry['tables']).split(','):
                start, length = (int(part, 0) for part in value.split(':'))
                self.assertGreaterEqual(start, address, entry['address'])
                self.assertLessEqual(start + length, address + size, entry['address'])
                self.assertEqual(start % width, 0, entry['address'])
                self.assertEqual(length % width, 0, entry['address'])

    def test_scanner_reproduces_every_planned_table(self):
        for entry in self.plan:
            key = (entry['module'], int(entry['address'], 16))
            row = transcribe_data_rows.load_row(*key)
            found = [(item['table'], item['length'])
                     for item in transcribe_data_rows.dispatch_sites(row)]
            if entry['module'] == 'main':
                # The two main rows carry a reciprocal table, not a dispatch table.
                self.assertEqual(found, [], entry['address'])
                continue
            planned = []
            for value in ','.join(entry['tables']).split(','):
                start, length = (int(part, 0) for part in value.split(':'))
                planned.append((start, length))
            self.assertEqual(found, sorted(planned), entry['address'])

    def test_lane_has_one_address_named_file_per_plan_row(self):
        found = {}
        for path in LANE.rglob('*'):
            if not path.is_file():
                continue
            match = re.search(r'native_(main|ov[0-9]{3})_([0-9a-f]{8})\.(c|s)$',
                              path.name)
            if not match:
                continue
            key = (match.group(1), int(match.group(2), 16))
            self.assertNotIn(key, found)
            found[key] = path
        planned = {(entry['module'], int(entry['address'], 16)) for entry in self.plan}
        self.assertEqual(set(found), planned)


if __name__ == '__main__':
    unittest.main()

