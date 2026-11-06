import json
import random
import struct
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/itcm/large53/native_itcm_01ff97e0.c'
DEPENDENCIES = [ROOT / 'src/itcm/large53/context.h']
REPORT = ROOT / 'evidence/matches/itcm-large53.json'
ADDRESS = 0x01FF97E0
BASE = 0x021CEB54
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
SELECTORS = list(range(29)) + [29, 30, 255, 0xffffffff]


def fixture(selector, scenario, early, original):
    required = bytearray(original)
    query = [0, 1, 2, 0xffffffff][scenario % 4]
    probe = [1, 0, 1, 2, 1, 0, 2, 1, 0, 1, 1, 0][scenario]
    meta58 = [-1, 0, 1, 2][scenario % 4]
    meta59 = int(scenario in (2, 3, 6, 7, 8, 11))
    meta5a = [0, 1, -1][scenario % 3]
    mode, selected = scenario % 3, scenario * 3 % 8
    active = [0, 255, 255, 85, 170, 1 << selected, 129, 126, 16, 240, 15, 255][scenario]
    bad = 2 if scenario in (1, 4, 7, 10) else -1
    event = [0, 8, 1, 2, 0xff7, 0xffff][scenario % 6]
    timer = [0, 1, 29, 30, 45, 46, 90, 91, 65534, 65535, 0, 1][scenario]
    if selector == 17:
        timer = [0, 1, 90, 91, 91, 45, 91, 90, 65535, 91, 65535, 91][scenario]
    paused = 1 if early == 'paused' else 2 if scenario & 1 else 0
    gate = 1 if early == 'gated' else 2 if scenario & 1 else 0
    struct.pack_into('<H', required, 0, timer)
    struct.pack_into('<III', required, 4, paused, mode, selector)
    initial = bytes(required)
    calls, bank_results = [], {}
    flag_clear = False
    token = (0x81350000 + scenario * 79 + selector) & 0xffffffff
    meta_count = 0
    returned = (token + 2) & 0xffffffff
    def state(value):
        struct.pack_into('<I', required, 12, value)
    def counter(value):
        struct.pack_into('<H', required, 0, value & 65535)
    def call(address, *arguments):
        nonlocal meta_count
        arguments = [value & 0xffffffff for value in arguments]
        result = (address * 2654435761 + len(calls) * 40503 + scenario) & 0xffffffff
        if address == 0x02223c60:
            result = 0x03001000
        elif address == 0x02223c54:
            meta_count += 1
            result = 0x03002000
        elif address == 0x01ffb230:
            result = gate
        elif address == 0x01ff97a0:
            result = 0xc9700000 | scenario
        elif address == 0x01ffb340:
            result = 0x03003000
        elif address == 0x01ffb35c:
            result = 0x03006000
        elif address == 0x01ffa010:
            result = 0x03007000
        elif address == 0x01ffb4ec:
            result = 0x03008000 + arguments[0] * 0x200
        elif address == 0x01ffa824:
            result = 0xdead0000 | selected
        elif address == 0x01ffa84c:
            result = 0x31000000 | scenario
        elif address == 0x01ffa5fc:
            result = (0x44000000 | arguments[0]) if arguments[1] == 3 and arguments[0] < 8 else query
        elif address == 0x020687dc:
            index = arguments[0] & 255
            result = 0xffffffff if index == bad else 0x10000 + index
        elif address == 0x01ffa394:
            result = 1 if active & (1 << arguments[0]) else 2 if scenario & 1 else 0
        elif address == 0x01ffa6c0:
            result = (2 if scenario % 3 == 0 else 0) if arguments[1] == 2 else (0 if scenario % 3 == 1 else 1)
        elif address == 0x01ffa2fc:
            result = probe
        elif address == 0x020644c0:
            result = query
        calls.append({'address': address, 'arguments': arguments, 'result': result, 'global': bytes(required)})
        return result
    call(0x02223c60)
    call(0x02223c54)
    call(0x02223c54)
    if paused == 1:
        call(0x020885d0)
    elif call(0x01ffb230) == 1:
        if selector == 24:
            call(0x01ffa440)
    else:
        simple = {0: [0x01ffb4c4, 0x01ff86cc], 2: [0x01ffb4c4, 0x01ff883c],
                  3: [0x01ffb4c4, 0x01ff8964], 4: [0x01ffb4c4, 0x01ff8a4c],
                  5: [0x01ffb03c, 0x01ff8c50], 6: [0x01ff96bc], 16: [0x01ff8f5c],
                  18: [0x01ffb03c, 0x01ff9204], 24: [0x01ffb4c4, 0x01ff92cc], 26: [0x01ff951c]}
        if selector in simple:
            for address in simple[selector]:
                call(address)
        elif selector == 1:
            returned = call(0x01ff97a0)
        elif selector == 7:
            if meta58 == 1 and meta5a == 0:
                call(0x0205e7a8, -1, 0x57)
            call(0x01ffae9c, 16, 6, 3, -1)
            state(8)
            counter(0)
            call(0x01ffb060, 1)
            call(0x02061260, 1)
        elif selector == 8:
            counter(timer + 1)
            if (timer + 1) & 65535 > 45:
                state(9)
                if meta58 != 1:
                    call(0x01ffa348, 3)
                call(0x01ffafb8)
        elif selector == 9:
            call(0x02223c54)
            special = meta59 == 1 and mode == 2
            if special:
                required[16:64] = bytes(48)
            call(0x01ffa5ac, BASE + 16, 48, 3)
            if call(0x01ffa5fc, call(0x01ffa84c), 3):
                call(0x02223c54)
                found = False
                if not special:
                    for index in range(8):
                        if call(0x01ffa394, index) == 1:
                            call(0x01ffa824)
                            if index != selected:
                                handle = call(0x01ffa5fc, index, 3)
                                pointer = call(0x01ffb4ec, index)
                                result = call(0x020687dc, handle, pointer)
                                found |= result == 0xffffffff
                                call(0x01ffa824)
                                call(0x01ffb4ec, selected)
                                bank_results[selected] = result
                if found:
                    call(0x01ffae9c, 16, 6, 4, 0x57)
                state(10 if found else 11)
        elif selector == 10:
            call(0x01ffb35c)
            if event & 0xff7:
                state(11)
                call(0x01ffa824)
                call(0x01ffb4ec, selected)
                bank_results[selected] = 0xffffffff
        elif selector == 11:
            call(0x01ffafb8)
            call(0x01ffae9c, 16, 6, 6, 0x57)
            call(0x01ffb060, 1)
            state(12)
        elif selector == 12:
            call(0x02089644)
            call(0x02089454)
            call(0x02064488, 2)
            state(13)
        elif selector == 13:
            if call(0x020644c0):
                call(0x02089680)
                call(0x01ffafb8)
                call(0x01ffae9c, 16, 6, 8, 0x57)
                state(14)
                counter(0)
                call(0x01ffb060, 1)
                if mode == 1:
                    call(0x0205e814, 0, 0, 20)
        elif selector == 14:
            if timer < 30:
                counter(timer + 1)
            else:
                call(0x01ffa5ac, BASE + 16, 48, 4)
                if call(0x01ffa5fc, 0, 4):
                    call(0x01ffafb8)
                    state(1)
                    call(0x01ffa010)
                    flag_clear = True
                    call(0x02041538, 1, 2, 10)
        elif selector == 15:
            if call(0x01ffa2fc) == 1:
                call(0x02223c54)
                state(16)
                if meta58 == 1:
                    call(0x020620e8, 21, 1)
        elif selector == 17:
            counter(timer + 1)
            if timer > 90:
                state(4)
                call(0x01ffafb8)
                if meta58 == 1:
                    call(0x02061260, 0)
                    call(0x01ffac9c, 2, 0, 13, 1, 2, 2)
                elif mode == 1:
                    call(0x01ffac9c, 2, 0, 2, 3, 2, meta58 + 1)
                else:
                    call(0x01ffac9c, 2, 0, 7, 0, 0, 2)
        elif selector == 19:
            call(0x020889cc, 1)
            call(0x01ff8eec)
            call(0x01ffa5ac, BASE + 64, 52, 1)
            counter(timer - 1)
            if timer == 0:
                state(20)
                struct.pack_into('<I', required, 84, 1)
                call(0x01ffa5ac, BASE + 64, 52, 2)
                call(0x01ffafb8)
        elif selector in (20, 21, 27):
            if selector != 21:
                call(0x020889cc, 2)
            if call(0x01ffa5fc, 0, 2):
                state(22 if selector == 21 else 7)
                if selector == 21:
                    counter(10)
        elif selector == 22:
            counter(timer - 1)
            if timer == 0:
                state(6)
                call(0x01ffa804)
        elif selector == 23:
            call(0x01ff8f5c)
            call(0x01ffb35c)
            if event & 0xff7:
                call(0x01ffafb8)
                call(0x01ffae5c, 16, 15, 1, -1, 1)
                state(16)
                call(0x0205e7a8, -1, 0x52)
        elif selector == 25:
            if meta58 == 1:
                if call(0x01ffa6c0, 0, 2) or call(0x01ffa6c0, 0, 1):
                    state(26)
                    call(0x020620e8, 21, 1)
            elif call(0x01ffa5fc, 0, 1):
                state(26)
        elif selector == 28:
            if meta58 == 1:
                state(6)
                call(0x01ffa804)
                call(0x020620e8, 27, 1)
            elif call(0x01ffa5fc, 0, 2):
                state(6)
                call(0x01ffa804)
        call(0x01ffab90)
        call(0x01ffb340)
        if scenario & 1:
            call(0x0208870c)
        call(0x01ffa4b4)
    return {'initial': initial, 'required': bytes(required), 'calls': calls, 'return': returned,
            'meta': bytes(value & 255 for value in (meta58, meta59, meta5a)), 'event': event,
            'banks': bank_results, 'flagClear': flag_clear, 'token': token, 'metaCount': meta_count}


