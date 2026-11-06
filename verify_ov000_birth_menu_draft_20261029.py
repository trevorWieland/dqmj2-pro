import itertools
import json
import sys
from pathlib import Path

import compile_ov000_birth_menu_20261029 as compilation
from link_runtime_unit import validate
from ov000_birth_menu_fixture_20261029 import Resources, ENTRY
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / "work/ov000-recovery/20261029/birth-menu-native"
REPORT = ROOT / "nonmatching/ov000/20261029-birth-context01/menu-native-result.json"


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python and Unicorn are required")
    compilation.run()
    source_report = ROOT / "nonmatching/ov000/20261029-birth-context01/compile-readable-speed1.json"
    entry = json.loads(source_report.read_text())["functions"][0]
    directory = WORK / "link" / entry["objectSha256"]
    bindings = qualified_bindings(entry)
    exact = False
    try:
        proof = validate(entry, bindings, directory)
        exact = proof["exactCallerBytes"]
        rejection = None
    except ValueError as error:
        rejection = str(error)
        if not isinstance(error.args[0], dict) or error.args[0].get("caller") != entry["name"]:
            raise
    output = directory / "caller.bin"
    code = output.read_bytes()
    resources = Resources()
    native = resources.overlay[ENTRY - 0x021D7240:ENTRY - 0x021D7240 + 360]
    pairs = [
        ((1, 0, 0), (2, 0, 0)),
        ((1, 0, 0), (1, 0, 0)),
        ((1, 0, 19), (2, 0, 0)),
        ((1, 0, 0), (2, 0, 19)),
        ((1, 0, 19), (2, 0, 19)),
        ((1, 0, 13), (2, 0, 14)),
        ((174, 0, 0), (1, 0, 0)),
        ((1, 0, 0), (174, 0, 0)),
    ]
    vectors, failures = [], []
    for serial, (parents, tier, selected) in enumerate(itertools.product(pairs, (0, 1, 5), range(3))):
        case = (*parents, tier, selected)
        try:
            original = resources.execute(native, case, serial)
            reconstructed = resources.execute(code, case, serial)
            if original["result"] != reconstructed["result"]:
                raise ValueError("Native/draft return or output field mismatch")
            if original["delegates"] != reconstructed["delegates"]:
                raise ValueError("Native/draft actual delegate inputs/results mismatch")
            vectors.append({"native": original, "draft": reconstructed})
        except Exception as error:
            failures.append({"case": case, "errorType": type(error).__name__, "error": str(error)})
    report = {
        "schemaVersion": 1,
        "createdUtc": now(),
        "romSha256": configuration()["romSha256"],
        "processor": "arm9",
        "module": "ov000",
        "mode": "arm",
        "address": hex(ENTRY),
        "bytes": 360,
        "moduleSha256": resources.overlay_meta["sha256"],
        "nativeSpanSha256": entry["targetSha256"],
        "source": entry["source"],
        "sourceSha256": entry["sourceSha256"],
        "objectSha256": entry["objectSha256"],
        "compilationReport": str(source_report.relative_to(ROOT)),
        "compilationReportSha256": sha256(source_report),
        "genuineLinkOutput": str(output.relative_to(ROOT)),
        "genuineLinkOutputSha256": sha256(output),
        "genuineLinkedBytes": len(code),
        "genuineLinkedMatchingBytes": sum(a == b for a, b in zip(native, code)),
        "genuineLinkExactCallerRejected": not exact,
        "genuineLinkRejection": rejection,
        "linkFiles": [{"path": str(path.relative_to(ROOT)), "sha256": sha256(path)}
                      for path in sorted(directory.iterdir()) if path.is_file()],
        "nativeSymbolEntries": bindings,
        "resourceHashes": resources.hashes,
        "vectorsPassed": len(vectors),
        "completedPassingExecutions": len(vectors) * 2,
        "vectors": vectors,
        "failures": failures,
        "accepted": False,
        "matchedSourceCredit": 0,
        "wholeModuleLinked": False,
        "reproduction": "python verify_ov000_birth_menu_draft_20261029.py",
        "generatorSha256": sha256(Path(__file__)),
        "fixtureGeneratorSha256": sha256(ROOT / "ov000_birth_menu_fixture_20261029.py"),
        "limitations": [
            "Actual genuine MW link still differs from native; draft remains unaccepted",
            "Disposable synthetic two-record stock, explicit resource pointers and zero-filled surrounding RAM",
            "Native delegate bodies run without host stubs; independent model checks caller aggregation",
            "The caller model delegates combination/paid rules to observed native helper outputs",
            "ABI return/output fields and preserved registers checked; volatile registers/flags not treated as equal",
            "Invalid selected slots, malformed resources and live scene/menu state unsupported",
        ],
    }
    write_json(REPORT, report)
    print(json.dumps({"vectorsPassed": len(vectors), "failures": len(failures),
                      "linkedMatchingBytes": report["genuineLinkedMatchingBytes"],
                      "accepted": False}))


if __name__ == "__main__":
    run()
