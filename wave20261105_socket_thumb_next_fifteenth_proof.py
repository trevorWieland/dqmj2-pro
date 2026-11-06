import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_fifteenth_build import build
from wave20261105_socket_thumb_next_fifteenth_models import SPECS, fixtures, scenario
from wave20261105_socket_thumb_next_fifteenth_execution import run
from wave20261105_socket_thumb_next_fifteenth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/fifteenth'
WORK = ROOT / 'work/w5st/fifteenth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/fifteenth'


def mutation(name, label, old, new, count, main, selected):
    source = SOURCE / (name + '.c')
    text = source.read_text()
    header=(SOURCE/'context.h').read_text()
    target='source' if text.count(old)==count else 'header' if header.count(old)==count else None
    if target is None or not selected:raise ValueError('Bounded whole-C/header mutation ambiguous/empty: '+label)
    directory = WORK / label / 'negative'
    directory.mkdir(parents=True, exist_ok=True)
    wrong = directory / 'source.c'
    wrong.write_text(text.replace(old,new) if target=='source' else text)
    (directory/'context.h').write_text(header.replace(old,new) if target=='header' else header)
    row, body = build(wrong, directory / 'build', True)
    rejected, aborted = [], []
    for ordinal, fixture in enumerate(selected):
        result = run(row, body, fixture, main, ordinal)
        if result['modelFailures']:
            rejected.append(ordinal)
            if not result['actualTopReturn']:
                aborted.append(ordinal)
    if len(rejected) != len(selected):
        raise ValueError(('Whole-C dispatch/timer error not independently rejected', label, rejected, len(selected)))
    return dict(case=label, translationUnitPart=target, old=old, new=new, expectedOccurrences=count, rejectedCases=rejected,
                rejectedAtObservedProtocolBoundary=aborted, abortedRunsAreNotCallerReturns=True, fixtures=selected, proof=row)


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/fifteenth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/fifteenth' or WORK!=ROOT/'work/w5st/fifteenth-proof':raise ValueError('New tenth source/evidence/work scope changed')
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned private native unit runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen dispatch/timer input changed: ' + pin['path'])
    if {format(int(row['address'], 0), '08x') for row in inputs['entries']} != set(SPECS):
        raise ValueError('Exact exclusive dispatch/timer caller identities differ')
    info, main, unused = L.measured_module('main')
    rows, traces = [], []
    for item in inputs['entries']:
        name = format(int(item['address'], 0), '08x')
        row, body = build(ROOT / item['source'], WORK / name / 'positive')
        if (row['targetSha256'], row['bytes']) != (item['targetSha256'], item['bytes']):
            raise ValueError('Full native dispatch/timer caller target differs')
        start = int(row['address'], 0) - 0x02000000
        native = main[start:start + row['bytes']]
        for ordinal, fixture in enumerate(fixtures(name)):
            original = run(row, native, fixture, main, ordinal)
            rebuilt = run(row, body, fixture, main, ordinal)
            if original != rebuilt or original['modelFailures'] or not original['actualTopReturn']:
                write_json(LANE / 'fixture-failure.json', dict(address=row['address'], fixture=fixture, original=original, rebuilt=rebuilt))
                raise ValueError(('Independent dispatch/timer protocol/full state differs', name, ordinal, original['modelFailures']))
            traces.append(dict(address=row['address'], ordinal=ordinal, fixture=fixture, result=original))
        rows.append(row)
        print('proved', row['address'], row['bytes'], len(fixtures(name)), flush=True)
    def selected(name,maximum=5,predicate=None,**fields):
        out=[]
        for ordinal,f in enumerate(fixtures(name)):
            if not all(f.get(k)==v for k,v in fields.items()):continue
            if predicate is not None and not predicate(f,scenario(name,f,ordinal)):continue
            out.append(f)
            if len(out)>=maximum:break
        return out
    cases=[
      ('0208fbe8','wrong-invalid-shutdown-error','return -28;','return -27;',1,selected('0208fbe8',invalid=1)),
      ('0208fbe8','wrong-uncreated-shutdown-error','return -39;','return -38;',1,selected('0208fbe8',state=0,invalid=0)),
      ('0208fbe8','wrong-shutdown-connected-bit','!state(socket,4)','!state(socket,8)',1,selected('0208fbe8',state=5,invalid=0)),
      ('0208fbe8','lost-closing-state','state70|=8','state70|=16',1,selected('0208fbe8',state=5,invalid=0)),
      ('0208fbe8','lost-signed-shutdown-block','send->executor10C,socket->block72','send->executor10C,(u8)socket->block72',1,selected('0208fbe8',state=5,invalid=0,block=128,send=True,executor=True)),
      ('0208fbe8','wrong-shutdown-callback','native_fn_0208ebd8(native_fn_0208fc70,','native_fn_0208ebd8(native_fn_0208fd4c,',1,selected('0208fbe8',state=5,invalid=0,send=True,executor=True)),
      ('0208fbe8','wrong-factory-executor','native_fn_0208fc70,send->executor10C,','native_fn_0208fc70,socket,',1,selected('0208fbe8',state=5,invalid=0,send=True,executor=True)),
      ('0208fbe8','lost-fresh-shutdown-executor','native_fn_0208ecb0(send->executor10C,command)','native_fn_0208ecb0(socket,command)',1,selected('0208fbe8',state=5,invalid=0,send=True,executor=True,allocated=True,mutate=False)),
      ('0208fbe8','lost-cached-shutdown-send','native_fn_0208ecb0(send->executor10C,command)','native_fn_0208ecb0(socket->send68->executor10C,command)',1,selected('0208fbe8',state=5,invalid=0,send=True,executor=True,allocated=True,mutate=True)),
      ('0208fbe8','wrong-no-shutdown-command-error','return -33;','return -32;',1,selected('0208fbe8',state=5,invalid=0,send=True,executor=True,allocated=False)),
      ('0208fbe8','lost-full-shutdown-result','return result;','return (u8)result;',1,selected('0208fbe8',state=5,invalid=0,send=True,executor=True,allocated=True,returned=0x80000000)),
      ('0208fc70','wrong-shutdown-TCP-mode','socket->mode73==4','socket->mode73==3',1,selected('0208fc70',mode=4)),
      ('0208fc70','wrong-shutdown-callback-result','return 0;','return 1;',1,selected('0208fc70')),
      ('0208fc90','wrong-zero-handle-closed-test','(int)socket>=0','(int)socket>0',1,selected('0208fc90',value=0,invalid=1,trash=0)),
      ('0208fc90','wrong-trash-closed-test','!native_fn_020902b4','native_fn_020902b4',1,selected('0208fc90',value=0x02402000,invalid=1,trash=0)),
      ('0208fc90','lost-negative-handle-guard','(int)socket>=0 && ','',1,selected('0208fc90',value=0x80000000)),
      ('0208fcb0','lost-zero-close-handle-guard','(int)socket<=0','(int)socket<0',1,selected('0208fcb0',value=0)),
      ('0208fcb0','wrong-close-progress-errors','return -26;','return -25;',2,selected('0208fcb0',trash=1)),
      ('0208fcb0','wrong-already-invalid-result','if(native_fn_02090294(socket)){return 0;}','if(native_fn_02090294(socket)){return -28;}',1,selected('0208fcb0',trash=0,invalid=1)),
      ('0208fcb0','wrong-wait-close-bit','state(socket,16)','state(socket,8)',1,selected('0208fcb0',state=17,trash=0,invalid=0)),
      ('0208fcb0','lost-wait-close-mark','state70|=24','state70|=8',1,selected('0208fcb0',state=1,trash=0,invalid=0)),
      ('0208fcb0','wrong-close-sentinel','native_fn_0208ec1c(socket->send68,0)','native_fn_0208ec1c(socket->send68,socket)',1,selected('0208fcb0',mode=0,state=1,trash=0,invalid=0)),
      ('0208fcb0','lost-response-queue-clear','command->response8=0','command->response8=socket',1,selected('0208fcb0',state=1,trash=0,invalid=0)),
      ('0208fcb0','wrong-close-command-block','native_fn_0208fd4c,socket,1','native_fn_0208fd4c,socket,0',1,selected('0208fcb0',state=1,trash=0,invalid=0)),
      ('0208fcb0','wrong-close-callback','native_fn_0208ebd8(native_fn_0208fd4c,','native_fn_0208ebd8(native_fn_0208fc70,',1,selected('0208fcb0',state=1,trash=0,invalid=0)),
      ('0208fcb0','lost-cached-close-socket','native_fn_0208ec50(socket,command)','native_fn_0208ec50(command->socket4,command)',1,selected('0208fcb0',state=1,trash=0,invalid=0,mutate=True)),
      ('0208fcb0','wrong-ignored-control-result','(void)native_fn_0208ec50(socket,command);\nreturn 0;','return native_fn_0208ec50(socket,command);',1,selected('0208fcb0',state=1,trash=0,invalid=0,returned=0x80000000))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Four complete ordinary-C main Thumb shutdown/closed-test/close callers356B genuinely MW-link whole original extents/literal pools/unchanged relocations and exact static canonical namespaces/Thumb callback words0x0208fc71 and0x0208fd4d. Frozen base C99 profile/old verifier/parser/normalizer unchanged; no compiler aliases/ASM/raw/object/register/instruction patches.',
      '1274 independent fixture pairs require2548 actual returning original/source callers, GPR/CPSR, complete8MiB RAM, exact widths/writes/frames/SP, ordered imported identities/modes/words and borrowed field/guard states. All original imported/allocator/command/CPS/OS bodies execute0 and receive0 extra source credit; selected32B callback is credited only through its separate top-level full native proof.',
      'Shutdown136B has513 cases including raw byte samples and focused negative signed block/connected16-bit state/send-null/executor-null/allocation-null/full result paths. Closing bit8 is written before checking send/executor. Factory receives cached executor, signed block and exact original tagged callback; final executor is read fresh from cached send after factory mutation. Allocation failure-33 retains prior closing-state effect.',
      'Shutdown callback32B has256 raw signed mode-byte fixtures and calls CPS shutdown only for modes0/4. Closed-test32B has54 cases covering signed negative/zero/positive handle words and invalid/trash full-word flags with original short-circuit order. Close156B has451 cases covering signed nonpositive handles, trash/invalid/created/wait16 checks, closing|wait24 mark, TCP null sentinel, original close callback+block1, response word8 zero and ignored control-send result.',
      'The close factory must supply a non-null writable minimum16B command: original release code has no null branch. Native close callback0x0208fd4c/124B is outside this selected source subset and stays0credit; models prove only caller boundaries. Typed minimum socket128/send272/header16 and signed state16/block8/mode8 are source/access evidence, no complete allocation/storage/original declaration credit.',
      'Actual original literal records/addend0/raw words/origins, canonical even Thumb entries, fresh caller.bin full SHA/word, actual linked STT_FUNC/$t/zero target output and relocatable STT_FUNC/$t/SHT_NOBITS zero-code anchors are checked.184 body/namespace/relocation negatives,10 wrong encoded-callable proofs,4 compiler layout failures,519 fresh signed-field ABI returns+3badABI and27 genuinely linked wrong-C/header cases reject. Aborted negative protocol runs never count as positive caller returns.',
      'New immutable primary public shutdown/close/cleanup text and prior public SDK header/types are comparison inputs only, no production includes/exact native SDK revision proof. Closed original/copied producers and original/copied canonical replays must all pass before READY; no original network/thread/game/platform behavior or full Windows/Android execution claim.',
      'Pending356B stays0 accepted source credit until coordinator acceptance. Combined49/4838B sealed from105/12396B claim leaves56/7558B reserved/uncredited. All earlier frozen READY/source/header/helper/native/reference inputs and bounded residuals stay unchanged.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=4,canonicalMatchedBytes=356,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=4,bytes=356,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
