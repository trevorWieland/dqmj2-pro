import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_second_build import build
from wave20261105_socket_thumb_next_second_models import SPECS, fixtures
from wave20261105_socket_thumb_next_second_execution import run
from wave20261105_socket_thumb_next_second_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/second'
WORK = ROOT / 'work/w5st/second-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/second'


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
    def selected(name,limit=8,**fields):
        return [f for f in fixtures(name) if all(f.get(k)==v for k,v in fields.items())][:limit]
    cases=[
      ('0208d820','wrong-tick-shift','()>>16','()>>15',1,selected('0208d820',outcome='immediate',tick=(65536,1))),
      ('0208d820','wrong-retry-limit','retry<3','retry<2',1,selected('0208d820',outcome='third')),
      ('0208d820','lost-initial-seed','socket->word28=seed;','socket->word28=0x13572468;',1,selected('0208d820',outcome='immediate')),
      ('0208d820','wrong-wait-state','socket->state8==2','socket->state8!=2',1,selected('0208d820',outcome='exhaust')),
      ('0208d968','wrong-wait-kind','socket->kind4=3','socket->kind4=2',1,selected('0208d968',waits=1)),
      ('0208d968','lost-captured-size','*output=size;','*output=socket->word44;',1,selected('0208d968',waits=1,mutate=True,alias=False)),
      ('0208d968','lost-fresh-buffer','return socket->buffer40;','return 0;',1,selected('0208d968',mutate=True)),
      ('0208d9a0','wrong-wait-state-four','socket->state8==4','socket->state8==5',2,selected('0208d9a0',size=0,state=4,waits=1,exitState=False,mutate=False)),
      ('0208d9a0','lost-fresh-size','size=socket->word44;','size=4;',1,selected('0208d9a0',size=4,mutate=True,alias=False)),
      ('0208d9f0','wrong-state-eleven','socket->state8==11','socket->state8==12',1,selected('0208d9f0',present=True,state=11,mode=0)),
      ('0208d9f0','wrong-null-output','*output=0;','*output=1;',1,selected('0208d9f0',present=False)),
      ('0208da30','wrong-full-zero-gate','count!=0','count==0',1,selected('0208da30',size=4,count=0,equal=True,state=4,mutate=False)),
      ('0208da30','wrong-consume-bound','count>=size','count>size',1,selected('0208da30',size=4,count=4,state=4,mutate=False)),
      ('0208da30','wrong-copy-remainder','size-count','size+count',2,selected('0208da30',size=8,count=3,state=4,mutate=False)),
      ('0208da88','wrong-mode-route','if(socket->mode9)','if(!socket->mode9)',1,selected('0208da88',present=True,mode=0))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Six complete ordinary-C main Thumb callers totaling426B genuinely MW-link every full configured native extent and preserve original relocations, BL/BLX interworking and actual target modes. No old normalizer/parser/validator edits, helper aliases, raw patches, ASM or allocation sweep.',
      '778 independent original/source fixture pairs require1556 actual returning callers, full GPR/CPSR, all provider identities/modes/argument words, writes and8MiB RAM equality. Finite0/1/2/3-step scripted progress, state/mode/null routing, wait-vs-yield control, full/partial/zero/all-ones consumption counts, overlapping bounded copy behavior and valid same-word output aliases are covered.',
      'The108B retry caller samples one two-word unsigned64 return and shifts it16 bits, tries at most3 iterations, caches its initial seed and IRQ mask, and rechecks state/network-address fields after provider boundaries. Immediate/second/third success, exhaustion, inactive address and restore-time address changes are distinct fixtures.',
      '54B wait variant captures available length before IRQ restore but returns a freshly read buffer pointer;78B variant reads both after restore/yield. Mutable provider schedules independently distinguish these boundaries. Readiness loops are only proven for explicitly bounded progress schedules, not arbitrary non-progress or physical thread/network termination.',
      'Borrowed views are Socket100 with capacity3C/buffer40/size44/tick10/word28, thread168, singleton8, address84,32-byte buffers and one valid word output; aliases point only to the compatible size44 word. Names and complete original allocations remain unproved, with0 data/storage credit.',
      'Providers may mutate buffers, size/state/capacity/owner/thread selection and return full32/64-bit ABI words. Actual original provider bodies execute0 and get0 source credit; original complete C declarations/game/hardware/socket semantics and platform execution remain unproved.',
      'All original namespace/mode/origin/instruction/addend negatives,5 real Thumb compiler layout failures,275 actual compiled byte/halfword/two-word/tick ABI returns plus4 signed/order/shift rejection controls, and15 genuinely linked wrong-C errors must reject. Protocol-aborted negative runs never count as caller returns.',
      'Complete private source/runtime inputs, original/copied producers and generic canonical original/copied replay are required before READY; pending426B source credit remains0 until serialized acceptance. All frozen first428B/main-tail/v13 inputs remain unchanged.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=6,canonicalMatchedBytes=426,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=6,bytes=426,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
