import itertools
import ov001_dispatch849_machine_20261102 as M


def signed(value):
    value &= 0xFFFFFFFF
    return value - 0x100000000 if value & 0x80000000 else value


def profiles():
    output = []

    def add(**changes):
        n = len(output)
        p = dict(ordinal=n, phase=100, item=n % 256, itemByte=[0, 4, 255][n % 3], move=n % 1024, nibbles=(n * 71) & 65535, flagByte=n % 256, actorByte=[0, 1, 128, 255][n % 4], side=n % 4, gateByte=[0, 1, 255][n % 3], policyWord=[0, 1, 0xFFFFFFFF][n % 3], identifierWord=M.word(0xABCD0000 + n), pointerWord=0x02550000 + n * 4, frameWord=M.word(n * 7111), advanceWord=M.word(n * 7111 + 5), context29=n % 256)
        p.update(changes)
        output.append(p)

    for nibble, item, flag, value, actor in itertools.product(range(16), [0, 1, 255], [0, 1], [0, 4], [0, 1, 128]):
        add(nibbles=nibble * 4096 + 0xA5B, item=item, flagByte=flag, itemByte=value, actorByte=actor)
    for side, gate, policy in itertools.product([0, 1, 2, 3, 127, 128, 255], [0, 255], [0, 1, 0xFFFFFFFF]):
        add(phase=0, side=side, gateByte=gate, policyWord=policy)
    for frame, equal in itertools.product([0, 1, 4095, 4096, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF], [False, True]):
        add(phase=10, frameWord=frame, advanceWord=M.word((signed(frame) >> 12) + 5 + (not equal)))
    for phase in [1, 20, 127, 128, 255]:
        add(phase=phase)
    return output


def model(vm, result):
    p = vm.p
    state = bytearray(vm.beforeState)
    calls = []

    def emit(pc, *args):
        args = list(map(M.word, args))
        calls.append(dict(target=hex(pc), callerWords=args, suppliedReturn=M.word(vm.provider(pc, args))))

    if p['phase'] == 0:
        if p['gateByte'] == 0:
            emit(0x021F949C, 0xDD if p['side'] == 0 else 0xE0, 1)
            emit(0x021EAA3C, p['move'])
            emit(0x021F1438, p['context29'])
            state[0xA] = 2
            emit(0x021DBAAC, M.ACTOR)
            if p['policyWord']:
                emit(0x021D75D4, 0x29 if p['side'] == 0 else 0x25)
                emit(0x02042C2C, M.ACTOR)
                emit(0x021D77B0, 0xFFFFFFFF, p['identifierWord'])
                emit(0x02041F74, M.ACTOR, 0)
                emit(0x021D7814, 0xFFFFFFFF, p['pointerWord'])
                emit(0x021D94CC, int(p['side'] == 0), int(p['side'] == 1))
            else:
                emit(0x021D7E80, M.ACTOR)
            emit(0x021D9494, M.ACTOR, 2, 1)
            state[0xE] = 10
    elif p['phase'] == 10:
        emit(0x021D9534, M.ACTOR, 0xFFFFFFFF, 6, 0)
        if M.word(p['advanceWord'] - 5) == M.word(signed(p['frameWord']) >> 12):
            state[0xE] = 100
    elif p['phase'] == 100:
        state[0xE] = 0
        yes = p['nibbles'] >> 12 == 1
        yes |= p['item'] != 0 and p['flagByte'] & 1 != 0 and p['itemByte'] == 4
        yes |= p['actorByte'] != 0
        state[0x13] = 6 if yes else 5
    failures = []
    if result['registers'][0] != 0:
        failures.append('proper zero caller return')
    if result['calls'] != calls:
        failures.append('ordered raw-word service/Boolean contracts')
    if result['state'] != bytes(state):
        failures.append('independent phase/gate/raw selector transitions')
    if result['actor'] != vm.beforeActor or result['table'] != vm.beforeTable or result['move'] != vm.beforeMove:
        failures.append('supplied actor/tables remain unchanged')
    return failures
