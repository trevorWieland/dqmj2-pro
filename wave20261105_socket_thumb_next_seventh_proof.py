import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_seventh_build import build
from wave20261105_socket_thumb_next_seventh_models import SPECS, fixtures, scenario, TARGETS
from wave20261105_socket_thumb_next_seventh_execution import run
from wave20261105_socket_thumb_next_seventh_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/seventh'
WORK = ROOT / 'work/w5st/seventh-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/seventh'


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
    def selected(name,limit=5,needs=None,predicate=None,**fields):
        out=[]
        for ordinal,f in enumerate(fixtures(name)):
            if not all(f.get(k)==v for k,v in fields.items()):continue
            plan=scenario(name,f,ordinal)
            if needs is not None and not any(a['address']==needs for a in plan['actions']):continue
            if predicate is not None and not predicate(f,plan):continue
            out.append(f)
            if len(out)>=limit:break
        return out
    cases=[
      ('0208eb34','wrong-packet-size','sizeof(CommandPacket)','(sizeof(CommandPacket)+4)',1,selected('0208eb34',maximum=1)),
      ('0208eb34','wrong-allocation-null-gate','if(!messages)','if(messages)',1,selected('0208eb34',maximum=1,fail=False)),
      ('0208eb34','wrong-packet-array-base','(u32)messages+messageBytes','(u32)messages+packetBytes',1,selected('0208eb34',maximum=1,fail=False)),
      ('0208eb34','wrong-loop-bound','while(maximum>0)','while(maximum>1)',1,selected('0208eb34',maximum=1,fail=False)),
      ('0208eb34','lost-message-array-publish','array0=messages;','array0=0;',1,selected('0208eb34',maximum=1,fail=False)),
      ('0208eb90','wrong-full-bound','used1C<','used1C<=',1,selected('0208eb90',count=2,used=2)),
      ('0208eb90','lost-clear','array0=0;','array0=(void **)1;',1,selected('0208eb90',count=2,used=2)),
      ('0208eb90','wrong-release-pointer','release1C(native_data_021d1580.array0)','release1C(&native_data_021d1580.queue4)',1,selected('0208eb90',count=2,used=2)),
      ('0208ebfc','wrong-null-command-gate','if(command)','if(!command)',1,selected('0208ebfc',present=True)),
      ('0208ebfc','wrong-free-queue-flag',',command,0)',',command,1)',1,selected('0208ebfc',present=True)),
      ('0208ec1c','wrong-block-bit','blockD&1','blockD&2',1,selected('0208ec1c',present=True,flag=1)),
      ('0208ec1c','wrong-null-block-gate','command &&','!command &&',1,selected('0208ec1c',present=True,flag=0)),
      ('0208ec1c','wrong-failure-free','if(!result)','if(result)',1,selected('0208ec1c',returned=0)),
      ('0208ec1c','wrong-error-code','result?0:-42','result?0:-41',1,selected('0208ec1c',returned=0)),
      ('0208ec60','wrong-blocking-equality','command->blockD==1','command->blockD&1',1,selected('0208ec60',flag=3)),
      ('0208ec60','lost-response-binding','response8=&queue;','response8=0;',1,selected('0208ec60',flag=1)),
      ('0208ec60','lost-direct-result','result=native_fn_0208ec1c(pipe,command);','result=0;native_fn_0208ec1c(pipe,command);',1,selected('0208ec60',flag=0,sendReturn=0x80000000)),
      ('0208ec60','wrong-reply-output','(void **)&result','&response',1,selected('0208ec60',flag=1)),
      ('0208eccc','lost-response-result','(void *)result,0','(void *)0,0',1,selected('0208eccc',events=1,response=True,mutate=False,returned=0x80000000)),
      ('0208eccc','lost-socket-result','->result6C=result;','->result6C=0;',1,selected('0208eccc',events=1,socket=True,mutate=False,returned=0x80000000)),
      ('0208eccc','lost-interrupt-mask','native_fn_02008008(level)','native_fn_02008008(0)',1,selected('0208eccc',events=1)),
      ('0208eccc','wrong-response-block','(void *)result,0','(void *)result,1',1,selected('0208eccc',events=1,response=True)),
      ('0208eccc','wrong-remove-block','&pipe->queue0,0,0','&pipe->queue0,0,1',1,selected('0208eccc',events=1)),
      ('0208eccc','lost-scheduler-enable','native_fn_02006ca4();','native_fn_02006c70();',1,selected('0208eccc',events=1))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    geometry=controls(rows)
    wrongTags=[]
    callerForKind={'allocate':'0208eb34','release':'0208eb90','handler':'0208eccc'}
    for (kind,mode),target in TARGETS.items():
        name=callerForKind[kind];chosen=selected(name,mode=mode,needs=target)
        if not chosen:raise ValueError('Actual scripted one-word provider fixture absent')
        fixture=dict(chosen[0],wrongCallbackTag=kind);row=next(r for r in rows if int(r['address'],0)==int(name,16));start=int(name,16)-0x02000000
        result=run(row,main[start:start+row['bytes']],fixture,main,0)
        if result['actualTopReturn'] or not result['modelFailures']:raise ValueError('Wrong runtime one-word callable mode tag admitted')
        wrongTags.append(dict(case=kind+'-'+mode,fixture=fixture,rejected=True,result=result,sourceCredit=0))
    geometry['wrongRuntimeCallbackTags']=wrongTags
    write_json(LANE / 'binding-layout-controls.json', geometry)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Six complete ordinary-C main Thumb command/queue callers368B genuinely MW-link every full configured original extent, relocations, original BL/BLX modes and data literal. Frozen base C99 profile/old parser/normalizer/verifier and all earlier packets remain unchanged; no ASM/raw/register/instruction patches or helper aliases.',
      '1092 independent original/source fixture pairs require2184 actual returning callers, full GPR/CPSR, all direct/indirect provider argument words/modes/SP, writes and8MiB RAM equality. All original imported/callback/OS bodies execute0 and receive0source credit; controlled fixture providers are explicitly separate from actual original registrations.',
      'Shared measured prefixes are signed-byte command header16, command union44, thread queue8, message queue32, pipe32, overlapping packet-queue state36, configuration32 and volatile-result socket112. The original queue starts4bytes into the same state; no duplicated or independent storage credit is assigned.',
      'Startup covers allocation failure,0/1/2/8 packet loops, huge/negative-word requests with allocation failure only, exact rounded message/packet strides and final global publication despite provider mutation. Cleanup uses signed full-count comparisons and clears the global pointer after a mutable release boundary.',
      'Free/send/execute cover null commands, all256 signed flag bytes, low-bit blocking versus exact flag1 response waits, return0/full-word failures, preserved local32-byte response queue/result slots and cached input/result words across providers. Handler fixtures terminate after0/1/2/3 scripted commands, distinguish cached handler results from fresh mutable command/socket/response fields and restore the captured interrupt word after scheduler boundaries.',
      'Three original indirect sites qualify only config allocate24/release28 and command handler0, one argument word and applicable result word. Fresh typed ARM/Thumb providers have26 separate actual test returns. Twenty-one wrong original-site contracts, two bad callable declarations, six runtime wrong tags, five wrong layouts,292 signed-byte/count ABI returns plus2badABI and24 genuinely linked wrong-C/header errors reject. Aborted negatives never count as returning callers.',
      'Public immutable SOCL command implementation/header, SDK message/thread and primitive-type text/manifests are pinned comparison inputs only. Production C/header is independently closed; exact native SDK version, full original declarations/storage, actual allocator/scheduler/message FIFO/game/hardware behavior and unbounded loop progress remain unproved.',
      'Original/copied producers and generic original/copied canonical replay plus complete private tool/runtime/native/reference pins are required before READY. Pending368B credit remains0 until serialized acceptance; combined28/2116B leaves77/10280B reserved/uncredited in105/12396B claim, coordinator160or later. Unmatched212/468/288B drafts remain excluded.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=6,canonicalMatchedBytes=368,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=6,bytes=368,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
