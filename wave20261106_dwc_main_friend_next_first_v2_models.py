import struct


GLOBAL, CONTROL, LIST, CONNECTION = 0x21d1b74, 0x2210000, 0x2211000, 0x2212000
ARG, MATCHES, USERDATA = 0x2213000, 0x2214000, 0x2215000
BUDDY, STATUS, STOP, SP = 0x2310000, 0x2310010, 0x2500000, 0x3008000
TOKEN = b'123456789ABCDxxxxxxx'
TEXT = b'fixture-status\0'
TICK = 0x1122334455667788
RET64 = {0x2007a9c}
ARITY = {0x209d168: 1, 0x20aa3e0: 3, 0x209d134: 1, 0x2007a9c: 0,
         0x209cbc4: 2, 0x209d03c: 2, 0x2096d9c: 1, 0x209d514: 3,
         0x20aa4f0: 3, 0x209d704: 1, 0x209d66c: 1, 0x20973a8: 2,
         0x2096dd0: 1, 0x209d238: 1, 0x2096e50: 2, 0x2096e08: 2,
         0x2096d04: 1, 0x2096e2c: 2, 0x209c5fc: 0, 0x20973c8: 3,
         0x20aa2f8: 2, 0x20aa334: 2, 0x20061ac: 7, 0x20972f4: 2,
         0x2096d24: 1, 0x209d58c: 3, 0x201d800: 2, 0x201b248: 3,
         BUDDY: 2, STATUS: 4}


def word(value):
    return struct.pack('<I', value & 0xffffffff)


def signed(value):
    return value - 0x100000000 if value & 0x80000000 else value


def callback(base, vector):
    return base | vector.get('callbackMode', 1)


def cases(address):
    if address == 0x209d0d4:
        return [dict(status=False), dict(status=True, found=-1), dict(status=True, found=2), dict(status=True, found=0, callbackMode=0)]
    if address == 0x209d168:
        return [dict(null=True), dict(target=0), dict(count=0), dict(target=22, count=3), dict(target=77, count=3), dict(count=-1)]
    if address == 0x209d1a8:
        return [dict(null=True), dict(), dict(counter=0xffffffff)]
    if address == 0x209d238:
        return [dict(), dict(buddy=True, state=0), dict(status=True), dict(buddy=True, status=True, state=0), dict(buddy=True, status=True, state=1), dict(buddy=True, status=True, state=0, callbackMode=0)]
    if address == 0x209d704:
        return [dict(result=value) for value in range(5)]
    if address == 0x209d758:
        return [dict(result=3), dict(matches=0, state=0), dict(matches=0), dict(matches=0, state=0, types=[0]),
                dict(state=0), dict(refresh=0, matches=2), dict(matches=2, buddyIndices=[-1, -1], more=0x600),
                dict(matches=2, buddyIndices=[-1, 4], ready=True), dict(matches=1, buddyIndices=[2]),
                dict(matches=2, buddyIndices=[-1, -1], more=0x601)]
    if address == 0x209d8f0:
        return [dict(result=1), dict(count=0), dict(types=[1], token=False), dict(types=[1], ready=True),
                dict(types=[3], ready=True), dict(types=[2], code=False), dict(types=[3], profileMatch=False)]
    if address == 0x209da68:
        return [dict(result=1), dict(count=0), dict(types=[1], token=False), dict(types=[1], ready=True),
                dict(types=[3], buddyAlready=True), dict(types=[1, 3], count=2, buddyFlags=[False, True], ready=True),
                dict(types=[2], profileMatch=False)]
    raise ValueError('Unknown friend fixture identity')


def normalized(vector):
    defaults = dict(count=1, state=1, status=False, buddy=False, types=[1], target=22, profiles=[11, 22, 33],
        result=0, matches=1, more=0x600, refresh=-1, buddyIndices=[-1, -1], ready=False,
        token=True, code=True, profileMatch=True, buddyAlready=False, refreshAll=0,
        counter=17, found=1, callbackMode=1)
    defaults.update(vector)
    return defaults


def initial(address, vector):
    v = normalized(vector)
    control = bytearray(96)
    for offset, value in [(0, v['state']), (4, CONNECTION), (8, v['counter']), (20, v['count']), (24, LIST),
                          (52, callback(STATUS, v) if v['status'] else 0), (56, 0x13579),
                          (68, callback(BUDDY, v) if v['buddy'] else 0), (72, 0x24680)]:
        control[offset:offset + 4] = word(value)
    control[12:20] = (0xfedcba9876543210).to_bytes(8, 'little')
    control[28:32] = bytes([7, 0, 0, 1])
    argument = bytearray(256)
    argument[:16] = word(v['result']) + word(v['matches']) + word(v['more']) + word(MATCHES)
    if address == 0x209d0d4:
        argument[:12] = word(77) + word(123) + word(9)
    if address in [0x209d8f0, 0x209da68]:
        argument[:8] = word(v['result']) + word(77)
        token = TOKEN if v['token'] else b'other-name'
        argument[142:142 + len(token) + 1] = token + b'\0'
        if not v['code']:
            argument[151:155] = b'WXYZ'
    matches = bytearray(344)
    for index, profile in enumerate([111, 222]):
        matches[index * 172:index * 172 + 4] = word(profile)
    user = bytearray(64)
    user[36:40] = word(0x41424344)
    regions = {GLOBAL: bytes(12) + word(0 if v.get('null') else CONTROL), CONTROL: bytes(control),
               LIST: bytes(48), CONNECTION: bytes(16), ARG: bytes(argument), MATCHES: bytes(matches), USERDATA: bytes(user)}
    if address in [0x209d168]:
        args = [v['target']]
    elif address in [0x209d238]:
        args = [0]
    elif address in [0x209d704]:
        args = [v['result']]
    elif address in [0x209d1a8]:
        args = []
    else:
        args = [CONNECTION, ARG, 0]
    return regions, args


