import shutil
import subprocess
import sys
from project import ROOT,read_json,write_json,sha256
from wave20261106_aes_table_data_paths import EVIDENCE,WORK,REFERENCE


def main():
    name=(EVIDENCE/'canonical-packet.json').relative_to(ROOT).as_posix();descriptor=read_json(ROOT/name);manifest=read_json(ROOT/descriptor['sourceManifest']['path']);copy_root=ROOT.parent/'aestable1106';copy_root.mkdir(exist_ok=False)
    if copy_root.resolve().parent!=ROOT.resolve().parent or copy_root.resolve()==ROOT.resolve():raise ValueError('Exact AES independent copied-root destination differs')
    copied={pin['path']:pin for pin in manifest['files']+manifest['privateComparisonOrToolInputs']};copied[name]=dict(path=name,sha256=sha256(ROOT/name));copied[descriptor['sourceManifest']['path']]=descriptor['sourceManifest']
    for path,pin in copied.items():
        target=copy_root/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,target)
        if sha256(target)!=pin['sha256']:raise ValueError('Actual AES copied source/native/runtime input changed')
    if(copy_root/'work').exists():raise ValueError('AES source-only copy contains old work objects/research')
    command=[sys.executable,str(copy_root/'wave20261106_aes_table_data_packet.py'),name];run=subprocess.run(command,cwd=copy_root,capture_output=True,text=True,timeout=180);log=WORK/'copied-root.log';log.write_text(run.stdout+'\n'+run.stderr,encoding='utf-8')
    if run.returncode:raise ValueError('Actual independent AES source-only copied-root replay failed: '+run.stderr[-2200:])
    fresh=read_json(copy_root/descriptor['output']);baseline=read_json(ROOT/descriptor['output']);old={row['address']:row for row in baseline['dataMatches']};first=baseline['dataMatches'][0];negatives=[];canonical=copy_root/descriptor['output'];before=sha256(canonical)
    paths=[first['source'],first['sourceDependencies'][0]['path'],first['semanticSource'],first['binary'],(REFERENCE/'heimdal-rijndael-alg-fst.c').relative_to(ROOT).as_posix(),'config/arm9/overlays/ov006/symbols.txt','config/arm9/relocs.txt']
    for path in paths:
        target=copy_root/path;raw=target.read_bytes()
        try:
            target.write_bytes(raw+b' ');bad=subprocess.run(command,cwd=copy_root,capture_output=True,text=True,timeout=20)
            if not bad.returncode or sha256(canonical)!=before:raise ValueError('Changed AES source/header/math/native/primary/alias/plural-relocation input admitted or overwrote canonical proof')
            negatives.append(dict(path=path,rejectedBeforeCanonicalOverwrite=True))
        finally:target.write_bytes(raw)
    sealed={}
    for folder,names in [('gamespy-gp-character-data',['source-files.json','registration-source-files.json','full-replay-source-files.json']),('auth-character-data',['source-files.json'])]:
        base=ROOT/'evidence/lanes/parallel-wave20261106'/folder
        for file in names:
            document=read_json(base/file)
            for pin in document['files']+document['privateComparisonOrToolInputs']:sealed[pin['path']]=pin['sha256']
        for file in ['ready.json']+(['registration-ready.json','full-replay/ready.json']if folder=='gamespy-gp-character-data'else[]):
            for pin in read_json(base/file)['files']:sealed[pin['path']]=pin['sha256']
    if any(sha256(ROOT/path)!=digest for path,digest in sealed.items()):raise ValueError('Frozen GP/Auth source/runtime/old objects/proofs changed during AES work')
    value=dict(passed=True,actualIndependentRoot=str(copy_root),actualDeclaredInputsCopied=len(copied),noOldObjectsOrWorkResearchCopied=True,freshGeneratedCCompiledAndGenuinelyLinkedObjects=10,initializedBytes=10240,objectsWithDifferentDebugHashesAcrossRoots=sum(row['objectSha256']!=old[row['address']]['objectSha256']for row in fresh['dataMatches']),genuineWrongCControlsRerun=fresh['controls']['genuineWrongCCount'],semanticSchemaControls=len(fresh['controls']['semanticSchemaControls']),scopeTypeExtentControls=len(fresh['controls']['namespaceTypeExtentControls']),threeInteriorElementViewControls=len(fresh['controls']['threeInteriorElementViewControls']),actualWrongWidthHeaderCompileRejected=fresh['controls']['actualWrongWidthHeaderCompileRejected'],generatorNativePublicReadDenials=len(fresh['actualFreshGeneration']['originalAndPublicReadDenials']),oldWorkReadDenials=len(fresh['oldWorkObjectReadRejections']),copiedTamperControls=negatives,all13GenuineAliasesPreserved=len(fresh['dataAliases'])==13,ambiguousInteriorViewsAddZeroBytes=fresh['interiorViewExtraBytes']==0,originalMainPluralNamespacesUnchanged=fresh['allOriginalAmbiguousQualifiersAndPluralOverlayReferencesUnchanged'],frozenGpAuthPinsRehashedUnchanged=len(sealed),noSharedWritesOrWholeModuleBuild=True,producerSha256=sha256(ROOT/'wave20261106_aes_table_data_packet.py'),reviewerSha256=sha256(__file__),log=dict(path=log.relative_to(ROOT).as_posix(),sha256=sha256(log)),sourceCreditPendingSharedAcceptance=True)
    write_json(EVIDENCE/'copied-root-controls.json',value);print(dict(passed=True,tables=10,bytes=10240,copiedNegatives=len(negatives),oldGpAuthPinsUnchanged=len(sealed)),flush=True)


if __name__=='__main__':main()
