import copy
import json
from pathlib import Path
import replay_arm7_sdk264_wireless_large_queue_20261101 as queue
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-sdk264-wireless-large-queue-controls-20261101.json'

def main():
    queue.main();profile=json.loads(queue.PROFILE.read_text());group=profile['groups'][0];controls=[]
    def rejected(name,changed):
        try:queue.compile_group(changed)
        except(ValueError,FileNotFoundError)as error:controls.append(dict(name=name,rejected=True,error=str(error)))
        else:raise ValueError('Invalid compile-ready hypothesis survived:'+name)
    for name,key,value in[('source','sourceSha256','0'*64),('compiler','compilerSha256','0'*64),('missing-source','source','nonmatching/no-sdk264-source.c'),('missing-include-closure','sourceDependencies',[])]:
        changed=copy.deepcopy(group);changed[key]=value;rejected(name,changed)
    changed=copy.deepcopy(group);changed['sourceDependencies'][0]['sha256']='0'*64;rejected('include-hash',changed)
    changed=copy.deepcopy(group);changed['sourceDependencies'][0]['path']='work/no-sdk264-include.inc';rejected('missing-include',changed)
    changed=copy.deepcopy(group);changed['targets'][0]['inputModuleSha256']='0'*64;rejected('current-input',changed)
    changed=copy.deepcopy(group);changed['targets'][0]['targetSha256']='0'*64;rejected('whole-range',changed)
    changed=copy.deepcopy(group);changed['targets'][0]['expectedRelocationMaskMatch']=not changed['targets'][0]['expectedRelocationMaskMatch'];rejected('expected-compiler-result',changed)
    queue.main();write_json(REPORT,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),replayReportSha256=sha256(queue.REPORT),controls=controls,controlCount=len(controls),sourceCredit=0,neverRegistersOrPublishesMatchedBytes=True,sharedSourceResolverUnchanged=True,allCompilationInputsClosedAndNoWorkCaches=True));print(json.dumps(dict(controls=len(controls),sha256=sha256(REPORT),sourceCredit=0)),flush=True)
if __name__=='__main__':main()

