import hashlib
import json
import random
from collections import Counter
from pathlib import Path
import match_runtime
import arm7_exchannel_model_20261030_65 as independent
import arm7_seq_neighbor_model_20261030 as memory
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
ADDRESS, CODE, SIZE = 0x037FF3AC, 932, 948
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
ARITIES = {ADDRESS: 1, 0x037FEB50: 1, 0x037FF82C: 2, 0x03806A40: 4, 0x03806C38: 2,
    0x037FFE14: 1, 0x037FFDB4: 1, 0x037FEDD8: 1, 0x037FECAC: 2,
    0x03800B38: 3, 0x037FFB1C: 1, 0x037FEDCC: 1, 0x037FEE4C: 1, 0x037FEE58: 1}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def ranges():
    rows = json.loads((ROOT/'evidence/arm7/ghidra-runtime-inventory.json').read_text())['functions']
    result = []
    for row in rows:
        first = int(row['address'], 0)
        if first in ARITIES or first in (0x03803828, 0x0380382C) or 0x03806A40 <= first < 0x03806E44:
            for start, stop in row['ranges']:
                result.append((int(start, 0), int(stop, 0), row['mode']))
    result.append((0x03806C38, 0x03806E44, 'arm'))
    return result


def cases():
    base = dict(index=0, active=False, start=False, hardware=False, callback=False, step=0,
        status=2, attenuation=0, velocity=127, sweep=0, sweepCounter=0, sweepLength=8,
        target=0, depth=0, speed=0, range=1, delay=0, phase=0, panRange=127,
        pan=0, userPan=0, userDecay=0, userDecay2=0, userPitch=0, midi=60, root=60,
        timer=4096, services=None, autoSweep=False, type=0, id=None, attack=64, sustain=127, decay=64, release=128, delayCounter=0, predecessor=False, passes=1)
    result = [dict(base)]
    for index in (0, 15):
        for callback in (False, True):
            result.append(dict(base, index=index, active=True, callback=callback))
            result.append(dict(base, index=index, active=True, start=True, callback=callback,
                status=3, velocity=0))
    result.append(dict(base, active=True, start=True, services=dict(pitch=0, volume=127)))
    result.append(dict(base, active=True, hardware=True, services=dict(pitch=0, volume=127)))
    bios = dict(pitch=0, volume=127)
    for status in (0, 1, 2, 3, 255):
        for step in (0, 1, 2, 0xFFFFFFFF):
            for attenuation in (0, -1, -92544):
                result.append(dict(base, active=True, start=True, status=status, step=step,
                    attenuation=attenuation, services=bios))
    for sweep in (-32768, -100, -1, 1, 100, 32767):
        for length in (1, 7, 65535, 0x7FFFFFFF):
            for position in sorted({0, length-1, length}):
                for step in (0, 1):
                    result.append(dict(base, active=True, start=True, status=3, velocity=0,
                        sweep=sweep, sweepLength=length, sweepCounter=position, step=step, autoSweep=True))
    for target in (0, 1, 2, 3, 255):
        for phase in (0, 0x1F00, 0x2000, 0x3F00, 0x4000, 0x5F00, 0x6000, 0x7FFF):
            for depth in (0, 127, 255):
                result.append(dict(base, active=True, start=True, target=target, phase=phase,
                    depth=depth, speed=255, range=16, step=1, services=bios))
    for pan in (-128, -64, -1, 0, 1, 63, 127):
        for pan_range in (0, 1, 126, 127, 128, 255):
            result.append(dict(base, active=True, start=True, pan=pan, panRange=pan_range,
                userPan=-128 if pan < 0 else 127, services=bios))
    for channel_type in (0, 1, 2, 255):
        for timer in (0, 1, 15, 16, 4097, 65535):
            for pitch, volume in ((0, 0), (1, 1), (65535, 127)):
                result.append(dict(base, active=True, start=True, type=channel_type, timer=timer,
                    services=dict(pitch=pitch, volume=volume), passes=2))
    for velocity in range(256):
        result.append(dict(base, active=True, start=True, velocity=velocity, services=bios))
    for status in (0, 1, 3):
        for rate in (0, 1, 127, 255, 65535):
            result.append(dict(base, active=True, start=True, status=status, step=1, attenuation=-92544,
                attack=rate & 255, sustain=0 if rate < 127 else 127, decay=rate, release=rate, services=bios))
    for delay in (0, 1, 65535):
        for counter in (0, 1, 65534, 65535):
            result.append(dict(base, active=True, start=True, delay=delay, delayCounter=counter,
                depth=127, speed=255, step=1, phase=0x4000, services=bios))
    for midi, root in ((0, 0), (0, 127), (127, 0), (127, 127)):
        for user_pitch in (-32768, -1, 0, 32767):
            result.append(dict(base, active=True, start=True, midi=midi, root=root,
                userPitch=user_pitch, services=bios))
    for index in (0, 15):
        result.append(dict(base, active=True, index=index, id=255, hardware=True,
            depth=127, speed=255, step=1, services=bios, passes=2))
        result.append(dict(base, active=True, index=index, callback=True, predecessor=True))
        result.append(dict(base, active=True, start=True, index=index, callback=True, predecessor=True,
            status=3, velocity=0))
    result.append(dict(base, active=True, start=True, sweep=-32768, sweepLength=7, autoSweep=False, step=1, services=bios))
    result.append(dict(base, active=True, start=True))
    unique = {}
    for item in result:
        unique[json.dumps(item, sort_keys=True)] = item
    return list(unique.values())


