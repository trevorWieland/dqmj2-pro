import hashlib
import json
import platform
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha256(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".pending." + str(os.getpid()))
    temporary.write_text(text, encoding="utf-8")
    for attempt in range(20):
        try:
            temporary.replace(path)
            return
        except OSError:
            if attempt == 19:
                raise
            time.sleep(0.05)


def write_json(path, value):
    write_text(path, json.dumps(value, indent=2) + "\n")


def now():
    return datetime.now(timezone.utc).isoformat()


def configuration(path=None):
    path = Path(path).resolve() if path else ROOT / "project.json"
    config = read_json(path)
    for key in ("rom", "save", "deps", "dsd", "compiler", "linker", "license", "output"):
        value = Path(config[key])
        config[key] = value if value.is_absolute() else path.parent / value
    config["root"] = ROOT
    return config


def verify_inputs(config):
    if platform.python_version() != "3.13.5":
        raise RuntimeError("Expected pinned Python 3.13.5")
    result = {}
    for name in ("rom", "save"):
        path = config[name]
        value = {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
        if value["sha256"] != config[name + "Sha256"]:
            raise ValueError("Input identity mismatch: " + name)
        result[name] = value
    return result


def native_dependencies(config):
    sys.path.insert(0, str(config["deps"]))
