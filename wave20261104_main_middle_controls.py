import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261104_main_middle_bindings import negative_controls, verify_original
from wave20261104_main_middle_compiler import COMPILER


def execute(rows):
    result = negative_controls(rows)
    row = next(row for row in rows if row['address'] == '0x2047428')
    branch = 'native_fn_02047b90'
    for label, key, value in [('wrong-callee-mode', 'mode', 'thumb'), ('wrong-callee-kind', 'kind', 'data'),
                              ('wrong-callee-module', 'module', 'ov000'), ('wrong-callee-address', 'address', '0x2047bfc')]:
        bindings = copy.deepcopy(row['nativeSymbolEntries'])
        bindings[branch][key] = value
        try:
            verify_original(row, bindings)
        except ValueError as error:
            result['negativeCases'].append(dict(case=label, rejected=True, reason=str(error)))
        else:
            raise ValueError('Invalid original branch binding accepted: ' + label)
    directory = ROOT / 'work/w4mm/first-controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261104/main-command-middle/first/context.h'
    shutil.copyfile(header, directory / 'context.h')
    source = directory / 'layout.c'
    source.write_text('#include "context.h"\ntypedef char CursorFieldWidth[(sizeof(((TextCursor *)0)->field80) == 2) ? 1 : -1];\n')
    output = directory / 'layout.o'
    command = [str(COMPILER), *C.FLAGS, '-opt', 'speed', '-c', str(source), '-o', str(output)]
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
    if process.returncode:
        raise ValueError(('Native layout assertions failed', process.stdout, process.stderr))
    result['nativeCompilerLayout'] = dict(compilerSha256=sha256(COMPILER), headerSha256=sha256(header),
                                         sourceSha256=sha256(source), objectSha256=sha256(output), exitCode=0,
                                         facts=['fieldOffset128', 'minimumTypedPrefix130', 'fieldWidth2', 'wordWidth4'])
    failures = []
    for label, old, new in [('wrong-prefix-offset', 'reserved[0x80]', 'reserved[0x7e]'),
                            ('wrong-field-width', 'u16 field80', 'u32 field80')]:
        if header.read_text().count(old) != 1:
            raise ValueError('Layout mutation ambiguous')
        (directory / 'context.h').write_text(header.read_text().replace(old, new))
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
        if not process.returncode or 'illegal constant expression' not in process.stdout:
            raise ValueError(('Wrong native field layout accepted', process.stdout, process.stderr))
        failures.append(dict(case=label, rejected=True, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr))
    result['wrongNativeLayouts'] = failures
    return result
