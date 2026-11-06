import shutil
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256


def main():
    lane = ROOT / 'evidence/lanes/parallel-wave20261104/child-arm7-wl/revision'
    copied = ROOT.parent / 'wl1104rev-replay'
    source = ROOT / 'wave20261104_child_wl_revision_conditions.py'
    destination = copied / source.name
    shutil.copyfile(source, destination)
    command = [sys.executable, str(destination)]
    process = subprocess.run(command, cwd=copied, capture_output=True, text=True, timeout=120)
    if process.returncode:
        raise ValueError((process.stdout, process.stderr))
    original = read_json(lane / 'native-condition-controls.json')
    fresh = read_json(copied / lane.relative_to(ROOT) / 'native-condition-controls.json')
    equal = original == fresh
    if not equal:
        raise ValueError('Copied-root condition/layout vectors or results differ')
    result = dict(status='passed', copiedRoot=str(copied), independentSourceAndToolCopies=True,
        originalWorkObjectsCopied=False, command=command, exitCode=process.returncode,
        stdout=process.stdout, stderr=process.stderr, conditionProducer=dict(path=source.name, sha256=sha256(source)),
        rootConditionReportSha256=sha256(lane / 'native-condition-controls.json'),
        copiedConditionReportSha256=sha256(copied / lane.relative_to(ROOT) / 'native-condition-controls.json'),
        actualOriginalAndLinkedFragments=fresh['fragments'], fixtureResultsIdentical=equal,
        fullNativeCallerExecutions=0, nativeDeviceOrHelperExecutions=0)
    write_json(lane / 'copied-root-condition-proof.json', result)
    print(dict(copiedRoot=str(copied), fragments=fresh['fragments'], fixtureResultsIdentical=equal))


if __name__ == '__main__':
    main()
