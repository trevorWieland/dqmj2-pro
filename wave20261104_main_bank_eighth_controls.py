import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
import link_runtime_unit as L
from wave20261104_main_bank_build import build
from wave20261104_main_bank_eighth_models import run
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

    overlay = copy.deepcopy(next(row for row in rows if row['address'] == '0x20540f4'))
    bindings = copy.deepcopy(overlay['nativeSymbolEntries'])
    bindings['native_fn_ov000_021e07b8']['module'] = 'ov001'
    reject('same-numeric-overlay-target-with-wrong-original-module', lambda: verify_original(overlay, bindings))
    helper = copy.deepcopy(next(row for row in rows if row['address'] == '0x20558ac'))
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
    directory = ROOT / 'work/w4mb/eighth-controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261104/main-bank-next/eighth/context.h'
    shutil.copyfile(header, directory / 'context.h')
    assertions = ['sizeof(CommandRecord) == 0x10c', '(u32)&((CommandRecord *)0)->status == 7',
                  '(u32)&((Context *)0)->bank == 3', '(u32)&((Context *)0)->parameters == 16',
                  '(u32)&((Context *)0)->records == 0x470', 'sizeof(Context) == 0x470',
                  '(u32)&((Instruction *)0)->advance == 4', '(u32)&((Instruction *)0)->payload == 8',
                  'sizeof(int) == 4', 'sizeof(float) == 4', 'sizeof(u32) == 4', 'sizeof(long long) == 8',
                  'sizeof(Vec3) == 12', '(u32)&((Vec3 *)0)->y == 4', '(u32)&((Vec3 *)0)->z == 8',
                  '(u32)&((SceneState *)0)->position == 0x70', '(u32)&((SceneState *)0)->matrix == 0x210', 'sizeof(SceneState) == 0x210']
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
            ('0205443c', 'apply-gate-before-required-intersection', 'native_fn_ov000_021da5e4(point, state->matrix, &result, 1) && apply', 'apply && native_fn_ov000_021da5e4(point, state->matrix, &result, 1)', [0, 3, 5]),
            ('020558ac', 'missing-fixed-product-rounding', 'FX_MUL', 'FX_MUL', [0, 1, 2, 4, 5, 6, 7])]:
        original_source = ROOT / 'src/runtime/parallel_wave20261104/main-bank-next/eighth' / (name + '.c')
        text = original_source.read_text()
        if label != 'missing-fixed-product-rounding' and text.count(old) != 1:
            raise ValueError('Semantic whole-C mutation ambiguous')
        folder = ROOT / 'work/w4mb/eighth-controls' / label
        folder.mkdir(parents=True, exist_ok=True)
        wrong_source = folder / 'source.c'
        wrong_source.write_text(text.replace(old, new))
        shutil.copyfile(header, folder / 'context.h')
        if label == 'missing-fixed-product-rounding':
            copied_header = folder / 'context.h'
            original_header = copied_header.read_text()
            if original_header.count('+ 2048') != 1:
                raise ValueError('Header rounding mutation ambiguous')
            copied_header.write_text(original_header.replace('+ 2048', '+ 0'))
        row, body = build(wrong_source, folder / 'build', True)
        rejected = [ordinal for ordinal in range(8) if run(row, body, ordinal, main, overlay_bytes)['modelFailures']]
        if rejected != required:
            raise ValueError(('Semantic branch mutation not independently rejected', label, rejected))
        semantic.append(dict(case=label, sourceSha256=sha256(wrong_source), headerSha256=sha256(folder / 'context.h'), rejectedCases=rejected, proof=row))
    return dict(status='passed', sourceCredit=0, bindingControls=checks, semanticWholeCControls=semantic, nativeCompilerLayout=positive,
                wrongStride=dict(rejected=True, exitCode=failed.returncode, stdout=failed.stdout, stderr=failed.stderr))