def setup(case, seed):
    raw = (ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw) != RAW_SHA:
        raise ValueError('Original ARM7 module changed')
    wram = bytearray(0x14000)
    wram[:len(raw)] = raw
    state = independent.Model(random.Random(20261030+seed).randbytes(0x4000), wram, bytes(0x2000), case['services'])
    for index in range(16):
        node = independent.CHANNELS+index*84
        for offset in range(84):
            state.put(node+offset, 1, 0)
        state.put(node, 1, index)
    node = independent.CHANNELS+case['index']*84
    flags = int(case['active']) | int(case['start'])*2 | int(case['autoSweep'])*4
    if case['id'] is not None:
        state.put(node, 1, case['id'])
    for offset, size, value in ((1, 1, case['type']), (2, 1, case['status']), (3, 1, flags),
        (4, 1, case['panRange']), (5, 1, case['root']), (6, 2, case['userDecay2']),
        (8, 1, case['midi']), (9, 1, case['velocity']), (10, 1, case['pan']), (11, 1, case['userPan']),
        (12, 2, case['userDecay']), (14, 2, case['userPitch']), (16, 4, case['attenuation']),
        (20, 4, case['sweepCounter']), (24, 4, case['sweepLength']), (28, 1, case['attack']), (29, 1, case['sustain']),
        (30, 2, case['decay']), (32, 2, case['release']), (34, 1, 100), (40, 1, case['target']),
        (41, 1, case['speed']), (42, 1, case['depth']), (43, 1, case['range']),
        (44, 2, case['delay']), (46, 2, case['delayCounter']), (48, 2, case['phase']), (50, 2, case['sweep']),
        (60, 2, case['timer']), (72, 4, 0x03800B38 if case['callback'] else 0),
        (76, 4, memory.TRACKS if case['callback'] else 0)):
        state.put(node+offset, size, value)
    state.put(memory.TRACKS+0x3C, 4, node)
    if case['predecessor']:
        other = independent.CHANNELS+(1 if case['index'] == 0 else 0)*84
        state.put(other+0x50, 4, node)
        state.put(memory.TRACKS+0x3C, 4, other)
    state.put(independent.MMIO+0x400+case['index']*16, 4, 0x80000000 if case['hardware'] else 0)
    return [bytes(state.regions[key]) for key in (memory.DATA, memory.BASE, independent.MMIO)]


