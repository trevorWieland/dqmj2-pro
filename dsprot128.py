import re
import struct

REFERENCE = 0x1000
UNKEYED_SEED = 0xF0B9A2EA


def category(word):
    opcode = word >> 24
    if opcode & 14 != 10:
        return "other"
    if opcode & 240 == 240:
        return "blx"
    return "bl" if opcode & 1 else "b"


def branch(word, encrypt):
    displacement = (REFERENCE + 8) // 4
    operands = (word & 0xFFFFFF) + (displacement if encrypt else -displacement)
    return ((word & 0xFF000000) ^ 0x01000000) | (operands & 0xFFFFFF)


class Stream:
    def __init__(self, seed, size):
        expanded = [
            (((seed << shift) | (seed >> ((32 - shift) & 31))) & 0xFFFFFFFF) ^ size
            for shift in [0, 8, 16, 24]
        ]
        key = struct.pack("<4I", *expanded)
        self.table = list(range(256))
        cursor = 0
        for index in range(256):
            position = 255 - index
            cursor = (cursor + self.table[position] + key[index % 16]) & 255
            self.table[cursor], self.table[position] = (
                self.table[position],
                self.table[cursor],
            )
        self.i = 0
        self.j = 0
        self.feedback = 0xAA

    def byte(self, value, encrypt):
        self.i = (self.i + 1 + self.feedback) & 255
        self.j = (self.j + self.table[self.i] + self.feedback) & 255
        self.table[self.i], self.table[self.j] = self.table[self.j], self.table[self.i]
        key = self.table[(self.table[self.i] + self.table[self.j]) & 255]
        result = value ^ key
        self.feedback = result if encrypt else value
        return result


def transform(code, seed=None, encrypt=False):
    if len(code) % 4:
        raise ValueError("DSProtect instruction range is not word aligned")
    stream = Stream(seed, len(code)) if seed is not None else None
    xor = UNKEYED_SEED
    result = []
    for (word,) in struct.iter_unpack("<I", code):
        kind = category(word)
        if stream is None:
            encodedBranch = kind in (["blx", "bl"] if encrypt else ["blx", "b"])
            if encodedBranch:
                new = branch(word, encrypt)
                plain = word if encrypt else new
                xor = (xor ^ (plain >> 24)) & 0xFFFFFF
            else:
                flipped = kind == ("b" if encrypt else "bl")
                new = word ^ xor ^ (0x01000000 if flipped else 0)
                plain = word if encrypt else new
                xor = (xor ^ plain ^ (plain >> 8)) & 0xFFFFFF
        else:
            encodedBranch = kind in (["blx", "bl"] if encrypt else ["blx", "b"])
            if encodedBranch:
                new = branch(word, encrypt)
                encoded = new if encrypt else word
                stream.feedback = (stream.feedback + (encoded >> 24)) & 255
            else:
                raw = list(struct.pack("<I", word))
                values = [
                    stream.byte(raw[0], encrypt),
                    stream.byte(raw[1], encrypt),
                    raw[2] ^ 255,
                    raw[3] ^ int(kind == ("b" if encrypt else "bl")),
                ]
                new = int.from_bytes(bytes(values), "little")
                encoded = values if encrypt else raw
                stream.feedback = (encoded[2] * stream.feedback - encoded[3]) & 255
        result.append(new & 0xFFFFFFFF)
    return struct.pack("<" + "I" * len(result), *result)


def metadata(text):
    sections = re.split(r"(?m)^  - id: (\d+)\s*$", text)
    block = next(
        sections[i + 1] for i in range(1, len(sections), 2) if sections[i] == "4"
    )
    if not re.search(r'version:\s*"1\.28"', block):
        raise ValueError("Expected pinned DSProtect1.28 metadata")
    bss = int(re.search(r"(?m)^        bss_variable: (\d+)", block)[1])
    functionsText, relocationsText = block.split("        functions:\n", 1)[1].split(
        "        relocations:\n", 1
    )
    records = re.split(r"(?m)^          - address: (\d+)\s*$", functionsText)
    functions = []
    for index in range(1, len(records), 2):
        body = records[index + 1]
        size = int(re.search(r"(?m)^            size: (\d+)", body)[1])
        pool = re.search(r"(?m)^            pool_size: (null|\d+)", body)[1]
        keyed = re.search(r"(?m)^              keyed: (\d+)", body)
        kind = (
            "keyed"
            if keyed
            else re.search(r"(?m)^            encryption: (\w+)", body)[1]
        )
        tableLength = re.search(r"(?m)^              length: (\d+)", body)
        functions.append(
            {
                "address": int(records[index]),
                "codeBytes": size,
                "poolBytes": None if pool == "null" else int(pool),
                "kind": kind,
                "seed": int(keyed[1]) if keyed else None,
                "tableLength": int(tableLength[1]) if tableLength else None,
                "hasGarbage": "has_garbage: true" in body,
                "hasOverwrite": "has_overwrite: true" in body,
            }
        )
    records = re.split(r"(?m)^          - from_address: (\d+)\s*$", relocationsText)
    relocations = []
    for index in range(1, len(records), 2):
        body = records[index + 1]
        relocations.append(
            {
                "from": int(records[index]),
                "to": int(re.search(r"to_address: (\d+)", body)[1]),
                "addend": int(re.search(r"addend: (\d+)", body)[1]),
            }
        )
    return bss, functions, relocations


def image_transform(image, functions, base, encrypt):
    result = bytearray(image)
    for function in functions:
        if function["kind"] == "none":
            continue
        start = function["address"] - base
        end = start + function["codeBytes"]
        if not 0 <= start < end <= len(result):
            raise ValueError("Protected function range escapes overlay")
        result[start:end] = transform(image[start:end], function["seed"], encrypt)
    return bytes(result)
