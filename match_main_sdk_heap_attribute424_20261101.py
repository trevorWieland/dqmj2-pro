import hashlib
import json
import sys
from pathlib import Path
import main_sdk_heap_attribute424_compile_20261101 as compiler
import main_sdk_heap_attribute424_native_20261101 as fixture
from project import ROOT,sha256,write_json

WORK=ROOT/'work/main-sdk-heap/20261101/lane-attribute424-final'
PROFILE=ROOT/'nonmatching/main-sdk-heap/20261101/lane-attribute424-final/profile.json'
REPORT=ROOT/'evidence/matches/main-sdk-heap-attribute424-20261101.json'
PROFILE_SHA='ed1bc343b102a80368b15833dcd3778872926effd4c187b120519d00b076e6b5'
PINS=PROFILE.with_name('generator-pins.json')
PIN_SHA='6bf787a43a39b61b3e058e8cd0e19892bb6197aee605c1b632371dfefef1b69b'
ROM='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
ORIGINAL_FIXTURE='1255df3abda60dc1934320d195d3b3c5e8f766ec1ffd57149a1892192c2cda8b'


def verify_inputs():
    import unicorn
    import elftools
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4'or elftools.__version__!='0.33':
        raise ValueError('Pinned heap compiler/native proof runtime differs')
    if sha256(ROOT/'inputs/game.nds')!=ROM or sha256(ROOT/'main_heap_commit_fixture_20261101.py')!=ORIGINAL_FIXTURE:
        raise ValueError('Original measured ROM or preserved independent heap fixture differs')
    if sha256(PROFILE)!=PROFILE_SHA or sha256(PINS)!=PIN_SHA:raise ValueError('Frozen scalar heap source/runtime profile differs')
    for item in json.loads(PINS.read_text())['files']:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:
            raise ValueError('Pinned scalar heap source/runtime input missing or changed: '+item['path'])
    reference=json.loads((ROOT/'evidence/research/20261101-main-heap-attribute424-sdk-reference.json').read_text())
    if reference['commit']!='fb9b7e4dd9b5babbc114d6165f0279352bd11ecc'or not reference['referenceOnly']or reference['compilerInput']:
        raise ValueError('Comparative SDK source provenance differs')
    for item in reference['files']:
        raw=(ROOT/item['localPath']).read_bytes()
        if len(raw)!=item['bytes']or hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=item['gitBlobSha1']:
            raise ValueError('Comparative SDK Git blob/length differs')
    profile=json.loads(PROFILE.read_text());pin=profile['matches'][0]
    if pin['sourceSha256']!='0b5bc1dd7565b4983a350a589cd84c6107eb03d37be18c8134f1aa6c47861adf'or sha256(ROOT/pin['source'])!=pin['sourceSha256']:
        raise ValueError('Frozen ordinary scalar heap source differs')
    if sha256(ROOT/pin['binary'])!=pin['inputModuleSha256']:
        raise ValueError('Original measured initialized module differs')
    return pin


def proof():
    pin=verify_inputs();entry,bindings,link,unused,code=compiler.build(pin,WORK/'caller')
    if len(code)!=424 or not link['exactCallerBytes']:raise ValueError('Complete genuine heap source link failed')
    oracle=fixture.oracle(code,ROOT,WORK)
    symbols={name:hex(int(row['address'],0)|(row.get('mode')=='thumb'))for name,row in bindings.items()}
    row=dict(entry,realMainLink=link,nativeSymbolEntries=bindings,nativeSymbols=symbols,
        exactBytes=False,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,matchingBytes=424,
        ordinaryFunctionCredit=1,executableInstructionBytes=416,generatedLiteralBytes=8,
        originalObjectScaffolding=False,originalDataSourceCredit=0,nativeCalleeSourceCredit=0,wholeModuleLinked=False,
        sourceOnlyCompilerInput=dict(source=pin['source'],sha256=pin['sourceSha256'],includes=[],originalCodeCompilerInput=False),
        sourceAbiContract=dict(physicalArgumentWords=5,argumentRegisters=4,callerStackWords=1,
            directionFormalBits=16,groupStoredBits=8,alignmentStoredBits=7,directionStoredBits=1,
            returnValue='original32-bit requested start address',original32BitMemoryView=True,arbitraryHeapValidityClaimed=False),
        sourceTypeHypothesis=dict(attribute='ordinary nonvolatileu16',groupAssignment='u32 maskBits/newValue then two ordinary scalar assignments',
            originalHistoricalVolatileQualifierProven=False,originalSdkRevisionEquivalenceProven=False),oracle=oracle)
    return dict(matches=[row],nativeSymbols=symbols,nativeSymbolEntries=bindings,matchedInitializedBytes=424,
        matchedInstructionBytes=416,generatedLiteralBytes=8,newOrdinaryFunctionCount=1,newInitializedCoverageBytes=424,
        originalHelperDataExtentOrAssemblyCredit=0,initializedDenominatorDelta=0,wholeModuleLinked=False,
        sourceReconstructionComplete=False,supportedContext='bounded synthetic free/used heap list and all six original lower routines; no providers')


def main():
    report=proof();names=[Path(__file__).name,'main_sdk_heap_attribute424_compile_20261101.py',
        'main_sdk_heap_attribute424_native_20261101.py','main_heap_commit_fixture_20261101.py',PROFILE.relative_to(ROOT).as_posix(),
        'evidence/research/20261101-main-heap-attribute424-sdk-reference.json']
    names=sorted(set(names+[PINS.relative_to(ROOT).as_posix()]+[item['path']for item in json.loads(PINS.read_text())['files']]))
    report.update(pinnedGeneratorAndRuntimeDependencies=json.loads(PINS.read_text())['files'],schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in names],romSha256=ROM,processor='arm9',program='',module='main',
        originalFixtureGenerator=dict(path='main_heap_commit_fixture_20261101.py',sha256=ORIGINAL_FIXTURE,
            untouched=True,instrumentedCopy='main_sdk_heap_attribute424_native_20261101.py'),
        comparativeReference=dict(path='evidence/research/20261101-main-heap-attribute424-sdk-reference.json',
            sha256=sha256(ROOT/'evidence/research/20261101-main-heap-attribute424-sdk-reference.json'),compilerInput=False,
            publicSdkRevisionEquivalenceProven=False,publicAllocatorThresholdAndFillPolicyAdopted=False))
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),
        matchedSourceBytes=424,actualOwnReturns=1120,actualHelperReturnsSeparate=report['matches'][0]['oracle']['actualOriginalHelperReturnTotalSeparate'])),flush=True)


if __name__=='__main__':main()
