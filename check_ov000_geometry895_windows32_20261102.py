import hashlib
import json
import struct
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import ROOT, read_json, write_json, sha256
import ov000_geometry877_model_20261102 as G

PORT = ROOT / 'ports/windows-geometry895'
WORK = ROOT / 'work/ol895-windows'
TOOLS = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
SOURCES = [('preferred', 'nonmatching/overlay-lane/20261102-geometry876/021dbc18/whole-q12/source.c'), ('wrong-return', 'nonmatching/overlay-lane/20261102-geometry877/wrong-return/source.c'), ('wrong-point', 'nonmatching/overlay-lane/20261102-geometry877/wrong-point/source.c'), ('wrong-divisor', 'nonmatching/overlay-lane/20261102-geometry877/wrong-divisor/source.c')]


def word(value):
    return value & 0xFFFFFFFF


def put(page, offset, values):
    struct.pack_into('<' + 'I' * len(values), page, offset, *map(word, values))


def vectors():
    chunks = [struct.pack('<I', len(G.profiles()))]
    expected = []
    for p in G.profiles():
        page = bytearray(4096)
        sx, sz = p.get('slopeX', 0), p.get('slopeZ', 0)
        sign = -1 if p['reverse'] else 1
        mag = p['normalMagnitude']
        normal = [sign * sx * mag, -sign * mag, sign * sz * mag]
        if p['zeroNormal']:
            normal = [0, 0, 0]
        vertices = [(-8192, -8192), (8192, -8192), (0, 8192)]
        if p['reverse']:
            vertices[1], vertices[2] = vertices[2], vertices[1]
        put(page, 0xC, [0x100])
        put(page, 0x100, normal)
        for index, (x, z) in enumerate(vertices):
            put(page, 0x10C + index * 12, [x, sx * x + sz * z, z])
        page[0x142] = p['flag']
        put(page, 0x200, p['point'])
        page[0x231] = p['count'] & 255
        poison = [0xA5A51234, 0x76543210, 0x87654321]
        put(page, 0x240, poison)
        header = [*p['point'], sx, sz, mag, int(p['reverse']), int(p['zeroNormal']), p['flag'], p['mask'], p['count'], int(p['nullOutput']), p['ordinal']]
        chunks.append(struct.pack('<13I', *map(word, header)) + page)
        x, y, z = p['point']
        targetY = sx * x + sz * z
        travel = y + 4096 - targetY
        hit = p['count'] > 0 and not p['zeroNormal'] and bool(p['flag'] & p['mask']) and travel >= 0 and travel * travel // 4096 <= 0x4000 and G.B.inside(x, z)
        out = [word(x), word(targetY), word(z)] if hit and not p['nullOutput'] else poison
        put(page, 0x240, out)
        callback = [0x02500220, 0, 0x02500100, 0x02500000] if hit else [0] * 4
        eligible = p['count'] > 0 and not p['zeroNormal'] and bool(p['flag'] & p['mask'])
        normalY = mag if p['reverse'] else -mag
        division = [int(eligible), word((-travel * normalY) // 4096) if eligible else 0, word(-normalY) if eligible else 0]
        expected.append(struct.pack('<14I', p['ordinal'], int(hit), *out, int(hit), *callback, 0, *division) + page)
    return b''.join(chunks), expected


def build(label, path):
    folder = WORK / label
    folder.mkdir(parents=True, exist_ok=True)
    kernel = folder / 'kernel.c'
    kernel.write_bytes(path.read_bytes())
    kernel.with_name('context.h').write_bytes((PORT / 'context.h').read_bytes())
    if sha256(kernel) != sha256(path):
        raise ValueError('895 source-body copy differs')
    definition = folder / 'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nGetStdHandle@4\nReadFile@20\nWriteFile@20\nVirtualAlloc@16\nVirtualFree@12\nExitProcess@4\n', encoding='ascii')
    library = folder / 'kernel32.lib'
    commands = [[str(TOOLS / 'llvm-dlltool.exe'), '-m', 'i386', '-k', '-d', str(definition), '-l', str(library)]]
    objects = []
    for index, source in enumerate([kernel, PORT / 'driver.c']):
        obj = folder / f'unit{index}.obj'
        objects.append(obj)
        commands.append([str(TOOLS / 'clang.exe'), '--driver-mode=cl', '--target=i686-pc-windows-msvc', '/TC', '/std:c11', '/O2', '/GS-', '/Zl', '/Brepro', '/clang:-ffreestanding', '/clang:-fno-builtin', '/clang:-fno-strict-aliasing', '/w', '/c', str(source), '/Fo' + str(obj)])
    executable = folder / 'geometry.exe'
    commands.append([str(TOOLS / 'ld.lld.exe'), '-flavor', 'link', '/entry:entry', '/subsystem:console', '/machine:x86', '/nodefaultlib', '/timestamp:0', '/fixed', '/base:0x00400000', '/out:' + str(executable), *map(str, objects), str(library)])
    for command in commands:
        run = subprocess.run(command, cwd=ROOT, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=60)
        if run.returncode:
            failure = dict(command=command, exitCode=run.returncode, stdout=run.stdout.decode(errors='replace'), stderr=run.stderr.decode(errors='replace'), sourceCredit=0)
            write_json(ROOT / 'evidence/attempts' / f'geometry895-{label}-build-rejected-20261102.json', failure)
            raise ValueError(failure)
    data = executable.read_bytes()
    pe = struct.unpack_from('<I', data, 0x3C)[0]
    if struct.unpack_from('<H', data, pe + 4)[0] != 0x14C or struct.unpack_from('<I', data, pe + 8)[0] != 0:
        raise ValueError('895 PE32 architecture/timestamp differs')
    if any(struct.unpack_from('<I', obj.read_bytes(), 4)[0] != 0 for obj in objects):
        raise ValueError('895 nondeterministic COFF timestamp')
    return executable, dict(sourceInput=dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)), unmodifiedSourceBytes=True, portableHeaderSha256=sha256(PORT / 'context.h'), driverSha256=sha256(PORT / 'driver.c'), compilerCommands=commands, objects=[dict(path=obj.relative_to(ROOT).as_posix(), sha256=sha256(obj)) for obj in objects], executable=dict(path=executable.relative_to(ROOT).as_posix(), sha256=sha256(executable)), machine='I386', peTimestamp=0)


