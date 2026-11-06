import copy
import re
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from replay_sdk_data_registration_v2_20261106 import qualify
from closed_c_compiler_inputs_20261105 import compiler_inputs
from wave20261106_gp_character_data_paths import SOURCE,EVIDENCE,assert_owned
from wave20261106_gp_character_data_codec import encode,render
from wave20261106_gp_character_data_validate import validate_reference,validate_native
from wave20261106_gp_character_data_build import inspect_object,LINKER,LINKER_HASH


def project(report,descriptor):
    if report['functionMatched']!=0 or report['functionMatches']!=[]or len(report['dataMatches'])!=259 or report['dataMatchedBytes']!=3696:raise ValueError('Exact data-only registration membership differs')
    if sha256(ROOT/'config/arm9/symbols.txt')!=descriptor['originalConfiguredSymbolsSha256']or sha256(LINKER)!=LINKER_HASH:raise ValueError('Original configured data labels or genuine linker changed')
    symbols=(ROOT/'config/arm9/symbols.txt').read_text().splitlines();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();result=copy.deepcopy(report);evidence=[];aliases={};generation={}
    for row in result['dataMatches']:
        if (row['program'],row['processor'],row['module'],row['kind'],row['mode'])!=('','arm9','main','data','data')or any(k in row for k in ['exactBytes','nativeAlias','targetSection']):raise ValueError('Registration crossed exact original data namespace or already projected metadata')
        proof=qualify(row)
        if sha256(ROOT/row['realLink']['lcf'])!=row['realLink']['lcfSha256']:raise ValueError('Original genuine-link placement contract changed')
        document=read_json(ROOT/row['semanticSource']);payload,_=encode(document);code,_=render(document,row['nativeSymbol'])
        if (ROOT/row['source']).read_text(encoding='utf-8')!=code:raise ValueError('Actual C literal source does not retain complete semantic character meaning')
        validate_reference(document);validate_native(row,payload,image);inspect_object(ROOT/row['object'],row['nativeSymbol'],payload);compiler_inputs(row)
        address=int(row['address'],0);matches=[re.fullmatch(r'(\S+) kind:data\(any\) addr:0x%08x'%address,x)for x in symbols];matches=[x for x in matches if x]
        if len(matches)!=1:raise ValueError('Character placement lacks one genuine configured native data label')
        alias=matches[0][1]
        if alias!=f'data_{address:08x}'or not 0x20dcb40<=address<address+row['bytes']<=0x20e3300:raise ValueError('Character alias or original initialized .data extent differs')
        aliases[alias]=row['address'];row.update(exactBytes=True,nativeAlias=alias,targetSection='.data');evidence.append(dict(proof,nativeAlias=alias,configuredRecord=matches[0].group(),sourceSectionUnchanged=row['section'],nativePlacementSection='.data',originalObjectUnmodified=True,sectionRetargetingMetadataOnly=True))
        for pin in row['dataSourceDependencies']:
            if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Explicit character-generation input changed')
            generation[pin['path']]=pin['sha256']
    before=[{k:v for k,v in r.items()if k not in ['exactBytes','nativeAlias','targetSection']}for r in result['dataMatches']]
    if before!=report['dataMatches']:raise ValueError('Registration transport changed original source/object/flags/relocations/native/link proofs')
    result.update(program='',processor='arm9',module='main',dataAliases=aliases,generationDependencies=[dict(path=p,sha256=h)for p,h in sorted(generation.items())])
    return result,evidence,generation


def main():
    assert_owned()
    if len(sys.argv)!=2:raise ValueError('Exact additive GP registration descriptor required')
    name=sys.argv[1];descriptor=read_json(ROOT/name)
    if not descriptor['registrationMetadataOnly']or descriptor['sourceCredit']!=0:raise ValueError('Registration transport is not metadata-only')
    for key in ['originalReport','originalReady','originalDescriptor','sourceManifest']:
        pin=descriptor[key]
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Sealed GP input changed: '+pin['path'])
    original=read_json(ROOT/descriptor['originalReport']['path']);report,evidence,generation=project(original,descriptor);pins={x['path']:x['sha256']for x in report['generatorSources']};roles={x['path']:'generator-code'for x in report['generatorSources']}
    for path in code_closure([Path(__file__).name]):
        if path in pins and pins[path]!=sha256(ROOT/path):raise ValueError('Prior frozen generator implementation changed')
        pins[path]=sha256(ROOT/path);roles[path]='generator-code'
    for path,digest in generation.items():pins[path]=digest;roles[path]='character-generation-input'
    manifest=descriptor['sourceManifest'];pins[manifest['path']]=manifest['sha256'];roles[manifest['path']]='immutable-generation-and-input-closure-manifest'
    report['generatorSources']=[dict(path=p,sha256=h)for p,h in sorted(pins.items())];report['generatorSourceRoles']=roles
    dependencies={p['path']:p['sha256']for p in report.get('replayDependencies',[])}
    for key in ['originalReport','originalReady','originalDescriptor','sourceManifest']:
        pin=descriptor[key];dependencies[pin['path']]=pin['sha256']
    dependencies[name]=sha256(ROOT/name);dependencies.update(generation);report['replayDependencies']=[dict(path=p,sha256=h)for p,h in sorted(dependencies.items())];report['privateComparisonOrToolInputs']=read_json(ROOT/manifest['path'])['privateComparisonOrToolInputs']
    report['gpCharacterRegistrationTransport']=dict(sourceCredit=0,originalReport=descriptor['originalReport'],originalReady=descriptor['originalReady'],sourceObjectFlagsRelocationsAndNativeProofsUnchanged=True,exactBytesDerivedOnlyAfterWholeTypedCObjectNativeAndGenuineLinkQualification=True,configuredAliasesOnly=True,noStorageDeclarationsInvented=True,actualCHeaderDependenciesUnchanged=True,generationInputsSeparatelyNamedAndRegistryHashLocked=True,noOriginalProducerOrCanonicalReportRerun=True,rebuildFromCQualifiedByOriginalIndependent259ObjectCopiedReplay=True,evidence=evidence,limit='Metadata registration verifies the sealed complete C/objects/links; fresh source compilation remains the original qualified producer and copied-root proof, not a new claim of full source-only ROM or module execution.')
    output=ROOT/descriptor['output']
    if not output.resolve().is_relative_to(ROOT/'evidence/matches'):raise ValueError('Additive GP registration output escaped report directory')
    write_json(output,report);print(dict(objects=259,initializedBytes=3696,metadataOnly=True,configuredAliases=259,output=descriptor['output']),flush=True)


if __name__=='__main__':main()
