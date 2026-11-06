from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from qualify_child_message_data_additions_20261106 import selected_data,identity
from closed_c_compiler_inputs_20261105 import compiler_inputs
from replay_sdk_data_registration_v2_20261106 import qualify as qualify_typed_object
from wave20261106_gp_character_data_additions import link as fresh_link
from wave20261106_aes_table_data_paths import SOURCE,EVIDENCE
from wave20261106_aes_table_data_codec import render
from wave20261106_aes_table_data_build import COMPILER,COMPILER_HASH,LINKER,LINKER_HASH,FLAGS
from wave20261106_aes_table_data_validate import validate_layout,validate_primary,validate_native,validate_views,validate_pointers,IMAGE,IMAGE_SHA


def require(value,message):
    if not value:raise ValueError(message)


def membership(before,after,expected,functions):
    layout=read_json(SOURCE/'layout.json');validate_layout(layout);admitted={identity(row):row for row in read_json(EVIDENCE/'data-claim.json')['claimedStorage']};assets={identity(row):row for row in layout['assets']};wanted={identity(row):row['bytes']for row in expected}
    require(len(expected)==len(wanted)==10 and sum(wanted.values())==10240,'AES exact ten whole objects/10240B additions differ')
    require(set(after)-set(before)==set(wanted)==set(admitted)==set(assets),'AES additions cross exact admitted whole-array identities')
    require(wanted=={key:row['bytes']for key,row in admitted.items()},'AES admitted complete typed extents changed')
    require(all(identity(row)==key for key,row in after.items()),'AES selected data identity differs from its key')
    for key,row in before.items():require(key in after and after[key]==row,'Earlier selected data row changed')
    occupied=[(key[:3],key[4],key[4]+row.get('bytes',row.get('size')))for key,row in before.items()]
    for row in functions.values():
        key=identity(dict(row,kind='data'));occupied.append((key[:3],key[4],key[4]+row['size']))
    for key in sorted(admitted):
        require(key[:4]==('','arm9','ov006','data'),'AES initialized table namespace changed');end=key[4]+wanted[key]
        require(not any(scope==key[:3]and max(key[4],start)<min(end,stop)for scope,start,stop in occupied),'AES whole table overlaps earlier data/function or another addition')
        occupied.append((key[:3],key[4],end))
    return layout,admitted,assets


def validate(row,asset,admitted,layout,image):
    require(row['kind']==row['mode']=='data'and row['exactBytes']is True,'AES row is not exact initialized typed data')
    require(all(row[key]==0 for key in ['ordinaryFunctionCredit','executableSectionBytes','allocatedZeroFillBytes','encodedAssetBytes','measuredZeroAlignmentBytes','interiorViewExtraBytes']),'AES data/view confers code/BSS/gap/alignment/storage credit')
    require(row['sourceLanguage']=='C'and row['relocations']==[]and row['formatKind']=='aes-rijndael-transform-table'and row['elementType']=='u32'and row['elementCount']==256,'AES data is not complete ordinary C uint32[256]')
    require(row['compiler']==COMPILER.relative_to(ROOT).as_posix()and row['compilerSha256']==COMPILER_HASH and row['compilerFlags']==FLAGS,'AES measured genuine ordinary-C data compiler profile changed')
    require(row['source']==asset['source']and row['sourceSha256']==asset['sourceSha256']==sha256(ROOT/row['source']),'AES actual promoted C source changed')
    require(row['semanticSource']==asset['semanticSource']==admitted['semanticSource']and sha256(ROOT/row['semanticSource'])==asset['semanticSourceSha256']==admitted['semanticSourceSha256'],'AES admitted mathematical descriptor changed')
    require(row['sourceDependencies']==[layout['wordHeader']],'AES actual fixed-width/extent C header dependency differs')
    for pin in row['sourceDependencies']:require(sha256(ROOT/pin['path'])==pin['sha256'],'AES real header changed')
    wanted={(SOURCE/'layout.json').relative_to(ROOT).as_posix():sha256(SOURCE/'layout.json'),asset['semanticSource']:asset['semanticSourceSha256']};observed={pin['path']:pin['sha256']for pin in row['dataSourceDependencies']};require(len(row['dataSourceDependencies'])==2 and wanted==observed,'AES mathematical generation dependencies changed or were treated as C includes')
    for path,digest in observed.items():require(sha256(ROOT/path)==digest,'AES actual semantic/layout generation input changed')
    document=read_json(ROOT/row['semanticSource']);code,payload=render(document,row['nativeSymbol']);require((ROOT/row['source']).read_text(encoding='utf-8')==code,'AES ordinary readable mathematical uint32 initializer changed')
    require(row['bytes']==row['size']==row['compiledBytes']==row['initializedBytes']==len(payload)==admitted['bytes']==1024,'AES whole256word extent changed')
    address=int(row['address'],0);require(row['nativeAlias']==f'data_ov006_{address:08x}'and row['nativeSymbol']==asset['nativeSymbol']and row['section']==row['targetSection']=='.rodata','AES genuine overlay-local alias or original rodata placement differs')
    require(row['existingConfiguredInteriorElementViews']==document['existingConfiguredInteriorElementViews'],'AES three ambiguous zero-credit interior views were changed/dropped')
    validate_primary(document,payload);validate_native(row,payload,image);aliases=validate_views(row,document,payload,image);compiler_inputs(row);qualify_typed_object(row)
    require(sha256(ROOT/row['realLink']['lcf'])==row['realLink']['lcfSha256'],'AES original complete genuine placement input changed')
    return payload,aliases


def qualify(before,after,expected,functions,directory):
    require(sha256(COMPILER)==COMPILER_HASH and sha256(LINKER)==LINKER_HASH,'AES pinned genuine compiler/linker changed');layout,admitted,assets=membership(before,after,expected,functions);image=(ROOT/IMAGE).read_bytes();require(sha256(ROOT/IMAGE)==IMAGE_SHA,'AES full original overlay6 image changed');witnesses=validate_pointers(layout,image);proofs=[];aliases={}
    for key in sorted(admitted):
        row=after[key];payload,views=validate(row,assets[key],admitted[key],layout,image);aliases.update(views);actual=fresh_link(row,payload,Path(directory)/f'ov006-{key[4]:08x}');proofs.append(dict(program='',processor='arm9',module='ov006',address=hex(key[4]),initializedBytes=1024,realLink=actual))
    require(len(aliases)==13 and all(after[key]['dataAliases']==aliases for key in admitted),'AES exact ten whole labels plus three existing interior element aliases changed')
    result=dict(passed=True,newInitializedDataObjects=10,newInitializedDataBytes=10240,newTypedConstantDataBytes=10240,newEncodedAssetBytes=0,newDataAlignmentBytes=0,newSourceFunctions=0,newExecutableBytes=0,newBssBytes=0,newGapBytes=0,newInteriorViewBytes=0,newInteriorViewObjects=0,existingAmbiguousViewsPreserved=3,originalPluralOverlayReferencesUnchanged=True,earlierDataPreserved=len(before),configuredThumbPointerWitnessObjects=len(witnesses),proofs=proofs,sourceCreditPendingSharedAcceptance=True);write_json(Path(directory)/'qualification.json',result);return result
