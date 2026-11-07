import copy
import tempfile
import unittest
from pathlib import Path

from native_mb_context import SOURCE, SOURCE_SHA, ADDRESS, SIZE, STORAGE, local_bss_profile, coalesce_layout
from native_objects import FreshObjects


class RegisterLocalStorageTests(unittest.TestCase):
    def setUp(self):
        self.unit = dict(processor='arm9', module='main', mode=None, kind='data', section='.bss',
            sourceSection='.bss', source=SOURCE, sourceSha256=SOURCE_SHA, start=hex(STORAGE), end=hex(STORAGE + 1),
            symbols={'data_020e68a4': 'update$40'}, initializedStorageCredit=0, compiledBytes=0, allocatedBytes=1,
            sourceDependencies=[dict(path='src/header.h', sha256='c' * 64)], object='work/original.o', sha256='b' * 64)
        self.row = dict(program=None, processor='arm9', module='main', mode='arm', address=hex(ADDRESS), bytes=SIZE,
            sourceUnit=SOURCE, sourceSha256=SOURCE_SHA, sourceDependencies=copy.deepcopy(self.unit['sourceDependencies']),
            object='work/original.o', objectSha256='b' * 64, compilerSha256='d' * 64, compilerFlags=['-lang', 'c99'])

    def test_local_bss_uses_its_exact_closed_function_profile(self):
        fresh = FreshObjects.__new__(FreshObjects)
        fresh.manifest, fresh.data = dict(functions=[self.row]), []
        self.assertEqual(fresh.profile(self.unit), (SOURCE, 'd' * 64, ('-lang', 'c99')))
        self.assertEqual(fresh.data, [])

    def test_unrelated_storage_does_not_gain_a_profile(self):
        unit = dict(self.unit, source='src/unqualified.c')
        self.assertIsNone(local_bss_profile(unit, dict(functions=[self.row])))

    def test_namespace_extent_payload_and_credit_changes_are_rejected(self):
        changes = dict(processor='arm7', module='ov000', program='child', mode='thumb', section='.data',
            sourceSection='.data', sourceSha256='0' * 64, start=hex(STORAGE + 1), end=hex(STORAGE + 2),
            initializedStorageCredit=1, compiledBytes=1, allocatedBytes=2, symbols={'data': 'other'},
            function='extra', interiorSymbols={'extra': 'name'}, relocationOffsets=[0], sectionPaddingBytes=1,
            nativeDataDeclaration={'name': 'extra'}, assemblyJustification={'classification': 'extra'},
            sourceDependencies=[], object='work/different.o', sha256='0' * 64)
        for key, value in changes.items():
            with self.subTest(field=key), self.assertRaises(ValueError):
                local_bss_profile(dict(self.unit, **{key: value}), dict(functions=[self.row]))

    def test_function_must_be_the_exact_unique_closed_owner(self):
        for rows in ([], [self.row, self.row], [dict(self.row, bytes=SIZE - 4)],
                     [dict(self.row, module='ov000')], [dict(self.row, sourceSha256='0' * 64)]):
            with self.subTest(rows=len(rows)), self.assertRaises(ValueError):
                local_bss_profile(self.unit, dict(functions=rows))

    def fixture(self):
        base = Path(__file__).resolve().parents[1] / 'work/native-mb-tests'
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        directory = Path(temporary.name)
        (directory / 'config-arm9').mkdir()
        first = f'\nMB_RegisterFile.c:\n    complete\n    .text start:0x{ADDRESS:08x} end:0x{ADDRESS + SIZE:08x}\n'
        second = f'\nMB_RegisterFile.c:\n    complete\n    .bss start:0x{STORAGE:08x} end:0x{STORAGE + 1:08x}\n'
        (directory / 'config-arm9/delinks.txt').write_text('unrelated\n' + first + second)
        (directory / 'config-arm9/symbols.txt').write_text('update$40 kind:bss(size=0x1) addr:0x020e68a4\n')
        return directory, first, second

    def test_whole_object_layout_retains_local_bss_without_initialized_credit(self):
        directory, first, second = self.fixture()
        report = {}
        coalesce_layout(directory, report)
        text = (directory / 'config-arm9/delinks.txt').read_text()
        self.assertEqual(text.count('MB_RegisterFile.c:'), 1)
        self.assertIn('    .text start:', text)
        self.assertIn('    .bss start:', text)
        self.assertTrue(text.startswith('unrelated\n'))
        self.assertIn('addr:0x020e68a4 local\n', (directory / 'config-arm9/symbols.txt').read_text())
        self.assertEqual(report['qualifiedRegisterLocalStorage']['initializedStorageCredit'], 0)

    def test_duplicate_or_missing_layout_is_rejected_before_writing(self):
        for duplicate in (False, True):
            directory, first, second = self.fixture()
            path = directory / 'config-arm9/delinks.txt'
            text = path.read_text() + first if duplicate else first
            path.write_text(text)
            with self.assertRaises(ValueError):
                coalesce_layout(directory, {})
            self.assertEqual(path.read_text(), text)


if __name__ == '__main__':
    unittest.main()
