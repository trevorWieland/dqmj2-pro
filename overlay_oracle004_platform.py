import json
import random

import audit_overlay004 as audit

FUNCTIONS = {0x021D8168, 0x021D8218}
HELPERS = {0x020081FC: 28, 0x02008218: 132, 0x02008BF8: 28, 0x02008E0C: 304}
FIRMWARE = 0x027FF000


class Machine(audit.Machine):
    def __init__(self, image, bss_size, seed, firmware):
        super().__init__(image, bss_size, seed)
        main = (audit.ROOT / "extract/arm9/arm9.bin").read_bytes()
        for address, size in HELPERS.items():
            self.engine.mem_write(
                address, main[address - 0x02000000 : address - 0x02000000 + size]
            )
        self.engine.mem_map(FIRMWARE, 0x1000)
        self.engine.mem_write(FIRMWARE, firmware)
        self.executed_helpers = set()

    def permitted(self, address, size):
        if super().permitted(address, size):
            return True
        if 0x027FFC80 <= address and address + size <= 0x027FFCFA:
            return True
        return any(
            start <= address and address + size <= start + span
            for start, span in HELPERS.items()
        )

    def write(self, engine, access, address, size, value, user):
        if not audit.Machine.permitted(self, address, size):
            raise ValueError(
                "Native platform check wrote outside own module/BSS/private stack"
            )
        super().write(engine, access, address, size, value, user)

    def step(self, engine, address, size, user):
        if any(start <= address < start + span for start, span in HELPERS.items()):
            self.steps += 1
            self.executed.add(address)
            if address in HELPERS:
                self.executed_helpers.add(address)
            return
        super().step(engine, address, size, user)


def fixture(data, index):
    randomizer = random.Random(0x0048168 + index)
    firmware = bytearray(randomizer.randbytes(0x1000))
    expected_mac = bytes(
        byte ^ 255
        for byte in data["analysis"][0x021D8EB4 - audit.BASE : 0x021D8EBA - audit.BASE]
    )
    mac = bytearray(expected_mac)
    variant = index % 8
    if variant == 1:
        mac = bytearray(6)
    elif variant >= 2:
        mac[variant - 2] ^= 1
    month = 1 if index // 8 & 1 else 12
    day = 1 if index // 8 & 2 else 31
    name_length = 0 if index // 8 & 4 else 10
    firmware[0xCF4:0xCFA] = mac
    firmware[0xC83] = month
    firmware[0xC84] = day
    firmware[0xC9A] = name_length
    valid = (
        bytes(mac) == expected_mac and month == 1 and day == 1 and name_length == 0
    ) or not any(mac)
    return bytes(firmware), valid


def oracle(entry, code):
    address = int(entry["address"], 16)
    data = audit.inputs()
    rebuilt = bytearray(data["analysis"])
    offset = address - audit.BASE
    rebuilt[offset : offset + len(code)] = code
    vectors = []
    for index in range(64):
        firmware, valid = fixture(data, index)
        factor = (
            (251 if valid else 241)
            if address == 0x021D8168
            else (241 if valid else 251)
        )
        multiplier = 197 if address == 0x021D8168 else 193
        expected = factor * multiplier
        paired = []
        for image in [data["analysis"], bytes(rebuilt)]:
            machine = Machine(image, data["entry"][3], index, firmware)
            result = machine.call(address)
            if result["result"] != expected or machine.executed_helpers != set(HELPERS):
                raise ValueError(
                    "Native/C hardware-buffer model or executed SDK helper set differs"
                )
            if bytes(machine.engine.mem_read(FIRMWARE, 0x1000)) != firmware:
                raise ValueError(
                    "Native SDK helpers modified read-only synthetic firmware"
                )
            paired.append(
                {
                    "result": result["result"],
                    "stackSha256": audit.sha(
                        bytes(machine.engine.mem_read(audit.STACK, 0x10000))
                    ),
                    "imageSha256": audit.sha(machine.image()),
                    "writes": machine.writes,
                    "instructions": machine.steps,
                }
            )
        if paired[0] != paired[1]:
            raise ValueError("Native/C complete private state or write trace differs")
        vectors.append(
            {
                "index": index,
                "ownerAndMacModelValid": valid,
                "stateSha256": audit.sha(
                    json.dumps(paired[0], sort_keys=True).encode()
                ),
            }
        )
    main = (audit.ROOT / "extract/arm9/arm9.bin").read_bytes()
    return {
        "passed": True,
        "vectors": len(vectors),
        "executions": len(vectors) * 2,
        "instructionLimit": 100000,
        "dependencyModel": "Four original SDK getter/copy helpers execute from independently synthesized private firmware buffers; no substituted native callees or device reads",
        "independentModel": "Six-byte complemented identifier match, month/day/name-length conjunction, all-zero identifier fallback, variant-specific factors and multiplication",
        "executedNativeHelpers": [
            {
                "address": hex(address),
                "bytes": size,
                "sha256": audit.sha(
                    main[address - 0x02000000 : address - 0x02000000 + size]
                ),
            }
            for address, size in HELPERS.items()
        ],
        "limitations": [
            "Synthetic firmware exercises bounded platform buffer semantics; real device firmware, hardware access timing and complete application behavior are not claimed."
        ],
        "results": vectors,
    }
