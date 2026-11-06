import json
import re
from pathlib import Path
import match_lowlevel
from utility_abi import argument_hints
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from capstone.arm import ARM_OP_MEM, ARM_REG_PC

ROOT = Path(__file__).resolve().parent


def infer(names):
    manifest = json.loads((ROOT / "provenance/seed-manifest.json").read_text())
    modules = {module["name"]: module for module in manifest["modules"]}
    results = {}
    for name in names:
        match = re.fullmatch(r"func_(ov\d+)_[0-9a-f]{8}", name)
        if not match:
            continue
        module = modules[match[1]]
        binary = (ROOT / module["binary"]).read_bytes()
        if match_lowlevel.sha(binary) != module["sha256"]:
            raise ValueError("Qualified overlay leaf native module changed")
        symbols = (ROOT / f"config/arm9/overlays/{match[1]}/symbols.txt").read_text()
        boundary = re.search(r"^" + name + r" kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)$", symbols, re.M)
        if not boundary or int(boundary[2], 0) > 64:
            continue
        mode, size, address = boundary[1], int(boundary[2], 0), int(boundary[3], 0)
        base = int(module["base"], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if mode == "thumb" else CS_MODE_ARM)
        decoder.detail = True
        instructions = list(decoder.disasm(binary[address - base:address - base + size], address))
        pools = {(((instruction.address + 4) & ~3) if mode == "thumb" else instruction.address + 8) + operand.mem.disp
                 for instruction in instructions for operand in instruction.operands if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC}
        instructions = [instruction for instruction in instructions if not any(location <= instruction.address < location + 4 for location in pools)]
        if not instructions or not (instructions[-1].mnemonic == "bx" and instructions[-1].op_str == "lr" or instructions[-1].mnemonic.startswith(("pop", "ldm")) and "pc" in instructions[-1].op_str):
            continue
        if any(instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP) and not (instruction.mnemonic == "bx" and instruction.op_str == "lr" or instruction.mnemonic.startswith(("pop", "ldm")) and "pc" in instruction.op_str) for instruction in instructions):
            continue
        results[name] = argument_hints([{"address": address, "instructions": instructions}])[0][address]
    return results
