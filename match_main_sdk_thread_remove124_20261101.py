import hashlib
import json
import sys
from pathlib import Path
import compile_main_sdk_aux_batch01_20261101 as compiler
import main_sdk_thread_remove124_native_20261101 as fixture
import main_sdk_thread_remove124_boundaries_20261101 as boundary
from project import ROOT,write_json

WORK=ROOT/'work/main-sdk-aux/20261101/thread-remove124-final'
PROFILE=ROOT/'nonmatching/main-sdk-aux/20261101/thread-remove124-final/closure.json'
PROFILE_SHA='0e270554a1e4adcebf20ccb83246e0d3fde432f6ec536c66befe472c05bf1159'
PINS=PROFILE.with_name('generator-pins.json')
PIN_SHA='fdbd4bb6497fcaedb08f313168bb6ef94cecaaae6b4dcad6864b23ecda652bce'
REPORT=ROOT/'evidence/matches/main-sdk-thread-remove124-20261101.json'
ROM='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):return hashlib.sha256(data).hexdigest()


def verify_inputs():
    import unicorn
    import elftools
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4'or elftools.__version__!='0.33':
        raise ValueError('Pinned thread-removal runtime differs')
    if digest(PROFILE.read_bytes())!=PROFILE_SHA or digest(PINS.read_bytes())!=PIN_SHA or digest((ROOT/'inputs/game.nds').read_bytes())!=ROM:
        raise ValueError('Thread-removal source/runtime/build profile differs')
    pins=json.loads(PINS.read_text())['files']
    for row in pins:
        path=(ROOT/row['path']).resolve()
        if not path.is_relative_to(ROOT)or digest(path.read_bytes())!=row['sha256']:
            raise ValueError('Pinned thread-removal source/include/compiler/runtime changed: '+row['path'])
    profile=json.loads(PROFILE.read_text());accepted=json.loads((ROOT/profile['acceptedSnapshot']).read_text())['functions']
    for pin in profile['matches']:
        first=int(pin['address'],0)
        for row in accepted:
            address=int(row['address'],0)if isinstance(row['address'],str)else row['address']
            if row['program']==''and row['module']=='main'and row['mode']=='arm'and first<address+(row.get('bytes')or 1)and address<first+pin['bytes']:
                raise ValueError('Thread-removal source overlaps accepted identity')
    return pins


def build(pin):
    result=compiler.build(pin,WORK/'caller')
    if not result.get('fullLinkedExact'):raise ValueError(result)
    row=result['entry'];link=result['realMainLink'];bindings=result['qualifiedBindings']
    return dict(row,realMainLink=link,nativeSymbolEntries=bindings,nativeSymbols={n:int(v['address'],0)for n,v in bindings.items()},
        exactAfterDeclaredRelocation=link['exactCallerBytes'],exactAfterRealMwLink=link['exactCallerBytes'],matchingBytes=124,compiledBytes=124,
        ordinaryFunctionCredit=1,executableInstructionBytes=120,generatedLiteralBytes=4,boundaries=boundary.boundaries(row),
        sourceAbiContract={'physicalArgumentWords':1,'argument':'minimumB4 thread pointer','return':'raw-u32 restore-helper residue in supported contexts',
            'threadMinimumViewBytes':0xB4,'schedulerGlobalDeclaration':'extern u8[]; address-preserving typed current-pointer access',
            'schedulerGlobalDeclarationChanged':False,'totalOriginalObjectExtentClaimed':False},originalDataSourceCredit=0,
        sourceOnlyCompilerInput={'source':pin['source'],'sha256':pin['sourceSha256'],'includes':pin['sourceDependencies'],'originalCodeCompilerInput':False})


def proof():
    verify_inputs();pin=json.loads(PROFILE.read_text())['matches'][0];row=build(pin)
    row['oracle']=fixture.oracle((WORK/'caller/genuine-link/caller.bin').read_bytes())
    return {'matches':[row],'nativeSymbols':row['nativeSymbols'],'nativeSymbolEntries':row['nativeSymbolEntries'],
        'matchedInitializedBytes':124,'matchedInstructionBytes':120,'generatedLiteralBytes':4,'newOrdinaryFunctionCount':1,
        'newInitializedCoverageBytes':124,'originalHelperDataExtentOrAssemblyCredit':0,'initializedDenominatorDelta':0,
        'wholeModuleLinked':False,'sourceReconstructionComplete':False,'supportedContext':'noncurrent target only; current-target bounded no-return separate'}


def main():
    pins=verify_inputs();report=proof()
    names=sorted({Path(__file__).name,PROFILE.relative_to(ROOT).as_posix(),PINS.relative_to(ROOT).as_posix()}|{r['path']for r in pins})
    report.update(schemaVersion=1,generator=Path(__file__).name,generatorSha256=digest(Path(__file__).read_bytes()),
        generatorSources=[dict(path=n,sha256=digest((ROOT/n).read_bytes()))for n in names],pinnedGeneratorAndRuntimeDependencies=pins,
        romSha256=ROM,processor='arm9',program='',module='main')
    write_json(REPORT,report);print(json.dumps({'report':REPORT.relative_to(ROOT).as_posix(),'sha256':digest(REPORT.read_bytes()),
        'newSourceBytes':124,'actualOwnReturns':report['matches'][0]['oracle']['actualOriginalAndCompiledReturns'],'helperCredit':0}),flush=True)


if __name__=='__main__':main()
