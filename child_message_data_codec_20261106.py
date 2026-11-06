def encode(decoded, groups):
    output = bytearray(b'\x10' + len(decoded).to_bytes(3, 'little'))
    cursor = 0
    for index, tokens in enumerate(groups):
        assert 1 <= len(tokens) <= 8 and (len(tokens) == 8 or index == len(groups) - 1)
        flags = sum(1 << (7 - bit) for bit, token in enumerate(tokens) if token is not None)
        output.append(flags)
        for token in tokens:
            if token is None:
                assert cursor < len(decoded)
                output.append(decoded[cursor])
                cursor += 1
            else:
                assert isinstance(token, list) and len(token) == 2
                length, distance = token
                assert 3 <= length <= 18 and 1 <= distance <= min(4096, cursor)
                assert cursor + length <= len(decoded)
                assert all(decoded[cursor + at] == decoded[cursor + at - distance] for at in range(length))
                output.extend((((length - 3) << 12) | (distance - 1)).to_bytes(2, 'big'))
                cursor += length
    assert cursor == len(decoded)
    return bytes(output)


def build(document, bmg):
    assert set(document) == {'version', 'source', 'compressionRecipe', 'storageAlignment'}
    assert document['version'] == 1 and document['storageAlignment'] == 4
    source = document['source']
    assert set(source) == {'id', 'encoding', 'endianness', 'unk14', 'unk18', 'unk1C', 'messages'}
    obj = bmg.BMG(id=source['id'])
    for key in ['encoding', 'endianness', 'unk14', 'unk18', 'unk1C']:
        setattr(obj, key, source[key])
    for message in source['messages']:
        assert set(message) == {'info', 'stringParts', 'isNull'}
        assert all(isinstance(part, str) for part in message['stringParts'])
    obj.messages = [bmg.Message(bytes(row['info']), list(row['stringParts']), row['isNull']) for row in source['messages']]
    decoded = obj.save()
    assert decoded.startswith(b'MESGbmg1') and not obj.instructions and not obj.labels and not obj.scripts
    payload = encode(decoded, document['compressionRecipe'])
    alignment_bytes = (-len(payload)) % document['storageAlignment']
    return payload, alignment_bytes


def c_source(document, symbol, bmg):
    import re
    assert re.fullmatch(r'native_child_message_data_[0-9a-f]{8}', symbol)
    payload, alignment_bytes = build(document, bmg)
    size = len(payload) + alignment_bytes
    lines = [f'const unsigned char {symbol}[{size}] = {{']
    lines += ['    ' + ', '.join(f'0x{value:02x}' for value in payload[at:at + 16]) + ','
              for at in range(0, len(payload), 16)]
    return '\n'.join(lines + ['};', '']), payload + bytes(alignment_bytes), len(payload), alignment_bytes
