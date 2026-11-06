import argparse, zipfile, uuid
import hashlib
import json
import os
import random
import re
import struct
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_INVALID
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
from overlay_oracle007 import seed_scalar, scalar_arguments, scalar_call, assert_scalar
from overlay_oracle007_objects import seed_objects, object_arguments, object_call, assert_objects, native_helpers
from overlay_oracle007_selection import seed_selection, selection_call, assert_selection
from overlay_oracle007_tables import seed_tables, table_arguments, table_call, assert_tables
from overlay_oracle007_manager import seed_manager, manager_call, assert_manager
from overlay_oracle007_tail import seed_tail, tail_arguments, tail_call, assert_tail
from overlay_oracle007_direction import seed_direction, direction_arguments, assert_direction
from overlay_oracle007_update import seed_update, update_call, assert_update
from overlay_oracle007_transition import seed_transition, assert_transition
from overlay_oracle007_transition_start import seed_transition_start, transition_start_arguments, assert_transition_start
from overlay_oracle007_sequence import seed_sequence, sequence_call, assert_sequence
from overlay_oracle007_flow import seed_flow, flow_call, assert_flow
from overlay_oracle002_objects import native_helpers002, seed_objects002, object_call002, assert_objects002
from overlay_oracle003_startup import seed_startup003, startup_arguments003, startup_call003, assert_startup003, native_helpers003, COUNTS_003, INDIRECT_003, MAIN_INDIRECT_003
WORK = ROOT / "work/overlay-recovery"
COMPILER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
ROM_HASH = "674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6"
COMPILER_PINS = {"tools/mwccarm/mwccarm/2.0/base/mwccarm.exe": "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880"}
PROCESSOR = None
OPTIMIZER_EXTRA = []
COUNTS_007 = {0x021D81D0: 512, 0x021D89C0: 48, 0x021D8BC0: 48, 0x021D7E1C: 320, 0x021D837C: 384, 0x021D9E68: 360, 0x021D9CCC: 1024, 0x021D9858: 1320, 0x021D76A0: 2200}
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]
def sha(data):
    return hashlib.sha256(data).hexdigest()
