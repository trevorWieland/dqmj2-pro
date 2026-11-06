import struct
import wave20261104_main_front_eighth_common as H
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC

ADDRESS = 0x02011AC8
BANK = 0x020E5D80
BANK_BYTES = 2720
USER = H.STOP + 0x100


class Machine(H.Machine):
    def store(self, uc, kind, where, size, value, unused):
        if BANK <= where and where + size <= BANK + BANK_BYTES:
            self.writes.append(('caller', where, size, value))
        else:
            super().store(uc, kind, where, size, value, unused)

    def snapshot(self, returned):
        state = super().snapshot(returned)
        state['commonBank'] = bytes(self.uc.mem_read(BANK, BANK_BYTES))
        return state


def invoke(code, case):
    memory = bytearray(0x8000)
    work, status, fifo, recv = H.RAM + 0x1000, H.RAM + 0x2000, H.RAM + 0x3000, H.RAM + 0x5000
    record = fifo if case['same'] else H.RAM + 0x4000
    def word(address, value):
        struct.pack_into('<I', memory, address - H.RAM, value)
    def half(address, value):
        struct.pack_into('<H', memory, address - H.RAM, value)
    word(work + 4, status)
    word(work + 16, fifo)
    half(work + 22, case['scan'])
    word(work + 332, 0x11)
    half(status + 114, 64)
    if case['callback']:
        for api in range(44):
            word(work + 24 + api * 4, USER)
        word(work + 200, USER)
        for port in [0, 5, 15]:
            word(work + 204 + port * 4, USER)
            word(work + 268 + port * 4, H.RAM + 0x6000 + port * 4)
    half(record, case['api'])
    half(record + 2, case['callbackError'])
    half(record + 8, case['state'])
    if case['api'] == 8:
        half(record + 16, case['aid'])
        half(record + 18, 0x7654)
        memory[record - H.RAM + 10:record - H.RAM + 16] = bytes(range(10, 16))
        memory[record - H.RAM + 20:record - H.RAM + 44] = bytes(range(24))
        half(record + 44, 0x1234)
        half(record + 46, 0x4321)
    elif case['api'] == 12:
        half(record + 10, case['aid'])
        half(record + 12, 0x7654)
        memory[record - H.RAM + 16:record - H.RAM + 22] = bytes(range(10, 16))
        half(record + 22, 0x1234)
        half(record + 24, 0x4321)
    elif case['api'] == 14:
        half(record + 4, case['state'])
        word(record + 8, recv)
    elif case['api'] == 129:
        word(record + 28, USER if case['callback'] else 0)
    elif case['api'] == 130:
        half(record + 6, 5)
        word(record + 8, recv)
    machine = Machine(ADDRESS, code, memory, [10, record, case['err']])
    initial_bank = bytearray(BANK_BYTES)
    struct.pack_into('<H', initial_bank, 0, 1)
    struct.pack_into('<I', initial_bank, 4, work)
    machine.uc.mem_write(BANK, bytes(initial_bank))
    terminated = False
    def read_half(address):
        return struct.unpack('<H', machine.uc.mem_read(address, 2))[0]
    def provide(address, data):
        assert H.RAM <= address and address + len(data) <= H.RAM + 0x8000 or BANK <= address and address + len(data) <= BANK + BANK_BYTES
        machine.provide(address, data)
    def step(uc, pc, size, unused):
        nonlocal terminated
        args = machine.arguments()
        if pc in [0x020072D0, 0x020072EC]:
            machine.calls.append(('invalidate' if pc == 0x020072D0 else 'store-range', args[0], args[1]))
            machine.finish_call(0)
        elif pc == 0x02011E74:
            machine.calls.append(('provided-clear-fifo-flag',))
            machine.finish_call(0)
        elif pc == 0x020117C4:
            machine.calls.append(('provided-WM-finish',))
            machine.finish_call(0)
        elif pc == 0x02008430:
            machine.calls.append(('termination-entry-stop',))
            terminated = True
            uc.emu_stop()
        elif pc in [0x02008D78, 0x02008BE0]:
            destination, value, count = (args[0], args[1], args[2]) if pc == 0x02008D78 else (args[1], args[0], args[2])
            unit = bytes([value & 255]) if pc == 0x02008D78 else struct.pack('<H', value & 65535)
            machine.calls.append(('provided-fill', pc, destination, value, count))
            provide(destination, (unit * ((count + len(unit) - 1) // len(unit)))[:count])
            machine.finish_call(0)
        elif pc in [0x02008E0C, 0x02008BF8]:
            source, destination, count = args[:3]
            machine.calls.append(('provided-copy', pc, source, destination, count))
            provide(destination, bytes(uc.mem_read(source, count)))
            machine.finish_call(0)
        elif pc == USER:
            argument = args[0]
            assert argument == record or argument == BANK + 80
            machine.calls.append(('provided-user-callback', argument, bytes(uc.mem_read(argument, 68))))
            if argument == record and case['disable']:
                provide(BANK, bytes(2))
            machine.finish_call(0)
        elif not ADDRESS <= pc < ADDRESS + len(code):
            raise ValueError('Unprovided SDK callee attempted: ' + hex(pc))
    machine.uc.hook_add(UC_HOOK_CODE, step)
    machine.uc.emu_start(ADDRESS, H.STOP, count=50000)
    assert machine.uc.reg_read(UC_ARM_REG_PC) == (0x02008430 if terminated else H.STOP)
    state = machine.snapshot(not terminated)
    assert terminated == (not case['err'] and case['api'] == 128 and case['callbackError'] == 19)
    calls = machine.calls
    users = [call for call in calls if call[0] == 'provided-user-callback']
    end = case['api'] == 2 and case['callbackError'] == 0
    disabled = case['api'] < 44 and case['callback'] and case['disable'] and not end
    normal = not case['err'] and not terminated and not end and not disabled
    expected_users = 0
    if not case['err'] and not terminated and case['callback']:
        expected_users = int(case['api'] < 44 or case['api'] in [128, 129, 130])
        if case['api'] in [8, 12] and case['state'] in [7, 9, 26] and not disabled:
            expected_users += 3
    assert len(users) == expected_users, (case, len(users), expected_users)
    assert sum(call[0] == 'provided-clear-fifo-flag' for call in calls) == int(normal)
    assert sum(call[0] == 'provided-WM-finish' for call in calls) == int(not case['err'] and end)
    assert sum(call[0] == 'store-range' for call in calls) == int(normal and not case['same'])
    if case['err']:
        assert not calls and all(H.STACK <= write[1] < H.STACK + 0x10000 for write in machine.writes)
    if not terminated:
        expected_api = 15 if case['api'] == 129 and not case['err'] else case['api']
        if normal and not case['same']:
            expected_api |= 0x8000
        assert read_half(record) == expected_api
    if normal and case['api'] in [8, 12] and case['state'] in [7, 9, 26]:
        aid, myaid = (case['aid'], 0) if case['api'] == 8 else (0, case['aid'])
        bitmap = 0x11 | (1 << aid) if case['state'] == 7 else 0x11 & ~(1 << aid)
        assert struct.unpack('<I', machine.uc.mem_read(work + 332, 4))[0] == bitmap
        assert read_half(work + 336) == myaid
        assert read_half(BANK + 80 + 6) == 15
        assert read_half(BANK + 80 + 34) == bitmap
        assert read_half(BANK + 80 + 64) == (0x1234 if myaid == 0 else 0x4321)
        assert read_half(BANK + 80 + 66) == (0x4321 if myaid == 0 else 0x1234)
    return state, terminated


def cases():
    base = dict(api=0, err=0, scan=0, same=False, callback=True, callbackError=0, state=0, aid=3, disable=False)
    result = [dict(base, api=api, scan=scan, same=same, callback=callback) for api in [0, 2, 8, 12, 14, 128, 129, 130, 131, 255] for scan, same in [(0, False), (1, True)] for callback in [False, True]]
    result += [dict(base, err=err) for err in [1, 0xffffffff]]
    result += [dict(base, api=128, callbackError=19)]
    result += [dict(base, api=api, state=state, aid=aid) for api in [8, 12] for state in [7, 9, 26] for aid in [0, 3, 15]]
    result += [dict(base, api=14, state=state, callbackError=error) for state in [11, 12] for error in [0, 1]]
    result += [dict(base, api=api, disable=True) for api in [0, 8, 12]]
    result += [dict(base, api=2, callbackError=1)]
    return result


def prove(row, linked):
    original = H.IMAGE[ADDRESS - H.BASE:ADDRESS - H.BASE + row['bytes']]
    selected = cases()
    stops = 0
    for case in selected:
        native = invoke(original, case)
        source = invoke(linked, case)
        assert native == source
        stops += int(native[1])
    return dict(modelCases=len(selected), actualNativeAndSourceCallerReturns=2 * (len(selected) - stops), nativeAndSourceTerminationEntryStops=2 * stops,
        completeGprCpsrRamStackCommonBankOrderedWriteAndProvidedCallComparison=True, suppliedCalleeSourceOrExecutionCredit=0,
        limits='Bounded supplied cache/WM/memory-copy/user-callback contracts; a terminate-entry stop is not a return or hardware execution.')
