import copy
import os
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261104_main_tail_compiler import COMPILER, helper_binding
from wave20261104_main_nextcmd_cmp_bindings import verify_original
from wave20261104_main_nextcmd_cmp_abi import HELPERS, binding, qualify_binding


def flattened_context():
    old = ROOT / 'src/runtime/parallel_wave20261104/main-runtime-tail/context.h'
    shared = ROOT / 'src/runtime/parallel_wave20261104/main-command-next/second/context.h'
    header = ROOT / 'src/runtime/parallel_wave20261104/main-command-next/sixth/context.h'
    first_include = '#include "../second/context.h"'
    second_include = '#include "../../main-runtime-tail/context.h"'
    text, shared_text = header.read_text(), shared.read_text()
    if text.count(first_include) != 1 or shared_text.count(second_include) != 1:
        raise ValueError('Frozen nested context include differs')
    return text.replace(first_include, shared_text.replace(second_include, old.read_text()))


def layout_checks():
    directory = ROOT / 'work/w4nc/sixth/controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    old = ROOT / 'src/runtime/parallel_wave20261104/main-runtime-tail/context.h'
    header = ROOT / 'src/runtime/parallel_wave20261104/main-command-next/sixth/context.h'
    flattened = flattened_context()
    (directory / 'context.h').write_text(flattened)
    conditions = ['sizeof(CommandRecord) == 0x10c', '(u32)&((CommandRecord *)0)->status == 7',
        '(u32)&((Context *)0)->bank == 3', '(u32)&((Context *)0)->parameters == 16',
        '(u32)&((Context *)0)->records == 0x470', 'sizeof(Context) == 0x470',
        '(u32)&((Instruction *)0)->advance == 4', '(u32)&((Instruction *)0)->payload == 8',
        'sizeof(int) == 4', 'sizeof(short) == 2', 'sizeof(signed char) == 1', 'sizeof(NativeVec3) == 12',
        '(u32)&((NativeVec3 *)0)->y == 4', '(u32)&((NativeVec3 *)0)->z == 8',
        'sizeof(float) == 4', '(u32)&((Context *)0)->parameters[6] == 0x28', 'sizeof(MeasureRecord) == 0x7a',
        '(u32)&((MeasureRecord *)0)->field18 == 0x18', '(u32)&((MeasureRecord *)0)->field1a == 0x1a',
        '(u32)&((MeasureRecord *)0)->data20 == 0x20', '(u32)&((MeasureRecord *)0)->data7a == 0x7a',
        'sizeof(u8[64]) == 64']
    source = directory / 'layout.c'
    source.write_text('#include "context.h"\n' + '\n'.join('typedef char NativeLayout' + str(i) + '[(' + expression + ') ? 1 : -1];' for i, expression in enumerate(conditions)) + '\n')
    output = directory / 'layout.o'
    command = [str(COMPILER), *C.FLAGS, '-lang', 'c99', '-opt', 'speed', '-c', str(source), '-o', str(output)]
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
    if process.returncode:
        raise ValueError(('MW layout witnesses failed', process.stdout, process.stderr))
    positive = dict(checks=conditions, compilerSha256=sha256(COMPILER), oldContextSha256=sha256(old),
        headerSha256=sha256(header), sourceSha256=sha256(source), objectSha256=sha256(output), exitCode=process.returncode)
    wrong = flattened.replace('padding[0x104]', 'padding[0x100]')
    if wrong == flattened:
        raise ValueError('Layout mutation did not change record stride')
    (directory / 'context.h').write_text(wrong)
    failed = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
    if failed.returncode == 0 or 'illegal constant expression' not in failed.stdout:
        raise ValueError(('Wrong layout was not rejected', failed.stdout, failed.stderr))
    return dict(positive=positive, wrongStrideRejected=True, wrongHeaderSha256=sha256(directory / 'context.h'),
        wrongCompileOutput=failed.stdout + failed.stderr, sourceCredit=0)


def execute(rows):
    checks = []

    def rejects(name, operation):
        try:
            operation()
        except ValueError as error:
            checks.append(dict(case=name, rejected=True, reason=str(error)))
            return
        raise ValueError('Invalid binding accepted: ' + name)

    caller = rows[0]
    rejects('unknown-comparison-helper-name', lambda: binding('_fle_typo'))
    for case, field, value in [('swapped-comparison-entry', 'address', '0x2025440'),
        ('comparison-interior-entry', 'address', '0x20253dc'), ('wrong-comparison-mode', 'mode', 'thumb'),
        ('wrong-comparison-CPU', 'processor', 'arm7'), ('wrong-comparison-program', 'program', 'dwc/utility.bin/move/child.srl'),
        ('wrong-comparison-module', 'module', 'ov000'), ('wrong-comparison-kind', 'kind', 'data')]:
        changed = copy.deepcopy(caller['nativeSymbolEntries'])
        changed['_fleq'][field] = value
        rejects(case, lambda changed=changed: verify_original(caller, changed))
    changed_row = copy.deepcopy(caller)
    next(item for item in changed_row['relocations'] if item['symbol'] == '_fleq')['target'] = '0x2025440'
    rejects('relocation-target-disagrees-with-qualified-original-entry', lambda: verify_original(changed_row, caller['nativeSymbolEntries']))
    changed_row = copy.deepcopy(caller)
    next(item for item in changed_row['relocations'] if item['symbol'] == '_fleq')['offset'] += 4
    rejects('helper-callsite-moved-within-native-caller', lambda: verify_original(changed_row, caller['nativeSymbolEntries']))
    changed_row = copy.deepcopy(caller)
    next(item for item in changed_row['relocations'] if item['symbol'] == '_fleq')['type'] = 10
    rejects('Thumb-relocation-type-for-original-ARM-BL', lambda: verify_original(changed_row, caller['nativeSymbolEntries']))
    for row in rows:
        verify_original(row, row['nativeSymbolEntries'])
    return dict(status='passed', negativeBindingCases=checks, actualCompilerLayoutWitnesses=layout_checks(),
        ambiguousOriginalOverlayCandidateSetsExcluded=True, sourceCredit=0)
