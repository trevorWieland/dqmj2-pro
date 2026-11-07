import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from project import ROOT, read_json, sha256, write_json
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261106/goal-resume-source-1/resource-display'
WORK = ROOT / 'work/goal-resume-20261106/source-1/resource-display-proof'
PRODUCER = 'goal_resume_source1_resource_display_proof.py'
CANONICAL = 'evidence/matches/goal-resume20261106-source1-resource-display.json'


def pin(path,role=None):
    result=dict(path=path,sha256=sha256(ROOT/path))
    if role:
        result['role']=role
    return result


def freeze():
    if (LANE/'ready.json').exists():
        raise ValueError('READY resource-display packet is immutable')
    path=LANE/'inputs.json'
    if path.exists():
        inputs=read_json(path)
        for item in inputs['files']:
            if sha256(ROOT/item['path'])!=item['sha256']:
                raise ValueError('Frozen resource-display input changed')
        return inputs
    prior=read_json(LANE.parent/'first-toggle/inputs.json')
    runtime={item['path'] for item in prior['files'] if item['path'].startswith('tools/') or
        item['path'].startswith(('deps/native/unicorn/','deps/native/elftools/')) and Path(item['path']).suffix in ('.py','.dll')}
    generators=set(code_closure([PRODUCER,'replay_parallel_packet.py']))
    mandatory=[dict(item) for item in prior['mandatoryExternalInputs']]
    paths=runtime|generators|{item['path'] for item in mandatory}
    paths.update(['src/runtime/goal_resume20261106/source_1/tail/020724f4.c',
        'src/runtime/goal_resume20261106/source_1/tail/resource_display.h',
        'src/runtime/runtime07/native_main_02061dcc.c',
        'src/runtime/runtime06/native_main_02049ffc.c',
        'src/runtime/runtime08/native_main_0204abd4.c','src/runtime/runtime08/native_main_02049ad0.c'])
    inputs=dict(schemaVersion=1,status='frozen-whole-resource-display-proof-inputs',sourceCredit=0,
        mandatoryExternalInputs=mandatory,files=[pin(name,'generator' if name in generators else 'private-runtime' if name in runtime else 'frozen-input') for name in sorted(paths)])
    write_json(path,inputs)
    return inputs


def main():
    LANE.mkdir(parents=True,exist_ok=True)
    inputs=freeze()
    subprocess.run([sys.executable,str(ROOT/PRODUCER)],cwd=ROOT,check=True)
    report=read_json(LANE/'match.json')
    row=report['matches'][0]
    identity={key:row[key] for key in ('program','processor','module','mode','address','bytes','source','sourceSha256','targetSha256')}
    identity['id']=report['romSha256']+'/arm9/main/arm/020724f4'
    descriptor=LANE/'canonical-packet.json'
    write_json(descriptor,dict(romSha256=report['romSha256'],producer=[PRODUCER],
        workerReport=(LANE/'match.json').relative_to(ROOT).as_posix(),canonicalReport=CANONICAL,
        frozenInputs=[pin((LANE/'inputs.json').relative_to(ROOT).as_posix()),*inputs['mandatoryExternalInputs']],identities=[identity]))
    command=[sys.executable,str(ROOT/'replay_parallel_packet.py'),descriptor.relative_to(ROOT).as_posix()]
    subprocess.run(command,cwd=ROOT,check=True)
    clone=ROOT/'work/copied-root-replays'/('s1d-'+uuid.uuid4().hex[:4])
    if clone.exists():
        raise ValueError('Independent resource-display replay root already exists')
    paths={item['path'] for item in inputs['files']}
    paths.update([(LANE/'inputs.json').relative_to(ROOT).as_posix(),descriptor.relative_to(ROOT).as_posix()])
    for name in sorted(paths):
        target=clone/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/name,target)
        if sha256(target)!=sha256(ROOT/name):
            raise ValueError('Copied immutable resource-display input hash differs')
    copied_command=[sys.executable,str(clone/'replay_parallel_packet.py'),descriptor.relative_to(ROOT).as_posix()]
    process=subprocess.run(copied_command,cwd=clone,capture_output=True,text=True,timeout=240)
    (LANE/'copied-root.log').write_text(process.stdout+process.stderr)
    if process.returncode:
        raise ValueError('Independent copied-root canonical resource-display proof failed')
    first,second=read_json(ROOT/CANONICAL),read_json(clone/CANONICAL)
    if first['generatedTrace']['uncompressedSha256']!=second['generatedTrace']['uncompressedSha256']:
        raise ValueError('Fresh independent resource-display trace differs')
    if len(second['matches'])!=1 or not second['matches'][0]['realLink']['exactCallerBytes'] or second['actualNativeAndSourceCallerReturns']!=160:
        raise ValueError('Fresh whole resource-display match or actual fixture returns missing')
    artifacts=[]
    for path in sorted((clone/WORK.relative_to(ROOT)).rglob('*')):
        if path.is_file():
            target=WORK/'copied-output'/path.relative_to(clone/WORK.relative_to(ROOT))
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(path,target)
            artifacts.append(dict(historicalPath=path.relative_to(clone).as_posix(),preservedPath=target.relative_to(ROOT).as_posix(),sha256=sha256(target)))
    write_json(LANE/'copied-root-match.json',second)
    replay=dict(status='passed',sourceCredit=0,copiedRoot=clone.relative_to(ROOT).as_posix(),command=copied_command,
        frozenInputFiles=len(paths),frozenInputBytes=sum((ROOT/name).stat().st_size for name in paths),
        workProductsCopied=False,originalRepositoryUsedAsRuntimeRoot=False,actualNativeAndSourceCallerReturns=160,
        actualNativeHelperReturnsPerSide=300,traceSha256=second['generatedTrace']['uncompressedSha256'],
        originalObjectSha256=first['matches'][0]['objectSha256'],freshObjectSha256=second['matches'][0]['objectSha256'],preservedArtifacts=artifacts)
    write_json(LANE/'copied-root.json',replay)
    files=list(inputs['files'])
    files.extend(pin((LANE/name).relative_to(ROOT).as_posix(),'produced-evidence') for name in ['inputs.json','match.json',
        'canonical-packet.json','traces.json.gz','binding-controls.json','prototype-control.json',
        'copied-root.json','copied-root.log','copied-root-match.json'])
    files.extend([pin(CANONICAL,'produced-report'),pin('goal_resume_source1_resource_display_packet.py','diagnostic-generator')])
    write_json(LANE/'ready.json',dict(schemaVersion=1,status='ready-for-coordinator-acceptance',acceptedBaselineCohort=172,
        functions=1,bytes=116,sourceCreditPendingIntegrator=148,romSha256=report['romSha256'],
        packets=[dict(report=CANONICAL,producer=[PRODUCER])],canonicalDescriptor=pin(descriptor.relative_to(ROOT).as_posix()),
        identities=[identity],files=files,generatorSources=[item for item in inputs['files'] if item['role']=='generator'],
        frozenInputManifest=pin((LANE/'inputs.json').relative_to(ROOT).as_posix()),
        admissionProvenance=pin('evidence/lanes/parallel-wave20261106/goal-resume-source-1/claim.json'),limits=report['limits']))
    print(dict(ready=(LANE/'ready.json').relative_to(ROOT).as_posix(),functions=1,bytes=116,copiedRoot=replay['copiedRoot'],frozenInputBytes=replay['frozenInputBytes']),flush=True)


if __name__=='__main__':
    main()
