import sys
from unittest.mock import patch
import build_lock
import build_modules as builder
from project import ROOT, configuration, now, read_json, write_json


def main():
    fixture = (ROOT / "work/build-status-fixture").resolve()
    if not fixture.is_relative_to((ROOT / "work").resolve()):
        raise ValueError("Unsafe build-status fixture")
    fixture.mkdir(parents=True, exist_ok=True)
    config = configuration()
    write_json(fixture / "project.json", {"dsd": str(config["dsd"]), "linker": str(config["linker"]), "license": str(config["license"]), "romSha256": config["romSha256"]})
    write_json(fixture / "evidence/linking/utility-latest.json", {"exactContainerMatch": True, "output": "build/missing-utility.bin"})
    work = fixture / "build/link-work"
    work.mkdir(parents=True, exist_ok=True)
    (work / "objects.txt").write_text("")
    def checked_modules(report):
        report["modules"] = [{"module": "injected-verified-module", "exactBytes": True}]
    with patch.object(builder, "ROOT", fixture), patch.object(builder, "WORK", work), patch.object(builder, "EVIDENCE", fixture / "evidence/linking"), patch.object(sys, "argv", ["build_modules.py"]), patch.object(builder, "prepare_units", return_value=[]), patch.object(builder, "generated_config", return_value=fixture / "config.yaml"), patch.object(builder, "run", return_value=True), patch.object(builder, "native_link_symbols"), patch.object(builder, "thumb_gap_alignment"), patch.object(builder, "replacements"), patch.object(builder, "compare_modules", side_effect=checked_modules):
        status = builder.main()
    result = read_json(fixture / "evidence/linking/latest.json")
    if status != 1 or not result.get("allModuleBytesExact") or not result.get("symbolCheckPassed") or "Recomposed utility input is missing or stale" not in result.get("failure", ""):
        raise ValueError("Late construction error was accepted despite module checks passing")
    blocked = False
    with patch.object(build_lock, "ROOT", fixture):
        with build_lock.accepted_build():
            try:
                with build_lock.accepted_build():
                    pass
            except (RuntimeError, BlockingIOError):
                blocked = True
        with build_lock.accepted_build():
            released = True
    if not blocked or not released:
        raise ValueError("Concurrent accepted build lock failed")
    report = {"schemaVersion": 1, "createdUtc": now(), "lateConstructionFailureReturnsNonzero": True, "earlierModuleChecksStillRecorded": True, "concurrentAcceptedBuildRejected": True, "lockReleasedAfterExit": True, "actualCompilerOrLinkerInvocations": 0, "fixture": fixture.relative_to(ROOT).as_posix(), "passed": True, "sourceReconstructionComplete": False}
    write_json(ROOT / "evidence/verification/build-status.json", report)
    print(report)


if __name__ == "__main__":
    main()
