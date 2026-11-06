import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_arm_next_seventh_build import build
from wave20261104_main_arm_next_seventh_models import SPECS, fixtures, run
from wave20261104_main_arm_next_seventh_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-arm-next/seventh'
WORK = ROOT / 'work/w4an/seventh-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-arm-next/seventh'


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
    first = [f for f in fixtures('02039ab0') if f['lookup']]
    second = [f for f in fixtures('02039b20') if not f['failed']]
    cases = [('02039ab0', 'wrong-explicit-zero-default', 'if (field8 < 0)', 'if (field8 <= 0)', [f for f in first if f['fields'][2] == 0]),
             ('02039ab0', 'wrong-halfword-sign', 'field4 = record->field4;', 'field4 = (signed short)record->field4;', [f for f in first if f['fields'][1] < 0 and f['ordinal'] % 4 in [1, 2]]),
             ('02039ab0', 'wrong-byte-sign', 'field9 = record->field9;', 'field9 = (signed char)record->field9;', [f for f in first if f['fields'][0] < 0]),
             ('02039ab0', 'wrong-sixth-stack-argument', 'record, index);', 'record, index + 1);', first),
             ('02039b20', 'wrong-resource-id', 'native_fn_0203917c(*info)', 'native_fn_0203917c(*info + 1)', second),
             ('02039b20', 'wrong-record-byte-pair', 'record->field9, record->field4, record->field8', 'record->field8, record->field4, record->field9', second),
             ('02039b20', 'wrong-eighth-stack-argument', 'archive, index, subindex);', 'archive, subindex, index);', [f for f in second if f['index'] != f['subindex']]),
             ('02039b20', 'wrong-forwarded-return', 'return native_fn_02039c9c(', 'return !native_fn_02039c9c(', second)]
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
               limits=['Seventh closed2-function record-caller subset of98/12440B claim; complete112/128-byte extents, ordinary C, pinned SP1 compiler and genuine MW full links with original ELF relocations/names; no allocation sweep or patches.',
                       '164 native/source fixture pairs compare complete GPR/CPSR/calls/writes/8MiB RAM and independent complete output/info/record models.128 cases cover lookup/null with all64 combinations of signed negative/minimum/zero/maximum overrides;36 cases cover independent index/subindex extremes and each of three nullable providers.',
                       'Six-argument boundary preserves original fifth input index, caller overrides or zero-extended unsigned byte8/9 and halfword4 defaults, and two native stack words at originalSPminus32. Eight-argument boundary preserves record/archive/original index/subindex as four stack words at originalSPminus40, validates nested resource ID resolution and propagates arbitrary32-bit provider result.',
                       'Providers explicitly mutate info/record/output, supply0/1/high-bit/all-ones results and clobber caller-saved GPR/flags. All native lookup/archive/record/action bodies remain modeled boundaries and execute0; their source/storage credit0, even when a lookup is separately reconstructed in the sixth packet.',
                       'Measured record accesses require minimum10 bytes with unsigned widths2/1/1 at4/8/9; source view padding and complete original declarations/object allocations/valid domains remain unproved. No original data/storage credit and no parser/sound/game/hardware/platform/source-only ROM proof is claimed.',
                       'Unchanged original branch verifier,12 namespace/name/address/mode controls,4 real native layout failures,8 genuine wrong-C signedness/default/index/ID/order/result errors and source-complete copied-root/generic canonical replay are required. Frozen first/second7/464B in155 and third/fourth/sixth11/1524B for156 remain unchanged; current packet belongs156or later.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
