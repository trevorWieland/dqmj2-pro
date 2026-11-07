import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from seal_recovery_evidence_20261031 import code_closure
from goal_resume_ctype_ascii_data import SOURCE,LANE,WORK,AUDIT

PRODUCER='goal_resume_ctype_ascii_proof.py'
REPORT='evidence/matches/goal-resume20261107-ctype-ascii-data640.json'


def pin(path,role=None):
    path=Path(path);name=path.relative_to(ROOT).as_posix()if path.is_absolute()else path.as_posix();value=dict(path=name,sha256=sha256(ROOT/name))
    if role:value['role']=role
    return value


def freeze():
    destination=LANE/'inputs.json'
    if destination.exists():
        value=read_json(destination)
        for p in value['files']:
            if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Frozen independent ctype input changed')
        return value
    generators=set(code_closure([PRODUCER]));generators.add((AUDIT/'native_bounds.py').relative_to(ROOT).as_posix());paths=set(generators)
    old=read_json(ROOT/'evidence/lanes/parallel-wave20261107/resource-path-api-migration/inputs-replay.json');paths.update(p['path']for p in old['files']if p['path'].startswith(('tools/','deps/')))
    paths.update(p.relative_to(ROOT).as_posix()for p in SOURCE.iterdir()if p.is_file());paths.update(p['path']for p in read_json(AUDIT/'seal.json')['files']);paths.add((AUDIT/'seal.json').relative_to(ROOT).as_posix())
    paths.update(['project.json','extract/arm9/arm9.bin',(LANE/'claim.json').relative_to(ROOT).as_posix(),(LANE/'source-generation.json').relative_to(ROOT).as_posix()])
    if any(p.startswith('work/')or p.endswith('.o')for p in paths):raise ValueError('Data replay contains historical objects or work outputs')
    value=dict(schemaVersion=1,status='frozen-independent-ASCII-data640-inputs',sourceCredit=0,historicalObjectsCopied=False,files=[pin(p,'generator'if p in generators else'private-runtime'if p.startswith(('tools/','deps/'))else'frozen-input')for p in sorted(paths)])
    write_json(destination,value);return value


def invoke(root,log):
    command=[sys.executable,str(root/PRODUCER)];process=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=300,env=dict(os.environ,PYTHONPATH=''));log.write_text(process.stdout+process.stderr)
    if process.returncode:raise ValueError(('Independent ctype data proof failed',str(log),process.returncode))
    return command


