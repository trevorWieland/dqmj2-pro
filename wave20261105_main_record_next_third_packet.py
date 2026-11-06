import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-record-next/third'
INPUT = LANE / 'inputs.json'
PRODUCER = 'wave20261105_main_record_next_third_match.py'
CANONICAL = 'evidence/matches/main-record-next-third-parallel-wave20261105.json'


def identity(row,rom):
    return dict(id=rom+'/arm9/main/arm/'+format(int(row['address'],0),'08x'),program='',processor='arm9',module='main',mode='arm',
        address=row['address'],bytes=row['bytes'],source=row['source'],sourceSha256=row['sourceSha256'],targetSha256=row['targetSha256'])


def prepare():
    from recover_linked_runtime import qualified_bindings
    from wave20261105_main_record_next_third_abi import VIEWS
    preliminary = read_json(LANE/'prelink.json')['matches']
    assert len(preliminary) == 1 and sum(row['bytes'] for row in preliminary) == 56
    entries = []
    for row in preliminary:
        item = {key:row[key] for key in ['address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerPath','compilerSha256']}
        item.update(flags=row['compilerFlags'],priorRelocations=row['relocations'],qualifiedDependencies=qualified_bindings(row),
            boundaryReturnContract='ARM R0 word',
            provenance=dict(typedStorageLayouts=[],reconstruction='Measured original control flow and raw scalar/bitfield accesses; ordinary C; no supplied callee source credit'),
            extraLayoutChecks=[dict(type='u8',bytes=1),dict(type='u32',bytes=4),dict(type='int',bytes=4),dict(type='void*',bytes=4)])
        entries.append(item)
    names = set(code_closure([PRODUCER]))
    prior = read_json(ROOT/'evidence/lanes/parallel-wave20261105/main-sdk-bulk/first/inputs.json')
    names.update(pin['path'] for pin in prior['files'] if pin['path'].startswith(('deps/native/','tools/mwccarm/')))
    names.update(['project.json','tools.lock.json','provenance/seed-manifest.json','extract/arm9/arm9.bin','config/arm9/symbols.txt','config/arm9/relocs.txt'])
    names.update(row[0] for row in VIEWS)
    for item in entries:
        names.add(item['source'])
        names.update(pin['path'] for pin in item['sourceDependencies'])
    document = dict(schemaVersion=1,romSha256=configuration()['romSha256'],moduleSha256=sha256(ROOT/'extract/arm9/arm9.bin'),
        ownershipOriginClaimSha256='29da44573f45db0d1b557f6f6f916ce89245c54be9c0d7e2563f0e794755e7f6',entries=entries,
        files=[dict(path=name,sha256=sha256(ROOT/name)) for name in sorted(names)],
        scope='One complete ordinary C host ARM9 main caller only; exploratory drafts and the remaining39 claimed functions are excluded from runtime inputs and credit.')
    if INPUT.exists():
        assert read_json(INPUT) == document
    write_json(INPUT,document)
    print(dict(inputs=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT),files=len(names)))


def descriptor():
    inputs = read_json(INPUT)
    body = dict(schemaVersion=1,romSha256=inputs['romSha256'],producer=[PRODUCER],workerReport=(LANE/'match.json').relative_to(ROOT).as_posix(),
        canonicalReport=CANONICAL,frozenInputs=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],
        identities=[identity(row,inputs['romSha256']) for row in inputs['entries']])
    path = LANE/'canonical.json'
    if path.exists():
        assert read_json(path) == body
    write_json(path,body)
    print(dict(descriptor=path.relative_to(ROOT).as_posix(),sha256=sha256(path)))


