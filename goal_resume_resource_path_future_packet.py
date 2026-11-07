import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from seal_recovery_evidence_20261031 import code_closure
from goal_resume_resource_path_future import FUTURE_SOURCE,FUTURE_LANE,FUTURE_WORK,OLD_SOURCE,OLD_LANE,LANE
from goal_resume_resource_path_future_proof import records

PRODUCER='goal_resume_resource_path_future_controls.py'
INPUTS=FUTURE_LANE/'inputs-controls.json'


def pin(path,role=None):
    path=Path(path);name=path.relative_to(ROOT).as_posix()if path.is_absolute()else path.as_posix();value=dict(path=name,sha256=sha256(ROOT/name))
    if role:value['role']=role
    return value


def freeze():
    destination=INPUTS
    if destination.exists():
        value=read_json(destination)
        for p in value['files']:
            if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Frozen typed future input changed')
        return value
    generators=set(code_closure([PRODUCER]));paths=set(generators)
    parent=read_json(LANE/'inputs-replay.json');paths.update(p['path']for p in parent['files']if p['path'].startswith(('tools/','deps/')))
    paths.update(p.relative_to(ROOT).as_posix()for p in FUTURE_SOURCE.rglob('*')if p.is_file());paths.add((FUTURE_SOURCE.parent/'resource_path_api.h').relative_to(ROOT).as_posix())
    paths.update(p.relative_to(ROOT).as_posix()for p in OLD_SOURCE.glob('*')if p.is_file())
    paths.update(['project.json','provenance/seed-manifest.json','extract/arm9/arm9.bin','config/arm9/symbols.txt','config/arm9/relocs.txt','config/arm9/delinks.txt'])
    paths.update((FUTURE_LANE/name).relative_to(ROOT).as_posix()for name in['claim.json','reference-contracts.json','inputs.json']);paths.add((LANE/'ready.json').relative_to(ROOT).as_posix())
    if any(p.startswith('work/')or p.endswith('.o')for p in paths):raise ValueError('Typed future replay contains cached outputs')
    value=dict(schemaVersion=1,status='frozen-typed-future268-and-residual432-inputs',sourceCredit=0,historicalObjectsCopied=False,canonicalApiDependency=pin(LANE/'ready.json'),files=[pin(p,'generator'if p in generators else'private-runtime'if p.startswith(('tools/','deps/'))else'frozen-input')for p in sorted(paths)])
    write_json(destination,value);return value


def invoke(root,log):
    command=[sys.executable,str(root/PRODUCER)];process=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=300,env=dict(os.environ,PYTHONPATH=''));log.write_text(process.stdout+process.stderr)
    if process.returncode:raise ValueError(('Typed future independent proof failed',str(log),process.returncode))
    return command


def main():
    if(FUTURE_LANE/'ready.json').exists():raise ValueError('Sealed typed future packet is immutable')
    inputs=freeze();invoke(ROOT,FUTURE_LANE/'main-controls-proof.log');clone=ROOT/'work/copied-root-replays'/('s1p700-'+uuid.uuid4().hex[:4]);paths={p['path']for p in inputs['files']}|{INPUTS.relative_to(ROOT).as_posix()}
    if clone.exists():raise ValueError('Typed future copied root already exists')
    for name in sorted(paths):
        target=clone/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
        if sha256(target)!=sha256(ROOT/name):raise ValueError('Typed future copied input differs')
    command=invoke(clone,FUTURE_LANE/'copied-controls-proof.log');first=read_json(FUTURE_LANE/'qualification.json');second=read_json(clone/FUTURE_LANE.relative_to(ROOT)/'qualification.json')
    if first['generatedTrace']['uncompressedSha256']!=second['generatedTrace']['uncompressedSha256']:raise ValueError('Typed future full diagnostic/observation trace differs')
    fields=lambda r:[(x['address'],x['bytes'],x['compiledBytes'],x['sourceSha256'],x['realLink']['exactCallerBytes'])for x in r['functions']]
    if fields(first)!=fields(second):raise ValueError('Typed future compiled source/native status differs')
    write_json(FUTURE_LANE/'copied-qualification.json',second);artifacts=[]
    for output_root in['work/p-api700','work/p-api700-neg','work/p-api700-types']:
        for path in sorted((clone/output_root).rglob('*')):
            if path.is_file():
                target=FUTURE_WORK/'copied-output'/output_root/path.relative_to(clone/output_root);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target);artifacts.append(dict(historicalPath=path.relative_to(clone).as_posix(),preservedPath=target.relative_to(ROOT).as_posix(),sha256=sha256(target)))
    replay=dict(status='passed',copiedRoot=clone.relative_to(ROOT).as_posix(),command=command,frozenInputFiles=len(paths),frozenInputBytes=sum((ROOT/name).stat().st_size for name in paths),historicalObjectsCopied=False,workOutputsCopied=False,originalRepositoryUsedAsRuntimeRoot=False,freshCompiledFunctions=2,matchedCandidateBytes=268,nonmatchingResidualBytes=432,actualTopReturns=second['actualTopReturns'],actualHelperReturnsPerSide=second['actualHelperReturnsPerSide'],traceSha256=second['generatedTrace']['uncompressedSha256'],preservedArtifacts=artifacts)
    write_json(FUTURE_LANE/'copied-root.json',replay);files=[dict(p)for p in inputs['files']]+[pin(Path(__file__),'packet-generator')]
    files.extend(pin(FUTURE_LANE/name,'produced-evidence')for name in['inputs-controls.json','qualification.json','traces.json.gz','main-controls-proof.log','copied-root.json','copied-controls-proof.log','copied-qualification.json']);report='evidence/matches/goal-resume20261107-resource-path-display268.json';files.append(pin(report,'canonical-report'))
    for p in files:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Final typed future packet pin changed')
    selected=next(r for r in records()if int(r['address'],0)==0x02061470);identity=dict(program='',processor='arm9',module='main',mode='arm',address=selected['address'],bytes=268,id=configuration()['romSha256']+'/arm9/main/arm/02061470')
    ready=dict(schemaVersion=1,status='ready-for-coordinator-acceptance',romSha256=configuration()['romSha256'],functions=1,bytes=268,newFunctionCandidates=1,newByteCandidates=268,sourceCreditPendingIntegrator=0,packets=[dict(report=report,producer=[sys.executable,PRODUCER])],identities=[identity],files=files,generatorSources=[p for p in inputs['files']if p['role']=='generator'],frozenInputManifest=pin(INPUTS),canonicalApiDependency=pin(LANE/'ready.json'),independentReplay=pin(FUTURE_LANE/'copied-root.json'),limits=first['limits'])
    write_json(FUTURE_LANE/'ready.json',ready)
    residual=next(r for r in first['functions']if int(r['address'],0)==0x02061088);write_json(FUTURE_LANE/'working432.json',dict(status='functional-C-API-medium-nonmatching',confidence='medium',sourceCredit=0,matched=False,function=residual,rawRegisterDifferences=[r for r in first['rawRegisterDifferences']if int(r['address'],0)==0x02061088],qualification=pin(FUTURE_LANE/'qualification.json'),independentReplay=pin(FUTURE_LANE/'copied-root.json'),files=files,limits=first['limits']))
    print(dict(ready=(FUTURE_LANE/'ready.json').relative_to(ROOT).as_posix(),matchedCandidateBytes=268,residualBytes=432,inputFiles=len(paths),copiedRoot=replay['copiedRoot'],sourceCredit=0),flush=True)


if __name__=='__main__':main()
