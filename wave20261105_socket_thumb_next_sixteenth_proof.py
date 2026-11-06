import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_sixteenth_build import build
from wave20261105_socket_thumb_next_sixteenth_models import SPECS, fixtures, scenario
from wave20261105_socket_thumb_next_sixteenth_execution import run
from wave20261105_socket_thumb_next_sixteenth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/sixteenth'
WORK = ROOT / 'work/w5st/sixteenth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/sixteenth'


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
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/sixteenth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/sixteenth' or WORK!=ROOT/'work/w5st/sixteenth-proof':raise ValueError('New tenth source/evidence/work scope changed')
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
      ('0208fdc8','wrong-null-cleanup-condition','if(socket)','if(!socket)',1,selected('0208fdc8',null=False)),
      ('0208fdc8','lost-zero-cleanup-state','state70=0','state70=1',1,selected('0208fdc8',null=False)),
      ('0208fdc8','wrong-TCP-cleanup-mode','socket->mode73==4','socket->mode73==3',1,selected('0208fdc8',mode=4,null=False)),
      ('0208fdc8','lost-fresh-receive-pipe','native_fn_0208fe74(socket->recv64)','native_fn_0208fe74(socket->send68)',2,selected('0208fdc8',mode=0,mutate=True,null=False)),
      ('0208fdc8','lost-cached-next-before-free','data=next;','data=data->next0;',1,selected('0208fdc8',mode=1,packets=2,mutate=True,null=False)),
      ('0208fdc8','lost-zero-UDP-byte-count','size108=0','size108=1',1,selected('0208fdc8',mode=1,null=False)),
      ('0208fdc8','lost-UDP-tail-reset','socket->recv64->in100=0','socket->recv64->in100=socket->recv64->out104',1,selected('0208fdc8',mode=1,packets=1,mutate=False,null=False)),
      ('0208fdc8','lost-UDP-head-reset','socket->recv64->out104=0;','',1,selected('0208fdc8',mode=1,packets=1,mutate=False,null=False)),
      ('0208fdc8','wrong-UDP-wakeup-queue','native_fn_02006924(socket->recv64->waiting10C)','native_fn_02006924(socket->send68->waiting104)',1,selected('0208fdc8',mode=1,null=False)),
      ('0208fdc8','lost-trash-unregistration','native_fn_02090284(socket)','native_fn_02090248(socket)',1,selected('0208fdc8',null=False)),
      ('0208fdc8','wrong-released-object','release1C(socket)','release1C(socket->recv64)',1,selected('0208fdc8',null=False)),
      ('0208fdc8','lost-cached-cleanup-IRQ-mask','native_fn_02008008(enable)','native_fn_02008008(0)',1,selected('0208fdc8',null=False)),
      ('0208fe74','wrong-joined-thread-offset','native_fn_02006890(pipe->thread20)','native_fn_02006890(pipe->mutexE0)',1,selected('0208fe74',null=False)),
      ('0208fe74','wrong-message-nonblock-flag','(void *)&command,0','(void *)&command,1',1,selected('0208fe74',null=False)),
      ('0208fe74','wrong-message-output-address','(void *)&command','(void **)0',1,selected('0208fe74',null=False)),
      ('0208fe74','lost-nonnull-command-guard','if(command)','if(!command)',1,selected('0208fe74',stream='command',null=False)),
      ('0208fe74','wrong-response-guard','if(command->response8)','if(!command->response8)',1,selected('0208fe74',stream='reply',null=False)),
      ('0208fe74','wrong-cancel-error-word','(void *)-11','(void *)-10',1,selected('0208fe74',stream='reply',null=False)),
      ('0208fe74','wrong-response-block-flag','(void *)-11,0','(void *)-11,1',1,selected('0208fe74',stream='reply',null=False)),
      ('0208fe74','wrong-freed-command','native_fn_0208ebfc(command)','native_fn_0208ebfc(pipe)',1,selected('0208fe74',stream='command',null=False)),
      ('0208fe74','lost-scheduler-enable','native_fn_02006ca4()','native_fn_02006c70()',1,selected('0208fe74',null=False)),
      ('0208fe74','lost-drain-IRQ-mask','native_fn_02008008(enable)','native_fn_02008008(0)',1,selected('0208fe74',null=False)),
      ('0208fedc','wrong-trash-list-loop-condition','native_data_021d15b0!=0','native_data_021d15b0==0',1,selected('0208fedc',count=2)),
      ('0208fedc','wrong-current-trash-object','native_fn_0208fdc8(native_data_021d15b0)','native_fn_0208fdc8(0)',1,selected('0208fedc',count=2)),
      ('0208fedc','lost-trash-loop-IRQ-mask','native_fn_02008008(enable)','native_fn_02008008(0)',1,selected('0208fedc'))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Three complete ordinary-C main Thumb cleanup/drain callers316B genuinely MW-link all full original bodies/literals/relocations and exact same-ROM ARM/Thumb/data/BSS namespace/origins, with unchanged old parser/normalizer/verifier/base C99 profile. No ordinary-logic ASM/binary/object/register/instruction patch/compiler alias.',
      '462 independent fixture pairs require924 actual original/source returning callers, complete GPR/CPSR/SP/writes/frame/field guards/ordered provider words/modes/LR sites and whole8MiB RAM equality. Functions return void: no invented result semantics. Every original imported/cleanup/free/scheduler/queue/OS body executes0 and receives0 extra credit, including other selected entries modeled as imported boundaries.',
      'Cleanup172B has416 bounded fixtures over nullable socket/all raw signed-mode input samples plus focused TCP/SSL/UDP/send/default modes,0..3 packets and controlled provider changes. It resets state before teardown, captures packet next before free, loads receive/config fields fresh at measured boundaries, clears current UDP links/count, wakes/frees the observed pipe, unregisters lists then releases socket under cached IRQ state. Mode/slot/provider models do not claim original allocator/list/scheduler semantics.',
      'Pipe-drain104B has40 bounded fixtures for null/nonnull pipe,0..3 message streams, null command/response variants and cancelled response word-11, exact queue/thread addresses, scheduler disable/enable/reschedule and IRQ restoration. Incoming stack out-pointer is SP-28 within original32B frame; response/free/message bodies are modeled only. Trash-loop40B has6 bounded cases for0..2 sockets and list changes during IRQ/provider boundaries, with cached IRQ and fresh observed slot0x021d15b0.',
      'Two original release sites0x0208fe0e and0x0208fe64 prove one pointer/void return, fresh config field28 and packet-next caching from exact disassembly/hash. Runtime LR identifies each16-bit BLX-register site. Only fresh typed controlled ARM/Thumb test providers are used:26 separate ABI returns,14badsite+2baddeclaration+4actual wrong-tag controls reject. No original callback identities, function-word patches or general free behavior is inferred.',
      'Private minimum CPS100/socket128/receive276/send272/pipe248/header16/config32 layouts and queue/thread32/mutex224 are fresh-compiled. Exact original config data-slot0x020de7cc and trash BSS-slot0x021d15b0 are strict literal/record witnesses,4B observed slot each,0 storage/original allocation credit.309 whole-caller/body/namespace/relocation negatives,4 layout failures,275 signed/width ABI+3badABI and25 genuinely linked wrong-C/header cases reject; aborted negatives are not positive caller returns.',
      'New immutable public shutdown/close/cleanup/header/type/thread references are actual comparison inputs only, no production headers/exact original SDK revision/original complete declaration proof. All original/copied producer and canonical replays must pass closed actual inputs before READY; no actual network/game/platform/Windows/Android execution or arbitrary-list convergence claim.',
      'Pending316B remains0 accepted credit until coordinator162or later. Combined52/5154B sealed from105/12396B claim leaves53/7242B reserved/uncredited. All previous READY/source/helper/header/native/reference inputs and bounded residual drafts remain unchanged.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=3,canonicalMatchedBytes=316,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=3,bytes=316,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