def record_index(pointer):
    if pointer < LIST or pointer >= LIST + 48 or (pointer - LIST) % 12:
        raise ValueError('Friend record pointer left declared fixture domain')
    return (pointer - LIST) // 12


def cstring(live, pointer, maximum=300):
    result = bytearray()
    for offset in range(maximum):
        value = live.read(pointer + offset, 1)
        if value == b'\0':
            return bytes(result)
        result.extend(value)
    raise ValueError('Fixture string has no declared terminator')


def effect(at, args, live, vector):
    v = normalized(vector)
    if at == 0x209d168:
        return v['found'], ('find', args[0])
    if at == 0x20aa3e0:
        value = bytearray(532)
        value[:8] = word(77) + word(0x1ab)
        value[264:264 + len(TEXT)] = TEXT
        live.write(args[2], bytes(value))
        return 0, ('buddy-status', args[0], args[1])
    if at == 0x209d134:
        return v['profiles'][args[0]], ('profile-at', args[0])
    if at == 0x2007a9c:
        return TICK, ('tick',)
    if at == 0x209cbc4:
        live.write(args[1], TEXT)
        return 0xab, ('friend-status', record_index(args[0]))
    if at == BUDDY:
        return 0, ('buddy-callback', args[0], args[1])
    if at == STATUS:
        return 0, ('status-callback', args[0], args[1], cstring(live, args[2]).decode(), args[3])
    if at == 0x209d03c:
        return 0, ('stop-friend', args[0], signed(args[1]))
    if at == 0x2096d9c:
        index = record_index(args[0])
        return v['types'][index], ('type', index)
    if at == 0x209d514:
        return int(args[2] == [111, 222][v['refresh']] if v['refresh'] >= 0 else False), ('refresh-one', args[0], args[1], args[2])
    if at == 0x20aa4f0:
        index = [111, 222].index(args[1])
        live.write(args[2], word(v['buddyIndices'][index]))
        return 0, ('buddy-index', args[0], args[1])
    if at == 0x209d704:
        return args[0], ('handle-gp', args[0])
    if at == 0x209d66c:
        return 0, ('send-request', args[0])
    if at == 0x20973a8:
        return 0, ('set-profile', record_index(args[0]), args[1])
    if at == 0x2096dd0:
        return 0, ('mark-buddy', record_index(args[0]))
    if at == 0x209d238:
        return 0, ('friend-callback', args[0])
    if at in [0x2096e50, 0x2096e08, 0x2096e2c]:
        return 0, ({0x2096e50: 'flag20', 0x2096e08: 'flag8', 0x2096e2c: 'flag10'}[at], record_index(args[0]), args[1])
    if at == 0x2096d04:
        return int(v['ready']), ('flag-query', record_index(args[0]))
    if at == 0x209c5fc:
        return USERDATA, ('user-data',)
    if at == 0x20973c8:
        live.write(args[2], TOKEN + b'\0')
        return 0, ('user-name', args[0], record_index(args[1]))
    if at in [0x20aa2f8, 0x20aa334]:
        return 0, ('auth-request' if at == 0x20aa2f8 else 'deny-request', args[0], args[1])
    if at == 0x20061ac:
        if cstring(live, args[2]) != b'%c%c%c%c' or args[1] != 5:
            raise ValueError('Original format contract or bounded output differs')
        raw = bytes(value & 255 for value in args[3:7])
        live.write(args[0], raw + b'\0')
        return 4, ('format-code', raw.decode())
    if at == 0x20972f4:
        return 77 if v['profileMatch'] else 88, ('get-profile', args[0], record_index(args[1]))
    if at == 0x2096d24:
        index = record_index(args[0])
        return int(v.get('buddyFlags', [v['buddyAlready']] * 4)[index]), ('is-buddy', index)
    if at == 0x209d58c:
        return v['refreshAll'], ('refresh-all', args[0], signed(args[1]), args[2])
    if at == 0x201d800:
        left, right = cstring(live, args[0]), cstring(live, args[1])
        return (left > right) - (left < right), ('strcmp', left.decode(), right.decode())
    if at == 0x201b248:
        left, right = live.read(args[0], args[2]), live.read(args[1], args[2])
        return (left > right) - (left < right), ('memcmp', left.hex(), right.hex(), args[2])
    raise ValueError(('Undeclared friend contract', hex(at)))


