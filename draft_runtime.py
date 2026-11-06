import argparse
import concurrent.futures
import json
import os
import re
import subprocess
from pathlib import Path
import match_runtime as matcher

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/runtime-recovery/m2c"
M2C = ROOT / "tools/m2c/m2c-c632946b8cfbe8fce442b522dba92dfa72f1f317/m2c.py"
PRELUDE = "typedef unsigned char u8;\ntypedef signed char s8;\ntypedef unsigned short u16;\ntypedef signed short s16;\ntypedef unsigned int u32;\ntypedef signed int s32;\ntypedef unsigned long long u64;\ntypedef signed long long s64;\ntypedef float f32;\ntypedef double f64;\n#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))\n"


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


PRELUDE += "#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))\n#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))\n"
PRELUDE += "#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))\n"
PRELUDE += "#define NULL ((void *)0)\n"

FUNCTION_INPUTS = {}
FUNCTION_ADDRESSES = {}
SOURCE_RETURNS = {}
OPTIONS = None


def module_paths(module):
    if module == "main":
        return ROOT / "extract/arm9/arm9.bin", ROOT / "config/arm9/symbols.txt", 0x02000000
    return ROOT / f"extract/arm9_overlays/{module}.bin", ROOT / f"config/arm9/overlays/{module}/symbols.txt", 0x021D7240


def inputs():
    module = getattr(OPTIONS, "module", "main")
    if getattr(OPTIONS, "source_returns", False):
        from known_returns import return_catalogue
        SOURCE_RETURNS.update(return_catalogue(module))
    files = sorted((ROOT / "asm").glob(f"_dsd_gap@{module}_*.s"))
    if not files:
        raise ValueError("No module-qualified analysis assembly inputs")
    text = "\n".join(path.read_text() for path in files)
    symbols = module_paths(module)[1].read_text()
    FUNCTION_ADDRESSES.update({name: address for name, address in re.findall(r"^(\S+) kind:function\([^\n]+\) addr:0x([0-9a-f]{8})$", symbols, re.M)})
    prefix = "thumb" if OPTIONS is not None and OPTIONS.thumb else "arm"
    for original, body in re.findall(r"    " + prefix + r"_func_start (\w+)\n(.*?)    " + prefix + r"_func_end \1", text, re.S):
        assembly = ".text\n.global " + original + "\n" + "\n".join(line.split(";")[0].rstrip() for line in body.splitlines()) + "\n"
        functions = sorted(set(re.findall(r"\bfunc_[A-Za-z0-9_]+", assembly)))
        data = sorted(set(re.findall(r"\bdata_[A-Za-z0-9_]+", assembly)))
        context = PRELUDE + "".join("extern u32 " + name + "();\n" for name in functions)
        context += "".join("extern u8 " + name + "[];\n" for name in data)
        if SOURCE_RETURNS:
            from known_returns import apply_context
            context = apply_context(context, SOURCE_RETURNS)
        FUNCTION_INPUTS[original] = (assembly, context)
    WORK.mkdir(parents=True, exist_ok=True)


def source_text(draft, original):
    if OPTIONS is not None and OPTIONS.word_args:
        declaration = re.search(r"\b" + original + r"\(([^()]*)\)\s*\{", draft)
        if declaration:
            parameters = re.sub(r"\bM2C_UNK(?:32)?\s+(?=arg\d+\b)", "u32 ", declaration[1])
            draft = draft[:declaration.start(1)] + parameters + draft[declaration.end(1):]
    if OPTIONS is not None and OPTIONS.abi_slots:
        from abi_slots import preserve_argument_slots
        draft, added = preserve_argument_slots(draft, original)
    if OPTIONS is not None and OPTIONS.register_order:
        from decompiler_shapes import order_register_locals
        draft = order_register_locals(draft, original)
    if OPTIONS is not None and OPTIONS.stack_buffers:
        from stack_buffers import recover_single_stack_buffer
        draft, changes = recover_single_stack_buffer(draft, FUNCTION_INPUTS[original][0])
    unknown = set(re.findall(r"\bM2C_[A-Z0-9_]+", draft)) - {"M2C_FIELD"}
    if unknown:
        raise ValueError("Untranslated decompiler macros: " + ", ".join(sorted(unknown)))
    module = getattr(OPTIONS, "module", "main")
    name = f"native_{module}_" + FUNCTION_ADDRESSES.get(original, original.removeprefix("func_"))
    functions = sorted(set(re.findall(r"\bfunc_[A-Za-z0-9_]+", draft)) - {original})
    data = sorted(set(re.findall(r"\bdata_[A-Za-z0-9_]+", draft)))
    declarations = "".join("extern " + SOURCE_RETURNS.get(function, {}).get("type", "u32") + " native_fn_" + function.removeprefix("func_") + "();\n" for function in functions)
    declarations += "".join("extern u8 native_data_" + item.removeprefix("data_") + "[];\n" for item in data)
    for function in functions:
        draft = re.sub(r"\b" + function + r"\b", "native_fn_" + function.removeprefix("func_"), draft)
    for item in data:
        draft = re.sub(r"\b" + item + r"\b", "native_data_" + item.removeprefix("data_"), draft)
    draft = re.sub(r"\b" + original + r"\b", name, draft)
    result = PRELUDE + declarations + draft
    if OPTIONS is not None and OPTIONS.direct_increments:
        from narrow_increments import canonical_byte_increments
        result, changes = canonical_byte_increments(result)
    if OPTIONS is not None and OPTIONS.typed_globals:
        from typed_global_fields import recover_global_records
        result, changes = recover_global_records(result)
    if len(result.splitlines()) > 500:
        raise ValueError("Recovered routine exceeds physical-line limit before refactoring")
    return result


