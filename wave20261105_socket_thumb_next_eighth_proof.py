import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_eighth_build import build
from wave20261105_socket_thumb_next_eighth_models import SPECS, fixtures, scenario
from wave20261105_socket_thumb_next_eighth_execution import run
from wave20261105_socket_thumb_next_eighth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/eighth'
WORK = ROOT / 'work/w5st/eighth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/eighth'


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
    def selected(name,limit=5,predicate=None,**fields):
        out=[]
        for ordinal,f in enumerate(fixtures(name)):
            if not all(f.get(k)==v for k,v in fields.items()):continue
            if predicate is not None and not predicate(f,scenario(name,f,ordinal)):continue
            out.append(f)
            if len(out)>=limit:break
        return out
    cases=[
      ('0208eff0','wrong-closing-bit','state(socket,8)','state(socket,4)',1,selected('0208eff0',state=5,mutate=False,invalid=False)),
      ('0208eff0','lost-created-gate','if(!created(socket))','if(created(socket))',1,selected('0208eff0',state=1,mutate=False,invalid=False)),
      ('0208eff0','wrong-connected-error','block(socket)?-30:0','block(socket)?-29:0',1,selected('0208eff0',state=5,mode=0,block=1,mutate=False)),
      ('0208eff0','lost-connecting-data','return native_data_020de7d0;','return -26;',1,selected('0208eff0',state=3,mode=0,connecting=7,mutate=False)),
      ('0208eff0','wrong-port-field','socket->remote76=remotePort;','socket->local74=remotePort;',2,selected('0208eff0',state=1,mutate=False)),
      ('0208eff0','lost-nonblock-progress','block(socket)?result:-26','block(socket)?result:0',1,selected('0208eff0',state=1,mode=0,block=0,mutate=False)),
      ('0208eff0','lost-volatile-connect-state','volatile s16 state70;','s16 state70;',1,selected('0208eff0',predicate=lambda f,p:bool(f.get('volatileTransitions')))),
      ('02090138','wrong-signed-readable','native_fn_020901e4(socket)>0','(u32)native_fn_020901e4(socket)>0',1,selected('02090138',state=5,mode=0,read=-1,mutate=False)),
      ('02090138','wrong-signed-writable','native_fn_0208f900(socket)>0','(u32)native_fn_0208f900(socket)>0',1,selected('02090138',state=5,mode=0,write=-1,mutate=False)),
      ('02090138','wrong-error-bit','state(socket,0x40)','state(socket,0x80)',1,selected('02090138',state=0x40,mutate=False)),
      ('02090138','wrong-established-state','cpsState8!=4','cpsState8!=0',1,selected('02090138',state=5,mode=0,cps=0,read=0,write=0,mutate=False,predicate=lambda f,p:not f.get('volatileTransitions'))),
      ('02090138','wrong-state-clear-mask','state70&=~6','state70&=~2',1,selected('02090138',state=5,mode=0,cps=0,read=0,write=0,mutate=False,predicate=lambda f,p:not f.get('volatileTransitions'))),
      ('02090138','wrong-connecting-hangup','!state(socket,2)','!state(socket,4)',1,selected('02090138',state=3,mode=0,read=0,mutate=False)),
      ('02090138','lost-interrupt-mask','native_fn_02008008(level)','native_fn_02008008(0)',1,selected('02090138',state=5,mode=0,read=0,mutate=False)),
      ('02090138','lost-volatile-poll-state','volatile s16 state70;','s16 state70;',1,selected('02090138',predicate=lambda f,p:bool(f.get('volatileTransitions')))),
      ('020901e4','wrong-UDP-mode','if(udp(socket))','if(tcp(socket))',1,selected('020901e4',receive=True,mode=1,datagram=True,predicate=lambda f,p:f['size']!=0)),
      ('020901e4','lost-datagram-size','out?out->size4:0','out?0:0',1,selected('020901e4',receive=True,mode=1,datagram=True,predicate=lambda f,p:f['size']!=0)),
      ('020901e4','wrong-consumed-sign','received44-(s32)receive','received44+(s32)receive',1,selected('020901e4',receive=True,mode=0,received=17,consumed=1)),
      ('020901e4','wrong-receive-null-gate','if(receive)','if(!receive)',1,selected('020901e4',receive=True,mode=0,received=17,consumed=1)),
      ('020901e4','wrong-empty-datagram','out?out->size4:0','out?out->size4:1',1,selected('020901e4',receive=True,mode=1,datagram=False))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Three complete ordinary-C main Thumb socket/state callers400B genuinely MW-link full configured original extents, relocations, original BL/BLX modes and initialized-data literal. Frozen base C99 profile/old parser/normalizer/verifier and all earlier packets remain unchanged; no ASM/raw/register/instruction patches, aliases or allocation sweep.',
      '1056 independent original/source fixture pairs require2112 actual returning callers, full GPR/CPSR, ordered provider words/modes, exact observed volatile-state read count, writes and8MiB RAM equality. All actual original imported bodies execute0 and get0 source credit; all external data/prefix storage gets0 credit.',
      'The176B connect caller covers invalid/closing/uncreated/connected/connecting/error/new-bind branches, raw signed modes/block bytes,16-bit ports/full32 IPs/results, initialized connecting-data reads and mutable provider boundaries. The172B poll caller covers signed readable/writable results, cached interrupt masks, fresh state/mode after providers, established/disconnected/hangup flags and16-bit state-mask writes.',
      'Eight targeted fixtures apply explicitly controlled data-only updates immediately before specified volatile state-read ordinals. They modify only the borrowed state field and never any original/generated instruction or register. Independent public-declaration-based model reads and actual CPU memory reads must agree; these are concurrency/volatile unit counterfactuals, not observed game/hardware scheduling.',
      'The52B occupied-size leaf covers absent receive views, UDP absent/present6-byte datagrams and full unsigned16 lengths, TCP/SSL received-minus-volatile-consumed values and other raw modes. Selected subtraction operands remain within defined signed32 arithmetic; no undefined-overflow input domain is claimed.',
      'Shared private views are128-byte socket,264-byte receive prefix,6-byte datagram and signed initialized connecting word. Actual compiler assertions,275 fresh signed-byte/signed-half/unsigned-half ABI returns, three signedness negatives, four layout negatives,96namespace/original-evidence negatives and20 genuinely linked wrong-C/header errors must reject. Aborted negatives never count as returning callers.',
      'Immutable public SOCL poll/bind/header and SDK primitive-type references are comparison text, not production includes or proof of exact native SDK version, complete original declarations/allocations, network/OS/game/platform behavior. Production C/header and full runtime/native/reference inputs must replay from an independent root.',
      'Original/copied producers and generic canonical original/copied replay must pass before READY. Pending400B remains0 source credit until serialized acceptance; combined31/2516B leaves74/9880B reserved/uncredited in105/12396B claim, coordinator160or later. Earlier packets remain immutable; unmatched212/468/288B drafts remain excluded.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=3,canonicalMatchedBytes=400,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=3,bytes=400,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
