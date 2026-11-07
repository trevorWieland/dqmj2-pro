import copy
import hashlib
import json
import os
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from bytematch_project import DENOMINATOR, REPORTS, digest, elf_object, function_contract, nonoverlap, prepare, verify_compilation_equivalence, write


class ByteMatchProjectTests(unittest.TestCase):
    def setUp(self):
        container = Path(__file__).resolve().parent.parent / 'work/bytematch-project-tests'
        container.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=container)
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root, self.private = self.base / 'public', self.base / 'private'
        self.output = self.root / 'build/B2JJ-modified'
        for root in (self.root, self.private):
            (root / 'src').mkdir(parents=True)
            (root / 'src/value.c').write_text('int value(void){return 7;}\n')
        self.body = bytes.fromhex('0700a0e3')
        self.obj = self.private / 'work/value.o'
        elf_object(self.obj, self.body, [('value', 0, 4, 'arm')])
        self.row = dict(id='accepted', buildSha256='a' * 64, processor='arm9', program=None, module='m00',
                        address='0x2000000', mode='arm', symbol='func_02000000', bytes=4,
                        sourceUnit='src/value.c', sourceSha256=digest(self.root / 'src/value.c'),
                        sourceDependencies=[], compilerSha256='b' * 64, compilerFlags=['-proc', 'arm946e'],
                        states=dict(functionMatched=True, moduleLinked=True))
        self.manifest = dict(schemaVersion=1, revision='closed', romSha256='a' * 64,
                             initializedDenominatorBytes=DENOMINATOR, functions=[self.row])
        write(self.root / 'public/accepted-functions.json', self.manifest)
        self.modules, self.links = [], []
        for index in range(20):
            size = DENOMINATOR - 19 * 8 if index == 0 else 8
            original = self.body + bytes(size - 4)
            native = self.private / f'inputs/m{index:02}.bin'
            linked = self.private / f'build/m{index:02}.bin'
            native.parent.mkdir(parents=True, exist_ok=True)
            linked.parent.mkdir(parents=True, exist_ok=True)
            native.write_bytes(original)
            linked.write_bytes(original)
            program = 'child.srl' if index >= 14 else None
            processor = 'arm7' if 11 <= index < 14 or index >= 17 else 'arm9'
            module = dict(name=f'm{index:02}', base='0x2000000', bytes=size, sha256=digest(native),
                          binary=native.relative_to(self.private).as_posix(), processor=processor, program=program)
            self.modules.append(module)
            self.links.append(dict(module=module['name'], inputSha256=module['sha256'], inputBytes=size,
                                   output=str(linked), outputSha256=digest(linked), exactBytes=True))
        self.unit = dict(module='m00', start='0x2000000', end='0x2000004', source='src/value.c',
                         sourceSha256=self.row['sourceSha256'], object=self.obj.relative_to(self.private).as_posix(),
                         sha256=digest(self.obj), kind='function', function='value', compiledBytes=4)
        write(self.private / 'ledger/modules.json', dict(buildSha256='a' * 64, modules=self.modules))
        (self.private / 'ledger/functions.jsonl').write_text(json.dumps(self.row) + '\n')
        for filename, begin, end in zip(REPORTS, (0, 11, 14), (11, 14, 20)):
            write(self.private / 'evidence/linking' / filename,
                  dict(buildNamespace='a' * 64, allModuleBytesExact=True, symbolCheckPassed=True,
                       modules=self.links[begin:end], sourceUnits=[self.unit] if begin == 0 else []))
        self.fresh_obj = self.root / 'build/compile/value.o'
        elf_object(self.fresh_obj, self.body, [('value', 0, 4, 'arm')])
        self.compilation = self.root / 'build/public-source-compile/report.json'
        self.compile_record = dict(source='src/value.c', compilerSha256='b' * 64, compilerFlags=['-proc', 'arm946e'],
                                   status='compiled', object=str(self.fresh_obj), objectSha256=digest(self.fresh_obj))
        self.compile_report = dict(status='source-compilation-passed', fullManifestCompiled=True,
                                   manifestSha256=digest(self.root / 'public/accepted-functions.json'),
                                   results=[self.compile_record])
        write(self.compilation, self.compile_report)
        pins = {'evidence/linking/' + name: dict(sha256=digest(self.private / 'evidence/linking' / name)) for name in REPORTS}
        write(self.output / 'build-receipt.json', dict(buildPassed=True, publicGitRevision='public-head', startedTimeNs=0,
              acceptedManifestSha256=digest(self.root / 'public/accepted-functions.json'), reports=pins))

    def export(self, diagnostic=True):
        with patch('bytematch_project.subprocess.check_output', return_value='public-head\n'), patch.dict(os.environ, {'GITHUB_SHA': ''}):
            return prepare(self.root, self.private, self.output, diagnostic=diagnostic)

    def test_verified_data_inside_broad_executable_section_stays_data(self):
        source = self.root / 'src/table.c'
        source.write_text('const unsigned int table = 0;\n')
        spans = {'m00': [dict(start=0x2000004, end=0x2000008, source='src/table.c', sourceSha256=digest(source), symbol='table')]}
        sections = lambda unused, module: [(0x2000000, 0x2000008, True)] if module['name'] == 'm00' else []
        with patch('bytematch_project.load_data_spans', return_value=spans), patch('bytematch_project.original_sections', side_effect=sections):
            summary = self.export()
        project = json.loads((self.output / 'objdiff.json').read_text())
        unit = next(u for u in project['units'] if u['name'].endswith('/m00/02000004'))
        self.assertEqual(summary['matchedTypedDataBytes'], 4)
        self.assertEqual(unit['metadata']['source_path'], 'src/table.c')
        self.assertTrue(unit['metadata']['complete'])
        self.assertNotEqual(unit['base_path'], 'base/empty.o')
        self.assertIn(b'.data\0', (self.output / unit['base_path']).read_bytes())

    def test_data_cannot_promote_a_measured_function(self):
        candidate = dict(self.row, id='unmatched', address='0x2000004', symbol='func_02000004')
        with (self.private / 'ledger/functions.jsonl').open('a') as stream:
            stream.write(json.dumps(candidate) + '\n')
        spans = {'m00': [dict(start=0x2000004, end=0x2000008, source='src/value.c')]}
        sections = lambda unused, module: [(0x2000000, 0x2000008, True)] if module['name'] == 'm00' else []
        with patch('bytematch_project.load_data_spans', return_value=spans), patch('bytematch_project.original_sections', side_effect=sections):
            with self.assertRaisesRegex(ValueError, 'data overlaps measured code'):
                self.export()

    def test_full_denominator_scaffolding_receives_no_source_credit(self):
        summary = self.export()
        project = json.loads((self.output / 'objdiff.json').read_text())
        self.assertEqual(summary['moduleCount'], 20)
        self.assertEqual(summary['originalInitializedBytes'], DENOMINATOR)
        self.assertEqual(summary['acceptedFunctions'], 1)
        self.assertFalse(summary['publishable'])
        complete = [u for u in project['units'] if u['metadata']['complete']]
        self.assertEqual(len(complete), 1)
        self.assertEqual(complete[0]['metadata']['source_path'], 'src/value.c')
        self.assertTrue(all(u['base_path'] == 'base/empty.o' for u in project['units'] if not u['metadata']['complete']))
        self.assertTrue(all('base_path' in u for u in project['units']))

    def test_normal_export_requires_and_verifies_fresh_compile_equivalence(self):
        summary = self.export(diagnostic=False)
        self.assertTrue(summary['publishable'])
        self.assertEqual(summary['publicGitRevision'], 'public-head')
        elf_object(self.fresh_obj, bytes.fromhex('0800a0e3'), [('value', 0, 4, 'arm')])
        self.compile_report['results'][0]['objectSha256'] = digest(self.fresh_obj)
        write(self.compilation, self.compile_report)
        with self.assertRaisesRegex(ValueError, 'Fresh compiler bytes or relocations differ'):
            self.export(diagnostic=False)

    def test_missing_fresh_compile_report_does_not_publish(self):
        self.compilation.unlink()
        with self.assertRaises(FileNotFoundError):
            self.export(diagnostic=False)

    def test_readonly_equivalence_check_covers_selected_functions(self):
        result = verify_compilation_equivalence(self.root, self.private, self.compilation)
        self.assertEqual(result['verifiedFreshSourceFunctions'], 1)
        self.assertTrue(result['publicSourceObjectsEquivalentToLinkedInputs'])
        self.assertTrue(result['historicalLinkReportsDoNotEstablishFreshLinking'])

    def test_source_hash_tampering_is_rejected(self):
        (self.root / 'src/value.c').write_text('int value(void){return 99;}\n')
        with self.assertRaisesRegex(ValueError, 'Source hash differs'):
            self.export()

    def test_partial_module_inventory_is_rejected(self):
        write(self.private / 'ledger/modules.json', dict(buildSha256='a' * 64, modules=self.modules[:-1]))
        with self.assertRaisesRegex(ValueError, 'All twenty original modules'):
            self.export()

    def test_overlapping_ranges_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            nonoverlap([(0, 8), (4, 12)], 0, 16)
        path = self.private / 'evidence/linking/latest.json'
        report = json.loads(path.read_text())
        report['sourceUnits'].append(copy.deepcopy(self.unit))
        write(path, report)
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            self.export()

    def test_newer_unaccepted_source_remains_a_gap(self):
        path = self.private / 'evidence/linking/latest.json'
        report = json.loads(path.read_text())
        newer = dict(self.unit, start='0x2000004', end='0x2000008', function='new_value')
        report['sourceUnits'].append(newer)
        write(path, report)
        summary = self.export()
        self.assertEqual(summary['acceptedFunctions'], 1)
        project = json.loads((self.output / 'objdiff.json').read_text())
        self.assertEqual(sum(u['metadata']['complete'] for u in project['units']), 1)

    def test_genuinely_linked_output_must_match_the_original(self):
        path = Path(self.links[0]['output'])
        raw = bytearray(path.read_bytes())
        raw[0] ^= 1
        path.write_bytes(raw)
        report_path = self.private / 'evidence/linking/latest.json'
        report = json.loads(report_path.read_text())
        report['modules'][0]['outputSha256'] = digest(path)
        write(report_path, report)
        with self.assertRaisesRegex(ValueError, 'genuinely linked module images differ'):
            self.export()

    def test_elf_function_contract_ignores_container_only_changes(self):
        other = self.root / 'build/other.o'
        elf_object(other, self.body, [('value', 0, 4, 'arm')])
        with other.open('ab') as stream:
            stream.write(b'path-only diagnostic trailer')
        self.assertNotEqual(digest(other), digest(self.obj))
        self.assertEqual(function_contract(other, 'value'), function_contract(self.obj, 'value'))

    def test_function_contract_detects_relocation_target_changes(self):
        def relocated(path, target):
            elf_object(path, bytes.fromhex('feffffeb'), [('value', 0, 4, 'arm')])
            raw = path.read_bytes()
            table = struct.unpack_from('<I', raw, 32)[0]
            sections = [list(struct.unpack_from('<IIIIIIIIII', raw, table + i * 40)) for i in range(5)]
            def body(index):
                section = sections[index]
                return raw[section[4]:section[4] + section[5]]
            strings, symbols, names = body(3), body(2), body(4)
            extern = len(symbols) // 16
            symbols += struct.pack('<IIIBBH', len(strings), 0, 0, 0x10, 0, 0)
            rel_name = len(names)
            names += b'.rel.text\0'
            strings += target.encode() + b'\0'
            sections.append([rel_name, 9, 0, 0, 0, 8, 2, 1, 4, 8])
            output = bytearray(raw[:table])
            for index, payload in ((2, symbols), (3, strings), (4, names), (5, struct.pack('<II', 0, extern << 8 | 28))):
                output.extend(bytes(-len(output) % 4))
                sections[index][4:6] = [len(output), len(payload)]
                output.extend(payload)
            output.extend(bytes(-len(output) % 4))
            at = len(output)
            output.extend(b''.join(struct.pack('<IIIIIIIIII', *s) for s in sections))
            struct.pack_into('<I', output, 32, at)
            struct.pack_into('<H', output, 48, len(sections))
            path.write_bytes(output)
        left, right = self.root / 'build/left.o', self.root / 'build/right.o'
        relocated(left, 'callee_one')
        relocated(right, 'callee_two')
        self.assertNotEqual(function_contract(left, 'value'), function_contract(right, 'value'))


if __name__ == '__main__':
    unittest.main()
