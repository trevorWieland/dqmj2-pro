import struct


GLOBAL, KEYS, CONTROL = 0x21d19e0, 0x21d1ba8, 0x2210000
MESSAGE, MATCH, ADDRESS, KEYSTRING = 0x2211000, 0x2212000, 0x2213000, 0x2214000
OLDSTRING, HEAP, VALUE = 0x2215000, 0x2216000, 0x2217000
BUDDY, STATUS, STOP, SP = 0x2310000, 0x2310010, 0x2500000, 0x3008000
RET64 = set()
ARITY = {0x209b368: 1, 0x20b5f38: 3, 0x20b4330: 5, 0x209bf8c: 1,
         0x20b4374: 2, 0x20b45a4: 2, 0x20a41b4: 4, 0x20b45a0: 1,
         0x20a8c9c: 1, 0x209a9f8: 2, 0x2008c14: 3, 0x20a3d70: 0,
         0x20b80a0: 4, 0x201b248: 3, 0x20b70c8: 3, 0x201d800: 2,
         0x20a2a9c: 0, 0x209aa64: 3, 0x201d69c: 1, 0x209aa38: 2,
         0x209f130: 2, 0x201d6b8: 2, 0x20b85d8: 2}


def word(value):
    return struct.pack('<I', value & 0xffffffff)


def signed(value):
    return value - 0x100000000 if value & 0x80000000 else value


def cases(address):
    if address == 0x209bc9c:
        return [dict(socket=0x1234), dict(), dict(random=0x3fff), dict(create=1)]
    if address == 0x209be4c:
        return [dict(close=0), dict(close=1), dict(close=255)]
    if address == 0x209be5c:
        return [dict(), dict(socket=123)]
    if address == 0x209c24c:
        return [dict(message=False, length=0), dict(reliable=1), dict(length=1024, reliable=0)]
    if address == 0x209c4c8:
        return [dict(), dict(fd=-1, error=-2)]
    if address == 0x209dd80:
        return [dict(keyNull=True), dict(valueNull=True), dict(keyID=0, newKey=0),
                dict(keyID=0), dict(existing=True), dict(existing=True, keySame=False),
                dict(existing=True, allocate=False), dict(existing=True, oldNull=True), dict(keyID=101, newKey=101)]
    if address == 0x209eca4:
        return [dict(length=0), dict(message=False), dict(payload='qr'), dict(payload='qr', qr=False),
                dict(payload='slash', port=0), dict(payload='nat', port=65535), dict(payload='fe'), dict(payload='unknown')]
    raise ValueError('Unknown second caller identity')


def normalized(vector):
    value = dict(socket=0, random=7, create=0, close=1, message=True, length=8, reliable=0,
        fd=5, error=37, keyID=100, newKey=100, existing=False, keyNull=False, valueNull=False,
        keySame=True, oldNull=False, allocate=True, payload='unknown', qr=True, port=0x1234, ip=0x01020304)
    value.update(vector)
    return value


def initial(address, vector):
    v = normalized(vector)
    core = bytearray(48)
    core[:4] = word(v['socket'])
    core[20:28] = word(8192) + word(4096)
    core[44] = v['close']
    keys = bytearray(36)
    index = v['keyID'] - 100 if v['keyID'] >= 100 else v['newKey'] - 100
    if v['existing']:
        keys[index * 12:index * 12 + 12] = bytes([v['keyID'], 1, 0x12, 0x34]) + word(0 if v['oldNull'] else OLDSTRING) + word(0x8899)
    match = bytearray(20)
    match[16:20] = word(0x12345678 if v['qr'] else 0)
    payloads = {'qr': b'\xfe\xfdquery', 'slash': b'\\query', 'nat': bytes.fromhex('fdfc1e666ab2') + b'xx',
                'fe': b'\xfe\xfegt2!', 'unknown': b'unknown!'}
    regions = {GLOBAL: word(CONTROL) + word(0x6677), KEYS: bytes(keys), CONTROL: bytes(core),
        MESSAGE: payloads[v['payload']].ljust(32, b'\0'), MATCH: bytes(match), ADDRESS: b'0.0.0.0:1234\0'.ljust(32, b'\0'),
        KEYSTRING: b'key\0'.ljust(16, b'\0'), OLDSTRING: (b'key' if v['keySame'] else b'other') + b'\0',
        HEAP: bytes(32), VALUE: word(123)}
    if address in [0x209bc9c, 0x209be4c, 0x209be5c]:
        args = []
    elif address == 0x209c24c:
        args = [0x4567, MESSAGE if v['message'] else 0, v['length'], v['reliable']]
    elif address == 0x209c4c8:
        args = [0x4567]
    elif address == 0x209dd80:
        args = [v['keyID'], 0 if v['keyNull'] else KEYSTRING, 0 if v['valueNull'] else VALUE]
    else:
        args = [0x4567, v['ip'], v['port'], MESSAGE if v['message'] else 0, v['length']]
    return regions, args


def cstring(live, pointer):
    raw = bytearray()
    for index in range(64):
        value = live.read(pointer + index, 1)
        if value == b'\0':
            return bytes(raw)
        raw.extend(value)
    raise ValueError('Undeclared string length')


def sockaddr(vector):
    v = normalized(vector)
    return bytes([0, 2, v['port'] >> 8, v['port'] & 255]) + word(v['ip'])


