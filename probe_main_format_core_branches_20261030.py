import os
import re
import subprocess
from project import ROOT, configuration, native_dependencies, sha256, write_json
native_dependencies(configuration())
import match_runtime as compiler
import link_runtime_unit as linker
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM


def main():
    folder = ROOT / 'nonmatching/main-runtime/20261030/format-core'
    source = (folder / 'native_main_0201cb74_ptrdiff_long.c').read_text()
    block = """                if (!(buff_ptr = longlong2str(long_long_num, buff + 512, format))) {
                    goto conversion_error;
                }"""
    assert source.count(block) == 2
    variants = {'separate': """                buff_ptr = longlong2str(long_long_num, buff + 512, format);
                if (buff_ptr == 0) goto conversion_error;""",
                'inverted': """                if ((buff_ptr = longlong2str(long_long_num, buff + 512, format)) != 0) {
                } else {
                    goto conversion_error;
                }""",
                'unbraced': """                if (!(buff_ptr = longlong2str(long_long_num, buff + 512, format)))
                    goto conversion_error;""",
                'explicit_equal': """                if ((buff_ptr = longlong2str(long_long_num, buff + 512, format)) == 0) {
                    goto conversion_error;
                }"""}
    clean = re.sub(r'                if \(0 && wcs_ptr == 0\)\{.*?                }\n', '', source, flags=re.S)
    clean = re.sub(r'            if \(0(?: && buff_ptr == 0)?\)\{.*?            }\n', '', clean, flags=re.S)
    bodies = {name: source.replace(block, value) for name, value in variants.items()}
    bodies['remove_secure'] = clean
    metadata, binary, config = linker.measured_module('main')
    native = binary[0x1CB74:0x1D390]
    def canonical(blob):
        values = []
        for instruction in Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(blob, 0):
            text = instruction.mnemonic + ' ' + instruction.op_str
            if instruction.mnemonic.startswith('b') and instruction.op_str.startswith('#'):
                text = instruction.mnemonic + ' TARGET'
            values.append(text)
        return values
    original = canonical(native)
    rows = []
    work = ROOT / 'work/main-runtime-20261030/format-core-branches'
    work.mkdir(parents=True, exist_ok=True)
    for label, text in bodies.items():
        path = folder / ('native_main_0201cb74_' + label + '.c')
        path.write_text(text, encoding='utf-8')
        obj = work / (label + '.o')
        command = [str(compiler.COMPILER), *compiler.FLAGS, '-O3', '-opt', 'speed', '-c', str(path), '-o', str(obj)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=60,
            env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
        assert result.returncode == 0, result.stdout + result.stderr
        with obj.open('rb') as stream:
            elf = ELFFile(stream)
            symbol = elf.get_section_by_name('.symtab').get_symbol_by_name('native_main_0201cb74')[0]
            body = elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']]
        values = canonical(body[:-8])
        differences = [index * 4 for index, (a, b) in enumerate(zip(original, values)) if a != b]
        rows.append({'variant': label, 'source': path.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(path),
                     'object': obj.relative_to(ROOT).as_posix(), 'objectSha256': sha256(obj), 'compiledBytes': len(body),
                     'instructionCountDifference': len(values) - len(original), 'branchTargetNormalizedDifferences': differences})
    write_json(ROOT / 'evidence/attempts/main-format-core-branch-profiles-20261030.json', {'sourceCredit': 0, 'rows': rows})
    print([{k: v for k, v in row.items() if k in ['variant', 'compiledBytes', 'instructionCountDifference', 'branchTargetNormalizedDifferences']} for row in rows])


if __name__ == '__main__':
    main()
