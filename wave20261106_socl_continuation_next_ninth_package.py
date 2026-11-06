import json
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT,sha256,read_json,write_json
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_socl_continuation_next_ninth_models import NAMES
import wave20261104_ov005_package as copy_template

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/ninth'
SOURCE='src/runtime/parallel_wave20261105/socl-continuation-next/ninth/'
CLONE=ROOT/'work/w6sc/ninth-copy'
PRODUCER='wave20261106_socl_continuation_next_ninth_proof.py'


def pin(name,role=None):
    value=dict(path=name,sha256=sha256(ROOT/name))
    if role:value['role']=role
    return value


def paths():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/ninth' or SOURCE!='src/runtime/parallel_wave20261105/socl-continuation-next/ninth/' or CLONE!=ROOT/'work/w6sc/ninth-copy':raise ValueError('Exact fresh packet source/evidence/work paths differ')
    if (LANE/'ready.json').exists():raise ValueError('READY packet is immutable')


def prepare():
    paths();claim=read_json(LANE.parent/'claim.json');selected=[]
    for row in claim['claimedFunctions']:
        name=format(int(row['address'],0),'08x')
        if name in NAMES:selected.append({k:row[k] for k in ['id','program','processor','module','mode','address','bytes','targetSha256','inputModuleSha256']}|dict(source=SOURCE+name+'.c',sourceSha256=sha256(ROOT/(SOURCE+name+'.c'))))
    if len(selected)!=3 or sum(r['bytes'] for r in selected)!=376:raise ValueError('Exact closed subset differs from exclusive ownership')
    names=set(code_closure([PRODUCER]))|{r['source'] for r in selected}|{SOURCE+'context.h'}
    mandatory=['project.json','provenance/seed-manifest.json','config/arm9/symbols.txt','config/arm9/relocs.txt','evidence/lanes/parallel-wave20261105/socl-continuation-next/ninth/native-inputs.json']
    reference='deps/reference/nitrowifi-e6048fc29448-socl-continuation-next/reference-manifest.json'
    mandatory+=[reference,'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/include/nitroWiFi/socl.h','deps/reference/nitrowifi-e6048fc29448-socket-socl-command/reference-manifest.json']
    names.update(p['path'] for p in read_json(ROOT/reference)['files'])
    names.update(mandatory);names.update(['extract/arm9/arm9.bin','tools/mwccarm/mwccarm/license.dat'])
    for profile,executable in [('2.0/base','mwldarm.exe'),('2.0/sp1p6','mwccarm.exe')]:
        names.update('tools/mwccarm/mwccarm/'+profile+'/'+n for n in [executable,'ELFIO.dll','lmgr8c.dll','MSL_All-DLL80_x86.dll'])
    names.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'deps/native').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
    files=[pin(n,'source' if n.startswith(SOURCE) else 'generator' if n.endswith('.py') and not n.startswith('deps/') else 'private-runtime' if n.startswith(('deps/','tools/','extract/')) else 'frozen-input') for n in sorted(names)]
    write_json(LANE/'inputs.json',dict(schemaVersion=1,romSha256=claim['claimedFunctions'][0]['id'].split('/')[0],entries=selected,files=files,mandatoryExternalInputs=[pin(n) for n in mandatory],limits=['Actual owned C/header are the compiler source inputs. Native image/inventories/tool binaries/dependency runtime are local validation provenance with zero source credit. Claim, admission epochs and mutable dispatch are not runtime inputs.']))
    print(dict(files=len(files),functions=3,bytes=376),flush=True)


