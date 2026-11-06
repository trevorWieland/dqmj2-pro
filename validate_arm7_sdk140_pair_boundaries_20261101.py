import copy
import json
from pathlib import Path
import survey_arm7_sdk140_pair_boundaries_20261101 as survey
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-sdk140-pair-boundary-controls-20261101.json'
_FRESH=None

def validate(report):
    global _FRESH
    if _FRESH is None:_FRESH=survey.measure()
    if report!=_FRESH:raise ValueError('Current complete qualified branch/pool/module boundary evidence differs')
    for function in report['functions']:
        for module in function['modules']:
            if sha256(ROOT/module['binary'])!=module['sha256']:raise ValueError('Current full executable module changed')
    return report['functions']

def main():
    global _FRESH
    report=survey.measure();_FRESH=report;write_json(survey.REPORT,report);validate(report);controls=[]
    changes=[(('generatorSha256',),'0'*64),(('romSha256',),'0'*64),(('sourceCredit',),192),(('functions',0,'processor'),'arm9'),(('functions',0,'program'),'child.srl'),(('functions',0,'module'),'arm7-wram'),(('functions',0,'mode'),'thumb'),(('functions',0,'address'),'0x27e9b9c'),(('functions',0,'bytes'),60),(('functions',0,'codeBytes'),64),(('functions',0,'literalBytes'),0),(('functions',0,'knownOutsideInteriorBranchCount'),1),(('functions',0,'wholeProgramIndirectOrThumbReferenceCompletenessProven'),True),(('functions',0,'sharedTailOrAlternateEntryAdopted'),True),(('functions',0,'denominatorDelta'),64),(('functions',1,'bytes'),124),(('functions',1,'codeBytes'),128),(('functions',1,'literalBytes'),0),(('functions',1,'references'),[])]
    for path,value in changes:
        changed=copy.deepcopy(report);target=changed
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:validate(changed)
        except ValueError as error:controls.append(dict(path=list(path),rejected=True,error=str(error)))
        else:raise ValueError('False boundary evidence survived')
    validate(report);result=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),inputReportSha256=sha256(survey.REPORT),controls=controls,controlCount=len(controls),restoredPositive=True,sourceCredit=0)
    write_json(REPORT,result);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),controls=len(controls))),flush=True)
if __name__=='__main__':main()
