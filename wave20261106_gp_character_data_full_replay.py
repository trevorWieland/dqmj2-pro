import argparse
import uuid
from pathlib import Path
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_gp_character_data_paths import WORK,EVIDENCE,SOURCE,assert_owned
from wave20261106_gp_character_data_codec import render
from wave20261106_gp_character_data_validate import validate_layout
from wave20261106_gp_character_data_registration import project
import wave20261106_gp_character_data_packet as packet
import wave20261106_gp_character_data_controls as controls


FIELDS=['program','processor','module','kind','mode','formatKind','address','bytes','nativeSymbol','name','source','sourceSha256','semanticSource','semanticSourceSha256','sourceLanguage','sourceDependencies','dataSourceDependencies','size','compiledBytes','initializedBytes','targetSha256','outputSha256','binary','inputModuleSha256','moduleBase','compiler','compilerSha256','compilerFlags','section','relocations','executableSectionBytes','allocatedZeroFillBytes','ordinaryFunctionCredit','encodedAssetBytes','measuredZeroAlignmentBytes']


def materialize(layout,folder):
    original=Path.open;blocked=[];declarations=[];generated=[];folder.mkdir(parents=True,exist_ok=True)
    def source_only(path,*args,**kwargs):
        if any(path.resolve().is_relative_to(ROOT/n)for n in ['inputs','extract','deps/reference']):raise PermissionError('Native/public inputs blocked during actual fresh GP character C/header generation')
        return original(path,*args,**kwargs)
    with patch.object(Path,'open',source_only):
        for row in layout['assets']:
            code,payload=render(read_json(ROOT/row['semanticSource']),row['nativeSymbol']);target=folder/f"{int(row['address'],0):08x}.c";target.write_text(code,encoding='utf-8')
            if target.read_bytes()!=(ROOT/row['source']).read_bytes()or sha256(target)!=row['sourceSha256']:raise ValueError('Fresh semantic-generated C differs from immutable promoted compiler source')
            generated.append(dict(path=target.relative_to(ROOT).as_posix(),sha256=sha256(target),promotedCompilerSource=row['source'],sameBytes=True));declarations.append(f"extern const char {row['nativeSymbol']}[{len(payload)}];")
        text='\n'.join(['#ifndef GP_CHARACTER_OBJECTS_H','#define GP_CHARACTER_OBJECTS_H','typedef char GPCharacterWidthMustBeOne[(sizeof(char)==1)?1:-1];',*declarations,'#endif','']);header=folder/'characters.h';header.write_text(text,encoding='utf-8')
        if header.read_bytes()!=(SOURCE/'characters.h').read_bytes()or sha256(header)!=layout['characterHeader']['sha256']:raise ValueError('Fresh actual typed character declarations differ from immutable compiler header')
        first=read_json(ROOT/layout['assets'][0]['semanticSource'])
        for path in [ROOT/'inputs/game.nds',ROOT/'extract/arm9/arm9.bin',ROOT/first['primaryReference']['path']]:
            try:path.read_bytes()
            except PermissionError:blocked.append(path.relative_to(ROOT).as_posix())
            else:raise ValueError('Fresh semantic generator read native/public source')
    return dict(generatedCObjects=generated,generatedHeader=dict(path=header.relative_to(ROOT).as_posix(),sha256=sha256(header)),allRegeneratedBytesEqualActualPromotedCompilerInputs=True,generationReadDenials=blocked,compilerUsesImmutablePromotedSourcesAfterFreshGenerationEqualityCheck=True)


