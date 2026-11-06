import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT, configuration, sha256, write_json
import match_runtime as C
import link_runtime_unit as L
import unicorn
from wave20261105_socket_thumb_next_fourth_build import build
from wave20261105_socket_thumb_next_fourth_models import SPECS, fixtures, scenario, TARGETS
from wave20261105_socket_thumb_next_fourth_execution import run
from wave20261105_socket_thumb_next_fourth_controls import execute as controls

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/socket-thumb-next/fourth'
WORK = ROOT / 'work/w5st/fourth-proof'
SOURCE = ROOT / 'src/runtime/parallel_wave20261105/socket-thumb-next/fourth'


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
    def selected(name='0208d228',limit=6,predicate=None,needs=None,**fields):
        chosen=[]
        for i,f in enumerate(fixtures(name)):
            if not all(f.get(k)==v for k,v in fields.items()):continue
            plan=scenario(name,f,i)
            if needs is not None and not any(a['address']==needs for a in plan['actions']):continue
            if predicate is not None and not predicate(f,plan):continue
            chosen.append(f)
            if len(chosen)>=limit:break
        return chosen
    copyCall=0x02008e0c
    callback=lambda f,p:any(a['fixtureMode'] is not None for a in p['actions'])
    cases=[
      ('0208d228','wrong-checksum-gate','packet->checksum6 &&','packet->checksum6 ||',1,selected(checksum=0)),
      ('0208d228','wrong-protocol-word','packet,bytes,ip,17','packet,bytes,ip,6',1,selected(checksum=1)),
      ('0208d228','wrong-datagram-state','state8!=10','state8!=11',1,selected(needs=copyCall)),
      ('0208d228','wrong-local-port','localA!=host16(packet->destination2)','localA!=host16(packet->source0)',1,selected(needs=copyCall,predicate=lambda f,p:f['sourcePort']!=f['destinationPort'])),
      ('0208d228','lost-bound-remote-port','socket->remote18 &&','socket->remote18==0 &&',1,selected(route=3,skip=4,predicate=lambda f,p:any(a['address']==0x02008008 for a in p['actions']))),
      ('0208d228','wrong-broadcast-word','address1C!=0xffffffff','address1C!=0xfffffffe',1,selected(peer='broadcast',needs=copyCall)),
      ('0208d228','wrong-local-IP','localIP14=host32(ip->destination10)','localIP14=host32(ip->sourceC)',1,selected(needs=copyCall)),
      ('0208d228','wrong-bind-IP','address1C=host32(ip->sourceC)','address1C=host32(ip->destination10)',1,selected(peer='unbound',needs=copyCall)),
      ('0208d228','lost-occupied-guard','if(socket->size44)break;','if(!socket->size44)break;',1,selected(needs=copyCall)),
      ('0208d228','wrong-capacity-bound','if(bytes>socket->capacity3C)','if(bytes<socket->capacity3C)',1,selected(needs=copyCall,predicate=lambda f,p:((f['length']-8)&0xffffffff)!=f['capacity'])),
      ('0208d228','wrong-payload-start','native_fn_02008e0c(packet+1','native_fn_02008e0c(packet',1,selected(needs=copyCall)),
      ('0208d228','wrong-wake-kind','socket->kind4==3','socket->kind4==2',1,selected(needs=0x0200698c)),
      ('0208d228','lost-fresh-owner','native_fn_0200698c(socket->owner0)','native_fn_0200698c(thread)',1,selected(route=1,mutate=True,needs=0x0200698c)),
      ('0208d228','wrong-callback-return','socket->size44,socket))socket->size44=0;','socket->size44,socket)==0)socket->size44=0;',1,selected(mutate=True,predicate=callback)),
      ('0208d228','lost-fresh-callback-length','callback38(socket->buffer40,socket->size44,socket)','callback38(socket->buffer40,socket->capacity3C,socket)',1,selected(mutate=True,predicate=lambda f,p:callback(f,p) and any(a['fixtureMode'] is not None and a['args'][1]!=f['capacity'] for a in p['actions'])))]
    negatives=[mutation(name,label,old,new,n,main,chosen) for name,label,old,new,n,chosen in cases]
    geometry=controls(rows)
    tagged=[]
    for mode,target in TARGETS.items():
        chosen=selected(needs=target)
        if not chosen:raise ValueError('Missing actual scripted callback fixture')
        fixture=dict(chosen[0],wrongCallbackTag=True)
        row=rows[0];start=int(row['address'],0)-0x02000000;native=main[start:start+row['bytes']]
        result=run(row,native,fixture,main,0)
        if result['actualTopReturn'] or not result['modelFailures']:raise ValueError('Wrong original runtime callback mode tag admitted')
        tagged.append(dict(case=mode+'-wrong-tag',fixture=fixture,rejected=True,result=result,sourceCredit=0))
    geometry['wrongRuntimeCallbackTags']=tagged
    write_json(LANE / 'binding-layout-controls.json', geometry)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    limits=[
      'One complete ordinary-C main Thumb caller336B genuinely MW-links its full original configured extent, relocations, BL/BLX modes and data literal. Frozen base C99 profile/old normalizer/parser/validator and all earlier packets remain unchanged; no aliases, raw patches, ASM or allocation sweep.',
      '480 independent original/source fixture pairs require960 actual returning callers, full GPR/CPSR, ordered provider identity/mode/argument words, writes and8MiB RAM equality. Original game/imported/callback bodies execute0 and get0 source credit; all storage/prefix/provider bytes get0 source credit.',
      'Fixtures cover empty/three-node/null-socket/ownerless/wrong-state/port/peer lists, first/second/third/no matching contexts, IPv4 endian reads, unbound/broadcast/exact peers, occupied buffers, bounded0/4/8capacity, raw4/8/12/40length words, wait-kind wakeups, mutable copy-boundary owner/size/buffer/callback fields and ARM/Thumb callbacks returning0/all-ones.',
      'Original callback-site proof checks loaded socket field56, null test, buffer64/length68/socket argument flow, actual BLX-register instruction, word return test and count-clear store. No original fixed target is encoded or inferred; controlled freshly compiled typed ARM/Thumb fixture providers qualify only their own test-mode/three-word ABI, with20 separate fresh-test returns and0 original game provider-body execution.',
      'The runtime model intercepts named/static and separately labeled controlled-fixture callbacks before their bodies. Twelve wrong original-site contracts, two wrong callable declarations, two wrong runtime mode tags, four actual layout failures,17 byte-order ABI returns plus2negativeABI,72namespace/original-evidence negatives and15 genuinely linked wrong-C errors reject. Aborted negatives never count as returning callers.',
      'Borrowed source views are100-byte socket,168-byte thread with next104/socket164,12-byte singleton with list8,20-byte IPv4 prefix,8-byte datagram header and32-byte buffers. Raw underlength arithmetic is a bounded caller-word counterfactual; actual network validity, memory/thread/hardware behavior, original callback registrations and complete original allocations/declarations remain unproved.',
      'Immutable public NitroWiFi100B CPSSoc/all25fields/state ABI comparison is independently compiled and pinned; exact native version/name correspondence remains unproved and the public text is not a production compiler include. Closed private C/header source, full local runtime/reference pins and original/copied producer/generic canonical replays are required before READY.',
      'Pending336B source credit stays0 until serialized acceptance, coordinator160or later. First/second/third17/1180B packets remain immutable; combined18/1516B leaves87/10880B reserved/uncredited in the105/12396B claim.']
    write_json(LANE / 'match.json', dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',program='',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=1,canonicalMatchedBytes=336,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=1,bytes=336,cases=len(traces)),flush=True)


if __name__ == '__main__':
    execute()
