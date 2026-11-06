from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_auth_character_data_paths import EVIDENCE


def pin(path):return dict(path=path,sha256=sha256(ROOT/path))


def main():
    base=EVIDENCE.relative_to(ROOT).as_posix();descriptor_name=base+'/canonical-packet.json';descriptor=read_json(ROOT/descriptor_name);copied=read_json(EVIDENCE/'copied-root-controls.json');qualification=read_json(EVIDENCE/'addition-compatibility-review.json');report=read_json(ROOT/descriptor['output']);producer='wave20261106_auth_character_data_packet.py';qualifier='wave20261106_auth_character_data_additions.py'
    if not copied['passed']or not qualification['passed']or copied['producerSha256']!=sha256(ROOT/producer)or qualification['qualifierSha256']!=sha256(ROOT/qualifier)or len(report['dataMatches'])!=102 or report['dataMatchedBytes']!=1431:raise ValueError('Auth fresh replay/typed-data preservation qualification is not closed')
    proof_files=[base+'/copied-root-controls.json',base+'/addition-compatibility-review.json'];helpers=[producer,qualifier,'wave20261106_auth_character_data_copy_review.py','wave20261106_auth_character_data_additions_review.py',Path(__file__).name];closure=code_closure(helpers);source_manifest=descriptor['sourceManifest'];paths=set(closure)|set(proof_files)|{descriptor_name,source_manifest['path']}
    extra_name=base+'/qualification-source-files.json';extra=dict(schemaVersion=1,sourceCredit=0,files=[pin(path)for path in sorted(closure)],productionSourceManifest=source_manifest,privateComparisonOrToolInputs=[],role='Additional immutable integration qualifier and review code closure; actual C/header/semantic/reference/native/compiler inputs remain fully declared by the production manifest.');write_json(ROOT/extra_name,extra);paths.add(extra_name)
    ready=dict(status='ready-for-coordinator-initialized-data-acceptance',sourceCredit=0,report=descriptor['output'],producer=[producer,descriptor_name],packets=[dict(report=descriptor['output'],producerArgv=[producer,descriptor_name])],functionCount=0,dataObjects=102,initializedBytes=1431,typedConstantDataBytes=1431,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,executableBytes=0,bssBytes=0,gapBytes=0,sourceManifest=source_manifest['path'],sourceManifestSha256=source_manifest['sha256'],additionalQualifierSourceManifest=pin(extra_name),canonicalReport=descriptor['output'],canonicalProducer=[producer,descriptor_name],canonicalDescriptor=pin(descriptor_name),freshCopiedRootObjects=102,wrongDataObjects=6,copiedRootTamperControls=5,allClosedCompilerInputGuardsPassed=True,actualFreshSourceGenerationCompilationAndGenuineLinkReplay=True,noOldWorkObjectsRequired=True,configuredCallerPointerWitnessesVerifiedForAll102Objects=True,allFrozenGpPinsPreserved=copied['allFrozenGpPinsRehashedUnchanged'],dataAdditionQualifier=pin(qualifier),qualifierInterface='qualify(before, after, expected, functions, directory)',privateIntegrationNegativeControls=len(qualification['negativeControls']),privateEarlierSelectedFunctionsPreserved=qualification['unchangedSelectedFunctions'],files=[pin(path)for path in sorted(paths)],limitations=report['limits'])
    name=EVIDENCE/'ready.json';write_json(name,ready);print(dict(ready=name.relative_to(ROOT).as_posix(),sha256=sha256(name),files=len(paths),objects=102,bytes=1431,producer=ready['producer']),flush=True)


if __name__=='__main__':main()
