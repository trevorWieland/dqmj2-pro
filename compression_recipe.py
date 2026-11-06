import base64
import struct


def parameters(stored):
    length, extra = struct.unpack_from("<II", stored, len(stored) - 8)
    header = length >> 24
    compressed = length & 0xFFFFFF
    if not 8 <= header <= 32 or not header <= compressed <= len(stored) or not extra:
        raise ValueError("Unsupported backward-LZ representation")
    return len(stored) - compressed, len(stored) - header - 1, len(stored) + extra


def transform(skeleton, decoded, clearing=False):
    result = bytearray(skeleton)
    prefix, cursor, decoded_size = parameters(result)
    if decoded_size != len(decoded):
        raise ValueError("Compression schedule decoded size changed")
    output = decoded_size - 1
    literals = 0
    references = 0
    while output >= prefix:
        flags = result[cursor]
        cursor -= 1
        for shift in range(7, -1, -1):
            if output < prefix:
                break
            if flags & (1 << shift):
                first, second = result[cursor], result[cursor - 1]
                cursor -= 2
                length = (first >> 4) + 3
                distance = (((first & 15) << 8) | second) + 3
                references += 1
                for _ in range(length):
                    if output < prefix or output + distance >= decoded_size:
                        raise ValueError("Invalid schedule backreference")
                    if decoded[output] != decoded[output + distance]:
                        raise ValueError(f"Rebuilt bytes violate schedule at {output:#x}")
                    output -= 1
            else:
                result[cursor] = 0 if clearing else decoded[output]
                cursor -= 1
                output -= 1
                literals += 1
    if cursor != prefix - 1:
        raise ValueError("Unconsumed compressed bytes")
    result[:prefix] = bytes(prefix) if clearing else decoded[:prefix]
    return bytes(result), {"literalBytes": literals, "prefixBytes": prefix, "backreferences": references}


def make_recipe(stored, decoded):
    skeleton, stats = transform(stored, decoded, clearing=True)
    reconstructed, _ = transform(skeleton, decoded)
    if reconstructed != stored:
        raise ValueError("Compression recipe does not reconstruct input")
    return {"schemaVersion": 1, "format": "backward-lz-original-token-schedule", "storedBytes": len(stored), "decodedBytes": len(decoded), "skeletonBase64": base64.b64encode(skeleton).decode("ascii"), "statistics": stats, "literalBytesStored": False, "limitation": "Exact-build token schedule; fails if rebuilt data cannot satisfy its original backreferences"}


def encode(recipe, decoded):
    result, _ = transform(base64.b64decode(recipe["skeletonBase64"]), decoded)
    return result
