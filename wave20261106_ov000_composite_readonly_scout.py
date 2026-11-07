import hashlib
import json
import re
import subprocess
from project import ROOT,read_json,write_json,sha256
from wave20261106_nns_primary_readonly_scout import intervals
from wave20261106_ov000_controller_followup_readonly_scout import cfg_v2,overlay_set

REV='0da3da2f2eaf3888774e1d2f0cd572c6db3e2cfb'
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov000-composite-scout'
SEEDS={0x2049ad0,0x2049be4,0x21ebdf0,0x21ef688,0x21f2d24,0x221c758,0x222b24c,0x2206868,0x220820c}


def blob(path):return subprocess.check_output(['git','show',REV+':'+path],cwd=ROOT)


def main():
    if(LANE/'inventory-v1.json').exists():raise ValueError('Read-only scout inventory already exists')
    raw=blob('ledger/functions.jsonl');rows=[json.loads(line)for line in raw.splitlines()];protect=[];pins={}
    for row in rows:
        if row['states']['functionMatched']or row.get('sourceUnit'):protect.extend((*r,REV+':ledger/functions.jsonl')for r in intervals(row))
    for name,key in[('ledger/data.json','records'),('ledger/linkage.json','regions')]:protect.extend((*r,REV+':'+name)for r in intervals(json.loads(blob(name))[key]))
    for path in sorted(set((ROOT/'evidence/lanes').rglob('claim.json'))|set((ROOT/'evidence/lanes').rglob('data-claim.json'))|set(ROOT.glob('cohort*-*specification.json'))):
        text=path.read_bytes();pins[path.relative_to(ROOT).as_posix()]=hashlib.sha256(text).hexdigest();protect.extend((*r,path.relative_to(ROOT).as_posix())for r in intervals(json.loads(text)))
    protections=[(a,b,origin)for program,cpu,module,a,b,origin in protect if(program,cpu,module)==('','arm9','ov000')]
    image_path=ROOT/'extract/arm9_overlays/ov000.bin';image=image_path.read_bytes();base=0x21d7240;symbol_path=ROOT/'config/arm9/overlays/ov000/symbols.txt';symbols=symbol_path.read_text().splitlines();reloc_path=symbol_path.with_name('relocs.txt');relocs=reloc_path.read_text().splitlines()
    for path in[image_path,symbol_path,reloc_path]:pins[path.relative_to(ROOT).as_posix()]=sha256(path)
    candidates=[];rejected=[]
    for row in rows:
        if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','ov000','arm')or row['states']['functionMatched']or not 256<=row['bytes']<=2048:continue
        a=int(row['address'],0);n=row['bytes'];outgoing=[line for line in relocs if a<=int(line.split()[0][5:],0)<a+n];calls=[line for line in outgoing if 'kind:arm_call'in line];targets={int(re.search(r'to:(0x[0-9a-f]+)',line)[1],0)for line in calls}
        if not targets&SEEDS:continue
        conflicts=[dict(start=hex(x),end=hex(y),origin=origin)for x,y,origin in protections if max(a,x)<min(a+n,y)]
        if conflicts:rejected.append(dict(address=row['address'],bytes=n,conflicts=conflicts));continue
        body=image[a-base:a-base+n]
        if len(body)!=n or hashlib.sha256(body).hexdigest()!=row['inputBytesSha256']:raise ValueError('Fresh original whole candidate span changed')
        flow=cfg_v2(image,base,a,n);covered={int(v['address'],0)+i for v in flow['instructions']for i in range(4)}|{int(v['address'],0)+i for v in flow['literals']for i in range(4)};uncovered=sorted(set(range(a,a+n))-covered)
        namespaces=[line for line in outgoing if not line.endswith(('module:main','module:overlay(0)'))]
        candidates.append(dict(identity=row,canonicalInventoryRecord=next((line for line in symbols if line.endswith('addr:0x'+format(a,'08x'))),None),originalRelocationRecords=outgoing,knownInterfaceHits=[hex(t)for t in sorted(targets&SEEDS)],rawOutgoingNamespacesUnresolved=namespaces,cfg=flow,unexplainedNativeBytes=[hex(v)for v in uncovered],nativeSha256=hashlib.sha256(body).hexdigest(),sourceMeaning='Measured game controller composition only; no public-primary source mapping.'))
    for name,h in pins.items():
        if sha256(ROOT/name)!=h:raise ValueError('Read-only protection/input epoch changed: '+name)
    result=dict(status='read-only-larger-cohesive-interface-scout',sourceRevision=REV,compilerInvoked=False,reconstructionSourceWritten=False,claimWritten=False,sourceCredit=0,seeds=[hex(v)for v in sorted(SEEDS)],candidates=candidates,protected=rejected,actualInputPins=[dict(path=name,sha256=h)for name,h in sorted(pins.items())],nativeImageSha256=sha256(image_path))
    write_json(LANE/'inventory-v1.json',result)
    for candidate in candidates:print(candidate['identity']['address'],candidate['identity']['bytes'],candidate['knownInterfaceHits'],len(candidate['cfg']['issues']),len(candidate['unexplainedNativeBytes']),candidate['rawOutgoingNamespacesUnresolved'])
    print(dict(functions=len(candidates),bytes=sum(c['identity']['bytes']for c in candidates),protected=len(rejected)))


if __name__=='__main__':main()
