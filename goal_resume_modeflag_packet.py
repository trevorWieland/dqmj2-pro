import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from seal_recovery_evidence_20261031 import code_closure
from goal_resume_modeflag_abi import LANE,SOURCE,WORK,references

JOBS=[('migration','goal_resume_modeflag_abi.py','match.json','evidence/matches/goal-resume20261106-modeflag-abi-migrations.json'),
    ('future','goal_resume_modeflag_future.py','future-detail/match.json','evidence/matches/goal-resume20261106-modeflag-abi-detail.json')]


def pin(path,role=None):
    path=Path(path);relative=path.relative_to(ROOT).as_posix()if path.is_absolute()else path.as_posix()
    value=dict(path=relative,sha256=sha256(ROOT/relative))
    if role:value['role']=role
    return value


def freeze():
    path=LANE/'inputs.json'
    if path.exists():
        value=read_json(path)
        for r in value['files']:
            if sha256(ROOT/r['path'])!=r['sha256']:raise ValueError('Frozen ABI replay input changed: '+r['path'])
        return value
    claim=read_json(LANE/'claim.json')
    for r in claim['preserveInputs']:
        if sha256(ROOT/r['path'])!=r['sha256']:raise ValueError('Inherited frozen artifact changed')
    generators=set(code_closure([j[1]for j in JOBS]+['replay_parallel_packet.py']))
    paths=set(generators)
    for package in ['elftools','unicorn','capstone']:
        paths.update(p.relative_to(ROOT).as_posix()for p in(ROOT/'deps/native'/package).rglob('*')if p.is_file()and p.suffix in('.py','.dll'))
    prior=read_json(ROOT/'evidence/lanes/parallel-wave20261106/goal-resume-source-1/detail-display/inputs.json')
    paths.update(r['path']for r in prior['files']if r['path'].startswith('tools/'))
    paths.update(['tools/mwccarm/mwccarm/2.0/base/mwccarm.exe','tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe','project.json','provenance/seed-manifest.json','extract/arm9/arm9.bin','config/arm9/symbols.txt','config/arm9/relocs.txt','config/arm9/delinks.txt','extract/arm9_overlays/ov000.bin','config/arm9/overlays/ov000/symbols.txt','evidence/lanes/parallel-wave20261105/game-main-arm-next/third/data-inputs.json','evidence/lanes/parallel-wave20261104/main-command-forward/data-inputs.json','evidence/matches/goal-resume20261106-source1-detail-display.json'])
    paths.update([(LANE/'claim.json').relative_to(ROOT).as_posix(),(LANE/'reference-contracts.json').relative_to(ROOT).as_posix(),claim['approvedPlan']['path']])
    for r in references():
        paths.add(r['source']);paths.add(r['newSource'])
        paths.update(d['path']for d in r.get('sourceDependencies')or[])
    paths.update(r['path']for r in claim['sourceViews'])
    if any(p.startswith('work/')or p.endswith('.o')for p in paths):raise ValueError('Input-only replay cannot copy historical compiler/link outputs or work helpers')
    value=dict(schemaVersion=1,status='frozen-input-only-modeflag-ABI-replay',sourceCredit=0,files=[pin(p,'generator'if p in generators else'private-runtime'if p.startswith(('tools/','deps/'))else'frozen-input')for p in sorted(paths)],historicalObjectsCopied=False,oldObjectReference=pin(LANE/'reference-contracts.json'),preservedHistoricalPinsVerified=len(claim['preserveInputs']))
    write_json(path,value)
    return value


def descriptors(inputs):
    result=[]
    for name,producer,worker,canonical in JOBS:
        entries=[r for r in references()if(int(r['address'],0)==0x020721b4)==(name=='future')]
        identities=[dict(program='',processor='arm9',module='main',mode='arm',address=r['address'],bytes=r['bytes'],source=r['newSource'],sourceSha256=sha256(ROOT/r['newSource']),targetSha256=r['targetSha256'],id=configuration()['romSha256']+'/arm9/main/arm/'+f"{int(r['address'],0):08x}")for r in entries]
        path=LANE/(name+'-canonical-packet.json')
        value=dict(romSha256=configuration()['romSha256'],producer=[producer],workerReport=(LANE/worker).relative_to(ROOT).as_posix(),canonicalReport=canonical,frozenInputs=[pin(LANE/'inputs.json')],identities=identities)
        write_json(path,value);result.append((path,value))
    return result


def invoke(root,descriptor,log):
    command=[sys.executable,str(root/'replay_parallel_packet.py'),descriptor.relative_to(ROOT).as_posix()]
    process=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=300,env=dict(os.environ,PYTHONPATH=''))
    log.write_text(process.stdout+process.stderr)
    if process.returncode:raise ValueError(('Canonical ABI replay failed',str(log),process.returncode))
    return command


