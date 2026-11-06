import argparse
import concurrent.futures
import uuid
from pathlib import Path
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256,now
from closed_c_compiler_inputs_20261105 import compiler_inputs
from replay_sdk_data_registration_v2_20261106 import qualify as qualify_typed_object
from wave20261106_aes_table_data_paths import SOURCE,EVIDENCE,WORK,REFERENCE,assert_owned
from wave20261106_aes_table_data_codec import render,header
from wave20261106_aes_table_data_build import compile_link,FLAGS
from wave20261106_aes_table_data_controls import execute as controls
from wave20261106_aes_table_data_validate import validate_layout,validate_primary,validate_native,validate_views,validate_pointers,IMAGE,IMAGE_SHA


def generate(layout,directory):
    original=Path.open;blocked=[];directory.mkdir(parents=True,exist_ok=True);values=[]
    def source_only(path,*args,**kwargs):
        if any(path.resolve().is_relative_to((ROOT/name).resolve())for name in ['inputs','extract','deps/reference']):raise PermissionError('Native/public references forbidden during AES mathematical C/header generation')
        return original(path,*args,**kwargs)
    with patch.object(Path,'open',source_only):
        for row in layout['assets']:
            code,payload=render(read_json(ROOT/row['semanticSource']),row['nativeSymbol']);path=directory/f"{int(row['address'],0):08x}.c";path.write_text(code,encoding='utf-8')
            if path.read_bytes()!=(ROOT/row['source']).read_bytes()or sha256(path)!=row['sourceSha256']:raise ValueError('Fresh mathematical AES C differs from immutable actual promoted compiler source')
            values.append((row,payload))
        path=directory/'aes_tables.h';path.write_text(header(layout['assets']),encoding='utf-8')
        if path.read_bytes()!=(SOURCE/'aes_tables.h').read_bytes()or sha256(path)!=layout['wordHeader']['sha256']:raise ValueError('Fresh actual AES word-width/table-extent declarations differ from promoted header')
        for path in [ROOT/'inputs/game.nds',ROOT/IMAGE,REFERENCE/'heimdal-rijndael-alg-fst.c',REFERENCE/'heimdal-rijndael-alg-fst.h']:
            try:path.read_bytes()
            except PermissionError:blocked.append(path.relative_to(ROOT).as_posix())
            else:raise ValueError('AES semantic generator read native/public comparison bytes')
    return values,dict(actualGeneratedWholeCTables=10,actualHeaderGenerated=True,allGeneratedBytesEqualActualPromotedCompilerInputs=True,originalAndPublicReadDenials=blocked,generatedDirectory=directory.relative_to(ROOT).as_posix(),actualCompilerUsesByteIdenticalImmutablePromotedSources=True,rawNativeAndPublishedInitializerBytesNeverUsedForGeneration=True)


