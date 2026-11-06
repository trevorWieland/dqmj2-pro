from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parent
INTEGRATOR=ROOT.parents[1]/'dqmj2pro-decomp'
SNAPSHOT='evidence/integration/root-accepted114-identities-v2-20261101.json'
SELF='evidence/matches/mechanics-save-20261101-lane-roster-initializer-v2.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    rows=[]
    receipts=[]
    def add(row,origin):
        if row.get('module')=='main' and row.get('processor','arm9') in ['arm9',None] and row.get('program','') in ['',None]:
            value=row['address']
            start=int(value,0) if isinstance(value,str) else value
            value=row.get('bytes',1)
            length=int(value,0) if isinstance(value,str) else value
            rows.append(dict(start=start,end=start+length,origin=origin,source=row.get('source')))
    path=ROOT/SNAPSHOT
    receipts.append(dict(path=SNAPSHOT,sha256=sha(path)))
    for row in json.loads(path.read_text())['functions']:
        add(row,SNAPSHOT)
    for path in sorted(INTEGRATOR.glob('cohort*-specification-20261101.json')):
        if int(re.search(r'cohort(\d+)',path.name)[1])<108:
            continue
        receipts.append(dict(integratorPath=path.name,sha256=sha(path)))
        for row in json.loads(path.read_text()).get('expectedAdditions',[]):
            add(row,path.name)
    for path in sorted((ROOT/'evidence/matches').glob('*.json')):
        if path==ROOT/SELF:
            continue
        for row in json.loads(path.read_text()).get('matches',[]):
            if isinstance(row,dict) and 'address' in row:
                add(row,path.relative_to(ROOT).as_posix())
    checks=[]
    for address,length in [(0x020C5B00,708),(0x0206C140,20)]:
        overlaps=[row for row in rows if address<row['end'] and row['start']<address+length]
        if address == 0x0206C140:
            assert overlaps and all(row['start']==address and row['end']==address+length and row['source']=='src/runtime/runtime07/native_main_0206c140.c' for row in overlaps),(hex(address),overlaps)
        else:
            assert not overlaps,(hex(address),overlaps)
        checks.append(dict(processor='arm9',program='',module='main',mode='arm',address=hex(address),bytes=length,overlaps=overlaps))
    output=dict(schema=1,sourceCreditAdded=0,checks=checks,exclusionReceipts=receipts,
        netNewFunctions=1,netNewBytes=708,reusedExistingBytes=20,ownPendingReportExcluded=dict(path=SELF,sha256=sha(ROOT/SELF)),
        qualification='Exact self-report is excluded by path only;accepted snapshot,all available108+integrator additions and every other local canonical report remain active.')
    path=ROOT/'evidence/lanes/save-core/roster-initializer257-overlap-20261101.json'
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(len(receipts),'receipts',sha(path))


if __name__=='__main__':
    main()
