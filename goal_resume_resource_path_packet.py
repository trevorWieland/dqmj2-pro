import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from seal_recovery_evidence_20261031 import code_closure
from goal_resume_resource_path_views import SOURCE,LANE,WORK,SDK,AUDIT
from goal_resume_resource_path_contracts import recipes,view,dependencies

PRODUCER='goal_resume_resource_path_replay.py'
INPUTS=LANE/'inputs-replay.json'


def pin(path,role=None):
    path=Path(path);name=path.relative_to(ROOT).as_posix()if path.is_absolute()else path.as_posix();result=dict(path=name,sha256=sha256(ROOT/name))
    if role:result['role']=role
    return result


def freeze():
    destination=INPUTS
    if destination.exists():
        value=read_json(destination)
        for p in value['files']:
            if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Frozen API replay input changed')
        return value
    generators=set(code_closure([PRODUCER]));paths=set(generators)
    old=read_json(ROOT/'evidence/lanes/parallel-wave20261106/goal-resume-source-1-modeflag-abi/inputs.json')
    paths.update(r['path']for r in old['files']if r['path'].startswith(('tools/','deps/')))
    paths.update(p.relative_to(ROOT).as_posix()for p in SOURCE.rglob('*')if p.is_file())
    paths.update(['project.json','provenance/seed-manifest.json',AUDIT.relative_to(ROOT).as_posix(),SDK.relative_to(ROOT).as_posix(),'src/runtime/runtime08/native_main_0200bd04.c','src/runtime/runtime08/native_main_0200c02c.c'])
    paths.update((LANE/name).relative_to(ROOT).as_posix()for name in['claim.json','reference-contracts.json','sdk-types.json','word-boundary-witness.json','faithful-structural-diff.json'])
    for ref in recipes():
        paths.add(ref['source']);paths.update(r['path']for r in ref['sourceDependencies'])
        paths.update(r['path']for r in dependencies(view(ref)))
    for module in['main','ov000','ov005','ov006']:
        module_info=next(m for m in read_json(ROOT/'provenance/seed-manifest.json')['modules']if m['name']==module);paths.add(module_info['binary'])
        paths.add('config/arm9/symbols.txt'if module=='main'else f'config/arm9/overlays/{module}/symbols.txt')
    if any(p.startswith('work/')or p.endswith('.o')for p in paths):raise ValueError('Input-only replay contains a cached object or work output')
    value=dict(schemaVersion=1,status='frozen-resource-path-API-input-only-replay',sourceCredit=0,historicalObjectsCopied=False,files=[pin(p,'generator'if p in generators else'private-runtime'if p.startswith(('tools/','deps/'))else'frozen-input')for p in sorted(paths)])
    write_json(destination,value);return value


def invoke(root,log):
    command=[sys.executable,str(root/PRODUCER)];process=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=300,env=dict(os.environ,PYTHONPATH=''))
    log.write_text(process.stdout+process.stderr)
    if process.returncode:raise ValueError(('Input-only API proof failed',str(log),process.returncode))
    return command


def main():
    if(LANE/'ready.json').exists():raise ValueError('Sealed API migration packet is immutable')
    inputs=freeze();invoke(ROOT,LANE/'main-replay-proof.log')
    clone=ROOT/'work/copied-root-replays'/('s1path-'+uuid.uuid4().hex[:4]);paths={r['path']for r in inputs['files']}|{INPUTS.relative_to(ROOT).as_posix()}
    if clone.exists():raise ValueError('Independent API replay root already exists')
    for name in sorted(paths):
        target=clone/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
        if sha256(target)!=sha256(ROOT/name):raise ValueError('Copied API input changed')
    command=invoke(clone,LANE/'copied-replay-proof.log');first=read_json(LANE/'qualification.json');second=read_json(clone/LANE.relative_to(ROOT)/'qualification.json')
    if first['generatedTrace']['uncompressedSha256']!=second['generatedTrace']['uncompressedSha256']:raise ValueError('Independent API full machine/behavior trace differs')
    fields=lambda r:[(x['identity'],x['bytes'],x['view']['sourceSha256'],x['view']['allocatedContractSha256'])for x in r['allocatedComparisons']]
    if fields(first)!=fields(second):raise ValueError('Independent old/view allocated source contract differs')
    write_json(LANE/'copied-qualification.json',second);artifacts=[]
    for output_root in[WORK.relative_to(ROOT),Path('work/p-api')]:
        for path in sorted((clone/output_root).rglob('*')):
            if path.is_file():
                target=WORK/'copied-output'/output_root/path.relative_to(clone/output_root);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
                artifacts.append(dict(historicalPath=path.relative_to(clone).as_posix(),preservedPath=target.relative_to(ROOT).as_posix(),sha256=sha256(target)))
    replay=dict(status='passed',copiedRoot=clone.relative_to(ROOT).as_posix(),command=command,frozenInputFiles=len(paths),frozenInputBytes=sum((ROOT/name).stat().st_size for name in paths),historicalObjectsCopied=False,workOutputsCopied=False,originalRepositoryUsedAsRuntimeRoot=False,freshPreviousSources=27,freshNewViews=27,genuineNativeFunctionLinks=54,actualTopReturns=second['behavior']['actualTopReturns'],actualHelperReturnsPerSide=second['behavior']['actualHelperReturnsPerSide'],traceSha256=second['generatedTrace']['uncompressedSha256'],preservedArtifacts=artifacts)
    write_json(LANE/'copied-root.json',replay)
    packets=[]
    for module in['main','ov000','ov005','ov006']:
        report='evidence/matches/goal-resume20261107-resource-path-api-'+module+'.json';packets.append(dict(report=report,producer=[sys.executable,PRODUCER]))
    files=[dict(p)for p in inputs['files']]+[pin(Path(__file__),'packet-generator')]
    files.extend(pin(LANE/name,'produced-evidence')for name in['inputs-replay.json','qualification.json','traces.json.gz','main-replay-proof.log','copied-root.json','copied-replay-proof.log','copied-qualification.json'])
    files.extend(pin(p['report'],'canonical-report')for p in packets)
    ready=dict(schemaVersion=1,status='ready-for-coordinator-acceptance',romSha256=configuration()['romSha256'],functions=27,bytes=4812,zeroCreditMigrationFunctions=27,preservedMigrationBytes=4812,acceptedFunctionCountDelta=0,acceptedByteCreditDelta=0,newFunctionCandidates=0,sourceCreditPendingIntegrator=0,originalClaimAccepted173Functions=23,originalClaimPrepared174Functions=4,packets=packets,identities=[dict(id=r['admittedIdentity'],program='',processor=r['processor'],module=r['module'],mode=r['mode'],address=r['address'],bytes=r['bytes'])for r in recipes()],files=files,generatorSources=[p for p in inputs['files']if p['role']=='generator'],frozenInputManifest=pin(INPUTS),independentReplay=pin(LANE/'copied-root.json'),limits=first['limits']+['The original failed ternary provider and every old/header/READY/proposal remain preserved. Only the faithful if/else source is proposed.','The four cohort174 rows remain classified by their frozen claim; only the coordinator may adopt this zero-credit migration after their shared acceptance.'])
    for p in files:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Final API packet pin changed')
    write_json(LANE/'ready.json',ready)
    print(dict(ready=(LANE/'ready.json').relative_to(ROOT).as_posix(),functions=27,preservedBytes=4812,inputFiles=len(paths),copiedRoot=replay['copiedRoot'],sourceCredit=0),flush=True)


if __name__=='__main__':main()