def execute(body, case, seed, budget=100000):
    ram, wram, io = setup(case, seed)
    wram = bytearray(wram)
    wram[ADDRESS-memory.BASE:ADDRESS-memory.BASE+len(body)] = body
    wram = bytes(wram)
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base, size, data in ((memory.DATA, 0x4000, ram), (memory.BASE, 0x14000, wram),
        (independent.MMIO, 0x2000, io), (memory.STACK, 0x4000, random.Random(seed+991).randbytes(0x4000)),
        (memory.RETURN, 0x1000, bytes(0x1000))):
        cpu.mem_map(base, size)
        cpu.mem_write(base, data)
    allowed, visited, writes, frames, calls, services, divisions = ranges(), set(), [], [], [], [], []
    nested, previous, failure = Counter(), [None], [None]
    def code(machine, pc, size, unused):
        while frames and pc == frames[-1]['return']:
            frame = frames.pop()
            nested[frame['address']] += 1
            if frame['address'] == 0x03806A40:
                a = memory.signed(frame['args'][0] | frame['args'][1] << 32, 64)
                b = memory.signed(frame['args'][2] | frame['args'][3] << 32, 64)
                result = machine.reg_read(match_runtime.REGISTERS[0]) | machine.reg_read(match_runtime.REGISTERS[1]) << 32
                if not b or result != independent.divide(a, b) & ((1 << 64)-1):
                    raise ValueError('Original signed64 runtime result differs from independent arithmetic')
                divisions.append([a, b, result])
        mode = 'thumb' if machine.reg_read(UC_ARM_REG_CPSR) & 32 else 'arm'
        if not any(first <= pc < last and current == mode for first,last,current in allowed):
            raise ValueError('Channel execution escaped qualified native code: '+hex(pc)+' '+mode)
        if pc in ARITIES:
            caller = previous[0]
            actual_call = pc == ADDRESS and not frames
            if caller:
                old_pc, old_mode, word = caller
                actual_call |= old_mode == 'arm' and word >> 24 & 15 == 11 and pc != old_pc+4
                actual_call |= old_mode == 'arm' and word & 0x0FFFFFF0 == 0x012FFF10 and machine.reg_read(match_runtime.REGISTERS[-1]) == old_pc+4
            if actual_call:
                args = [machine.reg_read(register) for register in match_runtime.REGISTERS[:ARITIES[pc]]]
                frames.append(dict(address=pc, args=args, **{'return': machine.reg_read(match_runtime.REGISTERS[-1])}))
                calls.append([pc, args])
        visited.add(pc)
        previous[0] = (pc, mode, int.from_bytes(machine.mem_read(pc, size), 'little'))
    def write(machine, access, location, size, value, unused):
        if not memory.STACK <= location < memory.STACK+0x4000:
            writes.append([location, size, value & ((1 << size*8)-1)])
    def interrupt(machine, number, unused):
        pc = machine.reg_read(UC_ARM_REG_PC)
        service = 27 if pc == 0x0380382A else 28 if pc == 0x0380382E else None
        argument = machine.reg_read(match_runtime.REGISTERS[0])
        if service is None:
            raise ValueError('Unexpected architectural interrupt')
        if case['services'] is None:
            failure[0] = dict(unsupportedExternalSvc=service, argument=argument, pc=pc)
            machine.emu_stop()
            return
        bound = 767 if service == 27 else 723
        result = case['services']['pitch' if service == 27 else 'volume']
        if not 0 <= argument <= bound or not 0 <= result <= (65535 if service == 27 else 127):
            raise ValueError('Synthetic BIOS service contract exceeded')
        services.append([service, argument, result])
        machine.reg_write(match_runtime.REGISTERS[0], result)
    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    cpu.hook_add(UC_HOOK_INTR, interrupt)
    records = []
    for phase in range(case['passes']):
        registers = [random.Random(seed+phase*888+index).getrandbits(32) for index in range(15)]
        registers[0], registers[-2], registers[-1] = case['step'], memory.STACK+0x3F00, memory.RETURN
        cpu.reg_write(UC_ARM_REG_CPSR, (seed % 16 << 28) | 0xD3)
        for register, value in zip(match_runtime.REGISTERS, registers):
            cpu.reg_write(register, value)
        first, svc_first = len(writes), len(services)
        frames.clear()
        previous[0] = None
        fault = None
        try:
            cpu.emu_start(ADDRESS, memory.RETURN, count=budget, timeout=100000)
        except UcError as error:
            fault = error.errno
        returned = cpu.reg_read(UC_ARM_REG_PC) == memory.RETURN
        observed = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if returned:
            expected = independent.Model(ram, wram, io, case['services'])
            expected.update(case['step'])
            if expected.writes != writes[first:] or expected.service_calls != services[svc_first:]:
                raise ValueError('Independent channel ordered writes/service indices differ: '+repr((case,writes[first:],expected.writes,services[svc_first:],expected.service_calls)))
            for base in (memory.DATA, memory.BASE, independent.MMIO):
                if bytes(cpu.mem_read(base, len(expected.regions[base]))) != bytes(expected.regions[base]):
                    raise ValueError('Independent channel full RAM/WRAM/MMIO effects differ')
            if observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:] or len(frames) != 1:
                raise ValueError('Actual channel root/nested return ABI differs')
            ram, wram, io = [bytes(expected.regions[key]) for key in (memory.DATA, memory.BASE, independent.MMIO)]
        records.append(dict(actualReturn=returned, fault=fault, externalFailure=failure[0],
            pc=cpu.reg_read(UC_ARM_REG_PC), registers=observed, cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            writes=writes[first:], biosServices=services[svc_first:],
            regionHashes=[digest(bytes(cpu.mem_read(base, size))) for base,size in ((memory.DATA,0x4000),(memory.BASE,0x14000),(independent.MMIO,0x2000),(memory.STACK,0x4000))]))
        if not returned:
            break
    return dict(states=records, visited=sorted(visited), actualCallArguments=calls,
        separatelyObservedNestedReturns={hex(key):value for key,value in nested.items()}, independentSigned64Returns=divisions)
