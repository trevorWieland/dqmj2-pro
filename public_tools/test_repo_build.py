"""Regression tests for repository-build compilation flags.

Thumb selection is a property of the source unit rule (``mode: thumb``), but the
way it is expressed depends on the compiler: mwccarm takes ``-thumb``, while
mwasmarm reads the ``.thumb`` directive in the source and rejects ``-thumb`` as
an unknown option.  These tests pin both halves of that contract: the flag
derivation for C/C++ versus assembly, and one real assembly compile of a
``mode: thumb`` unit with the pinned mwasmarm.
"""

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from repo_build import compile_all, compile_flags

ROOT = Path(__file__).resolve().parent.parent
MWASMARM = 'tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe'
MWASMARM_SHA256 = 'e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c'


class CompileFlagTests(unittest.TestCase):
    def test_thumb_c_source_gets_thumb_and_compile_only(self):
        flags = compile_flags(dict(path='src/main/thumb/unit.c', mode='thumb',
                                   profileFlags=['-proc', 'arm946e']))
        self.assertEqual(flags, ['-proc', 'arm946e', '-thumb', '-c'])

    def test_thumb_cpp_source_gets_thumb(self):
        flags = compile_flags(dict(path='src/main/thumb/unit.cpp', mode='thumb',
                                   profileFlags=['-proc', 'arm946e']))
        self.assertIn('-thumb', flags)

    def test_thumb_assembly_source_never_gets_thumb(self):
        flags = compile_flags(dict(path='src/verified_assembly/lane/ov006/thumb/unit.s', mode='thumb',
                                   profileFlags=['-proc', 'arm5TE', '-c']))
        self.assertEqual(flags, ['-proc', 'arm5TE', '-c'])

    def test_arm_source_never_gets_thumb(self):
        flags = compile_flags(dict(path='src/verified_assembly/lane/ov006/arm/unit.s', mode='arm',
                                   profileFlags=['-proc', 'arm946e']))
        self.assertEqual(flags, ['-proc', 'arm946e', '-c'])

    def test_existing_thumb_flag_is_not_duplicated(self):
        flags = compile_flags(dict(path='src/main/unit.c', mode='thumb',
                                   profileFlags=['-proc', 'arm946e', '-thumb', '-c']))
        self.assertEqual(flags.count('-thumb'), 1)


@unittest.skipUnless((ROOT / MWASMARM).is_file(), 'pinned mwasmarm is not present')
class ThumbAssemblyCompileTests(unittest.TestCase):
    """Compile a real ``mode: thumb`` .s unit through compile_all.

    The fixture carries the repository's twenty-module inventory (the build
    validates the denominator) and a one-row private ledger attributing the .s
    source to mwasmarm.  No game image is read: this exercises the compile path,
    which is exactly where the assembler rejected the spurious -thumb flag.
    """

    def setUp(self):
        container = ROOT / 'work/repo-build-tests'
        container.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=container)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        config = json.loads((ROOT / 'config/source_units.json').read_text(encoding='utf-8'))
        self.source = 'src/verified_assembly/lane/ov006/thumb/unit.s'
        self.write_source()
        self.write_compiler()
        self.write_config(config)
        self.write_ledger()

    def write_source(self):
        path = self.root / self.source
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            '.section .text\n'
            '.thumb\n'
            '.global thumb_probe\n'
            '.type thumb_probe, @function\n'
            'thumb_probe:\n'
            '    mov r0, #0\n'
            '    bx lr\n',
            encoding='utf-8')

    def write_compiler(self):
        # mwasmarm loads its DLLs from the directory beside the executable, so the
        # fixture needs the whole pinned compiler directory, not just the .exe.
        source_dir = (ROOT / MWASMARM).parent
        target_dir = (self.root / MWASMARM).parent
        target_dir.mkdir(parents=True, exist_ok=True)
        for source in source_dir.iterdir():
            if not source.is_file():
                continue
            target = target_dir / source.name
            try:
                os.link(source, target)
            except OSError:
                shutil.copyfile(source, target)

    def write_config(self, reference):
        module = reference['modules']['ov006']
        data = dict(
            schemaVersion=1,
            denominator=reference['denominator'],
            buildSha256=reference['buildSha256'],
            compiler=dict(path=MWASMARM, sha256=MWASMARM_SHA256),
            compilers={MWASMARM_SHA256: MWASMARM},
            modules=reference['modules'],
            flagProfiles={},
            rules=[dict(glob='src/verified_assembly/lane/ov006/thumb/**', module='ov006',
                        processor=module['processor'], loadAddressBase=module['loadAddressBase'],
                        originalImage=module['originalImage'], mode='thumb',
                        compilerFlags=['-proc', 'arm5TE', '-c'],
                        compilerSha256=MWASMARM_SHA256)],
            objects={},
            alternates={},
        )
        path = self.root / 'config/source_units.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding='utf-8')

    def write_ledger(self):
        row = dict(
            id='0' * 64 + '/arm9/ov006/thumb/021ebc2c',
            buildSha256='a' * 64,
            processor='arm9',
            module='ov006',
            address='0x21ebc2c',
            mode='thumb',
            symbol='thumb_probe',
            bytes=4,
            sourceUnit=self.source,
            compilerSha256=MWASMARM_SHA256,
            compilerFlags=['-proc', 'arm5TE', '-c'],
            sourceLanguage='assembly',
        )
        path = self.root / 'ledger/functions.jsonl'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(row) + '\n', encoding='utf-8')

    def test_thumb_assembly_compiles_without_the_thumb_flag(self):
        report = compile_all(self.root, self.root, self.root / 'work/compile', jobs=1,
                             sources=[self.source])
        self.assertEqual(report['status'], 'source-compilation-passed', report.get('failures'))
        self.assertEqual(report['compiledUnits'], 1)
        self.assertEqual(report['failedUnits'], 0)
        record = report['results'][0]
        self.assertEqual(record['source'], self.source)
        self.assertNotIn('-thumb', record['compilerFlags'])
        self.assertIn('-c', record['compilerFlags'])
        self.assertTrue((self.root / record['object']).is_file())


if __name__ == '__main__':
    unittest.main()
