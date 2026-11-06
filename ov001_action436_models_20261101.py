import struct
from ov001_action436_machine_20261101 import BASE, ENTRY, CONTEXT, RNG, TABLE, MOVE, STATE, STACK, ROOTS, signed

def profiles():
    base = dict(side=0, targetSide=1, targetSlot=1, eligible=7, seed=339125669, skill=12, mode=0, initial29=255, context14=0, selector19=2, available=200, required=5, maximum=1000, randomTarget=False, upperKind=0, propertyA=0, actor255=0, actor236=0, actor1FD=0, state2D=3, moveFlag=0, rule=0, flag29=2882400128, newSlot=2, actor356=255, actor346=2309737967, busy=0, display=1, **{'class': 0})
    cases = [('retarget', {}), ('free-mode', dict(mode=1)), ('insufficient', dict(available=2)), ('rule-word', dict(rule=4294967295)), ('raw15', dict(actor255=128, moveFlag=33554432)), ('raw255-zero-flag', dict(actor255=128)), ('raw255-free-mode', dict(actor255=1, moveFlag=1, mode=1)), ('same-side', dict(targetSide=0)), ('upper-nibble', dict(upperKind=1)), ('raw236', dict(actor236=128)), ('class2', {'class': 2}), ('word0', dict(actor1FD=1, state2D=4, skill=0)), ('wordCB', dict(actor1FD=1, state2D=4, skill=203)), ('wordCC', dict(actor1FD=1, state2D=4, skill=204)), ('word-outside', dict(actor1FD=1, state2D=4, skill=205)), ('context14', dict(actor1FD=1, state2D=4, skill=203, context14=1)), ('propertyA', dict(propertyA=-1)), ('negative-required', dict(required=-3)), ('bounded-maximum', dict(required=-3, available=1000)), ('raw10000', dict(available=10000, required=150)), ('zero-value', dict(available=0, required=0))]
    rows = []
    for name, updates in cases:
        for side in range(2):
            for turn in range(3):
                row = base.copy()
                row.update(updates)
                row.update(name=f'{name}-side{side}-v{turn}', side=side, targetSide=side if name == 'same-side' else 1 - side, initial29=[255, 0, 128][turn], display=turn % 2, busy=turn % 2, flag29=[0, 255, 2882400128][turn], actor356=[0, 127, 2882400128][turn], actor346=[0, 65535, 2309737967][turn], newSlot=turn)
                rows.append(row)
    for rawclass in range(3):
        for side in range(2):
            for seed in [0, 1, 2147483647, 4294967295]:
                for mask in [1, 3, 7]:
                    row = base.copy()
                    row.update(name=f'random-class{rawclass}-side{side}-seed{seed}-mask{mask}', side=side, targetSide=1 - side, randomTarget=True, seed=seed, eligible=mask)
                    row['class'] = rawclass
                    rows.append(row)
    return rows

