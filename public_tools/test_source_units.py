import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from source_units import SourceUnitError, check, enumerate_sources, load_config, resolve


MODULES = {
    'main': dict(processor='arm9', loadAddressBase='0x2000000', originalImage='extract/arm9/arm9.bin', bytes=64),
    'ov000': dict(processor='arm9', loadAddressBase='0x21d7240', originalImage='extract/arm9_overlays/ov000.bin', bytes=64),
}
FLAGS = ['-O2', '-proc', 'arm946e']


class SourceUnitTests(unittest.TestCase):
    def setUp(self):
        container = Path(__file__).resolve().parent.parent / 'work/source-unit-tests'
        container.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=container)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        for name in ('src/main/a.c', 'src/main/deep/b.c', 'src/ov000/c.c', 'src/nonmatching/d.c', 'src/main/header.h'):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('int value;\n' if name.endswith('.h') else 'int value(void){return 1;}\n')
        self.config = dict(
            schemaVersion=1, denominator=128, buildSha256='a' * 64, exclusions=['src/nonmatching/**'],
            compiler=dict(path='tools/mwccarm/2.0/base/mwccarm.exe', sha256='b' * 64),
            compilers={'b' * 64: 'tools/mwccarm/2.0/base/mwccarm.exe',
                       'c' * 64: 'tools/mwccarm/1.2/base/mwccarm.exe'},
            modules=MODULES,
            flagProfiles={'arm9': FLAGS},
            rules=[dict(glob='src/main/**', module='main', compilerFlags='arm9'),
                   dict(glob='src/ov000/**', module='ov000', compilerFlags=FLAGS),
                   dict(glob='src/main/deep/**', compilerFlags='arm9', processor='arm9')],
        )
        self.write_config()

    def write_config(self, value=None):
        path = self.root / 'config/source_units.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value or self.config))

    def test_resolution_fills_module_fields(self):
        config = load_config(self.root)
        rule = resolve(config, 'src/main/a.c')
        self.assertEqual(rule['module'], 'main')
        self.assertEqual(rule['processor'], 'arm9')
        self.assertEqual(rule['compilerFlags'], FLAGS)
        self.assertEqual(rule['loadAddressBase'], '0x2000000')
        self.assertEqual(rule['originalImage'], 'extract/arm9/arm9.bin')

    def test_inheritance_merges_only_changed_fields(self):
        config = load_config(self.root)
        rule = resolve(config, 'src/main/deep/b.c')
        self.assertEqual(rule['module'], 'main')
        self.assertEqual(rule['processor'], 'arm9')

    def test_enumeration_excludes_nonmatching_and_non_c(self):
        config = load_config(self.root)
        result = enumerate_sources(self.root, config)
        self.assertEqual([item['path'] for item in result['compiled']],
                         ['src/main/a.c', 'src/main/deep/b.c', 'src/ov000/c.c'])
        self.assertEqual(result['excluded'], ['src/nonmatching/d.c'])
        summary = check(self.root, config)
        self.assertEqual(summary['sourceFiles'], 5)
        self.assertEqual(summary['resolvedFiles'], 4)
        self.assertEqual(summary['compiledSources'], 3)

    def test_unmatched_file_fails_loudly(self):
        path = self.root / 'src/newdir/orphan.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('int orphan(void){return 0;}\n')
        with self.assertRaisesRegex(SourceUnitError, 'match no unit rule'):
            enumerate_sources(self.root)

    def test_duplicate_scope_is_rejected(self):
        self.config['rules'].append(dict(glob='src/main/**', module='ov000', compilerFlags='arm9'))
        with self.assertRaisesRegex(SourceUnitError, 'Duplicate'):
            load_config(None, self.config)

    def test_unknown_profile_is_rejected(self):
        self.config['rules'][0]['compilerFlags'] = 'missing'
        with self.assertRaisesRegex(SourceUnitError, 'Unknown compiler flag profile'):
            resolve(load_config(None, self.config), 'src/main/a.c')

    def test_processor_must_match_module_inventory(self):
        self.config['rules'][0]['processor'] = 'arm7'
        with self.assertRaisesRegex(SourceUnitError, 'Processor disagrees'):
            resolve(load_config(None, self.config), 'src/main/a.c')

    def test_compiler_defaults_and_rule_override(self):
        config = load_config(self.root)
        self.assertEqual(resolve(config, 'src/main/a.c')['compilerSha256'], 'b' * 64)
        self.config['rules'][0]['compilerSha256'] = 'c' * 64
        rule = resolve(load_config(None, self.config), 'src/main/a.c')
        self.assertEqual(rule['compilerSha256'], 'c' * 64)
        self.assertTrue(rule['compilerPath'].endswith('1.2/base/mwccarm.exe'))

    def test_unknown_compiler_is_rejected(self):
        self.config['rules'][0]['compilerSha256'] = 'd' * 64
        with self.assertRaisesRegex(SourceUnitError, 'Unknown compiler identity'):
            resolve(load_config(None, self.config), 'src/main/a.c')

    def test_alternates_are_resolved_for_profile_exceptions(self):
        self.config['alternates'] = {'src/main/a.c': [
            dict(compilerFlags='arm9', compilerSha256='c' * 64)]}
        config = load_config(None, self.config)
        item = next(item for item in enumerate_sources(self.root, config)['compiled']
                    if item['path'] == 'src/main/a.c')
        self.assertEqual(len(item['alternates']), 1)
        self.assertEqual(item['alternates'][0]['compilerSha256'], 'c' * 64)
        self.assertEqual(item['alternates'][0]['compilerFlags'], FLAGS)

    def test_deeper_rule_overrides_parent_module(self):
        self.config['rules'][2] = dict(glob='src/main/deep/**', module='ov000', compilerFlags='arm9')
        rule = resolve(load_config(None, self.config), 'src/main/deep/b.c')
        self.assertEqual(rule['module'], 'ov000')
        self.assertEqual(rule['loadAddressBase'], '0x21d7240')
        self.assertEqual(rule['originalImage'], 'extract/arm9_overlays/ov000.bin')


if __name__ == '__main__':
    unittest.main()
