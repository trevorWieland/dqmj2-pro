import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from seal_recovery_evidence_20261031 import code_closure
from goal_resume_material_pivot import SOURCE,LANE,WORK,AUDIT

PRODUCER='goal_resume_material_pivot_proof.py'
REPORTS=['evidence/matches/goal-resume20261107-material-pivot-data68.json','evidence/matches/goal-resume20261107-material-pivot-migrations2280.json']


def pin(path,role=None):
    path=Path(path);name=path.relative_to(ROOT).as_posix()if path.is_absolute()else path.as_posix();result=dict(path=name,sha256=sha256(ROOT/name))
    if role:result['role']=role
    return result


def freeze():
    destination=LANE/'inputs.json'
    if destination.exists():
        value=read_json(destination)
        for p in value['files']:
            if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Frozen material/pivot input changed')
        return value
    generators=set(code_closure([PRODUCER]));paths=set(generators);old=read_json(ROOT/'evidence/lanes/parallel-wave20261107/ctype-ascii-data-source1/inputs.json');paths.update(p['path']for p in old['files']if p['path'].startswith(('tools/','deps/')))
    paths.update(p.relative_to(ROOT).as_posix()for p in SOURCE.rglob('*')if p.is_file());paths.update(p['path']for p in read_json(AUDIT/'seal.json')['files']);paths.add((AUDIT/'seal.json').relative_to(ROOT).as_posix())
    for ref in read_json(LANE/'reference-contracts.json')['entries']:
        paths.add(ref['source']);paths.update(p['path']for p in ref['sourceDependencies'])
    paths.update(['project.json','extract/arm9/arm9.bin','config/arm9/symbols.txt','provenance/seed-manifest.json']);paths.update((LANE/name).relative_to(ROOT).as_posix()for name in['claim.json','reference-contracts.json','views.json'])
    if any(p.startswith('work/')or p.endswith('.o')for p in paths):raise ValueError('Independent material inputs contain cached objects/work outputs')
    value=dict(schemaVersion=1,status='frozen-independent-material-pivot-inputs',sourceCredit=0,historicalObjectsCopied=False,files=[pin(p,'generator'if p in generators else'private-runtime'if p.startswith(('tools/','deps/'))else'frozen-input')for p in sorted(paths)]);write_json(destination,value);return value


def invoke(root,log):
    command=[sys.executable,str(root/PRODUCER)];process=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=300,env=dict(os.environ,PYTHONPATH=''));log.write_text(process.stdout+process.stderr)
    if process.returncode:raise ValueError(('Independent material/pivot proof failed',str(log),process.returncode))
    return command


