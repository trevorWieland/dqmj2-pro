import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261104_main_arm_next_tenth_bindings import verify_original, negative_controls
from wave20261104_main_arm_next_tenth_compiler import COMPILER


def execute(rows):
    checks = negative_controls()['negativeCases']
    for row in rows:
        names = [symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function']
        if not names:
            continue
        symbol = names[0]
        for label, key, value in [('wrong-mode', 'mode', 'thumb'), ('function-as-data', 'kind', 'data'),
                                  ('same-address-wrong-overlay', 'module', 'ov000'), ('wrong-address', 'address', '0x203b8e0'),
                                  ('wrong-CPU', 'processor', 'arm7'), ('wrong-program', 'program', 'child')]:
            bindings = copy.deepcopy(row['nativeSymbolEntries'])
            bindings[symbol][key] = value
            try:
                verify_original(row, bindings)
            except ValueError as error:
                checks.append(dict(caller=row['address'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Invalid measured resource callee identity accepted')
    for row in rows:
        verify_original(row, row['nativeSymbolEntries'])
    directory = ROOT / 'work/w4an/tenth-controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261104/main-arm-next/tenth/context.h'
    shutil.copyfile(header, directory / 'context.h')
    source = directory / 'layout.c'
    source.write_text('#include "context.h"\n')
    output = directory / 'layout.o'
    command = [str(COMPILER), *C.FLAGS, '-opt', 'speed', '-c', str(source), '-o', str(output)]
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
    if process.returncode:
        raise ValueError(('Native pointer-field layout assertions failed', process.stdout, process.stderr))
    positive = dict(compilerSha256=sha256(COMPILER), headerSha256=sha256(header), sourceSha256=sha256(source),
                    objectSha256=sha256(output), exitCode=0,
                    facts=['signedBitfieldWord4', 'timer232', 'flags272', 'counter352', 'measuredNeighborStride372'])
    failures = []
    for label, old, new in [('wrong-flags-width', 'u32 remaining:28;', 'u32 remaining:27; u32 extra:2;'),
                            ('wrong-timer-offset', 'opaquec6[0x22]', 'opaquec6[0x1e]'),
                            ('wrong-flags-offset', 'timerDatae8[0x28]', 'timerDatae8[0x24]'),
                            ('wrong-counter-offset', 'opaque11c[0x38]', 'opaque11c[0x34]')]:
        if header.read_text().count(old) != 1:
            raise ValueError('Pointer-field layout mutation ambiguous')
        (directory / 'context.h').write_text(header.read_text().replace(old, new))
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
        if not process.returncode or 'illegal constant expression' not in process.stdout:
            raise ValueError(('Wrong native signed field/offset accepted', process.stdout, process.stderr))
        failures.append(dict(case=label, rejected=True, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr))
    return dict(status='passed', sourceCredit=0, bindingControls=checks, nativeCompilerLayout=positive, wrongNativeLayouts=failures, signedBitfieldProbe=bitfield_controls(header, directory))


def bitfield_controls(header, directory):
    import struct
    import unicorn
    from unicorn import arm_const as R
    from elftools.elf.elffile import ELFFile
    source = directory / 'bitfields.c'
    functions = []
    for n in range(4):
        functions.append('u32 abi_flag%d(u32 raw) { union { u32 word; PlayerFlags flags; } v; v.word = raw; return v.flags.bit%d; }' % (n, n))
    source.write_text('#include "context.h"\n' + '\n'.join(functions))
    output = directory / 'bitfields.o'
    command = [str(COMPILER), *C.FLAGS, '-opt', 'speed', '-inline', 'on', '-c', str(source), '-o', str(output)]
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))

    def probe(text):
        (directory / 'context.h').write_text(text)
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
        if process.returncode:
            raise ValueError('Native signed-bitfield probe failed to compile')
        tests = []
        with output.open('rb') as stream:
            elf = ELFFile(stream)
            symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
            for n in range(4):
                symbol = next(s for s in symbols if s.name == 'abi_flag%d' % n)
                body = elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']]
                for raw in list(range(16)) + [0x80000000, 0xffffffff]:
                    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
                    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
                    vm.mem_map(0x02300000, 0x1000)
                    vm.mem_write(0x02300000, body)
                    vm.reg_write(R.UC_ARM_REG_R0, raw)
                    vm.reg_write(R.UC_ARM_REG_LR, 0x02300800)
                    vm.reg_write(R.UC_ARM_REG_SP, 0x02300f00)
                    vm.emu_start(0x02300000, 0x02300800, count=100)
                    actual = vm.reg_read(R.UC_ARM_REG_R0)
                    if actual != (0xffffffff if raw & (1 << n) else 0) or vm.reg_read(R.UC_ARM_REG_PC) != 0x02300800:
                        raise ValueError('Actual native signed1-bit projection/position differs')
                    tests.append(dict(bit=n, input=raw, output=actual))
        return dict(sourceSha256=sha256(source), objectSha256=sha256(output), nativeAbiProbeReturns=len(tests), cases=tests, originalGameOrCalleeExecution=0)

    text = header.read_text()
    positive = probe(text)
    negative = []
    variants = [('unsigned-field', text.replace('s32 bit3:1;', 'u32 bit3:1;')),
                ('wrong-field-order', text.replace('s32 bit0:1;', 's32 temporary:1;').replace('s32 bit3:1;', 's32 bit0:1;').replace('s32 temporary:1;', 's32 bit3:1;'))]
    for label, wrong in variants:
        try:
            probe(wrong)
        except ValueError as error:
            negative.append(dict(case=label, rejected=True, reason=str(error)))
        else:
            raise ValueError('Wrong native bitfield ABI accepted')
    return dict(status='passed', positive=positive, negative=negative, sourceCredit=0)
