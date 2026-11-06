import json
import os
import struct
import subprocess
from pathlib import Path
import utility_code
import unicorn as un
from unicorn import arm_const as ar
from elftools.elf.elffile import ELFFile
from project import ROOT, read_json, write_json, sha256

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/child-arm7-wl/revision'
WORK = ROOT / 'work/wl1104rev/conditions'
ADDRESS, BASE, MANAGER = 0x037f9f14, 0x037f8000, 0x02400000
RETURNS = [0, 1, 2, 0x10000, 0x80000000, 0xffffffff]


def execute(wram, body, kind, result, parameter):
    cpu = un.Uc(un.UC_ARCH_ARM, un.UC_MODE_ARM)
    cpu.mem_map(0x037f0000, 0x30000)
    cpu.mem_map(0x027e0000, 0x20000)
    cpu.mem_map(0x04800000, 0x10000)
    cpu.mem_map(MANAGER, 0x10000)
    cpu.mem_write(BASE, wram)
    cpu.mem_write(ADDRESS, body)
    cpu.mem_write(0x0380fff4, struct.pack('<I', MANAGER))
    cpu.reg_write(ar.UC_ARM_REG_CPSR, 0xa0000010)
    cpu.reg_write(ar.UC_ARM_REG_R0, result)
    cpu.reg_write(ar.UC_ARM_REG_SP, 0x037f1000)
    if kind == 'counter':
        start, stop = 0x037fa260, 0x037fa2d8
        cpu.mem_write(MANAGER + 0x5a8, struct.pack('<I', parameter))
    else:
        start, stop = 0x037fa300, 0x037fa320
        cpu.reg_write(ar.UC_ARM_REG_R4, 0x1234)
        cpu.mem_write(0x04808054, struct.pack('<H', 0x1234 if parameter else 0x1235))
    pcs, stores, fatal = [], [], []

    def code(machine, address, size, user):
        if address == stop:
            machine.emu_stop()
            return
        if address == 0x027e9164:
            fatal.append(machine.reg_read(ar.UC_ARM_REG_R0))
            machine.reg_write(ar.UC_ARM_REG_PC, machine.reg_read(ar.UC_ARM_REG_LR))
            return
        pcs.append(address)

    def store(machine, access, address, size, value, user):
        stores.append(dict(address=hex(address), size=size, value=value))

    cpu.hook_add(un.UC_HOOK_CODE, code)
    cpu.hook_add(un.UC_HOOK_MEM_WRITE, store)
    cpu.emu_start(start, 0, count=32)
    if cpu.reg_read(ar.UC_ARM_REG_PC) != stop:
        raise ValueError('Original instruction fragment did not reach its measured join')
    if kind == 'counter':
        actual = int.from_bytes(cpu.mem_read(MANAGER + 0x5a8, 4), 'little')
        expected = (parameter + int(result == 0)) & 0xffffffff
        if actual != expected or bool(stores) != (result == 0) or fatal:
            raise ValueError('Measured zero-result counter condition differs')
    else:
        expected = [0x20] if result != 0 and parameter else []
        actual = fatal
        if fatal != expected or stores:
            raise ValueError('Measured full32-bit result/stability/fatal-flag condition differs')
    return dict(kind=kind, suppliedHelperR0=hex(result), parameter=parameter, actual=actual,
                expected=expected, originalInstructionPcs=[hex(p) for p in pcs], stores=stores,
                modeledProviderEvents=fatal, nativeProviderInstructionsExecuted=0,
                fullCallerExecutions=0, fullCallerReturns=0)


def layout(entry):
    source = WORK / 'layout'
    source.mkdir(parents=True, exist_ok=True)
    headers = []
    for pin in entry['sourceDependencies']:
        path = ROOT / pin['path']
        destination = source / path.name
        destination.write_bytes(path.read_bytes())
        headers.append(destination)
    includes = ''.join('#include "' + p.name + '"\n' for p in headers)
    checks = ["typedef char a[(sizeof(u32)==4)?1:-1];",
              "typedef char b[(sizeof(u16)==2)?1:-1];",
              "typedef char c[((u32)&((LPWL_MAN)0)->Counter.multiPoll.txNull==0x5a8)?1:-1];",
              "typedef char d[(sizeof(((LPWL_MAN)0)->Counter.multiPoll.txNull)==4)?1:-1];"]
    payload = includes + '\n'.join(checks) + '\n'
    compiler = ROOT / entry['compiler']
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    results = []
    for label, text in [('correct', payload), ('wrong-offset', payload.replace('==0x5a8', '==0x5ac'))]:
        path, obj = source / (label + '.c'), source / (label + '.o')
        path.write_text(text)
        command = [str(compiler), *entry['compilerFlags'], '-c', str(path), '-o', str(obj)]
        process = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)
        results.append(dict(label=label, exitCode=process.returncode, source=path.relative_to(ROOT).as_posix(),
                            sourceSha256=sha256(path), stdout=process.stdout, stderr=process.stderr))
    if results[0]['exitCode'] != 0 or results[1]['exitCode'] == 0:
        raise ValueError(('Correct/wrong context layout compiler control failed', results))
    return results


def main():
    report = read_json(LANE / 'packet-ready.json')
    entry = report['matches'][0]
    wram = (ROOT / 'extract/utility/runtime/utility-child-arm7-wram.bin').read_bytes()
    native = wram[ADDRESS - BASE:ADDRESS - BASE + entry['bytes']]
    linked_path = (ROOT / entry['realLink']['linkedElf']).with_name('caller.bin')
    linked = linked_path.read_bytes()
    if native != linked or sha256(linked_path) != entry['targetSha256']:
        raise ValueError('Actual linked function differs from the complete original native function')
    records = []
    for kind, parameters in [('counter', [0x12345678, 0xffffffff]), ('fatal', [False, True])]:
        for result in RETURNS:
            for parameter in parameters:
                original = execute(wram, native, kind, result, parameter)
                compiled = execute(wram, linked, kind, result, parameter)
                if original != compiled:
                    raise ValueError('Original and actual linked instruction fragments differ')
                records.append(dict(original=original, recompiled=compiled))
    layouts = layout(entry)
    write_json(LANE / 'native-condition-controls.json', dict(status='passed', fragments=len(records) * 2,
        records=records, sourceLayoutControls=layouts, completeNativeBytes=entry['bytes'],
        program=entry['program'], processor=entry['processor'], module=entry['module'], address=entry['address'],
        sourceSha256=entry['sourceSha256'], targetSha256=entry['targetSha256'], unicornVersion=un.__version__,
        limitation='Only original/linked instruction fragments run with supplied helper-return values and modeled manager/MMIO/provider state; no complete wireless caller, native helper or device execution is claimed',
        fullNativeCallerExecutions=0, fullNativeCallerReturns=0, actualNativeHelperExecutions=0,
        independentConditions=['Counter increments exactly for helperR0==0, including unsigned counter wrap',
                               'Stable current-register snapshot plus any nonzero32-bit helper result emits exactly0x20',
                               'High16-bit-only helper results are preserved instead of truncating to zero']))
    print(dict(nativeAndLinkedFragments=len(records) * 2, sourceLayoutPositive=True,
               wrongLayoutRejected=True, fullNativeCallerExecutions=0))


if __name__ == '__main__':
    main()
