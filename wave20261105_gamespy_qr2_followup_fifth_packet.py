import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-followup/fifth'
INPUT=LANE/'inputs.json'
PRODUCER='wave20261105_gamespy_qr2_followup_fifth_match.py'
CANONICAL='evidence/matches/gamespy-qr2-followup-fifth-parallel-wave20261105.json'


def identity(row,rom):
    return dict(id=rom+'/arm9/main/thumb/'+format(int(row['address'],0),'08x'),program='',processor='arm9',module='main',mode='thumb',address=row['address'],bytes=row['bytes'],source=row['source'],sourceSha256=row['sourceSha256'],targetSha256=row['targetSha256'])


def prepare():
    preliminary=read_json(LANE/'initial.json')['matches'];derivation=read_json(LANE/'derivation.json');entries=[]
    assert len(preliminary)==7 and sum(row['bytes'] for row in preliminary)==536
    for row in preliminary:
        item={key:row[key] for key in ['address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerPath','compilerSha256','compilerFlags','relocations','nativeSymbolEntries']}
        original=next(value for value in derivation['entries'] if value['address']==row['address'])
        item.update(sourceProvenance=original,boundaryReturnContract='void'if row['address']in ['0x20b87a8','0x20b9270','0x20b9d40']else'ARM R0 word')
        entries.append(item)
    names=set(code_closure([PRODUCER]))
    prior=read_json(ROOT/'evidence/lanes/parallel-wave20261105/main-record-next/third/inputs.json')
    names.update(pin['path'] for pin in prior['files'] if pin['path'].startswith(('deps/native/','tools/mwccarm/')))
    names.update(['project.json','tools.lock.json','provenance/seed-manifest.json','extract/arm9/arm9.bin','config/arm9/symbols.txt','config/arm9/relocs.txt'])
    names.update((LANE/name).relative_to(ROOT).as_posix() for name in ['original-imports.json','native-inputs.json','derivation.json'])
    names.add('tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
    for item in entries:
        names.add(item['source']);names.update(pin['path'] for pin in item['sourceDependencies'])
    document=dict(schemaVersion=1,romSha256=configuration()['romSha256'],moduleSha256=sha256(ROOT/'extract/arm9/arm9.bin'),ownershipOriginClaimSha256='82b672360ee1ea01b686d5777902e3b832cc42d31b8d728868084192664699ef',
        entries=entries,files=[dict(path=name,sha256=sha256(ROOT/name)) for name in sorted(names)],scope='Only seven selected complete ordinary C transport/lifecycle callers; exact original imports, bounded1044-byte frame, signed progress/unsigned sizeof bounds and16-bit register-word views qualify whole explicit-C99 linked extents; no unselected inventories, probes, original objects or provider bodies are runtime inputs.')
    if INPUT.exists():assert read_json(INPUT)==document
    write_json(INPUT,document);print(dict(inputs=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT),files=len(names)))


def descriptor():
    inputs=read_json(INPUT);body=dict(schemaVersion=1,romSha256=inputs['romSha256'],producer=[PRODUCER],workerReport=(LANE/'match.json').relative_to(ROOT).as_posix(),canonicalReport=CANONICAL,
        frozenInputs=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],identities=[identity(row,inputs['romSha256']) for row in inputs['entries']])
    path=LANE/'canonical.json'
    if path.exists():assert read_json(path)==body
    write_json(path,body);print(dict(descriptor=path.relative_to(ROOT).as_posix(),sha256=sha256(path)))


def copied_root():
    clone=ROOT/'work/w5qfc5';assert not clone.exists(),'Copied-root audit must start without prior outputs'
    inputs=read_json(INPUT);descriptor_name=(LANE/'canonical.json').relative_to(ROOT).as_posix();names={pin['path'] for pin in inputs['files']}
    names.update(code_closure([PRODUCER,'replay_parallel_packet.py']));names.update([INPUT.relative_to(ROOT).as_posix(),descriptor_name])
    for name in sorted(names):
        source,target=ROOT/name,clone/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
        assert sha256(source)==sha256(target)
    assert not (clone/'work').exists() and not (clone/CANONICAL).exists() and not (clone/LANE.relative_to(ROOT)/'match.json').exists()
    result=subprocess.run([sys.executable,str(clone/'replay_parallel_packet.py'),descriptor_name],cwd=clone,capture_output=True,text=True,timeout=300)
    if result.returncode:
        write_json(LANE/'copy-failure.json',dict(exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr));raise ValueError('Fresh copied-root Thumb packet failed')
    report=read_json(clone/CANONICAL);objects=[]
    for row in report['matches']:
        assert sha256(clone/row['object'])==row['objectSha256'] and Path(row['realLink']['linkerAttempt']['cwd']).is_relative_to(clone)
        assert row['ordinaryCBytes']==row['bytes'] and row['justifiedAssemblyBytes']==0
        objects.append(dict(address=row['address'],object=row['object'],sha256=row['objectSha256']))
    assert len(objects)==7 and report['matchedBytes']==536
    write_json(LANE/'copied-root.json',dict(allPassed=True,functions=7,bytes=536,freshCanonicalObjectsVerified=True,noInitialWorkWorkerOrCanonicalOutputs=True,
        allLinkerCwdsInsideCopiedRoot=True,immutableInputs=len(names),objects=objects,canonicalReportSha256=sha256(clone/CANONICAL),
        actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],suppliedCalleeSourceOrExecutionCredit=0,stdout=result.stdout,stderr=result.stderr))
    print(dict(copiedRootPassed=True,functions=7,bytes=536))


def ready():
    inputs,report,copied=read_json(INPUT),read_json(LANE/'match.json'),read_json(LANE/'copied-root.json')
    assert report['allPassed'] and copied['allPassed'] and report['matchedFunctions']==7 and report['matchedBytes']==copied['bytes']==536
    names={pin['path'] for pin in inputs['files']};names.update(code_closure([PRODUCER,Path(__file__).name,'replay_parallel_packet.py']))
    names.update((LANE/name).relative_to(ROOT).as_posix() for name in ['inputs.json','canonical.json','copied-root.json'])
    files=[dict(path=name,sha256=sha256(ROOT/name),kind='frozen-runtime-input-or-proof') for name in sorted(names)]
    files.append(dict(path=(LANE/'match.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'match.json'),kind='regenerated-worker-report'))
    body=dict(schemaVersion=1,status='ready-for-coordinator-acceptance',acceptedBaselineCohort=160,romSha256=inputs['romSha256'],functions=7,bytes=536,
        ordinaryCBytes=536,justifiedAssemblyBytes=0,packets=[dict(report=(LANE/'match.json').relative_to(ROOT).as_posix(),producer=[PRODUCER])],
        canonicalDescriptor=dict(path=(LANE/'canonical.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'canonical.json')),
        identities=[identity(row,inputs['romSha256']) for row in inputs['entries']],files=files,actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],
        suppliedCalleeSourceOrExecutionCredit=0,copiedRootFreshCanonicalReplayPassed=True,diagnosticInventoriesAreNotRuntimeInputs=True,sourceCreditPendingSharedAcceptance=True,limits=report['limits'])
    path=LANE/'ready.json'
    if path.exists():assert read_json(path)==body
    write_json(path,body);print(dict(ready=path.relative_to(ROOT).as_posix(),sha256=sha256(path),functions=7,bytes=536,files=len(files)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','descriptor','copied_root','ready']);globals()[parser.parse_args().action]()
