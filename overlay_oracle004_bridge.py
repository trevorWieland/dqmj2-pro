import json
import random
import struct

import audit_overlay004 as audit
import dsprot128
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_R0,
    UC_ARM_REG_R4,
    UC_ARM_REG_R10,
    UC_ARM_REG_R12,
    UC_ARM_REG_SP,
)

ADDRESS = 0x021D80EC
CONTEXT_FUNCTIONS = {ADDRESS, 0x021D7E24, 0x021D7F54, 0x021D8014}


def cache_operations(image):
    result = {}
    for start, size in [(0x021D7E24, 304), (0x021D7F54, 192), (0x021D8014, 216)]:
        for address in range(start, start + size, 4):
            word = struct.unpack_from("<I", image, address - audit.BASE)[0]
            if word & 0x0F100010 == 0x0E000010 and word >> 8 & 15 == 15:
                result[address] = (
                    (word >> 21) & 7,
                    (word >> 16) & 15,
                    word & 15,
                    (word >> 5) & 7,
                    (word >> 12) & 15,
                )
    return result


def expected_cache_pass():
    commands = []
    for segment in range(4):
        for index in range(0, 0x400, 32):
            commands.append((0, 7, 10, 4, 0))
            commands.append((0, 7, 14, 2, (segment << 30) | index))
    commands += [(0, 7, 5, 0, 0), (0, 7, 10, 4, 0)]
    return commands


def expected_cache_commands():
    return expected_cache_pass() * 2


class Machine(audit.Machine):
    def __init__(self, image, bss_size, seed, operations):
        super().__init__(image, bss_size, seed)
        self.operations = operations
        self.commands = []
        self.frames = []
        self.target = None
        self.arguments = None

    def registers(self, first, count):
        return [self.engine.reg_read(first + index) for index in range(count)]

    def step(self, engine, address, size, user):
        super().step(engine, address, size, user)
        if address in self.operations:
            op1, crn, crm, op2, register = self.operations[address]
            self.commands.append(
                (op1, crn, crm, op2, engine.reg_read(UC_ARM_REG_R0 + register))
            )
        if address == ADDRESS:
            metadata = engine.reg_read(UC_ARM_REG_R12)
            self.frames.append(
                {
                    "entryArguments": self.registers(UC_ARM_REG_R0, 4),
                    "entrySavedRegisters": self.registers(UC_ARM_REG_R4, 8),
                    "entrySp": engine.reg_read(UC_ARM_REG_SP),
                    "entryLr": engine.reg_read(UC_ARM_REG_LR),
                    "entryR10": engine.reg_read(UC_ARM_REG_R10),
                    "metadata": metadata,
                    "metadataBefore": struct.unpack(
                        "<6I", bytes(engine.mem_read(metadata, 24))
                    ),
                }
            )
        if address == self.target:
            frame = self.frames[-1]
            frame["targetArguments"] = self.registers(UC_ARM_REG_R0, 4)
            if frame["targetArguments"] != frame["entryArguments"] or frame[
                "targetArguments"
            ] != list(self.arguments):
                raise ValueError(
                    "Bridge did not preserve all four original argument words"
                )
        if address == ADDRESS + 36:
            self.frames[-1]["targetReturn"] = engine.reg_read(UC_ARM_REG_R0)
        if address == ADDRESS + 76:
            frame = self.frames[-1]
            after = struct.unpack("<6I", bytes(engine.mem_read(frame["metadata"], 24)))
            if self.registers(UC_ARM_REG_R4, 8) != frame["entrySavedRegisters"]:
                raise ValueError("Bridge changed a native callee-saved register")
            if (
                engine.reg_read(UC_ARM_REG_SP) != frame["entrySp"]
                or engine.reg_read(UC_ARM_REG_LR) != frame["entryLr"]
            ):
                raise ValueError(
                    "Bridge failed to restore its incoming stack/return state"
                )
            if engine.reg_read(UC_ARM_REG_R0) != frame["targetReturn"]:
                raise ValueError(
                    "Bridge lost the target return value across re-encryption"
                )
            if (
                after[0] != frame["entrySp"]
                or after[4] != frame["entryR10"]
                or any(
                    after[index] != frame["metadataBefore"][index]
                    for index in [2, 3, 5]
                )
            ):
                raise ValueError(
                    "Bridge metadata/control state differs from instruction-derived model"
                )
            frame["metadataAfter"] = after
            frame["returnAndSavedStatePreserved"] = True


def crc_value(data):
    value = 0xFFFFFFFF
    for byte in data:
        value ^= byte
        for _ in range(8):
            value = (value >> 1) ^ (((value & 1) ^ 1) * 0xEDB88320)
    return (~value) & 0xFFFFFFFF


