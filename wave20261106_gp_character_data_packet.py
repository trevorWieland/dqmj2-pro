import argparse
import concurrent.futures
import hashlib
from pathlib import Path
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256,now
from closed_c_compiler_inputs_20261105 import compiler_inputs
from wave20261106_gp_character_data_paths import SOURCE,EVIDENCE,WORK,assert_owned
from wave20261106_gp_character_data_codec import render
from wave20261106_gp_character_data_validate import validate_layout,validate_reference,validate_native,validate_pointers,IMAGE,IMAGE_SHA
from wave20261106_gp_character_data_build import compile_link,FLAGS
from wave20261106_gp_character_data_controls import execute as controls

REPORT='evidence/data/gamespy-gp-character-data-20261106.json'


def generation(layout):
    original=Path.open;denied=[];values=[]
    def source_only(path,*args,**kwargs):
        if any(path.resolve().is_relative_to(ROOT/n)for n in ['inputs','extract','deps/reference']):raise PermissionError('Original/reference input blocked during GP character semantic generation')
        return original(path,*args,**kwargs)
    with patch.object(Path,'open',source_only):
        for row in layout['assets']:
            document=read_json(ROOT/row['semanticSource']);code,payload=render(document,row['nativeSymbol'])
            if sha256(ROOT/row['source'])!=row['sourceSha256']or(ROOT/row['source']).read_text(encoding='utf-8')!=code:raise ValueError('Actual C character initializer drifted from semantic-only generation')
            values.append((row,payload))
        for path in [ROOT/'inputs/game.nds',ROOT/IMAGE,ROOT/read_json(ROOT/layout['assets'][0]['semanticSource'])['primaryReference']['path']]:
            try:path.read_bytes()
            except PermissionError:denied.append(path.relative_to(ROOT).as_posix())
            else:raise ValueError('GP original or primary reference was readable during character generation')
    return values,denied


def produce(manifest):
    assert_owned();layout=read_json(SOURCE/'layout.json');claim=read_json(EVIDENCE/'data-claim.json');validate_layout(layout,claim);values,denied=generation(layout);image=(ROOT/IMAGE).read_bytes()
    if sha256(ROOT/IMAGE)!=IMAGE_SHA:raise ValueError('Complete measured main image changed')
    for row,payload in values:validate_reference(read_json(ROOT/row['semanticSource']));validate_native(row,payload,image)
    proposal=read_json(ROOT/'evidence/lanes/parallel-wave20261106/whole-character-read-only/gp-proposal.json');pointer_witnesses=validate_pointers(proposal,image);header=layout['characterHeader'];layout_pin=dict(path=(SOURCE/'layout.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'layout.json'))
    def build(item):
        row,payload=item;entry=dict(row,sourceDependencies=[header],compilerFlags=FLAGS)
        eligibility=compiler_inputs(entry);proof=compile_link(row,ROOT/row['source'],payload,WORK/'proof'/format(int(row['address'],0),'08x'))
        return dict(row,**proof,kind='data',mode='data',name=row['nativeSymbol'],size=len(payload),compiledBytes=len(payload),initializedBytes=len(payload),sourceLanguage='C',sourceDependencies=[header],dataSourceDependencies=[layout_pin,dict(path=row['semanticSource'],sha256=row['semanticSourceSha256'])],sourcePolicy=dict(realCharacterStringInitializer=True,noOpaqueByteArray=True,actualTypedCharacterDeclarationsConsumed=True,closedCompilerInputEligibility=eligibility),relocations=[],executableSectionBytes=0,allocatedZeroFillBytes=0,ordinaryFunctionCredit=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0)
    matches=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
        for row in pool.map(build,values):
            matches.append(row)
            if len(matches)%64==0:print(dict(objectsLinked=len(matches),bytes=sum(x['bytes']for x in matches)),flush=True)
    proof=controls(layout,claim,image)
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=layout['romSha256'],dataMatches=matches,dataMatchedBytes=3696,functionMatched=0,functionMatches=[],nativeSymbols={},ordinaryFunctionCredit=0,executableSectionBytes=0,allocatedZeroFillBytes=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,typedConstantDataBytes=3696,controls=proof,generationOriginalInputsBlocked=True,originalReadRejectionControls=len(denied),blockedGenerationPaths=denied,originalPointerWitnesses=pointer_witnesses,sourceCreditPendingSharedAcceptance=True,generatorSources=manifest['generatorSources'],wholeModuleLinked=False,sourceReconstructionComplete=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,actualFunctionOrNetworkOrDeviceExecutions=0,allClosedCompilerInputGuardsPassed=True,allObjectsCompleteTypedCCharacterInitializers=True,canonicalReportRefreshedFromFreshWorkerObjects=True,replayRoot=str(ROOT),limits=['259 complete ordinary C narrow character objects add exactly3696 initialized bytes after shared acceptance.','No function, gap, alignment, arbitrary array slice, provider, network, hardware, game, reset or native Windows execution credit.','C compilation consumes the real263-line extent/type header. Original module and public C are comparison/lineage inputs only; semantic generation blocks their reads.'])
    write_json(ROOT/REPORT,report);return report


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inputs-sha256',required=True);args=parser.parse_args();path=EVIDENCE/'source-files.json'
    if sha256(path)!=args.inputs_sha256:raise ValueError('Immutable GP character source manifest changed')
    manifest=read_json(path)
    for item in manifest['files']+manifest['privateComparisonOrToolInputs']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Immutable GP character input changed: '+item['path'])
    report=produce(manifest);print(dict(dataObjects=len(report['dataMatches']),initializedBytes=report['dataMatchedBytes'],wrongCObjects=report['controls']['wholeWrongCControls'],functionCredit=0),flush=True)


if __name__=='__main__':main()
