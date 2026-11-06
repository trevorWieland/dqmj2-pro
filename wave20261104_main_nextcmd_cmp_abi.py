import gzip
import json
import math
import os
import re
import struct
import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, write_json, sha256, configuration
import match_runtime as C
from link_runtime_unit import measured_module, verify_binding
from wave20261104_main_tail_compiler import COMPILER
from wave20261104_main_tail_bindings import native_relocations
from elftools.elf.elffile import ELFFile
import unicorn
from unicorn import arm_const as R

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-next/sixth'
WORK = ROOT / 'work/w4nc/sixth/abi'
PROBE = ROOT / 'generated/parallel_wave20261104/main-nextcmd-comparison-abi/probe.c'
HELPERS = {'_fleq': (0x020253D8, 104), '_fls': (0x02025440, 92), '_feq': (0x0202549C, 104)}
CALLERS = [0x020528FC, 0x02052A2C, 0x02052B5C, 0x02052C8C]
WORDS = [0, 0x80000000, 1, 0x80000001, 0x007FFFFF, 0x807FFFFF, 0x00800000, 0x80800000,
    0x3DCCCCCD, 0x3E4CCCCC, 0x3E4CCCCD, 0x3E4CCCCE, 0x3F000000, 0xBF000000,
    0x3F800000, 0xBF800000, 0x40000000, 0x40400000,
    0x3F8CCCCD, 0x7F7FFFFF, 0xFF7FFFFF, 0x7F800000, 0xFF800000,
    0x7FC00000, 0x7F800001, 0xFFC12345, 0xFF800123]
STOP, STACK = 0x027E0000, 0x027F0000


def binding(name):
    if name not in HELPERS:
        raise ValueError('Unknown separately measured comparison helper')
    result = dict(program='', processor='arm9', module='main', mode='arm', kind='function', address=hex(HELPERS[name][0]))
    verify_binding(name, result)
    return result


def qualify_binding(name, candidate):
    if candidate != binding(name):
        raise ValueError('Comparison helper changed its original name/program/CPU/module/mode/entry identity')
    verify_binding(name, candidate)


def expected(name, left, right):
    a, b = [struct.unpack('<f', struct.pack('<I', word))[0] for word in (left, right)]
    return a <= b if name == '_fleq' else a < b if name == '_fls' else a == b


def subtraction_flags(left, right, cpsr):
    result = (left - right) & 0xFFFFFFFF
    flags = (result & 0x80000000) | (int(result == 0) << 30) | (int(left >= right) << 29)
    flags |= int(bool((left ^ right) & (left ^ result) & 0x80000000)) << 28
    return (cpsr & 0x0FFFFFFF) | flags


def fixed_body_reference(name, left, right, initial, cpsr):
    registers = initial[:]
    magnitude = [(word << 1) & 0xFFFFFFFF for word in (left, right)]
    state = subtraction_flags(0xFF000000, magnitude[0], cpsr)
    if state & 0x20000000:
        state = subtraction_flags(0xFF000000, magnitude[1], state)
    unordered = any(word > 0xFF000000 for word in magnitude)
    truth = expected(name, left, right)
    registers[3] = 0xFF000000
    if not unordered and name != '_feq':
        ranked = [(-int(word & 0x7FFFFFFF) if word & 0x80000000 else word) & 0xFFFFFFFF for word in (left, right)]
        registers[1] = ranked[1]
        state = subtraction_flags(*ranked, state)
    elif not unordered:
        combined = left | right
        registers[3] = (combined << 1) & 0xFFFFFFFF
        if registers[3] == 0:
            state = (state & 0x1FFFFFFF) | 0x40000000 | (int(bool(combined & 0x80000000)) << 29)
        else:
            state = subtraction_flags(left, right, state)
    if name == '_fleq':
        state = (state & ~0x60000000) | (0x40000000 if truth else 0x20000000)
    elif name == '_fls':
        state = (state & ~0x20000000) | (0 if truth else 0x20000000)
    else:
        state = (state & ~0x40000000) | (0x40000000 if truth else 0)
    registers[0], registers[12] = int(truth), state
    return registers, state


