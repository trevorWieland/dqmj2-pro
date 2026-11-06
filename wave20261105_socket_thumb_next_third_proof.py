import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_third_build import build
from wave20261105_socket_thumb_next_third_models import SPECS, fixtures
from wave20261105_socket_thumb_next_third_execution import run
from wave20261105_socket_thumb_next_third_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/third'
WORK = ROOT / 'work/w5st/third-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/third'


def mutation(name, label, old, new, count, main, selected):
    source = SOURCE / (name + '.c')
    text = source.read_text()
    if text.count(old) != count or not selected:
        raise ValueError('Bounded whole-C dispatch/timer mutation ambiguous/empty: ' + label)
    directory = WORK / label / 'negative'
    directory.mkdir(parents=True, exist_ok=True)
    wrong = directory / 'source.c'
    wrong.write_text(text.replace(old, new))
    shutil.copyfile(SOURCE / 'context.h', directory / 'context.h')
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
    return dict(case=label, old=old, new=new, expectedOccurrences=count, rejectedCases=rejected,
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
      ('0208d178','wrong-checksum-gate','!=0)return;','==0)return;',1,selected('0208d178',flags=16,checksum=0,mutate=False)),
      ('0208d178','wrong-header-length','0xf0)/4','0xf0)/2',1,selected('0208d178',flags=16,checksum=0,mutate=False,header=0xf5)),
      ('0208d178','wrong-flag-mask','flags13&0x17','flags13&0x13',1,selected('0208d178',flags=5,checksum=0,mutate=False)),
      ('0208d178','lost-push-guard','flags13&0x28','flags13&0x20',2,selected('0208d178',flags=10,checksum=0,mutate=False)),
      ('0208d178','wrong-syn-target','native_fn_0208cdd0(first','native_fn_0208ce58(first',1,selected('0208d178',flags=2,checksum=0,mutate=False)),
      ('0208d178','wrong-ack-target','native_fn_0208cef0(first','native_fn_0208cdd0(first',1,selected('0208d178',flags=16,checksum=0,mutate=False)),
      ('0208d178','wrong-fin-target','native_fn_0208d0e0(first','native_fn_0208cef0(first',1,selected('0208d178',flags=1,checksum=0,mutate=False)),
      ('0208d178','wrong-fallback-word','packet,bytes,0);','packet,bytes,1);',1,selected('0208d178',flags=0,checksum=0,mutate=False)),
      ('0208e53c','wrong-retry-limit','retry<4','retry<3',1,selected('0208e53c',outcome='fourth')),
      ('0208e53c','wrong-server-mode','if(mode==1)','if(mode==2)',1,selected('0208e53c',mode=1)),
      ('0208e53c','wrong-success-word','if(result==2)','if(result==1)',1,selected('0208e53c',outcome='first')),
      ('0208e53c','wrong-threshold','timer<60','timer<59',2,selected('0208e53c',mode=1,outcome='exhaust',timer=119)),
      ('0208e53c','lost-fresh-lease','(native_data_021cfcf8.lease4C*3)','(*output*3)',1,selected('0208e53c',mode=1,outcome='first',alias='out',lease=0xffffffff,mutate=False)),
      ('0208e53c','wrong-fallback-shift','lease4C>>3','lease4C>>2',1,selected('0208e53c',mode=1,outcome='exhaust',timer=119,lease=0xffffffff,mutate=False,alias='out')),
      ('0208e53c','lost-minimum-timeout','*output=1;','*output=0;',2,selected('0208e53c',mode=2,outcome='exhaust',timer=119))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Two complete ordinary-C main Thumb callers totaling326B genuinely MW-link every full configured native extent, original relocations and BL/BLX modes. Frozen compiler/base C99 profile, old normalizer/parser/validator and all previous packets remain unchanged; no helper aliases, raw patches, ASM or allocation sweep.',
      '605 independent original/source fixture pairs require1210 actual returning callers, full GPR/CPSR, provider identity/mode/argument words, writes and8MiB RAM equality. Original imported bodies execute0, with0 callee/storage/source credit outside the two selected complete caller extents.',
      'The174B dispatcher covers all256 flag bytes, all16 high data-offset nibbles, masked control-bit combinations, checksum rejection words, fresh mutated header bytes after the checksum boundary, modulo32 payload-length underflow and independently ordered provider routing. Only a14-byte packet prefix and an opaque borrowed20-byte first buffer are exposed; actual network validity, upstream parser safety and callee semantics remain unproved.',
      'The152B retry/timeout caller covers first/second/third/fourth success, four-attempt exhaustion, nonzero non-success words, modes -1/0/1/2/3,119/120/high-bit thresholds, mutable server/timer/lease fields and valid same-u32 output aliases to timer/lease. Output is stored before the freshly reloaded lease multiplication; the multiplication wraps unsigned32 before its logical shift.',
      'Fresh private Thumb compilation proves14-byte packet and84-byte address prefixes, exact byte/word offsets and519 actual unsigned byte/logical-word projection returns. Three wrong-layout, three signed-projection and15 genuinely linked wrong-C controls reject; protocol-aborted negative runs never count as returning callers.',
      'Immutable public NitroWiFi cps.h comparison text, manifest and actual100-byte CPSSoc layout/all25field/state checks are pinned and compiled separately. Public ABI correspondence is reference-consistent evidence, not proof of exact library version, original routine names, full original declarations or storage ownership. Production units remain closed private C/header inputs.',
      'Complete local compiler/linker/DLL/Python/native/reference inputs, original/copied producers and generic canonical original/copied replay are required before READY. Pending326B source credit stays0 until serialized acceptance; prior first/second/main-tail/v13 paths remain immutable.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=2,canonicalMatchedBytes=326,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=2,bytes=326,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
