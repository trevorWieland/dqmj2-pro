import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_register_flag80_20261101 as matcher
from project import ROOT,sha256,write_json

MATCHER_SHA='08e075e5e71a389d88e0aa5619bfbf7b134241b1923f3ae916a3a4903be4f59b'
CONTROLS=ROOT/'evidence/verification/arm7-register-flag80-controls-20261101.json'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:raise ValueError('Required current initializer source/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen flag source/runtime identity differs')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Complete flag source/runtime closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    for dependency,rows in [(False,report['matches']),(True,report['sourceLinkedDependencies'])]:
        for row in rows:
            for key,hashkey in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[key],row[hashkey])
            for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
            link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=matcher.WORK/('dependencies'if dependency else '')/row['address'][2:]/'real-link';checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256'])
            if not dependency:
                trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
                if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Current flag trace differs or has nonzero gzip mtime')
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh complete source-chain link/ABI/state/bus evidence differs')
    return {('arm7','','arm7-wram',row['address'],'arm'):row for row in report['matches']}


def main():
    matcher.main();report=json.loads(matcher.REPORT.read_text());validate(report);controls=[]
    def reject(name,keys,value):
        bad=copy.deepcopy(report);target=bad
        for key in keys[:-1]:target=target[key]
        target[keys[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid flag evidence survived: '+name)
    for name,keys,value in [('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('namespace',('program',),'child.srl'),('processor',('processor',),'arm9'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('new-count',('newOrdinaryFunctionCount',),5),('new-bytes',('matchedInitializedBytes',),320),('code',('matchedCodeBytes',),320),('literal',('generatedLiteralBytes',),32),('denominator',('initializedDenominatorDelta',),80),('data-credit',('originalDataAssemblyOrExtentCredit',),32),('module',('wholeModuleLinked',),True),('complete-game',('sourceReconstructionComplete',),True),('double-returns',('totalActualOwnReturns',),6740),('callees-credit',('sourceLinkedDependencyBytesSeparateZeroCredit',),0),('missing-closure',('sourceLinkedDependencies',),[]),('wrong-binding',('nativeSymbols','native_host_arm7_arm_03804c7c'),'0x3804c00')]:reject(name,keys,value)
    for i in range(2):
        for name,keys,value in [('address',('address',),'0x3804cf4'),('mode',('mode',),'thumb'),('source',('sourceSha256',),'0'*64),('flags',('compilerFlags',),[]),('blob',('originalObjectScaffolding',),True),('exact',('exactBytes',),False),('arg-erasure',('sourceAbiContract','physicalArgumentWords'),0),('word-narrowing',('sourceAbiContract','maskWordConsumedWithoutNarrowing'),False),('read-selector',('sourceAbiContract','readSelector'),1),('write-selector',('sourceAbiContract','writeSelector'),1),('physical',('oracle','physicalPeripheralExecution'),True),('providers',('oracle','providerReplacements'),['reader']),('raw-state',('oracle','rawRegistersFlagsStackAndMappedMemoryCompared'),False),('model',('oracle','independentWordArgumentHalfwordPortStackAndLowByteModel'),False),('coverage',('oracle','allOwnAndDependencyInstructionsVisited'),False),('cached-callee',('oracle','sourceLinkedDependenciesFreshlyBuilt'),False),('returns',('oracle','actualOriginalAndCompiledReturns'),337),('busy',('oracle','busyPhases'),2),('scene',('oracle','wholeSceneOrHardwareContextProven'),True),('missing-object',('object',),'work/arm7-bulk-20261030/absent-flag.o'),('missing-trace',('oracle','trace','path'),'work/arm7-bulk-20261030/absent-flag.json.gz')]:reject(str(i)+'-'+name,('matches',i)+keys,value)
    for i in range(3):
        reject('dependency'+str(i),('sourceLinkedDependencies',i,'sourceSha256'),'0'*64);reject('dependency-credit'+str(i),('sourceLinkedDependencies',i,'sourceCredit'),1)
    profile=json.loads((matcher.SOURCE/'profile.json').read_text());original=(ROOT/profile['units'][0]['binary']).read_bytes();lower={int(seed['address'],0):(matcher.WORK/'dependencies'/seed['address'][2:]/'real-link/caller.bin').read_bytes()for seed in profile['dependencies']};wrong=[]
    for i,(name,old,new,expected)in enumerate([('and-instead-of-set','value | mask','value & mask',329),('or-instead-of-clear','value & ~mask','value | ~mask',321)]):
        seed=profile['units'][i];text=(ROOT/seed['source']).read_text();assert old in text;source=ROOT/('generated/arm7-register-flag80-controls-20261101/'+name+'/'+Path(seed['source']).name);source.parent.mkdir(parents=True,exist_ok=True);source.write_text(text.replace(old,new),encoding='utf-8');row,comparison,body=matcher.compile_unit(seed,source,matcher.WORK/name,strict=False)
        if len(body)!=seed['bytes']or comparison.get('exactLinkedBytes'):raise ValueError('Wrong flag C matched or escaped its full extent')
        entry=int(seed['address'],0);bodies=dict(lower);bodies[entry]=body;records=[];rejects=0
        for index,case in enumerate(matcher.native.cases()):
            value=matcher.native.execute(original,bodies,entry,case,index);records.append(value);rejects+=not value['modelPassed']
        if rejects!=expected:raise ValueError('Wrong flag model rejection count differs '+str(rejects))
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,compilerResult=row,genuineLinkComparison=comparison,actualOwnReturns=337,independentModelRejections=rejects,sourceLinkedDependenciesRetained=True,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    seed=profile['units'][0];entry=int(seed['address'],0);bodies=dict(lower);bodies[entry]=(matcher.WORK/seed['address'][2:]/'real-link/caller.bin').read_bytes();value=matcher.native.execute(original,bodies,entry,matcher.native.cases()[0],0,budget=1,allow_no_return=True)
    if value['actualOwnReturn']or value['actualNestedReturns']:raise ValueError('Prefix gained return credit')
    controls.append(dict(name='one-instruction-prefix',rejected=True,execution=value));validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=674,independentWrongSourceRejections=650,sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0)
    write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongReturns=674,modelRejections=650)),flush=True)
if __name__=='__main__':main()
