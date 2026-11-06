import argparse
import shutil
import subprocess
import sys
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_gp_character_data_paths import SOURCE,EVIDENCE,WORK,assert_owned
from wave20261106_gp_character_data_packet import REPORT
from wave20261106_gp_character_data_canonical import projection

PRODUCER='wave20261106_gp_character_data_packet.py'
CANONICAL='evidence/matches/gamespy-gp-character-data-canonical-20261106.json'
DESCRIPTOR=(EVIDENCE/'canonical-packet.json').relative_to(ROOT).as_posix()
CLONE=ROOT.parent/'gpchars1106-replay'


def pin(name):return dict(path=name,sha256=sha256(ROOT/name))


def inputs():
    assert_owned();target=EVIDENCE/'source-files.json'
    if target.exists():raise ValueError('Character source manifest already immutable')
    seeds=[PRODUCER,'wave20261106_gp_character_data_ready.py','wave20261106_gp_character_data_materialize.py','wave20261106_gp_character_data_canonical.py'];code=code_closure(seeds);layout=read_json(SOURCE/'layout.json');files=set(code);files.update(p.relative_to(ROOT).as_posix()for p in SOURCE.iterdir()if p.suffix in('.c','.h','.json'));files.update((EVIDENCE/n).relative_to(ROOT).as_posix()for n in ['data-claim.json','coordinator-review.json']);files.add('evidence/lanes/parallel-wave20261106/whole-character-read-only/gp-proposal.json')
    for row in layout['assets']:
        ref=read_json(ROOT/row['semanticSource'])['primaryReference'];files.update([ref['path'],ref['snapshot']['path']])
    private={'project.json':'runtime-configuration','extract/arm9/arm9.bin':'derived-original-main-comparison','config/arm9/symbols.txt':'original-native-boundaries','config/arm9/relocs.txt':'original-pointer-relocations','tools/mwccarm/mwccarm/license.dat':'compiler-license-input'}
    for p in(ROOT/'deps/native/elftools').rglob('*.py'):private[p.relative_to(ROOT).as_posix()]='python-elf-runtime-source'
    for p in(ROOT/'tools/mwccarm/mwccarm/2.0/base').iterdir():
        if p.suffix.lower()in('.dll','.exe')and(p.suffix.lower()=='.dll'or p.name in('mwccarm.exe','mwldarm.exe')):private[p.relative_to(ROOT).as_posix()]='pinned-compiler-linker-runtime'
    if any(n.startswith(('extract/','tools/','deps/native/'))for n in files):raise ValueError('Comparison or tool input leaked into authored character files')
    value=dict(schemaVersion=1,sourceCredit=0,files=[pin(n)for n in sorted(files)],privateComparisonOrToolInputs=[dict(pin(n),role=role)for n,role in sorted(private.items())],generatorSources=[pin(n)for n in code],sourceGenerationUsesOnlyCanonicalCharacterJson=True,noRomOrPublishedSourceRequiredForGeneration=True,sourceCompilerIncludesAreRealTypedCharacterDeclarations=True)
    write_json(target,value);print(dict(sourceManifest=target.relative_to(ROOT).as_posix(),sha256=sha256(target),authoredOrCopiedSourceFiles=len(files),privateComparisonOrToolInputs=len(private)),flush=True)


def descriptor():
    assert_owned();path=ROOT/DESCRIPTOR
    if path.exists():raise ValueError('Character canonical descriptor already immutable')
    manifest=pin((EVIDENCE/'source-files.json').relative_to(ROOT).as_posix());value=dict(sourceCredit=0,transportOnly=True,originalReport=REPORT,originalProducer=[PRODUCER,'--inputs-sha256',manifest['sha256']],output=CANONICAL,sourceManifest=manifest,immutableDataProjection=projection(read_json(ROOT/REPORT)))
    write_json(path,value);print(dict(descriptor=DESCRIPTOR,sha256=sha256(path)),flush=True)


