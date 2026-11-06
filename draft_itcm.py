import argparse
import concurrent.futures
import json
import os
import re
import subprocess
from pathlib import Path
import match_lowlevel as matcher
from abi_slots import preserve_argument_slots
from decompiler_shapes import order_register_locals
from utility_shapes import reverse_register_locals
from narrow_increments import canonical_byte_increments
from typed_global_fields import recover_global_records

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/m2c"
M2C = ROOT / "tools/m2c/m2c-c632946b8cfbe8fce442b522dba92dfa72f1f317/m2c.py"
PRELUDE = "typedef unsigned char u8;\ntypedef signed char s8;\ntypedef unsigned short u16;\ntypedef signed short s16;\ntypedef unsigned int u32;\ntypedef signed int s32;\ntypedef unsigned long long u64;\ntypedef signed long long s64;\ntypedef float f32;\ntypedef double f64;\n#define NULL ((void *)0)\n#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))\n"
RESOLVE_WORD_TYPES = False
M2C_OPTIONS = []
VOLATILE_FIELDS = False
WORD_GLOBALS = False
VOID_RETURN = False
ARGUMENTS = {}
REGISTER_ORDER = False
ABI_HINTS = False
REVERSE_REGISTER_ORDER = False
DIRECT_INCREMENTS = False
TYPED_GLOBALS = False


def infer_arguments():
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
    from capstone.arm import ARM_OP_MEM, ARM_REG_PC
    from draft_arm7 import argument_counts
    specs = []
    for module, base, config, binary_path in [("itcm", 0x01ff8000, "config/arm9/itcm/symbols.txt", "extract/arm9/itcm.bin"),
                                              ("main", 0x02000000, "config/arm9/symbols.txt", "extract/arm9/arm9.bin")]:
        binary = (ROOT / binary_path).read_bytes()
        for mode, size, address in re.findall(r"kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)", (ROOT / config).read_text()):
            if mode == "thumb" and not ABI_HINTS:
                continue
            decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if mode == "thumb" else CS_MODE_ARM)
            decoder.detail = True
            location, count = int(address, 0), int(size, 0)
            instructions = list(decoder.disasm(binary[location - base:location - base + count], location))
            pools = {(((instruction.address + 4) & ~3) if mode == "thumb" else instruction.address + 8) + operand.mem.disp for instruction in instructions for operand in instruction.operands
                     if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC}
            pool_bytes = {address + offset for address in pools for offset in range(4)}
            specs.append({"address": location, "instructions": [instruction for instruction in instructions if instruction.address not in pool_bytes]})
    if ABI_HINTS:
        from utility_abi import argument_hints
        return argument_hints(specs)[0]
    return argument_counts(specs)


def declaration(name, native=False):
    address = matcher.symbol_address(name)
    count = ARGUMENTS.get(address) if not name.startswith("func_ov") else ARGUMENTS.get(name)
    parameters = "" if count is None else (", ".join(["u32"] * count) if count else "void")
    return "extern u32 " + ("native_fn_" + name.removeprefix("func_") if native else name) + "(" + parameters + ");\n"


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def inputs():
    assembly = (ROOT / "asm/_dsd_gap@itcm_1.s").read_text()
    assembly = "\n".join(line.split(";")[0].rstrip() for line in assembly.splitlines()
                         if not any(word in line for word in (".include", "arm_func_start", "arm_func_end")))
    functions = sorted(set(re.findall(r"\bfunc_[A-Za-z0-9_]+", assembly)))
    data = sorted(set(re.findall(r"\bdata_[A-Za-z0-9_]+", assembly)))
    context = PRELUDE + "".join(declaration(name) for name in functions)
    context += "".join("extern u32 " + name + ";\n" if WORD_GLOBALS else "extern u8 " + name + "[];\n" for name in data)
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "itcm.s").write_text(assembly)
    (WORK / "context.c").write_text(context)
    return assembly


