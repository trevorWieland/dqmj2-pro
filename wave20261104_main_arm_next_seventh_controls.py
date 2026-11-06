import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261104_main_tail_bindings import verify_original
from wave20261104_main_arm_next_compiler import COMPILER


def execute(rows):
    checks = []
    for row in rows:
        symbol = 'native_fn_02038d88' if row['address'] == '0x2039ab0' else 'native_fn_02038dec'
        for label, key, value in [('wrong-mode', 'mode', 'thumb'), ('function-as-data', 'kind', 'data'),
                                  ('same-address-wrong-overlay', 'module', 'ov000'), ('wrong-address', 'address', '0x2031fa8'),
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
    directory = ROOT / 'work/w4an/seventh-controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261104/main-arm-next/seventh/context.h'
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
                    facts=['word4', 'recordHalfword4at4', 'recordByte8at8', 'recordByte9at9', 'unsignedFieldWidths'])
    failures = []
    for label, old, new in [('wrong-word-width', 'typedef unsigned int u32;', 'typedef unsigned short u32;'),
                            ('wrong-halfword-width', 'u16 field4;', 'u32 field4;'),
                            ('wrong-byte-offset', 'opaque6[2]', 'opaque6[1]'),
                            ('wrong-field9-width', 'u8 field9;', 'unsigned short field9;')]:
        if header.read_text().count(old) != 1:
            raise ValueError('Pointer-field layout mutation ambiguous')
        (directory / 'context.h').write_text(header.read_text().replace(old, new))
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
        if not process.returncode or 'illegal constant expression' not in process.stdout:
            raise ValueError(('Wrong native signed field/offset accepted', process.stdout, process.stderr))
        failures.append(dict(case=label, rejected=True, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr))
    return dict(status='passed', sourceCredit=0, bindingControls=checks, nativeCompilerLayout=positive, wrongNativeLayouts=failures)
