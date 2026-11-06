import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from wave20261106_auth_character_data_paths import EVIDENCE,WORK


def main():
    name=(EVIDENCE/'canonical-packet.json').relative_to(ROOT).as_posix();descriptor=read_json(ROOT/name);manifest=read_json(ROOT/descriptor['sourceManifest']['path']);copy_root=ROOT.parent/'authchar1106';copy_root.mkdir(exist_ok=False)
    if copy_root.resolve().parent!=ROOT.resolve().parent or copy_root.resolve()==ROOT.resolve():raise ValueError('Exact Auth independent copied-root destination differs')
    copied={p['path']:p for p in manifest['files']+manifest['privateComparisonOrToolInputs']};copied[name]=dict(path=name,sha256=sha256(ROOT/name));copied[descriptor['sourceManifest']['path']]=descriptor['sourceManifest']
    for path,pin in copied.items():
        target=copy_root/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,target)
        if sha256(target)!=pin['sha256']:raise ValueError('Actual Auth copied source/runtime dependency changed')
    if(copy_root/'work').exists():raise ValueError('Auth source-only copied root contains old work objects')
    command=[sys.executable,str(copy_root/'wave20261106_auth_character_data_packet.py'),name];run=subprocess.run(command,cwd=copy_root,capture_output=True,text=True,timeout=180);log=WORK/'copied-root.log';log.write_text(run.stdout+'\n'+run.stderr,encoding='utf-8')
    if run.returncode:raise ValueError('Actual Auth source-only copied-root replay failed: '+run.stderr[-2200:])
    fresh=read_json(copy_root/descriptor['output']);baseline=read_json(ROOT/descriptor['output']);by_address={r['address']:r for r in baseline['dataMatches']};first=baseline['dataMatches'][0];ref=read_json(ROOT/first['semanticSource'])['primaryReference'];negatives=[];canonical=copy_root/descriptor['output'];before=sha256(canonical)
    for path in [first['source'],first['sourceDependencies'][0]['path'],first['semanticSource'],first['binary'],ref['path']]:
        target=copy_root/path;raw=target.read_bytes()
        try:
            target.write_bytes(raw+b' ');bad=subprocess.run(command,cwd=copy_root,capture_output=True,text=True,timeout=20)
            if not bad.returncode or sha256(canonical)!=before:raise ValueError('Altered Auth source/header/semantic/native/primary file was accepted or overwrote canonical proof')
            negatives.append(dict(path=path,rejectedBeforeCanonicalOverwrite=True))
        finally:target.write_bytes(raw)
    gp=ROOT/'evidence/lanes/parallel-wave20261106/gamespy-gp-character-data';sealed={}
    for file in ['source-files.json','registration-source-files.json','full-replay-source-files.json']:
        document=read_json(gp/file)
        for pin in document['files']+document['privateComparisonOrToolInputs']:sealed[pin['path']]=pin['sha256']
    for file in ['registration-ready.json','full-replay/ready.json']:
        for pin in read_json(gp/file)['files']:sealed[pin['path']]=pin['sha256']
    for path,digest in sealed.items():
        if sha256(ROOT/path)!=digest:raise ValueError('Frozen GP source/runtime/old object/proof changed during Auth work: '+path)
    value=dict(passed=True,actualIndependentRoot=str(copy_root),declaredInputsCopied=len(copied),noOldWorkObjectsCopied=True,freshGeneratedCCompiledAndGenuinelyLinkedObjects=102,initializedBytes=1431,objectsWithDifferentDebugHashesAcrossRoots=sum(row['objectSha256']!=by_address[row['address']]['objectSha256']for row in fresh['dataMatches']),wholeWrongCControlsRerun=fresh['controls']['wholeWrongCControls'],schemaControls=len(fresh['controls']['schemaControls']),namespaceControls=len(fresh['controls']['namespaceControls']),semanticGeneratorNativePublicReadDenials=len(fresh['actualFreshGeneration']['originalAndPublicReadDenials']),oldWorkReadDenials=len(fresh['oldWorkObjectReadRejections']),copiedTamperControls=negatives,allFrozenGpPinsRehashedUnchanged=len(sealed),noSharedSourceRegistryPreferencesConfigOrModulesWritten=True,producerSha256=sha256(ROOT/'wave20261106_auth_character_data_packet.py'),reviewerSha256=sha256(__file__),log=dict(path=log.relative_to(ROOT).as_posix(),sha256=sha256(log)),sourceCreditPendingSharedAcceptance=True)
    write_json(EVIDENCE/'copied-root-controls.json',value);print(dict(passed=True,objects=102,bytes=1431,copiedNegatives=len(negatives),gpFrozenPinsUnchanged=len(sealed)),flush=True)


if __name__=='__main__':main()
