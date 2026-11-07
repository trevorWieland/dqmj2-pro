import copy
import hashlib
import json
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from elf_metadata import inspect
from public_manifest import ManifestError, compiler_flags, digest, verify


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.container = Path(__file__).resolve().parent.parent / "build/public-tools-tests"
        self.container.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=self.container)
        self.root = Path(self.temporary.name).resolve()
        self.assertTrue(self.root.is_relative_to(self.container.resolve()))
        (self.root / "src").mkdir()
        (self.root / "public").mkdir()
        (self.root / "src/value.c").write_text('#include "value.h"\nint value(void){return VALUE;}\n', encoding="utf-8")
        (self.root / "src/value.h").write_text("#define VALUE 7\n", encoding="utf-8")
        self.row = dict(id="sample/arm9/main/arm/02000000", buildSha256="a" * 64, processor="arm9", module="main", mode="arm",
                        address="0x02000000", bytes=8, symbol="original_value", sourceUnit="src/value.c",
                        sourceSha256=digest(self.root / "src/value.c"), sourceDependencies=[dict(path="src/value.h", sha256=digest(self.root / "src/value.h"))],
                        compilerSha256="b" * 64, compilerFlags=["-O2", "-proc", "arm946e", "-inline", "off"],
                        states=dict(functionMatched=True, moduleLinked=True), object="inputs/absent-private-object.o")
        self.manifest = dict(schemaVersion=1, revision="c" * 40, romSha256="a" * 64, initializedDenominatorBytes=100,
                             acceptedInitializedBytes=8, functions=[self.row])
        self.path = self.root / "public/accepted-functions.json"
        self.save()

    def tearDown(self):
        self.assertTrue(self.root.is_relative_to(self.container.resolve()))
        self.temporary.cleanup()

    def save(self):
        self.path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_valid_without_originals_or_objects(self):
        unused, units, pins, result = verify(self.root, self.path)
        self.assertEqual(len(units), 1)
        self.assertEqual(len(pins), 2)
        self.assertFalse(result["originalInputsRead"])
        self.assertFalse(result["nativeMatchingVerified"])

    def test_required_prototypes_preserve_strict_warnings_and_reject_file_options(self):
        flags = ['-O2', '-requireprotos', '-w', 'error']
        actual, directories = compiler_flags(self.root, flags)
        self.assertEqual(actual, flags)
        self.assertEqual(directories, [])
        with self.assertRaises(ManifestError):
            compiler_flags(self.root, [*flags, '@private-options.txt'])

    def test_changed_header_rejected(self):
        (self.root / "src/value.h").write_text("#define VALUE 9\n", encoding="utf-8")
        with self.assertRaisesRegex(ManifestError, "hash mismatch"):
            verify(self.root, self.path)

    def test_unpinned_include_rejected(self):
        self.row["sourceDependencies"] = []
        self.save()
        with self.assertRaisesRegex(ManifestError, "lacks a declared hash"):
            verify(self.root, self.path)

    def test_macro_include_is_not_silently_closed(self):
        (self.root / "src/value.c").write_text('#define HEADER "value.h"\n#include HEADER\nint value(void){return VALUE;}\n', encoding="utf-8")
        self.row["sourceSha256"] = digest(self.root / "src/value.c")
        self.save()
        with self.assertRaisesRegex(ManifestError, "Macro-expanded includes"):
            verify(self.root, self.path)

    def test_private_and_escaping_source_paths_rejected(self):
        for value in ["../value.c", "inputs/value.c", "extract/value.c", "C:/value.c"]:
            self.row["sourceUnit"] = value
            self.save()
            with self.assertRaises(ManifestError):
                verify(self.root, self.path)

    def test_unaccepted_and_duplicate_rows_rejected(self):
        self.row["states"]["functionMatched"] = False
        self.save()
        with self.assertRaises(ManifestError):
            verify(self.root, self.path)
        self.row["states"]["functionMatched"] = True
        self.manifest["functions"].append(copy.deepcopy(self.row))
        self.save()
        with self.assertRaisesRegex(ManifestError, "Duplicate"):
            verify(self.root, self.path)

    def test_overlay_namespaces_are_distinct(self):
        row = copy.deepcopy(self.row)
        row.update(id="sample/arm9/ov001/arm/02000000", module="ov001")
        self.manifest["functions"].append(row)
        self.save()
        unused, units, pins, summary = verify(self.root, self.path)
        self.assertEqual(summary["acceptedFunctionsDeclared"], 2)
        self.assertEqual(len(units), 1)

    def test_output_response_and_forced_input_flags_rejected(self):
        for value in [["-o", "src/value.c"], ["@flags.txt"], ["-include", "inputs/native.bin"]]:
            self.row["compilerFlags"] = value
            self.save()
            with self.assertRaisesRegex(ManifestError, "Unsupported"):
                verify(self.root, self.path)

    def test_cross_directory_cli(self):
        script = Path(__file__).resolve().parent / "verify_sources.py"
        process = subprocess.run([sys.executable, str(script), "--root", str(self.root)], cwd=self.container,
                                 capture_output=True, text=True, timeout=20)
        self.assertEqual(process.returncode, 0, process.stderr + process.stdout)
        self.assertEqual(json.loads(process.stdout)["status"], "source-integrity-passed")


class ElfTests(unittest.TestCase):
    def object_bytes(self, machine=40, function_size=4):
        names = b"\0.text\0.shstrtab\0.strtab\0.symtab\0"
        strings = b"\0$a\0value\0"
        code = bytes.fromhex("1eff2fe1")
        symbols = bytes(16) + struct.pack("<IIIBBH", 1, 0, 0, 0, 0, 1) + struct.pack("<IIIBBH", 4, 0, function_size, 18, 0, 1)
        offsets = [52, 56, 56 + len(names), 56 + len(names) + len(strings)]
        table = offsets[3] + len(symbols)
        header = struct.pack("<16sHHIIIIIHHHHHH", b"\x7fELF\x01\x01\x01" + bytes(9), 1, machine, 1, 0, 0, table, 0, 52, 0, 0, 40, 5, 2)
        sections = [bytes(40), struct.pack("<IIIIIIIIII", 1, 1, 6, 0, offsets[0], 4, 0, 0, 4, 0),
                    struct.pack("<IIIIIIIIII", 7, 3, 0, 0, offsets[1], len(names), 0, 0, 1, 0),
                    struct.pack("<IIIIIIIIII", 17, 3, 0, 0, offsets[2], len(strings), 0, 0, 1, 0),
                    struct.pack("<IIIIIIIIII", 25, 2, 0, 0, offsets[3], len(symbols), 3, 2, 4, 16)]
        return header + code + names + strings + symbols + b"".join(sections)

    def test_generated_metadata_and_malformed_objects(self):
        container = Path(__file__).resolve().parent.parent / "build/public-tools-tests"
        container.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=container) as temporary:
            path = Path(temporary).resolve() / "fixture.o"
            self.assertTrue(path.is_relative_to(container.resolve()))
            path.write_bytes(self.object_bytes())
            result = inspect(path)
            self.assertEqual(result["functions"][0]["name"], "value")
            self.assertEqual(result["functions"][0]["mode"], "arm")
            self.assertFalse(result["nativeMatchingVerified"])
            for raw in [self.object_bytes(machine=183), self.object_bytes(function_size=8), self.object_bytes()[:51]]:
                path.write_bytes(raw)
                with self.assertRaises(ValueError):
                    inspect(path)


if __name__ == "__main__":
    unittest.main()
