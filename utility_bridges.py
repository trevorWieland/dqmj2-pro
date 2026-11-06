import json
import random
import struct
from pathlib import Path
import utility_runtime
import match_lowlevel
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR

ROOT = Path(__file__).resolve().parent
PATTERN = bytes.fromhex("7847c04604f01fe5")


def execute(binary, address, target, vector):
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.mem_map(0x02000000, 0x800000)
    engine.mem_map(0x037F8000, 0x18000)
    engine.mem_map(0x03000000, 0x20000)
    engine.mem_write(address, binary)
    rng = random.Random(20261027 + address + vector)
    flags = rng.getrandbits(4) << 28 | 0x30
    registers = [rng.getrandbits(32) for _ in match_lowlevel.REGISTERS]
    registers[-2] = 0x0301FFF0
    engine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(match_lowlevel.REGISTERS, registers):
        engine.reg_write(register, value)
    writes, visited = [], []
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, location, size, value, user: writes.append([location, size, value]))
    def intercept(uc, location, size, user):
        visited.append(location)
        if location == target:
            uc.emu_stop()
    engine.hook_add(UC_HOOK_CODE, intercept)
    engine.emu_start(address | 1, 0, count=6)
    actual = [engine.reg_read(register) for register in match_lowlevel.REGISTERS]
    if engine.reg_read(UC_ARM_REG_PC) != target or actual != registers or engine.reg_read(UC_ARM_REG_CPSR) != flags & ~0x20 or writes or visited != [address, address + 4, target]:
        raise ValueError("Utility bridge does not preserve native registers/flags while switching from Thumb into the measured ARM target")
    return utility_runtime.sha(json.dumps({"registers": actual, "cpsr": engine.reg_read(UC_ARM_REG_CPSR), "visited": visited}, sort_keys=True).encode())


def derive(test=False):
    layout, files = utility_runtime.derive()
    entries = []
    for module in layout["modules"]:
        binary = bytes(files[ROOT / module["binary"]])
        base = int(module["base"], 0)
        for offset in range(0, len(binary) - 11, 4):
            if binary[offset:offset + 8] != PATTERN:
                continue
            target = struct.unpack_from("<I", binary, offset + 8)[0]
            destination = next((candidate for candidate in layout["modules"] if candidate["processor"] == module["processor"] and
                                int(candidate["base"], 0) <= target < int(candidate["runtimeEnd"], 0)), None)
            if target % 4 or destination is None:
                raise ValueError("Utility interworking bridge has an unqualified or unaligned ARM target")
            address = base + offset
            entry = {"program": utility_runtime.PROGRAM, "processor": module["processor"], "module": module["id"],
                     "id": module["id"] + ":linkage:" + hex(address),
                     "address": hex(address), "bytes": 12, "sha256": utility_runtime.sha(binary[offset:offset + 12]),
                     "inputModuleSha256": module["sha256"], "entryMode": "thumb", "armInteriorEntry": hex(address + 4),
                     "targetModule": destination["id"], "targetAddress": hex(target), "targetMode": "arm",
                     "targetId": utility_runtime.PROGRAM + "::" + module["processor"] + "::" + destination["id"] + "::" + hex(target) + "::arm",
                     "instructionStructure": [{"offset": 0, "mode": "thumb", "instruction": "bx pc"},
                                              {"offset": 2, "mode": "thumb", "instruction": "mov r8, r8", "role": "unexecuted alignment NOP"},
                                              {"offset": 4, "mode": "arm", "instruction": "ldr pc, [pc, #-4]"}],
                     "literal": {"offset": 8, "value": hex(target)}, "kind": "measured-mixed-mode-linkage-unit",
                     "sourceReconstructed": False, "linkerRegenerated": False,
                     "analysisAliases": [{"address": hex(address), "mode": "thumb"}, {"address": hex(address + 4), "mode": "arm"}]}
            entry["modeSegments"] = [{"offset": first, "bytes": size, "mode": mode, "role": role,
                                      "sha256": utility_runtime.sha(binary[offset + first:offset + first + size])}
                                     for first, size, mode, role in [(0, 2, "thumb", "Thumb entry"), (2, 2, "thumb", "unexecuted alignment NOP"),
                                                                     (4, 4, "arm", "ARM interior entry"), (8, 4, "data", "ARM target pointer")]]
            if test:
                entry["oracle"] = {"nativeVectors": 16, "stateSha256": [execute(binary[offset:offset + 12], address, target, vector) for vector in range(16)],
                                   "registersAndFlagsPreserved": True, "switchesThumbToArm": True, "nativeTargetNotExecuted": True}
            entries.append(entry)
    return {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
            "runtimeMappingCanonical": True, "bridges": entries, "sourceMatchedBytes": 0,
            "linkageBytes": sum(entry["bytes"] for entry in entries), "unresolvedExecutableBytes": sum(entry["bytes"] for entry in entries),
            "ordinaryFunctionCredit": 0,
            "limitations": ["Structural and execution evidence identifies linkage units; historical original linker attribution is not asserted",
                            "The 2-byte Thumb and 4-byte ARM analysis entries are aliases within one 12-byte unit, with one actual pointer word",
                            "Only native bridge execution to the target boundary is tested; no target routine or reconstructed unit execution is credited",
                            "Future source/linker regeneration must use qualified target symbols and prove the complete native unit bytes"]}


def main():
    report = derive(True)
    output = ROOT / "evidence/utility/interworking-bridges.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print({"bridges": len(report["bridges"]), "nativeSpanBytes": sum(entry["bytes"] for entry in report["bridges"]),
           "nativeOnlyVectors": sum(entry["oracle"]["nativeVectors"] for entry in report["bridges"]), "sourceCredit": 0})


if __name__ == "__main__":
    main()
