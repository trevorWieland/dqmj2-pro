import json
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_arm7_wl_channel_source_first_build import LANE,SOURCE,WORK

PRODUCER='wave20261106_arm7_wl_channel_source_first_proof_v2.py'
CANONICAL='evidence/matches/parallel-wave20261106-arm7-wl-channel-next-first.json'
CLONE=ROOT/'work/copied-root-replays/w6wch-first-1106'


def pin(path,role=None):
    if not isinstance(path,str):path=path.relative_to(ROOT).as_posix()
    value=dict(path=path,sha256=sha256(ROOT/path))
    if role:value['role']=role
    return value
def guard():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-channel-next/first'or SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-channel-next/first'or WORK!=ROOT/'work/w6wch/first'or CLONE!=ROOT/'work/copied-root-replays/w6wch-first-1106':raise ValueError('Exact fresh RxMan source/evidence/work/copy scope differs')
def prepare():
    guard()
    if(LANE/'inputs-v2.json').exists():raise ValueError('RxMan input manifest already frozen')
    names=set(code_closure([PRODUCER,Path(__file__).name,'replay_parallel_packet.py']));names.update(p.relative_to(ROOT).as_posix()for p in SOURCE.rglob('*')if p.is_file());mandatory=['project.json','provenance/seed-manifest.json','evidence/arm7/runtime-layout.json','evidence/arm7/ghidra-runtime-inventory.json',*(str(LANE.relative_to(ROOT)).replace('\\','/')+'/'+name for name in['native-certificate.json','boundary-certificate.json','layout-baseline.json']),str((LANE.parent/'claim.json').relative_to(ROOT)).replace('\\','/')];mandatory += ['qualify_arm7_scoped_control.py','evidence/lanes/parallel-wave20261106/arm7-wl-channel-next/coordinator-admission.json','evidence/lanes/parallel-wave20261106/arm7-wl-channel-next-proposal/coordinator-scoped-flow.json','evidence/verification/arm7-channel-rtc-scoped-native-control-qualification-20261106.json'];names.update(mandatory);names.update(['extract/arm7/arm7.bin','extract/arm7/runtime/arm7-boot.bin','extract/arm7/runtime/arm7-wram.bin','extract/arm7/runtime/arm7-main.bin','tools/mwccarm/mwccarm/license.dat'])
    for version,exe in[('2.0/sp1p5','mwccarm.exe'),('2.0/base','mwldarm.exe')]:names.update('tools/mwccarm/mwccarm/'+version+'/'+name for name in[exe,'ELFIO.dll','lmgr8c.dll','MSL_All-DLL80_x86.dll'])
    names.update(p.relative_to(ROOT).as_posix()for p in(ROOT/'deps/native').rglob('*')if p.is_file()and '__pycache__'not in p.parts and p.suffix!='.pyc');files=[pin(name,'source'if name.startswith(SOURCE.relative_to(ROOT).as_posix())else'generator'if name.endswith('.py')and not name.startswith('deps/')else'private-runtime'if name.startswith(('tools/','deps/','extract/'))else'frozen-input')for name in sorted(names)];certificate=read_json(LANE/'native-certificate.json')['functions'][0];entry={k:certificate[k]for k in['program','processor','module','mode','address','bytes','targetSha256','inputModuleSha256','source']};entry['id']=read_json(ROOT/'project.json')['romSha256']+'/arm7/arm7-main/arm/027e990c';entry['sourceSha256']=sha256(ROOT/entry['source']);value=dict(schemaVersion=1,romSha256=entry['id'].split('/')[0],entries=[entry],files=files,mandatoryExternalInputs=[pin(name)for name in mandatory],generatorSources=[p for p in files if p['role']=='generator'],limits=['Only five closed readable C/header files,actual pinned compiler/linker/DLL/Python/native modules and real input manifests are runtime dependencies. No public reference object/archive or diagnostic work source is a compile/link input.']);write_json(LANE/'inputs-v2.json',value);print(dict(inputs=pin(LANE/'inputs-v2.json'),pins=len(files),functions=1,bytes=652),flush=True)
def descriptor():
    guard();report=read_json(LANE/'match.json');inputs=read_json(LANE/'inputs-v2.json');row=report['matches'][0];identity={k:row[k]for k in['program','processor','module','mode','address','bytes','source','sourceSha256','targetSha256']};identity['id']=inputs['entries'][0]['id'];value=dict(romSha256=report['romSha256'],producer=[PRODUCER],workerReport=(LANE/'match.json').relative_to(ROOT).as_posix(),canonicalReport=CANONICAL,frozenInputs=[pin(LANE/'inputs-v2.json'),*inputs['mandatoryExternalInputs']],identities=[identity]);write_json(LANE/'canonical-packet.json',value);print(pin(LANE/'canonical-packet.json'),flush=True)