def execute(code, selector, scenario, early):
    rng = random.Random(20261027 + selector + scenario * 65537 + len(early))
    model = fixture(selector, scenario, early, rng.randbytes(256))
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for address, size in [(0x01ff8000, 0x8000), (0x02000000, 0x500000), (0x03000000, 0x20000), (0x05000000, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(ADDRESS, code)
    machine.mem_write(BASE, model['initial'])
    machine.mem_write(0x03001000, struct.pack('<I', model['token']))
    machine.mem_write(0x03002058, model['meta'])
    machine.mem_write(0x03003011, bytes([scenario & 1]))
    machine.mem_write(0x03006002, struct.pack('<H', model['event']))
    banks = [bytes(machine.mem_read(0x03008000 + index * 0x200, 0x200)) for index in range(8)]
    flag = bytes(machine.mem_read(0x03007000, 1))
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[-2:] = [0x0301fff0, 0x05000000]
    flags = rng.getrandbits(4) << 28 | 0x10 | (0x80 if scenario & 1 else 0)
    machine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(matcher.REGISTERS, registers):
        machine.reg_write(register, value)
    calls, writes, visited = [], [], set()
    meta_count = 0
    def write(uc, access, address, size, value, user):
        if not (BASE <= address and address + size <= BASE + 256 or 0x03000000 <= address and address + size <= 0x03020000):
            raise ValueError('Unexpected state-machine write outside covered storage')
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    def store(uc, address, payload):
        uc.mem_write(address, payload)
        writes.append([address, len(payload), payload.hex()])
    def trace(uc, address, size, user):
        nonlocal meta_count
        if ADDRESS <= address < ADDRESS + len(code):
            visited.add(address)
            return
        stage = len(calls)
        actual = [uc.reg_read(register) for register in matcher.REGISTERS[:4]]
        stack = struct.unpack('<II', bytes(uc.mem_read(uc.reg_read(matcher.REGISTERS[-2]), 8)))
        required = model['calls'][stage] if stage < len(model['calls']) else None
        if required is None or address != required['address'] or (actual + list(stack))[:len(required['arguments'])] != required['arguments']:
            raise ValueError({'failure': 'Independent state-machine API contract differs', 'selector': selector,
                              'scenario': scenario, 'early': early, 'stage': stage, 'address': hex(address),
                              'actual': actual + list(stack), 'required': required})
        if bytes(uc.mem_read(BASE, 256)) != required['global']:
            raise ValueError({'failure': 'Global transition ordering differs before helper', 'selector': selector, 'scenario': scenario, 'stage': stage})
        result = required['result']
        if address == 0x02223c54:
            meta_count += 1
            store(uc, 0x03001000, struct.pack('<I', (model['token'] + meta_count) & 0xffffffff))
        store(uc, 0x03010000 + stage * 4, struct.pack('<I', result))
        returned = uc.reg_read(matcher.REGISTERS[-1])
        calls.append({'address': hex(address), 'arguments': actual, 'stack': list(stack)})
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | (flags & 0x80))
        uc.reg_write(UC_ARM_REG_PC, returned)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.hook_add(UC_HOOK_CODE, trace)
    machine.emu_start(ADDRESS, 0x05000000, count=10000)
    if machine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != len(model['calls']):
        raise ValueError('State machine did not return after the independent expected protocol')
    if machine.reg_read(matcher.REGISTERS[0]) != model['return'] or bytes(machine.mem_read(BASE, 256)) != model['required']:
        raise ValueError('Independent state-machine return/global model differs')
    for index, original in enumerate(banks):
        required = bytearray(original)
        if index in model['banks']:
            struct.pack_into('<I', required, 0x168, model['banks'][index])
        if bytes(machine.mem_read(0x03008000 + index * 0x200, 0x200)) != bytes(required):
            raise ValueError('Independent selected-bank result model differs')
    if bytes(machine.mem_read(0x03007000, 1)) != (bytes(1) if model['flagClear'] else flag):
        raise ValueError('Independent flag-byte model differs')
    if struct.unpack('<I', bytes(machine.mem_read(0x03001000, 4)))[0] != (model['token'] + model['metaCount']) & 0xffffffff:
        raise ValueError('Pointer snapshot timing fixture failed')
    return {'registers': [machine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(machine.mem_read(address, size))) for address, size in
                             [(0x01ff8000, 0x8000), (BASE, 256), (0x03000000, 0x20000)]]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('State-machine C compiler pin changed')
    dependencies = [{'path': item.relative_to(ROOT).as_posix(), 'sha256': matcher.sha(item.read_bytes())} for item in DEPENDENCIES]
    report = json.loads(REPORT.read_text()) if REPORT.exists() else {'schemaVersion': 1, 'module': 'itcm', 'matches': [],
             'romSha256': matcher.sha((ROOT / 'inputs/game.nds').read_bytes()), 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if report['matches'] and (matcher.sha(SOURCE.read_bytes()) != report['matches'][0]['sourceSha256'] or dependencies != report['matches'][0]['sourceDependencies']):
        raise ValueError('Frozen state-machine C source or dependency changed')
    attempts, matches = matcher.compare(SOURCE, 'itcm', 2, 'off', True)
    if 'native_itcm_01ff97e0' not in matches:
        raise ValueError('Ordinary C state machine stopped matching all native bytes')
    entry, compiled = matches['native_itcm_01ff97e0']
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    native = binary[ADDRESS - 0x01ff8000:ADDRESS - 0x01ff8000 + entry['bytes']]
    records, visited, external = [], set(), 0
    for selector in SELECTORS:
        for early, scenarios in [('normal', range(12)), ('paused', [0]), ('gated', [0])]:
            for scenario in scenarios:
                expected, actual = execute(native, selector, scenario, early), execute(compiled, selector, scenario, early)
                if expected != actual:
                    raise ValueError('Native and recompiled state-machine effects differ')
                visited.update(expected['visited'])
                external += len(expected['calls']) * 2
                records.append({'selector': hex(selector), 'scenario': scenario, 'early': early,
                                'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['sourceDependencies'] = dependencies
    entry['oracle'] = {'vectors': len(records), 'nativeAndRecompiledCalls': len(records) * 2, 'syntheticExternalCalls': external,
                       'nativeCalleeCalls': 0, 'verifiedReturn': True, 'independentStateAndApiAssertions': True,
                       'instructionAddressesVisited': [hex(address) for address in sorted(visited)], 'records': records,
                       'limitations': ['All29 dispatch values, four defaults and both early exits are checked under bounded synthetic API contracts',
                                       'Independent assertions cover transition ordering, wrapped halfword timers, signed metadata, exact-one gates,48-byte clearing,8-bank results and cached-pointer read timing',
                                       'Explicit arguments including fifth/sixth outgoing stack arguments are checked; unspecified external prototypes remain provisional',
                                       'Synthetic callees clobber caller-saved registers and NZCV and write isolated scratch; native external bodies and physical gameplay are not executed or credited']}
    report.update(matches=[entry], attempts=attempts, moduleInputSha256=matcher.sha(binary),
                  nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': len(records), 'nativeAndRecompiledCalls': len(records) * 2,
           'syntheticExternalCalls': external, 'visitedInstructions': len(visited)})


if __name__ == '__main__':
    main()
