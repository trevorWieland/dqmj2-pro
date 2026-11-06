import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/push'
CLONE=ROOT.parent/'gt1105-push-replay'
PRODUCER='wave20261105_gamespy_thumb_next_push_packet.py'
CANONICAL='evidence/matches/parallel-wave20261105-gamespy-thumb-next-push.json'


def pin(path):return dict(path=path,sha256=sha256(ROOT/path))


def prepare():
    report=read_json(LANE/'match.json');manifest=read_json(LANE/'inputs.json')
    identities=[]
    for row in report['matches']:
        identity={k:row[k] for k in ['program','processor','module','mode','address','bytes','source','sourceSha256','targetSha256']}
        identity['id']=report['romSha256']+'/arm9/main/thumb/'+format(int(row['address'],0),'08x')
        identities.append(identity)
    producer=[PRODUCER,'--inputs-sha256',sha256(LANE/'inputs.json')]
    descriptor=dict(schemaVersion=1,romSha256=report['romSha256'],producer=producer,workerReport=(LANE/'match.json').relative_to(ROOT).as_posix(),canonicalReport=CANONICAL,frozenInputs=[pin((LANE/'inputs.json').relative_to(ROOT).as_posix()),*manifest['mandatoryExternalInputs']],identities=identities)
    path=LANE/'canonical-packet.json'
    if path.exists() and read_json(path)!=descriptor:raise ValueError('Canonical identity descriptor already exists')
    write_json(path,descriptor)
    selected={i['address'] for i in identities};claim=read_json(LANE/'claim.json')
    remaining=[dict(r,sourceCredit=0,state='reserved-unaccepted') for r in claim['claimedFunctions'] if r['address'] not in selected]
    write_json(LANE/'residual.json',dict(functions=remaining,remainingFunctions=len(remaining),remainingBytes=sum(r['bytes'] for r in remaining),closedPreparedFunctions=len(identities),closedPreparedBytes=sum(i['bytes'] for i in identities),sourceCredit=0,namespacePolicy='Plural-overlay original records refuse singular binding; never infer module from numeric address'))
    print(dict(descriptor=path.relative_to(ROOT).as_posix(),functions=len(identities),bytes=sum(i['bytes'] for i in identities)),flush=True)


def copied_root():
    if CLONE.exists():raise ValueError('Independent copied root already exists')
    manifest=read_json(LANE/'inputs.json');descriptor=read_json(LANE/'canonical-packet.json')
    names={p['path'] for p in manifest['files']}
    names.update(code_closure(['replay_parallel_packet.py']))
    names.update([(LANE/'inputs.json').relative_to(ROOT).as_posix(),(LANE/'canonical-packet.json').relative_to(ROOT).as_posix()])
    copies=[]
    for name in sorted(names):
        target=CLONE/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
        if sha256(target)!=sha256(ROOT/name):raise ValueError('Copied immutable input differs')
        copies.append(dict(path=name,sha256=sha256(target)))
    original=read_json(LANE/'match.json');stale=dict(original,staleCanonicalNegativeControl=True)
    for name in [descriptor['workerReport'],descriptor['canonicalReport']]:write_json(CLONE/name,stale)
    command=[sys.executable,str(CLONE/'replay_parallel_packet.py'),(LANE/'canonical-packet.json').relative_to(ROOT).as_posix()]
    process=subprocess.run(command,cwd=CLONE.parent,capture_output=True,text=True,timeout=240)
    (LANE/'copied-root.log').write_text(process.stdout+process.stderr)
    if process.returncode:raise ValueError(('Independent canonical replay failed',process.stdout[-1500:],process.stderr[-1500:]))
    fresh=read_json(CLONE/descriptor['canonicalReport']);worker=read_json(CLONE/descriptor['workerReport'])
    contracts=['program','processor','module','mode','address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compiler','compilerSha256','compilerFlags','nativeSymbolEntries']
    baseline={r['name']:r for r in original['matches']}
    if fresh['matches']!=worker['matches'] or fresh.get('staleCanonicalNegativeControl') or worker.get('staleCanonicalNegativeControl') or not fresh.get('canonicalReportRefreshedFromFreshWorkerObjects'):raise ValueError('Fresh canonical report retained stale metadata')
    if fresh.get('callerFixtureTraceSha256')!=original.get('callerFixtureTraceSha256'):raise ValueError('Copied complete getter traces differ')
    records=[]
    for row in fresh['matches']:
        previous=baseline[row['name']]
        if any(row.get(k)!=previous.get(k) for k in contracts):raise ValueError('Copied source/native/compiler/binding contract differs')
        proof=row['realLink']
        if not proof['linkerAttempt']['cwd'].startswith(str(CLONE)) or not proof['exactCallerBytes'] or sha256(CLONE/row['object'])!=row['objectSha256'] or sha256(CLONE/proof['linkedElf'])!=proof['linkedElfSha256'] or sha256(CLONE/proof['lcf'])!=proof['lcfSha256']:raise ValueError('Copied canonical object/link metadata is not freshly valid')
        records.append(dict(address=row['address'],bytes=row['bytes'],objectHashChanged=row['objectSha256']!=previous['objectSha256'],freshObjectSha256=row['objectSha256'],copiedRootLinkMetadataVerified=True))
    inventory=CLONE/'config/arm9/relocs.txt';original_inventory=inventory.read_bytes()
    before=[(r['object'],sha256(CLONE/r['object']),(CLONE/r['object']).stat().st_mtime_ns) for r in fresh['matches']]
    try:
        inventory.write_bytes(original_inventory+b'\n')
        negative=subprocess.run([sys.executable,str(CLONE/PRODUCER),*descriptor['producer'][1:]],cwd=CLONE,capture_output=True,text=True,timeout=60)
    finally:inventory.write_bytes(original_inventory)
    after=[(r['object'],sha256(CLONE/r['object']),(CLONE/r['object']).stat().st_mtime_ns) for r in fresh['matches']]
    if negative.returncode==0 or 'Immutable packet input changed' not in negative.stderr or before!=after:raise ValueError('Changed original relocation inventory was not rejected before compilation')
    result=dict(status='passed',copiedRoot=str(CLONE),command=command,exitCode=process.returncode,independentSourceAndToolCopies=True,originalWorkObjectsCopied=False,originalBuildProductsCopied=False,canonicalReportFresh=True,sourceAndNativeContractsIdentical=True,staleWorkerAndCanonicalReportsReplaced=True,immutableExternalInputMutationRejected=True,compilerObjectsUnchangedByRejectedInventory=True,negativeExitCode=negative.returncode,negativeStderr=negative.stderr,functions=len(records),bytes=sum(r['bytes'] for r in records),objectHashesChanged=sum(r['objectHashChanged'] for r in records),records=records,copiedFiles=copies,actualNativeAndSourceCallerReturns=original['actualNativeAndSourceCallerReturns'],nativeCalleeExecutions=original['nativeCalleeBodiesExecuted'],nativeDevicesOrScenesExecuted=0,canonicalReportSha256=sha256(CLONE/descriptor['canonicalReport']))
    write_json(LANE/'copied-root-canonical-bridge-proof.json',result)
    print(dict(status='copied-root-passed',functions=len(records),bytes=result['bytes'],objectHashesChanged=result['objectHashesChanged']),flush=True)


