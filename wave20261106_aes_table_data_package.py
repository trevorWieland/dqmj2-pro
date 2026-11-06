from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_aes_table_data_paths import SOURCE,EVIDENCE,REFERENCE,assert_owned

PRODUCER='wave20261106_aes_table_data_packet.py'


def pin(path,role=None):
    value=dict(path=path,sha256=sha256(ROOT/path))
    if role:value['role']=role
    return value


def main():
    assert_owned();layout=read_json(SOURCE/'layout.json');files={path:pin(path)for path in code_closure([PRODUCER])};files[Path(__file__).name]=pin(Path(__file__).name);metadata=[]
    for path in [SOURCE/'layout.json',SOURCE/'aes_tables.h',EVIDENCE/'data-claim.json',EVIDENCE/'coordinator-review.json']:
        relative=path.relative_to(ROOT).as_posix();files[relative]=pin(relative)
        if path.parent==EVIDENCE:metadata.append(pin(relative))
    for path in ['admit_aes_table_storage_v2_20261106.py','initialized_storage_protection_v3_20261106.py','qualify_storage_protection_v3_20261106.py','evidence/verification/storage-protection-v3-all-cohort-scope-20261106.json','evidence/verification/storage-protection-v3-all-cohort-fixture-qualification-20261106.json']:
        files[path]=pin(path);metadata.append(pin(path))
    for row in layout['assets']:
        for path in [row['source'],row['semanticSource']]:files[path]=pin(path)
    for path in REFERENCE.iterdir():
        if path.is_file():relative=path.relative_to(ROOT).as_posix();files[relative]=pin(relative)
    base_runtime=read_json(ROOT/'evidence/lanes/parallel-wave20261106/gamespy-gp-character-data/source-files.json')['privateComparisonOrToolInputs'];private={p['path']:p for p in base_runtime}
    for path,role in [('extract/arm9_overlays/ov006.bin','complete-original-overlay6-native-comparison'),('config/arm9/overlays/ov006/symbols.txt','exact-overlay6-normal-and-ambiguous-native-data-symbols'),('config/arm9/overlays/ov006/relocs.txt','original-same-overlay-Thumb-pointer-records'),('config/arm9/overlays/ov006/delinks.txt','original-overlay6-rodata-placement'),('config/arm9/overlays/ov000/symbols.txt','preserved-other-overlay-namespace-evidence-only')]:private[path]=pin(path,role)
    if any(path.startswith(('work/','extract/','tools/'))for path in files)or any(path.startswith('work/')for path in private)or set(files)&set(private):raise ValueError('AES authored/copy/private native/compiler/runtime classification differs')
    manifest=dict(schemaVersion=1,sourceCredit=0,files=[files[path]for path in sorted(files)],privateComparisonOrToolInputs=[private[path]for path in sorted(private)],generatorSources=[pin(path)for path in code_closure([PRODUCER])],metadataDependencies=metadata,sourceGenerationUsesMathematicalDescriptorsOnly=True,noOldWorkObjectsRequired=True,classification='Copied readable mathematical C/realwidthheader/semanticJSON/canonicalprimarytext/code/contract metadata. Actual original overlay/main comparisons, exactnormal/ambiguous configuredsymbol+reloc metadata and pinnedcompiler/runtime remain private. No old GP/Auth/AES work objects or research files are inputs.')
    base=EVIDENCE.relative_to(ROOT).as_posix();manifest_name=base+'/source-files.json';write_json(ROOT/manifest_name,manifest);descriptor=dict(schemaVersion=1,sourceCredit=0,freshCompleteSourceReplay=True,sourceManifest=pin(manifest_name),output='evidence/matches/aes-table-data-20261106.json');name=base+'/canonical-packet.json';write_json(ROOT/name,descriptor);print(dict(descriptor=name,descriptorSha256=sha256(ROOT/name),sourceFiles=len(files),actualPrivateInputs=len(private)),flush=True)


if __name__=='__main__':main()
