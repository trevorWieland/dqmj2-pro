import struct
from project import ROOT
import wave20261104_main_front_eighth_common as H
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC

TGID = 0x020DCE84


class Machine(H.Machine):
    def store(self, uc, kind, where, size, value, unused):
        if TGID <= where and where + size <= TGID + 4:
            self.writes.append(('caller', where, size, value))
        else:
            super().store(uc, kind, where, size, value, unused)

    def snapshot(self, returned):
        state = super().snapshot(returned)
        state['tgid'] = struct.unpack('<I', self.uc.mem_read(TGID, 4))[0]
        return state


def invoke(address, code, case):
    memory = bytearray(0x8000)
    kind = case['kind']
    if kind == 'elements':
        desc, output = H.RAM + 0x100, H.RAM + 0x2000
        struct.pack_into('<H', memory, 0x100, case['length'])
        struct.pack_into('<HH', memory, 0x100 + 60, case['gameInfoLength'], case['count'])
        memory[0x140:0x140 + len(case['payload'])] = case['payload']
        args = [output, desc]
    elif kind == 'forward':
        args = [H.RAM + 0x400, 0x02014578, case['dma'], case['blink']]
    elif kind == 'tgid':
        args = []
    else:
        raise ValueError('Unknown measured SDK fixture')
    machine = Machine(address, code, memory, args)
    if kind == 'tgid':
        machine.uc.mem_write(TGID, struct.pack('<I', case['initial']))
    def step(uc, pc, size, unused):
        registers = machine.arguments()
        if pc == 0x0201278C and kind == 'forward':
            expected = [args[0], args[1], case['dma'], 1 if case['blink'] else 3]
            assert registers == expected, (registers, expected)
            machine.calls.append(('provided-WM-initialize', registers))
            machine.finish_call(case['result'])
        elif pc == 0x0200F304 and kind == 'tgid':
            machine.calls.append(('provided-RTC-init',))
            machine.finish_call(0)
        elif pc == 0x0200F48C and kind == 'tgid':
            destination = registers[0]
            assert H.STACK <= destination < H.STACK + 0x10000 - 12
            machine.calls.append(('provided-RTC-get-time', destination))
            if case['rtcResult'] == 0:
                machine.provide(destination, struct.pack('<iii', 9, case['minute'], case['second']))
            machine.finish_call(case['rtcResult'])
        elif not address <= pc < address + len(code):
            raise ValueError('SDK fixture attempted unprovided callee execution: ' + hex(pc))
    machine.uc.hook_add(UC_HOOK_CODE, step)
    machine.uc.emu_start(address, H.STOP, count=50000)
    assert machine.uc.reg_read(UC_ARM_REG_PC) == H.STOP
    state = machine.snapshot(True)
    if kind == 'elements':
        expected = 0 if case['gameInfoLength'] else min(case['count'] & 255, 16)
        consumed, cursor, parsed = 0, 0, []
        available = (case['length'] * 2 - 64) & 255
        for index in range(expected):
            element = case['payload'][cursor:]
            identifier, length = element[0], element[1]
            parsed.append((identifier, length, desc + 64 + cursor + 2))
            cursor += (length + 2) & 255
            consumed = (consumed + ((length + 2) & 255)) & 255
            if consumed > available:
                expected = 0
                break
        result = bytes(machine.uc.mem_read(output, 132))
        assert result[0] == expected, (result[0], expected, case)
        for index, (identifier, length, body) in enumerate(parsed):
            offset = 4 + index * 8
            assert result[offset:offset + 2] == bytes([identifier, length])
            assert struct.unpack_from('<I', result, offset + 4)[0] == body
    elif kind == 'forward':
        assert len(machine.calls) == 1 and state['registers'][0] == case['result']
    else:
        initial = case['initial']
        if initial == 65536 and case['rtcResult'] == 0:
            initial = (case['second'] + (case['minute'] << 8)) & 65535
        expected = (initial + 1) & 65535
        assert state['tgid'] == state['registers'][0] == expected
        assert len(machine.calls) == (2 if case['initial'] == 65536 else 0)
    return state


def cases(address):
    if address == 0x02012774:
        return [dict(kind='forward', dma=dma, blink=blink, result=result) for dma in [0, 3, 65535] for blink in [0, 1, 0x80000000] for result in [0, 7]]
    if address == 0x020125BC:
        result = [dict(kind='tgid', initial=n, rtcResult=0, minute=0, second=0) for n in [0, 1, 65534, 65535, 65537, 0xffff0000, 0xffffffff]]
        result += [dict(kind='tgid', initial=65536, rtcResult=r, minute=m, second=s) for r in [0, 1] for m, s in [(0, 0), (59, 59), (255, 255), (256, 65535)]]
        return result
    if address != 0x02012464:
        return []
    result = []
    for count in [0, 1, 2, 15, 16, 17, 255, 256]:
        for available in [0, 2, 32]:
            payload = bytes(v for i in range(32) for v in [i + 1, 0]) + bytes(512)
            result.append(dict(kind='elements', count=count, length=32 + available // 2, gameInfoLength=0, payload=payload))
    result += [dict(kind='elements', count=16, length=48, gameInfoLength=n, payload=bytes(512)) for n in [1, 65535]]
    for length in [1, 2, 253, 254, 255]:
        payload = bytes([42, length]) + bytes(510)
        result.append(dict(kind='elements', count=1, length=48, gameInfoLength=0, payload=payload))
    payload = bytearray(512)
    payload[:2] = bytes([41, 252])
    payload[254:256] = bytes([42, 0])
    result.append(dict(kind='elements', count=2, length=159, gameInfoLength=0, payload=bytes(payload)))
    return result


def prove(row, linked):
    address = int(row['address'], 0)
    original = H.IMAGE[address - H.BASE:address - H.BASE + row['bytes']]
    selected = cases(address)
    for case in selected:
        assert invoke(address, original, case) == invoke(address, linked, case)
    return dict(address=row['address'], modelCases=len(selected), actualNativeAndSourceCallerReturns=2 * len(selected), completeGprCpsrMemoryStackOrderedWriteAndProvidedCallComparison=True, suppliedRtcInitializerCalleeExecutionCredit=0, limits='Bounded supplied RTC/WM call contracts only; no native callee, hardware, radio, time or protocol execution credit.')
