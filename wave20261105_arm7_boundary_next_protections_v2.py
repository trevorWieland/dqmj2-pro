import hashlib
import json
from project import ROOT,read_json,sha256
from export_reconstruction_atlas import build as atlas_build
from wave20261105_arm7_boundary_next_audit import NAMESPACE,scope,number,pin,committed


def protections(revision,frontier):
    values=[];pins=[];rawLedger=committed(revision,'ledger/functions.jsonl')
    if hashlib.sha256(rawLedger).hexdigest()!=frontier['committedLedgerSha256']:raise ValueError('Committed159 native ledger differs from frontier')
    def add(row,kind,parent=None):
        identity=scope(row,parent)
        if identity!=NAMESPACE:return
        size=row.get('storedBytes',row.get('bytes'))
        if not size or not row.get('address'):return
        address=number(row['address']);values.append(dict(namespace=list(identity),start=address,end=address+size,kind=kind,id=row.get('id'),address=row['address'],bytes=size))
    ledger=[json.loads(line) for line in rawLedger.splitlines()]
    for r in ledger:add(r,'accepted-native-function-or-pool' if r['states']['functionMatched'] else 'existing-positive-native-function-extent')
    for name,key in [('ledger/data.json','records'),('ledger/linkage.json','regions')]:
        raw=committed(revision,name);pins.append(dict(gitObject=revision+':'+name,sha256=hashlib.sha256(raw).hexdigest()))
        for r in json.loads(raw)[key]:
            if not r.get('processor') and r.get('module')=='arm7-main':r=dict(r,processor='arm7')
            add(r,'committed-native-data-storage' if key=='records' else 'committed-linker-physical-region')
    atlas=atlas_build(revision,[],128)
    pins.append(dict(gitObject=revision+':manifest.json',sha256=hashlib.sha256(committed(revision,'manifest.json')).hexdigest()))
    pins.append(pin('export_reconstruction_atlas.py'))
    if atlas['sourceCommit']!=revision:raise ValueError('Private committed atlas reconstruction has wrong epoch')
    module=next(m for m in atlas['modules'] if (m.get('program') or '',m['processor'],m['name'])==NAMESPACE)
    for offset,size,category in module['regions']:
        if category in [1,2,3,4,5]:values.append(dict(namespace=list(NAMESPACE),start=module['base']+offset,end=module['base']+offset+size,kind='accepted-atlas-physical-category-'+str(category),bytes=size))
    files=sorted((ROOT/'evidence/lanes').rglob('claim.json'));unparsed=[];broad=[]
    for path in files:
        name=path.relative_to(ROOT).as_posix();pins.append(pin(name));claim=read_json(path);items=claim.get('claimedFunctions',claim.get('functions'))
        if not isinstance(items,list):
            if scope(claim)==NAMESPACE:unparsed.append(dict(path=name,reason='No explicit function ownership list'))
            continue
        for item in items:
            if isinstance(item,dict):
                r=dict(item)
                if not r.get('address') and r.get('id'):
                    try:r['address']=hex(int(r['id'].rsplit('/',1)[-1],16))
                    except ValueError:pass
                before=len(values);add(r,'existing-reserved-function',claim)
                if len(values)>before:values[-1]['claim']=name
                elif scope(r,claim)==NAMESPACE and not r.get('address'):unparsed.append(dict(path=name,reason='Unparsed explicit ARM7 ownership row'))
            elif scope(claim)==NAMESPACE:unparsed.append(dict(path=name,reason='Nonobject ARM7 function ownership row'))
        if scope(claim)==NAMESPACE and claim.get('regionStart') and claim.get('regionEndExclusive'):broad.append(dict(path=name,start=claim['regionStart'],endExclusive=claim['regionEndExclusive'],interpretation='Collection/discovery envelope retained separately; exact listed function extents are protected, matching existing frontier parser. Coordinator must independently confirm ownership before source admission.'))
    pending=[]
    for path in sorted((ROOT/'provenance').glob('cohort16[012]-*specification*.json')):
        pins.append(pin(path.relative_to(ROOT).as_posix()));value=read_json(path)
        def visit(node):
            if isinstance(node,dict):
                if scope(node)==NAMESPACE and node.get('address') and node.get('bytes'):
                    add(node,'pending-cohort-physical-extent');pending.append(node['address'])
                for child in node.values():visit(child)
            elif isinstance(node,list):
                for child in node:visit(child)
        visit(value)
    return values,pins,dict(committedLedger=dict(gitObject=revision+':ledger/functions.jsonl',sha256=hashlib.sha256(rawLedger).hexdigest()),claimFiles=len(files),claimPathSet=sorted(p.relative_to(ROOT).as_posix() for p in files),unparsedArm7Claims=unparsed,broadHistoricalCollectionEnvelopes=broad,pendingArm7ExtentRows=pending,physicalRows=len(values),acceptedAtlasBytes=module['acceptedBytes'])
