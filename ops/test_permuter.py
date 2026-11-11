"""Regression tests for the decomp-permuter adapter (ops/permuter.py, ops/mwcc_objdump.py).

These run without a ROM, without the mwccarm toolchain and without a decomp-permuter
checkout: they cover the generated workspace files and the pure helpers. The end-to-end
behaviour (image -> target.o -> permuter -> byte+reloc acceptance) needs all three and is
exercised by the workflow in docs/authoring/permuter.md.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import permuter  # noqa: E402


class FunctionNameTest(unittest.TestCase):
    def test_last_definition_wins(self):
        source = '''typedef unsigned int u32;
extern u32 native_fn_02002480(u16 value, s32 mode);
u32 helper(u32 x)
{
    return x;
}
u32 native_ov006_021fb384(u32 value)
{
    return helper(value) - -value;
}
'''
        self.assertEqual(permuter.detect_function_name(source), 'native_ov006_021fb384')

    def test_prototypes_are_not_definitions(self):
        source = 's32 native_ov006_02203ebc(u32 mask);\ns32 native_ov006_02203ebc(u32 mask)\n{\n}\n'
        self.assertEqual(permuter.detect_function_name(source), 'native_ov006_02203ebc')

    def test_pointer_return_type(self):
        source = 'u8 *native_ov006_02000000(void)\n{\n    return 0;\n}\n'
        self.assertEqual(permuter.detect_function_name(source), 'native_ov006_02000000')

    def test_missing_definition_is_reported(self):
        with self.assertRaises(SystemExit):
            permuter.detect_function_name('extern int x;\n')


class SettingsTest(unittest.TestCase):
    def test_literal_command_string_and_func_name(self):
        command = "C:/Python/python.exe C:/repo/ops/mwcc_objdump.py --mode thumb"
        text = permuter.settings_file('native_ov006_02203ebc', command,
                                      {'perm_commutative': 25})
        self.assertIn('func_name = "native_ov006_02203ebc"', text)
        self.assertIn('compiler_type = "mwcc"', text)
        # TOML literal string: shlex must see forward slashes and no escapes.
        self.assertIn(f"objdump_command = '{command}'", text)
        self.assertIn('perm_commutative = 25', text)

    def test_weights_render_as_integers_or_floats(self):
        text = permuter.settings_file('f', 'x', {'a': 100.0, 'b': 0.5})
        self.assertIn('a = 100', text)
        self.assertIn('b = 0.5', text)


class CompileScriptTest(unittest.TestCase):
    def test_thumb_precedes_c_and_uses_positional_args(self):
        script = permuter.compile_script('C:/tools/mwccarm.exe', ['-O2', '-proc', 'arm946e'],
                                         True, 'C:/tools/license.dat')
        self.assertIn('-thumb', script)
        self.assertLess(script.index('-thumb'), script.index('-c'))
        self.assertIn('"$1"', script)
        self.assertIn('"$3"', script)
        self.assertIn('LM_LICENSE_FILE', script)

    def test_arm_mode_has_no_thumb_flag(self):
        script = permuter.compile_script('C:/tools/mwccarm.exe', ['-O2'], False, 'C:/l.dat')
        self.assertNotIn('-thumb', script)


class PathTest(unittest.TestCase):
    def test_toml_path_uses_forward_slashes(self):
        self.assertEqual(permuter.toml_path(Path(r'C:\a\b\c.py')), 'C:/a/b/c.py')


class OutputParsingTest(unittest.TestCase):
    def test_status_stream_is_cleaned_and_scores_extracted(self):
        raw = ('[f] base score = 10\n'
               'iteration 1, 0 errors, score = 200\r'
               '\b\b\b\b\b iteration 2, 1 errors, score = inf\r   \n'
               'wrote to .\\output-0-1\n'
               'wrote to .\\output-5-1\n')
        clean = permuter.ANSI.sub('', raw)
        self.assertNotIn('\r', clean)
        self.assertNotIn('\b', clean)
        self.assertEqual(permuter.re.search(r'base score = (-?\d+)', clean).group(1), '10')
        outputs = permuter.re.findall(r'wrote to .*?output-(-?\d+)-(\d+)', clean)
        self.assertEqual(outputs, [('0', '1'), ('5', '1')])
        iterations = [int(value) for value in permuter.re.findall(r'iteration (\d+),', clean)]
        self.assertEqual(max(iterations), 2)


class ObjectFormatTest(unittest.TestCase):
    def test_relocation_names_cover_the_mwcc_kinds(self):
        # The three kinds decomp-permuter's ARM parser accepts must be spelled its way,
        # and the shim must name THM_JUMP24 (mwcc's Thumb BLX) rather than let it fall
        # through to an assertion inside the parser.
        import mwcc_objdump
        self.assertEqual(mwcc_objdump.RELOCATION_NAMES[2], 'R_ARM_ABS32')
        self.assertEqual(mwcc_objdump.RELOCATION_NAMES[10], 'R_ARM_THM_CALL')
        self.assertEqual(mwcc_objdump.RELOCATION_NAMES[28], 'R_ARM_CALL')
        self.assertIn('R_ARM_THM_JUMP24', mwcc_objdump.RELOCATION_NAMES.values())
        self.assertEqual(mwcc_objdump.SUPPORTED_RELOCATIONS,
                         {'R_ARM_ABS32', 'R_ARM_THM_CALL', 'R_ARM_CALL'})

    def test_mapping_symbols_split_code_and_data(self):
        import mwcc_objdump
        text = bytes(20)
        regions = mwcc_objdump.regions(text, [(0, 'thumb'), (12, 'data')], 'arm')
        self.assertEqual(regions, [(0, 12, 'thumb'), (12, 20, 'data')])

    def test_no_mapping_symbols_means_one_region(self):
        import mwcc_objdump
        self.assertEqual(mwcc_objdump.regions(bytes(8), [], 'arm'), [(0, 8, 'arm')])


class PermuterLocationTest(unittest.TestCase):
    def test_error_explains_how_to_acquire(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            with self.assertRaises(SystemExit) as caught:
                permuter.find_permuter(root)
            message = str(caught.exception)
            self.assertIn(permuter.PERMUTER_PIN, message)
            self.assertIn('work/decomp-permuter', message)


if __name__ == '__main__':
    unittest.main()
