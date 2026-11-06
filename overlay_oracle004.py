import json
import random
import struct

import audit_overlay004 as audit
import dsprot128
from overlay_oracle004_guards import GUARDS, oracle as guard_oracle
from overlay_oracle004_platform import FUNCTIONS, oracle as platform_oracle
from overlay_oracle004_bridge import CONTEXT_FUNCTIONS, oracle as bridge_oracle

CHECKS = {
    0x021D7854: (0x021D82C8, 0xAA65, 0xB177),
    0x021D7970: (0x021D8304, 0xB177, 0xAA65),
    0x021D7A8C: (0x021D8890, 0xAA65, 0xB177),
    0x021D7BA8: (0x021D88CC, 0xB177, 0xAA65),
}
SUPPORTED = (
    set(CHECKS)
    | set(GUARDS)
    | FUNCTIONS
    | CONTEXT_FUNCTIONS
    | {0x021D8340, 0x021D89E4, 0x021D8A70, 0x021D8AC8, 0x021D8DA0, 0x021D8DF8}
)


def expanded_key(seed, size):
    words = [
        (((seed << shift) | (seed >> ((32 - shift) & 31))) & 0xFFFFFFFF) ^ size
        for shift in [0, 8, 16, 24]
    ]
    return struct.pack("<4I", *words)


def state_vector(randomizer):
    feedback, first, second = [randomizer.randrange(256) for _ in range(3)]
    table = list(range(256))
    randomizer.shuffle(table)
    state = struct.pack("<3I", feedback, first, second) + bytes(table)
    first = (first + 1 + feedback) & 255
    second = (second + table[first] + feedback) & 255
    table[first], table[second] = table[second], table[first]
    output = table[(table[first] + table[second]) & 255]
    expected = struct.pack("<3I", feedback, first, second) + bytes(table)
    return state, expected, output