def oracle(entry, code):
    data = audit.inputs()
    analysis = bytearray(data["analysis"])
    source_address = int(entry["address"], 16)
    offset = source_address - audit.BASE
    analysis[offset : offset + len(code)] = code
    rebuilt = dsprot128.image_transform(
        bytes(analysis), data["functions"], audit.BASE, True
    )
    if rebuilt != data["decoded"]:
        raise ValueError(
            "Source-assembled bridge changed the complete encrypted cold image"
        )
    operations = cache_operations(data["analysis"])
    lanes = []
    for image in [data["decoded"], rebuilt]:
        machine = Machine(image, data["entry"][3], 0x00480EC, operations)
        for constructor in data["constructors"]:
            if constructor:
                machine.call(constructor)
        passes = sum(function["kind"] == "unkeyed" for function in data["functions"])
        if machine.commands != expected_cache_pass() * passes:
            raise ValueError(
                "Native constructor cache-maintenance command sequence differs"
            )
        for function in data["functions"]:
            start = function["address"] - audit.BASE
            span = function["codeBytes"] + (function["poolBytes"] or 0)
            if function["kind"] in ["keyed", "unkeyed"]:
                expected_image = (
                    data["decoded"] if function["kind"] == "keyed" else data["analysis"]
                )
                if (
                    machine.image()[start : start + span]
                    != expected_image[start : start + span]
                ):
                    raise ValueError(
                        "Full constructor decoded/ciphertext function partition differs"
                    )
        if machine.image()[offset : offset + len(code)] != code:
            raise ValueError(
                "Recovered source function full span differs after native constructors"
            )
        randomizer = random.Random(0x80EC)
        rows = []
        for index in range(48):
            arguments = [randomizer.getrandbits(32) for _ in range(4)]
            if index % 3 == 0:
                wrapper, target, expected = 0x021D8920, 0x021D8908, 0xAA65
            elif index % 3 == 1:
                wrapper, target, expected = 0x021D895C, 0x021D8914, 0xA99F
            else:
                wrapper, target = 0x021D83D4, 0x021D8340
                size = [0, 1, 7, 32, 128, 511][(index // 3) % 6]
                buffer = randomizer.randbytes(size)
                machine.engine.mem_write(audit.STACK + 0x4000, buffer)
                arguments[0:2] = [audit.STACK + 0x4000, size]
                expected = crc_value(buffer)
            machine.arguments = tuple(arguments)
            machine.target = target
            machine.commands = []
            machine.frames = []
            first_writes = len(machine.writes)
            result = machine.call(wrapper, arguments=arguments)
            if machine.image()[offset : offset + len(code)] != code:
                raise ValueError(
                    "Recovered context/cache function changed during wrapped execution"
                )
            if (
                result["result"] != expected
                or len(machine.frames) != 1
                or not machine.frames[0].get("returnAndSavedStatePreserved")
            ):
                raise ValueError(
                    "Native/source bridge call did not satisfy its complete context model"
                )
            if machine.commands != expected_cache_commands():
                raise ValueError(
                    "Native CP15 command order/index/segment values differ from ARM946 model"
                )
            observed = {
                "result": result,
                "frame": machine.frames[0],
                "writes": machine.writes[first_writes:],
                "stackSha256": audit.sha(
                    bytes(machine.engine.mem_read(audit.STACK, 0x10000))
                ),
                "moduleSha256": audit.sha(machine.image()),
                "cp15Commands": machine.commands,
            }
            rows.append(
                {
                    "index": index,
                    "target": hex(target),
                    "cp15Commands": len(machine.commands),
                    "argumentsPreserved": True,
                    "savedStateAndReturnPreserved": True,
                    "stateSha256": audit.sha(
                        json.dumps(observed, sort_keys=True).encode()
                    ),
                }
            )
        lanes.append(rows)
    if lanes[0] != lanes[1]:
        raise ValueError("Native/source bridge runtime states differ")
    return {
        "passed": True,
        "vectors": len(lanes[0]),
        "executions": len(lanes[0]) * 2,
        "instructionLimit": 100000,
        "constructorCachePasses": passes,
        "constructorCp15Commands": len(expected_cache_pass()) * passes,
        "sourceLanguage": "metrowerks-assembler-function"
        if source_address == ADDRESS
        else "c-with-hardware-assembly",
        "justification": "Transparent register/stack bridge only"
        if source_address == ADDRESS
        else "Ordinary decode/key derivation remains C; the isolated60-byte CP15 cache-maintenance sequence uses readable inline assembler",
        "dependencyModel": "Native constructors, key derivation, keyed crypto, constant/CRC target functions and CP15 command instructions execute without substituted callees",
        "independentModel": "All four argument words, nativeR4-R11/SP/LR preservation, targetR0 return retention, metadata slot writes and two exact258-command cache-maintenance sequences",
        "limitations": [
            "Unicorn System-mode execution observes emitted CP15 commands and their operands but does not establish physical cache/write-buffer effects or hardware timing."
        ],
        "results": lanes[0],
    }
