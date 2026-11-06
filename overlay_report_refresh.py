import copy
import hashlib
import json
import os
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OBJECT_FIELDS = {"object", "objectSha256"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def proof(value):
    if isinstance(value, dict):
        return {key: proof(item) for key, item in value.items() if key not in OBJECT_FIELDS}
    if isinstance(value, list):
        return [proof(item) for item in value]
    return value


def replace_metadata(frozen, current):
    if isinstance(frozen, dict):
        for key in frozen:
            if key in OBJECT_FIELDS:
                frozen[key] = current[key]
            else:
                replace_metadata(frozen[key], current[key])
    elif isinstance(frozen, list):
        for first, second in zip(frozen, current):
            replace_metadata(first, second)


def refresh_data_report(path, current):
    path = Path(path).resolve()
    if not path.is_relative_to(ROOT / "evidence/data"):
        raise ValueError("Data report destination must be inside repository evidence/data")
    source = (ROOT / current["source"]).resolve()
    if not source.is_relative_to(ROOT / "src") or sha(source) != current["sourceSha256"]:
        raise ValueError("Frozen data source path/content differs")
    if sha(ROOT / "inputs/game.nds") != current["romSha256"]:
        raise ValueError("Data report/input ROM namespace differs")
    if not current.get("dataMatches") or any(not (item.get("exactAfterDeclaredRelocation") or item.get("exactZeroStorage")) for item in current["dataMatches"]):
        raise ValueError("Data report contains an unverified region")
    for item in current["dataMatches"]:
        if item["sourceSha256"] != current["sourceSha256"] or item["objectSha256"] != current["objectSha256"]:
            raise ValueError("Per-region data provenance differs")
    if path.exists():
        frozen = json.loads(path.read_text())
        if proof(frozen) != proof(current):
            raise ValueError("Frozen data source/namespace/target/region/relocation/proof differs; metadata refresh refused")
        updated = copy.deepcopy(frozen)
        replace_metadata(updated, current)
        if updated == frozen:
            return False
    else:
        updated = current
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    temporary.write_bytes(json.dumps(updated, indent=2).encode())
    os.replace(temporary, path)
    return True