def ready():
    report=read_json(ROOT/CANONICAL);inputs=read_json(LANE/'inputs.json');copy=read_json(LANE/'copied-root-canonical-bridge-proof.json');descriptor=read_json(LANE/'canonical-packet.json')
    if copy['status']!='passed' or not report['allPassed']:raise ValueError('Canonical proof incomplete')
    for item in inputs['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Pre-freeze actual input changed: '+item['path'])
    names={p['path'] for p in inputs['files']};names.update(code_closure(['replay_parallel_packet.py']))
    names.update([(LANE/name).relative_to(ROOT).as_posix() for name in ['inputs.json','match.json','canonical-packet.json','binding-layout-controls.json','copied-root-canonical-bridge-proof.json','copied-root.log','residual.json','claim.json','caller-fixtures.json','derivation.json']])
    names.update([CANONICAL,Path(__file__).name])
    for name in names:
        if not (ROOT/name).is_file():raise ValueError('READY references missing actual file')
    value=dict(schemaVersion=1,status='ready-for-coordinator-acceptance',romSha256=report['romSha256'],functions=len(report['matches']),bytes=sum(r['bytes'] for r in report['matches']),sourceCreditPendingIntegrator=sum(r['bytes'] for r in report['matches']),packets=[dict(report=descriptor['workerReport'],producer=descriptor['producer'],producerargv=descriptor['producer'])],frozenInputManifest=pin((LANE/'inputs.json').relative_to(ROOT).as_posix()),canonicalDescriptor=pin((LANE/'canonical-packet.json').relative_to(ROOT).as_posix()),canonicalReplayCommand=['replay_parallel_packet.py',(LANE/'canonical-packet.json').relative_to(ROOT).as_posix()],identities=descriptor['identities'],files=[pin(n) for n in sorted(names)],generatorSources=inputs['generatorSources'],callerFixtureTraceSha256=report['callerFixtureTraceSha256'],copiedRootCanonicalReplayPassed=True,actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],nativeCalleeBodiesExecuted=report['nativeCalleeBodiesExecuted'],wholeCNegativeControlsRejected=report['wholeCNegativeControlsRejected'],actualStandaloneOriginalEntryExecutions=report['actualStandaloneOriginalEntryExecutions'],relocationsPreserved=sum(len(r['relocations']) for r in report['matches']),remainingFunctions=read_json(LANE/'residual.json')['remainingFunctions'],remainingBytes=read_json(LANE/'residual.json')['remainingBytes'],limits=report['limits'])
    path=LANE/'ready.json'
    if path.exists():raise ValueError('READY already frozen')
    write_json(path,value);print(dict(ready=path.relative_to(ROOT).as_posix(),sha256=sha256(path),pins=len(value['files']),functions=value['functions'],bytes=value['bytes']),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','copy','ready']);args=parser.parse_args()
    {'prepare':prepare,'copy':copied_root,'ready':ready}[args.action]()