class Runner:
    def __init__(self, name, main):
        self.name = name
        self.start, self.size = HELPERS[name]
        self.vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
        self.vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
        self.vm.mem_map(0x02000000, 0x800000)
        self.vm.mem_write(0x02000000, main)
        self.initial_ram = C.sha(bytes(self.vm.mem_read(0x02000000, 0x800000)))
        self.vm.hook_add(unicorn.UC_HOOK_CODE, self.code)
        self.vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, self.memory)

    def code(self, uc, address, size, user):
        if address == STOP:
            self.returned = True
            uc.emu_stop()
            return
        if not self.start <= address < self.start + self.size:
            raise ValueError('Helper escaped its configured complete native body')
        self.steps.append(dict(address=hex(address), bytes=size, thumb=bool(uc.reg_read(R.UC_ARM_REG_CPSR) & 32)))

    def memory(self, uc, access, address, size, value, user):
        self.writes.append(dict(address=hex(address), bytes=size, value=value))

    def run(self, expected_name, left, right, flags, ordinal, entry=None, thumb=False):
        initial = [0x11220000 + ordinal * 32 + index for index in range(15)]
        initial[:2], initial[-2:] = [left, right], [STACK, STOP]
        cpsr = flags | 0x10 | (32 if thumb else 0)
        self.vm.reg_write(R.UC_ARM_REG_CPSR, cpsr)
        for register, value in zip(C.REGISTERS, initial):
            self.vm.reg_write(register, value)
        self.returned, self.steps, self.writes = False, [], []
        error = None
        try:
            self.vm.emu_start((entry if entry is not None else self.start) | int(thumb), STOP + 4, timeout=200000, count=256)
        except Exception as exception:
            error = str(exception)
        registers = [self.vm.reg_read(register) for register in C.REGISTERS]
        final = self.vm.reg_read(R.UC_ARM_REG_CPSR)
        truth = expected(expected_name, left, right)
        reference_registers, reference_cpsr = fixed_body_reference(expected_name, left, right, initial, cpsr)
        condition = not bool(final & 0x20000000) or bool(final & 0x40000000) if expected_name == '_fleq' else (
            not bool(final & 0x20000000) if expected_name == '_fls' else bool(final & 0x40000000))
        checks = dict(actualReturn=self.returned, nativeBooleanReturn=registers[0] == int(truth),
            callerCondition=condition == truth, calleeSaved=registers[4:12] == initial[4:12],
            stackAndLink=registers[13:] == initial[13:], controlAndQPreserved=(final & 0x0FFFFFFF) == (cpsr & 0x0FFFFFFF),
            orderedWritesEmpty=not self.writes, armInstructions=bool(self.steps) and all(not step['thumb'] for step in self.steps),
            completeFixedBodyGprReference=registers == reference_registers,
            completeFixedBodyCpsrReference=final == reference_cpsr,
            configuredEntry=(entry is None or entry == self.start) and not thumb, noExecutionError=error is None)
        return dict(expectedHelper=expected_name, executedHelper=self.name, left=hex(left), right=hex(right),
            initialCpsr=hex(cpsr), finalCpsr=hex(final), initialRegisters=initial, registers=registers,
            referenceRegisters=reference_registers, referenceCpsr=hex(reference_cpsr),
            orderedMemoryWrites=self.writes, steps=self.steps, actualTopReturn=self.returned,
            expectedBoolean=int(truth), checks=checks, passed=all(checks.values()), error=error)

    def verify_immutable_ram(self):
        if C.sha(bytes(self.vm.mem_read(0x02000000, 0x800000))) != self.initial_ram:
            raise ValueError('Comparison helper changed native/scaffold RAM')


