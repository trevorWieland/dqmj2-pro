import json
import subprocess
from pathlib import Path
from project import ROOT,sha256,write_json
REPORT='evidence/arm7/lane-card-callback-scope-20261031.json'
EXPECTED='762a389d613559fa4216031db86a72fda3fad9a327d443e33347efe6131f2258'


def main():
    if sha256(ROOT/REPORT)!=EXPECTED:raise ValueError('Frozen callback boundary proof differs')
    names=['arm7_lane_card_service_engine_20261031.py','prove_arm7_lane_card_callbacks_scope_20261031.py',
        'publish_arm7_lane_card_callbacks_scope_20261031.py',REPORT,
        'provenance/arm7-lane-card-callback-scope-runtime-pins-20261031.json',
        'docs/2026-10-31-arm7-card-callback-boundaries.md',
        'evidence/attempts/arm7-lane-card-callback-linker-refusals-20261031.json']
    files=[dict(path=name,sha256=sha256(ROOT/name),bytes=(ROOT/name).stat().st_size) for name in sorted(names)]
    manifest=ROOT/'provenance/arm7-lane-card-callback-scope-handoff-20261031.json'
    write_json(manifest,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),files=files,
        newSourceCredit=0,initializedDenominatorBytesAdded=0,proposedInstructions=232,proposedPools=12,
        directCallbackReturns=360,transferCallerReturns=12,indirectCallbackReturns=12,controls=27,
        replayCommand='python prove_arm7_lane_card_callbacks_scope_20261031.py',
        privateInputsAndWorkProductsExcluded=True,sharedConfigRegistryLedgerUnchanged=True,
        dependencyClosure='Six explicitly hashed local runtime/inventory dependencies; known original binary hashes and pinned Python/Unicorn/pyelftools versions. Complete gzip trace is regenerated.',
        limitations='Boundary proposal and explicit synthetic SPI readback only; no source/module/physical-hardware/storage credit. Existing unknown-symbol linker guards remain intact. Global unknown indirect references are not proved closed.'))
    relative=sorted(set(names)|{manifest.relative_to(ROOT).as_posix()})
    staged=subprocess.run(['git','diff','--cached','--name-only'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.splitlines()
    if set(staged)-set(relative):raise ValueError('Refusing unrelated staged files')
    path=ROOT/'work/arm7-bulk-20261030/lane-card-callback-scope/publication-pathspec.bin'
    path.write_bytes(b'\0'.join(name.encode() for name in relative)+b'\0')
    subprocess.run(['git','add','--pathspec-from-file='+str(path),'--pathspec-file-nul'],cwd=ROOT,check=True)
    subprocess.run(['git','commit','-m','Qualify original ARM7 SPI callback boundaries without source credit'],cwd=ROOT,check=True)
    commit=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    print(json.dumps(dict(commit=commit,manifest=manifest.relative_to(ROOT).as_posix(),sha256=sha256(manifest),files=len(relative))))


if __name__=='__main__':main()
