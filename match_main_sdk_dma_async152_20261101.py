import hashlib
import json
import sys
from pathlib import Path
import compile_main_sdk_aux_batch01_20261101 as compiler
import main_sdk_dma_async152_native_20261101 as fixture
import main_sdk_dma_async152_boundaries_20261101 as boundary
from project import ROOT,write_json

WORK=ROOT/'work/main-sdk-aux/20261101/dma-async152-final'
PROFILE=ROOT/'nonmatching/main-sdk-aux/20261101/dma-async152-final/closure.json'
PROFILE_SHA='5c89fb076e2ffc03dbff8d992d9264628e54ae4291cc35629025f3cee2cb7043'
PINS=PROFILE.with_name('generator-pins.json')
PIN_SHA='b142b2c48879c44349ab810c99e720213c087909222312faaa7a5b4ef1dfd568'
REPORT=ROOT/'evidence/matches/main-sdk-dma-async152-20261101.json'
ROM='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):return hashlib.sha256(data).hexdigest()


def verify_inputs():
    import unicorn
    import elftools
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4'or elftools.__version__!='0.33':
        raise ValueError('Pinned DMA async setup runtime differs')
    if digest(PROFILE.read_bytes())!=PROFILE_SHA or digest(PINS.read_bytes())!=PIN_SHA or digest((ROOT/'inputs/game.nds').read_bytes())!=ROM:
        raise ValueError('Thread-removal source/runtime/build profile differs')
    pins=json.loads(PINS.read_text())['files']
    for row in pins:
        path=(ROOT/row['path']).resolve()
        if not path.is_relative_to(ROOT)or digest(path.read_bytes())!=row['sha256']:
            raise ValueError('Pinned DMA async setup source/include/compiler/runtime changed: '+row['path'])
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
    return dict(row,realMainLink=link,nativeSymbolEntries=bindings,nativeSymbols={n:hex(int(v['address'],0))for n,v in bindings.items()},
        exactAfterDeclaredRelocation=link['exactCallerBytes'],exactAfterRealMwLink=link['exactCallerBytes'],matchingBytes=152,compiledBytes=152,
        ordinaryFunctionCredit=1,executableInstructionBytes=152,generatedLiteralBytes=0,boundaries=boundary.boundaries(row),
        sourceAbiContract={'physicalArgumentWords':6,'argumentRegisters':4,'callerStackWords':2,'return':'void',
            'channelFixtureDomain':[0,3],'nativeChannelBoundsGuardClaimed':False,'addressesAndLengthBits':32,
            'callback':'u32(u32); selected original ARM restore-IRQ helper only','zeroLengthInvokesCallbackWithSixthWord':True,
            'nonzeroLengthOnlyStoresCallback':True,'registerShadowOnlyNoAutonomousTransfer':True},originalDataSourceCredit=0,
        sourceOnlyCompilerInput={'source':pin['source'],'sha256':pin['sourceSha256'],'includes':pin['sourceDependencies'],'originalCodeCompilerInput':False})


def proof():
    verify_inputs();pin=json.loads(PROFILE.read_text())['matches'][0];row=build(pin)
    row['oracle']=fixture.oracle((WORK/'caller/genuine-link/caller.bin').read_bytes())
    return {'matches':[row],'nativeSymbols':row['nativeSymbols'],'nativeSymbolEntries':row['nativeSymbolEntries'],
        'matchedInitializedBytes':152,'matchedInstructionBytes':152,'generatedLiteralBytes':0,'newOrdinaryFunctionCount':1,
        'newInitializedCoverageBytes':152,'originalHelperDataExtentOrAssemblyCredit':0,'initializedDenominatorDelta':0,
        'wholeModuleLinked':False,'sourceReconstructionComplete':False,'supportedContext':'idle channels0..3 register programming; sticky-busy and rejected-source bounded no-return separate'}


def main():
    pins=verify_inputs();report=proof()
    names=sorted({Path(__file__).name,PROFILE.relative_to(ROOT).as_posix(),PINS.relative_to(ROOT).as_posix()}|{r['path']for r in pins})
    report.update(schemaVersion=1,generator=Path(__file__).name,generatorSha256=digest(Path(__file__).read_bytes()),
        generatorSources=[dict(path=n,sha256=digest((ROOT/n).read_bytes()))for n in names],pinnedGeneratorAndRuntimeDependencies=pins,
        romSha256=ROM,processor='arm9',program='',module='main')
    write_json(REPORT,report);print(json.dumps({'report':REPORT.relative_to(ROOT).as_posix(),'sha256':digest(REPORT.read_bytes()),
        'newSourceBytes':152,'actualOwnReturns':report['matches'][0]['oracle']['actualOriginalAndCompiledReturns'],'helperCredit':0}),flush=True)


if __name__=='__main__':main()