def oracle(entry, code):
    address = int(entry["address"], 16)
    if address in GUARDS:
        return guard_oracle(entry, code)
    if address in FUNCTIONS:
        return platform_oracle(entry, code)
    if address in CONTEXT_FUNCTIONS:
        return bridge_oracle(entry, code)
    if address not in SUPPORTED:
        raise ValueError("Unsupported independent Overlay004 oracle")
    data = audit.inputs()
    native = data["analysis"]
    offset = address - audit.BASE
    rebuilt = bytearray(native)
    rebuilt[offset : offset + len(code)] = code
    randomizer = random.Random(address)
    vectors = []
    for vector in range(96):
        state_address = audit.STACK + 0x4000
        input_address = audit.STACK + 0x5000
        output_address = audit.STACK + 0x6000
        source_input = None
        key_input = None
        patch_address = None
        if address in CHECKS:
            patch_address, success, failure = CHECKS[address]
            signature = bytearray.fromhex("0fc08fe10cc01ce000c0a0031cc08c12")
            expected_result = success
            if vector % 33:
                position = (vector - 1) % 16
                signature[position] ^= [1, 0x80, 0xFF][(vector // 16) % 3]
                expected_result = failure
            initial = randomizer.randbytes(32)
            expected_state = initial
            args = ()
        elif address == 0x021D8340:
            size = [0, 1, 2, 3, 4, 7, 16, 31, 64, 127, 256, 1024][vector % 12]
            initial = randomizer.randbytes(size)
            crc = 0xFFFFFFFF
            for value in initial:
                crc ^= value
                for _ in range(8):
                    crc = (crc >> 1) ^ (((crc & 1) ^ 1) * 0xEDB88320)
            expected_state = initial
            expected_result = (~crc) & 0xFFFFFFFF
            args = (state_address, size)
        elif address == 0x021D89E4:
            length = [0, 1, 2, 3, 7, 16, 31, 64, 255, 256, 257, 512][vector % 12]
            key_input = randomizer.randbytes(max(1, length))
            if vector // 12 == 0:
                key_input = bytes(len(key_input))
            elif vector // 12 == 1:
                key_input = bytes([255]) * len(key_input)
            initial = randomizer.randbytes(268)
            table = list(range(256))
            accumulator = 0
            key_position = 0
            for position in range(255, -1, -1):
                accumulator = (accumulator + table[position] + key_input[key_position]) & 255
                table[position], table[accumulator] = table[accumulator], table[position]
                key_position += 1
                if key_position >= length:
                    key_position = 0
            expected_state = struct.pack("<3I", 0xAA, 0, 0) + bytes(table)
            expected_result = None
            args = (state_address, input_address, length)
        elif address == 0x021D8A70:
            initial, expected_state, expected_result = state_vector(randomizer)
            args = (state_address,)
        elif address == 0x021D8AC8:
            initial = randomizer.randbytes(256)
            expected_state = bytes(range(255, -1, -1))
            expected_result = 0
            args = (state_address,)
        else:
            size = [0, 4, 8, 12, 16, 32, 64, 128, 1, 2, 3, 5][vector % 12]
            seed = randomizer.getrandbits(32)
            initial = expanded_key(seed, size)
            high_bytes = [0xEA, 0xEB, 0xFA, 0xFB, 0x1A, 0x1B, 0xE1, 0xE5]
            words = [
                (high_bytes[(index + vector) % len(high_bytes)] << 24)
                | randomizer.randrange(0x1000000)
                for index in range((size + 3) // 4)
            ]
            source_input = struct.pack("<" + "I" * len(words), *words)
            encrypt = address == 0x021D8DA0
            expected_state = (
                dsprot128.transform(source_input, seed, encrypt)
                if size % 4 == 0
                else bytes([0xA5]) * max(4, len(source_input))
            )
            expected_result = 0 if size % 4 == 0 else 0xFFFFFFFF
            if not encrypt and vector % 2:
                output_address = input_address
                if size % 4:
                    expected_state = source_input
            elif not encrypt and size % 4 == 0:
                out_of_place = bytearray(expected_state)
                for index, word in enumerate(words):
                    if dsprot128.category(word) == "bl":
                        out_of_place[index * 4 + 3] ^= 1
                expected_state = bytes(out_of_place)
            args = (state_address, input_address, output_address, size)
        paired = []
        for image in [native, bytes(rebuilt)]:
            machine = audit.Machine(image, data["entry"][3], vector)
            machine.engine.mem_write(state_address, initial)
            if key_input is not None:
                machine.engine.mem_write(input_address, key_input)
            if patch_address is not None:
                machine.engine.mem_write(patch_address, bytes(signature))
            if source_input is not None:
                machine.engine.mem_write(input_address, source_input)
                if output_address != input_address:
                    machine.engine.mem_write(
                        output_address, bytes([0xA5]) * max(4, len(source_input))
                    )
            result = machine.call(address, arguments=args)
            if expected_result is not None and result["result"] != expected_result:
                raise ValueError("Independent native/C return value differs")
            observed_address = (
                output_address if source_input is not None else state_address
            )
            observed = bytes(
                machine.engine.mem_read(observed_address, len(expected_state))
            )
            if observed != expected_state:
                raise ValueError(
                    "Independent native/C stream state or cipher output differs"
                )
            paired.append(
                {
                    "return": result["result"],
                    "stackSha256": audit.sha(
                        bytes(machine.engine.mem_read(audit.STACK, 0x10000))
                    ),
                    "imageSha256": audit.sha(machine.image()),
                    "writes": machine.writes,
                    "instructions": machine.steps,
                }
            )
        if paired[0] != paired[1]:
            raise ValueError("Full native/C memory or trace differs")
        vectors.append(
            {
                "index": vector,
                "stateSha256": audit.sha(
                    json.dumps(paired[0], sort_keys=True).encode()
                ),
                "instructions": paired[0]["instructions"],
            }
        )
    return {
        "passed": True,
        "vectors": len(vectors),
        "executions": len(vectors) * 2,
        "instructionLimit": 100000,
        "dependencyModel": "Original native Overlay004 crypto helpers execute without substituted callees; only this source-compiled entry is replaced",
        "independentModel": "Reverse key scheduling, modified stream permutation/step, pinned independent keyed DSProtect V4 transform, or inverted-bit CRC polynomial recurrence; complete observed state/output; void key initializer has no promised return value",
        "inputDomain": "Nonnegative bounded byte lengths and valid private pointers; negative signed CRC lengths are not exercised",
        "memoryModel": "Native reads/writes limited to own image/BSS and bounded private stack; full64KiB stack hashes and exact write traces compared",
        "results": vectors,
    }