def model(result):
    p = result['profile']
    actor = result['actor']
    record = result['record']
    target = result['initialTarget']
    actors = result['actors']
    expected = bytearray(result['before'])
    events = []
    seed = p['seed']
    provided = 0

    def put(address, value, size):
        expected[address - BASE:address - BASE + size] = (value & (1 << size * 8) - 1).to_bytes(size, 'little')

    def event(kind, address, args, name=None):
        nonlocal provided
        row = dict(kind=kind, address=address, callerPreparedWords=[v & 4294967295 for v in args])
        if name is not None:
            row['name'] = name
        if kind == 'provided':
            provided += 1
        events.append(row)

    def service(address, name, args):
        event('provided', address, args, name)

    def native(address, args):
        event('native', address, args)

    def draw(limit):
        nonlocal seed
        native(33804948, [limit])
        seed = seed * 1103515245 + 12345 & 4294967295
        put(RNG, seed, 4)
        return (seed >> 16) % limit
    service(35560636, 'initialization', [])
    service(34058220, 'move-row', [p['skill']])
    if p['randomTarget']:
        native(33836252, [p['side'] * 3])
        if p['class'] == 0:
            value = draw(8)
            side = int(value < 3) if p['side'] == 0 else int(value >= 3)
        else:
            native(33836252, [p['side'] * 3])
            value = draw(2 if p['class'] == 1 else 4)
            side = int(value == 0) if p['side'] == 0 else int(value != 0)
        for trial in range(64):
            slot = draw(3)
            native(35501112, [side, slot])
            target = actors[side] + slot * 1088
            native(35502288, [target])
            if p['eligible'] >> slot & 1:
                break
        else:
            raise ValueError('436 deterministic random-target bound unsupported')
        put(CONTEXT + 84, target, 4)
    targetside = 0 if actors[0] <= target < actors[0] + 3 * 1088 else 1
    targetslot = (target - actors[targetside]) // 1088
    if p['mode'] == 1:
        required = 0
    else:
        native(35503408, [actor])
        service(34058820, 'required-value', [p['skill'], p['available'], record + 70])
        required = p['required']
    available = p['available']
    native(35503408, [actor])
    if p['initial29'] == 255:
        service(35591188, 'flag29', [p['side']])
        put(CONTEXT + 41, p['flag29'], 1)
    service(35715492, 'target-rule', [record + 70, p['skill'], CONTEXT + 18])
    if available >= required and p['rule'] == 0:
        native(35502132, [actor, required])
        native(35503408, [actor])
        value = available
        if available < 10000:
            if required == 10000:
                value = 0
            elif required == 10001:
                value = (available + 1) // 2
            else:
                native(35502028, [actor, -required])
                native(35503408, [actor])
                value = available - required
                if value < 0:
                    value = 0
                else:
                    native(35503344, [actor])
                    service(34063320, 'maximum-base', [actor + 492, record + 70])
                    maximum = min(p['maximum'], 9999)
                    if value > maximum:
                        native(35503344, [actor])
                        service(34063320, 'maximum-base', [actor + 492, record + 70])
                        value = maximum
            put(actor + 498, value, 2)
        service(35661012, 'resource-notify', [p['side'], 0, 0])
    special = False
    if p['actor255']:
        service(34058244, 'move-flag', [p['skill'], 33554432])
        special = p['moveFlag'] != 0 and p['mode'] != 1
    mark = False
    if special:
        state = 15
    elif available < required:
        state = 16
    elif p['rule'] != 0:
        state = 14
    elif p['side'] == targetside:
        state = 3
    else:
        service(34058220, 'move-row', [p['skill']])
        if p['upperKind'] == 1:
            state = 3
            mark = True
        elif p['actor236'] != 0:
            state = 3
            mark = True
        else:
            native(35502580, [actor])
            native(33836252, [p['side'] * 3])
            if p['class'] == 2:
                state = 7
            else:
                condition = False
                if p['actor1FD']:
                    service(33971592, 'state-pointer', [])
                    condition = p['state2D'] == 4 and p['skill'] in [0, 203, 204] and (p['context14'] == 0)
                if condition:
                    state = 3
                    mark = True
                else:
                    service(34058220, 'move-row', [p['skill']])
                    if p['propertyA'] != 0:
                        state = 1
                    else:
                        service(35595012, 'slot-selector', [target, p['skill'], p['selector19']])
                        put(CONTEXT + 29, int(p['newSlot'] != targetslot), 1)
                        native(35501112, [targetside, p['newSlot']])
                        target = actors[targetside] + p['newSlot'] * 1088
                        put(CONTEXT + 84, target, 4)
                        state = 2
    put(CONTEXT + 19, state, 1)
    if p['display']:
        service(35590804, 'display-notify', [16, 2])
    service(35525464, 'target-notify', [targetside])
    if mark:
        put(actor + 854, 1, 1)
    else:
        service(35589100, 'actor356', [actor])
        put(actor + 854, p['actor356'], 1)
    service(35589184, 'actor346', [actor])
    put(actor + 838, p['actor346'], 2)
    native(33590648, [actor + 846, 0, 6])
    put(actor + 846, 0, 6)
    service(35527112, 'busy', [])
    if p['busy'] == 0:
        service(35661160, 'actor-notify', [p['side'], 0])
    put(CONTEXT + 10, 0, 1)
    roots = {a for values in ROOTS.values() for a in values}
    actual = [e for e in result['events'] if e['kind'] == 'provided' or e['address'] in roots]
    if actual != events:
        for index, (a, b) in enumerate(zip(actual, events)):
            if a != b:
                raise ValueError(('436 independent call contract differs', p['name'], index, a, b))
        raise ValueError(('436 independent call count differs', p['name'], len(actual), len(events)))
    cut = STACK - 65536 - BASE
    end = STACK + 4096 - BASE
    after = result['after']
    if after[:cut] != expected[:cut] or after[end:] != expected[end:]:
        for address, (a, b) in enumerate(zip(after, expected)):
            if a != b and (not cut <= address < end):
                raise ValueError(('436 independent nonstack effect differs', p['name'], hex(BASE + address), a, b))
    if provided != result['providedCalls']:
        raise ValueError('436 provider accounting differs')
    return dict(rawState13=state, target=target, raw356=1 if mark else p['actor356'] & 255, rngState=seed, providedCalls=provided)
