import copy
import gzip
import json
from pathlib import Path
import prove_arm7_host_irq_gap208_scope_20261101 as proof
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-host-irq-gap208-scope-controls-20261101.json'
WORK=ROOT/'work/arm7-bulk-20261030/lane-host-irq-gap208-native/controls'


def run():
    baseline=json.loads(proof.REPORT.read_text());positive=proof.validate(baseline);controls=[]
    before=proof.linker.namespace('')[1]
    def reject(label,mutator):
        changed=copy.deepcopy(baseline);mutator(changed)
        try:proof.validate(changed)
        except(ValueError,FileNotFoundError)as error:controls.append(dict(name=label,rejected=True,error=str(error)))
        else:raise ValueError('Host IRQ scope mutation survived: '+label)
    for key in('sourceCredit','nativeCodeCredit','initializedDataCredit','initializedDenominatorDelta'):
        reject('no-credit-'+key,lambda r,k=key:r.__setitem__(k,1))
    for key,value in[('schemaVersion',2),('generator','unknown.py'),('generatorSha256','0'*64),
        ('generators',[]),('ordinarySourceReconstructionPending',False),('completeImageClaim',True)]:
        reject('proof-profile-'+key,lambda r,k=key,v=value:r.__setitem__(k,v))
    for key,value in[('program','dwc/utility.bin/move/child.srl'),('module','arm7-main'),('mode','thumb'),
        ('start','0x37fb6cc'),('bytes',212),('codeBytes',208),('literalBytes',0),('rangeSha256','0'*64),
        ('initializedDenominatorDelta',208),('historicalGhidraDiscontiguousCodeAssociation',[]),
        ('whollyUnconfiguredWrapperBytes',208),('originalDataGuardRefusals',[]),('platformWordSourceBindingApproved',True)]:
        reject('current-boundary-'+key,lambda r,k=key,v=value:r['boundary'].__setitem__(k,v))
    reject('wrapper-interior-entry',lambda r:r['boundary']['entries'][0].__setitem__('address','0x37fb6cc'))
    reject('wrapper-pool-as-code',lambda r:r['boundary']['entries'][0].__setitem__('codeBytes',16))
    reject('handler-shared-code-double-credit',lambda r:r['boundary']['separatelyCallableHandlerContainingExistingIsrCode'].__setitem__('existingGhidraCodeBytes',0))
    reject('vector-wrong-root',lambda r:r['boundary']['irqVectorTable']['words'].__setitem__(8,'0x37fb6cc'))
    for key,value in[('actualOwnedNativeReturns',408),('actualInitializerAndInstallerReturnsSeparate',204),
        ('actualCallbackReturnsSeparate',198),('actualTailWriterTransfersSeparate',192),('fullOwnCodeCoverageBytes',348),
        ('unvisitedCode',[hex(proof.START)]),('unsupportedReturnCredit',1),('sourceCredit',1)]:
        reject('native-evidence-'+key,lambda r,k=key,v=value:r['native'].__setitem__(k,v))
    WORK.mkdir(parents=True,exist_ok=True)
    def bad_trace(label,change):
        raw=gzip.decompress((ROOT/baseline['native']['trace']['path']).read_bytes());rows=json.loads(raw);change(rows)
        data=(json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode();path=WORK/(label+'.json.gz')
        path.write_bytes(gzip.compress(data,mtime=0))
        def mutate(report):
            report['native']['trace'].update(path=path.relative_to(ROOT).as_posix(),rawSha256=proof.linker.digest(data),compressedSha256=sha256(path))
        reject(label,mutate)
    bad_trace('actual-return-lost',lambda r:r[0]['execution'].__setitem__('actualReturn',False))
    bad_trace('real-installer-return-lost',lambda r:r[0]['prefixes'][1].__setitem__('actualReturn',False))
    bad_trace('actual-callback-tail-lost',lambda r:r[2]['execution'].__setitem__('tailTransfers',[]))
    bad_trace('record-source-credit',lambda r:r[0].__setitem__('sourceCredit',1))
    bad_trace('case-callback-profile',lambda r:r[0]['case'].__setitem__('callback',True))
    reject('missing-native-product',lambda r:r['native']['trace'].__setitem__('path','work/arm7-bulk-20261030/lane-host-irq-gap208-native/absent-native-records.json.gz'))
    return positive,controls,before


def main():
    positive,controls,before=run()
    if before!=proof.linker.namespace('')[1]:raise ValueError('Read-only scope validation altered default function namespace')
    try:proof.native.engine.setup(0,{proof.START:b'not-source'})
    except ValueError as error:
        if str(error)!='Read-only host IRQ gap witness forbids source replacement bodies':raise
        controls.append(dict(name='read-only-engine-rejects-code-replacement',rejected=True,error=str(error)))
    else:raise ValueError('Read-only host IRQ inventory accepted code replacement')
    if proof.validate(json.loads(proof.REPORT.read_text()))!=positive:raise ValueError('Positive restoration differs')
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        producerSha256=sha256(ROOT/proof.__file__),inputReportSha256=sha256(proof.REPORT),
        negativeControls=controls,negativeControlCount=len(controls),positiveCurrentInputs=positive,
        restoredPositive=True,originalNamespaceRestored=True,sourceCredit=0,initializedDenominatorDelta=0)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),controls=len(controls))),flush=True)


if __name__=='__main__':main()
