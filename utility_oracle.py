import json
import random
import struct
from functools import lru_cache
import utility_runtime
import match_lowlevel
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR


@lru_cache(maxsize=1)
def context():
    return utility_runtime.derive()


def execute(code, spec, vector, allowed_callees):
    layout, files = context()
    rng = random.Random(20261027 + spec["address"] + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for address, size in [(0x01FF8000, 0x8000), (0x02000000, 0x800000), (0x03000000, 0x20000),
                          (0x037F8000, 0x18000), (0x04000000, 0x2000), (0x05000000, 0x1000)]:
        engine.mem_map(address, size)
    snapshots = []
    for module in layout["modules"]:
        if module["processor"] != spec["processor"]:
            continue
        data = bytes(files[utility_runtime.ROOT / module["binary"]])
        engine.mem_write(int(module["base"], 0), data)
        snapshots.append((int(module["base"], 0), len(data)))
        if module["bssBytes"]:
            engine.mem_write(int(module["bssStart"], 0), bytes(module["bssBytes"]))
            snapshots.append((int(module["bssStart"], 0), module["bssBytes"]))
    engine.mem_write(0x03000000, rng.randbytes(0x20000))
    engine.mem_write(0x04000000, rng.randbytes(0x2000))
    engine.mem_write(spec["address"], code)
    snapshots.extend([(0x03000000, 0x20000), (0x04000000, 0x2000)])
    registers = [rng.getrandbits(32) for _ in match_lowlevel.REGISTERS]
    registers[0] = vector % 4
    registers[3] = [0, 0x80000000, 0x81400001, rng.getrandbits(32)][vector % 4]
    registers[-2:] = [0x0301FFF0, 0x05000000]
    if spec.get("oracleShape", {}).get("argumentPointer"):
        registers[0] = 0x03002000
    for index in spec.get("oracleShape", {}).get("argumentPointerRegisters", []):
        registers[index] = 0x03002000 + index * 0x1000
    for index, values in spec.get("oracleShape", {}).get("argumentValues", {}).items():
        registers[int(index)] = values[vector % len(values)]
    flags = rng.getrandbits(4) << 28 | 0x13 | (0x80 if vector % 2 else 0)
    engine.reg_write(UC_ARM_REG_CPSR, flags | (0x20 if spec["mode"] == "thumb" else 0))
    for register, value in zip(match_lowlevel.REGISTERS, registers):
        engine.reg_write(register, value)
    writes, calls, visited = [], [], set()
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value]))
    def intercept(uc, address, size, user):
        if spec["address"] <= address < spec["address"] + len(code):
            visited.add(address)
            return
        if address in allowed_callees:
            calls.append({"address": hex(address), "arguments": [uc.reg_read(register) for register in match_lowlevel.REGISTERS[:4]],
                          "cpsr": uc.reg_read(UC_ARM_REG_CPSR)})
        if not any(first <= address < first + length for first, length in allowed_callees.items()):
            raise ValueError("Utility unit executed a native callee outside its explicit oracle scope")
    engine.hook_add(UC_HOOK_CODE, intercept)
    engine.emu_start(spec["address"] | int(spec["mode"] == "thumb"), 0x05000000, count=1000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000:
        raise ValueError("Utility unit did not return within the native instruction bound")
    return {"registers": [engine.reg_read(register) for register in match_lowlevel.REGISTERS], "cpsr": engine.reg_read(UC_ARM_REG_CPSR),
            "writes": writes, "nativeCalleeCalls": calls, "visitedInstructions": sorted(visited),
            "memoryHashes": [utility_runtime.sha(bytes(engine.mem_read(first, size))) for first, size in snapshots]}


def oracle(code, spec):
    layout, files = context()
    if utility_runtime.sha(utility_runtime.INPUT.read_bytes()) != layout["inputSha256"]:
        raise ValueError("Utility oracle input changed during this run")
    module = next(module for module in layout["modules"] if module["id"] == spec["module"])
    binary = bytes(files[utility_runtime.ROOT / module["binary"]])
    offset = spec["address"] - spec["base"]
    native = binary[offset:offset + spec["bytes"]]
    allowed = {0x0200A64C: 20, 0x0200A660: 24} if spec["processor"] == "arm9" else {}
    results, visited = [], set()
    helper_calls, called_helpers = 0, set()
    for vector in range(24):
        expected, actual = execute(native, spec, vector, allowed), execute(code, spec, vector, allowed)
        if expected != actual:
            raise ValueError("Utility native and compiled unit effects differ")
        helper_calls += len(expected["nativeCalleeCalls"]) * 2
        called_helpers.update(int(call["address"], 0) for call in expected["nativeCalleeCalls"])
        visited.update(expected["visitedInstructions"])
        results.append({"vector": vector, "stateSha256": utility_runtime.sha(json.dumps(expected, sort_keys=True).encode()),
                        "nativeCalleeCalls": expected["nativeCalleeCalls"]})
    main = next(module for module in layout["modules"] if module["id"] == "utility-child-arm9-main")
    main_binary = bytes(files[utility_runtime.ROOT / main["binary"]])
    return {"vectors": 24, "nativeAndRecompiledCalls": 48, "nativeHelperCalls": helper_calls,
            "verifiedReturn": True, "instructionLimit": 1000, "records": results,
            "functionInstructionAddressesVisited": [hex(address) for address in sorted(visited)],
            "nativeHelperInputs": [{"program": utility_runtime.PROGRAM, "processor": "arm9", "module": main["id"],
                                    "address": hex(address), "bytes": size,
                                    "sha256": utility_runtime.sha(main_binary[address - int(main["base"], 0):address - int(main["base"], 0) + size])}
                                   for address, size in allowed.items() if address in called_helpers],
            "inputShape": spec.get("oracleShape", {"kind": "DMA", "channelValues": [0, 1, 2, 3]}),
            "limitations": ["Argument 0 uses bounded values 0 through 3 or a mapped scratch pointer when explicitly declared; both initial interrupt-mask states are used",
                            "When reached, whitelisted native interrupt-mask helpers execute in Unicorn supervisor mode; unused helpers receive no execution or source credit",
                            "MMIO is isolated synthetic memory; actual DMA transfers, IRQ delivery and physical aliasing are not modeled",
                            "Registers R0-R12/SP/LR, CPSR, ordered writes, native callee arguments and initialized memory are compared"]}
