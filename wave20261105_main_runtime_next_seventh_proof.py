import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_main_runtime_next_seventh_build import build
from wave20261105_main_runtime_next_seventh_models import SPECS, fixtures, run
from wave20261105_main_runtime_next_seventh_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-runtime-next/seventh'
WORK = ROOT / 'work/w5rn/seventh-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/main-runtime-next/seventh'


def mutation(source, label, old, new, main, selected):
    text = source.read_text()
    if text.count(old) != 1 or not selected:
        raise ValueError('Meaningful whole-C collection mutation is ambiguous/empty: ' + label)
    directory = WORK / label / 'negative'
    directory.mkdir(parents=True, exist_ok=True)
    wrong = directory / 'source.c'
    wrong.write_text(text.replace(old, new))
    shutil.copyfile(SOURCE / 'context.h', directory / 'context.h')
    row, body = build(wrong, directory / 'build', True)
    rejected = []
    for ordinal, fixture in enumerate(selected):
        if run(row, body, fixture, main, ordinal)['modelFailures']:
            rejected.append(ordinal)
    if len(rejected) != len(selected):
        raise ValueError(('Wrong collection C not independently rejected', label, rejected, len(selected)))
    return dict(case=label, old=old, new=new, rejectedCases=rejected, fixtures=selected, proof=row)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned native unit runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen collection input changed: ' + pin['path'])
    if {format(int(x['address'], 0), '08x') for x in inputs['entries']} != set(SPECS):
        raise ValueError('Frozen collection caller set differs')
    info, main, unused = L.measured_module('main')
    matches, traces = [], []
    for item in inputs['entries']:
        name = format(int(item['address'], 0), '08x')
        row, body = build(ROOT / item['source'], WORK / name / 'positive')
        if (row['targetSha256'], row['bytes']) != (item['targetSha256'], item['bytes']):
            raise ValueError('Frozen full native collection extent differs')
        start = int(row['address'], 0) - 0x02000000
        native = main[start:start + row['bytes']]
        for ordinal, fixture in enumerate(fixtures(name)):
            original = run(row, native, fixture, main, ordinal)
            rebuilt = run(row, body, fixture, main, ordinal)
            if original != rebuilt or original['modelFailures']:
                write_json(LANE / 'fixture-failure.json', dict(address=row['address'], fixture=fixture, original=original, rebuilt=rebuilt))
                raise ValueError(('Independent collection/classification full state differs', name, ordinal, original['modelFailures']))
            traces.append(dict(address=row['address'], ordinal=ordinal, fixture=fixture, result=original))
        matches.append(row)
        print('proved', name, row['bytes'], len(fixtures(name)), flush=True)
    classifications, counts = fixtures('02060b84'), fixtures('020640f0')
    cases = [('02060b84', 'wrong-zero-kind-code', 'alternate == 0 ? 4 : 7', 'alternate == 0 ? 5 : 7', [x for x in classifications if x['kind'] == 0 and x['alternate'] == 0]),
             ('02060b84', 'wrong-kind-boundary', 'if (kind <= 2)', 'if (kind < 2)', [x for x in classifications if x['kind'] == 2 and x['selected'] != 2]),
             ('02060b84', 'wrong-selected-kind-code', 'alternate == 0 ? 6 : 9', 'alternate == 0 ? 5 : 8', [x for x in classifications if x['kind'] > 2 and x['kind'] == x['selected']]),
             ('020640f0', 'wrong-nonzero-include', 'if (includeSecondary)', 'if (includeSecondary == 1)', [x for x in counts if x['include'] in [2, 0xffffffff]]),
             ('020640f0', 'wrong-count-zero-category', 'for (i = 1; i < 9;', 'for (i = 0; i < 9;', [x for x in counts if x['categories'] == [0, 0, 1, 2, 3, 4]]),
             ('020640f0', 'wrong-duplicate-threshold', 'counts[i] > 1', 'counts[i] > 2', [x for x in counts if x['categories'] == [1, 1, 2, 3, 4, 5]]),
             ('020640f0', 'wrong-clear-count', '0, sizeof(counts)', '0, sizeof(counts) - 1', counts[:8]),
             ('02064304', 'wrong-first-pair', 'points14[0] = points[0]', 'points14[0] = points[1]', fixtures('02064304')),
             ('020656f0', 'wrong-record-count', 'i < 36', 'i < 35', fixtures('020656f0')),
             ('020656f0', 'wrong-record-field', 'record->active2 = 0;', 'record->opaque1 = 0;', fixtures('020656f0'))]
    negatives = [mutation(SOURCE / (name + '.c'), label, old, new, main, selected) for name, label, old, new, selected in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(matches))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits = ['Third closed4/464-byte collection/classification packet from57/12340B main-runtime-next claim. Each full configured extent has readable ordinary C, untouched original ELF relocations/names and genuine pinned MW caller link. No instruction/object/binary patch, ordinary-logic ASM or allocation sweep.',
              'Unsigned classification covers kind0/1/2/other/high-bit/all-ones, alternate0/nonzero/high-bit and selected equal/different. Duplicate detection tests3/6 party IDs, nonzero include values, ignored category0, category8 and single/duplicate banks. Only valid modeled category returns0..8 are supplied; invalid indexes are not an allocation/bounds proof.',
              'SDK fill and category providers are independent scripted boundaries; category callbacks optionally mutate all six party IDs and clobber caller-saved words/flags. Exact9-byte stack fill, fresh ID reads, provider order, output result and complete context padding/mutations are checked. No actual SDK/game callee executes or receives source credit.',
              'Three Vec2 pairs are read and written in pair order. Separate/same/shifted overlapping-RAM ABI probes compare independent stepwise copies; shifted cases are counterfactual machine-memory probes, not original C object/allocation ownership or complete extent claims. The reset updates exactly36 byte-ordinal/byte-active fields at stride9 and its separate flag, preserving every neighboring/padding byte.',
              'BSS inputs use the unchanged original data and branch verifiers, additionally pinning exact whole original callers, ABS32 origins/addends, raw storage/load records, field/stride words and minimal ABI prefixes. The party52-byte, point32-byte, flag1-byte and record324-byte views have unknown original complete extents and zero external storage credit.',
              'Four real native-layout rejection controls,60 original-data negative controls, exact function CPU/program/module/mode/address controls,10 genuine wrong-C errors, source-complete original/copied producer and canonical replay are required. The party loop uses a measured SDK O4,p/on,noauto/file-IPA/C99 profile; the other three use pinned SP1p5 O2/speed/inline-on.',
              'All prior sealed packets remain frozen. Native ABI/fixture results do not establish full game/hardware/platform/source-only ROM execution. This packet is157or later, pending serialized coordinator acceptance.']
    write_json(LANE / 'match.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='main', program='', moduleSha256=info['sha256'],
               allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches), canonicalMatchedBytes=sum(x['bytes'] for x in matches), cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
               nativeCalleeBodiesExecuted=0, calleeSourceCredit=0, externalStorageCredit=0, negativeEvidence=negatives,
               inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
               bindingLayoutControls=dict(path=(LANE / 'binding-layout-controls.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'binding-layout-controls.json')),
               generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)), producer=Path(__file__).name, producerSha256=sha256(Path(__file__)), limits=limits))
    print(dict(functions=len(matches), bytes=sum(x['bytes'] for x in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
