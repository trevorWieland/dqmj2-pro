import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_fourteenth_build import build
from wave20261105_socket_thumb_next_fourteenth_models import SPECS, fixtures, scenario
from wave20261105_socket_thumb_next_fourteenth_execution import run
from wave20261105_socket_thumb_next_fourteenth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/fourteenth'
WORK = ROOT / 'work/w5st/fourteenth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/fourteenth'


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
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/fourteenth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/fourteenth' or WORK!=ROOT/'work/w5st/fourteenth-proof':raise ValueError('New tenth source/evidence/work scope changed')
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
      ('0208f91c','wrong-write-callback','native_fn_0208ebd8(native_fn_0208fa34,','native_fn_0208ebd8(native_fn_0208f540,',1,selected('0208f91c')),
      ('0208f91c','wrong-allocator-block-word','send->executor10C,flagBlock)','send->executor10C,0)',1,selected('0208f91c',flag=1)),
      ('0208f91c','wrong-no-command-error','return -33;','return -32;',1,selected('0208f91c',allocated=False)),
      ('0208f91c','wrong-noresult-header','command->blockD=3','command->blockD=1',1,selected('0208f91c',mode=0,flag=1,allocated=True,mutate=False)),
      ('0208f91c','wrong-command-nonblock','command->blockD=0','command->blockD=1',1,selected('0208f91c',flag=0,allocated=True)),
      ('0208f91c','wrong-ring-wrap-tie','writeIn+length<writeSize','writeIn+length<=writeSize',1,selected('0208f91c',wrap=True,length=1,allocated=True)),
      ('0208f91c','wrong-first-segment-size','writeSize-writeIn','writeSize-writeIn-1',1,selected('0208f91c',wrap=True,length=7,allocated=True)),
      ('0208f91c','wrong-second-source','buffer2=buffer+command->firstLength14','buffer2=buffer',1,selected('0208f91c',wrap=True,length=7,allocated=True)),
      ('0208f91c','wrong-second-destination','native_fn_02008e0c(buffer2,command->second18,','native_fn_02008e0c(buffer2,command->first10,',1,selected('0208f91c',wrap=True,length=7,allocated=True)),
      ('0208f91c','lost-fresh-saved-ring-input','native_fn_02008e0c(buffer,command->first10,(u32)command->firstLength14);\nsavedIn=send->in100;','savedIn=send->in100;native_fn_02008e0c(buffer,command->first10,(u32)command->firstLength14);\n',1,selected('0208f91c',wrap=False,allocated=True,mutate=True,enqueue=-1)),
      ('0208f91c','lost-failed-enqueue-rollback','send->in100=savedIn','send->in100=0',1,selected('0208f91c',allocated=True,enqueue=-1)),
      ('0208f91c','lost-fresh-executor','native_fn_0208ecb0(send->executor10C,command)','native_fn_0208ecb0(socket,command)',1,selected('0208f91c',allocated=True,mutate=False)),
      ('0208f91c','wrong-peer-selection','socket->peer78==0 || peer!=0','socket->peer78==0 && peer!=0',1,selected('0208f91c',allocated=True,mutate=True,inputPeer=0x89abcdef)),
      ('0208f91c','lost-CPS-local-port-mirror','socket->cps0.localA=socket->local74','socket->cps0.localA=0',1,selected('0208f91c',allocated=True,predicate=lambda f,p:any(a['address']==0x0208d6b4 for a in p['actions']))),
      ('0208f91c','wrong-explicit-remote-port','command->remote26=remotePort','command->remote26=socket->remote76',1,selected('0208f91c',allocated=True,mutate=True,inputPeer=0x89abcdef)),
      ('0208fa34','wrong-connected-state','state(socket,4)','state(socket,8)',1,selected('0208fa34',mode=0,state=4,peer=False,mutate=False)),
      ('0208fa34','wrong-bind-condition','if(command->peer28)','if(!command->peer28)',1,selected('0208fa34',mode=1,peer=False,mutate=False)),
      ('0208fa34','wrong-TCP-send-offset','offset=tcp(socket)?54:42','offset=tcp(socket)?53:42',1,selected('0208fa34',mode=0,state=4,peer=False,mutate=False)),
      ('0208fa34','wrong-UDP-send-offset','offset=tcp(socket)?54:42','offset=tcp(socket)?54:41',1,selected('0208fa34',mode=1,mutate=False)),
      ('0208fa34','lost-cached-send-buffer','native_fn_0208fb94(sendBuffer,sendLength,command)','native_fn_0208fb94(socket->cps0.sendBuffer4C+offset,sendLength,command)',1,selected('0208fa34',mode=0,state=4,peer=False,mutate=True)),
      ('0208fa34','lost-zero-write-timeout','result=(int)native_fn_0208dd38(sendBuffer,(u32)result);if(result<=0)','result=(int)native_fn_0208dd38(sendBuffer,(u32)result);if(result<0)',1,selected('0208fa34',mode=0,state=4,path='one',write=0)),
      ('0208fa34','lost-byte-result-count','copied+=result','copied++',1,selected('0208fa34',mode=0,state=4,path='one',write=2)),
      ('0208fa34','lost-closing-state-clear','state70&=~14','state70&=~6',1,selected('0208fa34',mode=1,path='one',mutate=True,write=-1)),
      ('0208fa34','wrong-reset-flag','state70|=128','state70|=64',1,selected('0208fa34',mode=1,path='one',mutate=True,write=-1)),
      ('0208fa34','lost-CPS-close','native_fn_0208d910()','native_fn_02006924(0)',1,selected('0208fa34',mode=1,path='one',mutate=True,write=-1)),
      ('0208fa34','lost-command-drained-position','send->out102=command->after20','send->out102=0',1,selected('0208fa34')),
      ('0208fa34','lost-cached-send-wakeup','native_fn_02006924(send->waiting104)','native_fn_02006924(socket->send68->waiting104)',1,selected('0208fa34',mode=0,state=4,mutate=True)),
      ('0208fa34','wrong-timeout-return','copied=-76','copied=-75',2,selected('0208fa34',mode=0,state=0))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Two complete ordinary-C main Thumb write-command/loop callers528B genuinely MW-link full configured bodies/literals, unchanged original relocations, static original canonical ARM/Thumb namespaces and exact original odd callback literal0x0208fa35. Frozen base C99 profile/old parser/normalizer/verifiers unchanged; no ASM, binary/object/register/instruction patch or compiler alias.',
      '1148 independent fixture pairs require2296 actual returning original/source callers, GPR/CPSR, exact minimum ABI/frame/SP/writes/field guards, full8MiB RAM and ordered providers. Imported allocator/copy/command/CPS/OS bodies execute0 and receive0 extra credit, including the selected callback when modeled only as the constructor-imported function pointer.',
      'The280B constructor has352 bounded fixtures for all raw mode samples plus focused TCP/UDP/SSL modes, low-bit block flag, null allocation-33, wrap/equal/nonwrap ring segments, second-before-first payload copy, signed32 lengths and seven incoming/outgoing words. It reads fresh send ring/flags after factory, caches borrowed send across socket mutation, captures ring input after copies, chooses fresh peer/local/executor fields, mirrors ephemeral local port and restores saved16-bit input on any enqueue error.',
      'The248B loop has796 bounded fixtures covering TCP connected/disconnected, optional bind and post-bind mode changes, cached send buffer/offset across optimum-buffer provider mutation, finite0..2 copy/write streams, signed negative/zero/positive returns, byte counts, current TCP failure classification, two volatile16-bit state stores and CPS-close boundary, fresh packet drained position and cached send wakeup. Original infinite streams and actual network/thread progress remain unproven.',
      'Private views are CPS100 first socket member/socket128,send272,write packet44 with word32/pointer32,16-bit ring indices/ports/position and signed32 segment lengths. These are minimum measured/public-corresponding source contexts, not complete original allocations/declarations or new external data/storage credit.',
      'Actual original callback load/addend/word/origin, canonical even Thumb entry, fresh caller.bin full SHA/literal, linked STT_FUNC/$t/zero target output and relocatable STT_FUNC/$t/SHT_NOBITS zero-code anchors are proved.158 native body/namespace/relocation negatives,five bad encoded-callable proofs,four layout failures,275 signed/width ABI+3badABI and28 genuinely linked wrong-C/header cases reject. No actual original callback bodies execute within constructor fixtures; selected248B credit comes only from its independent full top-level reconstruction.',
      'Immutable public write/CPS/header/type/thread queue references are comparison-only actual inputs, never production headers or exact native SDK revision proof. Closed original/copied producer and canonical replays must all pass before READY; aborted negative protocol runs do not count as returning callers.',
      'Pending528B remains0 accepted source credit until serialized coordinator acceptance. Combined45/4482B sealed from105/12396B claim leaves60/7914B reserved/uncredited, preserving all earlier READY/source/header/helper/native/reference pins and bounded drafts. No full network/game/Windows/Android/platform execution claim.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=2,canonicalMatchedBytes=528,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=2,bytes=528,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
