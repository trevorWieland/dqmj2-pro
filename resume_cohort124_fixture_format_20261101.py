import subprocess
import sys
from project import ROOT,read_json,write_json,sha256,now


def main():
    plan=read_json(ROOT/"evidence/verification/cohort-2026-10-29-124.json")
    assert not plan["linksPending"]and plan["sourceMatchedFunctions"]==9329 and plan["sourceLinkedBytes"]==729815
    assert sha256(ROOT/"recovery.json")==plan["sourceRegistrySha256"]
    assert sha256(ROOT/"source-preferences.json")==plan["sourcePreferenceSha256"]
    receipt=read_json(ROOT/"evidence/verification/cohort124-unregistered-fixture-format-20261101.json")
    assert sha256(ROOT/receipt["changed"])==receipt["newSha256"]
    assert sha256(ROOT/"main_resource_dictionary_fixture_v4_20261101.py")==receipt["selectedV4UnchangedSha256"]
    command=["finish_source_package_v10_20261101.py","--cohort","124","--stage",
     "stage_cohort124_pure_connected_v3_20261101.py","--document",
     "docs/2026-11-01-cohort124-fixture-format-recovery.md","--label","source-relative-include-and-connected-source"]
    log=ROOT/"logs/integration/cohort124-fixture-format-recovery-20261101.txt"
    output=ROOT/"evidence/verification/cohort124-fixture-format-recovery-20261101.json"
    result=dict(startedUtc=now(),state="running",command=command,sourceCredit=0,originalFailedDriverPreserved=True)
    write_json(output,result)
    with log.open("w",encoding="utf-8")as stream:
        run=subprocess.run([sys.executable,str(ROOT/command[0]),*command[1:]],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
    result.update(state="packaged"if run.returncode==0 else"failed",exitCode=run.returncode,
     finishedUtc=now(),log=log.relative_to(ROOT).as_posix(),logSha256=sha256(log))
    write_json(output,result)
    raise SystemExit(run.returncode)


if __name__=="__main__":
    main()
