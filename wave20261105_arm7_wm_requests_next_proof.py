import gzip
import json
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import match_runtime as C
import unicorn
from wave20261102_host_arm7_sixth_slice import functions
from wave20261105_arm7_wm_requests_next_build import SOURCE,LANE,WORK,build_all
from wave20261105_arm7_wm_requests_next_models import fixtures
from wave20261105_arm7_wm_requests_next_execution import run
from wave20261105_arm7_wm_requests_next_controls import execute as controls


def negative_cases():
    allFixtures=fixtures()
    def choose(entry,**fields):return [f for f in allFixtures if f['entry']==entry and all(f.get(k)==v for k,v in fields.items())][:3]
    return [
      (0x027e609c,'status->valarm_queuedFlag == 1','status->valarm_queuedFlag != 1',choose(0x027e609c,flag=1)),
      (0x027e609c,'buf[0] = WM_APIID_VALARM_MP','buf[0] = WM_APIID_VALARM_MP+1',choose(0x027e609c,flag=0,allocated=True)),
      (0x027e609c,'cb->reason = WM_APIID_VALARM_MP','cb->reason = WM_APIID_VALARM_MP+1',choose(0x027e609c,flag=0,allocated=False,wm7=True)),
      (0x027e614c,'status->minRssi = 4','status->minRssi = 5',choose(0x027e614c,rssi=1,minRssi=65535)),
      (0x027e614c,'status->sendQueueInUse == 1','status->sendQueueInUse != 1',choose(0x027e614c,state=10,use=1)),
      (0x027e614c,'status->mp_count = 256','status->mp_count = 255',choose(0x027e614c,state=9,child=3,count=255,freq=10)),
      (0x027e7d58,'auth_retry < 2','auth_retry < 1',[f for f in allFixtures if f['kind']=='deauth' and f['codes']==[7,0]]),
      (0x027e7d58,'case 0x0C :','case 0x0D :',[f for f in allFixtures if f['kind']=='deauth' and f['codes']==[12,0]]),
      (0x027e7cc8,'(u16)(buf[1])','(u16)(buf[0])',choose(0x027e7cc8,value=0)),
      (0x027e7cc8,'(u16)(16 + status->pparam.userGameInfoLength)','(u16)(15 + status->pparam.userGameInfoLength)',choose(0x027e7cc8)),
      (0x027e8320,'status->state != WM_STATE_IDLE','status->state == WM_STATE_IDLE',choose(0x027e8320,state=2)),
      (0x027e8320,'status->state = WM_STATE_STOP','status->state = WM_STATE_IDLE',choose(0x027e8320,state=2,code=0)),
      (0x027e83cc,'cb->mask = param->mask','cb->mask = param->mask+1',choose(0x027e83cc)),
      (0x027e83cc,'sizeof(cb->oldParam)','sizeof(cb->oldParam)-1',choose(0x027e83cc)),
      (0x027e8110,'(u16)(enableChannel >> 1)','(u16)(enableChannel >> 0)',choose(0x027e8110,fail=-1,channel=0x3ffe)),
      (0x027e8110,'(u64)(40 * 100)','(u64)(40 * 10)',choose(0x027e8110,fail=-1)),
      (0x027e87d8,'powerSave == 1','powerSave != 0',choose(0x027e87d8,state=11,power=2)),
      (0x027e87d8,'callback->wlCmdID = (0x0100 | 0x00)','callback->wlCmdID = (0x0100 | 0x01)',choose(0x027e87d8,state=11,fail=1))]


def wrong_c(case,ordinal,images):
    entry,old,new,selected=case;function='native_host_arm7_main_'+format(entry,'08x') if isinstance(entry,int) else entry;directory=WORK/'wrong-c'/str(ordinal)
    if not selected:raise ValueError('Meaningful wrong-C fixture selection empty')
    directory.mkdir(parents=True,exist_ok=True)
    sourceDir=SOURCE/format(entry,'08x');directory=directory/format(entry,'08x');directory.mkdir(parents=True,exist_ok=True)
    for p in sourceDir.iterdir():
        if p.is_file():(directory/p.name).write_bytes(p.read_bytes())
    found=[]
    for path in directory.iterdir():
        if path.suffix not in ['.c','.h']:continue
        text=path.read_text()
        for f in functions(text):
            if f['name']==function:found.append((path,text,f))
    if len(found)!=1:raise ValueError('Wrong-C target function is not unique')
    path,text,fragment=found[0];start,end=fragment['start'],fragment['end'];part=text[start:end]
    if part.count(old)!=1:raise ValueError(('Meaningful ordinary-C mutation ambiguous',function,old,part.count(old)))
    path.write_text(text[:start]+part.replace(old,new)+text[end:]);affected={'native_host_arm7_main_'+format(f['entry'],'08x') for f in selected};rows,outputs=build_all(directory/'build',{next(iter(affected)):directory/'main.c'},affected,affected);by={int(r['address'],0):r for r in rows};reject=[]
    for n,f in enumerate(selected):
        row=by[f['entry']]
        try:
            result=run(row,outputs[row['name']],f,images,n)
            if not result['modelFailures']:raise ValueError(('Wrong-C failed to alter independently modeled behavior',function,old,n))
            reject.append(dict(ordinal=n,actualTopReturn=result['actualTopReturn'],modelFailures=result['modelFailures']))
        except unicorn.UcError as error:reject.append(dict(ordinal=n,actualTopReturn=False,rejectedAtMemoryBoundary=True,error=str(error)))
    return dict(case=ordinal,function=function,old=old,new=new,genuinelyLinkedWrongC=rows,fixtures=selected,rejected=reject,abortedRunsAreNotCallerReturns=True)


