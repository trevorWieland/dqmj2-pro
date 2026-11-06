import json
import random

import audit_overlay004 as audit
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_CPSR,
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R12,
)

GUARDS = {
    0x021D7304: ([0x021D7D3C, 0x021D7D3C], [0xAA65, 0xAA65], 241, False),
    0x021D73A4: ([0x021D7D78, 0x021D7D78], [0xB177, 0xB177], 251, True),
    0x021D7444: ([0x021D82C8, 0x021D7CC4], [0xAA65, 0xAA65], 241, False),
    0x021D74E4: ([0x021D8304, 0x021D7D00], [0xB177, 0xB177], 251, True),
    0x021D7584: ([0x021D8920], [0xAA65], 241, False),
    0x021D7614: ([0x021D895C], [0xA99F], 251, True),
}


def classify(word):
    opcode = word >> 24
    if opcode & 14 != 10:
        return 0
    if opcode & 240 == 240:
        return 1
    return 2 if opcode & 1 else 3


def oracle(entry, code):
    address = int(entry["address"], 16)
    targets, canonical, prime, call_when_zero = GUARDS[address]
    data = audit.inputs()
    source_image = bytearray(data["analysis"])
    offset = address - audit.BASE
    source_image[offset : offset + len(code)] = code
    randomizer = random.Random(address)
    vectors = []
    for index in range(48):
        if index % 4 == 0:
            values = canonical
        elif index % 4 == 1:
            values = [value ^ 0x712 for value in canonical]
        elif index % 4 == 2:
            values = [randomizer.getrandbits(32) for _ in targets]
        else:
            values = [0xFFFFFFFF for _ in targets]
        argument = (
            [0xEA, 0xEB, 0xFA, 0xE1, 0x1A, 0x1B][index % 6] << 24
        ) | randomizer.randrange(0x1000000)
        total = (0x30EB87 + sum(values)) & 0xFFFFFFFF
        taken = (total % prime == 0) == call_when_zero
        expected = classify(argument) if taken else total
        states = []
        for image in [data["analysis"], bytes(source_image)]:
            machine = audit.Machine(image, data["entry"][3], index)
            calls = []
            callback_calls = []
            clobber = random.Random(index + address)

            def hook(engine, location, size, user):
                if location == 0x021D7DE8:
                    callback_calls.append(engine.reg_read(UC_ARM_REG_R0))
                if location not in targets:
                    return
                call_index = len(calls)
                if call_index >= len(targets) or location != targets[call_index]:
                    raise ValueError("Guard indirect callback order differs")
                result = values[call_index]
                calls.append({"target": hex(location), "result": result})
                return_address = engine.reg_read(UC_ARM_REG_LR)
                for register in [
                    UC_ARM_REG_R1,
                    UC_ARM_REG_R2,
                    UC_ARM_REG_R3,
                    UC_ARM_REG_R12,
                ]:
                    engine.reg_write(register, clobber.getrandbits(32))
                engine.reg_write(UC_ARM_REG_CPSR, 0x1F | (clobber.randrange(16) << 28))
                engine.reg_write(UC_ARM_REG_R0, result)
                engine.reg_write(UC_ARM_REG_PC, return_address)

            machine.engine.hook_add(UC_HOOK_CODE, hook)
            result = machine.call(address, arguments=(0x021D7DE8, argument))
            if result["result"] != expected or len(calls) != len(targets):
                raise ValueError(
                    "Independent modulo/unsigned accumulator model differs"
                )
            if callback_calls != ([argument] if taken else []):
                raise ValueError(
                    "Conditional callback or original argument preservation differs"
                )
            states.append(
                {
                    "calls": calls,
                    "callbackArguments": callback_calls,
                    "return": result["result"],
                    "stackSha256": audit.sha(
                        bytes(machine.engine.mem_read(audit.STACK, 0x10000))
                    ),
                    "imageSha256": audit.sha(machine.image()),
                    "writes": machine.writes,
                    "instructions": machine.steps,
                }
            )
        if states[0] != states[1]:
            raise ValueError("Native/C guard state/write trace differs")
        vectors.append(
            {
                "index": index,
                "callbackTaken": taken,
                "stateSha256": audit.sha(
                    json.dumps(states[0], sort_keys=True).encode()
                ),
            }
        )
    return {
        "passed": True,
        "vectors": len(vectors),
        "executions": len(vectors) * 2,
        "instructionLimit": 100000,
        "dependencyModel": "Declared integrity/hardware/constant callees return bounded scripted values and clobber caller-saved registers; actual plain native classifier executes as the selected callback",
        "independentModel": "Unsigned32-bit accumulation, prime241/251 remainder gate, exact indirect call sequence, preserved callback argument and modeled classifier result",
        "limitations": [
            "Scripted callee values exercise guard logic and do not establish complete callee/platform behavior; separate native protection chain evidence covers supported real callers."
        ],
        "results": vectors,
    }
