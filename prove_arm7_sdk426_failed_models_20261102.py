import gzip
import hashlib
import types
import json
from pathlib import Path
import match_runtime
from project import ROOT,sha256,write_json

def main():
    records=[];profile=ROOT/'provenance/arm7-sdk426-failed-models-20261102.json';main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    for row in json.loads(profile.read_text(encoding='utf-8'))['models']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Historical failed-model source changed')
        raw=gzip.decompress((ROOT/row['path']).read_bytes())
        if hashlib.sha256(raw).hexdigest()!=row['rawSha256']:raise ValueError('Historical unmodified raw source differs')
        module=types.ModuleType('historical_'+str(row['index']));module.__file__=str(ROOT/row['path']);exec(compile(raw.decode('utf-8'),module.__file__,'exec'),module.__dict__);case=module.cases()[row['index']];result=module.run(main,wram,case,row['index'])
        if not result['actualOwnReturn']or result['modelPassed']:raise ValueError('Failed model must be rejected after actual native return')
        records.append(dict(historicalSource=row,case=case,actualOriginalReturn=True,modelPassed=False,failedChecks=[k for k,v in result['modelChecks'].items()if not v],sourceCredit=0))
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),profileSha256=sha256(profile),records=records,actualOriginalDiagnosticReturns=len(records),sourceCredit=0,notAddedToCanonicalPositiveCounts=True);write_json(ROOT/'evidence/attempts/arm7-sdk426-failed-model-replay-20261102.json',report);print(json.dumps(dict(actualDiagnosticReturns=len(records),failedModelsRejected=len(records),sourceCredit=0)),flush=True)

if __name__=='__main__':main()
