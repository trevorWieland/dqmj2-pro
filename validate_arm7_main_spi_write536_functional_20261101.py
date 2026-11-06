import copy
import gzip
import hashlib
import json
from pathlib import Path
import qualify_arm7_main_spi_write536_functional_20261101 as producer
from project import ROOT,sha256,write_json
PRODUCER_SHA='c703dbcb47db24b36b1ba3b03dca38bb17a23a01dc2be0a9e9ba0794f31c7e20'
CONTROLS=ROOT/'evidence/verification/arm7-main-spi-write536-functional-controls-20261101.json'
_FRESH=None


def checked(name,expected):
    p=(ROOT/name).resolve()
    if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=expected:raise ValueError('Required current writer hypothesis/input/product missing or changed')
    return p


def validate(report):
    global _FRESH
    checked(Path(producer.__file__).name,PRODUCER_SHA)
    if report['generatorSha256']!=PRODUCER_SHA:raise ValueError('Frozen functional producer differs')
    pins=json.loads(producer.PINS.read_text())['files']
    if report['pinnedInputs']!=pins:raise ValueError('Full hypothesis/input closure differs')
    for item in pins:checked(item['path'],item['sha256'])
    for row in report['results']+[report['existingSourceHelper']]:
        for name,digest in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[name],row[digest])
        for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
    for row in report['results']:
        link=row['explicitRealLink'];checked(link['lcf'],link['lcfSha256']);checked(link['linkedElf'],link['linkedElfSha256'])
        for item in link['objects']:checked(item['path'],item['sha256'])
        checked(Path(link['lcf']).parent/'caller.bin',link['compiledFunctionSha256']);trace=row['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
        if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Writer trace changed or nonzero mtime')
    if _FRESH is None:producer.main();_FRESH=json.loads(producer.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only linked functional/limited-frame witness differs')
    return dict(qualifiedFunctions=0,sourceCredit=0,matchedByteCredit=0,functionalDraftInstances=2,functionalDraftNativeBytes=536,actualOwnReturns=report['totalActualOwnReturns'],existingSourceHelperReturnsSeparateZeroCredit=report['totalExistingSourceHelperReturnsSeparateZeroCredit'])


def main():
    global _FRESH
    producer.main();report=json.loads(producer.REPORT.read_text());_FRESH=report;summary=validate(report);controls=[]
    def reject(name,path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('False functional source claim survived '+name)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('pins',('pinnedInputs',),[]),('source-credit',('sourceCredit',),1),('byte-credit',('matchedByteCredit',),536),('function-credit',('functionMatched',),True),('module-credit',('wholeModuleMatched',),True),('raw-equivalence',('fullRawMachineEquivalenceClaim',),True),('returns',('totalActualOwnReturns',),2607),('helper-returns',('totalExistingSourceHelperReturnsSeparateZeroCredit',),0),('helper-credit',('existingSourceHelper','sourceCredit'),36),('ownership',('runtimeOwnership','romArm7Offset'),0),('address',('results',0,'address'),'0x27f5810'),('program',('results',0,'program'),'child.srl'),('module',('results',0,'module'),'arm7-wram'),('mode',('results',0,'mode'),'thumb'),('source',('results',0,'sourceSha256'),'0'*64),('flags',('results',0,'compilerFlags'),[]),('header',('results',0,'sourceDependencies'),[]),('exact',('results',0,'exactByteMatch'),True),('matched',('results',0,'functionMatched'),True),('row-credit',('results',0,'sourceCredit'),268),('comparison',('results',0,'genuineLink','matchingBytes'),268),('frame-order',('results',0,'sourcePrivateFrameWriteOrderDifferences'),0),('transfer-max',('results',0,'maximumSupportedTransferredBytes'),256),('port-reads',('results',0,'orderedPortWritesAndAllReadsCompared'),False),('raw-state',('results',0,'rawRegistersAndFlagsCompared'),False),('frame-limit',('results',0,'privateFrameStoreOrderExcludedOnlyFromFunctionalProjection'),False),('concurrency',('results',0,'noConcurrencyOrInterruptObserverClaim'),False),('physical',('results',0,'providerReplacements'),['SPI']),('busy-return',('results',0,'unsupported',0,'execution','actualOwnReturn'),True),('busy-error',('results',0,'unsupported',0,'supportedErrorPathCredit'),1),('linker',('results',0,'explicitRealLink','linkerSha256'),'0'*64),('link-command',('results',0,'explicitRealLink','actualExecutedArgv'),[]),('relocations',('results',0,'explicitRealLink','unchangedEncodedRelocationsAndAddends'),False),('anchor-credit',('results',0,'explicitRealLink','zeroCodeAnchorBytes'),36),('missing-object',('results',0,'object'),'work/arm7-bulk-20261030/no-writer.o'),('missing-trace',('results',0,'trace','path'),'work/arm7-bulk-20261030/no-writer.json.gz')]
    for name,path,value in changes:reject(name,path,value)
    profile=json.loads((producer.SOURCE/'profile.json').read_text());original=(ROOT/profile['units'][0]['binary']).read_bytes();helper=(producer.WORK/'helper/real-link/caller.bin').read_bytes();wrong=[]
    for seed in profile['units']:
        name='command-'+seed['address'][2:];text=(ROOT/seed['source']).read_text();old='[0] = '+hex(producer.native.COMMANDS[int(seed['address'],0)])+';';new='[0] = '+hex(producer.native.COMMANDS[int(seed['address'],0)]^1)+';'
        if old not in text:raise ValueError('Wrong-command source mutation absent')
        source=ROOT/('generated/arm7-write536-functional-controls/'+name+'/native.c');source.parent.mkdir(parents=True,exist_ok=True);header=ROOT/seed['sourceDependencies'][0]['path'];(source.parent/header.name).write_bytes(header.read_bytes());source.write_text(text.replace(old,new),encoding='utf-8');row,comparison,body=producer.compiler.compile_unit(seed,source,producer.WORK/name,strict=False)
        if len(body)!=268 or comparison.get('exactLinkedBytes'):raise ValueError('Wrong writer extent or byte match')
        rejected=0;records=[]
        for index,case in enumerate(producer.native.cases()):
            value=producer.native.execute(original,int(seed['address'],0),body,helper,case,index);records.append(value);rejected+=not value['functionalModelPassed']
        if rejected!=616:raise ValueError('Wrong command functional rejection count differs')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=producer.WORK/name/'records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,source=row,genuineLinkComparison=comparison,actualOwnReturns=len(records),independentModelRejections=rejected,zeroCountCasesStillValid=36,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    own=producer.WORK/profile['units'][0]['address'][2:]/'real-link/caller.bin';value=producer.native.execute(original,int(profile['units'][0]['address'],0),own.read_bytes(),helper,producer.native.cases()[0],0,budget=1,allow_no_return=True)
    if value['actualOwnReturn']or value['actualNestedReturns']:raise ValueError('One-instruction prefix gained a return')
    controls.append(dict(name='one-instruction-prefix',rejected=True,execution=value));validate(json.loads(producer.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),producerSha256=PRODUCER_SHA,inputReportSha256=sha256(producer.REPORT),summary=summary,metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=1304,independentModelRejections=1232,freshSourceOnlyBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongReturns=1304,wrongRejected=1232,sourceCredit=0)),flush=True)
if __name__=='__main__':main()
