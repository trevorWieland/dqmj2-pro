import os
import subprocess
from pathlib import Path
from link_arm7 import build_module
from project import ROOT, sha256, write_json


def build_cpu(modules, functions, symbols, bindings, config, work, reset_entry):
    from elftools.elf.elffile import ELFFile
    processor = modules[0]["processor"]
    plans, units = [], []
    for module in modules:
        plan, source = build_module(module, functions, symbols, config, work, bindings, prepare_only=True)
        plans.append(plan)
        units.extend(source)
    defined = {name for plan in plans for name in plan["defined"]}
    memory, sections, objects = [], [], []
    for index, plan in enumerate(plans):
        module = plan["module"]
        segment = f"MODULE{index}"
        output = module["name"] + "/module.bin"
        memory.append(f"{segment}: ORIGIN = {module['base']} > {output}")
        sections.append(f".module{index}: {{ ALIGNALL(2);\n" + "\n".join(plan["selectors"]) + f"\n}} > {segment}")
        if plan["bssSelectors"]:
            sections.append(f".bss{index}: {{\n" + "\n".join(plan["bssSelectors"]) + f"\n}} >> {segment}")
        objects.extend(plan["objects"])
    assignments = [f"{name} = {int(value, 0):#x};" for name, value in symbols.items() if name not in defined]
    for plan in plans:
        if plan["module"]["runtimeEntry"] is not None:
            assignments.append(f"{plan['entry']} = {int(plan['module']['runtimeEntry'], 0):#x};")
    entry_plan = next(plan for plan in plans if plan["module"]["runtimeEntry"] is not None and int(plan["module"]["runtimeEntry"], 0) == int(reset_entry, 0))
    lcf = work / (processor + ".lcf")
    lcf.write_text("MEMORY {\n" + "\n".join(memory) + "\n}\nSECTIONS {\n" + "\n".join(sections + assignments) + "\n}\n")
    response = work / (processor + "-objects.txt")
    response.write_text("\n".join('"' + item + '"' for item in objects) + "\n")
    elf_path = work / (processor + "-linked.elf")
    command = [str(config["linker"]), "-nostdlib", "-nodeadstrip", "-interworking", "-proc", "arm946e" if processor == "arm9" else "arm7tdmi", "-main", entry_plan["entry"], str(lcf), "@" + str(response), "-o", str(elf_path)]
    result = subprocess.run(command, cwd=work, env=dict(os.environ, LM_LICENSE_FILE=str(config["license"])), capture_output=True, text=True, errors="replace", timeout=180)
    reports = []
    linked_symbols = {}
    if result.returncode == 0:
        with elf_path.open("rb") as stream:
            elf = ELFFile(stream)
            elf_entry = elf["e_entry"]
            linked_symbols = {symbol.name: dict(symbol.entry) for symbol in elf.get_section_by_name(".symtab").iter_symbols()}
            segments = [dict(segment.header) for segment in elf.iter_segments()]
    for plan in plans:
        module = plan["module"]
        chosen = [unit for unit in units if unit["module"] == module["name"]]
        output = work / module["name"] / "module.bin"
        native = (ROOT / module["binary"]).read_bytes()
        checks = []
        for unit in chosen:
            symbol = linked_symbols.get(unit["function"])
            correct = bool(symbol and symbol["st_value"] & ~1 == int(unit["start"], 0) and symbol["st_size"] == int(unit["end"], 0) - int(unit["start"], 0))
            if unit["kind"] == "bss" and correct:
                correct = any(item["p_type"] == "PT_LOAD" and item["p_vaddr"] == int(unit["start"], 0) and item["p_memsz"] == unit["allocatedBytes"] and item["p_filesz"] == 0 for item in segments)
            checks.append({"symbol": unit["function"], "expectedAddress": unit["start"], "exact": correct})
            for interior in unit.get("interiorEntries", []):
                alias = linked_symbols.get(interior["name"])
                checks.append({"symbol": interior["name"], "expectedAddress": interior["address"], "separateFunctionCredit": False, "exact": bool(alias and alias["st_value"] & ~1 == int(interior["address"], 0))})
        exact = result.returncode == 0 and output.is_file() and output.read_bytes() == native and all(item["exact"] for item in checks)
        exact = exact and elf_entry & ~1 == int(reset_entry, 0) & ~1
        item = {"module": module["name"], "program": module["program"], "processor": processor, "inputSha256": module["sha256"], "output": str(output), "outputSha256": sha256(output) if output.is_file() else None, "inputBytes": len(native), "exactBytes": exact, "sourceFunctions": sum(unit["kind"] == "function" for unit in chosen), "sourceBytes": sum(unit["compiledBytes"] for unit in chosen), "sourceBssBytes": sum(unit.get("allocatedBytes", 0) for unit in chosen), "originalScaffoldingBytes": len(native) - sum(unit["compiledBytes"] for unit in chosen), "runtimeEntry": module["runtimeEntry"], "processorResetEntry": reset_entry, "linkedElfEntry": hex(elf_entry) if result.returncode == 0 else None, "symbolChecks": checks, "symbolCheckPassed": exact, "originalGapFunctionBindings": plan["gapDefinitions"], "command": command, "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        reports.append(item)
        item["sourceAlignmentFill"] = plan.get("sourceAlignmentFill")
        item["sourceAlignmentFillBytes"] = (plan.get("sourceAlignmentFill") or {}).get("bytes", 0)
        item["originalScaffoldingBytes"] -= item["sourceAlignmentFillBytes"]
        item["linkerRegeneratedBytes"] = sum(unit["compiledBytes"] for unit in chosen if unit["kind"] == "linkage")
        item["sourceBytes"] -= item["linkerRegeneratedBytes"]
    if not all(item["exactBytes"] for item in reports):
        write_json(ROOT / "evidence/linking/utility-failed-cpu.json", {"processor": processor, "modules": reports})
        raise ValueError("Combined embedded processor link differs: " + processor + result.stdout + result.stderr)
    return reports, units
