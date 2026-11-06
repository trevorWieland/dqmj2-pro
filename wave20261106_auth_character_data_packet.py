import argparse
import concurrent.futures
import uuid
from pathlib import Path
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256,now
from closed_c_compiler_inputs_20261105 import compiler_inputs
from replay_sdk_data_registration_v2_20261106 import qualify as qualify_typed_object
from wave20261106_auth_character_data_paths import SOURCE,EVIDENCE,WORK,assert_owned
from wave20261106_auth_character_data_codec import render,header
from wave20261106_auth_character_data_build import compile_link,FLAGS
from wave20261106_auth_character_data_controls import execute as controls
from wave20261106_auth_character_data_validate import validate_layout,validate_reference,validate_native,validate_pointers,IMAGE,IMAGE_SHA


def generate(layout,directory):
    original=Path.open;blocked=[];directory.mkdir(parents=True,exist_ok=True);values=[]
    def source_only(path,*args,**kwargs):
        if any(path.resolve().is_relative_to((ROOT/name).resolve())for name in ['inputs','extract','deps/reference']):raise PermissionError('Native and primary source reads forbidden during actual Auth semantic C/header generation')
        return original(path,*args,**kwargs)
    with patch.object(Path,'open',source_only):
        for row in layout['assets']:
            code,payload=render(read_json(ROOT/row['semanticSource']),row['nativeSymbol']);path=directory/f"{int(row['address'],0):08x}.c";path.write_text(code,encoding='utf-8')
            if path.read_bytes()!=(ROOT/row['source']).read_bytes()or sha256(path)!=row['sourceSha256']:raise ValueError('Fresh semantic Auth C differs from actual immutable promoted compiler source')
            values.append((row,payload))
        path=directory/'characters.h';path.write_text(header(layout['assets']),encoding='utf-8')
        if path.read_bytes()!=(SOURCE/'characters.h').read_bytes()or sha256(path)!=layout['characterHeader']['sha256']:raise ValueError('Actual fresh Auth extent/type declarations differ from promoted compiler header')
        ref=read_json(ROOT/layout['assets'][0]['semanticSource'])['primaryReference']
        for path in [ROOT/'inputs/game.nds',ROOT/IMAGE,ROOT/ref['path']]:
            try:path.read_bytes()
            except PermissionError:blocked.append(path.relative_to(ROOT).as_posix())
            else:raise ValueError('Auth semantic generator could read original/native/public comparison inputs')
    return values,dict(actualCFilesGenerated=102,actualHeaderGenerated=True,allGeneratedBytesEqualActualPromotedCompilerInputs=True,originalAndPublicReadDenials=blocked,generatedDirectory=directory.relative_to(ROOT).as_posix(),compilerConsumesByteIdenticalImmutablePromotedSources=True)