def main():
    assert_owned();parser=argparse.ArgumentParser();parser.add_argument('descriptor');args=parser.parse_args();descriptor_path=ROOT/args.descriptor;descriptor=read_json(descriptor_path)
    if descriptor['sourceCredit']!=0 or not descriptor['freshCompleteSourceReplay']:raise ValueError('Full GP replay descriptor contract differs')
    for key in ['sourceManifest','originalReport','originalReady','registrationContract']:
        pin=descriptor[key]
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Full replay immutable contract changed: '+pin['path'])
    manifest=read_json(ROOT/descriptor['sourceManifest']['path'])
    for pin in manifest['files']+manifest['privateComparisonOrToolInputs']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Full replay source/runtime closure changed: '+pin['path'])
    baseline=read_json(ROOT/descriptor['originalReport']['path']);contract=read_json(ROOT/descriptor['registrationContract']['path']);layout=read_json(SOURCE/'layout.json');validate_layout(layout,read_json(EVIDENCE/'data-claim.json'));run=WORK/'rf'/uuid.uuid4().hex[:8];diagnostics=run/'diagnostics';diagnostics.mkdir(parents=True,exist_ok=True);fresh_worker=run/'worker.json'
    original_open=Path.open;denied=[];old_packet=(packet.WORK,packet.REPORT);old_controls=(controls.WORK,controls.EVIDENCE)
    def no_old_objects(path,*arguments,**kwargs):
        if any(path.resolve().is_relative_to((WORK/name).resolve())for name in ['proof','wrong-c','registration-review','addition-review']):raise PermissionError('Old GP work objects/proofs are forbidden during full source replay')
        return original_open(path,*arguments,**kwargs)
    try:
        packet.WORK=run;packet.REPORT=fresh_worker.relative_to(ROOT).as_posix();controls.WORK=run;controls.EVIDENCE=diagnostics
        with patch.object(Path,'open',no_old_objects):
            for path in [ROOT/baseline['dataMatches'][0]['object'],ROOT/baseline['dataMatches'][0]['realLink']['linkedElf']]:
                try:path.read_bytes()
                except PermissionError:denied.append(path.relative_to(ROOT).as_posix())
                else:raise ValueError('Old sealed work object was readable during full GP source replay')
            generation=materialize(layout,run/'generated');fresh=packet.produce(manifest)
            old={row['address']:row for row in baseline['dataMatches']}
            if len(fresh['dataMatches'])!=259:raise ValueError('Full source replay lost character objects')
            for row in fresh['dataMatches']:
                if any(row.get(field)!=old[row['address']].get(field)for field in FIELDS):raise ValueError('Fresh C/compiler/native identity differs from immutable complete original contract')
                if not(ROOT/row['object']).resolve().is_relative_to(run.resolve()):raise ValueError('Full source replay reused an old work object')
            report,evidence,generation_inputs=project(fresh,contract)
    finally:packet.WORK,packet.REPORT=old_packet;controls.WORK,controls.EVIDENCE=old_controls
    pins={x['path']:x['sha256']for x in manifest['generatorSources']};roles={path:'generator-code'for path in pins}
    for path,digest in generation_inputs.items():pins[path]=digest;roles[path]='character-generation-input'
    source_manifest=descriptor['sourceManifest'];pins[source_manifest['path']]=source_manifest['sha256'];roles[source_manifest['path']]='immutable-full-source-replay-closure'
    report['generatorSources']=[dict(path=path,sha256=digest)for path,digest in sorted(pins.items())];report['generatorSourceRoles']=roles;report['generationDependencies']=[dict(path=path,sha256=digest)for path,digest in sorted(generation_inputs.items())]
    dependencies=[descriptor['sourceManifest'],descriptor['originalReport'],descriptor['originalReady'],descriptor['registrationContract'],dict(path=args.descriptor,sha256=sha256(descriptor_path)),*report['generationDependencies']];report['replayDependencies']=dependencies;report['privateComparisonOrToolInputs']=manifest['privateComparisonOrToolInputs']
    report['gpCharacterFullSourceReplay']=dict(ordinaryFunctionCredit=0,objectsFreshlyCompiledAndGenuinelyLinked=259,initializedBytes=3696,originalSourceCompilerFlagsRelocationsAndNativeContractsPreserved=True,actualFreshGeneration=generation,oldWorkReadRejections=denied,noOldObjectOrLinkRequired=True,freshWorkerReport=fresh_worker.relative_to(ROOT).as_posix(),freshWorkerReportSha256=sha256(fresh_worker),originalFrozenReportProvenance=descriptor['originalReport'],originalFrozenReadyProvenance=descriptor['originalReady'],sourceOnlyGenerationAndComparisonReadGuardsRetained=True,originalWrongCAndNativeSourceNamespaceControlsReexecuted=True,configuredAliases=evidence,allProcessLocalOutputOverridesRestored=True,noWholeModuleOrRomOrGameExecutionClaim=True)
    output=ROOT/descriptor['output']
    if not output.resolve().is_relative_to(ROOT/'evidence/matches')or output==ROOT/descriptor['originalReport']['path']:raise ValueError('Full replay report would overwrite an original sealed report')
    write_json(output,report);print(dict(passed=True,objects=259,bytes=3696,freshGeneratedCompiledLinked=True,wrongC=report['controls']['wholeWrongCControls'],oldObjectReadDenials=len(denied),report=descriptor['output']),flush=True)


if __name__=='__main__':main()
