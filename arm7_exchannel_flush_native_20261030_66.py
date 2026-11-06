import hashlib
import json
import random
from collections import Counter
from pathlib import Path
import match_runtime
import arm7_seq_neighbor_model_20261030 as memory
import arm7_exchannel_flush_model_20261030_66 as independent
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
ADDRESS, CODE, SIZE = 0x037FF1C0, 488, 492
ARITIES = {ADDRESS: 0, 0x037FEA20: 2, 0x037FE804: 10, 0x037FE8D0: 6,
    0x037FE97C: 5, 0x037FEAC0: 2, 0x037FEA48: 3, 0x037FEAD8: 2, 0x037FEC40: 2}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def ranges():
    rows = json.loads((ROOT/'evidence/arm7/ghidra-runtime-inventory.json').read_text())['functions']
    return [(int(a,0),int(z,0)) for row in rows if int(row['address'],0) in ARITIES for a,z in row['ranges']]


def cases():
    base = dict(index=0, sync=0, kind=0, volume=127, divisor=0, timer=4096, pan=64,
        pointer=0x023C1800, format=0, loop=0, loopStart=0, loopLength=16,
        override=-1, gate=0, factor=0, passes=1, id=0)
    result = [dict(base)]
    for index in (0, 15):
        for sync in (1, 2, 3, 4, 8, 16, 28, 31):
            for kind in (0, 1, 2, 255):
                result.append(dict(base, index=index, sync=sync, kind=kind))
    for sync in range(32):
        result.append(dict(base, sync=sync, kind=0, passes=2))
    for index in (0, 1, 3, 15):
        for pan in (0, 23, 24, 64, 104, 105, 127, 255):
            for factor in (0, 16384, 32767):
                result.append(dict(base, index=index, sync=31, kind=0, pan=pan,
                    gate=1, factor=factor, passes=2))
    for kind in (0, 1, 2, 255):
        for volume in (0, 1, 127, 128, 255):
            for divisor in (0, 1, 3, 255):
                result.append(dict(base, sync=31, kind=kind, volume=volume, divisor=divisor))
    for kind in (0, 1, 2):
        for override in (-1, 0, 64, 127):
            for sync in (1, 8, 16, 24, 31):
                result.append(dict(base, sync=sync, kind=kind, override=override, gate=1, factor=32767))
    for kind in (0, 1, 2):
        for word in (0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF):
            result.append(dict(base, index=15, id=255, sync=31, kind=kind,
                pointer=word, loopLength=word, loopStart=word & 65535, timer=word & 65535,
                format=word & 255, loop=word & 255))
    for gate in (-1, 0, 1, 16384, 32767):
        for sync in (1, 8, 16, 24, 31):
            result.append(dict(base, sync=sync, gate=gate, factor=gate, pan=0, volume=255))
    for turn in range(8):
        rows = [dict(index=index, id=255-index, sync=(index*7+turn)%32,
            kind=(index+turn)%4, pan=(index*19+turn)%256, volume=(index*31+turn)%256,
            divisor=(index+turn)%4, timer=index*4097+turn, pointer=0x80000000+index*16,
            loop=index%2, loopStart=index*4096, loopLength=0xFFFFFFFF-index,
            format=index%3) for index in range(1,16)]
        result.append(dict(base, sync=31, gate=1, factor=16384, otherRows=rows, passes=2))
    unique = {}
    for item in result:
        unique[json.dumps(item,sort_keys=True)] = item
    return list(unique.values())


def setup(case, seed):
    raw = (ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw) != 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':
        raise ValueError('Original ARM7 image changed')
    wram = bytearray(0x14000)
    wram[:len(raw)] = raw
    state = independent.Model(random.Random(seed+20261030).randbytes(0x4000), wram,
        random.Random(seed+991).randbytes(0x2000))
    for index in range(16):
        node = independent.CHANNELS+index*84
        for offset in range(84):
            state.put(node+offset, 1, 0)
    for row in [case]+[dict(case, **item) for item in case.get('otherRows',[])]:
        node = independent.CHANNELS+row['index']*84
        for offset,size,value in ((0,1,row['id']), (1,1,row['kind']), (3,1,row['sync'] << 3 | 7),
            (0x23,1,row['pan']), (0x24,2,row['volume'] | row['divisor'] << 8), (0x26,2,row['timer']),
            (0x38,1,row['format']), (0x39,1,row['loop']), (0x3E,2,row['loopStart']),
            (0x40,4,row['loopLength']), (0x44,4,row['pointer'])):
            state.put(node+offset,size,value)
    for address,value in ((independent.PAN_OVERRIDE,case['override']),
        (independent.ADJUST_GATE,case['factor'] if case['gate'] > 0 else case['gate'])):
        state.put(address,4,value)
    return [bytes(state.regions[key]) for key in (memory.DATA,memory.BASE,independent.MMIO)]


