import sys
from pathlib import Path
from project import ROOT, configuration, write_json
from rom_layout import compare


if __name__ == "__main__":
    target = (ROOT / sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "build/link-work/roundtrip.nds"
    report = compare(configuration()["rom"].read_bytes(), target.read_bytes())
    write_json(ROOT / "evidence/rom/repack-comparison.json", report)
    print({key: report[key] for key in ("exact", "sameComponentBytes", "changedComponentBytes")})
