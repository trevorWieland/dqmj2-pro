import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_ov001_state_controllers_source_second_paths import SOURCE,EVIDENCE,WORK,assert_owned
from wave20261106_ov001_state_controllers_source_second_build import build

PRODUCER='wave20261106_ov001_state_controllers_source_second_proof.py'
CANONICAL='evidence/matches/parallel-wave20261106-ov001-state-controllers-next-second.json'
CLONE=ROOT/'work/copied-root-replays/o1s-second-20261106'
CONTRACT=['program','processor','module','mode','address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerSha256','compilerFlags','nativeSymbolEntries']


def guard():
    assert_owned(EVIDENCE)
    if CLONE!=ROOT/'work/copied-root-replays/o1s-second-20261106'or not CLONE.resolve().is_relative_to((ROOT/'work/copied-root-replays').resolve()):raise ValueError('Exact new repo-local copied-root path differs')


def pin(name,role=None):
    result=dict(path=name,sha256=sha256(ROOT/name))
    if role:result['role']=role
    return result


def prepare():
    guard()
    if(EVIDENCE/'inputs.json').exists()or(EVIDENCE/'ready.json').exists():raise ValueError('Packet inputs already frozen')
    rows=[]
    for source in sorted(SOURCE.glob('*/main.c')):
        row,unused=build(source,WORK/'freeze'/source.parent.name);rows.append(row)
    if len(rows)!=2 or sum(r['bytes']for r in rows)!=712:raise ValueError('Exact one-function closed subset differs')
    names=set(code_closure([PRODUCER]));names.update(r['source']for r in rows);names.update(p['path']for r in rows for p in r['sourceDependencies']);mandatory=['project.json','provenance/seed-manifest.json',(EVIDENCE/'native-inputs.json').relative_to(ROOT).as_posix(),'config/arm9/symbols.txt','config/arm9/relocs.txt','config/arm9/overlays/ov001/symbols.txt','config/arm9/overlays/ov001/relocs.txt'];names.update(mandatory);native=read_json(EVIDENCE/'native-inputs.json');names.update([native['image']['path'],native['mainImage']['path'],'tools/mwccarm/mwccarm/license.dat'])
    for executable in['mwccarm.exe','mwldarm.exe']:names.update('tools/mwccarm/mwccarm/2.0/base/'+name for name in[executable,'ELFIO.dll','lmgr8c.dll','MSL_All-DLL80_x86.dll'])
    names.update(p.relative_to(ROOT).as_posix()for p in(ROOT/'deps/native').rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.suffix!='.pyc')
    if any(n.startswith(('work/','build/'))or n.endswith('.o')for n in names):raise ValueError('Work/compiler objects cannot be runtime implementation inputs')
    files=[pin(n,'source'if n.startswith(SOURCE.relative_to(ROOT).as_posix())else'generator'if n.endswith('.py')and not n.startswith('deps/')else'private-runtime-reference'if n.startswith(('extract/','tools/','deps/'))else'frozen-input')for n in sorted(names)];write_json(EVIDENCE/'inputs.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],entries=[{k:r[k]for k in CONTRACT}for r in rows],files=files,generatorSources=[p for p in files if p['role']=='generator'],mandatoryExternalInputs=[pin(n)for n in mandatory],limits=['No original/prebuilt game object,work product,mutable claim/dispatch/registry or inferred data payload is a compiler implementation input. Native images and local tool/runtime dependencies remain validation provenance with0source credit.']))
    print(dict(frozenFiles=len(files),functions=2,bytes=712,inputSha256=sha256(EVIDENCE/'inputs.json')),flush=True)


def execute():
    guard()
    if CLONE.exists()or(EVIDENCE/'ready.json').exists():raise ValueError('Fresh source-only clone/Ready required')
    manifest=read_json(EVIDENCE/'inputs.json');producer=[PRODUCER,'--inputs-sha256',sha256(EVIDENCE/'inputs.json')];subprocess.run([sys.executable,*producer],cwd=ROOT,check=True);original=read_json(EVIDENCE/'match.json');identities=[]
    for r in original['matches']:identity={k:r[k]for k in['program','processor','module','mode','address','bytes','source','sourceSha256','targetSha256']};identity['id']=original['romSha256']+'/arm9/ov001/arm/'+format(int(r['address'],0),'08x');identities.append(identity)
    descriptor=EVIDENCE/'canonical-packet.json';write_json(descriptor,dict(schemaVersion=1,romSha256=original['romSha256'],producer=producer,workerReport=(EVIDENCE/'match.json').relative_to(ROOT).as_posix(),canonicalReport=CANONICAL,frozenInputs=[pin((EVIDENCE/'inputs.json').relative_to(ROOT).as_posix()),*manifest['mandatoryExternalInputs']],identities=identities));command=[sys.executable,'replay_parallel_packet.py',descriptor.relative_to(ROOT).as_posix()];subprocess.run(command,cwd=ROOT,check=True);original=read_json(ROOT/CANONICAL);names={p['path']for p in manifest['files']}|set(code_closure(['replay_parallel_packet.py']))|{(EVIDENCE/'inputs.json').relative_to(ROOT).as_posix(),descriptor.relative_to(ROOT).as_posix()};copied=[]
    for name in sorted(names):
        target=CLONE/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
        if sha256(target)!=sha256(ROOT/name):raise ValueError('Fresh copied input hash differs')
        copied.append(pin(name))
    stale=dict(original,staleCanonicalNegativeControl=True)
    for name in[(EVIDENCE/'match.json').relative_to(ROOT).as_posix(),CANONICAL]:write_json(CLONE/name,stale)
    command=[sys.executable,str(CLONE/'replay_parallel_packet.py'),descriptor.relative_to(ROOT).as_posix()];process=subprocess.run(command,cwd=CLONE,capture_output=True,text=True,timeout=240);(EVIDENCE/'copied-root.log').write_text(process.stdout+process.stderr)
    if process.returncode:raise ValueError(('Fresh copied-root canonical replay failed',process.stdout[-2000:],process.stderr[-2000:]))
    fresh=read_json(CLONE/CANONICAL);worker=read_json(CLONE/EVIDENCE.relative_to(ROOT)/'match.json')
    if fresh.get('staleCanonicalNegativeControl')or worker.get('staleCanonicalNegativeControl')or fresh['matches']!=worker['matches']or not fresh.get('canonicalReportRefreshedFromFreshWorkerObjects')or fresh['generatedTrace']['uncompressedSha256']!=original['generatedTrace']['uncompressedSha256']:raise ValueError('Copied root retained stale reports or changed actual traces')
    records=[]
    for a,b in zip(original['matches'],fresh['matches']):
        if any(a[k]!=b[k]for k in CONTRACT)or not b['realLink']['exactCallerBytes']or not b['realLink']['linkerAttempt']['cwd'].startswith(str(CLONE))or sha256(CLONE/b['object'])!=b['objectSha256']:raise ValueError('Independent copied source/native/compiler/mode/object contract differs')
        records.append(dict(address=b['address'],bytes=b['bytes'],freshObjectSha256=b['objectSha256'],objectHashChanged=a['objectSha256']!=b['objectSha256'],freshGenuineEmbeddedLink=True))
    inventory=CLONE/'config/arm9/overlays/ov001/relocs.txt';before=inventory.read_bytes();objectPins=[(r['object'],sha256(CLONE/r['object']))for r in fresh['matches']]
    try:
        inventory.write_bytes(before+b'\n');negative=subprocess.run([sys.executable,str(CLONE/PRODUCER),*producer[1:]],cwd=CLONE,capture_output=True,text=True,timeout=60)
    finally:inventory.write_bytes(before)
    if negative.returncode==0 or'Immutable packet input changed'not in negative.stderr or objectPins!=[(r['object'],sha256(CLONE/r['object']))for r in fresh['matches']]:raise ValueError('Changed original input did not reject before compilation')
    write_json(EVIDENCE/'copied-root.json',dict(status='passed',sourceCredit=0,copiedRoot=str(CLONE),command=command,processExitCode=process.returncode,originalWorkObjectsCopied=False,originalBuildProductsCopied=False,sourceAndToolsCopiedFresh=True,staleWorkerAndCanonicalReportsReplaced=True,sourceNativeCompilerBindingsIdentical=True,traceSha256=fresh['generatedTrace']['uncompressedSha256'],actualNativeAndSourceCallerReturns=fresh['actualNativeAndSourceCallerReturns'],nativeCalleeBodiesExecutedInCallerFixtures=0,immutableInputMutationRejectedBeforeCompilation=True,negativeExitCode=negative.returncode,negativeStderr=negative.stderr,functions=len(records),bytes=712,records=records,copiedFiles=copied,log=pin((EVIDENCE/'copied-root.log').relative_to(ROOT).as_posix())))
    for p in manifest['files']:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Pinned source/compiler input changed during qualification')
    outputs=[(EVIDENCE/name).relative_to(ROOT).as_posix()for name in['match.json','controls.json','traces.json.gz']]+[CANONICAL];proofs=[(EVIDENCE/name).relative_to(ROOT).as_posix()for name in['copied-root.json','copied-root.log']];files=list(manifest['files'])+[pin(n,'diagnostic-proof')for n in proofs]+[pin(descriptor.relative_to(ROOT).as_posix(),'canonical-descriptor'),pin((EVIDENCE/'inputs.json').relative_to(ROOT).as_posix(),'input-manifest'),pin(Path(__file__).name,'diagnostic-generator')]+[pin(n,'produced-report'if n.endswith('.json')else'produced-trace')for n in outputs]
    write_json(EVIDENCE/'ready.json',dict(schemaVersion=1,status='ready-for-coordinator-acceptance',romSha256=original['romSha256'],functions=2,bytes=712,sourceCreditPendingIntegrator=712,acceptedBaselineCohort=172,packets=[dict(report=CANONICAL,producer=producer)],frozenInputManifest=pin((EVIDENCE/'inputs.json').relative_to(ROOT).as_posix()),canonicalDescriptor=pin(descriptor.relative_to(ROOT).as_posix()),identities=identities,files=files,generatorSources=manifest['generatorSources'],mutableGeneratedOutputs=[dict(path=n,observedSha256=sha256(ROOT/n),immutableReplayInput=False)for n in outputs],generatedReportsAreNotFrozenInputs=True,actualNativeAndSourceCallerReturns=original['actualNativeAndSourceCallerReturns'],wholeCNegativeControlsRejected=original['wholeCNegativeControlsRejected'],relocationsPreserved=28,copiedRootCanonicalReplayPassed=True,remainingFunctions=0,remainingBytes=0,limits=original['limits']))
    print(dict(ready=(EVIDENCE/'ready.json').relative_to(ROOT).as_posix(),sha256=sha256(EVIDENCE/'ready.json'),functions=2,bytes=712),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','execute']);{'prepare':prepare,'execute':execute}[parser.parse_args().action]()