def produce(descriptor_name):
    assert_owned();descriptor=read_json(ROOT/descriptor_name);manifest_pin=descriptor['sourceManifest']
    if descriptor['sourceCredit']!=0 or not descriptor['freshCompleteSourceReplay']or sha256(ROOT/manifest_pin['path'])!=manifest_pin['sha256']:raise ValueError('AES full-source replay descriptor/immutable closure changed')
    manifest=read_json(ROOT/manifest_pin['path'])
    for pin in manifest['files']+manifest['privateComparisonOrToolInputs']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('AES actual copied source/private runtime/native input changed: '+pin['path'])
    layout=read_json(SOURCE/'layout.json');validate_layout(layout);run=WORK/'rp'/uuid.uuid4().hex[:8];run.mkdir(parents=True,exist_ok=True);original_open=Path.open;denied=[]
    def no_old_work(path,*args,**kwargs):
        if path.resolve().is_relative_to((ROOT/'work').resolve())and not path.resolve().is_relative_to(run.resolve()):raise PermissionError('Old work objects/links/research are forbidden during full AES source replay')
        return original_open(path,*args,**kwargs)
    with patch.object(Path,'open',no_old_work):
        for path in [ROOT/'work/w6gp/proof/020e041c/data.o',ROOT/'work/w6ac/nonexistent-old/data.o',WORK/'nonexistent-old/data.o']:
            try:path.read_bytes()
            except PermissionError:denied.append(path.relative_to(ROOT).as_posix())
            else:raise ValueError('Old work object/research file was readable during AES replay')
        values,generation=generate(layout,run/'generated');image=(ROOT/IMAGE).read_bytes()
        if sha256(ROOT/IMAGE)!=IMAGE_SHA:raise ValueError('Complete original AES overlay6 image changed')
        aliases={};primary_proofs=[];views=[]
        for row,payload in values:
            doc=read_json(ROOT/row['semanticSource']);primary_proofs.append(validate_primary(doc,payload));validate_native(row,payload,image);aliases.update(validate_views(row,doc,payload,image));views.extend(doc['existingConfiguredInteriorElementViews'])
        if len(aliases)!=13 or len(views)!=3:raise ValueError('AES exact ten whole aliases plus three existing ambiguous views changed')
        pointers=validate_pointers(layout,image);header_pin=layout['wordHeader'];layout_pin=dict(path=(SOURCE/'layout.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'layout.json'))
        def build(value):
            row,payload=value;eligibility=compiler_inputs(dict(row,compilerFlags=FLAGS,sourceDependencies=[header_pin]));proof=compile_link(row,ROOT/row['source'],payload,run/'proof'/f"{int(row['address'],0):08x}");doc=read_json(ROOT/row['semanticSource'])
            result=dict(row,**proof,kind='data',mode='data',name=row['nativeSymbol'],size=1024,compiledBytes=1024,initializedBytes=1024,sourceLanguage='C',sourceDependencies=[header_pin],dataSourceDependencies=[layout_pin,dict(path=row['semanticSource'],sha256=row['semanticSourceSha256'])],sourcePolicy=dict(readableMathematicallyGeneratedUint32Initializer=True,noOpaqueRomByteArray=True,actualFixedWidthExtentHeaderConsumed=True,closedCompilerInputEligibility=eligibility),relocations=[],executableSectionBytes=0,allocatedZeroFillBytes=0,ordinaryFunctionCredit=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,interiorViewExtraBytes=0,existingConfiguredInteriorElementViews=doc['existingConfiguredInteriorElementViews'])
            qualify_typed_object(result);result.update(exactBytes=True,nativeAlias=f"data_ov006_{int(row['address'],0):08x}",targetSection='.rodata');return result
        with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:matches=list(pool.map(build,values))
        print(dict(freshCompleteTablesCompiledAndLinked=len(matches),bytes=sum(row['bytes']for row in matches)),flush=True);negative=controls(layout,image,run/'wrong-c')
    generators={pin['path']:pin['sha256']for pin in manifest['generatorSources']};roles={path:'generator-code'for path in generators};generation_inputs={layout_pin['path']:layout_pin['sha256']}
    for row in layout['assets']:generation_inputs[row['semanticSource']]=row['semanticSourceSha256']
    for path,digest in generation_inputs.items():generators[path]=digest;roles[path]='finite-field-table-generation-input'
    generators[manifest_pin['path']]=manifest_pin['sha256'];roles[manifest_pin['path']]='immutable-full-source-replay-closure';dependencies=[manifest_pin,dict(path=descriptor_name,sha256=sha256(ROOT/descriptor_name)),*manifest['metadataDependencies'],*[dict(path=path,sha256=digest)for path,digest in sorted(generation_inputs.items())]]
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=layout['romSha256'],program='',processor='arm9',module='ov006',functionMatched=0,functionMatches=[],ordinaryFunctionCredit=0,dataMatches=matches,dataMatchedBytes=10240,typedConstantDataBytes=10240,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,executableSectionBytes=0,allocatedZeroFillBytes=0,nativeSymbols={},dataAliases=aliases,generatorSources=[dict(path=path,sha256=digest)for path,digest in sorted(generators.items())],generatorSourceRoles=roles,generationDependencies=[dict(path=path,sha256=digest)for path,digest in sorted(generation_inputs.items())],replayDependencies=dependencies,privateComparisonOrToolInputs=manifest['privateComparisonOrToolInputs'],controls=negative,actualFreshGeneration=generation,oldWorkObjectReadRejections=denied,originalTablePointerWitnesses=pointers,completePrimaryDeclarations=primary_proofs,existingAmbiguousInteriorElementViews=views,interiorViewExtraBytes=0,interiorViewExtraObjects=0,allOriginalAmbiguousQualifiersAndPluralOverlayReferencesUnchanged=True,sourceCreditPendingSharedAcceptance=True,allWholeTablesFreshlyGeneratedCompiledAndGenuinelyLinked=True,noOldWorkObjectsOrLinksRequired=True,allClosedCompilerInputGuardsPassed=True,exactBytesMarkersDerivedAfterCompleteTypedObjectNativeGenuineLinkQualification=True,compilerSourceSection='.rodata',nativePlacementSection='.rodata',sectionRetargetingRequired=False,wholeModuleLinked=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,actualFunctionOrProviderOrNetworkOrDeviceExecutions=0,limits=['Ten complete mathematical AES/Rijndael uint32[256] arrays add10240 initialized bytes only after shared acceptance.','All13 existing native data labels retained; three ambiguous interior element views add0objects/bytes and do not resolve original main overlays(0,6) references.','No function/executable/BSS/gap/alignment/provider/network/hardware/game/native-Windows execution credit.','Actual source generation reads mathematical descriptors only and blocks original/public bytes; C compilation consumes byte-identical promoted sources and real16-line width/extent declarations.'])
    output=ROOT/descriptor['output']
    if not output.resolve().is_relative_to(ROOT/'evidence/matches')or output.name!='aes-table-data-20261106.json':raise ValueError('AES canonical report escaped owned output identity')
    write_json(output,report);return report


def main():
    parser=argparse.ArgumentParser();parser.add_argument('descriptor');args=parser.parse_args();report=produce(args.descriptor);print(dict(passed=True,objects=10,bytes=10240,genuineWrongC=report['controls']['genuineWrongCCount'],ambiguousInteriorViews=3,fullFreshSourceReplay=True),flush=True)


if __name__=='__main__':main()