def main():
    if sys.version_info[:3] != (3, 13, 5):
        raise ValueError('895 pinned Python differs')
    for pin in read_json(ROOT / 'evidence/verification/geometry895-inputs-20261102.json')['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError(('895 frozen input differs', pin['path']))
    receipt = read_json(ROOT / 'evidence/verification/geometry895-windows-tools-import-20261102.json')
    for row in receipt['files']:
        if sha256(ROOT / row['path']) != row['sha256']:
            raise ValueError(('895 local tool differs', row['path']))
    payload, expected = vectors()
    native = read_json(ROOT / 'evidence/ports/geometry895-native-contract-20261102.json')
    nativeRejects = native['nativeWrongFullContractRejects']
    if len(expected) != native['cases'] or sha256(ROOT / SOURCES[0][1]) != native['preferredSourceSha256']:
        raise ValueError('895 extracted native contract differs')
    results = []
    for label, name in SOURCES:
        executable, built = build(label, ROOT / name)
        runs = []
        for iteration in range(2 if label == 'preferred' else 1):
            run = subprocess.run([str(executable)], input=payload, cwd=ROOT.parent, capture_output=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
            if run.returncode != 0 or len(run.stdout) != 4152 * len(expected):
                failure = dict(label=label, iteration=iteration, exitCode=run.returncode, outputBytes=len(run.stdout), stderr=run.stderr.decode(errors='replace'), sourceCredit=0)
                write_json(ROOT / 'evidence/attempts' / f'geometry895-{label}-execution-rejected-20261102.json', failure)
                raise ValueError(failure)
            rejected = sum(run.stdout[index * 4152:(index + 1) * 4152] != wanted for index, wanted in enumerate(expected))
            outputRejected = sum(run.stdout[index * 4152:index * 4152 + 44] != wanted[:44] or run.stdout[index * 4152 + 56:(index + 1) * 4152] != wanted[56:] for index, wanted in enumerate(expected))
            if rejected != (0 if label == 'preferred' else nativeRejects[label]):
                raise ValueError(('895 independent corpus rejection count differs', label, rejected))
            runs.append(dict(actualPublicReturns=len(expected), rejected=rejected, publicOutputRejected=outputRejected, callContractOnlyRejected=rejected-outputRejected, legitimatePositiveCases=len(expected) - rejected, stdoutSha256=hashlib.sha256(run.stdout).hexdigest(), actualExitCode=run.returncode))
        if label == 'preferred' and runs[0]['stdoutSha256'] != runs[1]['stdoutSha256']:
            raise ValueError('895 fresh process outputs differ')
        results.append(dict(label=label, build=built, executions=runs))
    write_json(ROOT / 'evidence/ports/ov000-geometry895-windows32-20261102.json', dict(schemaVersion=1, passed=True, sourceCredit=0, originalArmByteCredit=0, generator=Path(__file__).name, generatorSha256=sha256(__file__), nativeContractSha256=sha256(ROOT / 'evidence/ports/geometry895-native-contract-20261102.json'), nativeOriginReport=native['originReport'], cases=len(expected), payloadSha256=hashlib.sha256(payload).hexdigest(), expectedSha256=hashlib.sha256(b''.join(expected)).hexdigest(), preferredPublicReturns=len(expected) * 2, wrongPublicReturns=len(expected) * 3, results=results, unmodifiedKernelSourceBytes=True, privateConsoleNoWindow=True, portableBackends=dict(signedFixedPointDivision=True, notificationWithoutMemoryEffects=True, preparationRejected=True, syntheticGlobalState=True), complete4096ByteObjectPageCompared=True, fullGame=False, renderedUi=False, androidDeviceExecutions=0, limits=['Actual PE32 console execution only; originalARM source match still fails and no ARM/source credit is added.', 'Frozen876 kernel and877 wrong-C text bytes are copied unchanged. Only explicit portable headers/backends replace fixed DS globals/division/notifications.', 'Two fresh preferred processes and three complete wrong-kernel processes return all1024 synthetic horizontal/tilted-plane cases. Native877 rejection counts and independent page/return/callback models agree.', 'This does not execute DS hardware, original runtime dependencies, ordinary scenes, GUI or any device. No claim outside the bounded877 source/input domain.']))
    print(dict(preferredPublicReturns=len(expected) * 2, wrongPublicReturns=len(expected) * 3, wrongRejected=sum(row['executions'][0]['rejected'] for row in results[1:]), sourceCredit=0), flush=True)


if __name__ == '__main__':
    main()
