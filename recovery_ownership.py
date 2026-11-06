import argparse
from project import ROOT, configuration, now, read_json, sha256, write_json
from recovery_registry import batches


def reservation(address, size=1):
    path = ROOT / "recovery-ownership.json"
    if not path.exists():
        return None
    return next((item for item in read_json(path)["mainReservedRanges"] if int(item["start"], 0) < address + size and address < int(item["end"], 0)), None)


def filter_batch(batch, module="main"):
    path = ROOT / f"evidence/matches/{module}-{batch}.json"
    if any(item["report"] == path.relative_to(ROOT).as_posix() for item in batches()):
        raise ValueError("Cannot filter an accepted source batch")
    from ledger_state import collect_matches
    accepted, rejected = collect_matches(configuration()["romSha256"])
    report = read_json(path)
    retained, excluded = [], []
    for item in report["matches"]:
        address = int(item["address"], 0)
        collision = next((entry for entry_key, entry in accepted.items() if entry_key[0] == item["module"] and entry_key[2] < address + item["bytes"] and address < entry_key[2] + entry["size"]), None)
        owner = reservation(address, item["bytes"]) if item["module"] == "main" else None
        if collision is None and owner is None:
            retained.append(item)
            continue
        source = (ROOT / item["source"]).resolve()
        allowed = (ROOT / "src/runtime" / batch).resolve()
        scalar_source = source.parent == (ROOT / "src/overlays").resolve() and source.name.startswith(f"{module}_{batch}_") and source.suffix == ".c"
        if not (source.is_relative_to(allowed) or scalar_source) or sha256(source) != item["sourceSha256"]:
            raise ValueError("Unsafe or changed unpublished source variant")
        if sum(entry["source"] == item["source"] for entry in report["matches"]) != 1:
            raise ValueError("Cannot relocate a source containing multiple reported functions")
        if any(item["source"] in entry["sourceHashes"] for entry in batches()):
            raise ValueError("Cannot relocate an accepted source")
        destination = (ROOT / "work/runtime-recovery/excluded" / batch / source.name).resolve()
        if not destination.is_relative_to((ROOT / "work").resolve()) or destination.exists():
            raise ValueError("Unsafe or occupied excluded-source destination")
        destination.parent.mkdir(parents=True, exist_ok=True)
        source.replace(destination)
        excluded.append({**item, "source": destination.relative_to(ROOT).as_posix(), "originalDraftSource": item["source"], "accepted": False, "exclusion": "function overlaps accepted source" if collision else "function assigned to another worker", "owner": owner["owner"] if owner else None, "existingSource": collision["source"] if collision else None})
    report["matches"] = retained
    report["unacceptedMatches"] = report.get("unacceptedMatches", []) + excluded
    report["ownershipFilter"] = {"createdUtc": now(), "ownershipSha256": sha256(ROOT / "recovery-ownership.json"), "retained": len(retained), "excluded": len(excluded)}
    write_json(path, report)
    return report["ownershipFilter"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("batch")
    parser.add_argument("--module", default="main", choices=("main", "ov000", "ov001", "ov002", "ov003", "ov005", "ov006", "ov007"))
    options = parser.parse_args()
    print(filter_batch(options.batch, options.module))
