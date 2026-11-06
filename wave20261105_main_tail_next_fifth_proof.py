import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_main_tail_next_fifth_build import build
from wave20261105_main_tail_next_fifth_models import SPECS, fixtures
from wave20261105_main_tail_next_fifth_execution import run
from wave20261105_main_tail_next_fifth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-tail-next/fifth'
WORK = ROOT / 'work/w5tn/fifth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/main-tail-next/fifth'


def mutation(name, label, old, new, count, main, selected):
    source = SOURCE / (name + '.c')
    text = source.read_text()
    if text.count(old) != count or not selected:
        raise ValueError('Bounded whole-C pagination mutation ambiguous/empty: ' + label)
    directory = WORK / label / 'negative'
    directory.mkdir(parents=True, exist_ok=True)
    wrong = directory / 'source.c'
    wrong.write_text(text.replace(old, new))
    shutil.copyfile(SOURCE / 'context.h', directory / 'context.h')
    row, body = build(wrong, directory / 'build', True)
    rejected, aborted = [], []
    for ordinal, fixture in enumerate(selected):
        result = run(row, body, fixture, main, ordinal)
        if result['modelFailures']:
            rejected.append(ordinal)
            if not result['actualTopReturn']:
                aborted.append(ordinal)
    if len(rejected) != len(selected):
        raise ValueError(('Whole-C pagination error not independently rejected', label, rejected, len(selected)))
    return dict(case=label, old=old, new=new, expectedOccurrences=count, rejectedCases=rejected,
                rejectedAtObservedProtocolBoundary=aborted, abortedRunsAreNotCallerReturns=True, fixtures=selected, proof=row)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned private native unit runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen pagination input changed: ' + pin['path'])
    if {format(int(row['address'], 0), '08x') for row in inputs['entries']} != set(SPECS):
        raise ValueError('Exact exclusive pagination caller identities differ')
    info, main, unused = L.measured_module('main')
    rows, traces = [], []
    for item in inputs['entries']:
        name = format(int(item['address'], 0), '08x')
        row, body = build(ROOT / item['source'], WORK / name / 'positive')
        if (row['targetSha256'], row['bytes']) != (item['targetSha256'], item['bytes']):
            raise ValueError('Full native pagination caller target differs')
        start = int(row['address'], 0) - 0x02000000
        native = main[start:start + row['bytes']]
        for ordinal, fixture in enumerate(fixtures(name)):
            original = run(row, native, fixture, main, ordinal)
            rebuilt = run(row, body, fixture, main, ordinal)
            if original != rebuilt or original['modelFailures'] or not original['actualTopReturn']:
                write_json(LANE / 'fixture-failure.json', dict(address=row['address'], fixture=fixture, original=original, rebuilt=rebuilt))
                raise ValueError(('Independent pagination protocol/full state differs', name, ordinal, original['modelFailures']))
            traces.append(dict(address=row['address'], ordinal=ordinal, fixture=fixture, result=original))
        rows.append(row)
        print('proved', row['address'], row['bytes'], len(fixtures(name)), flush=True)
    indicator, count, entry = [fixtures(name) for name in ['020cff18','020d0a24','020d0a74']]
    selected = lambda **fields: [f for f in indicator if all(f[key] == value for key, value in fields.items())][:8]
    selected_entry = lambda **fields: [f for f in entry if all(f[key] == value for key, value in fields.items())][:8]
    cases = [
        ('020cff18','wrong-zero-page-branch','pages != 1','pages > 1',2,selected(count=0,pages=(1,1))),
        ('020cff18','wrong-previous-bound','() > 0','() >= 0',1,selected(count=13,pages=(0,0))),
        ('020cff18','wrong-next-bound','< pages - 1','<= pages - 1',1,selected(count=13,pages=(1,1))),
        ('020cff18','wrong-enable-bit','|= 2','|= 1',2,selected(count=13,pages=(1,1),flags=0)),
        ('020cff18','wrong-disable-bit','&= ~2u','&= ~1u',2,selected(count=12,flags=3)),
        ('020cff18','wrong-widget-subobject',' + 8, 1',' + 4, 1',2,selected(count=13,pages=(1,1))),
        ('020d0a24','wrong-page-divisor',' / 12',' / 11',1,[f for f in count if f['count'] in [12,24,100]]),
        ('020d0a74','wrong-grid-stride','y1 * 4','y1 * 3',1,selected_entry(count=100,x=3,y=2,page=0,side=0,entries=True,mutate=False)),
        ('020d0a74','wrong-count-bound','index < count','index <= count',1,selected_entry(count=12,x=0,y=0,page=1,side=0,entries=True,mutate=False)),
        ('020d0a74','wrong-entry-null-guard','entries == 0','entries != 0',1,selected_entry(count=100,page=0,side=0,entries=True,mutate=False)),
        ('020d0a74','wrong-cursor-lifetime','    s32 index = native_data_021d6b64.x0 + native_data_021d6b64.y1 * 4;\n    s32 count = native_fn_020629e0();','    s32 count = native_fn_020629e0();\n    s32 index = native_data_021d6b64.x0 + native_data_021d6b64.y1 * 4;',1,selected_entry(count=100,page=0,side=1,entries=False,mutate=True))]
    negatives = [mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits = [
        'Three ordinary-C pagination callers totaling340B, complete code/literal bytes exact through genuine pinned MW compilation/linking with original untouched ELF symbols/relocations. No source/object/register/instruction patch, ASM, allocation sweep or shared pipeline change.',
        'Independent original/source caller returns, full GPR/CPSR, ordered callbacks, writes and8MiB RAM equality. Tests cover count0..100, page and null-entry boundaries, both indicators, shared widget pointers, fresh pointers/flags after callbacks and signed cursor coordinates captured before a mutable count provider.',
        'Page-count wrapper includes bounded negative count ABI counterfactuals; the measured roster count is0..100. Entry fixtures keep cursor x0..3 and y0..2 so successful indexing stays within twelve8-byte borrowed entries. All indicator widget pointers are valid minimum128-byte views; no general null-widget or invalid-index safety is claimed.',
        'Adjacent20/8/3-byte BSS ABI views share one backing region; widget flags at124, page-byte1, entries-pointer4 and signed cursor bytes0/1 are independently pinned to actual native instructions/loads/raw inventory. Original complete allocations and data storage authorship remain unproved; storage credit0.',
        'No actual count/page/widget provider body executes or gains source credit. Scripted minimum observed ABI boundaries and caller-saved clobbers only; complete original callee declarations, game/UI/hardware/platform semantics remain unproved. The indicator result is void; all actual machine registers are still compared exactly.',
        'All imported function namespace/mode/address and data origin/addend/layout negatives, real native layout failures,512 compiled signed-cursor ABI returns plus unsigned rejection controls and11 genuine wrong-C controls must reject. Protocol-aborted negative runs are explicit and are not counted as caller returns.',
        'Source-complete original/copied producer plus original/copied generic canonical replay required. Frozen1472-byte renderer and all prior claims/packets remain unchanged. This pending340B packet provides no accepted source credit before serialized coordinator integration.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=3,canonicalMatchedBytes=340,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=3,bytes=340,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
