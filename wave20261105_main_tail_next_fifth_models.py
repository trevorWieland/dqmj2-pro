import itertools
import struct

SPECS = {name: {} for name in ['020cff18', '020d0a24', '020d0a74']}
SP, STOP, STATE = 0x027f0000, 0x027e0000, 0x021d6b48
WIDGETS = [0x02400100 + i * 256 for i in range(4)]
TABLES = [0x02401000, 0x02401100]


def word(value):
    return struct.pack('<I', value & 0xffffffff)


def fixtures(name):
    if name == '020d0a24':
        return [dict(count=n) for n in list(range(101)) + [-1000, -25, -24, -23, -12, -11, -1, 101, 127, 1000]]
    if name == '020cff18':
        return [dict(count=n, pages=p, flags=f, shared=s, mutate=m) for n, p, f, s, m in itertools.product(
            [0, 1, 12, 13, 24, 25, 100], [(0, 0), (1, 1), (2, 2), (7, 3), (255, 0)],
            [0, 3, 0xfffffffd], [False, True], [False, True])]
    return [dict(count=n, x=x, y=y, page=p, side=s, entries=e, mutate=m)
            for n, (x, y), p, s, e, m in itertools.product([0, 1, 12, 13, 25, 100], [(0, 0), (3, 2), (1, 1), (2, 0)],
            [0, 1, 8], [0, 1], [False, True], [False, True])]


def scenario(name, f, ordinal):
    regions = {STATE - 16: bytearray((i * 31 + ordinal * 7) & 255 for i in range(64))}
    for index, address in enumerate(WIDGETS):
        regions[address] = bytearray((i * 13 + index * 19 + ordinal) & 255 for i in range(128))
    for index, address in enumerate(TABLES):
        regions[address] = bytearray().join(word(0x02450000 + index * 0x1000 + i * 16) + word(i ^ 0xa5a50000) for i in range(12))

    def set_bytes(address, raw):
        for base, region in regions.items():
            if base <= address and address + len(raw) <= base + len(region):
                region[address-base:address-base+len(raw)] = raw
                return
        raise ValueError('Independent pagination model write escaped its exact regions')

    def get_word(address):
        for base, region in regions.items():
            if base <= address and address + 4 <= base + len(region):
                return int.from_bytes(region[address-base:address-base+4], 'little')
        raise ValueError('Independent pagination model read escaped its exact regions')

    set_bytes(STATE+12, word(WIDGETS[0]))
    set_bytes(STATE+16, word(WIDGETS[0] if f.get('shared') else WIDGETS[1]))
    set_bytes(STATE+21, bytes([f.get('page', 0)]))
    set_bytes(STATE+24, word(TABLES[0] if f.get('entries') else 0))
    set_bytes(STATE+28, bytes([f.get('x', 0), f.get('y', 0), f.get('side', 0)]))
    for index, address in enumerate(WIDGETS):
        set_bytes(address+124, word(f.get('flags', 0x12345678) ^ (index * 0x10203040)))
    initial = {base: bytes(raw) for base, raw in regions.items()}
    actions = []

    def call(address, args, returned, mutations=None, checks=None):
        mutations = mutations or []
        for at, raw in mutations:
            set_bytes(at, raw)
        actions.append(dict(address=address, args=args, returned=returned & 0xffffffff, mutations=mutations, checks=checks or []))

    changes = []
    if f.get('mutate'):
        if name == '020d0a74':
            changes = [(STATE+21, bytes([(f['page']+1)%3])), (STATE+24, word(0 if f['entries'] else TABLES[1])),
                       (STATE+28, bytes([3-f['x'], 2-f['y'], 1-f['side']]))]
        else:
            changes = [(STATE+12, word(WIDGETS[2])), (STATE+16, word(WIDGETS[2] if f['shared'] else WIDGETS[3]))]
    call(0x020629e0, [], f['count'], changes)
    total = f['count'] + 11
    pages = abs(total)//12 * (-1 if total < 0 else 1)
    result = None
    if name == '020d0a24':
        result = pages & 0xffffffff
    elif name == '020d0a74':
        index = f['x'] + f['y']*4
        page = (f['page']+1)%3 if f['mutate'] else f['page']
        side = 1-f['side'] if f['mutate'] else f['side']
        entries = 0 if f['entries'] else TABLES[1] if f['mutate'] else 0
        if not f['mutate']:
            entries = TABLES[0] if f['entries'] else 0
        result = get_word(entries + index*8) if entries and page*12+index < f['count'] and side == 0 else 0
    else:
        for phase in range(2):
            enabled = False
            if pages != 1:
                changes = []
                if f['mutate']:
                    changes = [(STATE+12+phase*4, word(WIDGETS[2+phase]))]
                call(0x020d0a14, [], f['pages'][phase], changes)
                enabled = f['pages'][phase] > 0 if phase == 0 else f['pages'][phase] < pages-1
            pointer = get_word(STATE+12+phase*4)
            flags = get_word(pointer+124)
            set_bytes(pointer+124, word(flags | 2 if enabled else flags & ~2))
            if enabled:
                changes = [(STATE+16, word(WIDGETS[0]))] if f['mutate'] and phase == 0 else []
                call(0x02048a44, [pointer+8, 1], 0x24681357 + phase, changes, [(pointer+124, word(flags | 2))])
    return dict(initial=initial, regions={base: bytes(raw) for base, raw in regions.items()}, actions=actions, result=result)