def effect(at, args, live, vector):
    v = normalized(vector)
    if at == 0x209b368:
        return v['random'], ('random', args[0])
    if at == 0x20b5f38:
        return ADDRESS, ('address-string', args[0], args[1], args[2])
    if at == 0x20b4330:
        if v['create'] == 0:
            live.write(args[0], word(0x5432))
        return v['create'], ('create-socket', args[0], args[1], args[2], args[3], args[4])
    if at == 0x209bf8c:
        return args[0], ('handle-gt2', args[0])
    if at in [0x20b4374, 0x20b45a4]:
        return 0, ('listen' if at == 0x20b4374 else 'unrecognized-callback', args[0], args[1])
    if at == 0x20a41b4:
        return 0, ('receive', args[0], args[1], signed(args[2]), args[3])
    if at == 0x20b45a0:
        return v['fd'], ('socket-fd', args[0])
    if at == 0x20a8c9c:
        return v['error'], ('last-error', signed(args[0]))
    if at == 0x209a9f8:
        return 0, ('set-error', args[0], signed(args[1]))
    if at == 0x2008c14:
        if args[0] != 0 or args[2] != 8:
            raise ValueError('Source32-bit clear contract differs')
        live.write(args[1], bytes(8))
        return 0, ('clear-sockaddr', args[0], args[2])
    if at == 0x20a3d70:
        return MATCH, ('get-match',)
    if at == 0x20b80a0:
        return 0, ('qr-query', args[0], args[1], signed(args[2]), live.read(args[3], 8).hex())
    if at == 0x201b248:
        left, right = live.read(args[0], args[2]), live.read(args[1], args[2])
        return (left > right) - (left < right), ('memcmp', left.hex(), right.hex(), args[2])
    if at == 0x20b70c8:
        return 0, ('nat-data', args[0], signed(args[1]), live.read(args[2], 8).hex())
    if at == 0x201d800:
        left, right = cstring(live, args[0]), cstring(live, args[1])
        return (left > right) - (left < right), ('strcmp', left.decode(), right.decode())
    if at == 0x20a2a9c:
        return v['newKey'], ('new-key',)
    if at == 0x209aa64:
        return 0, ('free', args[0], args[1], args[2])
    if at == 0x201d69c:
        value = cstring(live, args[0])
        return len(value), ('strlen', value.decode())
    if at == 0x209aa38:
        return HEAP if v['allocate'] else 0, ('allocate', args[0], args[1])
    if at == 0x209f130:
        return 0, ('stop-matching', args[0], signed(args[1]))
    if at == 0x201d6b8:
        value = cstring(live, args[1])
        live.write(args[0], value + b'\0')
        return args[0], ('strcpy', args[0], value.decode())
    if at == 0x20b85d8:
        return 0, ('register-key', args[0], cstring(live, args[1]).decode())
    raise ValueError(('Unknown second provider', hex(at)))


def model(address, vector):
    v = normalized(vector)
    regions, args = initial(address, vector)
    expected = {at: bytearray(raw) for at, raw in regions.items()}
    events, contract, result = [], 'void', 0
    def event(*value):
        events.append(value)
    if address == 0x209bc9c:
        contract = 'word'
        if not v['socket']:
            event('random', 0x4000)
            event('address-string', 0, 0xc000 + v['random'], 0)
            event('create-socket', CONTROL, ADDRESS, 8192, 4096, 0x209c4c9)
            result = v['create']
            event('handle-gt2', result)
            if result == 0:
                expected[CONTROL][:4] = word(0x5432)
                event('listen', 0x5432, 0x209ed45)
                event('unrecognized-callback', 0x5432, 0x209eca5)
    elif address == 0x209be4c:
        expected[CONTROL][44] = 0
    elif address == 0x209c24c:
        event('receive', *args)
    elif address == 0x209c4c8:
        event('socket-fd', 0x4567);event('last-error', v['fd'])
        expected[GLOBAL][4:8] = word(v['error'])
        event('set-error', 9, -97003)
        expected[CONTROL][:4] = word(0)
    elif address == 0x209dd80:
        contract = 'word'
        if not v['keyNull'] and not v['valueNull']:
            selected = v['keyID']
            reject = False
            if selected >= 100 and v['existing']:
                if not v['oldNull']:
                    event('strcmp', 'key' if v['keySame'] else 'other', 'key')
                    reject = not v['keySame']
            else:
                event('new-key');selected = v['newKey'];reject = selected == 0
            if not reject:
                offset = (selected - 100) * 12
                expected[KEYS][offset:offset + 4] = bytes([selected, 0, 0, 0])
                if v['existing'] and not v['oldNull']:
                    event('free', 4, OLDSTRING, 0)
                event('strlen', 'key');event('allocate', 4, 4)
                expected[KEYS][offset + 4:offset + 8] = word(HEAP if v['allocate'] else 0)
                if v['allocate']:
                    event('strcpy', HEAP, 'key');expected[HEAP][:4] = b'key\0'
                    expected[KEYS][offset + 8:offset + 12] = word(VALUE)
                    event('register-key', selected, 'key');result = selected
                else:
                    event('stop-matching', 9, -80001)
    elif address == 0x209eca4:
        contract = 'word'
        if v['message'] and v['length']:
            event('clear-sockaddr', 0, 8)
            if v['payload'] in ['qr', 'slash']:
                event('get-match')
                if v['qr']:
                    event('get-match');event('qr-query', 0x12345678, MESSAGE, v['length'], sockaddr(v).hex())
                result = 1
            else:
                payload = regions[MESSAGE][:6]
                event('memcmp', payload.hex(), 'fdfc1e666ab2', 6)
                if v['payload'] == 'nat':
                    event('nat-data', MESSAGE, v['length'], sockaddr(v).hex());result = 1
    return {at: bytes(raw) for at, raw in expected.items()}, events, contract, result & 0xffffffff
