import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261104_main_tail_compiler import COMPILER, helper_binding
from wave20261104_main_command_forward_bindings import verify_original,negative_controls


def layout_checks():
    directory = ROOT / 'work/w4mcf/controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261104/main-command-forward/context.h'
    shutil.copyfile(header, directory / 'context.h')
    conditions = ['sizeof(CommandRecord) == 0x10c', '(u32)&((CommandRecord *)0)->status == 7',
                  '(u32)&((Context *)0)->bank == 3', '(u32)&((Context *)0)->parameters == 16',
                  '(u32)&((Context *)0)->records == 0x470', 'sizeof(Context) == 0x470',
                  '(u32)&((Instruction *)0)->advance == 4', '(u32)&((Instruction *)0)->payload == 8', 'sizeof(PackedFields4)==4', '(u32)&((PackedFields4*)0)->field2==2', '(u32)&((PackedFields4*)0)->field3==3', 'sizeof(Words4)==16', '(u32)&((ObjectPrefix*)0)->field18==0x18', 'sizeof(((ObjectPrefix*)0)->field18)==2', '(u32)&((ObjectPrefix*)0)->field1a==0x1a', '(u32)&((ObjectPrefix*)0)->field7a==0x7a', 'sizeof(Words3)==12', '(u32)&((ByteField8*)0)->field8==8', 'sizeof(((ByteField8*)0)->field8)==1']
    text = '#include "context.h"\n' + '\n'.join('typedef char NativeLayout' + str(i) + '[(' + expression + ') ? 1 : -1];' for i, expression in enumerate(conditions)) + '\n'
    source = directory / 'layout.c'
    source.write_text(text)
    output = directory / 'layout.o'
    command = [str(COMPILER), *C.FLAGS, '-opt', 'speed', '-c', str(source), '-o', str(output)]
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
    if process.returncode:
        raise ValueError(('Actual MW ABI witnesses failed', process.stdout, process.stderr))
    positive = dict(checks=conditions, compilerSha256=sha256(COMPILER), headerSha256=sha256(header),
                    sourceSha256=sha256(source), objectSha256=sha256(output), exitCode=process.returncode)
    wrong = header.read_text().replace('padding[0x104]', 'padding[0x100]')
    if wrong == header.read_text():
        raise ValueError('Layout mutation did not change the record stride')
    (directory / 'context.h').write_text(wrong)
    failed = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
    if failed.returncode == 0 or 'layout.c:2:' not in failed.stdout or 'illegal constant expression' not in failed.stdout:
        raise ValueError(('Wrong ABI layout did not fail its native compiler witnesses', failed.stdout, failed.stderr))
    return dict(positive=positive, wrongStrideRejected=True, wrongStrideExitCode=failed.returncode,
                wrongHeaderSha256=sha256(directory / 'context.h'), wrongCompileOutput=failed.stdout + failed.stderr, sourceCredit=0)


def execute(rows):
    checks = []

    def rejects(name, operation):
        try:
            operation()
        except ValueError as error:
            checks.append(dict(case=name, rejected=True, reason=str(error)))
            return
        raise ValueError('Invalid binding was accepted: ' + name)

    overlay = copy.deepcopy(next(row for row in rows if row['address'] == '0x20594ec'))
    helper = copy.deepcopy(next(row for row in rows if row['address'] == '0x20594ec'))
    overlay_name = 'native_fn_ov000_022096f4'
    bindings = copy.deepcopy(overlay['nativeSymbolEntries'])
    bindings[overlay_name]['module'] = 'ov001'
    rejects('same-address-wrong-overlay-at-original-main-02059508', lambda: verify_original(overlay, bindings))
    rejects('unknown-compiler-helper-name', lambda: helper_binding('_ffix_typo'))
    for name, field, value in [('wrong-helper-address-valid-other-native-entry', 'address', '0x2025a28'),
                               ('wrong-helper-mode', 'mode', 'thumb'), ('wrong-helper-CPU', 'processor', 'arm7'),
                               ('wrong-helper-program', 'program', 'dwc/utility.bin/move/child.srl'),
                               ('wrong-helper-kind', 'kind', 'data')]:
        changed = copy.deepcopy(helper['nativeSymbolEntries'])
        changed['_ffixu'][field] = value
        rejects(name, lambda changed=changed: verify_original(helper, changed))
    changed_row = copy.deepcopy(helper)
    relocation = next(row for row in changed_row['relocations'] if row['symbol'] == '_ffixu')
    relocation['symbol'] = '_ffix_typo'
    changed_bindings = copy.deepcopy(helper['nativeSymbolEntries'])
    changed_bindings['_ffix_typo'] = changed_bindings.pop('_ffixu')
    rejects('matching-address-with-unknown-helper-symbol', lambda: verify_original(changed_row, changed_bindings))
    for row in rows:
        verify_original(row, row['nativeSymbolEntries'])
    layout = layout_checks()
    data = negative_controls(rows)
    return dict(status='passed', dataLoadQualification=data, negativeBindingCases=checks, actualCompilerLayoutWitnesses=layout,
                originalMainToOverlayCallsite='0x02059508', originalMainToOverlayTarget='ov000:0x022096f4',
                originalSP1SymbolNamesRelocationsAndEncodedInstructionsUnchanged=True, sourceCredit=0)
