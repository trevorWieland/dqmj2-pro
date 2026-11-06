import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_eighteenth_build import build
from wave20261105_socket_thumb_next_eighteenth_models import SPECS, fixtures, scenario
from wave20261105_socket_thumb_next_eighteenth_execution import run
from wave20261105_socket_thumb_next_eighteenth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/eighteenth'
WORK = ROOT / 'work/w5st/eighteenth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/eighteenth'


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
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/eighteenth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/eighteenth' or WORK!=ROOT/'work/w5st/eighteenth-proof':raise ValueError('New tenth source/evidence/work scope changed')
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
    from wave20261105_socket_thumb_next_eighteenth_negatives import cases
    cases=cases()
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Seventeen complete ordinary-C ARM9-main Thumb lifecycle/list/SOC adapter/startup callers1190B genuinely MW-link exact full original measured bodies/literals/relocations using unchanged base C99/file-IPA profile/parser/normalizer/verifiers. No algorithm ASM, binary/object/register/instruction patch or compiler aliases.',
      'Independent finite original/source caller fixtures require ordered typed imports, all observed argument words, exact measured SP frames, actual caller returns and full GPR/CPSR/write/8MiB equality. All original imported CPS/OS/network/allocator/list and other selected caller bodies execute0 in caller fixtures and receive0 extra credit. No full game/platform/network/Windows/Android execution.',
      'Cleanup waits are bounded0..2 and list fixtures0..3 sockets. Provider changes distinguish cached versus fresh observed config/list/state/UDP handles; no arbitrary-list convergence or original scheduler/allocator semantics are claimed. Signed handles/results, nullable APIs, aliased DNS inputs, zero/nonzero endian values, caller stack output addresses and all minimum field widths are checked.',
      'SOC startup minimum config52B and wrapper120B/config56B alias at+64 are observed private layouts; original BSS is fixture modeled as one guarded240B region covering declared observed slots, not an authored storage extent. Five IP words, exact DHCP flag==1, callback words, raw alloc/free slots, command maximum64 and full32-bit MTU/window writes are checked. All storage/initialized data credit0.',
      'Three original indirect sites prove release1word/void, named allocator2words/pointer and named release3words/void.30 separate fresh ARM/Thumb provider returns,21 wrong-site controls,4 rejected actual callable declarations and6 actual wrong-runtime-tag controls qualify only fixture interfaces; original callback identities/general allocator semantics0.',
      'Three actual odd literal words bind canonical even Thumb entries0208ef98/02090608/02090624 with STT_FUNC+$t and zero initialized mode-only probes.15 callable-proof negatives,611 full namespace/body/origin/binding negatives,5 compiler-layout negatives,275 fresh signed/width ABI returns+3 badABI and39 genuinely linked wrong-C controls are required. Aborted negative runs are not positive returns.',
      'Public immutable NitroWiFi SOC/list/cleanup/header and SDK type references are comparison inputs, not proof of the exact original library revision, complete original types or behavior. No public production headers/system inputs are implicit. All closed actual original/copied producer/canonical replays required before READY.',
      'Pending1190B remains0 accepted credit until coordinator162or later; combined70/6448B sealed from105/12396B claim leaves35/5948B reserved/uncredited. Every prior READY/source/helper/header/reference input remains frozen; prior bounded partial drafts excluded.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=17,canonicalMatchedBytes=1190,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,nativeCalleeBodiesExecutedInCallerFixtures=0,distinctOriginalHelperBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=17,bytes=1190,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