def profile_probe():
    WORK.mkdir(parents=True, exist_ok=True)
    output = WORK / 'profile-probe.o'
    if sha256(COMPILER) != C.COMPILER_PINS[COMPILER.relative_to(ROOT).as_posix()]:
        raise ValueError('Comparison compiler differs from pinned SP1 profile')
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    command = [str(COMPILER), *C.FLAGS, '-lang', 'c99', '-opt', 'speed', '-c', str(PROBE), '-o', str(output)]
    process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
    if process.returncode:
        raise ValueError(('Pinned compiler comparison probe failed', process.stdout, process.stderr))
    wanted = {'probe_less_equal': '_fleq', 'probe_less': '_fls', 'probe_equal': '_feq'}
    with output.open('rb') as stream:
        elf = ELFFile(stream)
        table = elf.get_section_by_name('.symtab')
        witnesses = []
        for symbol in table.iter_symbols():
            if symbol.name not in wanted:
                continue
            imports = []
            for section in elf.iter_sections():
                if section['sh_type'] not in ('SHT_REL', 'SHT_RELA') or section['sh_info'] != symbol['st_shndx']:
                    continue
                symbols = elf.get_section(section['sh_link'])
                for relocation in section.iter_relocations():
                    if symbol['st_value'] <= relocation['r_offset'] < symbol['st_value'] + symbol['st_size']:
                        imports.append(dict(symbol=symbols.get_symbol(relocation['r_info_sym']).name, type=relocation['r_info_type']))
            if imports != [dict(symbol=wanted[symbol.name], type=1)]:
                raise ValueError(('Operator probe changed compiler helper ABI name/relocation', symbol.name, imports))
            witnesses.append(dict(probe=symbol.name, helper=wanted[symbol.name], bytes=symbol['st_size'], imports=imports))
    if len(witnesses) != 3:
        raise ValueError('Comparison operator probe set differs')
    return dict(source=PROBE.relative_to(ROOT).as_posix(), sourceSha256=sha256(PROBE), object=output.relative_to(ROOT).as_posix(),
        objectSha256=sha256(output), compilerSha256=sha256(COMPILER), flags=C.FLAGS + ['-lang', 'c99', '-opt', 'speed'],
        command=command, explicitFrontend='c99', witnesses=witnesses,
        probeOrHelperSourceCredit=0)


def original_witnesses(main):
    text = (ROOT / 'config/arm9/symbols.txt').read_text()
    records = native_relocations()
    rows = []
    for name, (address, size) in HELPERS.items():
        binding(name)
        if not re.search(r'^\S+ kind:function\(arm,size=0x' + format(size, 'x') + r'\) addr:0x' + format(address, '08x') + '$', text, re.M):
            raise ValueError('Comparison helper complete configured body differs')
        rows.append(dict(helper=name, binding=binding(name), bytes=size,
            targetSha256=C.sha(main[address - 0x02000000:address - 0x02000000 + size]), sourceCredit=0))
    callers = []
    for address in CALLERS:
        if not re.search(r'^\S+ kind:function\(arm,size=0x130\) addr:0x' + format(address, '08x') + '$', text, re.M):
            raise ValueError('Comparison caller complete configured body differs')
        sites = []
        for offset, name in [(0x94, '_fleq'), (0xAC, '_fls'), (0xC4, '_feq')]:
            origin = address + offset
            record = records.get(origin)
            word = struct.unpack_from('<I', main, origin - 0x02000000)[0]
            displacement = (word & 0xFFFFFF) << 2
            if displacement & 0x2000000:
                displacement -= 0x4000000
            target = origin + 8 + displacement
            if word >> 24 != 0xEB or target != HELPERS[name][0] or record is None or record['module'] != 'main' or int(record['address'], 0) != target:
                raise ValueError('Comparison caller branch instruction/namespace differs')
            sites.append(dict(helper=name, origin=hex(origin), encodedWord=hex(word), target=hex(target), mode='arm',
                originalRecord=record['record']))
        constants = []
        for offset, value in [(0x124, 0xBF800000), (0x128, 0x40400000), (0x12C, 0x3E4CCCCD)]:
            word = struct.unpack_from('<I', main, address - 0x02000000 + offset)[0]
            if word != value:
                raise ValueError('Comparison caller literal word differs')
            constants.append(dict(offset=hex(offset), word=hex(word)))
        callers.append(dict(program='', processor='arm9', module='main', mode='arm', address=hex(address), bytes=304,
            targetSha256=C.sha(main[address - 0x02000000:address - 0x02000000 + 304]), sites=sites, sourceCredit=0))
        callers[-1]['originalLiteralWords'] = constants
    return dict(helpers=rows, originalCallers=callers)


