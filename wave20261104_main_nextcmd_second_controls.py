import copy
import os
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261104_main_tail_compiler import COMPILER, helper_binding
from wave20261104_main_tail_bindings import verify_original


def layout_checks():
    directory = ROOT / 'work/w4nc/second/controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    old = ROOT / 'src/runtime/parallel_wave20261104/main-runtime-tail/context.h'
    header = ROOT / 'src/runtime/parallel_wave20261104/main-command-next/second/context.h'
    text = header.read_text()
    include = '#include "../../main-runtime-tail/context.h"'
    if text.count(include) != 1:
        raise ValueError('Measured context include differs')
    flattened = text.replace(include, old.read_text())
    (directory / 'context.h').write_text(flattened)
    conditions = ['sizeof(CommandRecord) == 0x10c', '(u32)&((CommandRecord *)0)->status == 7',
        '(u32)&((Context *)0)->bank == 3', '(u32)&((Context *)0)->parameters == 16',
        '(u32)&((Context *)0)->records == 0x470', 'sizeof(Context) == 0x470',
        '(u32)&((Instruction *)0)->advance == 4', '(u32)&((Instruction *)0)->payload == 8',
        'sizeof(int) == 4', 'sizeof(short) == 2', 'sizeof(signed char) == 1', 'sizeof(NativeVec3) == 12',
        '(u32)&((NativeVec3 *)0)->y == 4', '(u32)&((NativeVec3 *)0)->z == 8',
        'sizeof(CommandContext) == 0x470', '(u32)&((CommandContext *)0)->records == 0x470',
        '(u32)&((CommandContext *)0)->parameters[13] == 0x44', 'sizeof(TargetRecord) == 0xb8',
        '(u32)&((TargetRecord *)0)->state09 == 9', '(u32)&((TargetRecord *)0)->slot70 == 0x70',
        '(u32)&((TargetRecord *)0)->slot88 == 0x88', '(u32)&((TargetRecord *)0)->slot88[1] == 0x8c']
    source = directory / 'layout.c'
    source.write_text('#include "context.h"\n' + '\n'.join('typedef char NativeLayout' + str(i) + '[(' + expression + ') ? 1 : -1];' for i, expression in enumerate(conditions)) + '\n')
    output = directory / 'layout.o'
    command = [str(COMPILER), *C.FLAGS, '-opt', 'speed', '-c', str(source), '-o', str(output)]
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

    overlay = next(row for row in rows if row['address'] == '0x20508ac')
    helper = next(row for row in rows if row['address'] == '0x20507b0')
    changed = copy.deepcopy(overlay['nativeSymbolEntries'])
    changed['native_fn_ov000_021e582c']['module'] = 'ov001'
    rejects('same-address-wrong-overlay-at-original-main-02050bf4', lambda: verify_original(overlay, changed))
    rejects('unknown-helper-name', lambda: helper_binding('_ffix_typo'))
    for name, field, value in [('wrong-helper-address', 'address', '0x2025a28'), ('wrong-helper-mode', 'mode', 'thumb'),
        ('wrong-helper-CPU', 'processor', 'arm7'), ('wrong-helper-program', 'program', 'dwc/utility.bin/move/child.srl'),
        ('wrong-helper-kind', 'kind', 'data')]:
        changed = copy.deepcopy(helper['nativeSymbolEntries'])
        changed['_ffix'][field] = value
        rejects(name, lambda changed=changed: verify_original(helper, changed))
    renamed = copy.deepcopy(helper)
    next(item for item in renamed['relocations'] if item['symbol'] == '_ffix')['symbol'] = '_ffix_typo'
    changed = copy.deepcopy(helper['nativeSymbolEntries'])
    changed['_ffix_typo'] = changed.pop('_ffix')
    rejects('unknown-helper-with-valid-address', lambda: verify_original(renamed, changed))
    for row in rows:
        verify_original(row, row['nativeSymbolEntries'])
    return dict(status='passed', negativeBindingCases=checks, actualCompilerLayoutWitnesses=layout_checks(),
        ambiguousOriginalOverlayCandidateSetsExcluded=True, sourceCredit=0)
