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
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from repo_build import (RepositoryBuildError, compile_all, compile_flags,
                        encode_thumb_branch, patch_function)

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


class Xpc22PatchTests(unittest.TestCase):
    """R_ARM_THM_XPC22 (kind 16) must encode BLX or BL from the measured site.

    Each case uses a real measured call site and image word.  The patcher may
    not infer the form from the compiler's placeholder (mwasmarm always emits
    the BL spelling), and BLX must use Align(PC+4,4) while BL uses PC+4.
    """

    BASE = 0x021D7240

    def patch(self, function_address, size, where, target, image_word,
              kind=16, image_size=None):
        site = function_address + where
        offset = site - self.BASE
        image = bytearray(image_size or offset + 4)
        struct.pack_into('<I', image, offset, image_word)
        function = dict(name='native_probe', value=0, size=size, section=4,
                        address=function_address, mode='thumb', bytes=bytearray(size))
        relocations = {4: [dict(where=where, type=kind, addend=-4,
                                symbol=dict(name=target, shndx=0))]}
        return patch_function(function, dict(name='ov006', symbols={}, by_address={}, runtime={}),
                              self.BASE, [], relocations, bytes(image))

    def test_thm_xpc22_to_arm_uses_blx_with_aligned_base(self):
        # Real site 0x021EDE7A -> ARM 0x02008008; image word 0xE8C6F61A.
        # site + 4 is not 4-aligned, so the BLX base is Align(site + 4, 4).
        site = 0x021EDE7A
        self.assertNotEqual((site + 4) & ~3, site + 4)
        patched, unresolved, sources, outside = self.patch(
            0x021EDE50, 196, 0x2A, 'native_fn_02008008', 0xE8C6F61A)
        self.assertEqual(unresolved, [])
        self.assertEqual(sources['name'], 1)
        self.assertEqual(patched[0x2A:0x2E], struct.pack('<I', 0xE8C6F61A))
        second = struct.unpack_from('<H', patched, 0x2C)[0]
        self.assertEqual(second & 0xD000, 0xC000, 'BLX clears second-halfword bit 12')

    def test_thm_xpc22_to_thumb_uses_bl(self):
        # Real site 0x021F7212 -> Thumb 0x021F52CC; image word 0xF85BF7FE.
        patched, unresolved, sources, outside = self.patch(
            0x021F7212, 4, 0, 'native_fn_021F52CC', 0xF85BF7FE)
        self.assertEqual(unresolved, [])
        self.assertEqual(patched, struct.pack('<I', 0xF85BF7FE))
        second = struct.unpack_from('<H', patched, 2)[0]
        self.assertEqual(second & 0xD000, 0xD000, 'BL keeps second-halfword bit 12')

    def test_thm_xpc22_negative_control_mode_changes_the_word(self):
        # The same ARM-target site encoded as Thumb (BL) must not reproduce the
        # measured BLX word: the site's marker, not a default, decides the form.
        first, second = encode_thumb_branch(0x021EDE7A, 0x02008008, -4, False)
        self.assertNotEqual((first, second), (0xF61A, 0xE8C6))
        self.assertEqual(second & 0xD000, 0xD000, 'the BL form keeps bit 12 set')

    def test_unknown_relocation_kind_fails_loudly(self):
        with self.assertRaises(RepositoryBuildError) as raised:
            self.patch(0x021EDE50, 196, 0x2A, 'native_fn_02008008', 0xE8C6F61A, kind=99)
        message = str(raised.exception)
        self.assertIn('Unsupported relocation kind 99', message)
        self.assertIn('0x021ede7a', message)


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
