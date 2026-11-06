import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from source_links import HEADER, TABLE, generate_header, load_aliases


ROOT = Path(__file__).resolve().parents[1]


class SourceLinksTests(unittest.TestCase):
    def setUp(self):
        (ROOT / 'work').mkdir(exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(prefix='source-links-tests-', dir=ROOT / 'work')
        self.root = Path(self.directory.name)
        source = self.root / 'src/main.c'
        source.parent.mkdir()
        source.write_text('#include "context.h"\nint native_main_0202b1a8(void) { return VALUE; }\n')
        header = source.with_name('context.h')
        header.write_text('#define VALUE 1\n')
        self.row = dict(program='', processor='arm9', module='main', mode='arm', address='0x0202b1a8',
                        reportSymbol='func_0202b1a8', sourceSymbol='native_main_0202b1a8', sourcePath='src/main.c',
                        sourceSha256=self.hash(source), complete=False,
                        sourceDependencies=[dict(path='src/context.h', sha256=self.hash(header))])
        (self.root / TABLE).parent.mkdir()
        self.write_table()

    def tearDown(self):
        self.directory.cleanup()

    def hash(self, path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def write_table(self):
        (self.root / TABLE).write_text(json.dumps(dict(schemaVersion=1, aliases=[self.row])))

    def test_exact_names_header_and_source_mapping(self):
        generate_header(self.root)
        self.assertEqual((self.root / HEADER).read_bytes(), b'#define func_0202b1a8 native_main_0202b1a8\n')
        self.assertEqual(load_aliases(self.root), {'func_0202b1a8': 'src/main.c'})

    def test_changed_source_is_rejected(self):
        (self.root / 'src/main.c').write_text('int native_main_0202b1a8(void) { return 2; }\n')
        with self.assertRaisesRegex(ValueError, 'Source hash differs'):
            generate_header(self.root)

    def test_missing_quoted_header_is_rejected(self):
        (self.root / 'src/context.h').unlink()
        with self.assertRaisesRegex(ValueError, 'quoted include is missing'):
            generate_header(self.root)

    def test_unpinned_quoted_header_is_rejected(self):
        self.row['sourceDependencies'] = []
        self.write_table()
        with self.assertRaisesRegex(ValueError, 'Quoted include lacks a declared hash'):
            generate_header(self.root)

    def test_cross_overlay_alias_is_rejected(self):
        self.row['module'] = 'ov001'
        self.write_table()
        with self.assertRaisesRegex(ValueError, 'crosses its physical module namespace'):
            generate_header(self.root)

    def test_definition_cannot_be_a_comment_or_prototype(self):
        source = self.root / 'src/main.c'
        source.write_text('/* int native_main_0202b1a8(void) { return 1; } */\nint native_main_0202b1a8(void);\n')
        self.row.update(sourceSha256=self.hash(source), sourceDependencies=[])
        self.write_table()
        with self.assertRaisesRegex(ValueError, 'no unique top-level C definition'):
            generate_header(self.root)

    def test_stale_generated_header_is_rejected(self):
        generate_header(self.root)
        (self.root / HEADER).write_text('#define func_0202b1a8 wrong\n')
        with self.assertRaisesRegex(ValueError, 'header is missing or stale'):
            load_aliases(self.root)


if __name__ == '__main__':
    unittest.main()
