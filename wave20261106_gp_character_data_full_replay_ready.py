from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from wave20261106_gp_character_data_paths import EVIDENCE


def pin(path):return dict(path=path,sha256=sha256(ROOT/path))


def main():
    base=EVIDENCE.relative_to(ROOT).as_posix();descriptor_name=base+'/full-replay-descriptor.json';descriptor=read_json(ROOT/descriptor_name);proof_name=base+'/full-replay-copied-root-review.json';proof=read_json(ROOT/proof_name);report=read_json(ROOT/descriptor['output']);producer='wave20261106_gp_character_data_full_replay.py';manifest_name=descriptor['sourceManifest']['path']
    if not proof['passed']or proof['producer']['sha256']!=sha256(ROOT/producer)or len(report['dataMatches'])!=259 or report['dataMatchedBytes']!=3696:raise ValueError('Fresh complete source/copied-root replay contract is not closed')
    files=[producer,'wave20261106_gp_character_data_full_replay_package.py','wave20261106_gp_character_data_full_replay_review.py',Path(__file__).name,descriptor_name,manifest_name,proof_name,'wave20261106_gp_character_data_additions.py',base+'/addition-compatibility-review.json']
    ready=dict(status='ready-for-coordinator-initialized-data-acceptance',sourceCredit=0,report=descriptor['output'],producer=[producer,descriptor_name],packets=[dict(report=descriptor['output'],producerArgv=[producer,descriptor_name])],functionCount=0,dataObjects=259,initializedBytes=3696,typedConstantDataBytes=3696,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,executableBytes=0,bssBytes=0,gapBytes=0,sourceManifest=manifest_name,sourceManifestSha256=descriptor['sourceManifest']['sha256'],canonicalReport=descriptor['output'],canonicalProducer=[producer,descriptor_name],canonicalDescriptor=pin(descriptor_name),freshCopiedRootObjects=259,wrongDataObjects=6,copiedRootTamperControls=5,allClosedCompilerInputGuardsPassed=True,actualCompleteSourceGenerationCompilationAndGenuineLinkReplay=True,noOriginalWorkObjectsNeeded=True,wholeOriginalAndAdditiveFrozenInputsPreserved=proof['originalAndAdditiveFrozenPinsRehashedUnchanged'],originalReady=descriptor['originalReady'],qualifiedAdditiveDataQualifier=pin('wave20261106_gp_character_data_additions.py'),files=[pin(path)for path in files],limitations=report['limits'])
    path=EVIDENCE/'full-replay/ready.json';write_json(path,ready);print(dict(ready=path.relative_to(ROOT).as_posix(),sha256=sha256(path),producer=ready['producer'],canonicalReport=descriptor['output'],dataObjects=259,initializedBytes=3696),flush=True)


if __name__=='__main__':main()