def immutable(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError("Immutable output collision: " + str(path))
    else:
        path.write_bytes(data)
def symbol_data(module):
    lookup, boundaries = {"_fflt": 0x02025A28, "_fdiv": 0x02025578, "_fgr": 0x0202537C, "_fmul": 0x02025AB8, "_fadd": 0x02024E0C, "_fsub": 0x02025CA4, "_ffix": 0x020259B4}, {}
    for current, path in [("main", ROOT / "config/arm9/symbols.txt"), (module, ROOT / f"config/arm9/overlays/{module}/symbols.txt")]:
        for line in path.read_text().splitlines():
            match = re.match(r"(\S+) .*?addr:(0x[0-9a-f]+)", line)
            if not match:
                continue
            name, address = match.group(1), int(match.group(2), 16)
            lookup[name] = address
            function = re.search(r"kind:function\((arm|thumb),size:(0x[0-9a-f]+)", line.replace("size=", "size:"))
            if current == module and function:
                boundaries[address] = {"name": name, "mode": function.group(1), "size": int(function.group(2), 16)}
    for address, spec in boundaries.items():
        lookup[f"native_{module}_{address:08x}"] = address
    return lookup, boundaries
def compile_compare(module, source, optimization=2, inline="off", processor=None, optimizer_extra=None, symbol_mode=None):
    compiler_hash = sha(COMPILER.read_bytes())
    compiler_path = str(COMPILER.relative_to(ROOT)).replace("\\", "/")
    if compiler_path not in COMPILER_PINS:
        archive_path = ROOT / "tools/mwccarm.zip"
        if not COMPILER.is_relative_to(ROOT / "tools/mwccarm") or sha(archive_path.read_bytes()) != "dc386e37b2176e960954a733de928337d9b7e7620b9e94228008c31774339ace":
            raise ValueError("Alternative compiler archive provenance differs")
        with zipfile.ZipFile(archive_path) as archive:
            member = str(COMPILER.relative_to(ROOT / "tools/mwccarm")).replace("\\", "/")
            COMPILER_PINS[compiler_path] = sha(archive.read(member))
    if compiler_hash != COMPILER_PINS[compiler_path]:
        raise ValueError("Compiler changed")
    lookup, boundaries = symbol_data(module)
    flags = json.loads((ROOT / "oracle/results.json").read_text())["compiler"]["flags"][:]
    flags[0] = f"-O{optimization}"
    flags[flags.index("-inline") + 1] = inline
    if symbol_mode:
        flags[flags.index("-sym") + 1] = symbol_mode
    if processor or PROCESSOR:
        flags[flags.index("-proc") + 1] = processor or PROCESSOR
    for modifier in OPTIMIZER_EXTRA if optimizer_extra is None else optimizer_extra:
        flags += ["-opt", modifier]
    output = WORK / "compiles" / (str(uuid.uuid4()) + ".o")
    output.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    command = [str(COMPILER), *flags, "-c", str(source), "-o", str(output)]
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=45)
    snapshot = WORK / "sources" / (sha(source.read_bytes()) + source.suffix)
    immutable(snapshot, source.read_bytes())
    report = {"source": str(source.relative_to(ROOT)), "sourceSnapshot": str(snapshot.relative_to(ROOT)), "sourceSha256": sha(source.read_bytes()), "compiler": compiler_path, "flags": flags, "command": command, "returncode": result.returncode, "stdout": result.stdout.decode(errors="replace"), "stderr": result.stderr.decode(errors="replace"), "functions": []}
    if result.returncode:
        return report, {}
    obj_hash = sha(output.read_bytes())
    stable = WORK / "objects" / (obj_hash + ".o")
    immutable(stable, output.read_bytes())
    report.update(object=str(stable.relative_to(ROOT)), objectSha256=obj_hash, compilerSha256=compiler_hash)
    native = (ROOT / f"extract/arm9_overlays/{module}.bin").read_bytes()
    compiled = {}
    with output.open("rb") as stream:
        elf = ELFFile(stream)
        for symbol in elf.get_section_by_name(".symtab").iter_symbols():
            match = re.fullmatch(rf"native_{module}_([0-9a-f]{{8}})", symbol.name)
            if not match or not isinstance(symbol["st_shndx"], int):
                continue
            address = int(match.group(1), 16)
            spec = boundaries[address]
            start = symbol["st_value"] & ~1
            raw = elf.get_section(symbol["st_shndx"]).data()[start:start + symbol["st_size"]]
            code = bytearray(raw)
            relocations = []
            unresolved = []
            for section in elf.iter_sections():
                if section["sh_type"] not in ("SHT_REL", "SHT_RELA") or section["sh_info"] != symbol["st_shndx"]:
                    continue
                table = elf.get_section(section["sh_link"])
                for rel in section.iter_relocations():
                    at = rel["r_offset"] - start
                    if not 0 <= at < len(code):
                        continue
                    target_name = table.get_symbol(rel["r_info_sym"]).name
                    original_name = re.sub(r"_alias\d+$", "", target_name)
                    if target_name not in lookup and original_name in lookup:
                        lookup[target_name] = lookup[original_name]
                    if target_name not in lookup:
                        unresolved.append(target_name)
                        continue
                    target = lookup[target_name]
                    value = struct.unpack_from("<I", code, at)[0]
                    kind = rel["r_info_type"]
                    addend = rel["r_addend"] if section["sh_type"] == "SHT_RELA" else value
                    if kind == 2:
                        replacement = (target + addend) & 0xFFFFFFFF
                    elif kind in (1, 28, 29):
                        if section["sh_type"] == "SHT_REL":
                            addend = (value & 0xFFFFFF) << 2
                            if addend & 0x2000000:
                                addend -= 0x4000000
                        displacement = target + addend - address - at
                        replacement = (value & 0xFF000000) | ((displacement >> 2) & 0xFFFFFF)
                    else:
                        raise ValueError("Unsupported relocation kind: " + str(kind))
                    struct.pack_into("<I", code, at, replacement)
                    relocations.append({"offset": at, "type": kind, "symbol": target_name, "target": hex(target), "addend": addend})
            expected = native[address - 0x021D7240:address - 0x021D7240 + spec["size"]]
            exact = bytes(code) == expected and not unresolved
            entry = {"name": symbol.name, "nativeAlias": spec["name"], "originalSymbol": spec["name"], "module": module, "mode": spec["mode"], "address": hex(address), "bytes": spec["size"], "size": spec["size"], "compiledBytes": len(code), "matchingBytes": sum(a == b for a, b in zip(code, expected)), "exactBytes": raw == expected, "exactAfterDeclaredRelocation": exact, "targetSha256": sha(expected), "outputSha256": sha(code), "relocations": relocations, "flags": flags, "compilerFlags": flags, "source": report["source"], "sourceSha256": report["sourceSha256"], "object": report["object"], "objectSha256": obj_hash, "compilerSha256": compiler_hash, "linked": False}
            entry["compiler"] = compiler_path
            if address == 0x021D7CF0:
                entry["unknowns"] = ["For selector values outside 0/1, the native branch continues with incoming register values. Caller preconditions are not established; uninitialized C locals are retained to reproduce this native sequence."]
            if module == "ov007" and address == 0x021D7E1C:
                entry["unknowns"] = ["Directional signs are uninitialized for selectors outside1..4, matching the native incoming-register behavior. Oracle coverage is restricted to the four established directions."]
            if module == "ov003" and address in {0x021D9634, 0x021D97F8, 0x021D9984}:
                entry["unknowns"] = ["Record pointers are uninitialized for selector values outside 0/1, preserving native incoming-register behavior; bounded oracle coverage uses established selectors 0/1."]
            if not exact:
                entry.update(nativeHex=expected.hex(), compiledHex=code.hex(), unresolvedRelocations=unresolved)
            else:
                compiled[symbol.name] = bytes(code)
            report["functions"].append(entry)
    return report, compiled