def model(address, vector):
    v = normalized(vector)
    memory, unused = initial(address, vector)
    memory = {at: bytearray(raw) for at, raw in memory.items()}
    events, contract, result = [], 'void', 0
    def event(*value):
        events.append(value)
    def advance():
        memory[CONTROL][28] = 8
        memory[CONTROL][30] = 1
    def query_flags(index, flag8=False):
        if flag8:
            event('flag8', index, 1)
        event('flag-query', index)
        if v['ready']:
            event('flag10', index, 1)
    if address == 0x209d0d4 and v['status']:
        event('find', 77)
        if v['found'] != -1:
            event('buddy-status', CONNECTION, 9)
            event('status-callback', v['found'], 0xab, TEXT[:-1].decode(), 0x13579)
    elif address == 0x209d168:
        contract, result = 'int', -1
        if not v.get('null') and v['target']:
            for index in range(max(0, v['count'])):
                event('profile-at', index)
                if v['profiles'][index] == v['target']:
                    result = index
                    break
    elif address == 0x209d1a8 and not v.get('null'):
        memory[CONTROL][8:12] = word(0)
        memory[CONTROL][12:20] = TICK.to_bytes(8, 'little')
        event('tick')
    elif address == 0x209d238:
        if v['buddy'] and v['state'] != 1:
            event('buddy-callback', 0, 0x24680)
        if v['status']:
            event('friend-status', 0)
            event('status-callback', 0, 0xab, TEXT[:-1].decode(), 0x13579)
    elif address == 0x209d704:
        contract, result = 'int', v['result']
        if result:
            event('stop-friend', 9 if result in [1, 2] else 6, -71000 - {1: 1, 2: 2, 3: 10, 4: 20}[result])
    elif address == 0x209d758:
        if v['result']:
            event('handle-gp', v['result'])
        else:
            kind = v['types'][0]
            if v['matches']:
                event('type', 0)
            if v['matches'] and kind and v['state'] == 1:
                refreshed = False
                for index in range(v['matches']):
                    event('refresh-one', LIST, 0, [111, 222][index])
                    if index == v['refresh']:
                        advance();memory[ARG][8:12] = word(0x601);refreshed = True;break
                if not refreshed:
                    found = False
                    for index in range(v['matches']):
                        profile = [111, 222][index]
                        event('buddy-index', CONNECTION, profile);event('handle-gp', 0)
                        if v['buddyIndices'][index] == -1:
                            event('send-request', profile);event('flag20', 0, 1)
                        else:
                            event('set-profile', 0, 111);event('mark-buddy', 0);query_flags(0, True);event('friend-callback', 0)
                            advance();memory[CONTROL][29] = 1;memory[ARG][8:12] = word(0x601);found = True;break
                    if not found and v['more'] != 0x600:
                        advance()
            elif not (v['matches'] and kind):
                if v['state'] == 1:
                    advance()
                else:
                    event('type', 0)
                    if kind == 0:
                        advance()
    elif address in [0x209d8f0, 0x209da68] and not v['result']:
        confirm, changed, already = False, False, False
        for index in range(max(0, v['count'])):
            kind = v['types'][index];event('type', index)
            matched = False
            if kind == 1:
                event('user-data');event('user-name', USERDATA, index)
                target = TOKEN if v['token'] else b'other-name'
                event('strcmp', TOKEN.decode(), target.decode())
                matched = v['token']
            else:
                event('type', index)
                if kind != 3:
                    event('type', index)
                if kind in [2, 3]:
                    event('user-data')
                    if address == 0x209d8f0:
                        event('format-code', 'ABCD');event('user-data')
                    event('get-profile', USERDATA, index)
                    matched = v['profileMatch']
                    if matched and address == 0x209d8f0:
                        actual = b'ABCD' if v['code'] else b'WXYZ'
                        event('memcmp', b'ABCD'.hex(), actual.hex(), 4);matched = v['code']
                    if matched and address == 0x209da68:
                        event('is-buddy', index)
                        if v.get('buddyFlags', [v['buddyAlready']] * 4)[index]:
                            already = True;continue
            if matched:
                if address == 0x209d8f0:
                    event('auth-request', CONNECTION, 77)
                    if kind == 1:
                        event('set-profile', index, 77)
                    query_flags(index, True);confirm = True
                else:
                    event('set-profile', index, 77);event('mark-buddy', index);query_flags(index);changed = True
        if address == 0x209d8f0:
            event('send-request', 77) if confirm else event('deny-request', CONNECTION, 77)
        elif changed:
            event('refresh-all', LIST, v['count'], 77)
            if not already:
                query_flags(v['refreshAll'], True);event('friend-callback', v['refreshAll'])
            memory[CONTROL][29] = 1
    return {at: bytes(raw) for at, raw in memory.items()}, events, contract, result & 0xffffffff
