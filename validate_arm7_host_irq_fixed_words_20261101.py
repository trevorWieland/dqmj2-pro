import copy
import json
from pathlib import Path
import prove_arm7_host_irq_fixed_words_20261101 as proof
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-host-irq-fixed-words-controls-20261101.json'


def main():
    baseline=json.loads(proof.REPORT.read_text());positive=proof.validate(baseline);controls=[]
    def reject(label,mutator):
        changed=copy.deepcopy(baseline);mutator(changed)
        try:proof.validate(changed)
        except ValueError as error:controls.append(dict(name=label,rejected=True,error=str(error)))
        else:raise ValueError('Host IRQ fixed-word mutation survived: '+label)
    for key,value in[('program','dwc/utility.bin/move/child.srl'),('processor','arm9'),('sourceCredit',1),
        ('dataCredit',8),('initializedDenominatorDelta',8),('originalCheckWordReads',0),('originalCheckWordWrites',408),
        ('originalCounterReads',0),('originalCounterWrites',204),('originalCounterInitializerWritesSeparate',0),
        ('originalCallbackZeroResetReturnsSeparate',0),('originalCallbackNonzeroResetReturnsSeparate',96)]:
        reject('profile-'+key,lambda r,k=key,v=value:r.__setitem__(k,v))
    for key,value in[('address','0x380fffc'),('bytes',8),('mode','arm'),('program','child.srl'),
        ('initializedOrBssModuleOwnership',True),('sourceDataExtentCredit',4),('originalDataGuardStillRefuses',False),
        ('sourceBindingPermissionGranted',True)]:
        reject('check-word-'+key,lambda r,k=key,v=value:r['words'][0].__setitem__(k,v))
    reject('counter-neighbor',lambda r:r['words'][1].__setitem__('address','0x27ffc40'))
    reject('caller-interior',lambda r:r['words'][0]['qualifiedOriginalCallers'][0].__setitem__('address','0x37fb640'))
    reject('caller-full-hash',lambda r:r['words'][0]['qualifiedOriginalCallers'][0].__setitem__('fullRangeSha256','0'*64))
    reject('caller-mode',lambda r:r['words'][0]['qualifiedOriginalCallers'][0].__setitem__('mode','thumb'))
    reject('primary-git-blob',lambda r:r['references'][0].__setitem__('gitBlobSha1','0'*40))
    reject('primary-SDK-equivalence',lambda r:r['references'][0].__setitem__('sameHistoricalSdkRevisionProven',True))
    reject('primary-CC0-assumption',lambda r:r['references'][0].__setitem__('licenseQualification','CC0'))
    reject('source-scope-stale',lambda r:r['inputScope'].__setitem__('sha256','0'*64))
    reject('macro-closure-overclaim',lambda r:r['platformArithmetic'].__setitem__('referenceMainMemDefinitionClosureSupplied',True))
    if proof.validate(json.loads(proof.REPORT.read_text()))!=positive:raise ValueError('Positive fixed-word restoration differs')
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        inputReportSha256=sha256(proof.REPORT),producerSha256=sha256(proof.__file__),
        negativeControls=controls,negativeControlCount=len(controls),restoredPositive=positive,
        sourceCredit=0,dataCredit=0,initializedDenominatorDelta=0)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),controls=len(controls))),flush=True)


if __name__=='__main__':main()
