import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_arm_next_eighth_build import build
from wave20261104_main_arm_next_eighth_models import SPECS, fixtures, run
from wave20261104_main_arm_next_eighth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-arm-next/eighth'
WORK = ROOT / 'work/w4an/eighth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-arm-next/eighth'


def mutation(source, name, old, new, row, main, selected):
    text = source.read_text()
    if text.count(old) != 1:
        raise ValueError('Whole-C mutation ambiguous: ' + name)
    folder = WORK / name / 'negative'
    folder.mkdir(parents=True, exist_ok=True)
    wrong = folder / 'source.c'
    wrong.write_text(text.replace(old, new))
    shutil.copyfile(SOURCE / 'context.h', folder / 'context.h')
    badrow, body = build(wrong, folder / 'build', True)
    rejected = []
    for ordinal, fixture in enumerate(selected):
        if run(badrow, body, fixture, main, ordinal)['modelFailures']:
            rejected.append(ordinal)
    if len(rejected) != len(selected):
        raise ValueError(('Whole-C mutation not independently rejected', name, rejected))
    return dict(case=name, old=old, new=new, rejectedCases=rejected, fixtures=selected, proof=badrow)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen input changed: ' + pin['path'])
    if {format(int(row['address'], 0), '08x') for row in inputs['entries']} != set(SPECS):
        raise ValueError('Frozen text-family identity set differs')
    info, main, unused = L.measured_module('main')
    matches, traces, negatives = [], [], []
    for item in inputs['entries']:
        name = format(int(item['address'], 0), '08x')
        source = ROOT / item['source']
        row, body = build(source, WORK / name / 'positive')
        if row['targetSha256'] != item['targetSha256'] or row['bytes'] != item['bytes']:
            raise ValueError('Frozen caller span differs')
        at = int(row['address'], 0) - 0x02000000
        native = main[at:at + row['bytes']]
        for ordinal, fixture in enumerate(fixtures(name)):
            original = run(row, native, fixture, main, ordinal)
            rebuilt = run(row, body, fixture, main, ordinal)
            if original != rebuilt or original['modelFailures']:
                write_json(LANE / 'fixture-failure.json', dict(address=row['address'], fixture=fixture, original=original, rebuilt=rebuilt))
                raise ValueError(('Independent text protocol/full-state differs', name, ordinal, original['modelFailures']))
            traces.append(dict(address=row['address'], ordinal=ordinal, fixture=fixture, result=original))
        matches.append(row)
        print('proved', name, row['bytes'], len(fixtures(name)), flush=True)
    all_cases = fixtures('020294cc')
    dirty = [f for f in all_cases if f['dirty']]
    cases = [('020294cc', 'wrong-dirty-branch', 'if (state->dirty0f)', 'if (!state->dirty0f)', all_cases),
             ('020294cc', 'wrong-first-matrix-order', '&yrotation, &zrotation, &combined', '&zrotation, &yrotation, &combined', dirty),
             ('020294cc', 'wrong-dirty-clear', 'state->dirty0f = 0;', 'state->dirty0f = 1;', dirty),
             ('020294cc', 'wrong-flags-mask', 'flagsfc &= ~0xa4u;', 'flagsfc |= 0xa4u;', all_cases),
             ('020294cc', 'wrong-scale-pointer', 'native_fn_0202e6cc(&state->scale1c)', 'native_fn_0202e6cc(&state->position10)', all_cases),
             ('020294cc', 'wrong-model-cache', 'model = state->model08;', 'model = 0;', all_cases),
             ('020294cc', 'wrong-late-material-byte', 'model, 0, state->field0d', 'model, 0, (u8)(state->field0d + 1)', all_cases),
             ('020294cc', 'wrong-success-return', 'return 1;', 'return 0;', all_cases)]
    for name, label, old, new, selected in cases:
        if not selected:
            raise ValueError('Meaningful mutation has no selected fixtures')
        row = next(r for r in matches if r['address'] == hex(int(name, 16)))
        negatives.append(mutation(SOURCE / (name + '.c'), label, old, new, row, main, selected))
    write_json(LANE / 'binding-layout-controls.json', controls(matches))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    write_json(LANE / 'match.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='main', program='',
               moduleSha256=info['sha256'], allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches),
               canonicalMatchedBytes=sum(row['bytes'] for row in matches), cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
               nativeCalleeBodiesExecuted=0, calleeSourceCredit=0, externalStorageCredit=0, negativeEvidence=negatives,
               inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
               bindingLayoutControls=dict(path=(LANE / 'binding-layout-controls.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'binding-layout-controls.json')),
               generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)),
               producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)),
               limits=['Eighth closed332-byte rendering caller of98/12440B claim; complete configured extent, ordinary C, pinned SP1 compiler/genuine MW link and original ELF names/relocations; prior four-matrix declaration context gives immediate exact match without allocation sweep or patches.',
                       '32 native/source fixture pairs compare complete GPR/CPSR/calls/writes/8MiB RAM and independent complete96-byte caller state and one256-byte graphics union. Four dirty-byte classes, material extremes and signed angle extremes cover conditional four36-byte stack matrices, six-provider matrix order, dirty clear before copy, flags clear before translation, late state/member reload and nine-command sequence.',
                       'Matrix destination020ee04c equals graphics state020edf90+188. Both original BSS symbols/load records and exact source/copy/flags LDR-BIC-STR words are qualified; one union model prevents double-counted or contradictory overlapping state. Minimum matrix36/graphics-prefix256/caller-prefix88 are views only; complete original allocations/storage definitions/typedefs and valid game domains remain unproved. Source emits no data storage, storage/source credit0.',
                       'Original configured28-byte ARM copy helper is inspected read-only: three12-byte LDM/STM groups establish36-byte transfer width. Native helper execution0 and implementation/source credit0. All matrix/transform/graphics/model bodies are scripted ABI boundaries with prescribed output matrices/copy/state mutations and caller-saved GPR/flags clobbers; no actual matrix, graphics/game/hardware/platform/source-only ROM implementation claim.',
                       'Provider mutations distinguish fresh later angle/material/model reads, preserved original caller pointer, persistent cached model across nine setters, global-mask ordering, post-provider flags persistence and literal success independent of provider results. Original stack offsets0/36/72/108 follow measured local-object declaration order.',
                       'Unchanged common BSS and original branch qualification plus53 data/alias/read-only-helper controls,6 branch controls,4 real native ABI failures and8 genuine wrong-C errors are required. Source-complete copied-root producer and generic canonical replay required; all earlier READY/helper/source/input pins remain unchanged;156or later only.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