def main():
    if(LANE/'ready.json').exists():raise ValueError('Ready ABI packet is immutable')
    inputs=freeze();jobs=descriptors(inputs)
    for path,value in jobs:
        invoke(ROOT,path,LANE/(path.stem+'-main.log'))
    clone=ROOT/'work/copied-root-replays'/('s1abi-'+uuid.uuid4().hex[:4])
    if clone.exists():raise ValueError('Unique replay root already exists')
    paths={r['path']for r in inputs['files']}
    paths.update([(LANE/'inputs.json').relative_to(ROOT).as_posix(),*[p.relative_to(ROOT).as_posix()for p,v in jobs]])
    for name in sorted(paths):
        destination=clone/name;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,destination)
        if sha256(destination)!=sha256(ROOT/name):raise ValueError('Copied input changed')
    commands=[];replayed=[]
    for path,value in jobs:
        command=invoke(clone,path,LANE/(path.stem+'-copy.log'));commands.append(command)
        first=read_json(ROOT/value['canonicalReport']);second=read_json(clone/value['canonicalReport'])
        if first['generatedTrace']['uncompressedSha256']!=second['generatedTrace']['uncompressedSha256']:raise ValueError('Independent actual caller trace changed')
        if[(r['address'],r['bytes'],r['sourceSha256'],r['targetSha256'])for r in first['matches']]!=[(r['address'],r['bytes'],r['sourceSha256'],r['targetSha256'])for r in second['matches']]:raise ValueError('Independent source/target identity differs')
        if not all(r['realLink']['exactCallerBytes']for r in second['matches']):raise ValueError('Independent genuine link proof absent')
        write_json(LANE/(path.stem+'-copied-report.json'),second)
        replayed.append(dict(canonicalReport=value['canonicalReport'],functions=len(second['matches']),bytes=sum(r['bytes']for r in second['matches']),traceSha256=second['generatedTrace']['uncompressedSha256'],freshObjectHashes=[r['objectSha256']for r in second['matches']]))
    artifacts=[]
    for path in sorted((clone/WORK.relative_to(ROOT)).rglob('*')):
        if path.is_file():
            destination=WORK/'copied-output'/path.relative_to(clone/WORK.relative_to(ROOT));destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,destination)
            artifacts.append(dict(historicalPath=path.relative_to(clone).as_posix(),preservedPath=destination.relative_to(ROOT).as_posix(),sha256=sha256(destination)))
    replay=dict(status='passed',copiedRoot=clone.relative_to(ROOT).as_posix(),commands=commands,frozenInputFiles=len(paths),frozenInputBytes=sum((ROOT/name).stat().st_size for name in paths),historicalObjectsCopied=False,workOutputsCopied=False,originalRepositoryUsedAsRuntimeRoot=False,freshPreviousSourcesCompiled=5,freshNewViewsLinked=6,sourceCredit=0,reports=replayed,preservedArtifacts=artifacts)
    write_json(LANE/'copied-root.json',replay)
    for r in read_json(LANE/'claim.json')['preserveInputs']:
        if sha256(ROOT/r['path'])!=r['sha256']:raise ValueError('Inherited source/object/header/report/proposal changed')
    files=[dict(r)for r in inputs['files']]
    files.extend(pin(p,'produced-evidence')for p in sorted(LANE.rglob('*'))if p.is_file()and p.name!='ready.json'and p.relative_to(ROOT).as_posix()not in{r['path']for r in files})
    files.extend(pin(ROOT/j[3],'produced-report')for j in JOBS)
    files.append(pin(Path(__file__),'diagnostic-generator'))
    ready=dict(schemaVersion=1,status='ready-for-coordinator-acceptance',romSha256=configuration()['romSha256'],functions=6,bytes=1036,zeroCreditMigrationFunctions=5,preservedMigrationBytes=580,acceptedFunctionCountDelta=0,acceptedByteCreditDelta=0,newFunctionCandidates=1,newByteCandidates=456,sourceCreditPendingIntegrator=0,frozen174Excluded=True,packets=[dict(report=v['canonicalReport'],producer=v['producer'])for p,v in jobs],canonicalDescriptors=[pin(p)for p,v in jobs],identities=[r for p,v in jobs for r in v['identities']],files=files,generatorSources=[r for r in inputs['files']if r['role']=='generator'],frozenInputManifest=pin(LANE/'inputs.json'),admissionProvenance=pin(LANE/'claim.json'),independentReplay=pin(LANE/'copied-root.json'),limits=['Five previously accepted functions/580B remain zero-credit additive ABI migrations; the456B candidate remains unaccepted until coordinator adoption and shared gates.','Every old source/header/report/typed proposal/READY and canonical reference object remains unchanged.','Input-only replay copies no historical object or work output; both old pinned sources and new views compile independently against frozen actual allocated-object/relocation reference contracts.','Genuine native links cover six complete function spans. Shared20-module acceptance, registry/source preferences and publication remain coordinator-owned.'])
    write_json(LANE/'ready.json',ready)
    print(dict(ready=(LANE/'ready.json').relative_to(ROOT).as_posix(),migrations=5,preservedBytes=580,futureBytes=456,copiedRoot=replay['copiedRoot'],frozenInputBytes=replay['frozenInputBytes']),flush=True)


if __name__=='__main__':main()
