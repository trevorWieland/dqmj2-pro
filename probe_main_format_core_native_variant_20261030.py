import os
import subprocess
from project import ROOT, configuration, native_dependencies, sha256, write_json
native_dependencies(configuration())
import match_runtime as compiler
from elftools.elf.elffile import ELFFile


def main():
    source = ROOT / 'nonmatching/main-runtime/20261030/format-core/native_main_0201cb74_no_hex_prefix.c'
    work = ROOT / 'work/main-runtime-20261030/format-core-native-variant'
    work.mkdir(parents=True, exist_ok=True)
    rows = []
    for level in [2, 3, 4]:
        for option in ['space', 'speed']:
            obj = work / f'O{level}-{option}.o'
            command = [str(compiler.COMPILER), *compiler.FLAGS, '-O' + str(level), '-opt', option, '-c', str(source), '-o', str(obj)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=60,
                env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
            row = {'level': level, 'option': option, 'exitCode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
            if result.returncode == 0:
                with obj.open('rb') as stream:
                    elf = ELFFile(stream)
                    symbol = elf.get_section_by_name('.symtab').get_symbol_by_name('native_main_0201cb74')[0]
                    row.update(compiledBytes=symbol['st_size'], object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj))
            rows.append(row)
    write_json(ROOT / 'evidence/attempts/main-format-core-native-variant-profiles-20261030.json',
        {'sourceCredit': 0, 'source': source.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(source), 'targetBytes': 2084,
         'nativePaddingRegion': ['0x0201d22c', '0x0201d2e0'], 'removedReferenceOnlyHexPrefixPadding': True, 'profiles': rows})
    print([{key: value for key, value in row.items() if key in ['level', 'option', 'exitCode', 'compiledBytes', 'stderr']} for row in rows])


if __name__ == '__main__':
    main()
