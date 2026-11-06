import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_ninth_build import build
from wave20261105_socket_thumb_next_ninth_models import SPECS, fixtures, scenario
from wave20261105_socket_thumb_next_ninth_execution import run
from wave20261105_socket_thumb_next_ninth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/ninth'
WORK = ROOT / 'work/w5st/ninth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/ninth'


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
      ('0208f0a0','wrong-empty-command-error','return -33;','return -32;',1,selected('0208f0a0',allocated=False)),
      ('0208f0a0','wrong-original-callback','native_fn_0208ebd8(native_fn_0208f0e8,','native_fn_0208ebd8(native_fn_0208f234,',1,selected('0208f0a0',allocated=True)),
      ('0208f0a0','lost-signed-block-word','socket,socket->block72','socket,(u8)socket->block72',1,selected('0208f0a0',block=128)),
      ('0208f0a0','wrong-local-port','local10=socket->local74','local10=socket->remote76',1,selected('0208f0a0',allocated=True,mutate=False,predicate=lambda f,p:f['local']!=f['remote'])),
      ('0208f0a0','lost-peer-IP','peer14=socket->peer78','peer14=0',1,selected('0208f0a0',allocated=True,predicate=lambda f,p:f['ip']!=0)),
      ('0208f0a0','wrong-connecting-bit','state70|=2','state70|=4',1,selected('0208f0a0',allocated=True,mutate=False,predicate=lambda f,p:f['state']&6==0)),
      ('0208f0a0','lost-full-result','return result;','return (u8)result;',1,selected('0208f0a0',allocated=True,returned=0x80000000)),
      ('0208f0e8','wrong-lock-object','native_fn_0200708c(receive->mutexE0)','native_fn_0200708c(socket)',1,selected('0208f0e8')),
      ('0208f0e8','lost-cached-receive','receive->consumedF8=0;','socket->recv64->consumedF8=0;',1,selected('0208f0e8',mutate=True)),
      ('0208f0e8','lost-fresh-command-port','native_fn_0208d780(command->local10,','native_fn_0208d780(socket->local74,',1,selected('0208f0e8',mutate=True)),
      ('0208f0e8','wrong-TCP-mode','command->modeC==0 ||','command->modeC==1 ||',1,selected('0208f0e8',mode=0,mutate=False)),
      ('0208f0e8','lost-consumed-reset','receive->consumedF8=0;','receive->consumedF8=1;',1,selected('0208f0e8')),
      ('0208f0e8','lost-unlock','native_fn_02007110(receive->mutexE0)','native_fn_0200708c(receive->mutexE0)',1,selected('0208f0e8')),
      ('0208f0e8','lost-cached-socket','socket->state70|=','command->socket4->state70|=',2,selected('0208f0e8',mutate=True)),
      ('0208f0e8','wrong-error-flag','state70|=0x40','state70|=0x80',1,selected('0208f0e8',mode=0,mutate=False,returned=1,state=0)),
      ('0208f0e8','wrong-connected-flag','state70|=4','state70|=2',1,selected('0208f0e8',mode=0,mutate=False,returned=0,state=0)),
      ('0208f0e8','wrong-timeout-error','return -76;','return -75;',1,selected('0208f0e8',mode=0,mutate=False,returned=1))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Two complete ordinary-C main Thumb bind callers170B genuinely MW-link every full configured original extent, original relocations, BL/BLX modes and encoded callable literal. Frozen base C99 profile/old parser/normalizer/verifier and earlier packets remain unchanged; no ordinary-logic ASM/raw/register/instruction patches or helper aliases.',
      '632 independent original/source fixture pairs require1264 actual returning callers, full GPR/CPSR, ordered provider words/modes/SP, writes and8MiB RAM equality. All original imported/callback bodies execute0 within caller fixtures and receive0 extra source credit. The98B callback is credited only through its own separate full selected top-level proof.',
      'The72B caller passes the exact original odd Thumb pointer0x0208f0e9, cached socket and signed-extended block byte to its factory; allocation failure returns measured-33. After factory mutation it reads fresh ports/IP/state, writes24B bind fields/16-bit connecting state, and returns full command result. All256 raw block bytes, null allocations and controlled mutable boundaries are covered.',
      'The98B callback caches its socket/receive view before lock, reads fresh command fields after lock, resets cached receive consumed248, rechecks signed mode after bind, caches connect result through unlock, then updates the cached socket16-bit state from fresh data. All256 mode bytes, TCP/SSL/non-TCP/negative modes, full-word results, high16 state and socket/receive/command mutations are bounded fixtures.',
      'Original literal proof checks type2/addend0/origin68/raw odd word, canonical even Thumb entry and original inventory/record. Actual linked caller.bin bytes/hash preserve0x0208f0e9; actual linked ELF has even-valued zero-size STT_FUNC+$t and zero-size target output section. Actual relocatable mode probe is STT_FUNC+$t/SHT_NOBITS with0initialized code/callee credit. No callback tag/word/object/instruction is patched.',
      'Eighty-four namespace/original-evidence negatives, five wrong encoded-callable metadata proofs, three actual layout failures,275 signed/width ABI returns plus3badABI and17 genuinely linked wrong-C/header errors reject. Aborted negatives never count as returning callers. Private prefixes remain socket128,receive264,bind24,opaque mutex bytes224..247; all storage receives0credit.',
      'Immutable public bind/poll/header/primitive-type references are comparison inputs, not production includes or proof of exact native SDK version/full original declarations/allocations, allocator/mutex/network/OS/game/platform semantics. Production C/header and private runtime/native/reference pins must replay independently.',
      'Original/copied producers and generic original/copied canonical replay must pass before READY. Pending170B stays0 source credit until serialized acceptance, coordinator161or later. Combined33/2686B leaves72/9710B reserved/uncredited in105/12396B claim; all earlier packets stay frozen and unmatched212/468/288B drafts remain excluded.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=2,canonicalMatchedBytes=170,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=2,bytes=170,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