def source_text(draft, original, limit=500):
    if RESOLVE_WORD_TYPES:
        for unknown, scalar in [("M2C_UNK8", "s8"), ("M2C_UNK16", "s16"), ("M2C_UNK32", "s32"), ("M2C_UNK64", "s64"), ("M2C_UNK", "s32")]:
            draft = re.sub(r"\b" + unknown + r"\b", scalar, draft)
    if VOLATILE_FIELDS:
        draft = re.sub(r",\s*((?:s|u)(?:8|16|32|64)|void)(\s*\*+)\s*,", r", volatile \1\2,", draft)
    unknown = set(re.findall(r"\bM2C_[A-Z0-9_]+", draft)) - {"M2C_FIELD"}
    if unknown:
        raise ValueError("Untranslated decompiler macros: " + ", ".join(sorted(unknown)))
    name = "native_itcm_" + original.removeprefix("func_")
    functions = sorted(set(re.findall(r"\bfunc_[A-Za-z0-9_]+", draft)) - {original})
    data = sorted(set(re.findall(r"\bdata_[A-Za-z0-9_]+", draft)))
    declarations = "".join(declaration(function, True) for function in functions)
    declarations += "".join("extern u32 native_data_" + item.removeprefix("data_") + ";\n" if WORD_GLOBALS else "extern u8 native_data_" + item.removeprefix("data_") + "[];\n" for item in data)
    for function in functions:
        draft = re.sub(r"\b" + function + r"\b", "native_fn_" + function.removeprefix("func_"), draft)
    for item in data:
        draft = re.sub(r"\b" + item + r"\b", "native_data_" + item.removeprefix("data_"), draft)
    draft = re.sub(r"\b" + original + r"\b", name, draft)
    result = PRELUDE + declarations + draft
    result, added_slots = preserve_argument_slots(result, name)
    if REGISTER_ORDER:
        result = order_register_locals(result, name)
    if REVERSE_REGISTER_ORDER:
        result = reverse_register_locals(result, name)
    if DIRECT_INCREMENTS:
        result, changes = canonical_byte_increments(result)
    if TYPED_GLOBALS:
        result, changes = recover_global_records(result)
    if limit is not None and len(result.splitlines()) > limit:
        raise ValueError("Recovered routine exceeds physical-line limit before refactoring")
    return result


def one(original):
    context = WORK / "context.c"
    if VOID_RETURN:
        text = re.sub(r"extern u32 " + original + r"\(([^;]*)\);", r"extern void " + original + r"(\1);", context.read_text())
        context = WORK / "contexts" / (original + ".c")
        context.parent.mkdir(exist_ok=True)
        context.write_text(text)
    command = [matcher.sys.executable, str(M2C), "--target", "arm-mwcc-c", "--comment-style", "none",
               "--no-cache", "--valid-syntax", "--globals", "none", *M2C_OPTIONS, "--context", str(context),
               "-f", original, str(WORK / "itcm.s")]
    env = dict(os.environ, PYTHONPATH=str(ROOT / "tools/m2c-python"))
    item = {"nativeAlias": original, "command": command, "draftOnly": True}
    try:
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=60)
        item.update(exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr)
        if result.returncode:
            return item
        source = WORK / "drafts" / (original + ".c")
        source.parent.mkdir(exist_ok=True)
        source.write_text(source_text(result.stdout, original))
        item["draftSource"] = source.relative_to(ROOT).as_posix()
        item["attempts"] = []
        for optimization, inline, speed in [(2, "off", False), (2, "noauto", False), (2, "off", True), (3, "off", True), (4, "off", True)]:
            try:
                records, matches = matcher.compare(source, "itcm", optimization, inline, speed)
            except matcher.UnresolvedNativeSymbol as error:
                item["attempts"].append(error.details)
                continue
            item["attempts"].extend(records)
            if matches:
                item["match"] = next(iter(matches.values()))[0]
                break
    except Exception as error:
        item["failure"] = f"{type(error).__name__}: {error}"
    return item


def verify(report):
    accepted = []
    for match in report["matches"]:
        source = ROOT / match["source"]
        if matcher.sha(source.read_bytes()) != match["sourceSha256"]:
            raise ValueError("Accepted source changed: " + match["source"])
        flags = match["compilerFlags"]
        _, found = matcher.compare(source, "itcm", int(flags[0][2:]), flags[flags.index("-inline") + 1], "speed" in flags)
        if match["name"] not in found:
            raise ValueError("Accepted translated function stopped matching: " + match["name"])
        entry, code = found[match["name"]]
        binary = (ROOT / "extract/arm9/itcm.bin").read_bytes()
        address = int(entry["address"], 0)
        try:
            entry["oracle"] = matcher.oracle(entry, code, binary[address - 0x01FF8000:address - 0x01FF8000 + entry["bytes"]])
        except Exception as error:
            entry["oracle"] = {"supported": False, "failure": f"{type(error).__name__}: {error}", "limitation": "Byte/relocation matching is established; native behavior requires a broader platform model"}
        accepted.append(entry)
    return accepted