def execute():
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261105/arm7-wm-requests-next' or LANE!=ROOT/'evidence/lanes/parallel-wave20261105/arm7-wm-requests-next' or WORK!=ROOT/'work/w5wr':raise ValueError('New WM port proof source/evidence/work scope changed')
    if unicorn.__version__!='2.1.4':raise ValueError('Pinned actual native unit runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for p in inputs['files']:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Frozen actual WM port compiler/source/native/runtime input changed: '+p['path'])
    rows,outputs=build_all(WORK/'proof-positive');by={int(r['address'],0):r for r in rows};images=[(int(m['base'],0),(ROOT/m['binary']).read_bytes()) for m in read_json(ROOT/'evidence/arm7/runtime-layout.json')['modules']];traces=[];coverage={r['address']:set() for r in rows}
    for n,f in enumerate(fixtures()):
        row=by[f['entry']];image=(ROOT/row['binary']).read_bytes();native=image[f['entry']-row['base']:f['entry']-row['base']+row['bytes']];original=run(row,native,f,images,n);rebuilt=run(row,outputs[row['name']],f,images,n)
        if original!=rebuilt or original['modelFailures'] or not original['actualTopReturn']:
            write_json(WORK/'fixture-failure.json',dict(ordinal=n,fixture=f,original=original,rebuilt=rebuilt));raise ValueError('Independent complete WM port caller/model mismatch')
        coverage[row['address']].update(a for a in original['pcs'] if f['entry']<=a<f['entry']+row['bytes']);traces.append(dict(ordinal=n,fixture=f,result=original))
    print(dict(positiveNativeSourcePairs=len(traces),functions=len(rows),bytes=sum(r['bytes'] for r in rows)),flush=True);negative=[wrong_c(case,n,images) for n,case in enumerate(negative_cases())];controlled=controls(rows);write_json(LANE/'controls.json',controlled);raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));covered=[dict(address=address,originalInstructionBytes=4*len(pcs),completeNativeSpanBytes=by[int(address,0)]['bytes']) for address,pcs in coverage.items()]
    limits=[
      'Eight complete admitted host ARM7-main ARMv4T functions:2084 whole bytes=2016 reached instruction+68 actual literal bytes. All63 original ELF relocations/addends genuinely link under measured2.0/base O4,s/on,noauto/file-IPA/C99. Eight readable owned C files+16 closed bounded headers contain no comments/algorithm ASM/object/binary/register/instruction patch/fake alias/forced includes or original executable compiler inputs.',
      '250 original/source caller pairs require500 actual ARMv4T returning callers, independent state/return/import-word models, exact GPR/CPSR/SP/writes/full8MiB RAM+128KiB WRAM hashes. Fixtures cover valarm enqueue/RSSI/signed16 counter saturation/queue busy/ping, deauthentication retry7/12 versus other failures, entry low16/game-info length, power state transitions, parameter32-bit masks/28-byte copy, every initialization failure/success stage, ignored lifetime-result behavior and DCF power-save exactBOOL/frame/callback paths.',
      'All original imported bodies execute0; previous owned WM-port send callers are modeled imported boundaries here. IRQ/message/parameter core/parent-copy/memory-copy/wireless-request/channel/callback providers use explicit bounded contracts, not full DS/scheduler/radio/game/Windows/Android execution. Three actual original16-bit MMIO stores execute only against a controlled synthetic memory page with full expected-page comparison; no device behavior is modeled or credited.',
      '18 genuinely linked wrong-C controls,693 exact original binding negatives,50 applicable instruction/literal negatives,3 geometry rejects,25 actual fresh ABI returns+5badABI and independent fresh explicit C99 whole bodies/relocations/genuine links are required. Aborted wrong-C runs are not caller returns. Two functions contain no literal loads; literal-origin negatives apply only where actual reads exist.',
      'Primary SDK evidence supports types/context without establishing historical exact revision/names or original allocation extents. No callee/source/storage credit from original anchors or borrowed models. Minimal immutable native/boundary/layout/compiler/source/runtime inputs are production dependencies; claim/review/atlas/dispatch/source-materialization stay diagnostic/admission provenance. Old single4464B and9/6476B source/READY/helpers remain frozen; accepted credit awaits shared coordinator acceptance.']
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm7',program='',module='arm7-main',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes'] for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
