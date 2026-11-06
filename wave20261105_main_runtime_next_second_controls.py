import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261105_main_runtime_next_second_bindings import verify_original, negative_controls
from wave20261105_main_runtime_next_compiler import COMPILER


def execute(rows):
    checks = negative_controls(rows)['negativeCases']
    for row in rows:
        for symbol, binding in row['nativeSymbolEntries'].items():
            if binding['kind'] != 'function':
                continue
            wrong_module = 'ov001' if binding['module'] == 'ov000' else 'ov000'
            for label, key, value in [('wrong-mode', 'mode', 'thumb'), ('function-as-data', 'kind', 'data'),
                                      ('same-address-wrong-module', 'module', wrong_module), ('wrong-address', 'address', hex(int(binding['address'], 0) + 4)),
                                      ('wrong-CPU', 'processor', 'arm7'), ('wrong-program', 'program', 'child')]:
                bindings = copy.deepcopy(row['nativeSymbolEntries'])
                bindings[symbol][key] = value
                try:
                    verify_original(row, bindings)
                except ValueError as error:
                    checks.append(dict(symbol=symbol, caller=row['address'], case=label, rejected=True, reason=str(error)))
                else:
                    raise ValueError('Invalid original state main/ov000 callee identity accepted')
        verify_original(row, row['nativeSymbolEntries'])
    directory = ROOT / 'work/w5rn/second-controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261105/main-runtime-next/second/context.h'
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
                    facts=['transitionByte0', 'transitionWord4', 'modeDesiredWord0', 'modeCurrentWord4', 'bothMinimumPrefixes8'])
    failures = []
    for label, old, new in [('wrong-word-width', 'typedef unsigned int u32;', 'typedef unsigned short u32;'),
                            ('wrong-step-offset', 'opaque1[3]', 'opaque1[7]'),
                            ('wrong-mode-current-offset', 'u32 desired0;', 'unsigned long long desired0;'),
                            ('wrong-choice-width', 'u8 choice0;', 'u32 choice0;')]:
        if header.read_text().count(old) != 1:
            raise ValueError('Pointer-field layout mutation ambiguous')
        (directory / 'context.h').write_text(header.read_text().replace(old, new))
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
        if not process.returncode or 'illegal constant expression' not in process.stdout:
            raise ValueError(('Wrong native signed field/offset accepted', process.stdout, process.stderr))
        failures.append(dict(case=label, rejected=True, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr))
    return dict(status='passed', sourceCredit=0, bindingControls=checks, nativeCompilerLayout=positive, wrongNativeLayouts=failures)