def copied_root():
    clone = ROOT/'work/w5rns3c1'
    assert not clone.exists(),'A copied-root audit must start fresh'
    inputs = read_json(INPUT)
    descriptor_name = (LANE/'canonical.json').relative_to(ROOT).as_posix()
    names = {pin['path'] for pin in inputs['files']}
    names.update(code_closure([PRODUCER,'replay_parallel_packet.py']))
    names.update([INPUT.relative_to(ROOT).as_posix(),descriptor_name])
    for name in sorted(names):
        source,target = ROOT/name,clone/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
        assert sha256(source) == sha256(target)
    assert not (clone/'work').exists() and not (clone/CANONICAL).exists() and not (clone/LANE.relative_to(ROOT)/'match.json').exists()
    result = subprocess.run([sys.executable,str(clone/'replay_parallel_packet.py'),descriptor_name],cwd=clone,capture_output=True,text=True,timeout=300)
    if result.returncode:
        write_json(LANE/'copy-failure.json',dict(exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr))
        raise ValueError('Copied-root record packet failed')
    report = read_json(clone/CANONICAL)
    objects = []
    for row in report['matches']:
        assert sha256(clone/row['object']) == row['objectSha256']
        assert Path(row['realLink']['linkerAttempt']['cwd']).is_relative_to(clone)
        assert row['ordinaryCBytes'] == row['bytes'] and row['justifiedAssemblyBytes'] == 0
        objects.append(dict(address=row['address'],object=row['object'],sha256=row['objectSha256']))
    assert len(objects) == 1 and report['matchedBytes'] == 56
    write_json(LANE/'copied-root.json',dict(allPassed=True,functions=1,bytes=56,freshCanonicalObjectsVerified=True,noInitialWorkWorkerOrCanonicalOutputs=True,
        allLinkerCwdsInsideCopiedRoot=True,immutableInputs=len(names),objects=objects,canonicalReportSha256=sha256(clone/CANONICAL),
        actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],suppliedCalleeSourceOrExecutionCredit=0,stdout=result.stdout,stderr=result.stderr))
    print(dict(copiedRootPassed=True,functions=1,bytes=56))


def ready():
    inputs,report,copied = read_json(INPUT),read_json(LANE/'match.json'),read_json(LANE/'copied-root.json')
    assert report['allPassed'] and copied['allPassed'] and report['matchedFunctions'] == 1 and report['matchedBytes'] == copied['bytes'] == 56
    names = {pin['path'] for pin in inputs['files']}
    names.update(code_closure([PRODUCER,Path(__file__).name,'replay_parallel_packet.py']))
    names.update((LANE/name).relative_to(ROOT).as_posix() for name in ['inputs.json','canonical.json','copied-root.json'])
    files = [dict(path=name,sha256=sha256(ROOT/name),kind='frozen-runtime-input-or-proof') for name in sorted(names)]
    files.append(dict(path=(LANE/'match.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'match.json'),kind='regenerated-worker-report'))
    body = dict(schemaVersion=1,status='ready-for-coordinator-acceptance',acceptedBaselineCohort=156,romSha256=inputs['romSha256'],functions=1,bytes=56,
        ordinaryCBytes=56,justifiedAssemblyBytes=0,packets=[dict(report=(LANE/'match.json').relative_to(ROOT).as_posix(),producer=[PRODUCER])],
        canonicalDescriptor=dict(path=(LANE/'canonical.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'canonical.json')),
        identities=[identity(row,inputs['romSha256']) for row in inputs['entries']],files=files,actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],
        suppliedCalleeSourceOrExecutionCredit=0,copiedRootFreshCanonicalReplayPassed=True,diagnosticInventoriesAreNotRuntimeInputs=True,
        sourceClassification='Ordinary C caller preserving full-word argument forwarding through an original trampoline',sourceCreditPendingSharedAcceptance=True,limits=report['limits'])
    path = LANE/'ready.json'
    if path.exists():
        assert read_json(path) == body
    write_json(path,body)
    print(dict(ready=path.relative_to(ROOT).as_posix(),sha256=sha256(path),functions=1,bytes=56,files=len(files)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action',choices=['prepare','descriptor','copied_root','ready'])
    globals()[parser.parse_args().action]()
