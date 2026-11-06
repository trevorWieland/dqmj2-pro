from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_auth_character_data_paths import SOURCE,EVIDENCE,assert_owned

PRODUCER='wave20261106_auth_character_data_packet.py'


def pin(path,role=None):
    value=dict(path=path,sha256=sha256(ROOT/path))
    if role:value['role']=role
    return value


def main():
    assert_owned();layout=read_json(SOURCE/'layout.json');files={};metadata=[]
    for path in code_closure([PRODUCER]):files[path]=pin(path)
    files[Path(__file__).name]=pin(Path(__file__).name)
    for path in [SOURCE/'layout.json',SOURCE/'characters.h',EVIDENCE/'data-claim.json',EVIDENCE/'coordinator-review.json',ROOT/'evidence/lanes/parallel-wave20261106/whole-character-auth-read-only/proposal.json']:
        relative=path.relative_to(ROOT).as_posix();files[relative]=pin(relative)
        if path.parent==EVIDENCE or path.name=='proposal.json':metadata.append(pin(relative))
    for row in layout['assets']:
        for path in [row['source'],row['semanticSource']]:files[path]=pin(path)
        ref=read_json(ROOT/row['semanticSource'])['primaryReference']
        for path in [ref['path'],ref['snapshot']['path']]:files[path]=pin(path)
    private=read_json(ROOT/'evidence/lanes/parallel-wave20261106/gamespy-gp-character-data/source-files.json')['privateComparisonOrToolInputs']
    if any(p['path'].startswith('work/')for p in private)or any(path.startswith(('work/','extract/','tools/'))for path in files)or set(files)&{p['path']for p in private}:raise ValueError('Auth source/private input classification is not exact')
    generator=code_closure([PRODUCER]);manifest=dict(schemaVersion=1,sourceCredit=0,files=[files[p]for p in sorted(files)],privateComparisonOrToolInputs=private,generatorSources=[pin(p)for p in generator],metadataDependencies=metadata,noWorkObjectsRequired=True,sourceOnlySemanticGeneration=True,classification='Copied readable authored C/real header/semantic JSON/code/primary text/provenance; actual native comparison and pinned compiler/runtime remain private. No GP source objects, old work, ROM input, arbitrary byte arrays or opaque object inputs.')
    base=EVIDENCE.relative_to(ROOT).as_posix();manifest_name=base+'/source-files.json';write_json(ROOT/manifest_name,manifest);descriptor=dict(schemaVersion=1,sourceCredit=0,freshCompleteSourceReplay=True,sourceManifest=pin(manifest_name),output='evidence/matches/auth-character-data-20261106.json');name=base+'/canonical-packet.json';write_json(ROOT/name,descriptor);print(dict(descriptor=name,descriptorSha256=sha256(ROOT/name),sourceFiles=len(files),privateRuntimeOrComparisonInputs=len(private)),flush=True)


if __name__=='__main__':main()