def copied_root():
    guard()
    if CLONE.exists():raise ValueError('Independent copied root already exists')
    inputs=read_json(LANE/'inputs-v2.json');descriptor=read_json(LANE/'canonical-packet.json');names={p['path']for p in inputs['files']};names.update([(LANE/'inputs-v2.json').relative_to(ROOT).as_posix(),(LANE/'canonical-packet.json').relative_to(ROOT).as_posix()])
    for name in sorted(names):
        target=CLONE/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
        if sha256(target)!=sha256(ROOT/name):raise ValueError('Copied immutable runtime input changed')
    baseline=read_json(ROOT/CANONICAL)
    for name in[descriptor['workerReport'],CANONICAL]:write_json(CLONE/name,dict(baseline,staleCanonicalNegativeControl=True))
    command=[sys.executable,str(CLONE/'replay_parallel_packet.py'),(LANE/'canonical-packet.json').relative_to(ROOT).as_posix()];process=subprocess.run(command,cwd=CLONE,capture_output=True,text=True,timeout=240);(LANE/'copied-root.log').write_text(process.stdout+process.stderr,encoding='utf-8')
    if process.returncode:raise ValueError(('Fresh source-only copied canonical replay failed',process.stdout[-1500:],process.stderr[-1500:]))
    fresh=read_json(CLONE/CANONICAL);worker=read_json(CLONE/descriptor['workerReport'])
    if fresh.get('staleCanonicalNegativeControl')or worker.get('staleCanonicalNegativeControl')or not fresh.get('canonicalReportRefreshedFromFreshWorkerObjects')or fresh['matches']!=worker['matches']:raise ValueError('Fresh canonical replay retained stale worker/object metadata')
    if fresh['generatedTrace']['uncompressedSha256']!=baseline['generatedTrace']['uncompressedSha256']:raise ValueError('Independent source/native model traces differ')
    previous=baseline['matches'][0];row=fresh['matches'][0];contracts=['program','processor','module','mode','address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compiler','compilerSha256','compilerFlags','nativeSymbolEntries']
    if any(row.get(k)!=previous.get(k)for k in contracts):raise ValueError('Copied complete source/native/compiler/ABI contract differs')
    if not row['realLink']['linkerAttempt']['cwd'].startswith(str(CLONE))or sha256(CLONE/row['object'])!=row['objectSha256']or sha256(CLONE/row['realLink']['linkedElf'])!=row['realLink']['linkedElfSha256']or not row['realLink']['exactCallerBytes']:raise ValueError('Copied actual fresh compiler/link products invalid')
    original=CLONE/'extract/arm7/runtime/arm7-main.bin';raw=original.read_bytes();obj=CLONE/row['object'];before=(sha256(obj),obj.stat().st_mtime_ns)
    try:
        original.write_bytes(raw[:-1]+bytes([raw[-1]^1]));negative=subprocess.run([sys.executable,str(CLONE/PRODUCER)],cwd=CLONE,capture_output=True,text=True,timeout=60)
    finally:original.write_bytes(raw)
    if negative.returncode==0 or 'Frozen actual PM compiler/source/native/runtime input changed'not in negative.stderr or before!=(sha256(obj),obj.stat().st_mtime_ns):raise ValueError('Altered original native module not rejected before compiler execution')
    result=dict(status='passed',sourceCredit=0,copiedRoot=str(CLONE),command=command,exitCode=process.returncode,originalWorkObjectsCopied=False,originalBuildProductsCopied=False,staleWorkerAndCanonicalReportsReplaced=True,canonicalObjectsRefreshed=True,traceSha256=fresh['generatedTrace']['uncompressedSha256'],actualNativeAndSourceCallerReturns=fresh['actualNativeAndSourceCallerReturns'],nativeProviderBodiesExecuted=0,functions=1,bytes=652,freshObjectSha256=row['objectSha256'],objectHashChanged=row['objectSha256']!=previous['objectSha256'],actualCallerLinkMetadataVerified=True,changedNativeModuleRejectedBeforeCompilation=True,negativeExitCode=negative.returncode,negativeStderr=negative.stderr,canonicalReportSha256=sha256(CLONE/CANONICAL));write_json(LANE/'copied-root-canonical-proof.json',result);print(dict(status='copied-root-passed',functions=1,bytes=652),flush=True)
def ready():
    guard();inputs=read_json(LANE/'inputs-v2.json');report=read_json(ROOT/CANONICAL);descriptor=read_json(LANE/'canonical-packet.json');copied=read_json(LANE/'copied-root-canonical-proof.json')
    if copied['status']!='passed'or not report['allPassed']or(LANE/'ready.json').exists():raise ValueError('Immutable Ready exists or proof incomplete')
    for p in inputs['files']:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Pre-freeze actual runtime input changed:'+p['path'])
    extras=[LANE/'inputs-v2.json',LANE/'canonical-packet.json',LANE/'copied-root-canonical-proof.json',LANE/'copied-root.log',LANE/'source-materialization.json'];files=[*inputs['files'],*[pin(p)for p in extras]];outputs=[(LANE/'match.json').relative_to(ROOT).as_posix(),CANONICAL,(LANE/'controls.json').relative_to(ROOT).as_posix(),(LANE/'traces.json.gz').relative_to(ROOT).as_posix()];value=dict(schemaVersion=1,status='ready-for-coordinator-acceptance',acceptedBaselineCohort=171,romSha256=report['romSha256'],functions=1,bytes=652,sourceCreditPendingIntegrator=652,packets=[dict(report=descriptor['workerReport'],producer=[PRODUCER])],frozenInputManifest=pin(LANE/'inputs-v2.json'),canonicalDescriptor=pin(LANE/'canonical-packet.json'),identities=descriptor['identities'],files=files,generatorSources=inputs['generatorSources'],immutableReplayInputPins=inputs['files'],mutableGeneratedOutputs=[dict(path=p,observedSha256=sha256(ROOT/p),immutableReplayInput=False,role='Fresh producer/canonical output observation,not frozen runtime input')for p in outputs],generatedReportsAreNotFrozenInputs=True,copiedRootCanonicalReplayPassed=True,actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],nativeCalleeBodiesExecuted=0,ordinaryCBytes=652,justifiedAssemblyBytes=0,externalStorageCredit=0,relocationsPreserved=8,callerFixtureTraceSha256=report['generatedTrace']['uncompressedSha256'],limits=report['limits']);write_json(LANE/'ready.json',value);print(dict(ready=pin(LANE/'ready.json'),pins=len(files),functions=1,bytes=652),flush=True)


if __name__=='__main__':{'prepare':prepare,'descriptor':descriptor,'copy':copied_root,'ready':ready}[sys.argv[1]]()
