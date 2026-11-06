import subprocess
from project import ROOT, configuration, native_dependencies, write_json
native_dependencies(configuration())
import match_runtime as compiler


def main():
    text = (ROOT / 'deps/references/zeldaret-tp-c8fa8c9e/libs/PowerPC_EABI_Support/MSL/MSL_C/MSL_Common/Src/printf.c').read_text()
    start = text.index('static char* long2str')
    begin = text.index('{', start)
    depth, end = 1, begin + 1
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    body = text[start:end].replace('static char* long2str', 'char* native_main_0201b8c8')
    prefix = (ROOT / 'src/runtime/20261030_format_core/native_main_0201cb74.c').read_text().split('typedef char NdsFormatterAbiRequired')[0]
    work = ROOT / 'work/main-integer-formatter-20261030'
    work.mkdir(parents=True, exist_ok=True)
    draft = work / 'reference.input.c'
    draft.write_text(prefix + '\n#define PLATFORM_GCN 0\n' + body, encoding='utf-8')
    clang = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin/clang.exe'
    result = subprocess.run([str(clang), '-E', '-P', '-x', 'c', str(draft)], capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    source = ROOT / 'nonmatching/main-runtime/20261030/integer-formatter/native_main_0201b8c8.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(result.stdout, encoding='utf-8')
    rows = []
    for level in ['2', '3', '4']:
        for speed in [False, True]:
            compiler.WORK = work / ('O' + level + ('-speed' if speed else '-space'))
            try:
                values, unused = compiler.compare(source, 'main', level, 'off', speed)
                assert len(values) == 1
                rows.append(dict(values[0], level=level, speed=speed))
            except ValueError as error:
                rows.append({'level': level, 'speed': speed, 'failed': str(error)})
    write_json(ROOT / 'evidence/attempts/main-integer-formatter-profiles-20261030.json', {'sourceCredit': 0, 'matches': rows})
    print([{k: v for k, v in row.items() if k in ['level', 'speed', 'compiledBytes', 'matchingBytes', 'exactAfterDeclaredRelocation', 'failed']} for row in rows])


if __name__ == '__main__':
    main()
