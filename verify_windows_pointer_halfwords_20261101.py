import hashlib
import os
import random
import struct
import subprocess
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
import link_arm7_bulk_20261030 as arm7
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA, LINKER_SHA, DLLTOOL_SHA

WORK = ROOT / 'work/windows-pointer-halfwords-20261101'
DATA = 0x02380000
STACK = 0x03030000
STOP = 0x0F000000
ENTRIES = [0x03801C50, 0x03801C70]


def oracle(metadata, image, selector, arguments, page):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    base = int(metadata['base'], 0)
    machine.mem_map(base, 0x20000)
    machine.mem_write(base, image)
    machine.mem_map(DATA, 4096)
    machine.mem_write(DATA, page)
    machine.mem_map(STACK, 8192)
    guard = bytes([0xC7]) * 8192
    machine.mem_write(STACK, guard)
    machine.mem_map(STOP, 4096)
    machine.mem_write(0x03807EDC, struct.pack('<I', arguments[3]))
    machine.reg_write(UC_ARM_REG_CPSR, 0x1F)
    registers = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2]
    for register, value in zip(registers, arguments[:3]):
        machine.reg_write(register, value & 0xFFFFFFFF)
    preserved = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    for index, register in enumerate(preserved):
        machine.reg_write(register, 0x10203040 + index * 0x10001)
    machine.reg_write(UC_ARM_REG_SP, STACK + 4096)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    stores = []

    def write(unused, access, address, size, value, context):
        stores.append([address, size, value & ((1 << (size * 8)) - 1)])

    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRIES[selector], STOP, count=128)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == STACK + 4096
    assert bytes(machine.mem_read(STACK, 8192)) == guard
    for index, register in enumerate(preserved):
        assert machine.reg_read(register) == 0x10203040 + index * 0x10001
    a, b, c, pointer = arguments
    if selector == 0:
        result, value = (pointer + a * 36 + b * 2) & 0xFFFFFFFF, c
        destination = result + 0x20
    else:
        result, value = (pointer + a * 2 + 0x200) & 0xFFFFFFFF, b
        destination = result + 0x60
    expected = bytearray(page)
    struct.pack_into('<H', expected, destination - DATA, value & 0xFFFF)
    assert stores == [[destination, 2, value & 0xFFFF]], stores
    actual = bytes(machine.mem_read(DATA, 4096))
    assert actual == expected and machine.reg_read(UC_ARM_REG_R0) == result
    return struct.pack('<I', result) + actual


