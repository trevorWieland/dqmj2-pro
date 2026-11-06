import os
import struct
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import ROOT, write_json, sha256
from link_runtime_unit import ELFFile
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA

WORK = ROOT / 'work/windows-target-layout-20261101'
SOURCE = ROOT / 'nonmatching/portability/20261101-layout-probe/probe.c'
FIELDS = ['u32Bytes', 'pointerBytes', 'u64Bytes', 'doubleBytes', 'longDoubleBytes',
    'wideSize', 'wideValueOffset', 'wideTailOffset', 'floatSize', 'floatValueOffset',
    'floatTailOffset', 'pointerStructSize', 'pointerValueOffset', 'pointerTailOffset',
    'nestedSize', 'nestedValueOffset', 'nestedTailOffset']


def elf_values(path):
    with path.open('rb') as stream:
        elf = ELFFile(stream)
        assert elf.little_endian
        symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols()
            if symbol.name.lstrip('_') == 'j2p_layout_probe')
        data = elf.get_section(symbol['st_shndx']).data()
        offset = symbol['st_value']
        return list(struct.unpack('<17I', data[offset:offset + 68]))


def coff_values(path):
    data = path.read_bytes()
    machine, sections, stamp, offset, count, optional, flags = struct.unpack_from('<HHIIIHH', data)
    assert machine == 0x14C
    strings = offset + count * 18
    index = 0
    while index < count:
        start = offset + index * 18
        raw = data[start:start + 8]
        if raw[:4] == bytes(4):
            address = strings + struct.unpack_from('<I', raw, 4)[0]
            name = data[address:data.find(b'\0', address)].decode()
        else:
            name = raw.rstrip(b'\0').decode()
        value, section = struct.unpack_from('<Ih', data, start + 8)
        if name.lstrip('_') == 'j2p_layout_probe':
            base = 20 + optional + (section - 1) * 40
            raw_pointer = struct.unpack_from('<I', data, base + 20)[0]
            return list(struct.unpack_from('<17I', data, raw_pointer + value))
        index += 1 + data[start + 17]
    raise ValueError('Missing measured layout data')


def main():
    text = '''typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned long long u64;
typedef struct { u8 lead; u64 value; u8 tail; } Wide;
typedef struct { u8 lead; double value; u8 tail; } Float;
typedef struct { u8 lead; void *value; u8 tail; } Pointer;
typedef struct { u8 lead; Wide value; u8 tail; } Nested;
#define OFFSET(type, field) ((u32)&(((type *)0)->field))
const u32 j2p_layout_probe[17] = {
    sizeof(u32), sizeof(void *), sizeof(u64), sizeof(double), sizeof(long double),
    sizeof(Wide), OFFSET(Wide, value), OFFSET(Wide, tail),
    sizeof(Float), OFFSET(Float, value), OFFSET(Float, tail),
    sizeof(Pointer), OFFSET(Pointer, value), OFFSET(Pointer, tail),
    sizeof(Nested), OFFSET(Nested, value), OFFSET(Nested, tail)
};
'''
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    if SOURCE.exists():
        assert SOURCE.read_text() == text
    SOURCE.write_text(text, encoding='utf-8')
    WORK.mkdir(parents=True, exist_ok=True)
    environment = {key: value for key, value in os.environ.items()
        if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    environment['LM_LICENSE_FILE'] = str(ROOT / 'tools/mwccarm/mwccarm/license.dat')
    steps, targets = [], []

    def run(command):
        command = list(map(str, command))
        result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
            timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
        steps.append(dict(command=command, exitCode=result.returncode,
            stdout=result.stdout.decode(errors='replace'), stderr=result.stderr.decode(errors='replace')))
        assert result.returncode == 0, steps[-1]

    for number, profile in enumerate(['1.2/base', '2.0/base', '2.0/sp1p5', '2.0/sp1p6']):
        compiler = ROOT / f'tools/mwccarm/mwccarm/{profile}/mwccarm.exe'
        obj = WORK / f'arm-{number}.o'
        run([compiler, '-O2', '-enum', 'int', '-char', 'signed', '-proc', 'arm946e',
            '-gccinc', '-nolink', '-c', SOURCE, '-o', obj])
        targets.append(dict(profile=profile, compilerSha256=sha256(compiler), objectSha256=sha256(obj),
            values=dict(zip(FIELDS, elf_values(obj)))))
    clang = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin/clang.exe'
    assert sha256(clang) == CLANG_SHA
    windows = []
    for name, flags in [('default', []), ('pack4', ['-fpack-struct=4'])]:
        obj = WORK / (name + '.obj')
        run([clang, '--target=i686-pc-windows-msvc', '-std=c11', '-O2', '-ffreestanding',
            '-fno-builtin', *flags, '-c', SOURCE, '-o', obj])
        windows.append(dict(profile=name, compilerSha256=sha256(clang), objectSha256=sha256(obj),
            values=dict(zip(FIELDS, coff_values(obj)))))
    values = targets[0]['values']
    all_arm_equal = all(target['values'] == values for target in targets)
    same = {row['profile']: row['values'] == values for row in windows}
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        source=dict(path=SOURCE.relative_to(ROOT).as_posix(), sha256=sha256(SOURCE)),
        passed=True, targetProfilesAgree=all_arm_equal, windowsMatchesMeasuredTarget=same,
        armTargets=targets, windows=windows, steps=steps, sourceCredit=0, nativeGameExecutionCount=0,
        limitations=['Compile-time object-layout measurements only; no game function, hardware or application is executed',
            'These representative primitive/nested records do not prove every game layout or compiler-version uniqueness',
            'Explicit source layout assertions and subsequent native tests remain required'])
    output = ROOT / 'evidence/portability/windows-target-layout-20261101.json'
    write_json(output, report)
    print(dict(armProfilesAgree=all_arm_equal, windowsProfilesMatch=same, target=values, sourceCredit=0))


if __name__ == '__main__':
    main()
