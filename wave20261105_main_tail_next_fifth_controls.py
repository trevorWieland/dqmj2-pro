import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261105_main_tail_next_fifth_bindings import verify_original, negative_controls
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
    directory = ROOT / 'work/w5tn/fifth-controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261105/main-tail-next/fifth/context.h'
    shutil.copyfile(header, directory / 'context.h')
    source = directory / 'layout.c'
    source.write_text('#include "context.h"\n')
    output = directory / 'layout.o'
    command = [str(COMPILER), *C.FLAGS, '-opt', 'speed', '-c', str(source), '-o', str(output)]
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
    if process.returncode:
        raise ValueError(('Native pointer-field layout assertions failed', process.stdout, process.stderr))
    positive = dict(compilerSha256=sha256(COMPILER), headerSha256=sha256(header), sourceSha256=sha256(source), objectSha256=sha256(output), exitCode=0,
                    facts=['word32','pointer32','WidgetFlags124','WidgetPrefix128','MenuPointers12And16','PageByte1AndPointer4','EntryStride8','SignedCursorBytes0And1'])
    failures = []
    for label, old, new in [('wrong-widget-flag-offset','opaque0[0x7c]','opaque0[0x78]'),
                            ('wrong-menu-pointers','opaque0[12]','opaque0[8]'),
                            ('wrong-entry-stride','u32 opaque4;','u32 opaque4[2];'),
                            ('wrong-page-pointer','u8 opaque2[2]','u8 opaque2[6]')]:
        if header.read_text().count(old) != 1:
            raise ValueError('Pointer-field layout mutation ambiguous')
        (directory / 'context.h').write_text(header.read_text().replace(old, new))
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
        if not process.returncode or 'illegal constant expression' not in process.stdout:
            raise ValueError(('Wrong native signed field/offset accepted', process.stdout, process.stderr))
        failures.append(dict(case=label, rejected=True, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr))
    return dict(status='passed', sourceCredit=0, bindingControls=checks, nativeCompilerLayout=positive, wrongNativeLayouts=failures, signedCursorAbi=signed_abi(header, directory))


def signed_abi(header, directory):
    import match_runtime as C
    import unicorn
    from unicorn import arm_const as R
    from elftools.elf.elffile import ELFFile
    source = directory / 'signed.c'
    source.write_text('#include "context.h"\ns32 abi_x(MenuCursor *p) { return p->x0; }\ns32 abi_y(MenuCursor *p) { return p->y1; }\n')
    output = directory / 'signed.o'
    command = [str(COMPILER), *C.FLAGS, '-opt', 'speed', '-c', str(source), '-o', str(output)]
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))

    def probe(text):
        (directory / 'context.h').write_text(text)
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
        if process.returncode:
            raise ValueError(('Actual native signed cursor ABI probe compile failed', process.stdout, process.stderr))
        records = []
        with output.open('rb') as stream:
            elf = ELFFile(stream)
            symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
            for name, offset in [('abi_x', 0), ('abi_y', 1)]:
                symbol = next(s for s in symbols if s.name == name)
                body = elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']]
                vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
                vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
                vm.mem_map(0x02300000, 0x2000)
                vm.mem_write(0x02300000, body)
                for value in range(256):
                    vm.mem_write(0x02301000, bytes([value, value, 0]))
                    vm.reg_write(R.UC_ARM_REG_R0, 0x02301000)
                    vm.reg_write(R.UC_ARM_REG_LR, 0x02300800)
                    vm.reg_write(R.UC_ARM_REG_SP, 0x02301f00)
                    vm.emu_start(0x02300000, 0x02300800, count=100)
                    actual = vm.reg_read(R.UC_ARM_REG_R0)
                    expected = (value if value < 128 else value - 256) & 0xffffffff
                    if actual != expected or vm.reg_read(R.UC_ARM_REG_PC) != 0x02300800:
                        raise ValueError(('Native signed cursor byte ABI differs', name, value, actual, expected))
                    records.append(dict(field=name, byte=value, returned=actual))
        return dict(sourceSha256=sha256(source), objectSha256=sha256(output), actualNativeAbiProbeReturns=len(records), cases=records, originalGameOrCalleeBodiesExecuted=0)

    text = header.read_text()
    positive = probe(text)
    failures = []
    for field in ['x0', 'y1']:
        old = 'signed char ' + field + ';'
        if text.count(old) != 1:
            raise ValueError('Signed cursor field mutation ambiguous')
        try:
            probe(text.replace(old, 'unsigned char ' + field + ';'))
        except ValueError as error:
            failures.append(dict(case='wrong-unsigned-' + field, rejected=True, reason=str(error)))
        else:
            raise ValueError('Wrong unsigned cursor ABI accepted')
    return dict(status='passed', positive=positive, negative=failures, sourceCredit=0)