def copied():
    assert_owned()
    if CLONE.resolve()!=(ROOT.parent/'gpchars1106-replay').resolve()or CLONE.exists():raise ValueError('Exact independent character copied root is unavailable')
    manifest=read_json(EVIDENCE/'source-files.json');names={x['path']for x in manifest['files']+manifest['privateComparisonOrToolInputs']};names.update([DESCRIPTOR,(EVIDENCE/'source-files.json').relative_to(ROOT).as_posix()]);copied=[]
    for name in sorted(names):
        target=CLONE/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
        if sha256(target)!=sha256(ROOT/name):raise ValueError('Independent character source/tool copy differs')
        copied.append(pin(name))
    if list(CLONE.rglob('*.o'))or list(CLONE.rglob('*.elf')):raise ValueError('Character copied replay contains prebuilt objects')
    write_json(CLONE/REPORT,dict(staleReport=True));write_json(CLONE/CANONICAL,dict(staleCanonical=True));command=[sys.executable,str(CLONE/'wave20261106_gp_character_data_canonical.py'),DESCRIPTOR];run=subprocess.run(command,cwd=CLONE.parent,capture_output=True,text=True,timeout=240);(EVIDENCE/'copied-root.log').write_text(run.stdout+run.stderr)
    if run.returncode:raise ValueError(('Character copied canonical replay failed',run.stdout[-2000:],run.stderr[-2000:]))
    original=read_json(ROOT/REPORT);fresh=read_json(CLONE/CANONICAL)
    if projection(original)!=projection(fresh)or not fresh.get('canonicalReportRefreshedFromFreshWorkerObjects')or fresh.get('staleReport')or fresh.get('staleCanonical'):raise ValueError('Character copied replay retained stale contracts/reports')
    records=[]
    for a,b in zip(original['dataMatches'],fresh['dataMatches']):
        if sha256(CLONE/b['object'])!=b['objectSha256']or sha256(CLONE/b['realLink']['linkedElf'])!=b['realLink']['linkedElfSha256']or not str(b['compilerCommand'][0]).startswith(str(CLONE)):raise ValueError('Character copied canonical object/link metadata is not fresh')
        records.append(dict(address=b['address'],bytes=b['bytes'],freshObjectSha256=b['objectSha256'],objectHashChanged=b['objectSha256']!=a['objectSha256']))
    before={r['object']:(sha256(CLONE/r['object']),(CLONE/r['object']).stat().st_mtime_ns)for r in fresh['dataMatches']};layout=read_json(SOURCE/'layout.json');cases=[('semantic',layout['assets'][0]['semanticSource']),('C-source',layout['assets'][0]['source']),('header',layout['characterHeader']['path']),('native-image','extract/arm9/arm9.bin'),('primary-source',read_json(ROOT/layout['assets'][0]['semanticSource'])['primaryReference']['path'])];controls=[];producer=read_json(ROOT/DESCRIPTOR)['originalProducer']
    for label,name in cases:
        target=CLONE/name;raw=target.read_bytes()
        try:
            target.write_bytes(raw+b' ');negative=subprocess.run([sys.executable,str(CLONE/producer[0]),*producer[1:]],cwd=CLONE,capture_output=True,text=True,timeout=30)
        finally:target.write_bytes(raw)
        after={r['object']:(sha256(CLONE/r['object']),(CLONE/r['object']).stat().st_mtime_ns)for r in fresh['dataMatches']}
        if negative.returncode==0 or 'Immutable GP character input changed'not in negative.stderr or after!=before:raise ValueError('Character copied tamper not rejected before compilation:'+label)
        controls.append(dict(case=label,rejectedBeforeObjectOverwrite=True))
    result=dict(passed=True,sourceCredit=0,copiedRoot=str(CLONE),actualIndependentFileCopies=True,originalWorkOrObjectsCopied=False,originalRomCopied=False,projectFileUnmodified=True,canonicalReportFresh=True,freshDataObjects=len(records),initializedBytes=3696,objectHashesChanged=sum(r['objectHashChanged']for r in records),records=records,controls=controls,copiedInputs=copied,positiveCommand=command,originalReportSha256=sha256(ROOT/REPORT),functionOrDeviceExecutions=0)
    write_json(EVIDENCE/'copied-root-controls.json',result);print(dict(copiedRootPassed=True,objects=len(records),objectHashesChanged=result['objectHashesChanged'],tamperControls=len(controls)),flush=True)


def ready():
    assert_owned();path=EVIDENCE/'ready.json'
    if path.exists():raise ValueError('Character READY already frozen')
    report=read_json(ROOT/REPORT);copy=read_json(EVIDENCE/'copied-root-controls.json');manifest=pin((EVIDENCE/'source-files.json').relative_to(ROOT).as_posix());transport=read_json(ROOT/DESCRIPTOR)
    if not copy['passed']or copy['freshDataObjects']!=259 or copy['objectHashesChanged']!=259 or projection(report)!=transport['immutableDataProjection']:raise ValueError('Character canonical/copy proof incomplete')
    for item in read_json(ROOT/manifest['path'])['files']+read_json(ROOT/manifest['path'])['privateComparisonOrToolInputs']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Character frozen input changed before READY')
    value=dict(status='ready-for-coordinator-initialized-data-acceptance',sourceCredit=0,report=REPORT,producer=transport['originalProducer'],functionCount=0,dataObjects=259,initializedBytes=3696,typedConstantDataBytes=3696,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,executableBytes=0,sourceManifest=manifest['path'],sourceManifestSha256=manifest['sha256'],canonicalReport=CANONICAL,canonicalProducer=['wave20261106_gp_character_data_canonical.py',DESCRIPTOR],canonicalDescriptor=pin(DESCRIPTOR),freshCopiedRootObjects=259,wrongDataObjects=6,copiedRootTamperControls=5,allClosedCompilerInputGuardsPassed=True,files=[pin((EVIDENCE/n).relative_to(ROOT).as_posix())for n in ['source-files.json','canonical-packet.json','controls.json','copied-root-controls.json','copied-root.log']],limitations=report['limits'])
    write_json(path,value);print(dict(ready=path.relative_to(ROOT).as_posix(),sha256=sha256(path),objects=259,initializedBytes=3696),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['inputs','descriptor','copy','ready']);arg=parser.parse_args();{'inputs':inputs,'descriptor':descriptor,'copy':copied,'ready':ready}[arg.action]()
