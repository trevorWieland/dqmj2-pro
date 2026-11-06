import json
import os
from pathlib import Path
import arm7_runtime
import match_arm7_boot as boot

ROOT = Path(__file__).resolve().parent


def main():
    image = (ROOT / "extract/arm7/arm7.bin").read_bytes()
    layout = arm7_runtime.derive(image)
    if layout != json.loads(arm7_runtime.MANIFEST.read_text()):
        raise ValueError("ARM7 composition layout is stale")
    if boot.sha(boot.COMPILER.read_bytes()) != boot.COMPILER_HASH:
        raise ValueError("ARM7 composition compiler identity changed")
    source = ROOT / "src/arm7/boot/composition.c"
    boot.WORK.mkdir(parents=True, exist_ok=True)
    address = int(layout["compositionTableAddress"], 0)
    offset, size = layout["compositionTableFileOffset"], layout["compositionTableBytes"]
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    flags = ["-O2", "-proc", "arm7tdmi", "-sym", "on", "-nolink", "-c"]
    attempt, result = boot.compile_source(source, boot.COMPILER, flags, "native_arm7_composition_023a7118", address, environment)
    if result is None:
        raise ValueError("Typed ARM7 composition source did not compile")
    entry, code = result
    native = image[offset:offset + size]
    if code != native or len(code) != 24:
        raise ValueError("Typed ARM7 composition bytes differ from the measured descriptor table")
    entry.pop("module")
    entry.update(kind="typed-autoload-descriptors", placement="physical-arm7-image-metadata",
                 inputFileOffset=offset, inputImageSha256=layout["imageSha256"],
                 exactAfterDeclaredRelocation=True, targetSha256=boot.sha(native),
                 sourceMetadataBytes=size, runtimeFunctionBytes=0, runtimeDataBytes=0,
                 tableRows=layout["composition"], compiler=boot.COMPILER.relative_to(ROOT).as_posix())
    report = {"schemaVersion": 1, "romSha256": boot.sha((ROOT / "inputs/game.nds").read_bytes()),
              "processor": "arm7", "runtimeMappingCanonical": True, "containerMatches": [entry],
              "nativeSymbols": {}, "attempts": [attempt], "containerMetadataMatchedBytes": size,
              "functionMatched": 0, "dataMatchedBytes": 0, "bssMatchedBytes": 0,
              "limitations": ["This descriptor table is outside all three runtime module byte spans",
                              "Physical-image metadata equality does not contribute executable-function or runtime-data coverage"]}
    output = ROOT / "evidence/data/arm7-composition.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print({"typedPhysicalMetadataBytes": size, "objectSha256": entry["objectSha256"]})


if __name__ == "__main__":
    main()
