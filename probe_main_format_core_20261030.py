import os
import subprocess
from project import ROOT, configuration, native_dependencies, sha256, write_json
native_dependencies(configuration())
import match_runtime as compiler
from elftools.elf.elffile import ELFFile


def main():
    reference = ROOT / 'deps/references/zeldaret-tp-c8fa8c9e/libs/PowerPC_EABI_Support/MSL/MSL_C/MSL_Common/Src/printf.c'
    text = reference.read_text()
    enums = text[text.index('enum justification_options'):text.index('static const char* parse_format')]
    body = text[text.index('static int __pformatter'):text.index('static void* __FileWrite')]
    body = body.replace('static int __pformatter', 'int native_main_0201cb74')
    body = body.replace('void* (*WriteProc)', 'unsigned int (*WriteProc)')
    body = body.replace(',int is_secure', '')
    body = body.replace('(va_list*)arg', '&arg')
    header = """typedef unsigned int size_t;
typedef int ptrdiff_t;
typedef long long intmax_t;
typedef unsigned short wchar_t;
typedef char *va_list;
#define PLATFORM_GCN 0
#define is_secure 0
#define NULL 0
#define va_arg(ap, type) (*(type *)((ap += sizeof(type)) - sizeof(type)))
"""
    prototypes = """extern const char *parse_format(const char *, va_list *, print_format *);
extern char *long2str(long, char *, print_format);
extern char *longlong2str(long long, char *, print_format);
extern char *float2str(long double, char *, print_format);
extern char *double2hex(long double, char *, print_format);
extern unsigned int wcstombs(char *, const wchar_t *, unsigned int);
extern unsigned int strlen(const char *);
extern char *strchr(const char *, int);
extern void *memchr(const void *, int, unsigned int);
extern void __msl_runtime_constraint_violation_s(const char *, void *, int);
#define EINVAL 22
"""
    folder = ROOT / 'nonmatching/main-runtime/20261030/format-core'
    folder.mkdir(parents=True, exist_ok=True)
    draft = folder / 'reference-adaptation.input.c'
    draft.write_text(header + enums + prototypes + body, encoding='utf-8')
    clang = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin/clang.exe'
    result = subprocess.run([str(clang), '-E', '-P', '-x', 'c', str(draft)], capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    source = folder / 'native_main_0201cb74.c'
    source.write_text(result.stdout, encoding='utf-8')
    assert len(result.stdout.splitlines()) <= 500
    work = ROOT / 'work/main-runtime-20261030/format-core'
    work.mkdir(parents=True, exist_ok=True)
    records = []
    for level in [2, 3, 4]:
        for option in ['space', 'speed']:
            obj = work / f'O{level}-{option}.o'
            flags = [*compiler.FLAGS, '-O' + str(level), '-opt', option]
            result = subprocess.run([str(compiler.COMPILER), *flags, '-c', str(source), '-o', str(obj)], capture_output=True, text=True,
                timeout=60, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
            row = {'level': level, 'option': option, 'exitCode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
            if result.returncode == 0:
                with obj.open('rb') as stream:
                    elf = ELFFile(stream)
                    symbol = elf.get_section_by_name('.symtab').get_symbol_by_name('native_main_0201cb74')[0]
                    row.update(compiledBytes=symbol['st_size'], object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj))
            records.append(row)
    write_json(ROOT / 'evidence/attempts/main-format-core-reference-draft-20261030.json',
               {'sourceCredit': 0, 'source': source.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(source),
                'referenceSha256': sha256(reference), 'targetBytes': 2084, 'explicitSecureVariantDisabled': True,
                'armWordVaListAndEnumLayoutHypotheses': True, 'profiles': records})
    print([{key: value for key, value in row.items() if key in ['level', 'option', 'exitCode', 'compiledBytes', 'stderr']} for row in records])


if __name__ == '__main__':
    main()
