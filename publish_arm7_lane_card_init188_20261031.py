import json
import subprocess
from pathlib import Path
from project import ROOT,sha256,write_json


def main():
    if (ROOT/'docs/2026-10-31-arm7-card-init188.md').stat().st_size<100:
        raise ValueError('Publication requires completed documentation')
    canonical=ROOT/'evidence/matches/arm7-lane-card-init188-20261031.json'
    controls=ROOT/'evidence/verification/arm7-lane-card-init188-controls-20261031.json'
    if sha256(canonical)!='8b47646a164c43bb7411b80e1bdabde3312e13d7cf46823d84264cb68d613442' or sha256(controls)!='89e0a68e44f0d98ced46da2df4370b78303f3c6ec5bf7b863cac717186656b68':
        raise ValueError('Frozen terminal thread-list matcher/control products differ')
    names=['arm7_lane_card_init_native_20261031.py','arm7_lane_card_init_oracle_20261031.py',
        'arm7_lane_card_init_boundaries_20261031.py','match_arm7_lane_card_init_20261031.py',
        'validate_arm7_lane_card_init_20261031.py','seal_arm7_lane_card_init188_20261031.py',
        'publish_arm7_lane_card_init188_20261031.py','provenance/arm7-lane-card-init188-sealing-20261031.json',
        'docs/2026-10-31-arm7-card-init188.md',
        'compile_arm7_lane_card_init188_v3_20261031.py','compile_arm7_lane_card_init188_v4_20261031.py',
        'compile_arm7_lane_card_init188_v5_20261031.py',
        'evidence/attempts/arm7-card-init188-profile-evolution-20261031.json',
        'evidence/attempts/arm7-card-next800-cohort81-overlap-20261031.json',
        'evidence/attempts/arm7-lane-card-init188-inherited-abi-guard-20261031.json',
        'evidence/attempts/arm7-lane-card-init188-include-name-20261031.json',
        canonical.relative_to(ROOT).as_posix(),controls.relative_to(ROOT).as_posix()]
    for folder in ('src/arm7/lane_20261031_card_init188','nonmatching/arm7-bulk/20261031/lane-card-init188-final',
        'nonmatching/arm7-bulk/20261031/lane-card-init188-v3','nonmatching/arm7-bulk/20261031/lane-card-init188-v4',
        'nonmatching/arm7-bulk/20261031/lane-card-init188-v5'):
        names.extend(path.relative_to(ROOT).as_posix() for path in (ROOT/folder).rglob('*') if path.is_file())
    files=[dict(path=name,sha256=sha256(ROOT/name),bytes=(ROOT/name).stat().st_size) for name in sorted(set(names))]
    manifest=ROOT/'provenance/arm7-lane-card-init188-handoff-20261031.json'
    write_json(manifest,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),files=files,
        candidateQualifiedIdentities=[{key:row[key] for key in ('program','processor','module','mode','address','bytes','source','sourceSha256')}
            for row in json.loads(canonical.read_text())['matches']],
        functions=1,bytes=188,instructionBytes=164,literalBytes=24,actualOriginalAndCompiledReturns=200,
        nestedReturns=2800,separatePrerequisiteReturns=400,providerFreeReturns=200,controls=44,
        taskThreadExecutions=0,contextSwitchExecutions=0,physicalHardwareCredit=0,
        pendingIndependentIntegratorAcceptance=True,wholeModuleSourceCredit=0,originalDataCredit=0,calleeSourceCredit=0,
        existingDependencies='Frozen explicit source/runtime pins retain complete create-thread model and original kernel/PXI helpers. No task thread, context-switch, original-data or callee-source credit. Private inputs/tools/raw references and Work excluded.',
        noSharedRegistryConfigLedgerPreferencesOrAcceptedInputsChanged=True))
    relative=sorted({row['path'] for row in files}|{manifest.relative_to(ROOT).as_posix()})
    staged=subprocess.run(['git','diff','--cached','--name-only'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.splitlines()
    if set(staged)-set(relative):
        raise ValueError('Refusing unrelated staged paths')
    pathspec=ROOT/'work/arm7-bulk-20261030/lane-card-init188-final/publication-pathspec.bin'
    pathspec.write_bytes(b'\0'.join(name.encode() for name in relative)+b'\0')
    subprocess.run(['git','add','--pathspec-from-file='+str(pathspec),'--pathspec-file-nul'],cwd=ROOT,check=True)
    subprocess.run(['git','commit','-m','Recover ARM7 common card initializer with measured SDK qualifiers'],cwd=ROOT,check=True)
    commit=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    print(json.dumps(dict(commit=commit,manifest=manifest.relative_to(ROOT).as_posix(),manifestSha256=sha256(manifest),files=len(relative))))


if __name__=='__main__':
    main()
