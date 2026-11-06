import json
from pathlib import Path
import match_runtime
import probe_arm7_profiles_20261030 as compiler
import link_arm7_bulk_20261030 as linker
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-queue-unlink56-v2'
WORK=ROOT/'work/arm7-bulk-20261030/lane-queue-unlink56-v2'
def main():
    seed=json.loads((SOURCE/'seed.json').read_text());source=ROOT/seed['source'];origin=dict(source=seed['source'],sourceSha256=sha256(source));WORK.mkdir(parents=True,exist_ok=True);match_runtime.WORK=WORK/'isolated-runtime'
    compiler.COMPILER=ROOT/seed['compiler'];compiler.COMPILER_HASH=sha256(compiler.COMPILER)
    row=compiler.compile_source(seed,origin,source,(2,'off',False,True),WORK)
    result=dict(compilerResult=row,sourceCredit=0)
    if row.get('compiledBytes')==56:
        try:result['realLink']=linker.validate(row,WORK/'real-link')
        except Exception as error:result['linkFailure']=str(error)
    write_json(WORK/'report.json',result)
    print(json.dumps(dict(compiledBytes=row.get('compiledBytes'),exact=result.get('realLink',{}).get('exactLinkedBytes',False),failure=result.get('linkFailure',row.get('stderr')))),flush=True)
if __name__=='__main__':main()
