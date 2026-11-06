import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_eleventh_build import build
from wave20261105_socket_thumb_next_eleventh_models import SPECS, fixtures, scenario
from wave20261105_socket_thumb_next_eleventh_execution import run
from wave20261105_socket_thumb_next_eleventh_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/eleventh-qualified'
WORK = ROOT / 'work/w5st/eleventh-qualified-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/eleventh'


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
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/eleventh-qualified' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/eleventh' or WORK!=ROOT/'work/w5st/eleventh-qualified-proof':raise ValueError('New eleventh source/evidence/work scope changed')
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
      ('0208f404','wrong-read-callback','native_fn_0208ebd8(native_fn_0208f430,','native_fn_0208ebd8(native_fn_0208f540,',1,selected('0208f404')),
      ('0208f404','wrong-read-block-flag','native_fn_0208f430,socket,1','native_fn_0208f430,socket,0',1,selected('0208f404')),
      ('0208f404','lost-read-length-word','length14=bufferLength','length14=(u16)bufferLength',1,selected('0208f404',limit=0x7fffffff)),
      ('0208f404','wrong-read-IP-output','peer1C=remoteIp','peer1C=(u32 *)remotePort',1,selected('0208f404',port=0x02406000,ip=0x02406004)),
      ('0208f404','lost-cached-read-socket','native_fn_0208eca4(socket,command)','native_fn_0208eca4(command->socket4,command)',1,selected('0208f404',mutate=True)),
      ('0208f404','lost-full-read-result','return result;','return (u8)result;',1,selected('0208f404',returned=0x80000000)),
      ('0208f508','wrong-minimum-tie','consumedF8<(s32)receive->minFC','consumedF8<=(s32)receive->minFC',1,selected('0208f508',consumed=65535,minimum=65535)),
      ('0208f508','lost-signed-consumed','receive->consumedF8<(s32)','(u32)receive->consumedF8<(s32)',1,selected('0208f508',consumed=0x80000000,minimum=16)),
      ('0208f508','wrong-consume-callback','native_fn_0208ebd8(native_fn_0208f540,','native_fn_0208ebd8(native_fn_0208f430,',1,selected('0208f508',consumed=65535,minimum=16)),
      ('0208f508','wrong-consume-block-flag','native_fn_0208f540,socket,0','native_fn_0208f540,socket,1',1,selected('0208f508',consumed=65535,minimum=16)),
      ('0208f508','wrong-empty-consume-command-error','return -33;','return -32;',1,selected('0208f508',consumed=65535,minimum=16,allocated=False)),
      ('0208f508','lost-cached-consume-socket','native_fn_0208eca4(socket,command)','native_fn_0208eca4(command->socket4,command)',1,selected('0208f508',consumed=65535,minimum=16,allocated=True,mutate=True)),
      ('0208f508','lost-full-consume-result','return result;','return (u8)result;',1,selected('0208f508',consumed=65535,minimum=16,allocated=True,returned=0x80000000))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Two complete ordinary-C main Thumb read/consume command constructors100B genuinely MW-link every full original extent, unchanged original relocation payload, canonical BL/BLX/Thumb literal namespace and exact encoded odd pointers0x0208f431/0x0208f541. No compiler/normalizer/parser/verifier change, helper alias, ASM or raw/object/register/instruction patch.',
      '560 independent original/source fixture pairs require1120 actual returning callers, GPR/CPSR, ordered provider words/modes/SP, exact field widths/writes and8MiB RAM equality. All original imported/callback bodies execute0 and receive0 extra source credit. The216B read callback is not reconstructed by this packet.',
      'The44B constructor requires the original factory to return a non-null writable minimum32B packet: release SDK assertions did not emit a null branch, so no invented error path is inserted. It snapshots buffer/length/output arguments across the factory, forwards signed32 lengths and optional pointer words, uses cached input socket despite packet/socket mutations, and returns full result.',
      'The56B constructor compares signed32 consumed248 against unsigned16 minimum252, including exact ties, all tested INT32 boundaries and minimum0/1/16/65535. Below minimum returns0 without imports; eligible factory receives original odd callback plus flag0; null allocation returns measured-33, otherwise cached socket/full result survive controlled boundary mutations.',
      'Fresh source and layout independently compile word32/pointer32, socket128,receive264,read command minimum32: offsets16/20/24/28 and signed32 length are explicit. Minimum prefix does not prove actual complete public command union/allocation/declaration; all storage0credit. Release minimum0 and nonpositive length cases are measured code counterfactuals, not normal socket-use recommendations.',
      'Original load record/raw literal, actual caller.bin full SHA/word, canonical even entry, actual linked STT_FUNC/$t and zero-size initialized target output, relocatable STT_FUNC/$t/SHT_NOBITS zero-code anchors are checked for both targets. Ten wrong encoded-callable proofs,86 namespace/body/relocation negatives,three layout failures,275 signed/width ABI returns plus3badABI and13 genuinely linked wrong-C/header cases reject.',
      'Immutable public read/header/primitive-type references are comparison context only, no production includes, native SDK-version/network/OS/command/game/platform semantics or original imported callee execution claim. Source C/header and private runtime/native inputs must pass producer/canonical replay in original and independently copied roots before READY.',
      'Pending100B stays0 accepted credit until serialized coordinator acceptance. Combined38/3128B sealed from105/12396B claim leaves67/9268B reserved/uncredited. The216B callback remains uncredited at a bounded compiler-context discrepancy; all earlier120/212/468/288B drafts remain excluded and earlier READYs/inputs stay frozen.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=2,canonicalMatchedBytes=100,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=2,bytes=100,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
