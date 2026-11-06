import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261104_main_middle_fifth_bindings import verify_original, negative_controls
from wave20261104_main_middle_compiler import COMPILER


def execute(rows):
    data = negative_controls(rows)
    checks = data['negativeCases']
    row = next(row for row in rows if row['address'] == '0x2049be4')
    for label, key, value in [('wrong-mode', 'mode', 'thumb'), ('function-as-data', 'kind', 'data'),
                              ('same-address-wrong-overlay', 'module', 'ov000'), ('wrong-address', 'address', '0x205fe24'),
                              ('wrong-CPU', 'processor', 'arm7'), ('wrong-program', 'program', 'child')]:
        bindings = copy.deepcopy(row['nativeSymbolEntries'])
        bindings['native_fn_0205fe20'][key] = value
        try:
            verify_original(row, bindings)
        except ValueError as error:
            checks.append(dict(case=label, rejected=True, reason=str(error)))
        else:
            raise ValueError('Invalid original pointer-field callee binding accepted')
    for row in rows:
        verify_original(row, row['nativeSymbolEntries'])
    directory = ROOT / 'work/w4mm/fifth-controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261104/main-command-middle/eighth/context.h'
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
                    facts=['word4', 'argumentBlock16', 'blockOffsets4and8and12', 'entryMinimumView8', 'entryTagOffset6', 'signedAndUnsignedByte1'])
    failures = []
    for label, old, new in [('wrong-argument-block-view', 'u32 input;', 'u32 input; u32 extra;'),
                            ('reversed-argument-controls', 'u32 enabled; u32 include4;', 'u32 include4; u32 enabled;'),
                            ('wrong-entry-tag-offset', 's8 field5; s8 field6;', 's8 field5; u8 extra; s8 field6;'),
                            ('wrong-signed-byte', 'typedef signed char s8;', 'typedef unsigned char s8;')]:
        if header.read_text().count(old) != 1:
            raise ValueError('Pointer-field layout mutation ambiguous')
        (directory / 'context.h').write_text(header.read_text().replace(old, new))
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
        if not process.returncode or 'illegal constant expression' not in process.stdout:
            raise ValueError(('Wrong native signed field/offset accepted', process.stdout, process.stderr))
        failures.append(dict(case=label, rejected=True, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr))
    return dict(status='passed', sourceCredit=0, bindingControls=checks, nativeCompilerLayout=positive, wrongNativeLayouts=failures)
