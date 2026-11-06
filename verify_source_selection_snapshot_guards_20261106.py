import copy
import os
import shutil
import subprocess
import time
import uuid
from pathlib import Path
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256,configuration
import source_selection as P
from probe_source_selection_snapshot_20261106 import Tracker,EpochChanged,WORK,LANE
from guard_source_selection_snapshot_20261106 import GuardedSnapshot


class FixtureTracker(Tracker):
    def private(self,p):return False


def make(root):
    if root.exists() or not root.is_relative_to(WORK):raise ValueError('Guard fixture root is not fresh/owned')
    root.mkdir(parents=True);namespace=configuration()['romSha256'];document=read_json(P.POLICY);row=copy.deepcopy(next(r for r in document['preferences'] if r['module']=='main' and r['mode']=='arm' and int(r['address'],0)==0x02065dec));audit=read_json(ROOT/row['evidence'])
    for name in [row['evidence'],audit['previous']['source'],audit['preferred']['source']]:
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,path)
    write_json(root/'source-preferences.json',dict(schemaVersion=1,romSha256=namespace,preferences=[row]));write_json(root/'recovery.json',dict(batches=[]))
    return namespace,row,audit


def execute():
    outputs=[];base=WORK/('guards-'+uuid.uuid4().hex[:12])
    for label in ['registry-content','policy-content','audit-content','same-size-source','missing-source','file-to-directory','same-size-restored-mtime','observed-change-then-restore']:
        root=base/label;namespace,row,audit=make(root);source=root/audit['preferred']['source'];original=source.read_bytes();times=source.stat()
        with patch.object(P,'ROOT',root):
            snapshot=GuardedSnapshot(namespace,FixtureTracker(),root/'source-preferences.json',root/'recovery.json');snapshot.preferences(namespace)
            if label=='registry-content':write_json(root/'recovery.json',dict(batches=[dict(report='wrong')]))
            elif label=='policy-content':
                changed=read_json(root/'source-preferences.json');changed['romSha256']='0'*64;write_json(root/'source-preferences.json',changed)
            elif label=='audit-content':
                changed=read_json(root/row['evidence']);changed['newByteCredit']=1;write_json(root/row['evidence'],changed)
            elif label in ['same-size-source','same-size-restored-mtime','observed-change-then-restore']:
                payload=bytearray(original);payload[0]^=1;source.write_bytes(payload)
                if label=='same-size-restored-mtime':os.utime(source,ns=(times.st_atime_ns,times.st_mtime_ns))
            elif label=='missing-source':source.unlink()
            else:source.unlink();source.mkdir()
            if label=='observed-change-then-restore':
                try:snapshot.preferences(namespace)
                except EpochChanged:pass
                else:raise ValueError('Transient source change was not observed')
                source.write_bytes(original);os.utime(source,ns=(times.st_atime_ns,times.st_mtime_ns))
            try:snapshot.preferences(namespace);snapshot.verify()
            except (EpochChanged,ValueError,OSError) as error:outputs.append(dict(case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Changed policy snapshot epoch accepted: '+label)
    root=base/'path-target';namespace,row,audit=make(root);a=root/'target-a';b=root/'target-b';a.mkdir();b.mkdir();shutil.copyfile(root/row['evidence'],a/'audit.json');shutil.copyfile(root/row['evidence'],b/'audit.json');alias=root/'audit-alias'
    for target in [a,b]:
        if not target.resolve().is_relative_to(root.resolve()):raise ValueError('Owned junction target escaped fixture')
    script=base/'create-junction.ps1';script.write_text('param([string]$junctionPath,[string]$targetPath)\nNew-Item -ItemType Junction -Path $junctionPath -Target $targetPath | Out-Null\n',encoding='utf-8');command=['powershell','-NoProfile','-NonInteractive','-File',str(script),str(alias),str(a)];result=subprocess.run(command,capture_output=True,text=True)
    if result.returncode:raise ValueError(('Cannot qualify actual target-retarget guard',result.stdout,result.stderr))
    row['evidence']='audit-alias/audit.json';row['evidenceSha256']=sha256(a/'audit.json');write_json(root/'source-preferences.json',dict(schemaVersion=1,romSha256=namespace,preferences=[row]))
    with patch.object(P,'ROOT',root):
        snapshot=GuardedSnapshot(namespace,FixtureTracker(),root/'source-preferences.json',root/'recovery.json');os.rmdir(alias);command[-1]=str(b);result=subprocess.run(command,capture_output=True,text=True)
        if result.returncode:raise ValueError('Owned junction target mutation did not complete')
        try:snapshot.verify()
        except EpochChanged as error:outputs.append(dict(case='same-content-junction-target-changed',rejected=True,reason=str(error)))
        else:raise ValueError('Same-content retargeted policy path accepted')
    root=base/'custom-path';namespace,row,audit=make(root)
    with patch.object(P,'ROOT',root):
        snapshot=GuardedSnapshot(namespace,FixtureTracker(),root/'source-preferences.json',root/'recovery.json');changed=read_json(root/'source-preferences.json');changed['romSha256']='0'*64;custom=root/'custom.json';write_json(custom,changed)
        try:snapshot.preferences(namespace,custom)
        except ValueError as error:
            if 'namespace differs' not in str(error):raise
            outputs.append(dict(case='custom-negative-policy-still-runs-original',rejected=True,reason=str(error),uncachedCustomCalls=snapshot.customCalls))
        else:raise ValueError('Custom negative policy was cached or accepted')
        snapshot.verify()
    write_json(LANE/'snapshot-guard-controls.json',dict(passed=True,sourceCredit=0,controls=outputs,generatorSha256=sha256(__file__),snapshotImplementationSha256=sha256(ROOT/'guard_source_selection_snapshot_20261106.py'),allMutationsPrivate=True,noLiveInputsChanged=True,metadataNotIntegrityProof=True,finalExactContentAndPathTargetGuardsRequired=True));print(dict(passed=True,controls=len(outputs),receiptSha256=sha256(LANE/'snapshot-guard-controls.json')))


if __name__=='__main__':execute()
