import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261104_main_middle_fifth_build import build
from wave20261104_main_middle_fifth_models import SPECS, fixtures, run
from wave20261104_main_middle_fifth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-middle/fifth'
WORK = ROOT / 'work/w4mm/fifth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-command-middle/eighth'


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
    mutations = {'02049af0': ('return arguments.output;', 'return arguments.input;', fixtures('02049af0')),
                 '02049be4': ('entry->field5 = (s8)field5;', 'entry->field5 = (s8)field4;', [f for f in fixtures('02049be4') if f['present']])}
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
    source = SOURCE / '02049af0.c'
    text = source.read_text().replace('    u32 previous = native_fn_02048f7c(1);', '    u32 previous = native_fn_02048f7c(1);\n    u32 cached;')
    text = text.replace('    if (arguments.enabled) {', '    cached = arguments.output;\n    if (arguments.enabled) {').replace('return arguments.output;', 'return cached;')
    folder = WORK / 'cached-output/negative'
    folder.mkdir(parents=True, exist_ok=True)
    wrong = folder / 'source.c'
    wrong.write_text(text)
    shutil.copyfile(SOURCE / 'context.h', folder / 'context.h')
    badrow, body = build(wrong, folder / 'build', True)
    selected = [f for f in fixtures('02049af0') if f['enabled']]
    rejected = [i for i, f in enumerate(selected) if run(badrow, body, f, main, i)['modelFailures']]
    if len(rejected) != len(selected): raise ValueError('Cached-before-controller output word was not rejected')
    negatives.append(dict(case='cached-before-controller-output', rejectedCases=rejected, fixtures=selected, proof=badrow))
    source = SOURCE / '02049be4.c'
    selected = [f for f in fixtures('02049be4') if f['present']]
    negatives.append(mutation(source, 'signed-instead-of-unsigned-table-byte', 'native_data_021029c8[font]', '(s8)native_data_021029c8[font]', matches[1], main, selected))
    text = source.read_text().replace('    entry->field6 = link->first;\n', '')
    text = text.replace('    entry->link = link;', '    entry->field6 = link->first;\n    entry->link = link;')
    folder = WORK / 'late-entry-byte/negative'
    folder.mkdir(parents=True, exist_ok=True)
    wrong = folder / 'source.c'
    wrong.write_text(text)
    shutil.copyfile(SOURCE / 'context.h', folder / 'context.h')
    badrow, body = build(wrong, folder / 'build', True)
    rejected = [i for i, f in enumerate(selected) if run(badrow, body, f, main, i)['modelFailures']]
    if len(rejected) != len(selected): raise ValueError('Wrong post-provider entry-byte store was not rejected')
    negatives.append(dict(case='entry-byte-store-after-provider', rejectedCases=rejected, fixtures=selected, proof=badrow))
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
               limits=['Fifth disjoint2-function aggregate/eleven-argument family from67-function claim; full configured148/172-byte extents, pinned SP1 compiler and genuine MW links, original ELF names/relocations intact.',
                       'Eight finite fixtures per function with actual native/source returns, complete GPR/CPSR/calls/writes/8MiB RAM equality and independent complete escaped aggregate/entry/link/table models.',
                       'The16-byte word block is a measured by-value ABI view straddlingR3 and incoming stack words; its exact genuine address, initial contents and callback changes before flag tests and the final return are checked. Original complete source declaration remains unproved.',
                       'Eleven-argument fixtures check four unsigned stack bytes, two full words and one signed stack byte, low-byte signed lookup conversion, late unsigned BSS table reads, pre-provider entry+6 snapshot and post-provider pointer/field overwrites.',
                       'Two original BSS bases and full-word-index LDRB instructions are qualified; arrays are incomplete source views with unknown actual extents and zero storage credit. Non-NULL lookup fixtures use synthetic indices0..7; high/out-of-byte-range font words take the NULL lookup path. Shift fixtures stay in0..5; original valid game domains and actual complete object/source prototypes remain unproved.',
                       'All native providers are opaque modeled boundaries with prescribed return words, escaped-stack/entry/link/table effects and caller-saved-register/flag clobbers; native callee execution/source credit0, with no actual text/window/font/game execution claimed.',
                       'Frozen common data qualification and original branch verifier remain unchanged. Whole-C wrong output/entry field/signed table/cache/store-order controls, typed ABI failures and copied-root replay remain explicit; shared integration, hardware and source-only ROM proof remain outside this packet.']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches), cases=len(traces)), flush=True)


if __name__ == '__main__':
    execute()