def execute():
    if unicorn.__version__ != '2.1.4' or sys.version_info[:3] != (3, 13, 5):
        raise ValueError('Pinned native comparison runtime differs')
    inputs = read_json(LANE / 'helper-abi-inputs.json')
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen comparison input differs: ' + pin['path'])
    info, main, unused = measured_module('main')
    profile = profile_probe()
    witnesses = original_witnesses(main)
    traces, controls = [], []
    cases = [(a, b, flags << 28 | q << 27) for a in WORDS for b in WORDS for flags, q in [(0, 0), (15, 1)]]
    special = [(0, 0), (0x80000000, 0), (0x3DCCCCCD, 0x3DCCCCCD), (0x3F000000, 0x3F800000),
        (0x3F800000, 0x3F000000), (0x7FC00000, 0x3F800000), (0x7F800000, 0x7F800000), (0xFF800000, 0x7F800000),
        (0x3E4CCCCD, 0x3E4CCCCD), (0x3E4CCCCC, 0x3E4CCCCD), (0x3E4CCCCE, 0x3E4CCCCD)]
    cases += [(a, b, flags << 28 | q << 27) for a, b in special for flags in range(16) for q in range(2)]
    for name in HELPERS:
        runner = Runner(name, main)
        for ordinal, (a, b, flags) in enumerate(cases):
            result = runner.run(name, a, b, flags, ordinal)
            if not result['passed']:
                write_json(LANE / 'helper-abi-failure.json', result)
                raise ValueError(('Original comparison helper ABI failed', name, ordinal))
            traces.append(result)
        runner.verify_immutable_ram()
        for case, target, entry, thumb, pair in [
            ('swapped-helper', '_fls' if name != '_fls' else '_fleq', None, False,
                (0, 0) if name != '_feq' else (0, 0x3F800000)),
            ('interior-entry', name, HELPERS[name][0] + 4, False, (0x3F800000, 0x3F800000) if name == '_feq' else (0, 0x3F800000)),
            ('wrong-mode', name, None, True, (0x3F800000, 0x3F800000))]:
            bad = Runner(target, main).run(name, *pair, 0, 4096, entry=entry, thumb=thumb)
            if bad['passed'] or case in ('swapped-helper', 'interior-entry') and bad['checks']['nativeBooleanReturn']:
                raise ValueError(('Wrong comparison helper control was not discriminating', name, case))
            candidate = binding(name)
            candidate['address'] = hex(HELPERS[target][0]) if case == 'swapped-helper' else hex(entry or HELPERS[name][0])
            if case == 'wrong-mode':
                candidate['mode'] = 'thumb'
            try:
                qualify_binding(name, candidate)
            except ValueError as exception:
                controls.append(dict(helper=name, case=case, rejected=True, bindingReason=str(exception), actualExecution=bad))
            else:
                raise ValueError('Wrong comparison helper binding accepted')
        print('qualified', name, len(cases), flush=True)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'helper-abi-traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    write_json(LANE / 'helper-abi.json', dict(status='passed', romSha256=configuration()['romSha256'],
        mainSha256=info['sha256'], profile=profile, originalQualifiedBodiesAndCallsites=witnesses,
        cases=len(traces), casesPerHelper=len(cases), actualOriginalHelperReturns=len(traces), negativeControls=controls,
        trace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)),
        inputs=dict(path=(LANE / 'helper-abi-inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'helper-abi-inputs.json')),
        completeGprAndCpsrCaptured=True, calleeSavedStackLinkControlAndQPreserved=True, orderedMemoryWritesEmpty=True,
        completeFixedBodyGprAndCpsrReferenceEquality=True, unspecifiedScratchValuesAreNotGeneralSdkContract=True,
        helperProbeOrScaffoldingSourceCredit=0, callerSourceCredit=0,
        limits=['Actual original ARM helper bodies only; complete configured extents, original caller branches and native modes pinned independently.',
            'Ordered IEEE comparison results/branch flags tested on all supplied raw pairs including both zero signs, infinities, subnormals, quiet/signaling and high-sign NaN payloads; full16NZCV/twoQ states on eleven additional pairs including the measured0.2threshold and its adjacent float words.',
            'Original helper R0 returns, all GPRs, CPSR and ordered memory writes recorded; actual bounded returns, no RAM writes and no escaped native helper PC allowed.',
            'Nine swapped-helper/interior-entry/wrong-mode controls include actual native diagnostic execution and strict qualified-binding rejection.',
            'No source reconstruction or credit for probes/helpers/scaffolding; no full caller, game, floating exception environment or hardware/platform claim.']))
    print(dict(helperCases=len(traces), negativeControls=len(controls), sourceCredit=0), flush=True)


if __name__ == '__main__':
    execute()