def one(original):
    assembly, context = FUNCTION_INPUTS[original]
    if getattr(OPTIONS, "pointer_returns", False):
        from pointer_returns import memory_result_hints
        for function in memory_result_hints(assembly):
            context = context.replace("extern u32 " + function + "();", "extern u8 *" + function + "();")
    if OPTIONS.void:
        context = context.replace("extern u32 " + original + "();", "extern void " + original + "();")
    directory = WORK / "functions" / original
    directory.mkdir(parents=True, exist_ok=True)
    asm = directory / "input.s"
    ctx = directory / "context.c"
    asm.write_text(assembly)
    ctx.write_text(context)
    command = [matcher.sys.executable, str(M2C), "--target", "arm-mwcc-c", "--comment-style", "none",
               "--no-cache", "--valid-syntax", "--context", str(ctx),
               "-f", original, str(asm)]
    for enabled, option in ((OPTIONS.void, "--void"), (OPTIONS.descending_regs, "--descending-regs"), (OPTIONS.gotos_only, "--gotos-only")):
        if enabled:
            command.append(option)
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
        compilers = [None, ROOT / "tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe", ROOT / "tools/mwccarm/mwccarm/1.2/base/mwccarm.exe"] if OPTIONS.compiler_variants else [None]
        for compiler in compilers:
            for optimization, inline, speed in [(2, "off", False), (2, "noauto", False), (2, "off", True), (3, "off", True), (4, "off", True), (3, "off", False), (4, "off", False)]:
                records, matches = matcher.compare(source, OPTIONS.module, optimization, inline, speed, OPTIONS.thumb, compiler)
                item["attempts"].extend(records)
                if matches:
                    item["match"] = next(iter(matches.values()))[0]
                    break
            if "match" in item:
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
        compiler = ROOT / match["compilerPath"] if match.get("compilerPath") else None
        if compiler and matcher.sha(compiler.read_bytes()) != match["compilerSha256"]:
            raise ValueError("Accepted compiler changed")
        _, found = matcher.compare(source, report.get("module", "main"), flags[0][2:], flags[flags.index("-inline") + 1], "speed" in flags, "-thumb" in flags, compiler)
        if match["name"] not in found:
            raise ValueError("Accepted translated function stopped matching: " + match["name"])
        rebuilt = found[match["name"]][0]
        if rebuilt["outputSha256"] != match["outputSha256"]:
            raise ValueError("Accepted native code identity changed")
        accepted.append({**match, **rebuilt})
    return accepted


