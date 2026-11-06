import json
import subprocess
from project import ROOT,sha256,write_json


def main():
    files=['arm7_lane_alarm_selector_native_20261031.py','arm7_lane_alarm_selector_oracle_20261031.py',
        'arm7_lane_alarm_selector_boundaries_20261031.py','prove_arm7_lane_alarm_selector_source_20261031.py',
        'prepare_arm7_lane_alarm_selector_packet_20261031.py','derive_arm7_lane_alarm_selector_validator_20261031.py',
        'compile_arm7_lane_alarm_selector_20261031.py','compile_arm7_lane_alarm_selector_base_20261031.py',
        'match_arm7_lane_alarm_selector_20261031.py','validate_arm7_lane_alarm_selector_20261031.py',
        'publish_arm7_lane_alarm_selector_handoff_20261031.py','evidence/attempts/arm7-lane-alarm-selector-source-20261031.json',
        'evidence/matches/arm7-lane-alarm-selector-20261031.json','evidence/verification/arm7-lane-alarm-selector-controls-20261031.json',
        'docs/2026-10-31-arm7-raw-mode-alarm-selector-source.md']
    for directory in ('src/arm7/lane_20261031_alarm_selector','nonmatching/arm7-bulk/20261031/lane-alarm-selector-final',
        'nonmatching/arm7-bulk/20261031/lane-main-alarm-selector'):
        files.extend(path.relative_to(ROOT).as_posix() for path in (ROOT/directory).rglob('*') if path.is_file())
    files=sorted(set(files))
    for name in files:
        path=ROOT/name
        if path.suffix in ('.c','.h','.py'):
            text=path.read_text()
            if len(text.splitlines())>500 or (path.suffix in ('.c','.h') and ('/*' in text or '//' in text)):
                raise ValueError('Selector source policy failed: '+name)
    manifest=ROOT/'provenance/arm7-lane-alarm-selector-handoff-20261031.json'
    write_json(manifest,dict(kind='private-source-only-lane-handoff',files=[dict(path=name,sha256=sha256(ROOT/name)) for name in files],
        matchedCandidateBytes=176,acceptedSourceCredit=0,sharedRegistryConfigLedgerChanges=False,
        replay=['python match_arm7_lane_alarm_selector_20261031.py','python validate_arm7_lane_alarm_selector_20261031.py'],
        runtimeDependencyManifest='nonmatching/arm7-bulk/20261031/lane-alarm-selector-final/generator-pins.json'))
    subprocess.run(['git','add','--',*files,manifest.relative_to(ROOT).as_posix()],cwd=ROOT,check=True)
    subprocess.run(['git','commit','-m','Recover host ARM7 raw-mode alarm selector with native effect proof'],cwd=ROOT,check=True)
    print(json.dumps(dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        files=len(files)+1,manifestSha256=sha256(manifest))))


if __name__=='__main__':
    main()
