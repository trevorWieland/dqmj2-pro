import json
import re
from pathlib import Path
from project import ROOT,sha256,write_json
SNAPSHOT=ROOT/'evidence/verification/lane-root107-exclusion-observed-20261101.json'
SNAPSHOT_SHA='a9c5288f9deb58d7900ca5ce1bc01e8334315032294a023f59f851f79da2f832'
REPORT=ROOT/'evidence/verification/lane-qualified-exclusion107-audit-20261101.json'
QUERIES=[('arm9','','main','arm',0x0202B54C,72,True),('arm9','','main','arm',0x0202B594,128,True),('arm9','','main','arm',0x0202B614,124,True),('arm7','','arm7-main','arm',0x027E0564,56,False),('arm7','','arm7-wram','arm',0x037FD84C,56,False)]
def address(value):
    if isinstance(value,bool):raise ValueError('Boolean is not an address')
    if isinstance(value,int):result=value
    elif isinstance(value,str):
        text=value.strip().lower()
        if re.fullmatch(r'0x[0-9a-f]+',text):result=int(text,16)
        elif re.fullmatch(r'[0-9]+',text)and not text.startswith('0'):result=int(text,10)
        elif re.fullmatch(r'[0-9a-f]+',text)and(text.startswith('0')or any(x in text for x in 'abcdef')):result=int(text,16)
        else:raise ValueError('Unrecognized address encoding')
    else:raise ValueError('Address must be an integer or explicit string')
    if not 0<=result<=0xffffffff:raise ValueError('Address outside 32-bit guest space')
    return result

def identity(row):
    return (str(row['processor']).lower(),row.get('program')or'',str(row['module']).lower(),str(row['mode']).lower(),address(row['address']))

def overlaps(rows,query):
    processor,program,module,mode,start,size=query
    if isinstance(size,bool)or not isinstance(size,int)or size<1 or start+size>0x100000000:raise ValueError('Invalid query interval')
    hits=[]
    for row in rows:
        item=identity(row)
        if item[:4]!=(processor,program,module,mode):continue
        extent=row.get('bytes')
        if extent is not None and (isinstance(extent,bool)or not isinstance(extent,int)or extent<0):raise ValueError('Invalid accepted extent')
        end=item[4]+(extent or 1)
        if start<end and item[4]<start+size:hits.append(row)
    return hits

def main():
    if not SNAPSHOT.is_file()or sha256(SNAPSHOT)!=SNAPSHOT_SHA:raise ValueError('Frozen accepted107 snapshot missing or changed')
    snapshot=json.loads(SNAPSHOT.read_text());rows=snapshot['functions']
    if len(rows)!=9210 or snapshot['acceptedCohort']!=107:raise ValueError('Accepted snapshot identity/count differs')
    for row in rows:identity(row)
    results=[];controls=[]
    for processor,program,module,mode,start,size,expected in QUERIES:
        query=(processor,program,module,mode,start,size);hits=overlaps(rows,query)
        if bool(hits)!=expected:raise ValueError('Qualified overlap expectation differs')
        results.append(dict(processor=processor,program=program,module=module,mode=mode,address=hex(start),bytes=size,alreadySelected=bool(hits),newCoverageEligibleAfterSourceAndNativeGates=not bool(hits),selectedMatches=hits))
        for value in [start,hex(start),'0x'+format(start,'08X'),format(start,'08X'),str(start)]:
            if address(value)!=start:raise ValueError('Address normalization calibration failed')
            controls.append(dict(name='address-'+hex(start)+'-'+str(value),passed=True))
    synthetic=[dict(processor='arm7',program='child.srl',module='arm7-wram',mode='arm',address='037FD84C',bytes=56)]
    base=('arm7','child.srl','arm7-wram','arm',0x037fd84c,56)
    if len(overlaps(synthetic,base))!=1:raise ValueError('Qualified synthetic positive failed')
    for index,value in [(0,'arm9'),(1,''),(2,'arm7-main'),(3,'thumb')]:
        query=list(base);query[index]=value
        if overlaps(synthetic,tuple(query)):raise ValueError('Wrong qualified namespace matched')
        controls.append(dict(name='namespace-'+str(index),passed=True))
    if len(overlaps(synthetic,base[:4]+(0x037fd850,4)))!=1:raise ValueError('Interior overlap escaped exclusion')
    controls.append(dict(name='interior-overlap',passed=True))
    synthetic[0]['bytes']=None
    if overlaps(synthetic,base[:4]+(0x037fd850,4)):raise ValueError('Unsized accepted row invented an extent')
    if len(overlaps(synthetic,base))!=1:raise ValueError('Unsized accepted row lost its reserved start')
    controls.append(dict(name='unsized-reserves-only-start',passed=True))
    for bad in [True,1.5,-1,0x100000000,'unknown','0xG']:
        try:address(bad)
        except ValueError:controls.append(dict(name='reject-'+str(bad),passed=True))
        else:raise ValueError('Invalid address accepted')
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),snapshot=dict(path=SNAPSHOT.relative_to(ROOT).as_posix(),sha256=SNAPSHOT_SHA,rows=len(rows)),queries=results,controls=controls,controlCount=len(controls),core324ClassificationCorrection=dict(frozenManifest='provenance/main-frame-heap-core324-handoff-20261101.json',frozenSourceCommit='035eb91e',oldNewCoverageClaimRejected=True,correctNewFunctions=0,correctNewBytes=0,matchingProofPreserved=True,existingPrimariesPreserved=True,reason='The source reservation was incorrectly treated as evidence of uncovered coverage; the selected identity snapshot shows all three functions already accepted.'),additionalSourceCredit=0,frameworkOrAcceptedSourceChanged=False)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),controls=len(controls),existingCoreFunctions=3,uncoveredArm7Candidates=2)),flush=True)
if __name__=='__main__':main()