def execute():
    paths();subprocess.run([sys.executable,str(ROOT/PRODUCER)],cwd=ROOT,check=True)
    copy_template.LANE,copy_template.CLONE,copy_template.PRODUCER=LANE,CLONE,PRODUCER;copy_template.copied_root()
    report=read_json(LANE/'match.json');inputs=read_json(LANE/'inputs.json');identities=[]
    for row in report['matches']:
        item={k:row[k] for k in ['processor','program','module','mode','address','bytes','source','sourceSha256','targetSha256']};item['id']=report['romSha256']+'/arm9/main/thumb/'+format(int(row['address'],0),'08x');identities.append(item)
    descriptor=LANE/'canonical-packet.json';canonical='evidence/matches/parallel-wave20261106-socl-continuation-next-ninth.json'
    write_json(descriptor,dict(romSha256=report['romSha256'],producer=[PRODUCER],workerReport=(LANE/'match.json').relative_to(ROOT).as_posix(),canonicalReport=canonical,frozenInputs=[pin((LANE/'inputs.json').relative_to(ROOT).as_posix())]+inputs['mandatoryExternalInputs'],identities=identities))
    subprocess.run([sys.executable,str(ROOT/'replay_parallel_packet.py'),descriptor.relative_to(ROOT).as_posix()],cwd=ROOT,check=True)
    for name in code_closure(['replay_parallel_packet.py'])+[descriptor.relative_to(ROOT).as_posix()]:
        target=CLONE/name;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() and sha256(target)!=sha256(ROOT/name):raise ValueError('Copied canonical source conflict')
        shutil.copyfile(ROOT/name,target)
    command=[sys.executable,str(CLONE/'replay_parallel_packet.py'),descriptor.relative_to(ROOT).as_posix()];process=subprocess.run(command,cwd=CLONE,capture_output=True,text=True,timeout=240);(LANE/'canonical-copied-root.log').write_text(process.stdout+process.stderr)
    if process.returncode:raise ValueError(('Copied canonical replay failed',process.stdout,process.stderr))
    first=read_json(ROOT/canonical);second=read_json(CLONE/canonical)
    if first['generatedTrace']['uncompressedSha256']!=second['generatedTrace']['uncompressedSha256']:raise ValueError('Copied canonical fixture traces differ')
    if len(second['matches'])!=3 or any(not r['realLink']['exactCallerBytes'] for r in second['matches']):raise ValueError('Fresh copied canonical links incomplete')
    write_json(LANE/'canonical-copied-root.json',dict(status='passed',sourceCredit=0,command=command,processExitCode=0,functions=3,bytes=376,descriptor=pin(descriptor.relative_to(ROOT).as_posix()),actualNativeAndSourceCallerReturns=second['actualNativeAndSourceCallerReturns'],traceSha256=second['generatedTrace']['uncompressedSha256'],workProductsCopied=False,log=pin((LANE/'canonical-copied-root.log').relative_to(ROOT).as_posix())))
    files=list(inputs['files'])
    for name,role in [('inputs.json','input-manifest'),('match.json','produced-report'),('canonical-packet.json','canonical-descriptor'),('traces.json.gz','produced-trace'),('binding-layout-controls.json','produced-controls'),('copied-root.json','diagnostic-proof'),('copied-root.log','diagnostic-log'),('canonical-copied-root.json','diagnostic-proof'),('canonical-copied-root.log','diagnostic-log')]:files.append(pin((LANE/name).relative_to(ROOT).as_posix(),role))
    files.extend([pin(canonical,'produced-report'),pin(Path(__file__).name,'diagnostic-generator')])
    write_json(LANE/'ready.json',dict(schemaVersion=1,status='ready-for-coordinator-acceptance',acceptedBaselineCohort=165,functions=3,bytes=376,sourceCreditPendingIntegrator=376,romSha256=report['romSha256'],packets=[dict(report=canonical,producer=[PRODUCER])],canonicalDescriptor=pin(descriptor.relative_to(ROOT).as_posix()),identities=identities,files=files,generatorSources=[p for p in inputs['files'] if p['role']=='generator'],frozenInputManifest=pin((LANE/'inputs.json').relative_to(ROOT).as_posix()),admissionProvenance=pin((LANE.parent/'claim.json').relative_to(ROOT).as_posix()),limits=report['limits']))
    print(dict(ready=pin((LANE/'ready.json').relative_to(ROOT).as_posix()),functions=3,bytes=376),flush=True)


if __name__=='__main__':{'prepare':prepare,'execute':execute}[sys.argv[1]]()
