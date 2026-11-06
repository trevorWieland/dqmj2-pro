from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_gp_character_data_paths import EVIDENCE,assert_owned

PRODUCER='wave20261106_gp_character_data_full_replay.py'


def pin(path,role=None):
    entry=dict(path=path,sha256=sha256(ROOT/path))
    if role:entry['role']=role
    return entry


def main():
    assert_owned();base=EVIDENCE.relative_to(ROOT).as_posix();old=read_json(EVIDENCE/'source-files.json');contract=read_json(EVIDENCE/'registration-transport.json');files={p['path']:p for p in old['files']};private={p['path']:p for p in old['privateComparisonOrToolInputs']};closure=code_closure([PRODUCER]);generators={p['path']:p['sha256']for p in old['generatorSources']}
    for path in closure:files[path]=pin(path);generators[path]=sha256(ROOT/path)
    for path in [Path(__file__).name,base+'/source-files.json',contract['originalReady']['path'],base+'/registration-transport.json']:files[path]=pin(path)
    original=contract['originalReport'];private[original['path']]=dict(original,role='immutable-original-source-flags-native-contract-provenance-old-object-paths-not-used')
    if any(path.startswith(('work/','extract/','tools/'))for path in files)or set(files)&set(private):raise ValueError('Full replay source/private classification differs')
    if any(path.startswith('work/')for path in private):raise ValueError('Fresh full replay depends on old work objects')
    manifest=dict(schemaVersion=1,freshCompleteSourceReplay=True,sourceCredit=0,files=[files[p]for p in sorted(files)],privateComparisonOrToolInputs=[private[p]for p in sorted(private)],generatorSources=[dict(path=p,sha256=h)for p,h in sorted(generators.items())],sourceGenerationUsesOnlyAdmittedCharacterJson=True,noOldWorkObjectsRequired=True,classification='Copied authored C/header/semantics/public-text/code/contract metadata; actual pinned native comparison and compiler/runtime inputs private. The frozen canonical report is provenance metadata only. Old object/link files are neither copied nor read by this producer.')
    manifest_name=base+'/full-replay-source-files.json';write_json(ROOT/manifest_name,manifest)
    descriptor=dict(schemaVersion=1,sourceCredit=0,freshCompleteSourceReplay=True,sourceManifest=pin(manifest_name),originalReport=original,originalReady=contract['originalReady'],registrationContract=pin(base+'/registration-transport.json'),output='evidence/matches/gp-character-data-full-replay-registration-20261106.json',producerArgv=['python',PRODUCER,base+'/full-replay-descriptor.json'],allOldFrozenPathsPreserved=True)
    descriptor_name=base+'/full-replay-descriptor.json';write_json(ROOT/descriptor_name,descriptor);print(dict(descriptor=descriptor_name,descriptorSha256=sha256(ROOT/descriptor_name),sourceFiles=len(files),privateInputs=len(private),oldWorkObjectsRequired=False),flush=True)


if __name__=='__main__':main()
