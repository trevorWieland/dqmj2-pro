import copy
import json
from pathlib import Path
import survey_arm7_core118_packet176_boundary_20261101 as producer
from project import ROOT,sha256,write_json
PRODUCER_SHA='6de12d37b9be0a08d08a4a673e49949d325783dce51a3648a842d9d693a403d6'
CONTROLS=ROOT/'evidence/verification/arm7-core118-packet176-boundary-controls-20261101.json'
_FRESH=None


def validate(report):
    global _FRESH
    if sha256(producer.__file__)!=PRODUCER_SHA or report['generatorSha256']!=PRODUCER_SHA:raise ValueError('Frozen packet176 boundary generator differs')
    if _FRESH is None:producer.main();_FRESH=json.loads(producer.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh measured bounded original-entry/code/pool/reference scan differs')
    return dict(sourceDataAssemblyAndDenominatorCredit=0)


def main():
    global _FRESH
    producer.main();report=json.loads(producer.REPORT.read_text());_FRESH=report;validate(report);controls=[]
    def reject(name,path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('False original boundary claim survived '+name)
    changes=[('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('mode',('mode',),'thumb'),('address',('address',),'0x27e91c0'),('bytes',('bytes',),168),('code',('codeBytes',),176),('pool',('literalBytes',),0),('end',('end',),'0x27e9264'),('span-hash',('spanSha256',),'0'*64),('inventory-hash',('rawInventory','sha256'),'0'*64),('inventory-row',('rawInventory','matchingRows'),[]),('module-input',('inputModules',0,'sha256'),'0'*64),('entry-target',('outsideAlignedArmBranchCandidates',0,'target'),'0x27e91c0'),('interior',('outsideInteriorBranchCandidates',),[dict(target='0x27e91c0')]),('word',('outsideAlignedLiteralWordCandidates',0,'word'),'0x27e9264'),('scan-completeness',('thumbOrOpaqueReferenceCompletenessProven',),True),('credit',('sourceAssemblyDataOrDenominatorCredit',),176),('bounded',('boundedHostAlignedScanOnly',),False)]
    for name,path,value in changes:reject(name,path,value)
    validate(json.loads(producer.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),producerSha256=PRODUCER_SHA,inputReportSha256=sha256(producer.REPORT),controls=controls,controlCount=len(controls),freshCurrentInputScanBeforeValidation=True,restoredPositive=True,sourceDataAssemblyOrDenominatorCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),sourceCredit=0)),flush=True)
if __name__=='__main__':main()
