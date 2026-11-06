import copy
import gzip
import hashlib
import json
from pathlib import Path
import prove_arm7_core117_gap52_20261101 as producer
from project import ROOT,sha256,write_json
PRODUCER_SHA='2e02e0ac2e8fbe25e4270f9f8c843a55debb05e8f15a62a6dacb6914fcbdec60'
CONTROLS=ROOT/'evidence/verification/arm7-core117-gap52-controls-20261101.json'
_FRESH=None


def validate(report):
    global _FRESH
    if sha256(producer.__file__)!=PRODUCER_SHA or report['generatorSha256']!=PRODUCER_SHA:raise ValueError('Frozen native gap witness changed')
    trace=report['trace'];path=(ROOT/trace['path']).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=trace['compressedSha256']:raise ValueError('Native gap trace missing or changed')
    raw=path.read_bytes()
    if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Gap record content or deterministic mtime differs')
    if _FRESH is None:producer.main();_FRESH=json.loads(producer.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh full-span original ARM tail/read-cap/return witness differs')
    return dict(sourceCredit=0,assemblySourceCredit=0,initializedDenominatorDelta=0,proposedOriginalGapBytes=52)


def main():
    global _FRESH
    producer.main();report=json.loads(producer.REPORT.read_text());_FRESH=report;validate(report);controls=[]
    def reject(name,path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid original gap claim survived '+name)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-main'),('mode',('mode',),'thumb'),('entry',('address',),'0x37fb458'),('span-size',('bytes',),48),('code-size',('codeBytes',),52),('pool-size',('literalBytes',),0),('denominator',('initializedDenominatorDelta',),52),('source-credit',('sourceCredit',),52),('asm-credit',('assemblySourceCredit',),48),('match-credit',('functionMatchedBytes',),52),('data-credit',('originalDataSourceCredit',),4),('configuration',('sharedConfigOrInventoryEdited',),True),('module-input',('moduleInputSha256',),'0'*64),('span-hash',('spanSha256',),'0'*64),('inventory',('rawInventorySha256',),'0'*64),('pool',('bounds','pool'),'0x37fb480'),('end',('bounds','end'),'0x37fb484'),('tail-mode',('qualifiedIncomingTail','targetMode'),'thumb'),('tail-address',('qualifiedIncomingTail','address'),'0x27ea630'),('tail-target',('qualifiedIncomingTail','target'),'0x37fb458'),('tail-word',('qualifiedIncomingTail','literalHash'),'0'*64),('actual-bx',('qualifiedIncomingTail','actualBxToEntryObserved'),False),('runs',('actualEntryExecutions',),216),('overlap-count',('observedGapReturnsOverlapTailRunsNotAdditionalExecutions',),False),('direct-returns',('totals','directGapCompleteReturns'),0),('tail-returns',('totals','tailEntryCompleteReturns'),0),('missing-trace',('trace','path'),'work/arm7-bulk-20261030/no-gap.json.gz')]
    for name,path,value in changes:reject(name,path,value)
    prefix=[]
    for tail in(False,True):
        try:producer.execute(producer.cases()[0],0,tail,budget=1)
        except ValueError as error:prefix.append(dict(tail=tail,rejected=True,reason=str(error),returnCredit=0,postStateCredit=0))
        else:raise ValueError('Original one-instruction gap prefix acquired a return')
    controls.append(dict(name='one-instruction-prefixes',rejected=True,executions=prefix));validate(json.loads(producer.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),producerSha256=PRODUCER_SHA,inputReportSha256=sha256(producer.REPORT),controls=controls,controlCount=len(controls),freshOriginalNativeWitnessBeforeValidation=True,restoredPositive=True,sourceCredit=0,assemblySourceCredit=0,initializedDenominatorDelta=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),sourceCredit=0)),flush=True)
if __name__=='__main__':main()