def main():
    if(LANE/'ready.json').exists():raise ValueError('Sealed ctype data packet is immutable')
    inputs=freeze();invoke(ROOT,LANE/'main-proof.log');clone=ROOT/'work/copied-root-replays'/('s1ctype-'+uuid.uuid4().hex[:4]);paths={p['path']for p in inputs['files']}|{(LANE/'inputs.json').relative_to(ROOT).as_posix()}
    if clone.exists():raise ValueError('Independent ctype copied root exists')
    for name in sorted(paths):
        target=clone/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
        if sha256(target)!=sha256(ROOT/name):raise ValueError('Independent ctype copied input differs')
    command=invoke(clone,LANE/'copied-proof.log');first=read_json(LANE/'qualification.json');second=read_json(clone/LANE.relative_to(ROOT)/'qualification.json')
    if first['generatedTrace']['uncompressedSha256']!=second['generatedTrace']['uncompressedSha256']:raise ValueError('Independent ctype full native observation trace differs')
    fields=lambda value:[(r['address'],r['sourceSha256'],r['targetSha256'],r['bytes'],r['sourceSectionAlignment'])for r in value['dataMatches']]
    if fields(first)!=fields(second):raise ValueError('Independent ctype source/data geometry differs')
    write_json(LANE/'copied-qualification.json',second);artifacts=[]
    for path in sorted((clone/WORK.relative_to(ROOT)).rglob('*')):
        if path.is_file():
            target=WORK/'copied-output'/path.relative_to(clone/WORK.relative_to(ROOT));target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target);artifacts.append(dict(historicalPath=path.relative_to(clone).as_posix(),preservedPath=target.relative_to(ROOT).as_posix(),sha256=sha256(target)))
    replay=dict(status='passed',copiedRoot=clone.relative_to(ROOT).as_posix(),command=command,frozenInputFiles=len(paths),frozenInputBytes=sum((ROOT/name).stat().st_size for name in paths),historicalObjectsCopied=False,workOutputsCopied=False,originalRepositoryUsedAsRuntimeRoot=False,freshDataObjects=3,freshWrongPredicateObjects=3,genuineNativeDataLinks=6,initializedDataBytes=640,readerPairs=second['actualOriginalAndCompiledDataReaderPairs'],actualReaderReturns=second['actualReaderReturns'],traceSha256=second['generatedTrace']['uncompressedSha256'],preservedArtifacts=artifacts)
    write_json(LANE/'copied-root.json',replay)
    admission=dict(status='proposed-coordinator-interface-no-shared-edits',dataFamily='bounded-ascii-ctype',expectedInitializedObjects=3,expectedInitializedBytes=640,expectedFunctions=0,expectedExecutableBytes=0,expectedZeroFillBytes=0,expectedAlignmentBytes=0,qualifierSignature='qualify(before_data,after_data,expected_data,selected_functions,directory)',requiredChecks=['Exact admitted3 full program/CPU/module/data identities and128/256/256B extents','All earlier data identities/source/object hashes preserved and no selected function source/object/extent change','Independent ASCII predicate generation with original input reads blocked; current self-contained C equals generated source','Fresh pinned compile, STT_OBJECT/read-only PROGBITS/natural widths/zero allocated relocs/code/BSS/padding','Genuine MW data placement plus776 original/compiled-data reader pairs and compiled wrong-predicate controls','No physical overlap with functions/storage/claims; unchanged2512636-byte denominator','Input-only replay and all existing shared20-module/container/committed closure gates'],report=REPORT,claim=pin(LANE/'claim.json'),qualification=pin(LANE/'qualification.json'),registration='Pure dataMatches report; recovery_registry registration and expectedDataAdditions composition are coordinator-owned.',existingPrecedents=['match_main_ascii_lower_data_20261031.py','qualify_mixed_source_reference_inputs_20261106.py','prepare_source_data_cohort_v8_20261106.py'],frozen562BPolicy='Existing SDK constant family claim/codec/qualifier/preparer remain unchanged. A new ctype-specific qualifier/composer or reviewed generic mathematical-data extension must enforce the above rules.')
    write_json(LANE/'admission-interface.json',admission)
    files=[dict(p)for p in inputs['files']]+[pin(Path(__file__),'packet-generator')]
    files.extend(pin(LANE/name,'produced-evidence')for name in['inputs.json','qualification.json','traces.json.gz','main-proof.log','copied-root.json','copied-proof.log','copied-qualification.json','admission-interface.json']);files.append(pin(REPORT,'canonical-report'))
    for p in files:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Final ctype packet pin changed')
    claim=read_json(LANE/'claim.json');ready=dict(schemaVersion=1,status='ready-for-coordinator-acceptance',romSha256=configuration()['romSha256'],functions=0,bytes=640,initializedDataObjects=3,initializedDataBytes=640,ordinaryFunctionCredit=0,executableSectionBytes=0,allocatedZeroFillBytes=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,sourceCreditPendingIntegrator=0,dataOnly=True,packets=[dict(report=REPORT,producer=[sys.executable,PRODUCER])],canonicalReport=REPORT,canonicalProducer=[sys.executable,PRODUCER],identities=[{k:r[k]for k in('id','program','processor','module','mode','section','address','bytes')}for r in claim['claimedStorage']],claimedStorage=claim['claimedStorage'],files=files,generatorSources=[p for p in inputs['files']if p['role']=='generator'],frozenInputManifest=pin(LANE/'inputs.json'),independentReplay=pin(LANE/'copied-root.json'),admissionInterface=pin(LANE/'admission-interface.json'),limits=first['limits'])
    write_json(LANE/'ready.json',ready)
    print(dict(ready=(LANE/'ready.json').relative_to(ROOT).as_posix(),objects=3,initializedBytes=640,inputFiles=len(paths),copiedRoot=replay['copiedRoot'],sourceCredit=0),flush=True)


if __name__=='__main__':main()
