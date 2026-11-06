import itertools
import json
import os
import subprocess
from project import ROOT, configuration, native_dependencies, read_json, sha256, verify_inputs, write_json


def main():
    config = configuration()
    inputs = verify_inputs(config)
    native_dependencies(config)
    from elftools.elf.elffile import ELFFile
    flags = read_json(ROOT / "oracle/results.json")["compiler"]["flags"]
    source = ROOT / "evidence/attempts/sdk-fill.c"
    expected = (ROOT / "extract/arm9/arm9.bin").read_bytes()[0x8D78:0x8E0C]
    results = []
    pins = {"2.0/base": "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880", "2.0/sp1p5": "89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca", "1.2/base": "87b4f748825ded418355e4ae35e032ce8b27c083cc4c60598ce2a75d346e4399"}
    work = ROOT / "work/runtime-recovery/fill-options"
    work.mkdir(parents=True, exist_ok=True)
    configurations = itertools.product(pins, ["arm946e", "arm7tdmi", "arm9tdmi", "v5te"], ["none", "noprop", "nocse", "nolifetimes", "noloop", "nostrength", "nodeadstore", "nodeadcode"], ["2,p", "3,p", "4,p"])
    for compiler, processor, modifier, optimization in configurations:
        command_flags = flags[:]
        command_flags[0] = "-O" + optimization
        command_flags[command_flags.index("-proc") + 1] = processor
        if modifier != "none":
            command_flags += ["-opt", modifier]
        executable = ROOT / "tools/mwccarm/mwccarm" / compiler / "mwccarm.exe"
        if sha256(executable) != pins[compiler]:
            raise ValueError("Experimental compiler identity differs")
        obj = work / "trial.o"
        command = [str(executable), *command_flags, "-c", str(source), "-o", str(obj)]
        run = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(config["license"])), capture_output=True, timeout=30)
        row = {"compiler": executable.relative_to(ROOT).as_posix(), "compilerSha256": pins[compiler], "flags": command_flags, "exitCode": run.returncode}
        if run.returncode == 0:
            with obj.open("rb") as stream:
                elf = ELFFile(stream)
                symbol = next(item for item in elf.get_section_by_name(".symtab").iter_symbols() if item.name == "native_main_02008d78")
                code = elf.get_section(symbol["st_shndx"]).data()[symbol["st_value"]:symbol["st_value"] + symbol["st_size"]]
            row.update(bytes=len(code), equalBytes=sum(a == b for a, b in zip(code, expected)), exact=code == expected)
            if row["exact"]:
                (work / "exact.o").write_bytes(obj.read_bytes())
        results.append(row)
    report = {"romSha256": inputs["rom"]["sha256"], "module": "main", "processor": "arm9", "mode": "arm", "address": "0x02008d78", "bytes": 148, "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha256(source), "experimentScriptSha256": sha256(ROOT / "experiment_sdk_fill.py"), "reproduce": ["python", "experiment_sdk_fill.py"], "attempts": results, "accepted": False, "ordinarySourceCredit": 0, "limitations": ["Compiler settings are experimental hypotheses", "Partial instruction equality receives no source credit", "An exact result requires independent bounded behavior and full module linking before acceptance"]}
    write_json(ROOT / "evidence/attempts/sdk-fill-options.json", report)
    if inputs != verify_inputs(config):
        raise ValueError("Inputs changed during experiment")
    print(json.dumps({"trials": len(results), "exact": sum(item.get("exact", False) for item in results), "bestEqualBytes": max(item.get("equalBytes", 0) for item in results)}))


if __name__ == "__main__":
    main()
