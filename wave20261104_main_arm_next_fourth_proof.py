import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_arm_next_fourth_build import build
from wave20261104_main_arm_next_fourth_models import SPECS, fixtures, run
from wave20261104_main_arm_next_fourth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-arm-next/fourth'
WORK = ROOT / 'work/w4an/fourth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-arm-next/fourth'


def mutation(source, name, old, new, row, main, selected):
    text = source.read_text()
    if text.count(old) != (2 if name in ['wrong-owner-reload', 'wrong-auxiliary-commit-field'] else 1):
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
    bound = [f for f in fixtures('02028a4c') if f['signature'] == 0x30585442 and f['owner'] and f['parsed']]
    cleanup = fixtures('02028af4')
    flag1 = [f for f in cleanup if f['flags'] == 1]
    flag2 = [f for f in cleanup if f['flags'] == 2]
    cases = [('02028a4c', 'wrong-signature-family', '0x30585442', '0x30444d42', bound),
             ('02028a4c', 'wrong-parser-mode', 'if (mode)', 'if (!mode)', bound),
             ('02028a4c', 'wrong-owner-reload', 'native_fn_0202bedc(output->resource)', 'native_fn_0202bedc(resource)', bound),
             ('02028a4c', 'wrong-auxiliary-commit-field', 'output->auxiliary08 = resource;', 'output->resource = resource;', bound),
             ('02028af4', 'wrong-primary-status-bit', 'output->field38 & 1', 'output->field38 & 4', flag1),
             ('02028af4', 'wrong-secondary-result-bit', 'result |= 2;', 'result |= 4;', flag2),
             ('02028af4', 'wrong-animation-count-guard', 'if (output->animationCount0f)', 'if (!output->animationCount0f)', flag2),
             ('02028af4', 'wrong-final-status-clear', 'output->field38 = 0;', 'output->field38 = 1;', cleanup)]
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
               limits=['Fourth closed2-function resource caller subset of98/12440B claim; complete168/112-byte configured extents, ordinary C, pinned SP1 compiler and genuine MW full links; no instruction/object/register patches or allocation sweep.',
                       '287 native/source fixture pairs compare complete GPR/CPSR/calls/writes/8MiB RAM and independent complete96-byte context/32-byte resource models. All256 status-byte values plus16 pointer/count/callback combinations are covered; minimum actual context view88 and byte count15/embedded region16 are measured offsets, with complete original allocations/typedefs unproved.',
                       'BTX signature/current-resource guards, nonzero parser mode/result, two-argument parser boundary, texture pointer lifetime, post-query owner pointer reload, null model/texture forwarding, auxiliary pointer commit after binding and literal result normalization are caller-level checks.',
                       'Cleanup checks primary/secondary status bits, null resource guards, fresh secondary flag/auxiliary/count reload after callbacks, exact embedded animation address16, persistent provider mutations and unconditional final status clear. Result records tested status branches independently of actual release calls.',
                       'All native parser/query/binder/release/animation bodies are modeled ABI boundaries with prescribed returns/state mutations and caller-saved GPR/flags clobbers. Actual native callee execution/source/storage credit0; no parser, graphics/game/hardware or platform implementation claims.',
                       'Unchanged frozen original branch verifier supplies exact CPU/program/module/address/name/mode/original-relocation qualification.12 callee controls,4 real ABI layout failures and8 genuine whole-C errors are required; copied-root producer and generic canonical replay must pass. No new data or function-pointer exception applies to this packet.',
                       'Adjacent224/168-byte dictionary callers remain partial/uncredited after bounded typed-context and control-flow assessment; unsupported inline syntax was discarded before sealing. First7/464B in155 and third2/544B for156 remain immutable; current packet belongs156or later.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
