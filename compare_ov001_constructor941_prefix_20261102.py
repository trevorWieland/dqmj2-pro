import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import gzip
import json
from project import ROOT,read_json,write_json,sha256

def execute():
    reports=[ROOT/f'evidence/application/ov001-constructor{tag}-warm-prefix-20261102.json'for tag in [938,940]]
    inputs=[read_json(p)for p in reports]
    traces=[json.loads(gzip.decompress((ROOT/r['generatedTrace']['path']).read_bytes()))for r in inputs]
    if len(traces[0])!=60 or len(traces[1])!=60:raise ValueError('941 expected sixty independently modeled prefixes per implementation')
    fields=['draw','level','stat','add','cacheIndex','cachePointer','expectedTemplate','actualTemplate','rngState','unfinishedCheckpoint']
    rows=[]
    for left,right in zip(*traces):
        differences=[key for key in fields if left[key]!=right[key]]
        if differences:raise ValueError(('941 prefix differs',differences))
        rows.append(dict(draw=left['draw'],level=left['level'],stat=left['stat'],add=left['add'],matchingFields=fields,allPassed=True))
    result=dict(schemaVersion=1,allPassed=True,sourceCredit=0,comparedCases=60,nativePrefixCheckpoints=60,sourcePrefixCheckpoints=60,actualTopReturns=0,additionalExecutions=0,inputs=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in reports],cases=rows,limitations=['Derived comparison of already executed/report-hashed cases; zero additional native/source executions are counted here.','Complete genuine1340-byte C remains unmatched to native1352; only unfinished prefix before cache cleanup compared.','Each run independently compares its own complete nonstackRAM model; code images/stack layouts differ, so no cross-image raw CPU/fullRAM identity is asserted.'])
    write_json(ROOT/'evidence/application/ov001-constructor941-native-c-prefix-comparison-20261102.json',result)
    print(dict(comparedCases=60,sourceCredit=0,additionalExecutions=0))

if __name__=='__main__':execute()
