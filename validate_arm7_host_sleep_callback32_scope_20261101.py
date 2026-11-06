import copy
import gzip
import json
from pathlib import Path
import prove_arm7_host_sleep_callback32_scope_20261101 as proof
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-host-sleep-callback32-scope-controls-20261101.json'
WORK=ROOT/'work/arm7-bulk-20261030/lane-host-sleep-callback32-native/controls'


def main():
    baseline=json.loads(proof.REPORT.read_text());positive=proof.validate(baseline);controls=[]
    namespace=proof.linker.namespace('')[1]
    def reject(label,change):
        report=copy.deepcopy(baseline);change(report)
        try:proof.validate(report)
        except ValueError as error:controls.append(dict(name=label,rejected=True,error=str(error)))
        else:raise ValueError('Callback scope mutation survived: '+label)
    for key,value in[('schemaVersion',2),('generator','unknown.py'),('generatorSha256','0'*64),('generators',[]),
        ('sourceCredit',1),('initializedDenominatorDelta',32),('sleepCallerCompleteSourceCredit',164)]:
        reject('profile-'+key,lambda r,k=key,v=value:r.__setitem__(k,v))
    for key,value in[('program','dwc/utility.bin/move/child.srl'),('processor','arm9'),('module','arm7-main'),
        ('mode','thumb'),('address','0x37fc510'),('bytes',36),('codeBytes',32),('literalBytes',0),('fullRangeSha256','0'*64),
        ('configuredOverlap',[{'parent':'0x37fc468'}]),('originalNamespaceStillRefusesEntry',False)]:
        reject('boundary-'+key,lambda r,k=key,v=value:r['boundary'].__setitem__(k,v))
    reject('ARM9-alarm-offset',lambda r:r['boundary']['nativeSlotAbi'].__setitem__('threadAlarmOffset',0xB0))
    reject('tail-literal-neighbor',lambda r:r['boundary']['literalWords'][0].__setitem__('value','0x37fc370'))
    for key,value in[('actualCallbackReturns',144),('actualWakeTailTransfersSeparate',144),('callbackCodeCoverageBytes',32),
        ('sleepCallerPrefixBoundaryStops',0),('sleepCallerActualOuterReturns',7),('sleepCallerReturnCredit',7),
        ('sourceCredit',32),('nativeCodeCredit',32),('unsupportedReturnCredit',1)]:
        reject('native-'+key,lambda r,k=key,v=value:r['native'].__setitem__(k,v))
    WORK.mkdir(parents=True,exist_ok=True)
    def trace_mutation(label,change):
        payload=json.loads(gzip.decompress((ROOT/baseline['native']['trace']['path']).read_bytes()));change(payload)
        raw=(json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode();path=WORK/(label+'.json.gz');path.write_bytes(gzip.compress(raw,mtime=0))
        def mutate(report):report['native']['trace'].update(path=path.relative_to(ROOT).as_posix(),rawSha256=proof.linker.digest(raw),compressedSha256=sha256(path))
        reject(label,mutate)
    trace_mutation('actual-callback-return-lost',lambda r:r['records'][0]['execution'].__setitem__('actualReturn',False))
    trace_mutation('wake-tail-evidence-lost',lambda r:r['records'][0]['execution'].__setitem__('wakeDirectTailEntries',[]))
    trace_mutation('prefix-fake-return',lambda r:r['prefixes'][0]['execution'].__setitem__('actualReturn',True))
    trace_mutation('prefix-wrong-delay',lambda r:r['prefixes'][-1]['actualCallArguments'].__setitem__('tickHigh',0))
    reject('missing-product-fixed-diagnostic',lambda r:r['native']['trace'].__setitem__('path','work/arm7-bulk-20261030/lane-host-sleep-callback32-native/nonexistent.json.gz'))
    for label,kwargs,message in [('code-replacement',dict(bodies={proof.ENTRY:b'not-source'}),'Read-only Sleep callback inventory forbids replacement bodies'),
        ('wrong-producer-stop',dict(stop_at=0x037FC4D0),'Unqualified Sleep caller prefix boundary')]:
        try:proof.native.engine.setup(0,**kwargs)
        except ValueError as error:
            if str(error)!=message:raise
            controls.append(dict(name=label,rejected=True,error=message))
        else:raise ValueError('Read-only callback engine control survived: '+label)
    if namespace!=proof.linker.namespace('')[1]or proof.validate(json.loads(proof.REPORT.read_text()))!=positive:
        raise ValueError('Positive callback/default-namespace restoration differs')
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),producerSha256=sha256(proof.__file__),
        inputReportSha256=sha256(proof.REPORT),negativeControls=controls,negativeControlCount=len(controls),restoredPositive=positive,
        originalNamespaceRestored=True,sourceCredit=0,initializedDenominatorDelta=0)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),controls=len(controls))),flush=True)


if __name__=='__main__':main()
