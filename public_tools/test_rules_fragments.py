"""Tests for lane-owned source-unit rule fragments (``config/rules.d/*.json``).

The migration invariant is that fragment loading is a pure refactor: the merged
fragment-plus-base rule set must resolve every source file exactly as the same
rules inlined into the legacy base ``rules`` array.  The full-tree test below is
that golden comparison; the fixture tests pin the loading, ordering, precedence
and duplicate-glob contract.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from source_units import (SourceUnitError, config_digest, enumerate_sources, excluded,
                          load_config, resolve, rule_fragment_files, scope_of,
                          source_files)

ROOT = Path(__file__).resolve().parent.parent
MODULES = {
    'main': dict(processor='arm9', loadAddressBase='0x2000000',
                 originalImage='extract/arm9/arm9.bin', bytes=64),
    'ov000': dict(processor='arm9', loadAddressBase='0x21d7240',
                  originalImage='extract/arm9_overlays/ov000.bin', bytes=64),
}
FLAGS = ['-O2', '-proc', 'arm946e']
COMPILER = 'b' * 64


class RuleFragmentFixture(unittest.TestCase):
    def setUp(self):
        container = ROOT / 'work/source-unit-tests'
        container.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=container)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        for name in ('src/main/a.c', 'src/main/deep/b.c', 'src/main/deep/leaf/c.c',
                     'src/verified/x/e.c', 'src/ov000/g1/f.c'):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('int value(void){return 1;}\n')
        self.config = dict(
            schemaVersion=1, denominator=128, buildSha256=COMPILER,
            exclusions=['src/nonmatching/**'],
            compiler=dict(path='tools/mwccarm/mwccarm/2.0/base/mwccarm.exe', sha256=COMPILER),
            compilers={COMPILER: 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'},
            modules=MODULES,
            flagProfiles={'p001': FLAGS, 'p002': FLAGS + ['-O3'], 'p003': FLAGS + ['-Os']},
            rules=[
                dict(glob='src/**', module='main', compilerFlags='p001'),
                dict(glob='src/main/deep/**', module='ov000', compilerFlags='p003'),
            ],
        )
        self.write_config()
        self.write_fragment('a-lane.json', [
            dict(glob='src/main/**', module='main', compilerFlags='p002'),
            dict(glob='src/ov000/g1/**', module='ov000', compilerFlags='p002'),
        ])
        self.write_fragment('b-lane.json', [dict(glob='src/main/deep/leaf/**', mode='thumb')])

    def write_config(self, value=None):
        path = self.root / 'config/source_units.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(json.dumps(value or self.config, indent=1).encode('utf-8'))

    def write_fragment(self, name, value, raw=None):
        path = self.root / 'config/rules.d' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if raw is not None:
            path.write_text(raw, encoding='utf-8')
        else:
            path.write_bytes(json.dumps(value, indent=1).encode('utf-8'))


class FragmentLoadingTests(RuleFragmentFixture):
    def test_missing_rules_directory_is_not_an_error(self):
        for path in (self.root / 'config/rules.d').glob('*.json'):
            path.unlink()
        (self.root / 'config/rules.d').rmdir()
        config = load_config(self.root)
        self.assertEqual(config['fragments'], [])
        self.assertEqual(config['fragmentRules'], 0)
        self.assertEqual(config['baseRules'], 2)
        self.assertEqual(resolve(config, 'src/main/a.c')['compilerFlags'], FLAGS)

    def test_fragment_files_load_in_filename_order(self):
        self.write_fragment('0-first.json', [dict(glob='src/verified/**', module='main',
                                                  compilerFlags='p002')])
        self.write_fragment('z-last.json', [])
        config = load_config(self.root)
        self.assertEqual([path.name for path in rule_fragment_files(self.root)],
                         ['0-first.json', 'a-lane.json', 'b-lane.json', 'z-last.json'])
        self.assertEqual(config['fragments'], [
            'config/rules.d/0-first.json', 'config/rules.d/a-lane.json',
            'config/rules.d/b-lane.json', 'config/rules.d/z-last.json'])
        self.assertEqual(config['fragmentRules'], 4)
        self.assertEqual(config['baseRules'], 2)

    def test_fragments_precede_the_base_rules_in_merge_order(self):
        config = load_config(self.root)
        self.assertEqual(config['mergeOrder'], [
            'src/main', 'src/ov000/g1', 'src/main/deep/leaf',
            'src', 'src/main/deep'])
        self.assertEqual(config['origins']['src/main'], 'config/rules.d/a-lane.json')
        self.assertEqual(config['origins']['src'], 'config/source_units.json')

    def test_resolution_sorts_the_merged_list_by_specificity(self):
        config = load_config(self.root)
        self.assertEqual([rule['scope'] for rule in config['rules']],
                         ['src', 'src/main', 'src/ov000/g1', 'src/main/deep',
                          'src/main/deep/leaf'])

    def test_fragment_rule_overrides_its_base_parent(self):
        config = load_config(self.root)
        rule = resolve(config, 'src/ov000/g1/f.c')
        self.assertEqual(rule['module'], 'ov000')
        self.assertEqual(rule['compilerFlags'], FLAGS + ['-O3'])

    def test_more_specific_base_rule_beats_a_shallower_fragment_rule(self):
        config = load_config(self.root)
        rule = resolve(config, 'src/main/deep/b.c')
        self.assertEqual(rule['module'], 'ov000')
        self.assertEqual(rule['compilerFlags'], FLAGS + ['-Os'])
        self.assertEqual(rule['mode'], 'arm')

    def test_fragment_and_base_fields_merge_along_the_chain(self):
        config = load_config(self.root)
        rule = resolve(config, 'src/main/deep/leaf/c.c')
        # The leaf fragment changes only mode; module and flags come from the
        # deeper base rule, not from the shallow fragment rule.
        self.assertEqual(rule['mode'], 'thumb')
        self.assertEqual(rule['module'], 'ov000')
        self.assertEqual(rule['compilerFlags'], FLAGS + ['-Os'])

    def test_fragment_rules_participate_in_full_enumeration(self):
        result = enumerate_sources(self.root, load_config(self.root))
        leaf = next(item for item in result['compiled'] if item['path'].endswith('leaf/c.c'))
        self.assertEqual(leaf['mode'], 'thumb')
        self.assertEqual(len(result['compiled']), 5)


class FragmentValidationTests(RuleFragmentFixture):
    def test_duplicate_glob_between_fragments_names_both_sources(self):
        self.write_fragment('b-lane.json', [dict(glob='src/main/**', module='main',
                                                 compilerFlags='p001')])
        with self.assertRaisesRegex(SourceUnitError, 'Duplicate') as caught:
            load_config(self.root)
        message = str(caught.exception)
        self.assertIn("Duplicate source-unit rule glob 'src/main'", message)
        self.assertIn('config/rules.d/a-lane.json', message)
        self.assertIn('config/rules.d/b-lane.json', message)

    def test_duplicate_glob_between_fragment_and_base_names_the_base(self):
        self.write_fragment('a-lane.json', [dict(glob='src/main/deep/**', module='main',
                                                 compilerFlags='p001')])
        with self.assertRaisesRegex(SourceUnitError, 'Duplicate') as caught:
            load_config(self.root)
        message = str(caught.exception)
        self.assertIn("Duplicate source-unit rule glob 'src/main/deep'", message)
        self.assertIn('config/rules.d/a-lane.json', message)
        self.assertIn('config/source_units.json', message)

    def test_fragment_must_be_a_json_array(self):
        self.write_fragment('object.json', None, raw='{"rules": []}\n')
        with self.assertRaisesRegex(SourceUnitError, 'must be a JSON array'):
            load_config(self.root)

    def test_fragment_must_be_valid_json(self):
        self.write_fragment('broken.json', None, raw='[{"glob": ]\n')
        with self.assertRaisesRegex(SourceUnitError, 'not valid JSON'):
            load_config(self.root)

    def test_fragment_entry_must_be_an_object(self):
        self.write_fragment('scalar.json', None, raw='["src/main/**"]\n')
        with self.assertRaisesRegex(SourceUnitError, 'must be objects'):
            load_config(self.root)

    def test_fragment_rule_is_validated_and_names_its_source(self):
        self.write_fragment('bad-field.json', [dict(glob='src/other/**', module='main',
                                                    bogus='value')])
        with self.assertRaisesRegex(SourceUnitError, 'Unsupported source-unit fields') as caught:
            load_config(self.root)
        self.assertIn('config/rules.d/bad-field.json', str(caught.exception))


class DeriveFragmentTests(RuleFragmentFixture):
    def test_derivation_omits_globs_owned_by_a_fragment(self):
        from derive_source_units import without_fragment_rules
        rules = [dict(glob='src/main/**'), dict(glob='src/ov000/g1/**'),
                 dict(glob='src/other/**')]
        kept, dropped = without_fragment_rules(rules, self.root)
        self.assertEqual([rule['glob'] for rule in kept], ['src/other/**'])
        self.assertEqual(dropped, 2)


class ConfigDigestTests(RuleFragmentFixture):
    def test_digest_covers_the_base_and_the_fragments(self):
        before = config_digest(self.root)
        self.assertEqual(before, config_digest(self.root))
        self.write_fragment('b-lane.json', [dict(glob='src/main/deep/leaf/**', mode='arm')])
        self.assertNotEqual(config_digest(self.root), before)
        after_fragment = config_digest(self.root)
        self.config['description'] = 'changed'
        self.write_config()
        self.assertNotEqual(config_digest(self.root), after_fragment)


class ShippedFragmentTests(unittest.TestCase):
    """A lane ships its own fragment; the loader account must stay exact."""

    def test_shipped_fragments_account_for_the_merged_rule_count(self):
        self.assertTrue((ROOT / 'config/rules.d/README.md').is_file())
        config = load_config(ROOT)
        base = json.loads((ROOT / 'config/source_units.json').read_text(encoding='utf-8-sig'))
        shipped = sum(len(json.loads(path.read_text(encoding='utf-8')))
                      for path in rule_fragment_files(ROOT))
        self.assertEqual(config['fragmentRules'], shipped)
        self.assertEqual(config['baseRules'], len(base['rules']))
        self.assertEqual(len(config['rules']), len(base['rules']) + shipped)

    def test_the_first_lane_fragment_resolves_its_own_sources(self):
        config = load_config(ROOT)
        for mode, profile in (('thumb', 'p033'), ('arm', 'p003')):
            path = 'src/ov006/g1_ov006_sweep2/%s/ov006/native_ov006_00000000.c' % mode
            rule = resolve(config, path)
            self.assertEqual(rule['module'], 'ov006')
            self.assertEqual(rule['mode'], mode)
            self.assertEqual(rule['compilerFlags'], config['profiles'][profile])
            self.assertEqual(rule['compilerSha256'],
                             '89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca')
            scope = 'src/ov006/g1_ov006_sweep2/' + mode
            self.assertEqual(config['origins'][scope], 'config/rules.d/ov006-sweep2.json')

    def test_a_fragment_repeating_a_shipped_base_rule_is_rejected(self):
        base = json.loads((ROOT / 'config/source_units.json').read_text(encoding='utf-8-sig'))
        rule = base['rules'][0]
        container = ROOT / 'work/source-unit-tests'
        container.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=container) as name:
            root = Path(name)
            folder = root / 'config/rules.d'
            folder.mkdir(parents=True)
            (folder / 'duplicate.json').write_bytes(json.dumps([rule]).encode('utf-8'))
            with self.assertRaisesRegex(SourceUnitError, 'Duplicate') as caught:
                load_config(root, base)
        message = str(caught.exception)
        self.assertIn("Duplicate source-unit rule glob '" + scope_of(rule['glob']) + "'", message)
        self.assertIn('config/rules.d/duplicate.json', message)
        self.assertIn('config/source_units.json', message)


class FullTreeGoldenTests(unittest.TestCase):
    """Moving a shipped base rule into a fragment must not change resolution."""

    def test_full_tree_resolves_the_same_when_a_shipped_base_rule_moves_to_a_fragment(self):
        config = load_config(ROOT)
        rules = [item['raw'] for item in config['rules']]
        target = next(rule for rule in rules if rule['glob'] == 'src/main/**')
        split_data = dict(config['data'])
        split_data['rules'] = [rule for rule in rules if rule is not target]
        container = ROOT / 'work/source-unit-tests'
        container.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=container) as name:
            root = Path(name)
            folder = root / 'config/rules.d'
            folder.mkdir(parents=True)
            (folder / 'golden-split.json').write_bytes(json.dumps([target]).encode('utf-8'))
            split = load_config(root, split_data)
        self.assertEqual(len(split['rules']), len(config['rules']))
        self.assertEqual(split['fragmentRules'], 1)
        checked = 0
        for name in source_files(ROOT):
            if excluded(config, name):
                continue
            merged = resolve(config, name)
            reference = resolve(split, name)
            if merged != reference:
                self.fail(f'{name}: split base rule resolves differently from the base config')
            checked += 1
        self.assertGreater(checked, 10000)


if __name__ == '__main__':
    unittest.main()
