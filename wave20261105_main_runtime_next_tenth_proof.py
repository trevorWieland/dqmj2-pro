import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_main_runtime_next_tenth_build import build
from wave20261105_main_runtime_next_tenth_models import SPECS, fixtures, run
from wave20261105_main_runtime_next_tenth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-runtime-next/tenth'
WORK = ROOT / 'work/w5rn/tenth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/main-runtime-next/tenth'


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
    cast = fixtures('02060adc')
    first = fixtures('02060c1c')
    square = fixtures('02060c60')
    second = fixtures('02060cb4')
    alloc = fixtures('02067754')
    cases = [('02060adc', 'wrong-byte-projection', 'return (s8)value;', 'return (s8)(value >> 8);', [x for x in cast if x['value'] & 255 != (x['value'] >> 8) & 255]),
             ('02060adc', 'wrong-signed-byte-result', 's8 native_main_', 'u8 native_main_', [x for x in cast if x['value'] & 255 >= 128]),
             ('02060c1c', 'wrong-zero-kind-guard', 'if (kind != 0)', 'if (kind == 0)', first),
             ('02060c60', 'wrong-equal-zero-priority', 'if (kindY == selectedY)', 'if (kindY == selectedY && kindY != 0)', [x for x in square if x['y'] == 0 and x['sy'] == 0]),
             ('02060cb4', 'wrong-alternate-stride', 'if (alternate) result += 3;', 'if (alternate) result += 2;', [x for x in second if x['alternate']]),
             ('02067754', 'wrong-allocation-count', 'i < 9', 'i < 8', alloc),
             ('02067754', 'wrong-primary-request-size', '7, 0x1100, 4', '7, 0x1000, 4', alloc),
             ('02067754', 'wrong-primary-alignment', '7, 0x1100, 4', '7, 0x1100, 8', alloc),
             ('02067754', 'wrong-primary-store-field', '.primary8 =', '.tail1C =', alloc)]
    negatives = [mutation(SOURCE / (name + '.c'), label, old, new, main, selected) for name, label, old, new, selected in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(matches))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits = ['Fourth closed5/348-byte integer/allocation packet from57/12340B main-runtime-next claim. Each full configured extent has readable ordinary C and a genuine pinned MW link preserving original ELF symbols/relocations; no patches, ordinary-logic ASM, allocator search or shared verifier change.',
              'The byte projection checks all256 low-byte patterns with three representative upper-word patterns, including high-bit/all-ones inputs and negative signed-byte returns. Three classification routines preserve zero-kind guards, alternate nonzero behavior, equal-vs-zero priority and signed-byte intermediate conversions. These pure callers map only code, stack and stop pages; all mapped RAM, full GPR/CPSR and actual caller returns are compared. No exhaustive claim is made for all2^32 input words.',
              'The allocation caller requests11 independently modeled blocks: tag7/alignment4 with one0x1100 request, nine0x5c0 requests and one0x440 request. Nullable returns, distinct pointer words, provider mutation of all context/array/padding bytes and caller-saved clobbers are exercised. Every ordered pointer store is checked independently so later provider mutations cannot conceal a missing/misdirected earlier store.',
              'No actual allocation/SDK/game provider body executes or receives credit. Returned pointers are scripted ABI values; actual heap allocation, ownership, lifetime and storage extents remain unproved. The two BSS views cover only pointer fields at8/28 and a nine-pointer36-byte array; original complete extents and external storage credit remain unknown/zero.',
              'The unchanged original branch/data qualifiers plus frozen caller hashes, ABS32 origin/addend, raw inventory/load records and exact field/store words are required.30 meaningful data negatives,6 all-import namespace/mode/address controls,3 real native layout failures and9 genuine whole-C errors must reject. Source-complete original/copied producer and generic canonical original/copied replay are required.',
              'Only the allocation loop uses measured SP1p5 O4,p/on,noauto/file-IPA/C99; the four pure integer callers use pinned SP1p5 O2/speed/inline-on. All old packets remain immutable. Caller fixture/ABI evidence does not establish game/hardware/platform/source-only ROM execution or accepted credit before serialized coordinator publication.']
    write_json(LANE / 'match.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='main', program='', moduleSha256=info['sha256'],
               allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches), canonicalMatchedBytes=sum(x['bytes'] for x in matches), cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces),
               nativeCalleeBodiesExecuted=0, calleeSourceCredit=0, externalStorageCredit=0, negativeEvidence=negatives,
               inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')),
               bindingLayoutControls=dict(path=(LANE / 'binding-layout-controls.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'binding-layout-controls.json')),
               generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=C.sha(raw)), producer=Path(__file__).name, producerSha256=sha256(Path(__file__)), limits=limits))
    print(dict(functions=len(matches), bytes=sum(x['bytes'] for x in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