def execute(body, case, seed, budget=100000):
    ram,wram,io = setup(case,seed)
    wram = bytearray(wram)
    wram[ADDRESS-memory.BASE:ADDRESS-memory.BASE+len(body)] = body
    wram = bytes(wram)
    cpu = Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,size,data in ((memory.DATA,0x4000,ram),(memory.BASE,0x14000,wram),
        (independent.MMIO,0x2000,io),(memory.STACK,0x4000,random.Random(seed+811).randbytes(0x4000)),
        (memory.RETURN,0x1000,bytes(0x1000))):
        cpu.mem_map(base,size)
        cpu.mem_write(base,data)
    allowed,frames,visited,writes,calls = ranges(),[],set(),[],[]
    nested = Counter()
    def code(machine,pc,size,unused):
        while frames and pc == frames[-1][1]:
            nested[frames.pop()[0]] += 1
        if machine.reg_read(UC_ARM_REG_CPSR) & 32 or not any(a <= pc < z for a,z in allowed):
            raise ValueError('Flush escaped qualified original ARM code: '+hex(pc))
        if pc in ARITIES:
            words = [machine.reg_read(reg) for reg in match_runtime.REGISTERS[:min(4,ARITIES[pc])]]
            if ARITIES[pc] > 4:
                stack = machine.reg_read(match_runtime.REGISTERS[-2])
                words += [int.from_bytes(machine.mem_read(stack+i*4,4),'little') for i in range(ARITIES[pc]-4)]
            frames.append((pc,machine.reg_read(match_runtime.REGISTERS[-1])))
            calls.append([pc,words])
        visited.add(pc)
    def write(machine,access,address,size,value,unused):
        if not memory.STACK <= address < memory.STACK+0x4000:
            writes.append([address,size,value & ((1 << size*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    records = []
    for phase in range(case['passes']):
        registers = [random.Random(seed+phase*613+i).getrandbits(32) for i in range(15)]
        registers[-2:] = [memory.STACK+0x3F00,memory.RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,seed % 16 << 28 | 0xD3)
        for reg,value in zip(match_runtime.REGISTERS,registers):
            cpu.reg_write(reg,value)
        first,call_first = len(writes),len(calls)
        frames.clear()
        fault = None
        try:
            cpu.emu_start(ADDRESS,memory.RETURN,count=budget,timeout=100000)
        except UcError as error:
            fault = error.errno
        returned = cpu.reg_read(UC_ARM_REG_PC) == memory.RETURN
        observed = [cpu.reg_read(reg) for reg in match_runtime.REGISTERS]
        if returned:
            expected = independent.Model(ram,wram,io)
            expected.flush()
            actual_calls = [row for row in calls[call_first:] if row[0] not in (ADDRESS,0x037FEC40)]
            if expected.writes != writes[first:] or expected.calls != actual_calls:
                raise ValueError('Independent flush stores or full driver ABI differ: '+repr((case,writes[first:],expected.writes,actual_calls,expected.calls)))
            for base in (memory.DATA,memory.BASE,independent.MMIO):
                if bytes(cpu.mem_read(base,len(expected.regions[base]))) != bytes(expected.regions[base]):
                    raise ValueError('Independent full RAM/WRAM/MMIO effects differ')
            if observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:] or frames != [(ADDRESS,memory.RETURN)]:
                raise ValueError('Actual flush root/nested return ABI differs')
            ram,wram,io = [bytes(expected.regions[key]) for key in (memory.DATA,memory.BASE,independent.MMIO)]
        records.append(dict(actualReturn=returned,fault=fault,pc=cpu.reg_read(UC_ARM_REG_PC),registers=observed,
            cpsr=cpu.reg_read(UC_ARM_REG_CPSR),writes=writes[first:],actualCallArguments=calls[call_first:],
            stateHashes=[digest(bytes(cpu.mem_read(base,size))) for base,size in
                ((memory.DATA,0x4000),(memory.BASE,0x14000),(independent.MMIO,0x2000),(memory.STACK,0x4000))]))
        if not returned:
            break
    return dict(states=records,visited=sorted(visited),separatelyObservedNestedReturns={hex(k):v for k,v in nested.items()})
