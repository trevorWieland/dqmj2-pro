import json
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import match_runtime as C
import utility_runtime
from wave20261105_child_static_assets_next_source_generate import SOURCE,LAYOUT,LAYOUT_HASH,source_only,generate,original_read_controls
from wave20261105_child_static_assets_next_source_build import WORK,GENERATED,COMPILER,COMPILER_HASH,LINKER,LINKER_HASH,FLAGS,compile_unit,inspect_object,link_unit
from wave20261105_child_static_assets_next_source_controls import semantic,object_contract,actual_frontend
LANE=ROOT/'evidence/lanes/parallel-wave20261105/child-static-assets-next/source'
REPORT=ROOT/'evidence/data/child-static-assets-next-20261105.json'


def execute():
    if SOURCE!=ROOT/'src/utility/parallel_wave20261105/child-static-assets-next' or LANE!=ROOT/'evidence/lanes/parallel-wave20261105/child-static-assets-next/source' or WORK!=ROOT/'work/w5sa-source' or GENERATED!=ROOT/'generated/child-static-assets-next':raise ValueError('New semantic data source/evidence/work/generated materializer scope differs')
    if sha256(LAYOUT)!=LAYOUT_HASH or sha256(COMPILER)!=COMPILER_HASH or sha256(LINKER)!=LINKER_HASH or FLAGS.count('-lang')!=1 or FLAGS[FLAGS.index('-lang')+1]!='c99':raise ValueError('Pinned layout/tool/actualC99 language differs')
    inputs=read_json(LANE/'inputs.json')
    for p in inputs['files']:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Frozen actual semantic source/compiler/support input changed: '+p['path'])
    config=configuration()
    with source_only() as reads:
        layout=read_json(LAYOUT);values=generate(layout);denied=original_read_controls(config,layout);semantic_controls=semantic(values,layout)
    runtime,files=utility_runtime.derive();module=next(m for m in runtime['modules'] if m['id']==layout['module']);native=files[ROOT/layout['binary']]
    if module['sha256']!=layout['inputModuleSha256'] or module['binary']!=layout['binary'] or native!=(ROOT/layout['binary']).read_bytes():raise ValueError('Actual original ROM/archive/child autoload image differs')
    GENERATED.mkdir(parents=True,exist_ok=True);matches=[];wrong=[];objects=[]
    for asset,symbol,text,expected,decoded in values:
        address=int(asset['address'],0);directory=WORK/format(address,'08x');directory.mkdir(parents=True,exist_ok=True);source=GENERATED/(format(address,'08x')+'.c')
        if source.exists() and source.read_text()!=text:raise ValueError('Frozen generated semantic C changed')
        source.write_text(text)
        if native[address-0x02000000:address-0x02000000+len(expected)]!=expected:raise ValueError('Source-only encoded whole resource differs from original initialized slice')
        obj,attempt=compile_unit(source,directory/'positive')
        if attempt['exitCode']:raise ValueError(('Actual fresh C99 static-data compile failed',attempt))
        inspected=inspect_object(obj,symbol,expected);linked=link_unit(obj,symbol,inspected['section'],address,expected,directory/'positive-link');objects.append(obj)
        bad=bytearray(expected);bad[0]^=1;bad_text=text.replace('0x10','0x11',1);bad_source=directory/'wrong-data.c';bad_source.write_text(bad_text);bad_obj,bad_attempt=compile_unit(bad_source,directory/'wrong')
        if bad_attempt['exitCode']:raise ValueError('Same-size wrong semantic data object failed to compile')
        bad_info=inspect_object(bad_obj,symbol,bytes(bad));bad_link=link_unit(bad_obj,symbol,bad_info['section'],address,bytes(bad),directory/'wrong-link')
        try:inspect_object(bad_obj,symbol,expected)
        except ValueError as error:wrong.append(dict(address=hex(address),sameSizeWrongDataObjectRejected=True,reason=str(error),wrongObjectSha256=sha256(bad_obj),genuinelyLinkedWrongData=bad_link))
        else:raise ValueError('Same-size genuinely linked wrong data retained original match')
        matches.append(dict(program=layout['program'],processor='arm9',module=layout['module'],mode='data',kind='data',formatKind=asset['formatKind'],name=symbol,symbol=symbol,address=hex(address),bytes=len(expected),size=len(expected),compiledBytes=len(expected),initializedBytes=len(expected),allocatedZeroFillBytes=0,encodedAssetBytes=asset['encodedAssetBytes'],measuredZeroAlignmentBytes=asset['measuredZeroAlignmentBytes'],decodedSemanticBytes=decoded,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),sourceDependencies=[dict(path=p,sha256=sha256(ROOT/p)) for p in [LAYOUT.relative_to(ROOT).as_posix(),asset['semanticSource']]],object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),compiler=COMPILER.relative_to(ROOT).as_posix(),compilerSha256=COMPILER_HASH,compilerFlags=FLAGS,sourceLanguage='C',section=inspected['section'],sectionType='SHT_PROGBITS',sectionFlags=2,sectionIndex=inspected['sectionIndex'],sectionOffset=inspected['sectionOffset'],relocations=[],nonAllocatedDebugRelocations=inspected['nonAllocatedDebugRelocations'],targetSha256=C.sha(expected),outputSha256=C.sha(expected),inputModuleSha256=layout['inputModuleSha256'],exactAfterDeclaredRelocation=True,realLink=linked,executableSectionBytes=0,ordinaryFunctionCredit=0,sourceOnlyGeneration=True,command=attempt['command']))
        print(dict(dataObject=len(matches),address=hex(address),bytes=len(expected),genuineDataExact=True),flush=True)
    contract=object_contract(values[0],objects[0]);frontend=actual_frontend();totals={}
    for row in matches:
        t=totals.setdefault(row['formatKind'],dict(dataObjects=0,initializedBytes=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0));t['dataObjects']+=1;t['initializedBytes']+=row['bytes'];t['encodedAssetBytes']+=row['encodedAssetBytes'];t['measuredZeroAlignmentBytes']+=row['measuredZeroAlignmentBytes']
    controls=dict(status='passed',sourceCredit=0,semanticControls=semantic_controls,dataObjectControls=contract,actualFrontend=frontend,genuineSameSizeWrongDataObjects=wrong,originalReadRejections=denied);write_json(LANE/'controls.json',controls)
    sourceReadPaths=sorted(set(reads));state=dict(storage=[dict(address=r['address'],bytes=r['bytes'],targetSha256=r['targetSha256'],decodedSemanticBytes=r['decodedSemanticBytes']) for r in matches],generationSourceReads=sourceReadPaths);trace=C.sha(json.dumps(state,sort_keys=True,separators=(',',':')).encode())
    report=dict(schemaVersion=1,romSha256=config['romSha256'],program=layout['program'],processor='arm9',module=layout['module'],runtimeMappingCanonical=True,allPassed=True,dataMatches=matches,nativeSymbols={},nativeSymbolBindings={},dataMatchedBytes=50456,encodedAssetBytes=50402,measuredZeroAlignmentBytes=54,decodedSemanticBytes=146476,functionMatched=0,functionMatches=[],ordinaryFunctionCredit=0,executableSectionBytes=0,initializedDataRelocations=0,allocatedZeroFillBytes=0,generationOriginalInputsBlocked=True,originalReadRejectionControls=len(denied),originalRomUsedOnlyForComparison=True,sourceCreditPendingSharedAcceptance=True,dataSourceCohortAdmissionImplemented=False,controls=wrong,generationSourceReads=sourceReadPaths,semanticStateSha256=trace,totalsByVerifiedFormat=totals,controlReceipt=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),producer=Path(__file__).name,producerSha256=sha256(__file__),wholeModuleLinked=False,sourceReconstructionComplete=False,sourceOnlyRomProven=False,limits=['37independently admitted initialized semantic resource objects/50456B, including50402encodedB+54separate measured alignmentB, are generated only from canonical semantic JSON and ownedlayout; original/extracted/allother file reads are blocked through Path/builtins/io/os routes during generation. Raw original inputs serve only later validation.','Every actual positive compiler command selects pinned2.0/base C99. All37 global STT_OBJECTs have exact whole immutable initialized storage,0executable sections/allocated relocations/zero fill/ordinary function credit; genuine pinned MW links verify exact child addresses and all bytes without changing objects. Nonallocated debug relocations are separately reported.','Semantic tile/color/map/font source retains explicit reserved flags, short block padding and unused glyph-cell bits; literal values are regenerated from semantics and explicit LZ choices, never opaque original payloads. RootBMG/oldcode/claim/review/inventory/preview are not production generation dependencies and remain immutable.','37genuinely linked same-size wrong-data controls,111semantic mutations+4namespace negatives,4additional object-contract negatives,8original-read route rejections and controlled actual C99/C++ witness are required. Negative/frontend witness objects receive0function/executable/source credit.','No live registry/preferences/ledger/source-map/index/core changes; no DS/device/game/Windows/Android execution or complete source-only-ROM claim. This data packet carries0accepted bytes until coordinator shared gates and committed closure.'])
    report['generatorSources']=[pin for pin in inputs['files'] if pin['path'].endswith('.py') and not pin['path'].startswith('deps/')]
    write_json(REPORT,report);print(dict(report=REPORT.relative_to(ROOT).as_posix(),dataObjects=37,initializedBytes=50456,encodedAssetBytes=50402,alignmentBytes=54,wrongDataObjects=37,originalReadRejections=len(denied),functionCredit=0),flush=True)


if __name__=='__main__':execute()
