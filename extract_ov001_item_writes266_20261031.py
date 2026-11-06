import gzip
import hashlib
import json
from pathlib import Path

import match_runtime
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/application/ov001-item-byte-writes266-20261031.json'
SOURCE_REPORT=ROOT/'evidence/matches/ov001-20261031-phases259.json'
PINNED_TRACE='fc30656db69da6c8e30f12151d2ef003260d5bd7d16b6e89cac099e0d591871f'


def run():
    report=json.loads(SOURCE_REPORT.read_text());row=next(r for r in report['matches']if int(r['address'],0)==0x0220C9EC);artifact=row['oracle']['rawTraceArtifact'];path=ROOT/artifact['path']
    if artifact['sha256']!=PINNED_TRACE or sha256(path)!=artifact['sha256']:raise ValueError('Writes266 original trace artifact identity differs')
    raw=gzip.decompress(path.read_bytes())
    if hashlib.sha256(raw).hexdigest()!=artifact['uncompressedSha256']:raise ValueError('Writes266 original uncompressed identity differs')
    traces=json.loads(raw);entry=next(r for r in traces['results']if int(r['address'],0)==0x0220C9EC);vectors=[]
    for case in entry['results']:
        recipe=case['recipe'];result=case['result']
        if recipe['phase']!=0:continue
        writes=[w for w in result['writes']if w[1]==1 and 0x02380000<=w[0]<0x02380C00 and(w[0]-0x02380000)%256==0xB0]
        helper=[r for r in result['nativeDependencyActualReturns']if r['address']=='0x2065d88']
        if len(writes)!=1 or len(helper)!=1 or helper[0]['result']!=0x02300000+recipe['counter']*88:raise ValueError('Writes266 actual native item-write/getter pattern differs')
        vectors.append(dict(nativeItemIndex=recipe['counter'],nativeRowPointer=hex(helper[0]['result']),sourceOffset='0x2A',actualWriteAddressInSyntheticVm=hex(writes[0][0]),targetDescriptorOffset='0xB0',actualByte=writes[0][2]&255,actualWriteSize=writes[0][1],actualCallerReturnWord=result['returnWord'],actualCallerResultSha256=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest(),actualRamSha256=result['ramSha256']))
    if len(vectors)!=256 or sorted(v['nativeItemIndex']for v in vectors)!=list(range(256)):raise ValueError('Writes266 all256 native item indices required')
    output=dict(schemaVersion=1,romSha256=report['romSha256'],processor='arm9',program='',module='ov001',mode='arm',address='0x0220C9EC',bytes=196,moduleSha256=report['moduleInputSha256'],nativeSpanSha256=row['targetSha256'],sourceSha256=row['sourceSha256'],evidenceClass='Extraction of actual UC_HOOK_MEM_WRITE events from frozen original/source-equal native traces, no new execution',actualTraceArtifactSha256=artifact['sha256'],uncompressedTraceSha256=artifact['uncompressedSha256'],itemTable=report['itemTableEvidence'],vectors=vectors,additionalExecutions=0,additionalSourceBytes=0,additionalFunctionCredit=0,sourceCredit=0,generatorSha256=sha256(Path(__file__)),limitations=['Raw item-table byte and descriptor offset only; no item effect, value meaning, current scene or future state claim','Valid actor/descriptor/cache setup was supplied in proof259; native getter and byte copy execute actual original instructions','DescriptorB0 is distinct from eligibility descriptorAC; record33 and its writers/lifecycle are not reinterpreted','Referenced original/source trace counts belong to proof259 and are not counted again'])
    output['deterministicContentSha256']=hashlib.sha256(json.dumps(output,sort_keys=True,separators=(',',':')).encode()).hexdigest();write_json(REPORT,output);print(json.dumps(dict(vectors=len(vectors),sourceCredit=0,additionalExecutions=0,traceSha256=artifact['sha256'])))


if __name__=='__main__':run()
