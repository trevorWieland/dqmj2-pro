import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_main_tail_next_eighth_build import build
from wave20261105_main_tail_next_eighth_models import SPECS, fixtures
from wave20261105_main_tail_next_eighth_execution import run
from wave20261105_main_tail_next_eighth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-tail-next/eighth'
WORK = ROOT / 'work/w5tn/eighth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/main-tail-next/eighth'


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
    from wave20261105_main_tail_next_eighth_models import scenario
    cases=[]
    for name in SPECS:
        all_f=fixtures(name)
        valid=[f for f in all_f if f['mode'] in [1,2,3] and f['index'] < (3 if f['mode']==1 else 6)]
        default=0xffffffff if name=='020d3dc0' else 0
        cases.append((name,'wrong-last-index-'+name,'index < 3','index < 2',1,[f for f in valid if f['mode']==1 and f['index']==2 and scenario(name,f,0)['result']!=default]))
        cases.append((name,'wrong-sixth-index-'+name,'index < 6','index < 5',1,[f for f in valid if f['mode']==2 and f['index']==5 and scenario(name,f,0)['result']!=default]))
        cases.append((name,'wrong-mode-three-'+name,'case 3:','case 4:',1,[f for f in valid if f['mode']==3 and scenario(name,f,0)['result']!=default][:8]))
        cast='(u16) ' if name=='020d3dc0' else '(signed char) '
        chosen=[f for f in valid if scenario(name,f,0)['result']&0x80000000] if name=='020d3dc0' else [f for f in valid if scenario(name,f,0)['result']>=128]
        cases.append((name,'wrong-field-signedness-'+name,'result = native_data_','result = '+cast+'native_data_',2,chosen[:8]))
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
        'Three ordinary-C strided record projections totaling288B. Complete code/literal bytes exact through genuine pinned MW compilation/linking with untouched original ELF names/relocations, no patches/ASM/allocation sweep/shared changes.',
        '486 original/source fixture pairs require actual caller returns, full registers/CPSR, all writes and8MiB RAM equality. Modes-1/0/1/2/3/4, every valid3/6-record index and invalid3/6/0xffffffff/0x80000000 boundaries are checked. Signed16 IDs include-32768/-1/0/32767; byte variants/categories include0/127/128/255.',
        'Six exact raw BSS aliases and their original literal/load/field instructions are pinned independently. All read views share one54-byte backing region with guards; data storage authorship, complete original allocations and storage credit remain unknown/zero.',
        'No callee/provider body executes and none gains credit; these callers contain no imports.9 actual compiled native signed16 ABI probe returns plus unsigned rejection,90 data origin/addend/field/identity negatives,3 real layout failures and12 genuine wrong-C controls must pass.',
        'No game/mechanics/hardware/platform semantics or broader safety outside measured mode/index contracts are established. Source-complete original/copied producer and generic canonical original/copied replays required. Pending288B source credit remains0 until serialized coordinator integration.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=3,canonicalMatchedBytes=288,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=3,bytes=288,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
