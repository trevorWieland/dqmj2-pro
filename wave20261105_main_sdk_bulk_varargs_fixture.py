import struct
import wave20261104_main_front_eighth_common as H
from wave20261105_main_sdk_bulk_system_fixture import Machine, BANK, BANK_BYTES
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_PC


def invoke(address, code, case):
    kind = case['kind']
    memory = bytearray([0xa5] * 0x8000)
    dest, work, status, text, arguments = [H.RAM + value for value in [0x1000, 0x2000, 0x3000, 0x4000, 0x5000]]
    buffer = H.RAM + 0x6000
    def word(pointer, value):
        struct.pack_into('<I', memory, pointer - H.RAM, value & 0xffffffff)
    def half(pointer, value):
        struct.pack_into('<H', memory, pointer - H.RAM, value & 65535)
    extra = []
    if kind in ['fill', 'copy']:
        structure = H.RAM + 0x800
        word(structure, case['capacity'])
        word(structure + 4, dest)
        word(structure + 8, dest)
        memory[text - H.RAM:text - H.RAM + 64] = bytes(range(64))
        args = [structure, case['character'] if kind == 'fill' else text, case['count']]
    elif kind == 'send':
        values = case['values']
        complete = [case['api'], len(values), *values]
        args, extra = complete[:4], complete[4:]
    elif kind == 'state':
        values = case['values']
        complete = [len(values), *values]
        args, extra = complete[:4], complete[4:]
        word(work + 4, status)
        half(status, case['now'])
    else:
        memory[text - H.RAM:text - H.RAM + len(case['format']) + 1] = case['format'] + bytes(1)
        string = H.RAM + 0x7000
        memory[string - H.RAM:string - H.RAM + 7] = b'abcdef\0'
        payload = bytearray()
        for value, width in case['values']:
            actual = string if value == 'string' else H.RAM + 0x7100 if value == 'count' else value
            payload.extend((actual & ((1 << (width * 8)) - 1)).to_bytes(width, 'little'))
        memory[arguments - H.RAM:arguments - H.RAM + len(payload)] = payload
        args = [dest, case['capacity'], text, arguments]
    machine = Machine(address, code, memory, args)
    bank = bytearray(BANK_BYTES)
    struct.pack_into('<I', bank, 4, work)
    machine.uc.mem_write(BANK, bytes(bank))
    entry_sp = machine.initial[13]
    for index, value in enumerate(extra):
        machine.uc.mem_write(entry_sp + index * 4, struct.pack('<I', value & 0xffffffff))
    var_start = entry_sp - (8 if kind == 'send' else 12)
    var_end = var_start + (len(case.get('values', [])) * 4)
    reads = []
    def read(uc, access, where, size, value, unused):
        if kind in ['send', 'state'] and var_start <= where < var_end:
            reads.append((where, size))
    def put(pointer, data):
        assert H.RAM <= pointer and pointer + len(data) <= H.RAM + 0x8000 or H.STACK <= pointer and pointer + len(data) <= H.STACK + 0x10000
        machine.provide(pointer, data)
    def get_word(pointer):
        return struct.unpack('<I', machine.uc.mem_read(pointer, 4))[0]
    def string_call(pc, args):
        structure = args[0]
        remaining, current, base = struct.unpack('<III', machine.uc.mem_read(structure, 12))
        if pc == 0x0201A594:
            if remaining:
                put(current, bytes([args[1] & 255]))
                put(structure, struct.pack('<I', remaining - 1))
            put(structure + 4, struct.pack('<I', current + 1))
        else:
            count = H.signed(args[2])
            if count > 0:
                length = min(remaining, count)
                content = bytes([args[1] & 255]) * length if pc == 0x0201A5C4 else bytes(machine.uc.mem_read(args[1], length))
                if length:
                    put(current, content)
                put(structure, struct.pack('<I', remaining - length))
                put(structure + 4, struct.pack('<I', current + count))
    def step(uc, pc, size, unused):
        args = machine.arguments()
        if pc == 0x0201184C and kind == 'send':
            machine.calls.append(('provided-command-buffer',))
            machine.finish_call(buffer if case['available'] else 0)
        elif pc == 0x0200A440 and kind == 'send':
            assert args[:3] == [10, buffer, 0]
            machine.calls.append(('provided-PXI-send', args[:3]))
            machine.finish_call(case['sendResult'])
        elif pc == 0x02006E24 and kind == 'send':
            assert args[:3] == [BANK + 8, buffer, 1]
            machine.calls.append(('provided-queue-send', args[:3]))
            machine.finish_call(1)
        elif pc == 0x020119D0 and kind == 'state':
            machine.calls.append(('provided-check-initialized',))
            machine.finish_call(case['initializedResult'])
        elif pc in [0x020072D0, 0x020072EC] and kind in ['state', 'send']:
            assert args[:2] == ([status, 2] if kind == 'state' else [buffer, 256])
            machine.calls.append(('provided-cache-range', args[:2]))
            machine.finish_call(0)
        elif kind == 'format' and pc in [0x0201A594, 0x0201A5C4, 0x0201A618]:
            machine.calls.append(('provided-string-operation', pc, args[:3]))
            string_call(pc, args)
            machine.finish_call(0)
        elif kind == 'format' and pc == 0x020260DC:
            numerator, denominator = args[0] | args[1] << 32, args[2] | args[3] << 32
            assert denominator in [8, 10, 16]
            quotient = numerator // denominator
            machine.calls.append(('provided-unsigned64-quotient', numerator, denominator))
            machine.finish_call(quotient & 0xffffffff)
            machine.uc.reg_write(H.REGISTERS[1], quotient >> 32)
        elif not address <= pc < address + len(code):
            raise ValueError('Unprovided variadic/formatter callee attempted: ' + hex(pc))
    machine.uc.hook_add(UC_HOOK_CODE, step)
    machine.uc.hook_add(UC_HOOK_MEM_READ, read)
    machine.uc.emu_start(address, H.STOP, count=100000)
    assert machine.uc.reg_read(UC_ARM_REG_PC) == H.STOP
    state = machine.snapshot(True)
    state['variadicArgumentReads'] = reads
    if kind in ['fill', 'copy']:
        count = max(0, H.signed(case['count']))
        length = min(case['capacity'], count)
        expected = bytes([case['character'] & 255]) * length if kind == 'fill' else bytes(range(length))
        assert bytes(machine.uc.mem_read(dest, 64)) == expected + bytes([0xa5]) * (64 - length)
        assert struct.unpack('<III', machine.uc.mem_read(structure, 12)) == (case['capacity'] - length, dest + count, dest)
    elif kind == 'send':
        expected = 8 if not case['available'] or H.signed(case['sendResult']) < 0 else 2
        assert state['registers'][0] == expected
        assert len(machine.calls) == (4 if case['available'] else 1)
        if case['available']:
            assert struct.unpack('<H', machine.uc.mem_read(buffer, 2))[0] == case['api'] & 65535
            assert bytes(machine.uc.mem_read(buffer + 2, 2)) == bytes([0xa5]) * 2
            assert [get_word(buffer + 4 + index * 4) for index in range(len(values))] == [value & 0xffffffff for value in values]
        assert reads == ([(var_start + index * 4, 4) for index in range(len(values))] if case['available'] else [])
    elif kind == 'state':
        expected = case['initializedResult'] or (0 if case['now'] in values else 3)
        assert state['registers'][0] == expected
        assert reads == ([(var_start + index * 4, 4) for index in range(len(values))] if case['initializedResult'] == 0 else [])
    else:
        expected, capacity = case['expected'], case['capacity']
        content = expected[:max(0, capacity - 1)] + bytes(1) if capacity else b''
        assert bytes(machine.uc.mem_read(dest, 96)) == content + bytes([0xa5]) * (96 - len(content)), (case, bytes(machine.uc.mem_read(dest, 32)))
        assert state['registers'][0] == len(expected), (case, state['registers'][0])
        if case.get('storedCount') is not None:
            assert get_word(H.RAM + 0x7100) == case['storedCount']
    return state