def main():
    if(LANE/'ready.json').exists():raise ValueError('Sealed material/pivot packet is immutable')
    inputs=freeze();invoke(ROOT,LANE/'main-proof.log');clone=ROOT/'work/copied-root-replays'/('s1mat-'+uuid.uuid4().hex[:4]);paths={p['path']for p in inputs['files']}|{(LANE/'inputs.json').relative_to(ROOT).as_posix()}
    if clone.exists():raise ValueError('Independent material copied root exists')
    for name in sorted(paths):
        target=clone/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
        if sha256(target)!=sha256(ROOT/name):raise ValueError('Independent material copied input differs')
    command=invoke(clone,LANE/'copied-proof.log');first=read_json(LANE/'qualification.json');second=read_json(clone/LANE.relative_to(ROOT)/'qualification.json')
    if first['generatedTrace']['uncompressedSha256']!=second['generatedTrace']['uncompressedSha256']:raise ValueError('Independent material full observation trace differs')
    geometry=lambda v:(v['data']['address'],v['data']['sourceSha256'],v['data']['targetSha256'],v['data']['bytes'],v['data']['sourceSectionAlignment'],[(r['address'],r['sourceSha256'],r['targetSha256'],r['bytes'])for r in v['migrations']])
    if geometry(first)!=geometry(second):raise ValueError('Independent material source/native geometry differs')
    write_json(LANE/'copied-qualification.json',second);artifacts=[]
    for path in sorted((clone/WORK.relative_to(ROOT)).rglob('*')):
        if path.is_file():
            target=WORK/'copied-output'/path.relative_to(clone/WORK.relative_to(ROOT));target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target);artifacts.append(dict(historicalPath=path.relative_to(clone).as_posix(),preservedPath=target.relative_to(ROOT).as_posix(),sha256=sha256(target)))
    replay=dict(status='passed',copiedRoot=clone.relative_to(ROOT).as_posix(),command=command,frozenInputFiles=len(paths),frozenInputBytes=sum((ROOT/name).stat().st_size for name in paths),historicalObjectsCopied=False,workOutputsCopied=False,originalRepositoryUsedAsRuntimeRoot=False,freshConsumerCompiles=4,freshPositiveDataObjects=1,freshWrongDataObjects=2,genuineNativeLinks=7,initializedDataBytes=68,migrationFunctions=2,migrationBytes=2280,newFunctionCredit=0,readerPairs=second['readerPairs'],actualReaderReturns=second['actualReaderReturns'],actualThumbHelperReturnsPerSide=second['actualThumbHelperReturnsPerSide'],traceSha256=second['generatedTrace']['uncompressedSha256'],preservedArtifacts=artifacts);write_json(LANE/'copied-root.json',replay)
    interface=dict(status='proposed-coupled-mathematical-data-and-zero-credit-view-interface',expectedInitializedObjects=1,expectedInitializedBytes=68,expectedMigrationFunctions=2,expectedMigrationBytes=2280,acceptedFunctionCountDelta=0,acceptedFunctionByteDelta=0,registration='Coordinator-owned pure dataMatches registration plus exactly two reviewed source-view preferences; no worker shared edits.',requiredChecks=['Exact admitted main/ARM9 data020d9068/68B and ARM0202fde0/1160B plus0203048c/1120B identities only','Every prior selected data/function identity and unchanged2512636-byte denominator preserved, with no physical overlap','All other original/header/object/producers unchanged; canonical const unsigned-long4 masks[8] plusu8 pivots[9][4] header closure','Fresh unchanged per-unit recipes, whole allocated/symbol/raw-relocation contracts and genuine MW links for old/new complete consumers','Independent mathematical data generation, exact68B read-only STT_OBJECT with no allocated relocs/functions/BSS/padding and genuine native data placement','416 original/fresh model pairs, actual288 Thumb helper returns per side, compiled wrong-data/type controls and no execution of unsupported pivots9..15','Independent input-only replay; existing full20-module/container/committed-source checks remain mandatory'],dataReport=REPORTS[0],migrationReport=REPORTS[1],frozenSDK562AndCtype640PoliciesUnchanged=True,sourceCredit=0);write_json(LANE/'admission-interface.json',interface)
    files=[dict(p)for p in inputs['files']]+[pin(Path(__file__),'packet-generator')];files.extend(pin(LANE/name,'produced-evidence')for name in['inputs.json','common-header-closure.json','qualification.json','traces.json.gz','main-proof.log','copied-root.json','copied-proof.log','copied-qualification.json','admission-interface.json','consumers-qualified.json']);files.extend(pin(p,'canonical-report')for p in REPORTS)
    for p in files:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Final material/pivot packet pin differs')
    claim=read_json(LANE/'claim.json');ready=dict(schemaVersion=1,status='ready-for-coordinator-acceptance',romSha256=configuration()['romSha256'],functions=0,bytes=68,initializedDataObjects=1,initializedDataBytes=68,ordinaryFunctionCredit=0,newFunctionCredit=0,zeroCreditMigrationFunctions=2,zeroCreditMigrationBytes=2280,acceptedFunctionCountDelta=0,acceptedFunctionByteDelta=0,executableSectionBytes=0,allocatedZeroFillBytes=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,sourceCreditPendingIntegrator=0,coupledDataAndZeroCreditMigration=True,packets=[dict(report=p,producer=[sys.executable,PRODUCER])for p in REPORTS],canonicalReports=REPORTS,canonicalProducer=[sys.executable,PRODUCER],claimedStorage=claim['claimedStorage'],migrationFunctions=claim['migrationFunctions'],files=files,generatorSources=[p for p in inputs['files']if p['role']=='generator'],frozenInputManifest=pin(LANE/'inputs.json'),independentReplay=pin(LANE/'copied-root.json'),admissionInterface=pin(LANE/'admission-interface.json'),limits=first['limits']);write_json(LANE/'ready.json',ready)
    print(dict(ready=(LANE/'ready.json').relative_to(ROOT).as_posix(),dataObjects=1,initializedBytes=68,migrationFunctions=2,zeroCreditBytes=2280,inputFiles=len(paths),copiedRoot=replay['copiedRoot'],sourceCredit=0),flush=True)


if __name__=='__main__':main()