def inputs():
    modules, unused = arm7.namespace('')
    metadata = modules['arm7-wram']
    image = (ROOT / metadata['binary']).read_bytes()
    assert hashlib.sha256(image).hexdigest() == metadata['sha256']
    rng = random.Random(0x1C501C70)
    payload = bytearray(struct.pack('<I', 1024))
    expected = bytearray()
    offsets = [-16, -8, -1, 0, 1, 8, 15, 16]
    values = [-32768, -1, 0, 1, 127, 255, 32767, 0x12345678]
    for selector in range(2):
        for index in range(512):
            a = offsets[index % 8]
            b = offsets[(index // 8) % 8] if selector == 0 else values[(index // 8) % 8]
            c = values[(index // 64) % 8]
            pointer = DATA + (0x400 if index % 2 else 0x800)
            page = rng.randbytes(4096)
            arguments = [a, b, c, pointer]
            expected.extend(oracle(metadata, image, selector, arguments, page))
            payload.extend(struct.pack('<5I', selector, *(value & 0xFFFFFFFF for value in arguments)))
            payload.extend(page)
    return bytes(payload), bytes(expected), metadata


def main():
    proof_path = ROOT / 'evidence/portability/windows-pointer-cast-arm-proof-v2-20261101.json'
    proof = read_json(proof_path)
    rows = [row for row in proof['candidates'] if any(f'{address:08x}.c' in row['source'] for address in ENTRIES)]
    assert len(rows) == 2
    for row in rows:
        assert row['state'] == 'genuine-arm-linked-unadopted'
        assert sha256(ROOT / row['source']) == row['sourceSha256']
        assert sha256(ROOT / row['candidate']) == row['candidateSha256']
    directory = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    clang, linker, dlltool = [directory / name for name in ['clang.exe', 'ld.lld.exe', 'llvm-dlltool.exe']]
    assert [sha256(path) for path in [clang, linker, dlltool]] == [CLANG_SHA, LINKER_SHA, DLLTOOL_SHA]
    WORK.mkdir(parents=True, exist_ok=True)
    environment = {key: value for key, value in os.environ.items()
        if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    steps = []

    def run(command, data=None):
        command = list(map(str, command))
        result = subprocess.run(command, cwd=ROOT, env=environment, input=data, capture_output=True,
            timeout=120, creationflags=subprocess.CREATE_NO_WINDOW)
        steps.append(dict(command=command, exitCode=result.returncode,
            stdoutSha256=hashlib.sha256(result.stdout).hexdigest(), stderr=result.stderr.decode(errors='replace')))
        assert result.returncode == 0, steps[-1]
        return result.stdout

    definition = WORK / 'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nReadFile@20\nWriteFile@20\nVirtualAlloc@16\n', encoding='ascii')
    library = WORK / 'kernel32.lib'
    run([dlltool, '-m', 'i386', '-k', '-d', definition, '-l', library])
    runner = ROOT / 'ports/windows-native/pointer_halfword_runner_20261101.c'
    sources = [ROOT / row['candidate'] for row in rows]

    def build(paths, label):
        objects = []
        for index, source in enumerate([runner] + paths):
            obj = WORK / f'{label}-{index}.obj'
            run([clang, '--target=i686-pc-windows-msvc', '-std=c11', '-O2', '-fpack-struct=4',
                '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-strict-aliasing', '-c', source, '-o', obj])
            objects.append(obj)
        executable = WORK / (label + '.exe')
        run([linker, '-flavor', 'link', '/machine:x86', '/subsystem:console', '/nodefaultlib', '/entry:j2p_entry',
            '/safeseh:no', '/fixed', '/dynamicbase:no', '/timestamp:0', '/manifest:embed',
            "/manifestuac:level='asInvoker' uiAccess='false'", '/out:' + str(executable), *objects, library])
        binary = executable.read_bytes()
        pe = struct.unpack_from('<I', binary, 0x3C)[0]
        assert binary[pe:pe + 4] == b'PE\0\0' and struct.unpack_from('<H', binary, pe + 4)[0] == 0x14C
        assert struct.unpack_from('<H', binary, pe + 24)[0] == 0x10B and b'asInvoker' in binary
        return executable

    executable = build(sources, 'halfwords')
    payload, expected, metadata = inputs()
    outputs = [run([executable], payload) for unused in range(2)]
    assert outputs[0] == outputs[1] == expected
    negative = WORK / 'negative-halfword-offset.c'
    original = sources[0].read_text()
    assert original.count('s16 *, 0x20') == 1
    negative.write_text(original.replace('s16 *, 0x20', 's16 *, 0x22'), encoding='utf-8')
    bad = run([build([negative, sources[1]], 'negative-halfwords')], payload)
    assert len(bad) == len(expected)
    width = 4100
    rejected = sum(bad[index * width:(index + 1) * width] != expected[index * width:(index + 1) * width] for index in range(1024))
    assert rejected == 512
    report = dict(passed=True, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        actualWindowsNativeExecution=True, originalArmCodeInNativeProcess=False, newSourceCoverageCredit=0,
        fullGame=False, selectedSourceModified=False, uniqueSyntheticContexts=1024, freshProcessRuns=2,
        originalArmActualReturns=1024, sourceNativeCallsPerProcess=1024, providerCalls=0,
        returnAndFullPageMismatches=0, orderedOriginalHalfwordStores=1024,
        originalCalleeSaveStackAndGuardsPreserved=True, deterministicOutput=True,
        wrongControlActualReturns=1024, independentWrongRejections=rejected, unchangedWrongControlPositives=512,
        module=metadata, pointerCastArmProof=dict(path=proof_path.relative_to(ROOT).as_posix(), sha256=sha256(proof_path)),
        sourceInputs=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in [runner, ROOT / __file__, *sources]],
        tools=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in [clang, linker, dlltool]],
        inputSha256=hashlib.sha256(payload).hexdigest(), outputSha256=hashlib.sha256(expected).hexdigest(), steps=steps,
        limitations=['Two existing halfword-store functions only; no new decompilation byte credit',
            'Finite bounded signed arithmetic and aligned in-page destinations; invalid pointers and overflow excluded',
            'Windows return values and full data pages compared; original ARM additionally checked for ordered writes and callee saves',
            'No scheduler, hardware, full game or complete native port is exercised'])
    write_json(ROOT / 'evidence/portability/pointer-halfwords-windows32-20261101.json', report)
    print(dict(passed=True, originalReturns=1024, nativeRuns=2, differences=0, wrongRejections=rejected, sourceCredit=0))


if __name__ == '__main__':
    main()
