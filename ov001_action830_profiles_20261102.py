import itertools
from ov001_action822_profiles_20261102 import base


def profiles():
    output = []

    def add(**changes):
        p = base()
        p.update(actionPhase=100, context10=0, context13=0, oldToken=0x80, rowHalf=1, opponentFlags=[0, 0, 0], timerWord=0, statusWord=0)
        p.update(changes)
        p['ordinal'] = len(output)
        output.append(p)

    for phase, category in itertools.product([0, 5, 10, 15, 20, 25, 30, 100, 1, 255], range(16)):
        n = len(output)
        add(actionPhase=phase, moveNibbles=0xF0F0 | (category << 8), effect=[-32768, -1, 0, 1, 32767][n % 5], lookupSide=[0, 1, 3, 255][n % 4], currentSide=n % 4, currentSlot=n % 3, tokenWord=[0, 127, 128, 255, 0x80000180, 0xFFFFFFFF][n % 6], timerWord=[0, 1, 0x80000000, 0xFFFFFFFF][n % 4], statusWord=n % 2, moveByte21=[0, 1, 255][n % 3], rowHalf=[0, 1, 65535][n % 3])
    for category, first, second, move in itertools.product([0, 7, 9], [0, 1, 255], [0, 1, 255], [1, 0xB6]):
        add(actionPhase=0, moveNibbles=category << 8, context10=first, context13=second, moveId=move)
    for token, timer, effect, phase in itertools.product([0, 127, 128, 255, 0x80000180, 0xFFFFFFFF], [0, 1, 0x80000000, 0xFFFFFFFF], [0, -1, 1, -32768], [15, 20]):
        add(actionPhase=phase, tokenWord=token, oldToken=token & 255, timerWord=timer, effect=effect, moveByte21=255, rowHalf=65535)
    for mask, marker, descriptor, flag in itertools.product(range(8), [0, 1, 255], [0, 1, 255], [0, 0x8000]):
        add(opponentFlags=[-128 if mask & (1 << i) else 0 for i in range(3)], markers=[marker, 0, 0], descriptorFlags=[descriptor, 0, 0], halfFlags=flag)
    for category, high in itertools.product(range(16), [0, 0x00F0, 0xF0F0]):
        add(moveNibbles=high | (category << 8), halfFlags=0x8000, opponentFlags=[0, 127, 0], markers=[0, 128, 0])
    for side, flaggedSide, index in itertools.product([0, 1, 2, 3, 255], range(4), range(3)):
        flags = [[0, 0, 0] for unused in range(4)]
        flags[flaggedSide][index] = -128
        add(lookupSide=side, flagsBySide=flags, halfFlags=0x8000)
    return output
