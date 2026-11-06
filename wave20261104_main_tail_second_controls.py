import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261104_main_tail_compiler import COMPILER, helper_binding
from wave20261104_main_tail_bindings import verify_original


def execute(rows):
    checks = []

    def reject(name, operation):
        try:
            operation()
        except ValueError as error:
            checks.append(dict(case=name, rejected=True, reason=str(error)))
            return
        raise ValueError('Invalid namespace/helper accepted: ' + name)

    overlay = copy.deepcopy(next(row for row in rows if row['address'] == '0x20574dc'))
    bindings = copy.deepcopy(overlay['nativeSymbolEntries'])
    bindings['native_fn_ov000_02214a54']['module'] = 'ov001'
    reject('same-numeric-overlay-target-with-wrong-original-module', lambda: verify_original(overlay, bindings))
    helper = copy.deepcopy(next(row for row in rows if row['address'] == '0x2057434'))
    for label, field, value in [('address', 'address', '0x2025a28'), ('mode', 'mode', 'thumb'), ('CPU', 'processor', 'arm7'),
                                ('program', 'program', 'dwc/utility.bin/move/child.srl'), ('kind', 'kind', 'data')]:
        changed = copy.deepcopy(helper['nativeSymbolEntries'])
        changed['_ffixu'][field] = value
        reject('wrong-helper-' + label, lambda changed=changed: verify_original(helper, changed))
    reject('unknown-helper-name', lambda: helper_binding('_ffixu_typo'))
    badrow = copy.deepcopy(helper)
    next(r for r in badrow['relocations'] if r['symbol'] == '_ffixu')['symbol'] = '_ffixu_typo'
    badbindings = copy.deepcopy(helper['nativeSymbolEntries'])
    badbindings['_ffixu_typo'] = badbindings.pop('_ffixu')
    reject('unknown-helper-at-correct-numeric-address', lambda: verify_original(badrow, badbindings))
    for row in rows:
        verify_original(row, row['nativeSymbolEntries'])
    directory = ROOT / 'work/w4mt/second-controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261104/main-runtime-tail/second/context.h'
    shutil.copyfile(header, directory / 'context.h')
    assertions = ['sizeof(CommandRecord) == 0x10c', '(u32)&((CommandRecord *)0)->status == 7',
                  '(u32)&((Context *)0)->bank == 3', '(u32)&((Context *)0)->parameters == 16',
                  '(u32)&((Context *)0)->records == 0x470', 'sizeof(Context) == 0x470',
                  '(u32)&((Instruction *)0)->advance == 4', '(u32)&((Instruction *)0)->payload == 8']
    source = directory / 'layout.c'
    source.write_text('#include "context.h"\n' + '\n'.join('typedef char Check' + str(i) + '[(' + expression + ') ? 1 : -1];' for i, expression in enumerate(assertions)) + '\n')
    output = directory / 'layout.o'
    command = [str(COMPILER), *C.FLAGS, '-opt', 'speed', '-c', str(source), '-o', str(output)]
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise ValueError(('Actual native ABI assertions failed', result.stdout, result.stderr))
    positive = dict(assertions=assertions, sourceSha256=sha256(source), headerSha256=sha256(header),
                    objectSha256=sha256(output), compilerSha256=sha256(COMPILER), exitCode=0)
    wrong = header.read_text().replace('padding[0x104]', 'padding[0x100]')
    if wrong == header.read_text():
        raise ValueError('Record stride mutation absent')
    (directory / 'context.h').write_text(wrong)
    failed = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
    if not failed.returncode or 'layout.c:2:' not in failed.stdout or 'illegal constant expression' not in failed.stdout:
        raise ValueError(('Wrong stride did not fail native assertion', failed.stdout, failed.stderr))
    return dict(status='passed', sourceCredit=0, bindingControls=checks, nativeCompilerLayout=positive,
                wrongStride=dict(rejected=True, exitCode=failed.returncode, stdout=failed.stdout, stderr=failed.stderr))