def main():
    global RESOLVE_WORD_TYPES, M2C_OPTIONS, VOLATILE_FIELDS, WORD_GLOBALS, VOID_RETURN, ARGUMENTS, REGISTER_ORDER, ABI_HINTS, REVERSE_REGISTER_ORDER, DIRECT_INCREMENTS, TYPED_GLOBALS
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default="translated03")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--resolve-word-types", action="store_true")
    parser.add_argument("--volatile-fields", action="store_true")
    parser.add_argument("--m2c-option", action="append", default=[])
    parser.add_argument("--word-globals", action="store_true")
    parser.add_argument("--void-return", action="store_true")
    parser.add_argument("--infer-arguments", action="store_true")
    parser.add_argument("--register-order", action="store_true")
    parser.add_argument("--abi-hints", action="store_true")
    parser.add_argument("--reverse-register-order", action="store_true")
    parser.add_argument("--direct-increments", action="store_true")
    parser.add_argument("--typed-globals", action="store_true")
    parser.add_argument("--overlay-leaf-hints", action="store_true")
    args = parser.parse_args()
    target = ROOT / f"evidence/matches/itcm-{args.batch}.json"
    if args.verify:
        report = json.loads(target.read_text())
        verified = verify(report)
        report["matches"] = verified
        write(target, report)
        print({"verifiedFunctions": len(verified), "bytes": sum(item["bytes"] for item in verified)})
        return
    if target.exists():
        raise ValueError("Accepted batch exists; select a new batch name")
    RESOLVE_WORD_TYPES = args.resolve_word_types
    M2C_OPTIONS = args.m2c_option
    VOLATILE_FIELDS = args.volatile_fields
    WORD_GLOBALS = args.word_globals
    VOID_RETURN = args.void_return
    ABI_HINTS = args.abi_hints
    ARGUMENTS = infer_arguments() if args.infer_arguments or ABI_HINTS else {}
    if args.overlay_leaf_hints:
        from overlay_leaf_hints import infer
        names = sorted(set(re.findall(r"\bfunc_ov\d+_[0-9a-f]{8}\b", (ROOT / "asm/_dsd_gap@itcm_1.s").read_text())))
        ARGUMENTS.update(infer(names))
    REGISTER_ORDER = args.register_order
    REVERSE_REGISTER_ORDER = args.reverse_register_order
    DIRECT_INCREMENTS = args.direct_increments
    TYPED_GLOBALS = args.typed_globals
    inputs()
    accepted = {item.get("nativeAlias", item.get("originalSymbol"))
                for path in (ROOT / "evidence/matches").glob("*.json")
                for item in json.loads(path.read_text()).get("matches", []) if item.get("module") == "itcm"}
    originals = re.findall(r"^(\S+) kind:function", (ROOT / "config/arm9/itcm/symbols.txt").read_text(), re.M)
    originals = [name for name in originals if name not in accepted][:args.limit]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(one, originals):
            results.append(result)
            print(json.dumps({"function": result["nativeAlias"], "matched": "match" in result,
                              "failure": result.get("failure"), "exitCode": result.get("exitCode")}), flush=True)
    matches = []
    for item in results:
        if "match" not in item:
            continue
        old = item["match"]
        source = ROOT / f"src/itcm/{args.batch}/{old['name']}.c"
        if source.exists():
            raise ValueError("Refusing to overwrite accepted source: " + str(source))
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes((ROOT / item["draftSource"]).read_bytes())
        flags = old["compilerFlags"]
        _, found = matcher.compare(source, "itcm", int(flags[0][2:]), flags[flags.index("-inline") + 1], "speed" in flags)
        if old["name"] not in found:
            raise ValueError("Promoted source differs from exact draft")
        entry, code = found[old["name"]]
        binary = (ROOT / "extract/arm9/itcm.bin").read_bytes()
        address = int(entry["address"], 0)
        try:
            entry["oracle"] = matcher.oracle(entry, code, binary[address - 0x01FF8000:address - 0x01FF8000 + entry["bytes"]])
        except Exception as error:
            entry["oracle"] = {"supported": False, "failure": f"{type(error).__name__}: {error}", "limitation": "Byte/relocation matching is established; native behavior requires a broader platform model"}
        matches.append(entry)
    report = {"schemaVersion": 1, "romSha256": matcher.sha((ROOT / "inputs/game.nds").read_bytes()),
              "module": "itcm", "moduleInputSha256": matcher.sha((ROOT / "extract/arm9/itcm.bin").read_bytes()),
              "matches": matches, "nativeSymbols": {rel["symbol"]: rel["target"] for match in matches for rel in match["relocations"]},
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": ["Decompiler output is accepted only after complete native byte and relocation comparison", "Unsupported behavioral paths remain explicit"]}
    write(ROOT / f"evidence/attempts/itcm-{args.batch}-drafts.json", results)
    write(target, report)
    print({"drafted": len(results), "matched": len(matches), "bytes": sum(item["bytes"] for item in matches)})


if __name__ == "__main__":
    main()
