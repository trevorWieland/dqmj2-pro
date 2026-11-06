import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_middle_build import build
from wave20261104_main_middle_third_models import SPECS, fixtures, run
from wave20261104_main_middle_third_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-middle/third'
WORK = ROOT / 'work/w4mm/third-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-command-middle/fourth'


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
    mutations = {'0204b380': ('object->field7c |= 2;', 'object->field7c |= 4;', [fixtures('0204b380')[1]]),
                 '0204b4f4': ('state, 0, point, argument3', 'state, 1, point, argument3', [fixtures('0204b4f4')[0]]),
                 '0204b5b0': ('state->step = step;', 'state->step = step ^ 1u;', fixtures('0204b5b0')),
                 '0204b74c': ('state->step = step;', 'state->step = step ^ 1u;', fixtures('0204b74c')),
                 '0204b82c': ('native_fn_0202a498(2,', 'native_fn_0202a498(3,', [fixtures('0204b82c')[1]])}
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
        old, new, selected = mutations[name]
        negatives.append(mutation(source, name, old, new, row, main, selected))
        matches.append(row)
        print('proved', name, row['bytes'], len(fixtures(name)), flush=True)
    source = SOURCE / '0204b380.c'
    old = '    if (enabled) {\n        if (!native_fn_0204b4b8(state)) return;\n        last->field7c |= 2;'
    new = '    if (enabled) {\n        u32 flags = last->field7c;\n        if (!native_fn_0204b4b8(state)) return;\n        last->field7c = flags | 2;'
    negatives.append(mutation(source, 'cached-pre-predicate-child-word', old, new, matches[0], main, [fixtures('0204b380')[2]]))
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
               limits=['Third disjoint5-function pointer-field/stack-wrapper family from67-function claim; full configured extents, pinned SP1 compiler and genuine MW links; original ELF names/relocations preserved.',
                       'Eight finite fixtures per function with actual native/source caller returns and complete GPR/CPSR/calls/writes/8MiB RAM equality; independent complete state, point, child and pointer-table memory models.',
                       'Modeled providers mutate group pointers, child words before predicate return, state/point fields, stack-local points and selected table entries; six-argument forwarding, unsigned-byte stack extraction, signed-halfword snapshots, post-callback overwrites and conditional bit1 updates remain explicit.',
                       'All native providers are modeled boundaries with prescribed returns and caller-saved-register/flag clobbers; zero native callee body execution or source credit. The model performs no real allocation/free, drawing or game execution.',
                       'Measured minimum source views are48-byte state,4-byte signed-halfword pair and child word+0x7c; native compiler assertions and changed-width/sign/offset controls qualify them. Actual object allocations, valid game index domains and semantic meanings remain unproved; external declarations are measured caller register/stack views, while original full source prototypes and return declarations remain unproved; no global data storage credit.',
                       'Two adjacent placement routines remain unmatched and uncredited; wrappers model their call boundaries. Meaningful original-relocation namespace and whole-C flag/stack/step/tag/cached-word controls and copied-root reconstruction remain explicit.',
                       'All earlier READY/helper/input/source paths remain frozen; shared integration, actual game/hardware execution and source-only ROM proof remain outside this packet.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
