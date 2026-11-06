import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_queue_unlink56_20261101 as matcher
from project import ROOT,sha256,write_json

MATCHER_SHA='bd622c5a41e0772dff99c625b48ba70859afd28a846a8faab26da37db6162103'
CONTROLS=ROOT/'evidence/verification/arm7-queue-unlink56-controls-20261101.json'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:raise ValueError('Required current initializer source/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA)
    pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen initializer generator/runtime identity differs')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Complete initializer source/runtime closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    row=report['matches'][0]
    checked(row['source'],row['sourceSha256']);checked(row['compiler'],row['compilerSha256']);checked(row['object'],row['objectSha256'])
    link=row['realLink'];checked(link['lcf'],link['lcfSha256'])
    checked(matcher.WORK/'caller/real-link/linked.elf',link['linkedElfSha256'])
    checked(matcher.WORK/'caller/real-link/caller.bin',row['targetSha256'])
    trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Current initializer trace differs or is not deterministic gzip')
    if _FRESH is None:
        matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only link/native execution/coverage/effect evidence differs')
    return {('arm7','','arm7-wram','0x37fd84c','arm'):row}


def main():
    matcher.main();report=json.loads(matcher.REPORT.read_text());validate(report);controls=[]
    def reject(label,keys,value):
        bad=copy.deepcopy(report);target=bad
        for key in keys[:-1]:target=target[key]
        target[keys[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=label,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid initializer evidence survived: '+label)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),
        ('program',('program',),'child'),('module',('module',),'arm7-main'),('source-closure',('generatorSources',),[]),
        ('runtime-pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('count',('newOrdinaryFunctionCount',),2),
        ('coverage',('matchedInitializedBytes',),100),('code-bytes',('matchedCodeBytes',),56),('literal-bytes',('generatedLiteralBytes',),0),
        ('data-credit',('originalDataHelperAssemblyOrExtentCredit',),40),('denominator',('initializedDenominatorDelta',),60),
        ('module-success',('wholeModuleLinked',),True),('full-source',('sourceReconstructionComplete',),True),
        ('address',('matches',0,'address'),'0x37fd850'),('size',('matches',0,'bytes'),52),('mode',('matches',0,'mode'),'thumb'),
        ('source',('matches',0,'sourceSha256'),'0'*64),('compiler-flags',('matches',0,'compilerFlags'),[]),
        ('blob',('matches',0,'originalObjectScaffolding'),True),('exact',('matches',0,'exactAfterDeclaredRelocation'),False),
        ('input-words',('matches',0,'sourceAbiContract','physicalArgumentWords'),0),
        ('historical-types',('matches',0,'sourceAbiContract','historicalTypesProven'),True),
        ('model',('matches',0,'oracle','independentFullMappedMemoryAndOrderedStoreModel'),False),
        ('returns',('matches',0,'oracle','actualOriginalAndCompiledReturns'),2048),('providers',('matches',0,'oracle','providerReplacements'),['memory']),
        ('unchecked-cpu',('matches',0,'oracle','rawRegistersFlagsStackModeAndMappedMemoryCompared'),False),
        ('scene',('matches',0,'oracle','wholeSceneOrHardwareContextProven'),True),
        ('wrong-binding',('nativeSymbols','native_host_arm7_data_038078b4'),'0x38078b8'),
        ('missing-object',('matches',0,'object'),'work/arm7-bulk-20261030/absent-halfword.o'),
        ('missing-trace',('matches',0,'oracle','trace','path'),'work/arm7-bulk-20261030/absent-halfword.json.gz')]
    changes.extend([('return-type',('matches',0,'sourceAbiContract','sourceReturnType'),'u32'),('residue-as-value',('matches',0,'sourceAbiContract','incidentalPhysicalR0ComparedNotSemanticReturn'),False),('branch-counts',('matches',0,'oracle','fiveWayContextCounts'),{}),('aliases',('matches',0,'oracle','syntheticAliasCases'),0)])
    for label,keys,value in changes:reject(label,keys,value)
    seed=json.loads((matcher.SOURCE/'final-seed.json').read_text());text=(ROOT/seed['source']).read_text()
    if text.count('next = node->next;')!=1 or text.count('.tail')!=1 or text.count('.head')!=1:raise ValueError('Expected queue source controls absent')
    swapped_roots=text.replace('.tail','.temporary_swap').replace('.head','.tail').replace('.temporary_swap','.head')
    swapped_links=text.replace('next = node->next;','next = node->previous;').replace('previous = node->previous;','previous = node->next;')
    wrong=[]
    for name,body_text in [('swapped-roots',swapped_roots),('swapped-links',swapped_links)]:
        source=ROOT/('generated/arm7-queue-unlink56-negative-20261101/'+name+'/native_arm7_wram_037fd84c.c');source.parent.mkdir(parents=True,exist_ok=True)
        source.write_text(body_text,encoding='utf-8')
        bad,comparison,body=matcher.compile_unit(seed,source,matcher.WORK/name,strict=False)
        if comparison.get('exactLinkedBytes'):raise ValueError('Wrong queue links matched native')
        original=(ROOT/seed['binary']).read_bytes();records=[];rejections=0
        for index in range(640):
            value=matcher.native.execute(original,body,index);records.append(value);rejections+=int(not value['modelPassed'])
        if rejections!=(384 if name=='swapped-roots' else 512):raise ValueError('Wrong queue control independent rejection count differs')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
        wrong.append(dict(name=name,compilerResult=bad,genuineLinkComparison=comparison,actualOwnReturns=640,independentModelRejections=rejections,
            trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    try:matcher.native.execute(original,(matcher.WORK/'caller/real-link/caller.bin').read_bytes(),0,budget=1)
    except ValueError:controls.append(dict(name='bounded-exhaustion',rejected=True,reason='Prefix did not return; post-state excluded'))
    else:raise ValueError('Bounded initializer prefix acquired return credit')
    validate(json.loads(matcher.REPORT.read_text()))
    result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,
        inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),
        wrongSources=wrong,wrongSourceControlCount=len(wrong),actualWrongSourceReturns=1280,independentWrongSourceModelRejections=896,
        restoredPositive=True,sourceOnlyFreshCompileBeforeValidation=True,additionalSourceCredit=0)
    write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),
        metadataControls=len(controls),wrongSourceReturns=1280,wrongSourceRejections=896)),flush=True)


if __name__=='__main__':main()
