import copy
import subprocess
from pathlib import Path
from unittest.mock import patch
import install_tools
import ledger_state
import run_checks
import verify_workspace
from project import ROOT, now, read_json, write_json


if __name__ == "__main__":
    tests = []
    accepted_state = ledger_state.build_state(write=False)
    accepted_count = accepted_state["functionMatched"]
    lock = read_json(ROOT / "tools.lock.json")
    changed = copy.deepcopy(lock)
    changed["nativeDependencies"][0]["importedVersion"] = "unaccepted-version"
    try:
        install_tools.enforce_existing_runtime(lock, changed)
    except ValueError:
        tests.append("Changed native dependency pin rejected")
    else:
        raise ValueError("Changed runtime silently repinned")
    changed = copy.deepcopy(lock)
    changed["python"]["sha256"] = "0" * 64
    try:
        install_tools.enforce_existing_runtime(lock, changed)
    except ValueError:
        tests.append("Changed Python identity rejected")
    else:
        raise ValueError("Changed Python silently repinned")
    source = {"baseline": str(ROOT / "work/nonexistent-baseline"), "application": str(ROOT / "work/nonexistent-app"), "baselineFiles": [], "applicationFiles": [], "originalInputs": [{"path": str(ROOT / "work/nonexistent-original.nds"), "sha256": "0" * 64}]}
    with patch.object(verify_workspace, "read_json", return_value=source):
        audit = verify_workspace.isolation()
    if audit["auditAvailable"] or audit["allRecordedFilesUnchanged"] or len(audit["unavailableSnapshots"]) != 3:
        raise ValueError("Unavailable external audit counted as passed")
    tests.append("Absent external snapshot paths reported unavailable without crashing")
    for label, error in (("launch", OSError("injected launch failure")), ("timeout", subprocess.TimeoutExpired("injected command", 1))):
        fixture = (ROOT / "work" / ("runner-failure-" + label)).resolve()
        if not fixture.is_relative_to((ROOT / "work").resolve()):
            raise ValueError("Unsafe runner fixture path")
        fixture.mkdir(parents=True, exist_ok=True)
        (fixture / "recovery.json").write_bytes((ROOT / "recovery.json").read_bytes())
        with patch.object(run_checks, "ROOT", fixture), patch.object(run_checks.sys, "argv", ["run_checks.py"]), patch.object(run_checks.subprocess, "run", side_effect=error), patch.object(verify_workspace, "index_evidence"):
            status = run_checks.main()
        failure_report = read_json(fixture / "evidence/verification/checks.json")
        if status != 1 or failure_report["allChecksPassed"] or not failure_report["steps"][0].get("failure"):
            raise ValueError("Runner failed to persist launch/timeout evidence")
        tests.append("Runner persists injected " + label + " failure")
    fixture = ROOT / "work/runner-registry-mutation"
    fixture.mkdir(parents=True, exist_ok=True)
    (fixture / "recovery.json").write_bytes((ROOT / "recovery.json").read_bytes())
    def mutate_registry(command, **options):
        document = read_json(fixture / "recovery.json")
        document["injectedScopeChange"] = True
        write_json(fixture / "recovery.json", document)
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
    with patch.object(run_checks, "ROOT", fixture), patch.object(run_checks.sys, "argv", ["run_checks.py"]), patch.object(run_checks.subprocess, "run", side_effect=mutate_registry), patch.object(verify_workspace, "index_evidence"):
        status = run_checks.main()
    changed_scope = read_json(fixture / "evidence/verification/checks.json")
    if status != 1 or changed_scope["allChecksPassed"] or changed_scope["buildAndOracleChecksPassed"] or changed_scope["recoveryRegistryUnchanged"]:
        raise ValueError("Changed source registry retained successful validation status")
    tests.append("Changed source registry rejects otherwise successful runner steps")
    accepted_matches, unused = ledger_state.collect_matches(accepted_state["rom"]["sha256"])
    dependent = next(item for item in accepted_matches.values() if item.get("name") and item["source"].startswith("src/") and not item.get("alternativeImplementations"))
    dependency_report = ROOT / dependent["report"]
    changed_dependency = copy.deepcopy(read_json(dependency_report))
    source_rows = changed_dependency.get("functionMatches", changed_dependency.get("matches", []))
    changed_row = next(item for item in source_rows if item.get("name") == dependent["name"])
    changed_row["sourceDependencies"] = [{"path": dependent["source"], "sha256": "0" * 64}]
    original_reader = ledger_state.read_json
    with patch.object(ledger_state, "read_json", side_effect=lambda path: changed_dependency if Path(path) == dependency_report else original_reader(path)):
        invalid_dependency = ledger_state.build_state(write=False)
    if invalid_dependency["functionMatched"] >= accepted_count:
        raise ValueError("Changed include dependency retained its source-match status")
    tests.append("Changed authored dependency invalidates source acceptance without altering source files")
    latest = read_json(ROOT / "evidence/linking/latest.json")
    old_maybe = ledger_state.maybe
    failure = copy.deepcopy(latest)
    failure["symbolCheckPassed"] = False
    with patch.object(ledger_state, "maybe", side_effect=lambda path, default=None: failure if path == "evidence/linking/latest.json" else old_maybe(path, default)):
        rejected = ledger_state.build_state(write=False)
    if rejected["currentHostArm9ModuleLinksExact"] or any(m["sourceLinkedBytes"] for m in rejected["modules"] if m["processor"] == "arm9" and not m.get("program")):
        raise ValueError("Failed symbol check accepted as source linked")
    tests.append("Failed symbol check invalidates source-link acceptance")
    arm7_failure = copy.deepcopy(read_json(ROOT / "evidence/linking/arm7-latest.json"))
    arm7_failure["symbolCheckPassed"] = False
    with patch.object(ledger_state, "maybe", side_effect=lambda path, default=None: arm7_failure if path == "evidence/linking/arm7-latest.json" else old_maybe(path, default)):
        rejected = ledger_state.build_state(write=False)
    if rejected["arm7RuntimeModuleLinksExact"] or rejected["arm7RecomposedImageExact"] or any(m["sourceLinkedBytes"] for m in rejected["modules"] if m["processor"] == "arm7" and not m.get("program")):
        raise ValueError("Failed ARM7 symbol check accepted as source linked")
    tests.append("Failed ARM7 symbol check invalidates runtime source-link acceptance")
    utility_failure = copy.deepcopy(read_json(ROOT / "evidence/linking/utility-latest.json"))
    utility_failure["symbolCheckPassed"] = False
    with patch.object(ledger_state, "maybe", side_effect=lambda path, default=None: utility_failure if path == "evidence/linking/utility-latest.json" else old_maybe(path, default)):
        rejected = ledger_state.build_state(write=False)
    if rejected["currentUtilityModuleLinksExact"] or rejected["utilityContainerRecomposedExact"] or rejected["outerRomUsesRecomposedUtility"]:
        raise ValueError("Failed embedded symbol check accepted as source linked")
    tests.append("Failed embedded symbol check invalidates only embedded acceptance")
    from source_variants import consolidate
    units = read_json(ROOT / "build/link-work/source-units.json")["units"]
    for unit in units:
        if not unit.get("equivalentUnlinkedImplementations"):
            continue
        chosen = {key: value for key, value in unit.items() if key != "equivalentUnlinkedImplementations"}
        previous = unit["equivalentUnlinkedImplementations"][0]
        if len(consolidate([copy.deepcopy(previous), copy.deepcopy(chosen)])) != 1:
            raise ValueError("Equivalent source proofs inflate linked definitions")
        for field, value in (("targetSha256", "0" * 64), ("sha256", "0" * 64), ("mode", "invalid-mode")):
            changed = {**chosen, field: value}
            try:
                consolidate([copy.deepcopy(previous), changed])
            except ValueError:
                tests.append("Source variant rejects altered " + field)
            else:
                raise ValueError("Invalid equivalent source proof was accepted")
        break
    targets = [ROOT / "build/exact-layout.nds", ROOT / "build/arm7-link/image.bin", ROOT / "build/utility-link/utility.bin"]
    legacy = ROOT / "build/link-work/arm7/arm7.bin"
    if legacy.exists():
        targets.append(legacy)
    moved = []
    try:
        for target in targets:
            temporary = ROOT / "work" / (target.name + ".freshness-test")
            if not target.resolve().is_relative_to(ROOT.resolve()) or temporary.exists():
                raise ValueError("Unsafe freshness fixture path")
            target.rename(temporary)
            moved.append((target, temporary))
        missing = ledger_state.build_state(write=False)
        if missing["arm7OriginalBlobLinkExact"] or missing["arm7RecomposedImageExact"] or missing["utilityContainerRecomposedExact"] or missing["exactContainerMatchWithScaffolding"]:
            raise ValueError("Missing generated output retained current-match status")
        tests.append("Missing ARM7 and exact-ROM products invalidate current-match flags")
    finally:
        for target, temporary in moved:
            temporary.rename(target)
        restored = ledger_state.build_state(write=False)
    if restored["functionMatched"] != accepted_count or restored["arm7OriginalBlobLinkExact"] != accepted_state["arm7OriginalBlobLinkExact"] or not restored["arm7RecomposedImageExact"] or not restored["exactContainerMatchWithScaffolding"]:
        raise ValueError("Valid evidence was not restored")
    report = {"schemaVersion": 1, "createdUtc": now(), "passed": True, "negativeAcceptanceCases": tests, "restoredSourceFunctions": restored["functionMatched"], "sourceReconstructionComplete": False}
    write_json(ROOT / "evidence/verification/evidence-freshness.json", report)
    print(report)
