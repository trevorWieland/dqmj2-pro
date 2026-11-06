import itertools


def base():
    return dict(ordinal=0, phase=100, effect=0, moveId=1, moveFlags=0, halfFlags=0, costField=5, moveNibbles=0, moveByte21=0, currentSide=0, currentSlot=0, lookupSide=0, enabled=[1, 1, 1], markers=[0, 0, 0], descriptorFlags=[0, 0, 0], values=[10, 20, 30], traits=[0] * 6, selection=-1, selectedWord=2, special=0, priorToken=0x81, tokenWord=0xFFFFFFFE, gate=1, policy=0, frameWord=0x10000, threshold6=5, threshold8=10, allowedWord=1, lowerCostWord=5, maximumWord=1000)


def profiles():
    output = []

    def add(**changes):
        p = base()
        p.update(changes)
        p['ordinal'] = len(output)
        output.append(p)

    for phase, effect, side in itertools.product([0, 10, 15, 20, 100, 110, 1, 255], [0, 1, -1, -32768], [0, 3, 4, 255]):
        index = len(output)
        add(phase=phase, effect=effect, lookupSide=side, currentSide=index % 4, currentSlot=index % 3, special=[0, 1, 255][index % 3], moveId=[1, 52, 53, 193, 511][index % 5], moveNibbles=[0, 1, 5, 0x405][index % 4], selection=[-1, 0, 2, -128, 127][index % 5], halfFlags=0x400 if index & 1 else 0, allowedWord=[0, 1, 0x80000000, 0xFFFFFFFF][index % 4], gate=[0, 1, 255][index % 3])
    for field, cost, multi, mask in itertools.product([0, 10000, 10001, 10002, 20000], [0, 1, -1, 32767, -32768], [0, 0x400], [0, 1, 7]):
        add(costField=field, lowerCostWord=cost & 0xFFFFFFFF, halfFlags=multi, values=[-1, 0, 32767], enabled=[(mask >> index) & 1 for index in range(3)])
    for trait, value, special in itertools.product(range(6), [-128, -1, 0, 1, 127], [0, 1, 255]):
        fields = [0] * 6
        fields[trait] = value
        add(traits=fields, special=special, moveFlags=[2, 8, 0x4000000, 4, 0x2000000, 0][trait], moveNibbles=0x400, moveByte21=0x2B)
    for word, six, eight in itertools.product([0, 0xFFF, 0x1000, 0xFFFFFFFF, 0xFFFFF000, 0x7FFFFFFF, 0x80000000], [0, 1, 0x80000000, 0xFFFFFFFF], [0, 10]):
        add(phase=20, frameWord=word, threshold6=six, threshold8=eight, effect=1)
    for marker, descriptor, gate, allowed in itertools.product([0, 1, 128, 255], [0, 1, 255], [0, 1], [0, 0xFFFFFFFF]):
        add(markers=[marker, 0, 255], descriptorFlags=[descriptor, 1, 0], halfFlags=0x400, gate=gate, allowedWord=allowed, policy=255, moveFlags=0x20000)
    for move, policy, flags in itertools.product([0, 52, 53, 193, 511], [0, 1, 2, 255], [0, 0x20000]):
        add(moveId=move, policy=policy, moveFlags=flags)
    return output