def execute(module, address, code, record, vector, argument_overrides=None):
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.mem_map(0x02000000, 0x400000)
    engine.mem_map(0x03000000, 0x20000)
    engine.mem_map(0x04000000, 0x2000)
    engine.mem_write(0x02000000, (ROOT / "extract/arm9/arm9.bin").read_bytes())
    engine.mem_write(0x021D7240, (ROOT / f"extract/arm9_overlays/{module}.bin").read_bytes())
    rng = random.Random(20261027 + address + vector)
    data = rng.randbytes(0x18000)
    engine.mem_write(0x03000000, data)
    engine.mem_write(0x04000000, rng.randbytes(0x2000))
    if module == "ov002":
        engine.mem_write(0x021DAEC0 + 12, struct.pack("<3I", 0x03001000, 0x03002000, 0x03003000))
    engine.mem_write(0x03003000 + 28, struct.pack("<I", 0x03004000))
    engine.mem_write(0x03001000 + 124, struct.pack("<I", rng.getrandbits(32)))
    engine.mem_write(0x03005000, struct.pack("<I", 0x03006000))
    engine.mem_write(0x03008000, struct.pack("<I", 0x03006000))
    engine.mem_write(0x03008004, struct.pack("<I", 0x03007000))
    engine.mem_write(0x03006004, struct.pack("<I", 0x03007000))
    engine.mem_write(0x03005002, struct.pack("<H", [0, 8, 16, 0xff7][vector % 4]))
    if module == "ov002":
        engine.mem_write(0x021DAEE8, struct.pack("<I", vector % 4))
        engine.mem_write(0x021DB274, struct.pack("<I", vector % 4))
        engine.mem_write(0x021DA541, bytes([vector % 2]))
        engine.mem_write(0x021DA544, bytes([vector % 2, (vector // 2) % 2]))
        engine.mem_write(0x021DB3C0, struct.pack("<2I", vector % 5, 13 if vector % 2 else 14))
        engine.mem_write(0x021DB21C, struct.pack("<I", vector % 9))
        engine.mem_write(0x021DB290, struct.pack("<I", vector % 5))
        engine.mem_write(0x021DB284, struct.pack("<4H", vector % 7, [0, 1, 6, 7, 12, 65535][vector % 6], vector % 9, [65535, 12, 7, 6, 1, 0][vector % 6]))
    if module == "ov007":
        engine.mem_write(0x021DA980, bytes(2400))
        engine.mem_write(0x021DA9A4, struct.pack("<I", 0x0300F000 if vector % 2 else 0))
        if address == 0x021D7C5C:
            engine.mem_write(0x021DA9B8, bytes([0xFF, 0, 1, 7, 127][vector % 5:vector % 5 + 1]))
            engine.mem_write(0x021DA9C0, struct.pack("<I", 0x0300F000 if vector % 2 else 0))
    engine.mem_write(0x03005002, struct.pack("<3H", [0, 1, 0x800, 0x801][vector % 4], 0, [0, 64, 128, 192][(vector // 4) % 4]))
    engine.mem_write(0x03007000, struct.pack("<I", vector % 3))
    scalar_context = seed_scalar(engine, address, vector) if module == "ov007" else {}
    object_context = seed_objects(engine, address, vector) if module == "ov007" else {}
    selection_context = seed_selection(engine, address, vector) if module == "ov007" else {}
    table_context = seed_tables(engine, address, vector) if module == "ov007" else {}
    manager_context = seed_manager(engine, address, vector) if module == "ov007" else {}
    tail_context = seed_tail(engine, address, vector) if module == "ov007" else {}
    direction_context = seed_direction(engine, address, vector) if module == "ov007" else {}
    update_context = seed_update(engine, address, vector) if module == "ov007" else {}
    transition_context = seed_transition(engine, address, vector) if module == "ov007" else {}
    transition_start_context = seed_transition_start(engine, address, vector) if module == "ov007" else {}
    sequence_context = seed_sequence(engine, address, vector) if module == "ov007" else {}
    flow_context = seed_flow(engine, address, vector) if module == "ov007" else {}
    objects002_context = seed_objects002(engine, address, vector) if module == "ov002" else {}
    startup003_context = seed_startup003(engine, address, vector) if module == "ov003" else {}
    gpu_before = {}
    if module == "ov007" and address in {0x021D7240, 0x021D7AE8}:
        for base in [0x04000000, 0x04001000]:
            gpu_before[base] = int.from_bytes(engine.mem_read(base, 4), "little")
            for offset in range(8, 16, 2):
                gpu_before[base + offset] = int.from_bytes(engine.mem_read(base + offset, 2), "little")
    engine.mem_write(address, code)
    callbacks = {int(item["target"], 16): item["symbol"] for item in record["relocations"] if item["type"] in (1, 28, 29) or item["type"] == 2 and item["symbol"].startswith(("func_", "native_"))}
    callbacks.update(startup003_context.get("callbacks", {}))
    executed_helpers = native_helpers(address) if module == "ov007" else native_helpers002(address) if module == "ov002" else native_helpers003(address) if module == "ov003" else {}
    if module == "ov007" and address in {0x021D9E68, 0x021D9CCC}:
        callbacks.update({target: name for name, (target, size) in executed_helpers.items()})
    for target, name in callbacks.items():
        if name not in executed_helpers:
            engine.mem_write(target, struct.pack("<I", 0xE12FFF1E))
    args = [vector % 8, [0, 1, 127, 255][vector % 4], rng.getrandbits(32), rng.getrandbits(32)]
    if module == "ov002" and address == 0x021D7850:
        table = (ROOT / f"extract/arm9_overlays/{module}.bin").read_bytes()[0x021DA57B - 0x021D7240:]
        args[0] = [127, 0xFFFFFFFF, *[int.from_bytes(table[index:index + 1], "little", signed=True) & 0xFFFFFFFF for index in range(0, 63, 3)]][vector % 23]
    if module == "ov002" and address in {0x021D789C, 0x021D7930, 0x021D7A50, 0x021D7BB8, 0x021D7C28, 0x021D7CF0, 0x021D7DC4, 0x021D7E64, 0x021D7F98}:
        args[0] = 0x0300A000
    if module == "ov002" and address == 0x021D7CF0:
        args[1] = [0, 1, 2, 0xffffffff][vector % 4]
    if module == "ov002" and address == 0x021D7E64:
        args[1] = vector % 4
        args[2] = 0x0300A800 if vector % 2 else 0
    if module == "ov002" and address == 0x021D7F98:
        args[2] = vector % 4
    if module == "ov002" and address == 0x021DA058:
        args[2] = 0x0300B000
    if module == "ov007" and address == 0x021D74E4:
        args[0] = [0, 1, 14, 15, 16, 0xFFFFFFFF][vector % 6]
    if module == "ov007" and address == 0x021D85E4:
        args[0] = 0x0300A000
    table_fields = {0x021D8634: (0x021DA5EC, 48, 4), 0x021D864C: (0x021DA5F0, 48, 4), 0x021D8664: (0x021DA5F4, 48, 4), 0x021D867C: (0x021DA5F8, 48, 2), 0x021D8694: (0x021DA5FA, 48, 2), 0x021D86AC: (0x021DA5FC, 48, 1), 0x021D86C4: (0x021DA610, 48, 1), 0x021D86DC: (0x021DA534, 12, 4), 0x021D86F4: (0x021DA538, 12, 4), 0x021D870C: (0x021DA53C, 12, 4), 0x021D873C: (0x021DA614, 48, 1), 0x021D8838: (0x021DA06C, 1, 1)}
    if module == "ov007" and address in table_fields:
        args[0] = vector % (16 if address == 0x021D8838 else 15)
    if module == "ov007" and address in {0x021D8724, 0x021D8754}:
        args[0] = vector % 15
        args[1] = [0, 1, 255, 256, 65535, 65536, 0xFFFFFFFF][vector % 7]
    if module == "ov007":
        scalar_arguments(address, vector, args)
        object_arguments(address, vector, args)
        table_arguments(address, vector, args)
        tail_arguments(address, vector, args)
        direction_arguments(address, vector, args)
        transition_start_arguments(address, vector, args)
    for index, value in (argument_overrides or {}).items():
        if index not in range(4) or not 0 <= value <= 0xFFFFFFFF:
            raise ValueError("Invalid bounded register argument override")
        args[index] = value
    if module == "ov003":
        startup_arguments003(address, vector, args)
    registers = args + [rng.getrandbits(32) for _ in range(9)] + [0x0301FF00, 0x04000000]
    engine.reg_write(UC_ARM_REG_CPSR, (rng.getrandbits(4) << 28) | 0x10)
    for register, value in zip(REGS, registers):
        engine.reg_write(register, value)
    calls, writes, invalid = [], [], []
    def hook(uc, location, size, user):
        if location in callbacks:
            name = callbacks[location]
            calls.append({"name": name, "args": [uc.reg_read(x) for x in REGS[:4]], "stack": bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 16)).hex()})
            if name in executed_helpers:
                return
            pointer_results = {"func_0205f98c": 0x03005000, "func_02049ad0": 0x03008000, "func_02049ae4": 0x03008000, "func_0202a634": 0x03005000, "func_0207f3b0": 0x03005000, "func_02063aa4": 0x03006000, "func_ov002_021da04c": 0x03007000, "func_ov002_021da040": 0x03007000}
            value = pointer_results.get(name, vector % 2 if name in {"func_02048f7c", "func_0202a818"} else 0)
            if name == "func_ov002_021d828c":
                count = struct.unpack("<I", bytes(uc.mem_read(0x021DAEE8, 4)))[0]
                uc.mem_write(0x021DAEE8, struct.pack("<I", max(0, count - 1)))
            if name == "func_02027400":
                value = [0, 15, 16][vector % 3]
            if name == "func_ov002_021da030":
                value = [0, 1, 2, 4][vector % 4]
            if name in {"func_0207e874", "func_0207f390", "func_02041814"}:
                value = vector % 2
            if name == "func_02064510":
                value = vector % 2
            if name == "func_0204518c":
                uc.mem_write(uc.reg_read(UC_ARM_REG_R0), struct.pack("<2I", 0x03009000, 32))
            if name == "func_0202a44c":
                value = 0x0300C000
            if module == "ov007" and name == "func_0203cc2c":
                value = 0x0300C000 if vector % 3 else 0
            if module == "ov007" and name in {"func_02040d18", "func_02040d5c"}:
                value = (0x0300D000 if name == "func_02040d18" else 0x0300E000) + (uc.reg_read(UC_ARM_REG_R1) & 0xFF) * 32
            if module == "ov007" and name in {"func_ov007_021d8838", "func_ov007_021d8634", "func_ov007_021d864c", "func_ov007_021d867c"}:
                value = vector % 15
            if module == "ov007":
                value = scalar_call(uc, address, name, value, scalar_context)
                value = object_call(address, name, value, object_context)
                value = selection_call(uc, address, name, value, selection_context)
                value = table_call(uc, address, name, value, table_context)
                value = manager_call(address, name, value, manager_context)
                value = tail_call(uc, address, name, value, tail_context)
                value = update_call(address, name, value, update_context)
                value = sequence_call(address, name, value, sequence_context)
                value = flow_call(address, name, value, flow_context)
            if module == "ov002":
                value = object_call002(uc, address, name, value, objects002_context)
            if module == "ov003":
                value = startup_call003(uc, address, name, value, startup003_context)
            uc.reg_write(UC_ARM_REG_R0, value)
    engine.hook_add(UC_HOOK_CODE, hook)
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, location, size, value, user: writes.append([location, size, value]))
    def invalid_access(uc, access, location, size, value, user):
        invalid.append({"address": hex(location), "pc": hex(uc.reg_read(UC_ARM_REG_PC)), "registers": [hex(uc.reg_read(x)) for x in REGS]})
        return False
    engine.hook_add(UC_HOOK_MEM_INVALID, invalid_access)
    try:
        engine.emu_start(address, 0x04000000, count=16384 if module == "ov002" and address == 0x021D838C else 4096)
    except Exception as failure:
        raise ValueError(str(failure) + " " + json.dumps(invalid)) from failure
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
        raise ValueError("Instruction bound reached before native return")
    if module == "ov002" and address == 0x021D8CE0 and args[0] < 4:
        expected = struct.unpack("<H", bytes(engine.mem_read(0x021DB284 + args[0] * 2, 2)))[0] // 6 * 6
        actual = struct.unpack("<I", bytes(engine.mem_read(0x03007004, 4)))[0]
        if actual != expected:
            raise ValueError("Selection setup did not preserve measured six-entry division behavior")
    if module == "ov007" and address == 0x021D85E4:
        if bytes(engine.mem_read(args[0], 16)) != bytes(engine.mem_read(0x021DA0F4, 16)):
            raise ValueError("Struct return did not copy its complete sixteen-byte value")
    if module == "ov007" and address == 0x021D7C5C:
        opened = vector % 2 == 0 and vector % 3 != 0
        expected_resource = 0x0300F000 if vector % 2 else 0x0300C000 if opened else 0
        if engine.reg_read(UC_ARM_REG_R0) != int(opened) or struct.unpack("<I", bytes(engine.mem_read(0x021DA9C0, 4)))[0] != expected_resource:
            raise ValueError("Secondary resource selection lost existing/open-failure/open-success behavior")
    if module == "ov007" and address in table_fields:
        base, stride, width = table_fields[address]
        expected = int.from_bytes(engine.mem_read(base + args[0] * stride, width), "little", signed=address == 0x021D8838) & 0xFFFFFFFF
        if engine.reg_read(UC_ARM_REG_R0) != expected:
            raise ValueError("Typed table field extraction differs from its independently addressed value")
    if module == "ov007" and address in {0x021D8724, 0x021D8754}:
        width, base = (1, 0x021DA614) if address == 0x021D8724 else (2, 0x021DA612)
        if int.from_bytes(engine.mem_read(base + args[0] * 48, width), "little") != args[1] & ((1 << (width * 8)) - 1):
            raise ValueError("Typed table field storage lost the measured byte/halfword truncation")
    if gpu_before:
        expected_gpu = dict(gpu_before)
        base = 0x04000000 if address == 0x021D7240 else 0x04001000
        control = (gpu_before[base] & 0xFFCFFFEF) | 0x10
        if address == 0x021D7240:
            control &= ~0x3F000000
            expected_gpu[base] = (control & ~0x1F00) | 0x1D00
            for index, mode, priority in [(0, 0x1090, 2), (2, 0x1220, 1), (3, 0x0E00, 0)]:
                expected_gpu[base + 8 + index * 2] = ((gpu_before[base + 8 + index * 2] & 0x43) | mode) & ~3 | priority
        else:
            expected_gpu[base] = (control & ~0x1F00) | 0x1600
            expected_gpu[base + 8] &= ~3
            for index, mode, priority in [(1, 0x94, 2), (2, 0x488, 1)]:
                expected_gpu[base + 8 + index * 2] = ((gpu_before[base + 8 + index * 2] & 0x43) | mode) & ~3 | priority
        for location, expected in expected_gpu.items():
            width = 4 if location in {0x04000000, 0x04001000} else 2
            if int.from_bytes(engine.mem_read(location, width), "little") != expected:
                raise ValueError("Display register fields differ from their independent mask/mode/priority model")
    if module == "ov007":
        assert_scalar(engine, address, args, calls, scalar_context)
        assert_objects(engine, address, args, calls, object_context)
        assert_selection(engine, address, calls, selection_context)
        assert_tables(engine, address, args, calls, table_context)
        assert_manager(engine, address, calls, manager_context)
        assert_tail(engine, address, args, calls, tail_context)
        assert_direction(engine, address, args, calls, direction_context)
        assert_update(engine, address, calls, update_context)
        assert_transition(engine, address, calls, transition_context)
        assert_transition_start(engine, address, calls, transition_start_context)
        assert_sequence(engine, address, calls, sequence_context)
        assert_flow(engine, address, calls, flow_context)
    if module == "ov002":
        assert_objects002(engine, address, args, calls, objects002_context)
    if module == "ov003":
        assert_startup003(engine, address, args, calls, startup003_context)
    return {"registers": [engine.reg_read(x) for x in REGS], "cpsr": engine.reg_read(UC_ARM_REG_CPSR), "calls": calls, "writes": writes, "memorySha256": sha(bytes(engine.mem_read(0x03000000, 0x20000)) + bytes(engine.mem_read(0x021DA500, 0x1200)))}
def oracle(module, entry, code):
    address = int(entry["address"], 16)
    if module == "ov004" and address in __import__("overlay_oracle004").SUPPORTED: return __import__("overlay_oracle004").oracle(entry,code)
    if module == "ov005" and address in {0x021D7338,0x021D738C}: return __import__("overlay_oracle005_registry").oracle(entry,code)
    native = (ROOT / f"extract/arm9_overlays/{module}.bin").read_bytes()[address - 0x021D7240:address - 0x021D7240 + entry["bytes"]]
    vectors = []
    count = COUNTS_007.get(address, 36) if module == "ov007" else 36
    if module == "ov003":
        count = COUNTS_003.get(address, 36)
    for vector in range(count):
        first = execute(module, address, native, entry, vector)
        second = execute(module, address, code, entry, vector)
        if first != second:
            raise ValueError("Isolated native/recompiled state mismatch")
        vectors.append({"index": vector, "stateSha256": sha(json.dumps(first, sort_keys=True).encode()), "calls": first["calls"], "writes": first["writes"]})
    result = {"passed": True, "vectors": len(vectors), "executions": len(vectors) * 2, "instructionLimit": 4096, "dependencyModel": "Relocated call targets are isolated deterministic stubs; external callee semantics are not claimed", "results": vectors}
    helpers = native_helpers(address) if module == "ov007" else native_helpers002(address) if module == "ov002" else native_helpers003(address) if module == "ov003" else {}
    if helpers:
        main = (ROOT / "extract/arm9/arm9.bin").read_bytes()
        overlay = (ROOT / f"extract/arm9_overlays/{module}.bin").read_bytes()
        result["executedNativeHelpers"] = [{"name": name, "address": hex(target), "bytes": size, "sha256": sha((main[target - 0x02000000:target - 0x02000000 + size] if target < 0x021D7240 else overlay[target - 0x021D7240:target - 0x021D7240 + size]))} for name, (target, size) in helpers.items()]
        result["dependencyModel"] = "Reported native helpers execute their original instructions; other relocated call targets are isolated deterministic stubs, whose external semantics are not claimed"
    if module == "ov002" and address == 0x021D838C:
        result["instructionLimit"] = 16384
    if module == "ov003" and address == 0x021D72D0:
        result["indirectCallbackTargets"] = {hex(target): name for target, name in INDIRECT_003.items()}
        result["callbackTableRowsExercised"] = [0]
        result["dependencyModel"] = "Relocated and reported indirect callback targets are isolated deterministic stubs; their external semantics are not claimed"
        result["limitations"] = ["Initialized callback rows1/2 contain null handlers; only active row0 is exercised, consistent with startup's current-index initialization."]
    if module == "ov003" and address == 0x021DA50C:
        result.update(indirectCallbackTargets={hex(target): name for target, name in MAIN_INDIRECT_003.items()}, callbackTableRowsExercised=list(range(8)), limitations=["Callback row8 contains null handlers; bounded coverage uses the eight initialized rows with deterministic external callbacks."])
    return result
def filter_source(text, names):
    matches = list(re.finditer(r"(?m)^[A-Za-z_][\w *]*?\b(native_ov\d{3}_[0-9a-f]{8})\s*\([^;]*?\)\s*\{", text))
    prefix = text[:matches[0].start()]
    bodies = []
    for match in matches:
        depth, end = 1, match.end()
        while depth:
            depth += (text[end] == "{") - (text[end] == "}")
            end += 1
        if match.group(1) in names:
            bodies.append(text[match.start():end])
    return prefix.rstrip() + "\n\n" + "\n\n".join(bodies) + "\n"
def main():
    global COMPILER, PROCESSOR, OPTIMIZER_EXTRA
    parser = argparse.ArgumentParser()
    parser.add_argument("module")
    parser.add_argument("source")
    parser.add_argument("--optimization", default="2")
    parser.add_argument("--inline", default="off")
    parser.add_argument("--search", action="store_true")
    parser.add_argument("--publish")
    parser.add_argument("--include", nargs="+")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--compiler", default="tools/mwccarm/mwccarm/2.0/base/mwccarm.exe")
    parser.add_argument("--processor")
    parser.add_argument("--optimizer-modifier", action="append", default=[])
    args = parser.parse_args()
    source = (ROOT / args.source).resolve()
    COMPILER = (ROOT / args.compiler).resolve()
    PROCESSOR = args.processor
    OPTIMIZER_EXTRA = args.optimizer_modifier
    if not re.fullmatch(r"ov00[0-7]", args.module) or not source.is_relative_to(ROOT):
        raise ValueError("Invalid module/source")
    if sha((ROOT / "inputs/game.nds").read_bytes()) != ROM_HASH:
        raise ValueError("Unexpected ROM namespace")
    WORK.mkdir(parents=True, exist_ok=True)
    configurations = [(args.optimization, args.inline)]
    if args.search:
        configurations += [(x, inline) for x in ["2", "2,p", "2,s", "1", "1,p", "3", "3,p", "4", "4,p", "0"] for inline in ["off", "noauto"] if (x, inline) not in configurations]
    attempts = []
    best, codes = {}, {}
    for optimization, inline in configurations:
        report, current = compile_compare(args.module, source, optimization, inline)
        attempts.append(report)
        for entry in report["functions"]:
            if args.include and entry["name"] not in args.include:
                continue
            if entry["exactAfterDeclaredRelocation"] and entry["name"] not in best:
                best[entry["name"]] = entry
                codes[entry["name"]] = current[entry["name"]]
    for name, entry in list(best.items()):
        try:
            entry["oracle"] = oracle(args.module, entry, codes[name])
        except Exception as failure:
            entry["oracle"] = {"passed": False, "failure": str(failure)}
    summary = {"module": args.module, "source": args.source, "matches": [{"name": name, "bytes": entry["bytes"], "oraclePassed": entry["oracle"]["passed"]} for name, entry in best.items()], "attemptedFunctions": len(attempts[0]["functions"]), "attempts": len(attempts)}
    history = {"schemaVersion": 1, "date": "2026-10-27", "romSha256": ROM_HASH, "module": args.module, "attempts": attempts, "summary": summary}
    immutable(WORK / "attempts" / (sha(json.dumps(history, sort_keys=True).encode()) + ".json"), json.dumps(history, indent=2).encode())
    if args.publish:
        accepted = {name for name, entry in best.items() if entry["oracle"]["passed"]}
        if not accepted:
            raise ValueError("No validated source functions to publish")
        text = filter_source(source.read_text(), accepted)
        if len(text.splitlines()) > 500:
            raise ValueError("Accepted source exceeds 500 lines")
        frozen = ROOT / f"src/overlays/{args.module}_{args.publish}_{sha(text.encode())[:12]}{source.suffix}"
        immutable(frozen, text.encode())
        final, final_code = compile_compare(args.module, frozen, args.optimization, args.inline)
        if {entry["name"] for entry in final["functions"]} != accepted:
            raise ValueError("Source filtering omitted an accepted function")
        if any(not entry["exactAfterDeclaredRelocation"] for entry in final["functions"]):
            raise ValueError("Source filtering changed a compiler match")
        for entry in final["functions"]:
            entry["oracle"] = oracle(args.module, entry, final_code[entry["name"]])
            entry["state"] = "function-matched"
        report = {"schemaVersion": 1, "date": "2026-10-27", "romSha256": ROM_HASH, "module": args.module, "source": final["source"], "sourceSha256": final["sourceSha256"], "compilerSha256": final["compilerSha256"], "matches": final["functions"], "nativeSymbols": {item["symbol"]: item["target"] for entry in final["functions"] for item in entry["relocations"]}, "wholeModuleLinked": False, "wholeRomMatched": False}
        destination = ROOT / f"evidence/matches/overlays-{args.module}-{final['sourceSha256'][:12]}.json"
        immutable(destination, json.dumps(report, indent=2).encode())
        summary["published"] = str(destination.relative_to(ROOT))
        summary["publishedFunctions"] = len(final["functions"])
    print(json.dumps(summary, indent=2))
    if args.verify and (not best or len(best) != len(attempts[0]["functions"]) or any(not entry["oracle"]["passed"] for entry in best.values())):
        raise SystemExit(1)
if __name__ == "__main__":
    main()
