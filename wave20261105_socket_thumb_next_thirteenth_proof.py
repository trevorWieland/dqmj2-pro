import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_thirteenth_build import build
from wave20261105_socket_thumb_next_thirteenth_models import SPECS, fixtures, scenario
from wave20261105_socket_thumb_next_thirteenth_execution import run
from wave20261105_socket_thumb_next_thirteenth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/thirteenth'
WORK = ROOT / 'work/w5st/thirteenth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/thirteenth'


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
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/thirteenth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/thirteenth' or WORK!=ROOT/'work/w5st/thirteenth-proof':raise ValueError('New tenth source/evidence/work scope changed')
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
      ('0208f724','wrong-invalid-write-error','return -28;','return -27;',1,selected('0208f724',invalid=1)),
      ('0208f724','wrong-uncreated-write-error','return -39;','return -38;',1,selected('0208f724',null=True,invalid=0)),
      ('0208f724','wrong-connected-bit','!state(socket,4)','!state(socket,8)',1,selected('0208f724',mode=0,state=5,flag=0,block=1)),
      ('0208f724','wrong-dontwait-mask','(flags&4)','(flags&1)',1,selected('0208f724',mode=1,state=1,flag=4,block=1)),
      ('0208f724','wrong-no-block-value','block72==0','block72==1',1,selected('0208f724',mode=1,state=1,flag=0,block=1)),
      ('0208f724','wrong-trylock-result','if(!native_fn_020071a8','if(native_fn_020071a8',1,selected('0208f724',mode=1,state=1,flag=4,tryResult=0)),
      ('0208f724','lost-cached-send-unlock','native_fn_02007110(send->mutexE0)','native_fn_02007110(socket->send68->mutexE0)',1,selected('0208f724',mode=1,state=1,flag=0,block=1,mutate=True)),
      ('0208f724','lost-full-write-result','return result;','return (u8)result;',1,selected('0208f724',mode=1,state=1,flag=0,block=1,returned=0x80000000)),
      ('0208f7e4','wrong-UDP-payload-limit','sendLength-=42','sendLength-=41',1,selected('0208f7e4',mode=1,length=29)),
      ('0208f7e4','wrong-message-size-error','return -35;','return -34;',1,selected('0208f7e4',mode=1,length=29)),
      ('0208f7e4','wrong-TCP-prefix-size','sendLength-=54','sendLength-=53',1,selected('0208f7e4',mode=0,length=29)),
      ('0208f7e4','lost-minimum-bound','minimum=length>sendLength?sendLength:length','minimum=length',1,selected('0208f7e4',mode=0,length=29)),
      ('0208f7e4','wrong-buffer-advance','buffer+=writeLength','buffer+=1',1,selected('0208f7e4',length=17,flag=1,path='normal')),
      ('0208f7e4','wrong-copied-count','copied+=writeLength','copied++',1,selected('0208f7e4',length=8,flag=0,path='normal')),
      ('0208f7e4','wrong-block-flag-lowbit','(flagBlock&1)','(flagBlock==1)',1,selected('0208f7e4',length=17,flag=3,path='normal')),
      ('0208f7e4','lost-zero-execution-error','if(result<=0)','if(result<0)',1,selected('0208f7e4',mode=1,length=8,path='exec-fail')),
      ('0208f7e4','wrong-allocation-output-pointer','&writeIn','(s32 *)0',1,selected('0208f7e4',length=8,path='normal')),
      ('0208f900','lost-ring-one-byte-gap','available=out-in-1','available=out-in',1,selected('0208f900')),
      ('0208f900','wrong-zero-wrap-condition','available<0','available<=0',1,selected('0208f900',inValue=0,outValue=1,size=16)),
      ('0208f900','lost-unsigned-ring-index','volatile u16 in100;','volatile s16 in100;',1,selected('0208f900',inValue=65535))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Three complete ordinary-C main Thumb write forwarding/buffering/ring callers398B genuinely MW-link all whole configured extents/original relocations, exact CPU/program/module/mode and canonical target entries under unchanged old parser/normalizer/verifiers/base C99 profile. No ordinary-logic ASM, raw/object/register/instruction patch or compiler alias.',
      '1523 fixture pairs require3046 actual original/source caller returns, GPR/CPSR, ordered provider modes/words/stack slots, exact writes/SP and whole8MiB RAM equality. Original imported/mutex/allocator/send/command bodies execute0 and receive0 extra credit even where another selected entry is independently proved as a top-level function.',
      'The190B forwarder has579 fixtures covering 256 raw mode/block-byte input samples plus focused path cases, invalid/null/uncreated/TCP-disconnected/closing cases, flag4/no-block0/trylock paths, cached send/mutex after provider mutation, six forwarded words including unsigned16 remote port and full result. Null socket fixtures stop at the measured invalid/created checks before field accesses.',
      'The180B buffer caller has864 fixtures over signed nonpositive/positive lengths, UDP payload28 vs oversized29, TCP prefix54/UDP42, min bounds, low-bit block flags, finite allocator0/positive streams, executor negative/zero/INT_MIN, cached size/minimum across mutation and address/count progress. Blocking infinite-zero allocators are excluded from returning fixtures; modeled streams are bounded. Original frame56 also stores4bytes into incoming fifth-argument home SP+0: exact original store and preservation of that formal word are explicit, not a broad frame exception.',
      'The28B leaf has80 fixtures over unsigned16 producer/consumer ring indices and signed32 ring size, one-byte gap and negative wrap. Minimum typed projections are CPS100 first socket member/socket128/send272/write command44; mutex224,ring size248/data252/in256/out258/wait260/executor268 and volatile16-bit indices are checked. External storage/original complete declarations/allocation credit0.',
      '105 whole-caller/native namespace/relocation negatives plus7 exact incoming-formal/store negatives,4 actual compiler layout failures,275 signed/width ABI returns+3badABI and20 genuinely linked wrong-C/header cases must reject. New immutable public write text plus prior CPS/header/type/queue references are comparison inputs, not production headers or proof of exact native SDK revision.',
      'Original and copied producer/canonical roots must all pass with frozen actual source/header/tools/native/reference inputs before READY. Unit providers model only minimum observed ABI/state, no original network/mutex/OS/game/hardware/platform execution or convergence guarantee beyond the bounded returning streams.',
      'Pending398B stays0 accepted source credit until coordinator acceptance. Combined43/3954B sealed from105/12396B claim leaves62/8442B reserved/uncredited; two exact command/callback candidates528B remain independently unsealed outside this packet. Earlier source/helper/READY pins and bounded drafts remain immutable.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=3,canonicalMatchedBytes=398,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=3,bytes=398,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
