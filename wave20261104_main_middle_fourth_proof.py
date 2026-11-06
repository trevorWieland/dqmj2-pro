import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_middle_fourth_build import build
from wave20261104_main_middle_fourth_models import SPECS, fixtures, run
from wave20261104_main_middle_fourth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-middle/fourth'
WORK = ROOT / 'work/w4mm/fourth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-command-middle/seventh'


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
    mutations = {name: ('return value;', 'return (void *)1;', [fixtures(name)[1]]) for name in SPECS if name != '0204983c'}
    mutations['0204983c'] = ('entry->field4 == first', 'entry->field4 != first', [f for i, f in enumerate(fixtures('0204983c')) if i != 4])
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
        if name == '0204983c':
            negatives[-1]['nonDistinguishingPositiveFixture'] = dict(ordinal=4, reason='Both comparisons produce no handler: the only matching second-field entry has a NULL resource. All8 positive fixtures remain required.')
        matches.append(row)
        print('proved', name, row['bytes'], len(fixtures(name)), flush=True)
    source = SOURCE / '02048d14.c'
    old = '    if (value) {'
    text = source.read_text()
    changed = text.replace(old, '    int cached = native_data_02102970;\n' + old).replace('native_fn_0204532c(native_data_02102970, value);', 'native_fn_0204532c(cached, value);')
    folder = WORK / 'cached-tag/negative'
    folder.mkdir(parents=True, exist_ok=True)
    wrong = folder / 'source.c'
    wrong.write_text(changed)
    shutil.copyfile(SOURCE / 'context.h', folder / 'context.h')
    badrow, body = build(wrong, folder / 'build', True)
    selected = fixtures('02048d14')[3:]
    rejected = [i for i, f in enumerate(selected) if run(badrow, body, f, main, i)['modelFailures']]
    if len(rejected) != len(selected): raise ValueError('Pre-predicate cached byte was not rejected')
    negatives.append(dict(case='cached-before-predicate-global-byte', rejectedCases=rejected, fixtures=selected, proof=badrow))
    negatives.append(mutation(source, 'unsigned-global-byte-instead-of-signed', 'native_fn_0204532c(native_data_02102970, value);',
                              'native_fn_0204532c((u8)native_data_02102970, value);', matches[0], main, fixtures('02048d14')[6:]))
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
               limits=['Fourth disjoint5-function signed-byte/guarded-pointer family from67-function claim; full configured extents, pinned SP1 compiler, genuine MW links and original ELF/relocations intact.',
                       'Eight finite fixtures per caller, actual native/source returns and complete GPR/CPSR/calls/writes/8MiB RAM equality. Guarded callers cover NULL, nonzero predicate results, preserved input pointer, all signed-byte boundaries and callback changes before the late byte reload.',
                       'Entry filter checks36 sequential indices, null link/resource gates, signed fields+4/+5 including out-of-byte-range comparison words, and a prescribed handler changing the next entry. No native getter/handler bodies execute.',
                       'Original configured BSS02102970 load records and late LDRSB are independently qualified. Only a one-byte minimal view is claimed; original complete allocation/storage credit0. Entry/link8-byte types are minimum aligned caller views, with full real source types/object extents and original function declarations unproved.',
                       'Native providers are opaque modeled boundaries with prescribed return words, object/global/entry effects and caller-saved-register/flag clobbers; actual native callee execution/source credit0 and no real allocation/free or game behavior is claimed.',
                       'Frozen common data qualification and original branch verifier are unchanged. Strict signed-byte/literal/base/addend/extent/namespace controls, signed-byte/offset ABI controls and whole-C pointer-return/signedness/predicate-cache/filter controls remain explicit.',
                       'All older READY/helper/input/source paths remain frozen; shared module acceptance, hardware and source-only ROM proof remain outside this packet.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
