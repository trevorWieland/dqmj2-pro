import json
import subprocess
from project import ROOT,sha256,write_json


def main():
    files=['arm7_lane_initializer_native_20261031.py','arm7_lane_initializer_oracle_20261031.py',
        'arm7_lane_initializer_boundaries_20261031.py','prepare_arm7_lane_initializer_packet_20261031.py',
        'derive_arm7_lane_initializer_validator_20261031.py','match_arm7_lane_initializer_20261031.py',
        'validate_arm7_lane_initializer_20261031.py','publish_arm7_lane_initializer_handoff_20261031.py',
        'evidence/matches/arm7-lane-initializer-20261031.json','evidence/verification/arm7-lane-initializer-controls-20261031.json',
        'docs/2026-10-31-arm7-lane-channel-initializer-source.md']
    for directory in ('src/arm7/lane_20261031_initializer','nonmatching/arm7-bulk/20261031/lane-initializer-final'):
        files.extend(path.relative_to(ROOT).as_posix() for path in (ROOT/directory).rglob('*') if path.is_file())
    files=sorted(set(files))
    for name in files:
        path=ROOT/name
        if path.suffix in ('.c','.h','.py'):
            text=path.read_text()
            if len(text.splitlines())>500 or (path.suffix in ('.c','.h') and ('/*' in text or '//' in text)):
                raise ValueError('Initializer source policy failed: '+name)
    manifest=ROOT/'provenance/arm7-lane-initializer-handoff-20261031.json'
    write_json(manifest,dict(kind='private-source-only-lane-handoff',files=[dict(path=name,sha256=sha256(ROOT/name)) for name in files],
        matchedCandidateBytes=92,acceptedSourceCredit=0,sharedRegistryConfigLedgerChanges=False,
        replay=['python match_arm7_lane_initializer_20261031.py','python validate_arm7_lane_initializer_20261031.py'],
        runtimeDependencyManifest='nonmatching/arm7-bulk/20261031/lane-initializer-final/generator-pins.json'))
    subprocess.run(['git','add','--',*files,manifest.relative_to(ROOT).as_posix()],cwd=ROOT,check=True)
    subprocess.run(['git','commit','-m','Recover ARM7 channel initializer with source-only execution proof'],cwd=ROOT,check=True)
    print(json.dumps(dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        files=len(files)+1,manifestSha256=sha256(manifest))))


if __name__=='__main__':
    main()
