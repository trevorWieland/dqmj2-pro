import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_first_build import build
from wave20261105_socket_thumb_next_first_models import SPECS, fixtures
from wave20261105_socket_thumb_next_first_execution import run
from wave20261105_socket_thumb_next_first_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/first'
WORK = ROOT / 'work/w5st/first-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/first'


def mutation(name, label, old, new, count, main, selected):
    source = SOURCE / (name + '.c')
    text = source.read_text()
    if text.count(old) != count or not selected:
        raise ValueError('Bounded whole-C pagination mutation ambiguous/empty: ' + label)
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
        raise ValueError(('Whole-C pagination error not independently rejected', label, rejected, len(selected)))
    return dict(case=label, old=old, new=new, expectedOccurrences=count, rejectedCases=rejected,
                rejectedAtObservedProtocolBoundary=aborted, abortedRunsAreNotCallerReturns=True, fixtures=selected, proof=row)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned private native unit runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    for pin in inputs['files']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen pagination input changed: ' + pin['path'])
    if {format(int(row['address'], 0), '08x') for row in inputs['entries']} != set(SPECS):
        raise ValueError('Exact exclusive pagination caller identities differ')
    info, main, unused = L.measured_module('main')
    rows, traces = [], []
    for item in inputs['entries']:
        name = format(int(item['address'], 0), '08x')
        row, body = build(ROOT / item['source'], WORK / name / 'positive')
        if (row['targetSha256'], row['bytes']) != (item['targetSha256'], item['bytes']):
            raise ValueError('Full native pagination caller target differs')
        start = int(row['address'], 0) - 0x02000000
        native = main[start:start + row['bytes']]
        for ordinal, fixture in enumerate(fixtures(name)):
            original = run(row, native, fixture, main, ordinal)
            rebuilt = run(row, body, fixture, main, ordinal)
            if original != rebuilt or original['modelFailures'] or not original['actualTopReturn']:
                write_json(LANE / 'fixture-failure.json', dict(address=row['address'], fixture=fixture, original=original, rebuilt=rebuilt))
                raise ValueError(('Independent pagination protocol/full state differs', name, ordinal, original['modelFailures']))
            traces.append(dict(address=row['address'], ordinal=ordinal, fixture=fixture, result=original))
        rows.append(row)
        print('proved', row['address'], row['bytes'], len(fixtures(name)), flush=True)
    def selected(name,limit=8,**fields):
        return [f for f in fixtures(name) if all(f.get(k)==v for k,v in fields.items())][:limit]
    cases=[
      ('0208d0e0','wrong-sequence-step','++socket->sequence24;','socket->sequence24+=2;',3,selected('0208d0e0',state=4,present=True,mutate=False)),
      ('0208d0e0','wrong-terminal-state','socket->state8=9','socket->state8=8',1,selected('0208d0e0',state=7,present=True,mutate=False)),
      ('0208d0e0','lost-second-lookup-word','native_fn_0208cb1c(first,second)','native_fn_0208cb1c(first,third)',1,selected('0208d0e0',state=4,present=True,mutate=False)),
      ('0208d154','wrong-kind-zero-guard','socket->kind4==1 || socket->kind4==2','socket->kind4<=2',1,selected('0208d154',kind=0,present=True,mutate=False)),
      ('0208d764','wrong-reset-field','socket->word44=0','socket->word38=0',1,selected('0208d764',present=True)),
      ('0208d780','wrong-loopback-word','0x7f000001','0x7f000002',1,selected('0208d780',address=0x7f000001,present=True,mutate=False)),
      ('0208d780','wrong-remote-duplicate','socket->remote18=socket->remote1A','socket->remote18=0',1,selected('0208d780',remote=65537,present=True,mutate=False)),
      ('0208d780','wrong-auto-port-guard','if(local==0)','if(local==1)',1,selected('0208d780',local=0,present=True,mutate=False)),
      ('0208d7c0','wrong-word60-value','socket->word60=0','socket->word60=1',1,selected('0208d7c0',present=True)),
      ('0208d7e0','wrong-detach-field','socket->owner0=0','socket->kind4=0',1,selected('0208d7e0',present=True)),
      ('0208d88c','wrong-null-result','return 1;','return 0;',1,selected('0208d88c',present=False)),
      ('0208d88c','truncated-full-provider-result','return native_fn_0209280c(socket)','return (u8)native_fn_0209280c(socket)',1,selected('0208d88c',mode=1,present=True,returned=0x80000000)),
      ('0208d8b4','wrong-adjacent-state','state==4','state==5',1,selected('0208d8b4',state=4,mutate=False)),
      ('0208d8e8','dropped-zero-mode-dispatch','native_fn_0208d8b4(socket);','if(socket->mode9)native_fn_0208d8b4(socket);',1,selected('0208d8e8',mode=0,present=True,mutate=False))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    write_json(LANE / 'binding-layout-controls.json', controls(rows))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'Nine ordinary-C host-main Thumb callers totaling428B genuinely MW-link every complete original configured code/literal extent with unchanged original ELF names/relocations. The unchanged old normalizer and real linker preserve actual Thumb BL/ARM BLX mode/H bits; no helper aliases, raw patches, ASM, allocation sweep or shared changes.',
      '668 independent original/source fixture pairs require actual caller returns, full GPR/CPSR, all calls/writes and8MiB RAM equality. Null socket branches, states0/1/2/3/4/5/6/7/8/9/10/255, kinds0/1/2/3/all-ones, byte modes0/1/255, unsigned sequence wrap, port truncation/zero auto-selection,127.0.0.1 literal substitution, full-word callback returns and two lookup argument words are checked.',
      'Original208cb1c demonstrably consumes both incomingR0 andR1. Original20069f8 overwrites incomingR0 before use; its minimum observed caller view is zero-argument. Other provider signatures describe minimum observed argument/return words only; complete original C declarations are not established.',
      'Providers may mutate state/kind/owner/sequence/mode and singleton-thread selection after each observed call, and clobber caller-saved registers/flags. Cached context pointers, fresh post-provider fields, ordered increments/resets and full pre-provider region/guard snapshots are independently checked. All original provider bodies execute0 and gain0 source credit.',
      'Measured ABI views are Socket100, thread-associated168, singleton8 and address-state84, with native field widths/offsets and explicit same-programCPU/module/mode/origin proofs. All names are provisional; complete original allocations/game/socket/hardware semantics and storage authorship remain unproved/zero credit.',
      'Non-null valid thread-associated pointers are a precondition; direct208d8b4 input is non-null. Scripted provider returns/mutations include ABI counterfactuals and do not establish physical-thread/network behavior. Void returns have no invented result contract; actual registers still compare exactly.',
      'All original import/data namespace/mode/origin/addend/instruction negatives,4 native compiler layout failures,265 actual compiled Thumb byte/halfword ABI returns plus signed rejection controls, and14 genuinely linked wrong-C controls must pass. Protocol-aborted negative runs never count as caller returns.',
      'Source-complete original/copied producers and generic canonical original/copied replay required before READY. Imported helpers/data/mode anchors gain0 bytes; pending428B gets0 accepted source credit until serialized coordinator acceptance. Prior main-tail/v13/frozen packets remain unchanged.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=9,canonicalMatchedBytes=428,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=9,bytes=428,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
