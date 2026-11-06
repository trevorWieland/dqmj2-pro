import json
import subprocess
from pathlib import Path
from project import ROOT,sha256,write_json
REPORT='evidence/matches/arm7-lane-card-abi16-1252-20261031.json'
CONTROL='evidence/verification/arm7-lane-card-abi16-1252-controls-20261031.json'


def main():
    if sha256(ROOT/REPORT)!='bf09612598c6c1486c9f3496c60259c268e04a79cf03c8dbf883ed2eb81fc249' or sha256(ROOT/CONTROL)!='a250928a1cc7c35304076968060631169d76cde027ce1f4ef0d2ab3d9c61733c':
        raise ValueError('Frozen unified source proof/control products differ')
    names=['match_arm7_lane_card_abi16_20261031.py','validate_arm7_lane_card_abi16_20261031.py',
        'compile_arm7_lane_card_abi16_1252_20261031.py','publish_arm7_lane_card_abi16_1252_20261031.py',
        'arm7_lane_card_abi16_boundaries_20261031.py','arm7_lane_card_abi16_oracle_20261031.py',
        'arm7_lane_card_callbacks_native_20261031.py','arm7_lane_card_callbacks_oracle_20261031.py',
        'arm7_lane_card_callbacks_boundaries_20261031.py','arm7_lane_card_pages_engine_20261031.py',
        'arm7_lane_card_pages_native_20261031.py','arm7_lane_card_pages_oracle_20261031.py',
        'qualified_arm7_card_scope_20261031.py','prove_arm7_card_shared_layout_20261031.py',
        'nonmatching/arm7-bulk/20261031/lane-card-abi16-layout-probe/layout_probe.c',
        'evidence/verification/arm7-card-shared-layout-20261031.json',
        'evidence/attempts/arm7-card-callbacks244-negative-size-20261031.json',
        'docs/2026-10-31-arm7-card-shared-interface1252.md',REPORT,CONTROL]
    for folder in ('src/arm7/lane_20261031_card_abi16','nonmatching/arm7-bulk/20261031/lane-card-abi16-1252-final'):
        names.extend(p.relative_to(ROOT).as_posix() for p in (ROOT/folder).rglob('*') if p.is_file())
    files=[dict(path=name,sha256=sha256(ROOT/name),bytes=(ROOT/name).stat().st_size) for name in sorted(set(names))]
    manifest=ROOT/'provenance/arm7-lane-card-abi16-1252-handoff-20261031.json'
    report=json.loads((ROOT/REPORT).read_text())
    write_json(manifest,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),files=files,
        functions=9,bytes=1252,instructionBytes=1168,literalBytes=84,actualOwnedOriginalAndCompiledReturns=4224,
        actualOriginalHelperReturns=55400,controls=58,separateAbiLayoutControls=3,sharedHeader='src/arm7/lane_20261031_card_abi16/native_card_types.h',
        unchangedCBodyHistory=report['unchangedCBodyHistory'],sharedInterface=report['sharedInterface'],
        supersedesUnacceptedHistoricalCandidates=['arm7-lane-card-service452','arm7-lane-card-init188','arm7-lane-card-callbacks244'],
        additionalInitializedDenominatorBytes=0,physicalHardwareCredit=0,ordinaryAssemblyOrBlobCredit=0,
        sourceAcceptancePendingIntegrator=True,privateInputsToolsOriginalReferencesAndWorkExcluded=True,
        frozenHistoricalFilesChanged=False,acceptedSourceOrSharedRegistryConfigLedgerChanged=False,
        existingDependencies='Explicit53-file AST/runtime closure uses frozen source-independent models and exact canonical callback supplement. Previous frozen models and historical hypotheses retain their original hashes. No original executable is a compiler input. Rebuild all output products with the matcher; Root owns registry/module/ROM acceptance.'))
    relative=sorted({r['path'] for r in files}|{manifest.relative_to(ROOT).as_posix()})
    staged=subprocess.run(['git','diff','--cached','--name-only'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.splitlines()
    if set(staged)-set(relative):raise ValueError('Refusing unrelated staged files')
    path=ROOT/'work/arm7-bulk-20261030/lane-card-abi16-1252/publication-pathspec.bin'
    path.write_bytes(b'\0'.join(name.encode() for name in relative)+b'\0')
    subprocess.run(['git','add','--pathspec-from-file='+str(path),'--pathspec-file-nul'],cwd=ROOT,check=True)
    subprocess.run(['git','commit','-m','Recover nine ARM7 card routines through one complete shared interface'],cwd=ROOT,check=True)
    commit=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    print(dict(commit=commit,manifest=manifest.relative_to(ROOT).as_posix(),manifestSha256=sha256(manifest),files=len(relative)))


if __name__=='__main__':main()
