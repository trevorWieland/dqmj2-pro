import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_arm_next_third_build import build
from wave20261104_main_arm_next_third_models import SPECS, fixtures, run
from wave20261104_main_arm_next_third_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-arm-next/third'
WORK = ROOT / 'work/w4an/third-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-arm-next/third'


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
    narrow = [f for f in fixtures('020289cc') if f['signature'] == 0x30444d42 and f['parsed']]
    constructors = fixtures('0202882c')
    palette = [f for f in constructors if f['signature'] in [0x30444d42, 0x30585442] and f['texture'] and f['sizes'][2]]
    model_missing = [f for f in constructors if f['signature'] == 0x30444d42 and f['texture'] and not f['model'] and not f['failed']]
    key_pairs = [f for f in constructors if f['signature'] in [0x30444d42, 0x30585442] and f['texture'] and not f['failed'] and f['sizes'][0] and f['sizes'][1]]
    cases = [('020289cc', 'wrong-parser-mode', 'if (mode)', 'if (!mode)', narrow),
             ('020289cc', 'wrong-query-normalization', 'native_fn_0202beec(resource) != 0', 'native_fn_0202beec(resource) == 0', narrow),
             ('020289cc', 'wrong-post-query-status-bit', 'output->field38 |= 1;', 'output->field38 &= 1;', narrow),
             ('0202882c', 'wrong-palette-flag-width', 'texture->flags20 & 0x8000', 'texture->flags20 != 0', palette),
             ('0202882c', 'wrong-missing-model-result', 'else result = 0;', 'else result = 1;', model_missing),
             ('0202882c', 'wrong-auxiliary-key-pair', 'output->key44 = key1;', 'output->key44 = key0;', key_pairs),
             ('0202882c', 'wrong-size-clear', 'output->field4c = output->field50 = output->field54 = 0;', 'output->field4c = output->field50 = output->field54 = 1;', constructors)]
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
               limits=['Third closed2-function resource caller subset of98/12440B claim; complete128/416-byte configured extents, pinned SP1 compiler and genuine MW full links; ordinary C, no instruction/object/register patches or allocation sweep.',
                       '45 native/source fixture pairs compare complete GPR/CPSR/calls/writes/8MiB RAM and independent complete96-byte context,32-byte resource,64-byte texture and4-byte callable-slot models. Minimum actual context view88 and texture flag prefix34; complete original object allocations/types/valid domains remain unknown.',
                       'Invalid signatures, BTX0/BMD0 selector, null texture, all allocation failure masks/zero sizes/high-bit sizes, parser mode/nonzero returns, pointer commit before query, post-provider status reload, raw palette flag, persistent resource signature capture, callback slot reassignment/reload, no partial key commit, and missing model after commit are caller-level checks.',
                       'Native resource/SDK/default allocator bodies do not execute and receive zero source credit. Providers prescribe pointer/size/key results and mutate signature/status/flags/slot while clobbering caller-saved registers/flags. This does not prove SDK parser, texture, allocator, graphics/game/hardware or current native Windows/Android execution.',
                       'Only two exact original initialized data(any) callable slots are qualified by original inventory, pool load, initializer load, actual initialized word, complete configured default ARM function identity/hash and original LDR/dereference/BLX sites. Observed call shape is three32-bit arguments/result; arbitrary runtime replacement modes/ABI and full original typedefs remain unproved. Data/default-callee source/storage credit is zero.',
                       'Frozen original direct-branch and common data verifiers remain unchanged; a new narrow callable-slot witness handles exactly the two measured data(any) globals.60 data/default controls,6 branch controls,4 real native layout failures and7 genuine whole-C errors are required, along with source-complete copied-root producer and generic canonical replay.',
                       'Captured resource signature is read after all three size clears. Key/size stores are paired in native order and local declarations recover measured scalar stack lifetime. BTX/BMD field meanings are tentative caller-level interpretations. Frozen first/second7/464B in155 are unchanged; current packet belongs156or later.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
