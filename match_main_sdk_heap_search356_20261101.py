import json
from pathlib import Path
import main_sdk_heap_attribute424_compile_20261101 as compiler
import main_sdk_heap_search356_native_20261101 as fixture
from project import ROOT,sha256,write_json

WORK=ROOT/'work/main-sdk-heap/20261101/lane-search356-final'
PROFILE=ROOT/'nonmatching/main-sdk-heap/20261101/lane-search356-final/profile.json'
COMMIT_PROFILE=ROOT/'nonmatching/main-sdk-heap/20261101/lane-attribute424-final/profile.json'
REPORT=ROOT/'evidence/matches/main-sdk-heap-search356-20261101.json'
PINS=PROFILE.parent/'generator-pins.json'
ROM='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def verify_inputs():
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:
            raise ValueError('Pinned heap-search source/runtime/reference input missing or changed')
    return json.loads(PROFILE.read_text())['matches']



def proof():
    verify_inputs()
    commit_pin=json.loads(COMMIT_PROFILE.read_text())['matches'][0]
    commit_entry,commit_bindings,commit_link,unused,commit=compiler.build(commit_pin,WORK/'source-linked-commit424')
    rows=[];callers={}
    for pin in json.loads(PROFILE.read_text())['matches']:
        entry,bindings,link,unused,code=compiler.build(pin,WORK/pin['address'])
        address=int(pin['address'],0);callers[address]=code
        symbols={name:hex(int(value['address'],0)|(value.get('mode')=='thumb'))for name,value in bindings.items()}
        rows.append(dict(entry,realMainLink=link,nativeSymbolEntries=bindings,nativeSymbols=symbols,exactAfterDeclaredRelocation=True,
            exactAfterRealMwLink=True,matchingBytes=pin['bytes'],executableInstructionBytes=pin['bytes'],generatedLiteralBytes=0,
            sourceOnlyCompilerInput=dict(source=pin['source'],sha256=pin['sourceSha256'],includes=pin['sourceDependencies'],originalCodeCompilerInput=False),
            originalObjectScaffolding=False,originalDataSourceCredit=0,nativeCalleeSourceCredit=0,wholeModuleLinked=False,
            sourceAbiContract=dict(physicalArgumentWords=3,alignmentFormalBits=32,alignmentFormalSigned=True,
                supportedPositivePowerOfTwoAlignment=[1,2,4,8,16,32,64],formalZeroNegativeOrNonPowerAlignmentProven=False),
            sourceTypeHypothesis=dict(blockBytes=16,expHeapBytes=20,commonFlagsOffset=32,expHeapOffset=36,
                totalReconstructedPrefixViewBytes=56,originalTotalHeapObjectExtentProven=False)))
    evidence=fixture.oracle(ROOT,WORK,callers,commit)
    for row in rows:row['oracle']=evidence[row['address']]
    return dict(matches=rows,matchedInitializedBytes=356,matchedInstructionBytes=356,generatedLiteralBytes=0,
        newOrdinaryFunctionCount=2,newInitializedCoverageBytes=356,originalHelperDataExtentOrAssemblyCredit=0,initializedDenominatorDelta=0,wholeModuleLinked=False,
        sourceReconstructionComplete=False,nativeSymbols={name:value for row in rows for name,value in row['nativeSymbols'].items()},
        sourceLinkedCommit424=dict(entry=commit_entry,bindings=commit_bindings,realMainLink=commit_link,additionalSourceCredit=0))


def main():
    report=proof();names={Path(__file__).name,'main_sdk_heap_attribute424_compile_20261101.py',
        'main_sdk_heap_search356_native_20261101.py',PROFILE.relative_to(ROOT).as_posix(),PINS.relative_to(ROOT).as_posix()}
    names.update(item['path']for item in json.loads(PINS.read_text())['files'])
    report.update(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted(names)],
        pinnedGeneratorAndRuntimeDependencies=json.loads(PINS.read_text())['files'],
        romSha256=ROM,processor='arm9',program='',module='main')
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),
        matchedBytes=356,actualOwnReturns=sum(row['oracle']['actualOriginalAndCompiledReturns']for row in report['matches']))),flush=True)


if __name__=='__main__':main()
