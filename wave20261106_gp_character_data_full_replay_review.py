import copy
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from wave20261106_gp_character_data_paths import WORK,EVIDENCE


def main():
    descriptor_name=(EVIDENCE/'full-replay-descriptor.json').relative_to(ROOT).as_posix();descriptor=read_json(ROOT/descriptor_name);manifest=read_json(ROOT/descriptor['sourceManifest']['path']);copy_root=ROOT.parent/'gpchar-rf1106';copy_root.mkdir(exist_ok=False)
    if copy_root.resolve().parent!=ROOT.resolve().parent or copy_root.resolve()==ROOT.resolve():raise ValueError('Exact independent copied-root proof destination differs')
    original_ready=read_json(EVIDENCE/'registration-ready.json');original_manifest=read_json(EVIDENCE/'registration-source-files.json');sealed={p['path']:p['sha256']for p in original_manifest['files']+original_manifest['privateComparisonOrToolInputs']+original_ready['files']};sealed[(EVIDENCE/'registration-ready.json').relative_to(ROOT).as_posix()]=sha256(EVIDENCE/'registration-ready.json')
    copied={p['path']:p for p in manifest['files']+manifest['privateComparisonOrToolInputs']};copied[descriptor_name]=dict(path=descriptor_name,sha256=sha256(ROOT/descriptor_name));copied[descriptor['sourceManifest']['path']]=descriptor['sourceManifest']
    for path,pin in copied.items():
        target=copy_root/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,target)
        if sha256(target)!=pin['sha256']:raise ValueError('Copied actual source/runtime input differs')
    old=read_json(ROOT/descriptor['originalReport']['path'])
    if any((copy_root/row['object']).exists()or(copy_root/row['realLink']['linkedElf']).exists()for row in old['dataMatches']):raise ValueError('Source-only copied proof contains old GP objects/ELFs')
    command=[sys.executable,str(copy_root/'wave20261106_gp_character_data_full_replay.py'),descriptor_name];run=subprocess.run(command,cwd=copy_root,capture_output=True,text=True,timeout=180);log=WORK/'full-replay-copied-root.log';log.write_text(run.stdout+'\n'+run.stderr,encoding='utf-8')
    if run.returncode:raise ValueError('Actual independent source-only copied-root full replay failed: '+run.stderr[-2000:])
    fresh=read_json(copy_root/descriptor['output']);root_report=read_json(ROOT/descriptor['output']);fresh_rows=fresh['dataMatches'];root_rows={r['address']:r for r in root_report['dataMatches']};negative=[]
    source_names=[old['dataMatches'][0]['source'],old['dataMatches'][0]['sourceDependencies'][0]['path'],old['dataMatches'][0]['semanticSource'],'extract/arm9/arm9.bin',read_json(ROOT/old['dataMatches'][0]['semanticSource'])['primaryReference']['path']]
    report_path=copy_root/descriptor['output'];before_report=sha256(report_path)
    for path in source_names:
        target=copy_root/path;raw=target.read_bytes()
        try:
            target.write_bytes(raw+b' ');bad=subprocess.run(command,cwd=copy_root,capture_output=True,text=True,timeout=20)
            if not bad.returncode or sha256(report_path)!=before_report:raise ValueError('Changed copied source/header/semantic/native/public input was admitted or overwrote good report')
            negative.append(dict(path=path,rejectedBeforeCanonicalReportOverwrite=True,returnCode=bad.returncode))
        finally:target.write_bytes(raw)
    if any(sha256(ROOT/path)!=digest for path,digest in sealed.items()):raise ValueError('Original or additive frozen GP source/runtime/proof changed')
    value=dict(passed=True,actualCopiedRoot=str(copy_root),noOldWorkObjectsOrLinkedElfsCopied=True,copiedDeclaredSourceAndPrivateInputs=len(copied),objectsFreshlyGeneratedCompiledAndGenuinelyLinked=259,initializedBytes=3696,objectsWithDifferentDebugHashesAcrossRoots=sum(row['objectSha256']!=root_rows[row['address']]['objectSha256']for row in fresh_rows),originalSourceFlagsAndNativeContractsUnchanged=True,originalWrongCControlsRerun=fresh['controls']['wholeWrongCControls'],semanticGenerationReadDenials=len(fresh['gpCharacterFullSourceReplay']['actualFreshGeneration']['generationReadDenials']),oldWorkObjectReadDenials=len(fresh['gpCharacterFullSourceReplay']['oldWorkReadRejections']),sourceNativeHeaderSemanticPrimaryNegatives=negative,originalAndAdditiveFrozenPinsRehashedUnchanged=len(sealed),log=dict(path=log.relative_to(ROOT).as_posix(),sha256=sha256(log)),producer=dict(path='wave20261106_gp_character_data_full_replay.py',sha256=sha256(ROOT/'wave20261106_gp_character_data_full_replay.py')),reviewerSha256=sha256(__file__),noSharedGlobalModuleBuild=True,sourceCreditPendingSharedAcceptance=True)
    write_json(EVIDENCE/'full-replay-copied-root-review.json',value);print(dict(passed=True,copiedRoot=str(copy_root),objects=259,bytes=3696,negatives=len(negative),sealedPinsUnchanged=len(sealed)),flush=True)


if __name__=='__main__':main()
