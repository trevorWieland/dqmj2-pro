from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from qualify_child_message_data_additions_20261106 import selected_data,identity
from closed_c_compiler_inputs_20261105 import compiler_inputs
from replay_sdk_data_registration_v2_20261106 import qualify as qualify_typed_object
from wave20261106_gp_character_data_additions import link as fresh_link
from wave20261106_auth_character_data_paths import SOURCE,EVIDENCE
from wave20261106_auth_character_data_codec import render
from wave20261106_auth_character_data_build import COMPILER,COMPILER_HASH,LINKER,LINKER_HASH,FLAGS
from wave20261106_auth_character_data_validate import validate_layout,validate_reference,validate_native,validate_pointers,IMAGE,IMAGE_SHA


def require(value,message):
    if not value:raise ValueError(message)


def membership(before,after,expected,functions):
    layout=read_json(SOURCE/'layout.json');validate_layout(layout);admitted={identity(row):row for row in read_json(EVIDENCE/'data-claim.json')['claimedStorage']};assets={identity(row):row for row in layout['assets']};wanted={identity(row):row['bytes']for row in expected}
    require(len(expected)==len(wanted)==102 and sum(wanted.values())==1431,'Auth exact102/1431 additions differ')
    require(set(after)-set(before)==set(wanted)==set(admitted)==set(assets),'Auth additions cross exact admitted whole-character objects')
    require(wanted=={key:row['bytes']for key,row in admitted.items()},'Auth admitted complete extents changed')
    require(all(identity(row)==key for key,row in after.items()),'Auth selected data identity differs from its key')
    for key,row in before.items():require(key in after and after[key]==row,'Earlier selected data row changed')
    occupied=[(key[:3],key[4],key[4]+row.get('bytes',row.get('size')))for key,row in before.items()]
    for row in functions.values():
        key=identity(dict(row,kind='data'));occupied.append((key[:3],key[4],key[4]+row['size']))
    for key in sorted(admitted):
        require(key[:4]==('','arm9','main','data'),'Auth data namespace changed');end=key[4]+wanted[key]
        require(not any(scope==key[:3]and max(key[4],start)<min(end,stop)for scope,start,stop in occupied),'Auth data overlaps earlier selected data/function or another addition')
        occupied.append((key[:3],key[4],end))
    return layout,admitted,assets


def validate(row,asset,admitted,layout,image):
    require(row['kind']==row['mode']=='data'and row['exactBytes']is True,'Auth row is not exact typed data')
    require(all(row[key]==0 for key in ['ordinaryFunctionCredit','executableSectionBytes','allocatedZeroFillBytes','encodedAssetBytes','measuredZeroAlignmentBytes']),'Auth data confers code/BSS/gap/alignment credit')
    require(row['sourceLanguage']=='C'and row['relocations']==[]and row['formatKind']=='whole-primary-c-character-object','Auth data is not ordinary complete readable character C')
    require(row['compiler']==COMPILER.relative_to(ROOT).as_posix()and row['compilerSha256']==COMPILER_HASH and row['compilerFlags']==FLAGS,'Auth genuine ordinary-C compiler profile changed')
    require(row['source']==asset['source']and row['sourceSha256']==asset['sourceSha256']==sha256(ROOT/row['source']),'Auth actual promoted C source changed')
    require(row['semanticSource']==asset['semanticSource']==admitted['semanticSource']and sha256(ROOT/row['semanticSource'])==asset['semanticSourceSha256']==admitted['semanticSourceSha256'],'Auth admitted complete semantics changed')
    require(row['sourceDependencies']==[layout['characterHeader']],'Auth actual typed C header dependency changed')
    for pin in row['sourceDependencies']:require(sha256(ROOT/pin['path'])==pin['sha256'],'Auth real C header changed')
    wanted={str((SOURCE/'layout.json').relative_to(ROOT).as_posix()):sha256(SOURCE/'layout.json'),asset['semanticSource']:asset['semanticSourceSha256']};observed={p['path']:p['sha256']for p in row['dataSourceDependencies']}
    require(len(row['dataSourceDependencies'])==2 and wanted==observed,'Auth actual generation dependencies changed or were confused with C includes')
    for path,digest in observed.items():require(sha256(ROOT/path)==digest,'Auth semantic/layout generation source changed')
    doc=read_json(ROOT/row['semanticSource']);code,payload=render(doc,row['nativeSymbol']);require((ROOT/row['source']).read_text(encoding='utf-8')==code,'Auth actual readable C initializer changed')
    require(row['bytes']==row['size']==row['compiledBytes']==row['initializedBytes']==len(payload)==admitted['bytes'],'Auth whole character extent changed')
    address=int(row['address'],0);require(row['nativeAlias']==f'data_{address:08x}'and row['nativeSymbol']==asset['nativeSymbol']and row['section']=='.rodata'and row['targetSection']=='.data','Auth configured data alias or placement changed')
    validate_reference(doc);validate_native(row,payload,image);compiler_inputs(row);qualify_typed_object(row)
    require(sha256(ROOT/row['realLink']['lcf'])==row['realLink']['lcfSha256'],'Auth original genuine placement contract changed')
    return payload


def qualify(before,after,expected,functions,directory):
    require(sha256(COMPILER)==COMPILER_HASH and sha256(LINKER)==LINKER_HASH,'Auth pinned compiler/linker changed');layout,admitted,assets=membership(before,after,expected,functions);image=(ROOT/IMAGE).read_bytes();require(sha256(ROOT/IMAGE)==IMAGE_SHA,'Full original Auth native image changed');witnesses=validate_pointers(layout,image);proofs=[]
    for key in sorted(admitted):
        row=after[key];payload=validate(row,assets[key],admitted[key],layout,image);actual=fresh_link(row,payload,Path(directory)/f'main-{key[4]:08x}');proofs.append(dict(program='',processor='arm9',module='main',address=hex(key[4]),initializedBytes=len(payload),realLink=actual))
    result=dict(passed=True,newInitializedDataObjects=102,newInitializedDataBytes=1431,newTypedConstantDataBytes=1431,newEncodedAssetBytes=0,newDataAlignmentBytes=0,newSourceFunctions=0,newExecutableBytes=0,newBssBytes=0,newGapBytes=0,earlierDataPreserved=len(before),configuredCallerWitnessObjects=len(witnesses),proofs=proofs,sourceCreditPendingSharedAcceptance=True);write_json(Path(directory)/'qualification.json',result);return result
