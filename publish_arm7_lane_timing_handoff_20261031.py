import json
import subprocess
from pathlib import Path
from project import ROOT,sha256,write_json


def main():
    files=['arm7_lane_calc_timer_native_20261030.py','prove_arm7_lane_calc_timer_native_20261030.py',
        'arm7_lane_skip_native_20261031.py','prove_arm7_lane_skip_native_20261031.py',
        'arm7_lane_timing_oracle_20261031.py','arm7_lane_timing_boundaries_20261031.py',
        'prepare_arm7_lane_timing_packet_20261031.py','derive_arm7_lane_timing_matcher_20261031.py',
        'derive_arm7_lane_timing_validator_20261031.py','match_arm7_lane_timing_20261031.py',
        'validate_arm7_lane_timing_20261031.py','publish_arm7_lane_timing_handoff_20261031.py',
        'evidence/attempts/arm7-lane-calc-timer-native-20261030.json','evidence/attempts/arm7-lane-skip-native-20261031.json',
        'evidence/matches/arm7-lane-timing-20261031.json','evidence/verification/arm7-lane-timing-controls-20261031.json',
        'docs/2026-10-31-arm7-lane-timing-source.md']
    for directory in ('src/arm7/lane_20261031_timing','nonmatching/arm7-bulk/20261031/lane-timing-final'):
        files.extend(path.relative_to(ROOT).as_posix() for path in (ROOT/directory).rglob('*') if path.is_file())
    files=sorted(set(files))
    if any(name.startswith(('work/','config/','inputs/','tools/','deps/')) for name in files):
        raise ValueError('Source-only handoff contains prohibited generated/shared/private input trees')
    for name in files:
        path=ROOT/name
        if path.suffix in ('.c','.h','.py'):
            text=path.read_text()
            if len(text.splitlines())>500 or (path.suffix in ('.c','.h') and ('/*' in text or '//' in text)):
                raise ValueError('Handoff source policy failed: '+name)
    manifest=ROOT/'provenance/arm7-lane-timing-handoff-20261031.json'
    write_json(manifest,dict(kind='private-source-only-lane-handoff',files=[dict(path=name,sha256=sha256(ROOT/name)) for name in files],
        matchedCandidateBytes=492,acceptedSourceCredit=0,sharedRegistryConfigLedgerChanges=False,
        replay=['python match_arm7_lane_timing_20261031.py','python validate_arm7_lane_timing_20261031.py'],
        runtimeDependencyManifest='nonmatching/arm7-bulk/20261031/lane-timing-final/generator-pins.json'))
    paths=files+[manifest.relative_to(ROOT).as_posix()]
    subprocess.run(['git','add','--',*paths],cwd=ROOT,check=True)
    subprocess.run(['git','commit','-m','Recover and qualify ARM7 timer calculation and sequence skip source'],cwd=ROOT,check=True)
    print(json.dumps(dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        files=len(paths),manifest=manifest.relative_to(ROOT).as_posix(),manifestSha256=sha256(manifest))))


if __name__=='__main__':
    main()
