import argparse
from pathlib import Path
from project import ROOT, configuration, read_json, sha256, write_json

REGISTRY = ROOT / "recovery.json"


def batches():
    return read_json(REGISTRY)["batches"] if REGISTRY.exists() else []


def oracles():
    return read_json(REGISTRY).get("oracles", []) if REGISTRY.exists() else []


def entries(report):
    return report.get("functionMatches", report.get("matches", report.get("functions", []))) + report.get("dataMatches", []) + report.get("containerMatches", []) + report.get("linkageMatches", [])


def register(path, reproduction):
    path = (ROOT / path).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError("Report lies outside private repository")
    report = read_json(path)
    if report.get("romSha256") != configuration()["romSha256"]:
        raise ValueError("Report namespace differs")
    hashes = {}
    for item in entries(report):
        from source_dependencies import dependency_hashes, dependencies_current
        dependencies = dependency_hashes(item, report)
        if not dependencies_current(item, report):
            raise ValueError("Published source include closure is incomplete or stale")
        item = {**report, **item}
        linkage = item.get("linkerRegenerated") and item.get("exactNativeLinkageBytes") and item.get("linkageOnlyRelink", {}).get("exactBytes") and item.get("ordinaryFunctionCredit") == 0
        if not (item.get("exactBytes") or item.get("exactAfterDeclaredRelocation") or item.get("kind") == "bss" and item.get("exactZeroStorage") or linkage):
            raise ValueError("Published source contains an unaccepted byte comparison")
        source, obj = ROOT / item["source"], ROOT / item["object"]
        if sha256(source) != item["sourceSha256"] or sha256(obj) != item["objectSha256"]:
            raise ValueError("Published source/object identity differs")
        hashes[item["source"]] = item["sourceSha256"]
        for relative, expected in dependencies.items():
            if sha256(ROOT / relative) != expected or relative in hashes and hashes[relative] != expected:
                raise ValueError("Published source dependency differs")
            hashes[relative] = expected
    for generator in report.get("generatorSources", []):
        if sha256(ROOT / generator["path"]) != generator["sha256"]:
            raise ValueError("Generated linkage implementation changed")
        hashes[generator["path"]] = generator["sha256"]
    if not hashes:
        raise ValueError("Cannot register an empty source batch")
    relative = path.relative_to(ROOT).as_posix()
    existing = batches()
    previous = next((b for b in existing if b["report"] == relative), None)
    if previous and previous["sourceHashes"] != hashes:
        raise ValueError("An accepted source was changed; explicit regression migration required")
    existing = [b for b in existing if b["report"] != relative]
    kind = "linkage" if report.get("linkageMatches") else "mixed" if report.get("containerMatches") and report.get("dataMatches") else "container" if report.get("containerMatches") else "data" if report.get("dataMatches") else "functions"
    existing.append({"report": relative, "reproduce": reproduction, "sourceHashes": hashes, "entries": len(entries(report)), "kind": kind})
    document = read_json(REGISTRY) if REGISTRY.exists() else {"schemaVersion": 1}
    document["batches"] = sorted(existing, key=lambda b: b["report"])
    write_json(REGISTRY, document)


def verify_sources():
    for batch in batches():
        for source, expected in batch["sourceHashes"].items():
            if sha256(ROOT / source) != expected:
                raise ValueError("Accepted source changed: " + source)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("reproduce", nargs="+")
    options = parser.parse_args()
    register(options.report, options.reproduce)