def main():
    global OPTIONS, WORK
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default="runtime01")
    parser.add_argument("--module", choices=("main", "ov000", "ov001", "ov002", "ov003", "ov005", "ov006", "ov007"), default="main")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--workers", type=int, choices=range(1, 4), default=3)
    parser.add_argument("--void", action="store_true")
    parser.add_argument("--descending-regs", action="store_true")
    parser.add_argument("--gotos-only", action="store_true")
    parser.add_argument("--word-args", action="store_true")
    parser.add_argument("--thumb", action="store_true")
    parser.add_argument("--abi-slots", action="store_true")
    parser.add_argument("--register-order", action="store_true")
    parser.add_argument("--compiler-variants", action="store_true")
    parser.add_argument("--direct-increments", action="store_true")
    parser.add_argument("--typed-globals", action="store_true")
    parser.add_argument("--stack-buffers", action="store_true")
    parser.add_argument("--pointer-returns", action="store_true")
    parser.add_argument("--source-returns", action="store_true")
    parser.add_argument("--min-bytes", type=int, default=100)
    parser.add_argument("--max-bytes", type=int, default=512)
    parser.add_argument("--start", type=lambda x: int(x, 0), default=0x02000800)
    parser.add_argument("--end", type=lambda x: int(x, 0), default=0x02020000)
    args = parser.parse_args()
    OPTIONS = args
    WORK = WORK / args.batch
    target = ROOT / f"evidence/matches/{args.module}-{args.batch}.json"
    if args.verify:
        report = json.loads(target.read_text())
        verified = verify(report)
        report["matches"] = verified
        report["nativeSymbols"] = {rel["symbol"]: rel["target"] for item in verified for rel in item["relocations"]}
        write(target, report)
        print({"verifiedFunctions": len(verified), "bytes": sum(item["bytes"] for item in verified)})
        return
    if target.exists():
        raise ValueError("Accepted batch exists; select a new batch name")
    inputs()
    from ledger_state import collect_matches
    from project import configuration
    accepted, _ = collect_matches(configuration()["romSha256"])
    mode = "thumb" if args.thumb else "arm"
    from recovery_ownership import reservation
    candidates = re.findall(r"^(\S+) kind:function\(" + mode + r",size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)", module_paths(args.module)[1].read_text(), re.M)
    originals = [name for name, size, address in candidates if args.start <= int(address, 0) < args.end and args.min_bytes <= int(size, 0) <= args.max_bytes and (args.module, mode, int(address, 0)) not in accepted and name in FUNCTION_INPUTS and (args.module != "main" or reservation(int(address, 0)) is None)][:args.limit]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for result in pool.map(one, originals):
            results.append(result)
            print(json.dumps({"function": result["nativeAlias"], "matched": "match" in result,
                              "failure": result.get("failure"), "exitCode": result.get("exitCode")}), flush=True)
    matches = []
    for item in results:
        if "match" not in item:
            continue
        old = item["match"]
        source = ROOT / f"src/runtime/{args.batch}/{old['name']}.c"
        if source.exists():
            raise ValueError("Refusing to overwrite accepted source: " + str(source))
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes((ROOT / item["draftSource"]).read_bytes())
        flags = old["compilerFlags"]
        compiler = ROOT / old["compilerPath"] if old.get("compilerPath") else None
        _, found = matcher.compare(source, args.module, int(flags[0][2:]), flags[flags.index("-inline") + 1], "speed" in flags, args.thumb, compiler)
        if old["name"] not in found:
            raise ValueError("Promoted source differs from exact draft")
        entry, code = found[old["name"]]
        binary_path, symbols_path, base = module_paths(args.module)
        binary = binary_path.read_bytes()
        address = int(entry["address"], 0)
        try:
            if args.module == "main":
                entry["oracle"] = matcher.oracle(entry, code, binary[address - base:address - base + entry["bytes"]])
            else:
                from reuse_overlay_c import bounded_oracle
                entry["oracle"] = bounded_oracle(entry, code, binary[address - base:address - base + entry["bytes"]])
        except Exception as error:
            entry["oracle"] = {"supported": False, "failure": f"{type(error).__name__}: {error}", "limitation": "Byte/relocation matching is established; native behavior requires a broader platform model"}
        matches.append(entry)
    report = {"schemaVersion": 1, "romSha256": matcher.sha((ROOT / "inputs/game.nds").read_bytes()),
              "module": args.module, "moduleInputSha256": matcher.sha(module_paths(args.module)[0].read_bytes()),
              "matches": matches, "nativeSymbols": {rel["symbol"]: rel["target"] for match in matches for rel in match["relocations"]},
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "parameterWordHypothesis": args.word_args,
              "argumentSlotRepairRequested": args.abi_slots,
              "registerDeclarationOrderRequested": args.register_order,
              "sourceReturnHypotheses": SOURCE_RETURNS,
              "limitations": ["Decompiler output is accepted only after complete native byte and relocation comparison", "Unsupported behavioral paths remain explicit", "Word-argument mode infers only unspecified 32-bit register parameter types; unknown local/aggregate types remain rejected", "Recovered source return declarations are caller-typing hypotheses rather than proof of historical prototypes; complete native byte and relocation gates still apply"]}
    write(ROOT / f"evidence/attempts/{args.module}-{args.batch}-drafts.json", results)
    write(target, report)
    print({"drafted": len(results), "matched": len(matches), "bytes": sum(item["bytes"] for item in matches)})


if __name__ == "__main__":
    main()
