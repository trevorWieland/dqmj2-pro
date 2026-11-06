import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261105_main_tail_next_second_bindings import verify_original, negative_controls
from wave20261105_main_tail_next_compiler import COMPILER


def execute(rows):
    checks = negative_controls(rows)['negativeCases']
    for row in rows:
        names = [symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function']
        if not names:
            continue
        for symbol in names:
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
    directory = ROOT / 'work/w5tn/second-controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261105/main-tail-next/second/context.h'
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
                    facts=['word32', 'pointer32', 'Vec2Size4', 'SummaryPrefix64', 'value20at32', 'packedWordsAt56And60', 'WidgetContentAt4', 'Unsigned10BitFields'])
    failures = []
    for label, old, new in [('wrong-summary-halfword-offset', 'opaque0[0x20]', 'opaque0[0x1e]'),
                            ('wrong-Vec2-width', 'Vec2 { s16 x;', 'Vec2 { s32 x;'),
                            ('wrong-packed-width', 'u32 opaque30:2;', 'u32 opaque30:3;'),
                            ('wrong-widget-content', 'Widget { u32 opaque0;', 'Widget { u32 opaque0[2];')]:
        if header.read_text().count(old) != 1:
            raise ValueError('Pointer-field layout mutation ambiguous')
        (directory / 'context.h').write_text(header.read_text().replace(old, new))
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
        if not process.returncode or 'illegal constant expression' not in process.stdout:
            raise ValueError(('Wrong native signed field/offset accepted', process.stdout, process.stderr))
        failures.append(dict(case=label, rejected=True, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr))
    return dict(status='passed', sourceCredit=0, bindingControls=checks, nativeCompilerLayout=positive, wrongNativeLayouts=failures, unsignedPackedAbi=packed_abi(header, directory))


def packed_abi(header, directory):
    import struct
    import unicorn
    from unicorn import arm_const as R
    from elftools.elf.elffile import ELFFile
    source = directory / 'packed.c'
    names = [('low0', 0), ('middle10', 10), ('high20', 20)]
    source.write_text('#include "context.h"\n' + '\n'.join(
        'u32 abi_' + name + '(u32 raw) { union { u32 word; PackedCounts bits; } v; v.word=raw; return v.bits.' + name + '; }'
        for name, shift in names))
    output = directory / 'packed.o'
    command = [str(COMPILER), *C.FLAGS, '-opt', 'speed', '-inline', 'on', '-c', str(source), '-o', str(output)]
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))

    def probe(text):
        (directory / 'context.h').write_text(text)
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
        if process.returncode:
            raise ValueError(('Actual native unsigned10-bit probe compile failed', process.stdout, process.stderr))
        cases = []
        with output.open('rb') as stream:
            elf = ELFFile(stream)
            symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
            for name, shift in names:
                symbol = next(s for s in symbols if s.name == 'abi_' + name)
                body = elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']]
                vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
                vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
                vm.mem_map(0x02300000, 0x1000)
                vm.mem_write(0x02300000, body)
                for value in range(1024):
                    raw = (0xa5a5a5a5 & ~(1023 << shift)) | value << shift
                    vm.reg_write(R.UC_ARM_REG_R0, raw)
                    vm.reg_write(R.UC_ARM_REG_LR, 0x02300800)
                    vm.reg_write(R.UC_ARM_REG_SP, 0x02300f00)
                    vm.emu_start(0x02300000, 0x02300800, count=100)
                    actual = vm.reg_read(R.UC_ARM_REG_R0)
                    if actual != value or vm.reg_read(R.UC_ARM_REG_PC) != 0x02300800:
                        raise ValueError(('Actual native unsigned10-bit signedness/position differs', name, raw, actual, value))
                    cases.append(dict(field=name, input=raw, result=actual))
        return dict(sourceSha256=sha256(source), objectSha256=sha256(output), nativeAbiProbeReturns=len(cases), cases=cases, originalGameOrCalleeExecution=0)

    text = header.read_text()
    positive = probe(text)
    variants = [('signed-low10', text.replace('u32 low0:10;', 's32 low0:10;')),
                ('swapped-low-middle', text.replace('u32 low0:10;', 'u32 temporary:10;').replace('u32 middle10:10;', 'u32 low0:10;').replace('u32 temporary:10;', 'u32 middle10:10;'))]
    failures = []
    for label, wrong in variants:
        try:
            probe(wrong)
        except ValueError as error:
            failures.append(dict(case=label, rejected=True, reason=str(error)))
        else:
            raise ValueError('Invalid signed/order packed ABI accepted')
    return dict(status='passed', positive=positive, negative=failures, sourceCredit=0)
