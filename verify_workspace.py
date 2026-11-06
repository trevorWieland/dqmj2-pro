import io
import json
import re
import subprocess
import tokenize
from pathlib import Path
from project import ROOT, configuration, now, read_json, sha256, verify_inputs, write_json


def isolation():
    snapshot = read_json(ROOT / "provenance/seed-inventory.json")
    changes = []
    unavailable = []
    checked = {}
    for category, parent, rows in (("baseline", snapshot["baseline"], snapshot["baselineFiles"]), ("application", snapshot["application"], snapshot["applicationFiles"])):
        checked[category] = len(rows)
        if not Path(parent).is_dir():
            unavailable.append({"category": category, "path": parent})
            continue
        for row in rows:
            path = Path(parent) / row["path"]
            if not path.is_file() or sha256(path) != row["sha256"]:
                changes.append({"category": category, "path": str(path), "expectedSha256": row["sha256"], "actualSha256": sha256(path) if path.is_file() else None})
    for row in snapshot["originalInputs"]:
        path = Path(row["path"])
        if not path.is_file():
            unavailable.append({"category": "original-input", "path": str(path)})
            continue
        if sha256(path) != row["sha256"]:
            changes.append({"category": "original-input", "path": str(path)})
    return {"filesChecked": checked, "originalInputsChecked": len(snapshot["originalInputs"]), "unavailableSnapshots": unavailable, "auditAvailable": not unavailable, "observedChanges": changes, "allRecordedFilesUnchanged": not changes and not unavailable, "baselineAndInputsUnchanged": None if any(row["category"] != "application" for row in unavailable) else not any(row["category"] != "application" for row in changes), "applicationObservedUnchanged": None if any(row["category"] == "application" for row in unavailable) else not any(row["category"] == "application" for row in changes), "limitations": ["Hash snapshots detect observed changes but do not attribute changes by concurrent external processes", "External snapshot paths are optional audit inputs; unavailable paths are reported and never count as unchanged"]}


def policy():
    paths = list(ROOT.glob("*.py")) + list((ROOT / "src").rglob("*.c")) + list((ROOT / "src").rglob("*.h"))
    paths += list((ROOT / "src").rglob("*.s")) + list((ROOT / "src").rglob("*.cpp"))
    paths += list((ROOT / "src").rglob("*.inc"))
    for extension in ('.c', '.h', '.cpp', '.inc'):
        paths += list((ROOT / 'nonmatching').rglob('*' + extension))
        paths += list((ROOT / 'ports').rglob('*' + extension))
    paths += list((ROOT / "config/arm7").glob("*.py"))
    paths += list((ROOT / "evidence/tools").glob("*.java"))
    paths += list((ROOT / "evidence/save").glob("*.py"))
    failures = []
    files = []
    for path in sorted(set(paths)):
        text = path.read_text(encoding="utf-8-sig")
        count = len(text.splitlines())
        comments = False
        if path.suffix == ".py":
            comments = any(t.type == tokenize.COMMENT for t in tokenize.generate_tokens(io.StringIO(text).readline))
        else:
            stripped = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', "", text)
            comments = bool(re.search(r"//|/\*", stripped))
        row = {"path": path.relative_to(ROOT).as_posix(), "physicalLines": count, "hasComments": comments, "sha256": sha256(path)}
        files.append(row)
        if count > 500 or comments:
            failures.append(row)
    return {"authoredFiles": files, "passed": not failures, "failures": failures, "excluded": ["unmodified seed evidence/provenance", "third-party tools and dependencies", "generated analysis, configuration and ledgers"]}


def index_evidence():
    rows = []
    for path in sorted((ROOT / "evidence").rglob("*.json")):
        if path.name == "index.json":
            continue
        rows.append({"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
    write_json(ROOT / "evidence/index.json", {"schemaVersion": 1, "createdUtc": now(), "buildSha256": configuration()["romSha256"], "records": rows})


if __name__ == "__main__":
    config = configuration()
    inputs = verify_inputs(config)
    remote = subprocess.run(["git", "remote"], cwd=ROOT, capture_output=True, text=True, check=True)
    report = {"schemaVersion": 1, "createdUtc": now(), "inputs": inputs, "gitRemotes": remote.stdout.splitlines(), "isolation": isolation(), "sourcePolicy": policy()}
    write_json(ROOT / "evidence/verification/workspace.json", report)
    index_evidence()
    print({"originalsAndRecordedSourcesUnchanged": report["isolation"]["allRecordedFilesUnchanged"], "sourcePolicyPassed": report["sourcePolicy"]["passed"], "remoteCount": len(report["gitRemotes"])})
    if report["gitRemotes"] or not report["sourcePolicy"]["passed"] or not report["isolation"]["allRecordedFilesUnchanged"]:
        raise SystemExit(1)
