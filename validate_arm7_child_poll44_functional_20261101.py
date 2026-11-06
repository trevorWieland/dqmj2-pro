import copy
import gzip
import hashlib
import json
from pathlib import Path
import qualify_arm7_child_poll44_functional_20261101 as producer
from project import ROOT,sha256,write_json
PRODUCER_SHA='426e8dabab76210f2dccbb94f2fe6f753e3d2ce59fc8a8194154a8b99df0a998'
CONTROLS=ROOT/'evidence/verification/arm7-child-poll44-functional-controls-20261101.json'
_FRESH=None


def checked(name,digest):
    p=(ROOT/name).resolve()
    if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=digest:raise ValueError('Current bounded-poll source/input/product missing or changed')
    return p


def validate(report):
    global _FRESH
    checked(Path(producer.__file__).name,PRODUCER_SHA);pins=json.loads(producer.PINS.read_text())['files']
    if report['generatorSha256']!=PRODUCER_SHA or report['pinnedInputs']!=pins:raise ValueError('Frozen functional-poll source/input closure differs')
    for item in pins:checked(item['path'],item['sha256'])
    row=report['row']
    for name,digest in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[name],row[digest])
    for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
    link=report['explicitRealLink']
    for name,digest in [('lcf','lcfSha256'),('object','objectSha256'),('linkedElf','linkedElfSha256')]:checked(link[name],link[digest])
    checked(Path(link['lcf']).parent/'caller.bin',link['linkedCodeSha256']);trace=report['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Functional poll native records changed or have nonzero mtime')
    if _FRESH is None:producer.main();_FRESH=json.loads(producer.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only linked limited poll evidence differs')
    return dict(sourceCredit=0,functionMatched=False,matchedByteCredit=0,actualOwnReturns=report['actualOriginalAndCompiledOwnReturns'])


def main():
    global _FRESH
    producer.main();report=json.loads(producer.REPORT.read_text());_FRESH=report;validate(report);controls=[]
    def reject(name,path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('False bounded-poll source claim survived '+name)
    changes=[('generator',('generatorSha256',),'0'*64),('pins',('pinnedInputs',),[]),('source-credit',('sourceCredit',),1),('function-credit',('functionMatched',),True),('byte-credit',('matchedByteCredit',),44),('module-credit',('wholeModuleMatched',),True),('game',('sourceReconstructionComplete',),True),('address',('identity','address'),'0x37fb790'),('program',('identity','program'),''),('module',('identity','module'),'arm7-wram'),('mode',('identity','mode'),'thumb'),('source',('row','sourceSha256'),'0'*64),('flags',('row','compilerFlags'),[]),('header',('row','sourceDependencies'),[]),('comparison',('genuineNativeComparison','matchingBytes'),44),('returns',('actualOriginalAndCompiledOwnReturns',),691),('readcap',('supportedPeripheralContract','testedMaximumReadCount'),4096),('return-values',('supportedPeripheralContract','rawReturnValues'),[0,1]),('timeout-return',('supportedPeripheralContract','limitExhaustionIsAnActualReturnNotErrorClaim'),False),('physical-timing',('physicalHardwareTimingProven',),True),('initial-order',('initialInstructionOrderDiffers',),False),('definite-assignment',('sourceControlDomain','readyAssignedBeforeEveryFeasibleSourceRead'),False),('initial-counter',('sourceControlDomain','remainingInitialValue'),0),('other-uninit',('sourceControlDomain','readDominanceDoesNotGeneralizeToOtherUninitializedDeclarations'),False),('raw-state',('fullRawRegistersFlagsAndOrderedReadsAndMappedFrameIoCompared',),False),('coverage',('allOwnInstructionsVisited',),False),('missing-object',('row','object'),'work/arm7-bulk-20261030/no-poll.o'),('missing-trace',('trace','path'),'work/arm7-bulk-20261030/no-poll.json.gz')]
    for name,path,value in changes:reject(name,path,value)
    seed=json.loads((producer.SOURCE/'seed.json').read_text());text=(ROOT/seed['source']).read_text();original=(ROOT/seed['binary']).read_bytes();wrong=[]
    for name,old,new in [('wrong-mask','&0x80','&0x40'),('wrong-bound','remaining=4000','remaining=4096')]:
        if old not in text:raise ValueError('Wrong poll source mutation absent')
        folder=ROOT/('generated/arm7-poll44-functional-controls/'+name);folder.mkdir(parents=True,exist_ok=True);header=folder/'native_poll_types.h';header.write_bytes((ROOT/seed['sourceDependencies'][0]['path']).read_bytes());source=folder/'native.c';source.write_text(text.replace(old,new),encoding='utf-8');wrong_seed=dict(seed,sourceDependencies=[dict(path=header.relative_to(ROOT).as_posix(),sha256=sha256(header))]);row,comparison,body=producer.compiler.compile_unit(wrong_seed,source,producer.WORK/name,strict=False)
        if len(body)!=44 or comparison.get('exactLinkedBytes'):raise ValueError('Wrong poll matched or escaped full source scope')
        rejected=0;records=[]
        for index,case in enumerate(producer.native.cases()):
            value=producer.native.execute(original,body,case,index);records.append(value);rejected+=not value['modelPassed']
        if not rejected:raise ValueError('Wrong bounded poll survived independent return/read/model checks')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=producer.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,source=row,genuineLinkComparison=comparison,actualOwnReturns=len(records),independentModelRejections=rejected,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    original_code=original[producer.native.ENTRY-producer.native.BASE:producer.native.ENTRY-producer.native.BASE+44];source_code=(producer.WORK/'caller/real-link/caller.bin').read_bytes();prefix=[]
    for name,body in [('original',original_code),('compiled',source_code)]:
        value=producer.native.execute(original,body,producer.native.cases()[0],0,budget=1,allow_no_return=True)
        if value['actualOwnReturn']or value['actualNestedReturns']:raise ValueError('One-instruction prefix gained return credit')
        prefix.append(dict(kind=name,execution=value))
    controls.append(dict(name='distinct-initial-instruction-prefixes',rejected=True,prefixes=prefix,prefixEquivalenceClaim=False));validate(json.loads(producer.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),producerSha256=PRODUCER_SHA,inputReportSha256=sha256(producer.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=sum(x['actualOwnReturns']for x in wrong),independentWrongSourceRejections=sum(x['independentModelRejections']for x in wrong),sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongReturns=result['actualWrongOwnReturns'],modelRejections=result['independentWrongSourceRejections'],sourceCredit=0)),flush=True)
if __name__=='__main__':main()
