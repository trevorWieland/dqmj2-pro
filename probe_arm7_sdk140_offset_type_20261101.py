import json
from project import ROOT,sha256,write_json
import compile_arm7_sdk140_wl_pair192_20261101 as strict
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic

def main():
    profile=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk140-wl-pair192-final/profile.json';seed=json.loads(profile.read_text())['units'][1];source=ROOT/seed['source'];directory=ROOT/'work/arm7-bulk-20261030/sdk140-offset-type-isolation-final'
    if sha256(source)!=seed['sourceSha256']:raise ValueError('Matching source changed')
    row,link,original=strict.compile_unit(seed,source,directory/'positive');text=source.read_text();body,build=diagnostic.build(seed,text.replace('unsigned long offset','unsigned int offset'),directory/'local-uint',link['bindings'])
    result=dict(generator='probe_arm7_sdk140_offset_type_20261101.py',generatorSha256=sha256(__file__),scope='Only offset local unsigned long changed to unsigned int; all interfaces/expressions unchanged',compiledBytes=len(body),matchingBytes=sum(a==b for a,b in zip(body,original)),exact=body==original,build=build,unsignedLongAloneEstablishedAsCause=False,sourceCredit=0)
    output=ROOT/'evidence/attempts/arm7-sdk140-offset-type-isolation-final-20261101.json';write_json(output,result);print(json.dumps(dict(report=output.relative_to(ROOT).as_posix(),sha256=sha256(output),exact=result['exact'],sourceCredit=0)),flush=True)
if __name__=='__main__':main()
