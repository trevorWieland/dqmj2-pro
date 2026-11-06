import collections
import hashlib
import os
import re
from pathlib import Path
import struct
import subprocess
from project import ROOT, configuration, native_dependencies, sha256, write_json
native_dependencies(configuration())
import match_runtime as compiler
import link_runtime_unit as linker
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_926, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2
from unicorn.arm_const import UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6
from unicorn.arm_const import UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10
from unicorn.arm_const import UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR

ENTRY, SIZE, DATA, CALLBACK, STACK, STOP = 0x0201D470, 356, 0x02500000, 0x02600000, 0x02700000, 0x02800000
SOURCE = 'nonmatching/main-sort/20261030/heap_sort_m2c_pointer.c'
WORK = ROOT / 'work/coordinator-main-sort-20261030/native-proof'
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
FLAGS = [*compiler.FLAGS, '-opt', 'speed']


def build(source, name, tag):
    obj = WORK / (tag + '.o')
    result = subprocess.run([str(compiler.COMPILER), *FLAGS, '-c', str(source), '-o', str(obj)],
        capture_output=True, timeout=60,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:
        raise ValueError((result.stdout + result.stderr).decode(errors='replace'))
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = elf.get_section_by_name('.symtab').get_symbol_by_name(name)[0]
        data = elf.get_section(symbol['st_shndx']).data()
        body = data[symbol['st_value']:symbol['st_value'] + symbol['st_size']]
    return obj, body


def execute(body, callback, payload, count, width):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_926)
    for address, size in [(0x0201D000, 0x1000), (DATA, 0x4000), (CALLBACK, 0x1000), (STACK, 0x4000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(ENTRY, body)
    machine.mem_write(CALLBACK, callback)
    machine.mem_write(DATA, bytes([0xA5]) * 0x4000)
    array = DATA + 128
    machine.mem_write(array, payload or bytes([0]))
    machine.mem_write(STACK, bytes([0x5A]) * 0x4000)
    machine.reg_write(UC_ARM_REG_CPSR, 0xA000001F)
    initial = [(0x13579BDF * (i + 1)) & 0xFFFFFFFF for i in range(13)]
    for reg, value in zip(REGS, initial):
        machine.reg_write(reg, value)
    for reg, value in [(UC_ARM_REG_R0, array), (UC_ARM_REG_R1, count), (UC_ARM_REG_R2, width),
                       (UC_ARM_REG_R3, CALLBACK), (UC_ARM_REG_SP, STACK + 0x3000), (UC_ARM_REG_LR, STOP)]:
        machine.reg_write(reg, value)
    pending, comparisons, writes, events = [], [], [], []

    def code(uc, address, size, data):
        if pending and address == pending[-1]['returnPc']:
            row = pending.pop()
            assert uc.reg_read(UC_ARM_REG_SP) == row['sp']
            assert uc.reg_read(UC_ARM_REG_R0) == row['expected'] & 0xFFFFFFFF
            comparisons.append([row['left'], row['right'], row['expected']])
        if address == CALLBACK:
            left, right = uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)
            assert array <= left < array + max(len(payload), 1)
            assert array <= right < array + max(len(payload), 1)
            a = int.from_bytes(uc.mem_read(left, 1), 'little', signed=True)
            b = int.from_bytes(uc.mem_read(right, 1), 'little', signed=True)
            pending.append({'returnPc': uc.reg_read(UC_ARM_REG_LR), 'sp': uc.reg_read(UC_ARM_REG_SP),
                            'left': left - array, 'right': right - array, 'expected': (a > b) - (a < b)})
        elif address == STOP:
            events.append('actual-return')
            uc.emu_stop()
        elif not ENTRY <= address < ENTRY + SIZE and not CALLBACK <= address < CALLBACK + len(callback):
            raise AssertionError('UnexpectedSortExecution')
        if address == 0x0201D5CC:
            raise AssertionError('UnreachableConfiguredEpilogueExecuted')

    def store(uc, access, address, size, value, data):
        if DATA <= address < DATA + 0x4000:
            assert array <= address and address + size <= array + len(payload)
            writes.append([address - array, size, value & ((1 << (size * 8)) - 1)])
        else:
            assert STACK <= address and address + size <= STACK + 0x4000

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, store)
    machine.emu_start(ENTRY, STOP + 4, count=300000, timeout=500000)
    assert events == ['actual-return'] and not pending
    assert machine.reg_read(UC_ARM_REG_SP) == STACK + 0x3000
    assert [machine.reg_read(reg) for reg in REGS[4:]] == initial[4:]
    actual = bytes(machine.mem_read(array, len(payload)))
    assert bytes(machine.mem_read(DATA, 128)) == bytes([0xA5]) * 128
    assert bytes(machine.mem_read(array + max(len(payload), 1), 128)) == bytes([0xA5]) * 128
    if width:
        before = [payload[i * width:(i + 1) * width] for i in range(count)]
        after = [actual[i * width:(i + 1) * width] for i in range(count)]
        assert collections.Counter(before) == collections.Counter(after)
        keys = [int.from_bytes(x[:1], 'little', signed=True) for x in after]
        assert keys == sorted(keys)
    else:
        assert not writes
    return {'output': actual.hex(), 'comparisons': comparisons, 'arrayWrites': writes,
            'actualReturn': True, 'syntheticComparatorReturns': len(comparisons)}


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    assert sha256(compiler.COMPILER) == compiler.COMPILER_PINS[compiler.COMPILER.relative_to(ROOT).as_posix()]
    metadata, binary, config = linker.measured_module('main')
    native = binary[ENTRY - int(metadata['base'], 0):ENTRY - int(metadata['base'], 0) + SIZE]
    obj, compiled = build(ROOT / SOURCE, 'native_main_0201d470', 'source')
    assert len(compiled) == SIZE
    configured = int(re.search(r'^\S+ kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x0201d470$', config, re.M)[1], 0)
    assert configured in (348, 356)
    entry = {'processor': 'arm9', 'module': 'main', 'mode': 'arm', 'address': hex(ENTRY), 'bytes': configured,
             'targetSha256': hashlib.sha256(native[:configured]).hexdigest(), 'source': SOURCE,
             'sourceSha256': sha256(ROOT / SOURCE), 'object': obj.relative_to(ROOT).as_posix(),
             'objectSha256': sha256(obj), 'name': 'native_main_0201d470'}
    link_directory = (WORK / 'real-link').resolve()
    assert link_directory.is_relative_to(WORK.resolve())
    for name in ['caller.bin', 'linked.elf']:
        path = link_directory / name
        if path.exists():
            path.unlink()
    try:
        linker.validate(entry, {}, link_directory)
    except ValueError as error:
        link_failure = str(error)
    else:
        raise AssertionError('NonmatchingHypothesisUnexpectedlyAccepted')
    linked = (link_directory / 'caller.bin').read_bytes()
    assert linked == compiled
    callback_source = WORK / 'synthetic_comparator.c'
    callback_source.write_text('int synthetic_comparator(const signed char *a, const signed char *b) { return (*a > *b) - (*a < *b); }\n', encoding='utf-8')
    callback_obj, callback = build(callback_source, 'synthetic_comparator', 'comparator')
    vectors = []
    for count in [0, 1, 2, 3, 5, 8, 17]:
        for width in [0, 1, 2, 4, 7]:
            for pattern in range(5):
                payload = bytes(((i * [0, 1, 255, 17, 113][pattern] + pattern * 63) & 255) for i in range(count * width))
                vectors.append((count, width, payload))
    vectors += [(16, 1, bytes(range(start, start + 16))) for start in range(0, 256, 16)]
    records = []
    for count, width, payload in vectors:
        original = execute(native, callback, payload, count, width)
        rebuilt = execute(linked, callback, payload, count, width)
        assert original == rebuilt
        records.append({'count': count, 'width': width, 'inputSha256': hashlib.sha256(payload).hexdigest(),
                        'stateSha256': hashlib.sha256(repr(original).encode()).hexdigest(),
                        'syntheticComparatorReturns': original['syntheticComparatorReturns'] * 2})
    report = {'romSha256': configuration()['romSha256'], 'module': 'main', 'processor': 'arm9', 'mode': 'arm',
              'address': hex(ENTRY), 'provisionalWholeExtent': SIZE, 'configuredExtent': configured,
              'source': SOURCE, 'sourceSha256': sha256(ROOT / SOURCE), 'objectSha256': sha256(obj),
              'compiledBytes': len(compiled), 'sameOffsetBytes': sum(a == b for a, b in zip(native, compiled)),
              'exactNativeBytes': compiled == native, 'genuineLinkProducedUnmodifiedSourceBytes': linked == compiled,
              'normalAcceptanceLinkFailure': link_failure, 'boundaryConfigChanged': False,
              'freshGenuineLinkOutputRequired': True, 'linkerSha256': sha256(linker.LINKER),
              'sourceCredit': 0, 'cases': len(records), 'actualOriginalAndSourceReturns': len(records) * 2,
              'syntheticComparatorSourceSha256': sha256(callback_source), 'syntheticComparatorObjectSha256': sha256(callback_obj),
              'hostProviders': 0, 'syntheticComparatorGameSourceCredit': 0, 'records': records,
              'limitations': ['The final eight bytes are a compiler-owned epilogue fragment, not an independently credited function',
                  'Genuine source link remains a native-byte mismatch; this hypothesis receives no source credit',
                  'Caller-saved registers/flags/stack spills can differ in nonmatching void C',
                  'Synthetic signed-byte comparator is compiled test context, not an original game callback']}
    write_json(ROOT / 'evidence/functional/main-heap-sort-near-20261030.json', report)
    print({'cases': len(records), 'actualReturns': len(records) * 2, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
