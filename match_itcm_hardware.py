import hashlib
import json
import os
import random
import struct
import subprocess
import sys
from pathlib import Path
import match_lowlevel as common

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR

ASSEMBLER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe"
EXPECTED = "e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c"
SPECS = {
    0x01FF8000: (88, "IRQ dispatch directly reads/writes interrupt MMIO and tail-dispatches through an IRQ callback table with a special continuation; a conventional C function ABI does not describe its entry/exit contract"),
    0x01FF8058: (348, "IRQ scheduler context switch uses privileged CPSR/SPSR mode changes and user-bank LDM/STM transfers; these operations require assembly rather than ordinary C"),
    0x01FF81E8: (204, "Restart handoff performs interprocessor MMIO polling, clears fixed hardware handoff ranges, restores a register block and branches into a new execution context")
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def irq_run(code, registers, mask, enabled, requested, seed):
    rng = random.Random(seed)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for location, size in [(0x01FF8000, 0x8000), (0x027E0000, 0x1000), (0x03000000, 0x20000), (0x04000000, 0x1000)]:
        engine.mem_map(location, size)
    engine.mem_write(0x01FF8000, code)
    engine.mem_write(0x0301F000, rng.randbytes(0x1000))
    engine.mem_write(0x027E0000, struct.pack("<32I", *[0x03001000 + i * 16 for i in range(32)]))
    for location, value in [(0x04000208, enabled), (0x04000210, mask), (0x04000214, requested)]:
        engine.mem_write(location, struct.pack("<I", value))
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for register, value in zip(common.REGISTERS, registers):
        engine.reg_write(register, value)
    writes, calls, instructions = [], [], []
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value]))
    def intercept(uc, address, size, user):
        instructions.append(address)
        if 0x03001000 <= address < 0x03001200:
            calls.append({"callbackIndex": (address - 0x03001000) // 16,
                          "arguments": [uc.reg_read(register) for register in common.REGISTERS[:4]],
                          "continuation": hex(uc.reg_read(UC_ARM_REG_LR))})
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == 0x01FF8058:
            stack = uc.reg_read(UC_ARM_REG_SP)
            target = struct.unpack("<I", bytes(uc.mem_read(stack, 4)))[0]
            uc.reg_write(UC_ARM_REG_SP, stack + 4)
            uc.reg_write(UC_ARM_REG_PC, target)
    engine.hook_add(UC_HOOK_CODE, intercept)
    engine.emu_start(0x01FF8000, 0x04000000, count=1000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
        raise ValueError("IRQ dispatch did not reach bounded continuation")
    pending = mask & requested
    expected = (pending & -pending).bit_length() - 1
    if enabled and pending:
        if len(calls) != 1 or calls[0]["callbackIndex"] != expected or calls[0]["continuation"] != "0x1ff8058":
            raise ValueError("IRQ callback selection differs from measured bit-scan behavior")
    elif calls:
        raise ValueError("IRQ callback executed without an enabled pending bit")
    return {"registers": [engine.reg_read(register) for register in common.REGISTERS],
            "cpsr": engine.reg_read(UC_ARM_REG_CPSR), "writes": writes, "calls": calls,
            "stackSha256": sha(bytes(engine.mem_read(0x0301F000, 0x1000))),
            "mmioSha256": sha(bytes(engine.mem_read(0x04000200, 0x20))),
            "visitedAddresses": sorted(set(instructions))}


def irq_oracle(native, rebuilt):
    rng = random.Random(20261027)
    records = []
    for index in range(64):
        registers = [rng.getrandbits(32) for _ in common.REGISTERS]
        registers[-2:] = [0x0301FFF0, 0x04000000]
        mask = [0, 1, 0xFFFFFF, 1 << (index % 24), rng.getrandbits(24)][index % 5]
        pending = [0, 1, 0xFFFFFF, 1 << (index % 24), rng.getrandbits(24)][(index // 5) % 5]
        enabled = index % 3 != 0
        first = irq_run(native, registers, mask, enabled, pending, index)
        second = irq_run(rebuilt, registers, mask, enabled, pending, index)
        if first != second:
            raise ValueError("IRQ dispatch native/rebuilt effects differ")
        records.append({"mask": hex(mask), "pending": hex(pending), "enabled": enabled,
                        "stateSha256": sha(json.dumps(first, sort_keys=True).encode()),
                        "calls": first["calls"], "visitedAddresses": first["visitedAddresses"]})
    return {"vectors": len(records), "nativeAndRecompiledCalls": 2 * len(records), "instructionLimit": 1000,
            "verifiedReturn": True, "records": records,
            "limitations": ["MMIO uses an isolated RAM model; no physical interrupt controller behavior is asserted", "Synthetic callback and scheduler continuation contracts are used; the scheduler itself is tested separately"]}


def main():
    if sha(ASSEMBLER.read_bytes()) != EXPECTED:
        raise ValueError("Pinned hardware assembler differs")
    binary = (ROOT / "extract/arm9/itcm.bin").read_bytes()
    if sha(binary) != "69b4ab1dc8c4f9c05388bbcc456ba6037fd8f09ab774d65a3eb8adc130e1c1fb":
        raise ValueError("Measured ITCM bytes changed")
    work = ROOT / "work/lowlevel-recovery/hardware"
    work.mkdir(parents=True, exist_ok=True)
    flags = ["-proc", "arm5TE", "-c"]
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    matches, attempts = [], []
    for address, (size, justification) in SPECS.items():
        name = f"native_itcm_{address:08x}"
        source = ROOT / f"src/itcm/hardware/{name}.s"
        obj = work / (name + ".o")
        command = [str(ASSEMBLER), *flags, str(source), "-o", str(obj)]
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=30)
        attempt = {"command": command, "exitCode": result.returncode,
                   "stdout": result.stdout.decode(errors="replace"), "stderr": result.stderr.decode(errors="replace")}
        attempts.append(attempt)
        if result.returncode:
            continue
        object_hash = sha(obj.read_bytes())
        stable = work / (object_hash + ".o")
        if not stable.exists():
            stable.write_bytes(obj.read_bytes())
        relocations = []
        with obj.open("rb") as stream:
            elf = ELFFile(stream)
            symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == name)
            code = bytearray(elf.get_section(symbol["st_shndx"]).data())
            for section in elf.iter_sections():
                if section["sh_type"] not in ("SHT_RELA", "SHT_REL") or section["sh_info"] != symbol["st_shndx"]:
                    continue
                table = elf.get_section(section["sh_link"])
                for rel in section.iter_relocations():
                    target_name = table.get_symbol(rel["r_info_sym"]).name
                    target = common.symbol_address(target_name)
                    offset, kind = rel["r_offset"], rel["r_info_type"]
                    value = struct.unpack_from("<I", code, offset)[0]
                    addend = rel["r_addend"] if section["sh_type"] == "SHT_RELA" else value
                    if kind == 2:
                        value = target + addend
                    elif kind in (1, 28, 29):
                        if section["sh_type"] == "SHT_REL":
                            addend = (value & 0xFFFFFF) << 2
                            if addend & 0x2000000:
                                addend -= 0x4000000
                        value = (value & 0xFF000000) | (((target + addend - address - offset) >> 2) & 0xFFFFFF)
                    else:
                        raise ValueError("Unsupported hardware relocation: " + str(kind))
                    struct.pack_into("<I", code, offset, value)
                    relocations.append({"offset": offset, "type": kind, "symbol": target_name, "target": hex(target), "addend": addend})
        native = binary[address - 0x01FF8000:address - 0x01FF8000 + size]
        matched = bytes(code) == native
        entry = {"name": name, "module": "itcm", "processor": "arm9", "mode": "arm", "address": hex(address),
                 "bytes": size, "compiledBytes": len(code), "matchingBytes": sum(a == b for a, b in zip(native, code)),
                 "exactAfterDeclaredRelocation": matched, "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source.read_bytes()),
                 "object": stable.relative_to(ROOT).as_posix(), "objectSha256": object_hash,
                 "compilerSha256": EXPECTED, "assemblerSha256": EXPECTED, "compilerFlags": flags,
                 "targetSha256": sha(native), "outputSha256": sha(code), "nativeAlias": f"func_{address:08x}",
                 "sectionIndex": symbol["st_shndx"], "sectionOffset": symbol["st_value"], "relocations": relocations,
                 "reconstructionKind": "justified-hardware-assembly", "assemblyJustification": justification, "linked": False}
        attempt["comparison"] = entry
        if matched:
            if address == 0x01FF8000:
                entry["oracle"] = irq_oracle(native, bytes(code))
            else:
                entry["oracle"] = {"supported": False, "reason": "Requires a privileged banked-register and interprocessor handoff model", "limitation": "Only complete byte and relocation equality is currently established"}
            matches.append(entry)
    report = {"schemaVersion": 1, "romSha256": sha((ROOT / "inputs/game.nds").read_bytes()), "module": "itcm",
              "moduleInputSha256": sha(binary), "matches": matches, "attempts": attempts,
              "nativeSymbols": {rel["symbol"]: rel["target"] for entry in matches for rel in entry["relocations"]},
              "wholeModuleLinked": False, "sourceReconstructionComplete": False}
    target = ROOT / "evidence/matches/itcm-hardware.json"
    target.write_text(json.dumps(report, indent=2) + "\n")
    print({"matched": len(matches), "bytes": sum(entry["bytes"] for entry in matches), "failed": len(SPECS) - len(matches)})
    if len(matches) != len(SPECS):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
