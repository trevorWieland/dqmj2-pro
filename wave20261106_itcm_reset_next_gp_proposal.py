import bisect
import re
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from initialized_storage_protection_v2_20261106 import protected

FOLDER=ROOT/'evidence/lanes/parallel-wave20261106/whole-character-read-only'
COMMIT='a2f340195975f4f042e28a60b62561dd9a0b2700'


def main():
    if FOLDER.resolve()!=(ROOT/'evidence/lanes/parallel-wave20261106/whole-character-read-only').resolve():raise ValueError('Exact GP read-only evidence directory differs')
    path=FOLDER/'inventory.json';inventory=read_json(path);rows=[];sources={};snapshots={};functions=[];symbols=(ROOT/'config/arm9/symbols.txt').read_text()
    for line in symbols.splitlines():
        m=re.fullmatch(r'(\S+) kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',line)
        if m:functions.append((int(m[4],0),int(m[4],0)+int(m[3],0),m[2],line))
    functions.sort();starts=[f[0]for f in functions];intervals,pins=protected(('','arm9','main'),inventory['sourceRevision'])
    for value in inventory['wholeCharacterCandidates']:
        refs=[s for s in value['primaryCompleteCLiteralExpressions']if '/gp/'in s['path'].lower()]
        if int(value['address'],0)<0x20e0400 or not refs:continue
        if any(max(int(value['address'],0),a)<min(int(value['endExclusive'],0),b)for a,b in intervals):continue
        reference=dict(refs[0]);source=ROOT/reference['path']
        if sha256(source)!=reference['sha256']:raise ValueError('Selected actual primary GP source changed')
        root=ROOT/Path(*Path(reference['path']).parts[:3]);metadata=next((root/n for n in ['reference-snapshot.json','snapshot.json']if(root/n).is_file()),None)
        if metadata is None:raise ValueError('Actual immutable GP source snapshot absent')
        manifest=read_json(metadata);commit=manifest.get('commit',manifest.get('primaryCommit',manifest.get('revision')))
        if commit!=COMMIT:raise ValueError('Complete primary GP commit differs')
        record=next((x for x in manifest['files']if x['path']==reference['path']or(root/x['path']).resolve()==source.resolve()),None)
        if not record or record['sha256']!=reference['sha256']or '/'+COMMIT+'/'not in record['url']:raise ValueError('Actual primary GP URL/hash snapshot differs')
        reference.update(primaryUrl=record['url'],primaryCommit=COMMIT,snapshot=dict(path=metadata.relative_to(ROOT).as_posix(),sha256=sha256(metadata)));sources[reference['path']]=dict(path=reference['path'],sha256=reference['sha256'],url=reference['primaryUrl']);snapshots[reference['snapshot']['path']]=reference['snapshot'];row={k:v for k,v in value.items()if k!='primaryCompleteCLiteralExpressions'};row.update(primaryReference=reference,objectType='narrow char[sizeof(complete primary C literal expression)]',explicitByteWidth=1,includesExactlyOneFinalNulTerminator=True)
        for witness in row['originalPointerWitnesses']:
            origin=int(witness['origin'],0);i=bisect.bisect_right(starts,origin)-1;fn=functions[i]if i>=0 and functions[i][0]<=origin<functions[i][1]else None
            witness['containingConfiguredFunction']=dict(program='',processor='arm9',module='main',mode=fn[2],address=hex(fn[0]),bytes=fn[1]-fn[0],canonicalRecord=fn[3])if fn else None
        rows.append(row)
    for a,b in zip(rows,rows[1:]):
        if int(a['endExclusive'],0)>int(b['address'],0):raise ValueError('Selected complete GP character objects overlap')
    if any(p.get('path')and sha256(ROOT/p['path'])!=p['sha256']for p in pins):raise ValueError('Protection epoch changed before GP proposal publication')
    document=dict(status='read-only-proposed-whole-GameSpy-GP-character-objects-needs-admission',sourceCredit=0,dataCredit=0,newSourceAuthored=False,newClaimsCreated=False,sourceRevision=inventory['sourceRevision'],scope=dict(program='',processor='arm9',module='main',mode='data'),originalInventory=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)),generator=dict(path=Path(__file__).name,sha256=sha256(__file__)),objects=rows,objectCount=len(rows),opportunityBytes=sum(x['bytes']for x in rows),objectIntervalsDisjoint=True,wholePrimaryCharacterLiteralExpressions=True,allObjectsHaveConfiguredDataStartAndExactOriginalPointerWords=True,allObjectsIncludeFullOriginalFinalNulAndNoInteriorConfiguredBoundary=True,allCommittedPendingFunctionDataLinkageAndHistoricalReservationsExcluded=True,protectedIntervals=len(intervals),protectionPins=pins,protectionEpochStableAtPublication=True,sourcePins=list(sources.values()),snapshotPins=list(snapshots.values()),module=inventory['module'],symbols=inventory['symbols'],relocations=inventory['relocations'],omittedNasUrlAt020deb48Uncredited=True,protectedAuthParameter020deb2c28BytesUnchanged=True,unselectedWholeLiteralCandidatesRemainUnclaimed=True,meaning='Complete narrow C GP/GPI error/protocol/format strings from exact primary GameSpy sources. Every native character and final NUL retained; no opcode/text heuristic, arbitrary array slice, alignment or original storage-author assumption.',coordinatorStillRequired=['Fresh independent physical/storage exclusion and complete source-literal/API-context review.','Separate storage admission before data source generation.','Genuine complete C STT_OBJECT payload/placement and copied-root proofs; meaningful wrong-character/terminator/extent/source/native/namespace controls.'])
    target=FOLDER/'gp-proposal.json';write_json(target,document);print(dict(objects=len(rows),bytes=document['opportunityBytes'],sources=len(sources),snapshots=len(snapshots),originalPointerWords=sum(len(x['originalPointerWitnesses'])for x in rows),configuredCallerWords=sum(w['containingConfiguredFunction']is not None for x in rows for w in x['originalPointerWitnesses']),sha256=sha256(target)),flush=True)


if __name__=='__main__':main()
