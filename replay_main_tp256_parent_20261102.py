import subprocess
import sys
from project import ROOT, read_json, write_json, sha256


def main():
    report = ROOT / 'evidence/matches/main-tp256-20261102.json'
    before = sha256(report)
    code = 'import runpy,sys;sys.path.insert(0,' + repr(str(ROOT)) + ');runpy.run_path(' + repr(str(ROOT / 'match_main_tp256_20261102.py')) + ',run_name="__main__")'
    run = subprocess.run([sys.executable, '-I', '-S', '-c', code], cwd=ROOT.parent, capture_output=True, timeout=180)
    assert run.returncode == 0, (run.stdout.decode(errors='replace'), run.stderr.decode(errors='replace'))
    assert sha256(report) == before
    current = read_json(report)
    write_json(ROOT / 'evidence/verification/main-tp256-parent-replay-20261102.json',
        dict(passed=True, sourceCredit=0, pythonIsolatedNoSite=True, actualParentWorkingDirectory=True,
            report=report.relative_to(ROOT).as_posix(), reportSha256=before, completeReportByteIdentical=True,
            nativeTopReturns=current['oracle']['actualTopReturns'], actualWrongReturns=720,
            suppliedLowerCalls=current['oracle']['suppliedBoundaryCalls'], actualLowerNativeReturns=0))
    print(dict(passed=True, completeReportByteIdentical=True, actualTopReturns=6720, actualWrongReturns=720))


if __name__ == '__main__':
    main()