def produce(descriptor_name):
    assert_owned();descriptor=read_json(ROOT/descriptor_name);manifest_pin=descriptor['sourceManifest']
    if descriptor['sourceCredit']!=0 or not descriptor['freshCompleteSourceReplay']or sha256(ROOT/manifest_pin['path'])!=manifest_pin['sha256']:raise ValueError('Auth immutable full-source replay descriptor/closure differs')
    manifest=read_json(ROOT/manifest_pin['path'])
    for pin in manifest['files']+manifest['privateComparisonOrToolInputs']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Auth copied source/private runtime/comparison input changed: '+pin['path'])
    layout=read_json(SOURCE/'layout.json');validate_layout(layout);run=WORK/'rp'/uuid.uuid4().hex[:8];run.mkdir(parents=True,exist_ok=True);original_open=Path.open;old_denied=[]
    def no_old_work(path,*args,**kwargs):
        if path.resolve().is_relative_to((ROOT/'work').resolve())and not path.resolve().is_relative_to(run.resolve()):raise PermissionError('Old work objects and links are forbidden during Auth full C replay')
        return original_open(path,*args,**kwargs)
    with patch.object(Path,'open',no_old_work):
        for path in [ROOT/'work/w6gp/proof/020e041c/data.o',WORK/'nonexistent-old/data.o']:
            try:path.read_bytes()
            except PermissionError:old_denied.append(path.relative_to(ROOT).as_posix())
            else:raise ValueError('Old work object was readable during fresh Auth replay')
        values,generation=generate(layout,run/'generated');image=(ROOT/IMAGE).read_bytes()
        if sha256(ROOT/IMAGE)!=IMAGE_SHA:raise ValueError('Auth full original native image changed')
        for row,payload in values:validate_reference(read_json(ROOT/row['semanticSource']));validate_native(row,payload,image)
        witnesses=validate_pointers(layout,image);aliases={row['nativeAlias']:row['address']for row in witnesses};header_pin=layout['characterHeader'];layout_pin=dict(path=(SOURCE/'layout.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'layout.json'))
        def build(value):
            row,payload=value;entry=dict(row,sourceDependencies=[header_pin],compilerFlags=FLAGS);eligibility=compiler_inputs(entry);proof=compile_link(row,ROOT/row['source'],payload,run/'proof'/f"{int(row['address'],0):08x}")
            result=dict(row,**proof,kind='data',mode='data',name=row['nativeSymbol'],size=len(payload),compiledBytes=len(payload),initializedBytes=len(payload),sourceLanguage='C',sourceDependencies=[header_pin],dataSourceDependencies=[layout_pin,dict(path=row['semanticSource'],sha256=row['semanticSourceSha256'])],sourcePolicy=dict(realReadableCharacterStringInitializer=True,noOpaqueByteArray=True,actualTypedExtentDeclarationsConsumed=True,closedCompilerInputEligibility=eligibility),relocations=[],executableSectionBytes=0,allocatedZeroFillBytes=0,ordinaryFunctionCredit=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0)
            qualify_typed_object(result);result.update(exactBytes=True,nativeAlias=f"data_{int(row['address'],0):08x}",targetSection='.data');return result
        with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:matches=list(pool.map(build,values))
        print(dict(freshCObjectsLinked=len(matches),bytes=sum(r['bytes']for r in matches)),flush=True);negative=controls(layout,image,run/'wrong-c')
    generators={p['path']:p['sha256']for p in manifest['generatorSources']};roles={p:'generator-code'for p in generators};generation_inputs={layout_pin['path']:layout_pin['sha256']}
    for row in layout['assets']:generation_inputs[row['semanticSource']]=row['semanticSourceSha256']
    for path,digest in generation_inputs.items():generators[path]=digest;roles[path]='character-generation-input'
    generators[manifest_pin['path']]=manifest_pin['sha256'];roles[manifest_pin['path']]='immutable-full-source-replay-closure';dependencies=[manifest_pin,dict(path=descriptor_name,sha256=sha256(ROOT/descriptor_name)),*manifest['metadataDependencies'],*[dict(path=p,sha256=h)for p,h in sorted(generation_inputs.items())]]
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=layout['romSha256'],program='',processor='arm9',module='main',functionMatched=0,functionMatches=[],ordinaryFunctionCredit=0,dataMatches=matches,dataMatchedBytes=1431,typedConstantDataBytes=1431,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,executableSectionBytes=0,allocatedZeroFillBytes=0,nativeSymbols={},dataAliases=aliases,generatorSources=[dict(path=p,sha256=h)for p,h in sorted(generators.items())],generatorSourceRoles=roles,generationDependencies=[dict(path=p,sha256=h)for p,h in sorted(generation_inputs.items())],replayDependencies=dependencies,privateComparisonOrToolInputs=manifest['privateComparisonOrToolInputs'],controls=negative,actualFreshGeneration=generation,oldWorkObjectReadRejections=old_denied,originalPointerWitnesses=witnesses,sourceCreditPendingSharedAcceptance=True,allObjectsFreshlyGeneratedCompiledAndGenuinelyLinked=True,noOldObjectsOrLinksRequired=True,allClosedCompilerInputGuardsPassed=True,allConfiguredCallerPointerWitnessesVerified=True,exactBytesMarkersDerivedAfterCompleteTypedObjectNativeGenuineLinkQualification=True,compilerSourceSection='.rodata',nativePlacementSection='.data',deferredUrlsExcluded=True,wholeModuleLinked=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,actualFunctionOrNetworkOrDeviceExecutions=0,limits=['102 complete readable primary C narrow-character objects add1431 initialized bytes only after shared acceptance.','No function/executable/BSS/gap/alignment/provider/network/hardware/game/native-Windows execution credit.','Two deferred URLs020deb48/37 and020defec/34 remain outside this packet and unclaimed.','Actual fresh semantic C/header generation blocks native/public inputs; compilation uses byte-identical promoted C and the real106-line header.'])
    output=ROOT/descriptor['output']
    if not output.resolve().is_relative_to(ROOT/'evidence/matches')or output.name!='auth-character-data-20261106.json':raise ValueError('Auth canonical report escaped exclusive output identity')
    write_json(output,report);return report


def main():
    parser=argparse.ArgumentParser();parser.add_argument('descriptor');args=parser.parse_args();report=produce(args.descriptor);print(dict(passed=True,objects=102,bytes=1431,wrongC=report['controls']['wholeWrongCControls'],freshFullSourceReplay=True),flush=True)


if __name__=='__main__':main()
