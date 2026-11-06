import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_twelfth_build import build
from wave20261105_socket_thumb_next_twelfth_models import SPECS, fixtures, scenario
from wave20261105_socket_thumb_next_twelfth_execution import run
from wave20261105_socket_thumb_next_twelfth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/twelfth'
WORK = ROOT / 'work/w5st/twelfth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/twelfth'


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
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/twelfth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/twelfth' or WORK!=ROOT/'work/w5st/twelfth-proof':raise ValueError('New tenth source/evidence/work scope changed')
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
      ('0208f578','wrong-block-bit','(flagBlock&1)','(flagBlock==1)',1,selected('0208f578',flag=3,path=2)),
      ('0208f578','wrong-empty-error','result=-6','result=-5',1,selected('0208f578',flag=0,path=6)),
      ('0208f578','wrong-disconnect-error','result=-56','result=-55',1,selected('0208f578',flag=1,path=4)),
      ('0208f578','wrong-sleep-queue','native_fn_020068d4(receive->waiting10C)','native_fn_020068d4((void *)&receive->out104)',1,selected('0208f578',flag=1,path=2)),
      ('0208f578','wrong-copy-limit','bufferLength>data->size4','bufferLength<data->size4',1,selected('0208f578',size=16,limit=8)),
      ('0208f578','wrong-remote-port','*remotePort=data->remote6','*remotePort=(u16)data->peer8',1,selected('0208f578',predicate=lambda f,p:bool(p['args'][3]))),
      ('0208f578','lost-no-consume','if(!receive->noConsumeFE)','if(receive->noConsumeFE)',1,selected('0208f578',path=0,noConsume=0,mutate=False)),
      ('0208f578','lost-next-packet','out104=data->next0','out104=0',1,selected('0208f578',path=0,noConsume=0,mutate=False,next=True)),
      ('0208f578','wrong-empty-input-reset','data->next0==0','data->next0!=0',1,selected('0208f578',path=0,noConsume=0,mutate=False,next=False)),
      ('0208f578','wrong-queue-consumed-size','size108-=result','size108-=1',1,selected('0208f578',path=0,noConsume=0,mutate=False,size=16)),
      ('0208f578','wrong-release-pointer','release1C(data)','release1C(buffer)',1,selected('0208f578',path=0,noConsume=0,mutate=False)),
      ('0208f578','lost-cached-UDP-IRQ-mask','native_fn_02008008(enable)','native_fn_02008008(0)',1,selected('0208f578')),
      ('0208f660','wrong-capacity-test','max10A>=receive->size108+length','max10A<receive->size108+length',1,selected('0208f660',capacity=True)),
      ('0208f660','wrong-allocation-size','sizeof(UdpView)+length','sizeof(UdpView)+length+1',1,selected('0208f660',capacity=True)),
      ('0208f660','lost-allocated-size-count','size108+=length','size108+=1',1,selected('0208f660',capacity=True,allocated=True,length=16)),
      ('0208f660','lost-packet-length','packet->size4=(u16)length','packet->size4=0',1,selected('0208f660',capacity=True,allocated=True,length=16)),
      ('0208f660','wrong-packet-remote-port','remote6=cps->remote18','remote6=cps->bound1A',1,selected('0208f660',capacity=True,allocated=True)),
      ('0208f660','lost-previous-tail-link','if(receive->in100)','if(0)',1,selected('0208f660',capacity=True,allocated=True,mutate=False,predicate=lambda f,p:f['queues']&1)),
      ('0208f660','wrong-empty-out-condition','out104==0','out104!=0',1,selected('0208f660',capacity=True,allocated=True,mutate=False,queues=0)),
      ('0208f660','wrong-allocation-failure-counter','native_data_021d15a4[0]++','native_data_021d15a4[1]++',1,selected('0208f660',capacity=True,allocated=False)),
      ('0208f660','lost-capacity-failure-counter','native_data_021d15a4[1]++','native_data_021d15a4[1]=0',1,selected('0208f660',capacity=False,counter=0x7fffffff)),
      ('0208f660','wrong-local-port-condition','local74==0','local74!=0',1,selected('0208f660',local=65535,mutate=False)),
      ('0208f660','lost-peer-bound-restore','peer1C=cps->bound20','peer1C=0',1,selected('0208f660')),
      ('0208f660','lost-cached-receive-wakeup','native_fn_02006924(receive->waiting10C)','native_fn_02006924(socket->recv64->waiting10C)',1,selected('0208f660',mutate=True)),
      ('0208f660','lost-cached-callback-IRQ-mask','native_fn_02008008(enable)','native_fn_02008008(0)',1,selected('0208f660'))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Two complete ordinary-C main Thumb UDP receive callers428B genuinely MW-link original whole functions/literal pools/relocations and exact original static ARM/Thumb/data/BSS namespaces with unchanged old verifiers/parser/normalizer and base C99 profile. No ASM, raw/object/register/instruction patches, compiler aliases or guessed original callback registration.',
      '632 independent original/source fixture pairs require1264 actual returning callers, GPR/CPSR, exact fields/writes/frame/SP/stack words, complete8MiB RAM and ordered provider behavior. Original imported/allocator/free/network/OS bodies execute0 and receive0 extra source credit. Only separate fresh typed fixture-provider probes execute their own26 returning test cases.',
      'The232B receiver has504 bounded fixtures across empty/immediate/post-IRQ/waited queues,0..2 sleeps, disconnection/created checks, low-bit block flags, partial/aliased peer outputs, payload/min-copy lengths, queue links and no-consume cases. Cached receive/IRQ words survive provider changes; post-copy packet/flag fields and post-free16-bit queue byte counts are read fresh. Caller returns full packet size even when copy is bounded smaller.',
      'The196B callback has128 bounded fixtures across capacity, allocation success/failure, both queue-tail/head presence bits, local port preservation, payload lengths0/1/16/31, u32 failure-counter overflow and controlled IRQ/allocator/copy state changes. It uses cached receive/IRQ, fresh config allocator/mode, fresh post-allocator metadata/count and post-copy volatile links, then restores current bound peer fields and wakes cached queue.',
      'Original runtime indirect sites0x0208f640 free1word/0return and0x0208f68a allocate1word/1return are independently disassembled/hashed from exact configured bodies. Only fresh controlled ARM/Thumb providers are used.14 wrong origin/load/field/target/ABI/body controls,2 bad callable declarations and4 actual wrong runtime-tag cases reject. These dynamic tags are fixture data, not patches to any original encoded callback literal.',
      'Minimum private types are CPS100 embedded as first socket member/socket128,receive276,UDP header12 with variable bounded payload,config32 and8 observed BSS counter bytes. Actual public volatile in/out pointers and16-bit queue size match repeated native loads. Data-slot0x020de7cc and BSS0x021d15a4 records, literal words/origins and fields0/4 are strict witnesses; external storage/counter array-total/authorship credit0.',
      '158 native body/namespace/relocation negatives,5 compiler layout failures,275 signed/width ABI returns+3badABI and25 genuinely linked wrong-C/header cases must reject. Immutable public read/CPS/header/type/thread-queue references are comparison inputs, no production includes or exact original SDK-version/full declaration/allocation proof. Negative aborted callers never count as positive returns.',
      'Original/copied producer and canonical replays must pass from closed actual inputs before READY. Pending428B stays0 accepted credit until coordinator acceptance. Combined40/3556B sealed from105/12396B leaves65/8840B reserved/uncredited; all earlier source/helper/READY pins and bounded uncredited drafts remain unchanged. No full network/thread/hardware/game/platform execution claim.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=2,canonicalMatchedBytes=428,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=2,bytes=428,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