def cases(address):
    if address in [0x0201A5C4, 0x0201A618]:
        return [dict(kind='fill' if address == 0x0201A5C4 else 'copy', capacity=capacity, count=count, character=character)
            for capacity in [0, 1, 8, 32] for count in [0, 1, 7, 40, 0xffffffff] for character in [0x41, 0x180]]
    words = [0, 0xffffffff, 0x80000000, 0x7fffffff, 0x12345678, 3, 0x12340003, 65535, 17, 9]
    if address == 0x020118A4:
        return [dict(kind='send', api=api, values=words[:count], available=available, sendResult=result)
            for api in [3, 0xffffa123] for count in [0, 1, 2, 3, 7, 10] for available, result in [(False, 0), (True, 0), (True, 0xffffffff)]]
    if address == 0x02011A34:
        return [dict(kind='state', now=now, values=words[:count], initializedResult=result)
            for now in [0, 3, 65535] for count in [0, 1, 2, 3, 5, 8] for result in [0, 3]]
    if address != 0x0201A670:
        return []
    samples = [(b'', [], b''), (b'abc', [], b'abc'), (b'%d', [(-1, 4)], b'-1'), (b'%d', [(-2147483648, 4)], b'-2147483648'),
        (b'%u', [(0xffffffff, 4)], b'4294967295'), (b'%08x', [(0x123ab, 4)], b'000123ab'), (b'%#08X', [(0xab, 4)], b'%#08X'),
        (b'%08X', [(0xab, 4)], b'000000AB'),
        (b'%-8s', [('string', 4)], b'abcdef  '), (b'%.3s', [('string', 4)], b'abc'), (b'%*.*d', [(8, 4), (4, 4), (12, 4)], b'    0012'),
        (b'%hhd', [(0x80, 4)], b'-128'), (b'%hhu', [(0x1234, 4)], b'52'), (b'%hd', [(0x8000, 4)], b'-32768'),
        (b'%llu', [(0xffffffffffffffff, 8)], b'18446744073709551615'), (b'%llx', [(0xfedcba9876543210, 8)], b'fedcba9876543210'),
        (b'%d:%llx', [(7, 4), (0x1122334455667788, 8)], b'7:1122334455667788'), (b'%%:%c', [(65, 4)], b'%:A'),
        (b'\x82\xa0x:%d', [(3, 4)], b'\x82\xa0x:3'), (b'abc%nEND', [('count', 4)], b'abcEND')]
    return [dict(kind='format', format=fmt, values=values, expected=expected, capacity=capacity, storedCount=3 if b'%n' in fmt else None)
        for fmt, values, expected in samples for capacity in [0, 1, 2, 8, 32]]


def prove(row, linked):
    address = int(row['address'], 0)
    native = H.IMAGE[address - H.BASE:address - H.BASE + row['bytes']]
    selected = cases(address)
    for case in selected:
        assert invoke(address, native, case) == invoke(address, linked, case)
    return dict(address=row['address'], modelCases=len(selected), actualNativeAndSourceCallerReturns=2 * len(selected),
        completeGprCpsrRamStackCommonBankOrderedWriteCallAndVariadicHomeReadComparison=True, providedCalleeSourceOrExecutionCredit=0,
        limits='Bounded supplied initialization/cache/PXI/queue/string/unsigned-division contracts only; no supplied native callee, radio, queue or hardware execution credit.')
