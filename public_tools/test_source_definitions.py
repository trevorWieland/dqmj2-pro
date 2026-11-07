import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from source_links import DEFINITIONS, generate_definitions, load_definition_paths


ROOT = Path(__file__).resolve().parents[1]


class SourceDefinitionTests(unittest.TestCase):
    def setUp(self):
        (ROOT / 'work').mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix='source-definitions-tests-', dir=ROOT / 'work')
        self.root = Path(self.temporary.name)
        (self.root / 'src').mkdir()
        (self.root / 'public').mkdir()
        (self.root / 'public_tools').mkdir()
        (self.root / 'build').mkdir()
        self.primary = self.root / 'src/main.c'
        self.header = self.root / 'src/body.inc'
        self.primary.write_text('#include "body.inc"\n')
        self.header.write_text('int Work(void) { return 1; }\n')
        self.row = dict(id='fixture/arm9/main/arm/02000000', program='', processor='arm9', module='main', mode='arm',
                        address='0x02000000', bytes=8, sourceUnit='src/main.c', sourceSha256=self.hash(self.primary),
                        compilerFlags=['-O2'], sourceDependencies=[dict(path='src/body.inc', sha256=self.hash(self.header))],
                        states=dict(functionMatched=True, moduleLinked=True))
        self.write_manifest()
        report = dict(units=[dict(name='src/main/host/arm9/main/02000000', metadata=dict(complete=True),
                                 functions=[dict(name='Work', size='8', address='0')])])
        (self.root / 'build/report.json').write_text(json.dumps(report))
        generate_definitions(self.root, Path('build/report.json'))

    def tearDown(self):
        self.temporary.cleanup()

    def hash(self, path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def write_manifest(self):
        (self.root / 'public/accepted-functions.json').write_text(json.dumps(dict(schemaVersion=1, functions=[self.row])))

    def table(self):
        return json.loads((self.root / DEFINITIONS).read_text())

    def write_table(self, table):
        (self.root / DEFINITIONS).write_text(json.dumps(table))

    def test_unique_definition_in_frozen_include(self):
        self.assertEqual(load_definition_paths(self.root), {(self.row['id'], 'Work'): 'src/body.inc'})

    def test_changed_definition_bytes_are_rejected(self):
        self.header.write_text('int Work(void) { return 2; }\n')
        with self.assertRaisesRegex(ValueError, 'include hash differs'):
            load_definition_paths(self.root)

    def test_cross_cpu_identity_is_rejected(self):
        table = self.table()
        table['definitions'][0]['processor'] = 'arm7'
        self.write_table(table)
        with self.assertRaisesRegex(ValueError, 'physical function identity'):
            load_definition_paths(self.root)

    def test_header_outside_real_include_closure_is_rejected(self):
        other = self.root / 'src/unreached.inc'
        other.write_text(self.header.read_text())
        table = self.table()
        table['definitions'][0]['definitionPath'] = 'src/unreached.inc'
        self.write_table(table)
        with self.assertRaisesRegex(ValueError, 'unique frozen include definition'):
            load_definition_paths(self.root)

    def test_conditional_duplicate_definitions_are_rejected(self):
        self.header.write_text('#if FIRST\nint Work(void) { return 1; }\n#else\nint Work(void) { return 2; }\n#endif\n')
        self.row['sourceDependencies'][0]['sha256'] = self.hash(self.header)
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, 'ambiguous within its actual compiler include closure'):
            generate_definitions(self.root, Path('build/report.json'))

    def test_changed_accepted_manifest_requires_regeneration(self):
        self.row['bytes'] = 12
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, 'stale for this frozen accepted manifest'):
            load_definition_paths(self.root)

    def test_definition_after_split_struct_tail_is_recognized(self):
        self.header.write_text('int member;\n} Shared;\nint Work(void) { return 1; }\n')
        self.row['sourceDependencies'][0]['sha256'] = self.hash(self.header)
        self.write_manifest()
        generate_definitions(self.root, Path('build/report.json'))
        self.assertEqual(load_definition_paths(self.root), {(self.row['id'], 'Work'): 'src/body.inc'})


if __name__ == '__main__':
    unittest.main()
