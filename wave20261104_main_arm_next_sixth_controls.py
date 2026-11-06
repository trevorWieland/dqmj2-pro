import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261104_main_arm_next_sixth_bindings import verify_original, negative_controls
from wave20261104_main_arm_next_compiler import COMPILER


def execute(rows):
    data = negative_controls(rows)
    checks = data['negativeCases']
    for row in rows:
        verify_original(row, row['nativeSymbolEntries'])
    directory = ROOT / 'work/w4an/sixth-controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261104/main-arm-next/sixth/context.h'
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
                    facts=['word4', 'managerBlob140', 'managerPrefix144', 'blobPrefix40', 'tableItems4', 'tableStride4', 'flexibleArraysNoInventedBounds'])
    failures = []
    for label, old, new in [('wrong-word-width', 'typedef unsigned int u32;', 'typedef unsigned short u32;'),
                            ('wrong-manager-field', 'opaque00[0x8c]', 'opaque00[0x88]'),
                            ('wrong-table-stride', 'u32 offsets[];', 'unsigned short offsets[];'),
                            ('wrong-blob-prefix', 'u8 header00[8]', 'u8 header00[4]')]:
        if header.read_text().count(old) != 1:
            raise ValueError('Pointer-field layout mutation ambiguous')
        (directory / 'context.h').write_text(header.read_text().replace(old, new))
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
        if not process.returncode or 'illegal constant expression' not in process.stdout:
            raise ValueError(('Wrong native signed field/offset accepted', process.stdout, process.stderr))
        failures.append(dict(case=label, rejected=True, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr))
    return dict(status='passed', sourceCredit=0, bindingControls=checks, nativeCompilerLayout=positive, wrongNativeLayouts=failures)
