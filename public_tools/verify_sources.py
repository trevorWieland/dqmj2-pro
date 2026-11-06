import argparse
import json
import sys
from pathlib import Path
from public_manifest import ManifestError, verify, write_report


def main():
    parser = argparse.ArgumentParser(description="Verify accepted public source hashes and include closure without reading a ROM or invoking a compiler.")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=Path("public/accepted-functions.json"))
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    try:
        unused, units, pins, summary = verify(root, manifest_path)
    except (ManifestError, OSError, KeyError, TypeError, ValueError) as error:
        summary = dict(status="source-integrity-failed", error=str(error), compilerInvoked=False, originalInputsRead=False,
                       nativeMatchingVerified=False, moduleLinkingVerified=False, wholeRomVerified=False)
    if args.report:
        report = args.report if args.report.is_absolute() else root / args.report
        report = report.resolve()
        if not report.is_relative_to(root / "build") and not report.is_relative_to(root / "work"):
            raise ManifestError("Report must be a JSON output beneath --root/build or --root/work")
        if report.suffix.lower() != ".json":
            raise ManifestError("Report output must be JSON")
        write_report(report, summary)
    print(json.dumps(summary, indent=2))
    return 0 if summary["status"] == "source-integrity-passed" else 1


if __name__ == "__main__":
    sys.exit(main())
