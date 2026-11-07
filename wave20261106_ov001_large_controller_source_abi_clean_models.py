from wave20261106_arm7_wl_followon_source_receive_fixture import Plan, SP, STOP, p32

STATE = 0x022497e8
BANKS = [0x02236f6c, 0x022362ac, 0x022355ec, 0x02237c2c]
CHILDREN = 0x02724000
RECORDS = 0x02730000


def word(value):
    return value & 0xffffffff


def signed(value):
    return value - 256 if value & 128 else value


def fixtures():
    result = []
    for state in [0, 5, 10, 20, 30, 40, 100, 1, 255]:
        for counter in [0, 29, 30, 31, 44, 45, 46, 254, 255]:
            n = len(result)
            result.append(dict(entry=0x0222c338, state=state, counter=counter,
                               selector=[0, 1, 2, 3, 255][n % 5], mask=n & 7,
                               mutateSelector=n % 2, seed=n))
    return result


def scenario(f, ordinal):
    p = Plan(ordinal, 40)
    p.buffers.clear()
    p.initial.clear()
    p.regions.clear()
    p.buffer(STATE, 12, 0x69)
    p.buffer(CHILDREN, 12 * 256, 0x83)
    p.buffer(RECORDS, 256 * 40, 0x94)
    p.buffer(SP - 40, 4, 0xa5)
    p.args = []
    p.allowed.append((STATE, STATE + 9))
    p.write(STATE, bytes([f['selector']]))
    p.write(STATE + 7, bytes([f['counter'], f['state']]))
    for bank, base in enumerate(BANKS):
        p.buffer(base, 3 * 0x440, 0xb7)
        for slot in range(3):
            address = base + slot * 0x440
            child = CHILDREN + (bank * 3 + slot) * 256
            p.u32(address + 0x1e8, child)
            p.write(address + 0x31c, bytes([(f['mask'] >> slot) & 1]))
            p.write(address + 0x1ff, b'\0')
            p.write(child + 0xac, b'\0')
            p.write(address + 0x234, bytes([[128, 255, 0, 127][(slot + f['seed']) % 4]]))
    p.capture()
    p.action(0x0207afec, [0xd7], RECORDS + 40 * 0xd7)
    state, counter, selector = f['state'], f['counter'], f['selector']
    if state == 0:
        changes = []
        if f['mutateSelector']:
            selector = (selector + 1) & 3
            changes = [(STATE, bytes([selector]))]
        p.action(0x021d7f54, [f['selector']], mutations=changes)
        p.write(STATE, bytes([selector]))
        p.action(0x021f1354, [1, 0, 0x31, 1])
        mapped = selector if selector in [0, 1] else 2
        p.action(0x021f1414, [selector], mapped)
        p.action(0x021f1438, [mapped])
        counter, state = 0, 5
        p.write(STATE + 7, bytes([counter, state]))
    if state == 5:
        counter = (counter + 1) & 255
        if counter > 30:
            state = 10
        p.write(STATE + 7, bytes([counter, state]))
    if state == 10:
        for slot in range(3):
            address = BANKS[selector] + slot * 0x440 if selector < 4 else 0
            p.action(0x021db438, [selector, slot], address)
            present = bool(address and p.read(address + 0x31c, 1)[0])
            p.action(0x021db8d0, [address], int(present))
            if present:
                changes = []
                if f['mutateSelector']:
                    selector = (selector + 1) & 3
                    changes = [(STATE, bytes([selector]))]
                p.u32(SP - 40, 0)
                p.action(0x021dbf98, [address, 8, 1, 0xffffffff, 0], mutations=changes)
                p.write(STATE, bytes([selector]))
        counter, state = 0, 20
        p.write(STATE + 7, bytes([counter, state]))
    elif state == 20:
        counter = (counter + 1) & 255
        if counter > 30:
            state = 30
        p.write(STATE + 7, bytes([counter, state]))
    elif state == 30:
        changes = []
        for bank in BANKS:
            for slot in range(3):
                address = bank + slot * 0x440 + 0x234
                raw = bytes([[255, 128, 127, 0][(f['seed'] + slot) % 4]])
                changes.append((address, raw))
                p.write(address, raw)
        p.action(0x021f14a4, mutations=changes)
        for slot in range(3):
            address = BANKS[selector] + slot * 0x440 if selector < 4 else 0
            p.action(0x021db438, [selector, slot], address)
            present = bool(address and p.read(address + 0x31c, 1)[0])
            p.action(0x021db8d0, [address], int(present))
            if present:
                p.action(0x021ee91c, [address, word(signed(p.read(address + 0x234, 1)[0]))])
        counter, state = 0, 40
        p.write(STATE + 7, bytes([counter, state]))
    elif state == 40:
        counter = (counter + 1) & 255
        if counter > 45:
            state = 100
        p.write(STATE + 7, bytes([counter, state]))
    if state == 100:
        state = 0
        p.write(STATE + 8, b'\0')
        p.write(STATE + 1, b'\7')
    p.returned = 0
    result = p.finish()
    result.update(sramReads=[], sramWrites=[], sramFault='none', expectedMmioReads=[],
                  faultRegisters=[], spiReadScript=[], instructionBudget=10000,
                  expectedTableReads=[], expectedFlagReads=[])
    return result
