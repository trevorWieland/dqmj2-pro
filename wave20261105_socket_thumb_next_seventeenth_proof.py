import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_seventeenth_build import build
from wave20261105_socket_thumb_next_seventeenth_models import SPECS, fixtures, scenario
from wave20261105_socket_thumb_next_seventeenth_execution import run
from wave20261105_socket_thumb_next_seventeenth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/seventeenth'
WORK = ROOT / 'work/w5st/seventeenth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/seventeenth'


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
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/seventeenth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/seventeenth' or WORK!=ROOT/'work/w5st/seventeenth-proof':raise ValueError('New tenth source/evidence/work scope changed')
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
    def denominator(plan):
        return next((a['args'][1] for a in plan['actions'] if a['address']==0x02026144),None)
    cases=[
      ('0208fb2c','lost-pre-IRQ-specific-data','u32 enabled=native_fn_02007ff4();','u32 enabled=native_fn_02007ff4();soc=native_data_020e33e4.current4->specificA4;',1,selected('0208fb2c',hasSoc=True,mutate=True,predicate=lambda f,p:denominator(p) is not None and f['mss']>1 and f['window']>1)),
      ('0208fb2c','wrong-MSS-positive-check','soc->mss2E>0','soc->mss2E==0',1,selected('0208fb2c',hasSoc=True,mutate=False,mss=512,window=1,config=128)),
      ('0208fb2c','wrong-window-positive-check','soc->window2C>0','soc->window2C==0',1,selected('0208fb2c',hasSoc=True,mutate=False,mss=1,window=512,config=128)),
      ('0208fb2c','lost-window-minimum','minimum(soc->mss2E,soc->window2C)','minimum(soc->mss2E,soc->mss2E)',1,selected('0208fb2c',hasSoc=True,mutate=False,mss=512,window=1,config=128)),
      ('0208fb2c','lost-local-MSS-bound','minimum(minimum(soc->mss2E,soc->window2C),(int)native_data_021d1550.mss24)','minimum(soc->mss2E,soc->window2C)',1,selected('0208fb2c',hasSoc=True,mutate=False,mss=512,window=512,config=1)),
      ('0208fb2c','lost-doubled-fallback','temp=2*(int)native_data_021d1550.mss24','temp=(int)native_data_021d1550.mss24',2,selected('0208fb2c',hasSoc=False,config=128,mutate=False)),
      ('0208fb2c','lost-zero-SOC-fallback','else{temp=2*(int)native_data_021d1550.mss24;}','else{temp=0;}',2,selected('0208fb2c',hasSoc=False,config=128,mutate=False)),
      ('0208fb2c','lost-cached-sizing-IRQ-mask','native_fn_02008008(enabled)','native_fn_02008008(0)',1,selected('0208fb2c')),
      ('0208fb2c','lost-cached-MSS-after-restore','if(temp>0)','temp=2*(int)native_data_021d1550.mss24;if(temp>0)',1,selected('0208fb2c',mutate=True,predicate=lambda f,p:denominator(p) is not None and p['result']!=f['length'])),
      ('0208fb2c','wrong-divide-argument-order','native_fn_02026144(length,temp)','native_fn_02026144(temp,length)',1,selected('0208fb2c',predicate=lambda f,p:denominator(p) is not None and f['length']!=denominator(p))),
      ('0208fb2c','wrong-zero-quotient-boundary','if(count>0)','if(count>=0)',1,selected('0208fb2c',length=1,config=128,mutate=False,hasSoc=False)),
      ('0208fb2c','wrong-positive-quotient-boundary','if(count>0)','if(count<0)',1,selected('0208fb2c',length=0x80000000,config=65535,mutate=False,hasSoc=False)),
      ('0208fb2c','wrong-rounded-result','return temp*count;','return temp*count+1;',1,selected('0208fb2c',predicate=lambda f,p:denominator(p) is not None and f['length']==0x7fffffff)),
      ('0208fb2c','lost-full-unchanged-length','return length;','return (u16)length;',1,selected('0208fb2c',length=0x80000000))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'One complete ordinary-C main Thumb send-buffer optimum caller104B genuinely MW-links its whole original extent/literals/relocations and exact static original ARM/data/BSS namespaces under frozen base C99 flags/compiler and unchanged old parser/normalizer/verifier. No compiler helper alias, raw/object/register/instruction patch or ASM.',
      '768 independent fixture pairs require1536 actual returning original/source callers, complete GPR/CPSR/SP/frame/writes/field guards, ordered provider words/modes and whole8MiB RAM equality. Every original imported/IRQ/divide body executes0 and receives0 extra source credit. Native_fn02026144(int,int) is an explicit canonical ARM import with observed two32-bit inputs/R0 result, not an object symbol rename or compiler-binding adapter; scripted quotient/remainder do not prove callee implementation.',
      'The current specific-data SOC pointer is captured before IRQ disable. Fields and local MSS are read after disable; IRQ restore may mutate all inputs but cached temporary/length remain. Cases cover nullable SOC, unsigned16 zero/1/512/65535 windows/MSS, local MSS0/1/128/65535, signed32 INT_MIN/-1/0/1/255/INT_MAX lengths, positive/zero/negative mathematical quotient and cached rounding. Config values stay in a bounded no-signed-overflow range; arbitrary malformed TCP/config states are not claimed.',
      'Actual new primary public NitroSDK math/math.h defines MATH_IMin(int,int) as `(a <= b) ? a : b`; this exact readable inline form reproduces native argument-load scheduling. Private minimum kernel8/thread168/SOC48/config40 views assert current4/specific164/window44/MSS46/configMSS36 and word32/pointer32; BSS0x020e33e4/0x021d1550 records/literal words are strict witnesses with0 storage/full declaration/allocation credit.',
      '67 native body/namespace/relocation negatives,4 actual compiler layout failures,52 fresh unsigned-field/signed-minimum ABI returns+3badABI and14 genuinely linked wrong-C/header cases reject. Positive results model only caller boundaries, never original divide algorithm/network/OS/game/platform behavior; aborted protocol counterexamples are not returning callers.',
      'Immutable public write/math/CPS/header/type references are actual comparison inputs only, not production headers or native SDK-version proof. Closed original/copied producers and original/copied canonical replays must all pass before READY.',
      'Pending104B stays0 accepted credit until coordinator162or later. Combined53/5258B sealed from105/12396B claim leaves52/7138B reserved/uncredited, preserving every earlier READY/source/header/helper/native/reference pin and bounded draft. No original helper/native Windows/Android/full game execution claim.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=1,canonicalMatchedBytes=104,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=1,bytes=104,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
