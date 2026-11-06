import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
import link_runtime_unit as L
from wave20261104_main_bank_build import build
from wave20261104_main_bank_models import run
from wave20261104_main_bank_compiler import COMPILER, helper_binding
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

    overlay = copy.deepcopy(next(row for row in rows if row['address'] == '0x20534e4'))
    bindings = copy.deepcopy(overlay['nativeSymbolEntries'])
    bindings['native_fn_ov000_02229f68']['module'] = 'ov001'
    reject('same-numeric-overlay-target-with-wrong-original-module', lambda: verify_original(overlay, bindings))
    helper = copy.deepcopy(next(row for row in rows if row['address'] == '0x2053114'))
    for label, field, value in [('address', 'address', '0x2025a28'), ('mode', 'mode', 'thumb'), ('CPU', 'processor', 'arm7'),
                                ('program', 'program', 'dwc/utility.bin/move/child.srl'), ('kind', 'kind', 'data')]:
        changed = copy.deepcopy(helper['nativeSymbolEntries'])
        changed['_ffix'][field] = value
        reject('wrong-helper-' + label, lambda changed=changed: verify_original(helper, changed))
    reject('unknown-helper-name', lambda: helper_binding('_ffix_typo'))
    badrow = copy.deepcopy(helper)
    next(r for r in badrow['relocations'] if r['symbol'] == '_ffix')['symbol'] = '_ffix_typo'
    badbindings = copy.deepcopy(helper['nativeSymbolEntries'])
    badbindings['_ffix_typo'] = badbindings.pop('_ffix')
    reject('unknown-helper-at-correct-numeric-address', lambda: verify_original(badrow, badbindings))
    for row in rows:
        verify_original(row, row['nativeSymbolEntries'])
    directory = ROOT / 'work/w4mb/controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261104/main-bank-next/context.h'
    shutil.copyfile(header, directory / 'context.h')
    assertions = ['sizeof(CommandRecord) == 0x10c', '(u32)&((CommandRecord *)0)->status == 7',
                  '(u32)&((Context *)0)->bank == 3', '(u32)&((Context *)0)->parameters == 16',
                  '(u32)&((Context *)0)->records == 0x470', 'sizeof(Context) == 0x470',
                  '(u32)&((Instruction *)0)->advance == 4', '(u32)&((Instruction *)0)->payload == 8', 'sizeof(NativeRecord) == 0x84', '(u32)&((NativeRecord *)0)->field14 == 0x14', '(u32)&((NativeRecord *)0)->field18 == 0x18', '(u32)&((NativeRecord *)0)->field1a == 0x1a', '(u32)&((NativeRecord *)0)->field1b == 0x1b', '(u32)&((NativeRecord *)0)->field1e == 0x1e', 'sizeof(s16) == 2', 'sizeof(u32) == 4']
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
    info, main, unused = L.measured_module('main')
    overlay_info, overlay_bytes, unused = L.measured_module('ov000')
    semantic = []
    for name, label, old, new, required in [
            ('02053088', 'ninety-nine-record-loop', 'index < 100', 'index < 99', [0, 2, 3, 4, 6, 7]),
            ('0205321c', 'wrong-gate-false-sentinel', 'int result = -1;', 'int result = 0;', [0, 2, 4, 6])]:
        original_source = ROOT / 'src/runtime/parallel_wave20261104/main-bank-next' / (name + '.c')
        text = original_source.read_text()
        if text.count(old) != 1:
            raise ValueError('Semantic whole-C mutation ambiguous')
        folder = ROOT / 'work/w4mb/controls' / label
        folder.mkdir(parents=True, exist_ok=True)
        wrong_source = folder / 'source.c'
        wrong_source.write_text(text.replace(old, new))
        shutil.copyfile(header, folder / 'context.h')
        row, body = build(wrong_source, folder / 'build', True)
        rejected = [ordinal for ordinal in range(8) if run(row, body, ordinal, main, overlay_bytes)['modelFailures']]
        if rejected != required:
            raise ValueError(('Semantic branch mutation not independently rejected', label, rejected))
        semantic.append(dict(case=label, sourceSha256=sha256(wrong_source), rejectedCases=rejected, proof=row))
    return dict(status='passed', sourceCredit=0, bindingControls=checks, semanticWholeCControls=semantic, nativeCompilerLayout=positive,
                wrongStride=dict(rejected=True, exitCode=failed.returncode, stdout=failed.stdout, stderr=failed.stderr))
