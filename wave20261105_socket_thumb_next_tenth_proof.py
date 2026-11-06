import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_tenth_build import build
from wave20261105_socket_thumb_next_tenth_models import SPECS, fixtures, scenario
from wave20261105_socket_thumb_next_tenth_execution import run
from wave20261105_socket_thumb_next_tenth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/tenth'
WORK = ROOT / 'work/w5st/tenth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/tenth'


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
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/tenth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/tenth' or WORK!=ROOT/'work/w5st/tenth-proof':raise ValueError('New tenth source/evidence/work scope changed')
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
    def selected(name,limit=5,predicate=None,**fields):
        out=[]
        for ordinal,f in enumerate(fixtures(name)):
            if not all(f.get(k)==v for k,v in fields.items()):continue
            if predicate is not None and not predicate(f,scenario(name,f,ordinal)):continue
            out.append(f)
            if len(out)>=limit:break
        return out
    cases=[
      ('0208f2ac','wrong-SSL-mode','mode73==4','mode73==0',1,selected('0208f2ac',mode=4)),
      ('0208f2ac','wrong-block-bit','(flagBlock&1)','(flagBlock==1)',1,selected('0208f2ac',flag=0xffffffff,first=-6,mode=0)),
      ('0208f2ac','wrong-wouldblock-sentinel','result==-6','result==-7',1,selected('0208f2ac',first=-6,mode=0,flag=0xffffffff)),
      ('0208f2ac','lost-full-helper-result','return result;','return (u8)result;',2,selected('0208f2ac',mode=4,predicate=lambda f,p:f['second']<0 or f['second']>255)),
      ('0208f2f8','wrong-invalid-error','result=-28','result=-27',1,selected('0208f2f8',kind=0)),
      ('0208f2f8','wrong-empty-receive-error','result=-6','result=-5',1,selected('0208f2f8',kind=2)),
      ('0208f2f8','wrong-TCP-consumption','tcp(socket)?copyLength:cpsLength','tcp(socket)?cpsLength:copyLength',1,selected('0208f2f8',kind=4,limit=1)),
      ('0208f2f8','lost-no-consume-flag','if(!receive->noConsumeFE)','if(receive->noConsumeFE)',1,selected('0208f2f8',kind=3,noConsume=0,mutate=False)),
      ('0208f2f8','lost-fresh-receive','native_fn_02008e0c(cpsBuffer,buffer,(u32)copyLength);receive=socket->recv64;','receive=socket->recv64;native_fn_02008e0c(cpsBuffer,buffer,(u32)copyLength);',1,selected('0208f2f8',kind=3,noConsume=1,mutate=True)),
      ('0208f2f8','lost-peer-outputs','if(remotePort&&remoteIp)','if(remotePort&&remoteIp&&0)',1,selected('0208f2f8',kind=3,outputs=3)),
      ('0208f2f8','wrong-local-bind-condition','socket->local74==0','socket->local74!=0',1,selected('0208f2f8',kind=3,local=0)),
      ('0208f2f8','lost-cached-IRQ-mask','native_fn_02008008(enable)','native_fn_02008008(0)',1,selected('0208f2f8')),
      ('0208f2f8','lost-connecting-clear','state70&=~6','state70&=~4',1,selected('0208f2f8',kind=0)),
      ('0208f3bc','wrong-zero-boundary','length>=0','length>0',1,selected('0208f3bc',length=0,consumed=0,state=4)),
      ('0208f3bc','wrong-remote-port-source','*remotePort=cps->remote18','*remotePort=cps->localA',1,selected('0208f3bc',alias=0,length=16,consumed=0)),
      ('0208f3bc','wrong-established-state','cps->state8!=4','cps->state8!=3',1,selected('0208f3bc',length=0,consumed=0,state=4)),
      ('0208f3bc','lost-buffer-offset','cps->buffer40+consumed','cps->buffer40',1,selected('0208f3bc',length=16,consumed=1)),
      ('0208f3bc','lost-IP-word-width','*remoteIp=cps->peer1C','*(u16 *)remoteIp=(u16)cps->peer1C',1,selected('0208f3bc',alias=0,length=16,consumed=0)),
      ('0208f3bc','wrong-negative-length','*bufferLength=-1','*bufferLength=0',1,selected('0208f3bc',length=0,consumed=1))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Three complete ordinary-C main Thumb receive callers342B genuinely MW-link all full configured extents, original relocations, native BL/BLX modes and same-ROM canonical namespaces. Frozen base C99 profile and old parser/normalizer/verifiers remain unchanged; no ASM, binary/register/instruction patches or helper aliases.',
      '3472 independent fixture pairs require6944 actual original/source caller returns with GPR/CPSR, full8MiB RAM, exact writes/frame/SP, stack formal/output words, ordered provider modes and minimum argument words. All original imported bodies execute0 and receive0 extra credit, including when another selected function is modeled only as an imported boundary.',
      'The76B selector covers all256 raw signed mode bytes, full-word helper returns, SSL direct route, exact-6 fallback, low-bit block flag and preservation of five original arguments through provider mutation. Formal sixth word and provider fifth stack word are checked as actual AAPCS words.',
      'The194B caller has2880 bounded fixtures covering null/non-null buffers, empty/negative/positive observed lengths, TCP/SSL/datagram signed mode, min/copy/consume lengths, all four optional-output combinations, no-consume flags and controlled post-boundary socket/receive changes. IRQ mask is cached through complete provider clobbers; fresh receive pointer/state/ports and16/32-bit writes are independently modeled. Provider copy and output-local effects are models, not original callee execution.',
      'The72B leaf has240 bounded fixtures covering signed remaining-byte subtraction, negative/zero/positive length, established state4, five-word stack output ABI, aliased outputs/CPS/socket/receive fields and buffer offset. CPS view72,receive prefix264,socket128 are private minimum views only; thread-specific196/mutex224/consumed248/no-consume254 and all observed field widths are checked. All storage attribution0.',
      'Fresh C layout and ABI, explicit whole-caller/relocation namespace and native-input negatives plus19 genuinely linked wrong-C/header cases must pass. Native/source traces and whole function comparisons are replayed in original/copied producer and canonical roots before READY; aborted counterexamples are not caller returns.',
      'New immutable public NitroWiFi read source and prior public primitive/header references are comparison context only, no production system includes, original SDK version/declaration/allocation proof or network/mutex/thread/game/platform execution claim. The194B min tie-expression source shape is measured by exact bytes, not an invented instruction patch.',
      'The120B peek wrapper differs outside relocation fields at a bounded compiler context plateau and remains excluded with original draft under generated. Pending342B remains0 accepted credit until coordinator161or later. Combined36/3028B sealed from105/12396B claim leaves69/9368B reserved/uncredited, including all earlier unmatched drafts.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=3,canonicalMatchedBytes=342,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=3,bytes=342,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
