import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_arm_next_sixth_build import build
from wave20261104_main_arm_next_sixth_models import SPECS, fixtures, run
from wave20261104_main_arm_next_sixth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-arm-next/sixth'
WORK = ROOT / 'work/w4an/sixth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-arm-next/sixth'


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
    for row in matches:
        name = format(int(row['address'], 0), '08x')
        selected = [f for f in fixtures(name) if f['table'] and not f['empty'] and 0 <= f['index'] < f['count']]
        boundary = [f for f in fixtures(name) if f['table'] and not f['empty'] and f['index'] == f['count']]
        original_field = 'table%02x' % SPECS[name]
        wrong_field = 'table0c' if SPECS[name] == 8 else 'table08'
        cases = [('wrong-blob-table-field', original_field, wrong_field, selected),
                 ('wrong-record-relative-base', '(u8 *)base + offset', '(u8 *)table + offset', selected),
                 ('wrong-inclusive-count', '(u32)index >= table->count', '(u32)index > table->count', boundary),
                 ('wrong-optional-table-polarity', '!relative ? 0 :', 'relative ? 0 :', selected)]
        for label, old, new, subset in cases:
            if not subset:
                raise ValueError('Leaf lookup mutation lacks a distinguishing fixture')
            negatives.append(mutation(SOURCE / (name + '.c'), name + '-' + label, old, new, row, main, subset))
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
               limits=['Sixth closed7-function manager/relative-resource-table subset of98/12440B claim; all seven complete100-byte extents, ordinary C, pinned SP1 compiler and genuine MW full links with original ELF relocations/names; no instruction/object/register patches or allocation sweep.',
                       '1008 native/source fixture pairs compare complete GPR/CPSR/instruction path/read-only writes/8MiB RAM and independent complete160-byte manager/8192-byte resource blob/4-byte global state. No native callee/helper executes; no callee/data/source storage credit.',
                       'Each distinct blob table offset8/12/16/20/24/32/36 is independently selected against six populated alternative tables. Optional table/record offsets, counts0/1/4/17, signed index extremes/-1/0/1/3/4/16/17, exact boundary rejection and absolute blob-relative result are tested with complete no-write state.',
                       'Minimum measured pointer width4, manager prefix144 and blob prefix40, count/item width4, item offset4/stride4 are qualified from exact original BSS load, original configured caller/native hash and original LDR/signed guard/unsigned guard/shift/index/base-load words. Complete original object/table/record allocations/typedefs and valid game domains remain unproved; flexible arrays avoid invented fixed table/payload bounds.',
                       'Unchanged frozen common data and branch qualifiers are reused; new lane-local field/width/count/stride witness requires161 meaningful negative controls and four real native ABI layout failures.28 genuine wrong-C table-field/base/count/polarity variants must fail independent distinguishing fixtures; copied-root producer and generic canonical replay required.',
                       'Source null-first resolution and explicit pre-record-test base capture recover measured source-expression control flow, without an allocation search. Frozen first/second7/464B in155 and third/fourth4/824B for156 remain unchanged; this packet belongs156or later. No graphics/game/hardware/platform or source-only ROM proof is claimed.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
