import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_fifth_build import build
from wave20261105_socket_thumb_next_fifth_models import SPECS, fixtures
from wave20261105_socket_thumb_next_fifth_execution import run
from wave20261105_socket_thumb_next_fifth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/fifth'
WORK = ROOT / 'work/w5st/fifth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/fifth'


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
    def selected(name,limit=8,**fields):
        return [f for f in fixtures(name) if all(f.get(k)==v for k,v in fields.items())][:limit]
    cases=[
      ('0208d71c','wrong-high-word-shift','next_value()>>32','next_value()>>31',1,selected('0208d71c',seed=0,multiplier=0,increment=0x8000000000000000,mutate=False)),
      ('0208d71c','lost-state-update','seed68=value;','seed68=0;',1,selected('0208d71c',increment=1,mutate=True)),
      ('0208d71c','lost-increment-high-word','+native_data_021cfcf8.increment78','+(u32)native_data_021cfcf8.increment78',1,selected('0208d71c',increment=0x8000000000000000)),
      ('0208e7f8','lost-initial-end','*end=text;','*end=text+1;',1,selected('0208e7f8',text='00')),
      ('0208e7f8','wrong-digit-upper-bound','digit>9','digit>8',1,selected('0208e7f8',text='39')),
      ('0208e7f8','wrong-digit-origin','*text-48','*text-49',1,selected('0208e7f8',text='30')),
      ('0208e7f8','wrong-decimal-scale','value*10','value*9',1,selected('0208e7f8',text=b'12345x'.hex())),
      ('0208e7f8','lost-end-progress','*end=++text;','++text;',1,selected('0208e7f8',text=b'12345x'.hex())),
      ('0208e820','lost-nondigit-guard','if(text==end)','if(text!=end)',1,selected('0208e820',text=b'.1.2.3'.hex())),
      ('0208e820','wrong-octet-upper-bound','value>255','value>256',1,selected('0208e820',text=b'1.2.3.256'.hex())),
      ('0208e820','wrong-separator','*text++!=46','*text++!=47',1,selected('0208e820',text=b'1.2.3.4'.hex())),
      ('0208e820','wrong-part-count','part<4','part<3',1,selected('0208e820',text=b'1.2.3.4'.hex())),
      ('0208e820','wrong-octet-shift','address<<=8','address<<=7',1,selected('0208e820',text=b'1.2.3.4'.hex())),
      ('0208e820','wrong-trailing-nul','*text!=0','*text==0',1,selected('0208e820',text=b'1.2.3.4'.hex())),
      ('0208e878','wrong-server-null-gate','if(!server)','if(server)',1,selected('0208e878',server=1)),
      ('0208e878','wrong-query-type','name,1,transaction','name,2,transaction',1,selected('0208e878',server=1)),
      ('0208e878','wrong-fifth-stack-word','transaction,0,0','transaction,0,1',1,selected('0208e878',server=1)),
      ('0208e878','lost-captured-result','return result;','return 0;',1,selected('0208e878',server=1,returned=0x80000000))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Four complete ordinary-C main Thumb callers232B genuinely MW-link every full configured native extent, relocations, original BL/BLX and target modes. Frozen base C99 compiler/profile, old parser/normalizer/verifier and earlier packets remain unchanged; no raw/ASM/register/instruction patches or helper aliases.',
      '811 independent original/source fixture pairs require1622 actual returning callers, full GPR/CPSR, ordered direct-provider arguments/modes, actual fifth stack word and SP, writes and8MiB RAM equality. Caller fixtures intercept all original imported bodies; separate ABI qualification executes49 bounded returns from the one original32B ARM multiply primitive with0 primitive source credit.',
      'The40B caller consumes two64-bit operands through four argument registers, preserves unsigned64 carry/wrap, reloads increment after a scripted provider boundary, writes the64-bit seed and returns its upper32 bits. Three hundred caller fixtures vary full64-bit seed/multiplier/increment and controlled counterfactual provider mutations; actual game concurrent mutation is not claimed.',
      'The38B prefix parser covers all256 input bytes, digit/end-pointer handling, long decimal overflow wrapping modulo32 and bounded terminators. The88B four-part caller includes high-byte/nondigit/separator/trailing-NUL/255/256 cases and faithfully preserves the measured decimal overflow acceptance behavior; no stricter IP-validity rule is invented.',
      'The66B wrapper checks zero server, caches all borrowed inputs/results across named providers, forwards a genuine fifth stack argument0 and preserves full returned words. Transaction fixtures are well-formed unsigned16 argument words; actual original provider declarations remain minimum observed interfaces.',
      'Ninety-six strict namespace/original-evidence negatives, four actual64-bit layout failures,56 fresh compiled carry/range ABI returns plus2negativeABI and18 genuinely linked wrong-C/header errors reject. Protocol-aborted negatives never count as caller returns. Exact128B address-prefix storage itself receives0 credit.',
      'New immutable public math/rand.h and manifest are explicitly comparison inputs, with no production include or upstream SDK header-closure/version/name claim. The212B resolver draft is excluded/parked and gets0 credit; bounded source/context work reached212 compiled bytes but did not close induction setup/order.',
      'Complete private C/header/compiler/linker/runtime/native/public-reference inputs, original/copied producer and generic canonical original/copied replay must pass before READY. Pending232B credit stays0 until serialized acceptance; combined22/1748B leaves83/10648B reserved/uncredited in105/12396B claim, coordinator160or later.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=4,canonicalMatchedBytes=232,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=49,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=1,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=4,bytes=232,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
