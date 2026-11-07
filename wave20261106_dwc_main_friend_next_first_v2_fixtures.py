import hashlib
import json
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT
import wave20261106_dwc_main_friend_next_first_v2_models as F


class Live:
    def __init__(self, cpu, writes):
        self.cpu, self.writes = cpu, writes

    def read(self, address, size):
        return bytes(self.cpu.mem_read(address, size))

    def write(self, address, raw):
        self.cpu.mem_write(address, raw)
        self.writes.append(('contract', address, len(raw), raw.hex()))


def run(image, row, body, vector, seed):
    address = int(row['address'], 0)
    regions, args = F.initial(address, vector)
    expected, wanted, contract, result = F.model(address, vector)
    cpu = un.Uc(un.UC_ARCH_ARM, un.UC_MODE_THUMB)
    cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946)
    cpu.mem_map(0x2000000, 0x400000)
    cpu.mem_write(0x2000000, image)
    cpu.mem_write(address, body)
    cpu.mem_map(F.STOP, 0x1000)
    cpu.mem_map(F.SP - 0x4000, 0x5000)
    for at, raw in regions.items():
        cpu.mem_write(at, raw)
    initial = [(0x11440000 + seed * 0x101 + index * 0x110011) & 0xffffffff for index in range(15)]
    initial[:min(len(args), 4)] = [value & 0xffffffff for value in args[:4]]
    initial[-2:] = [F.SP, F.STOP | 1]
    cpu.reg_write(ar.UC_ARM_REG_CPSR, [0x30, 0x10000030, 0x80000030, 0xf0000030][seed % 4])
    for reg, value in zip(C.REGISTERS, initial):
        cpu.reg_write(reg, value)
    bindings = {int(value['address'], 0): value for value in row['nativeSymbolEntries'].values() if value['kind'] == 'function'}
    mode = 'thumb' if vector.get('callbackMode', 1) else 'arm'
    bindings.update({F.BUDDY: dict(mode=mode), F.STATUS: dict(mode=mode)})
    writes, calls, raw_calls, reads, pcs = [], [], [], [], []
    returned = False
    live = Live(cpu, writes)
    def code(machine, at, size, user):
        nonlocal returned
        if at == F.STOP:
            returned = True
            machine.emu_stop()
            return
        if at in bindings:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR) & 32) != (bindings[at]['mode'] == 'thumb'):
                raise ValueError('Actual friend contract entry mode differs')
            count = F.ARITY[at]
            values = [machine.reg_read(reg) for reg in C.REGISTERS[:min(4, count)]]
            if count > 4:
                values.extend(struct.unpack('<' + 'I' * (count - 4), live.read(machine.reg_read(ar.UC_ARM_REG_SP), 4 * (count - 4))))
            value, normalized = F.effect(at, values, live, vector)
            calls.append(normalized)
            raw_calls.append((hex(at), values))
            link = machine.reg_read(ar.UC_ARM_REG_LR)
            for index in [1, 2, 3, 12]:
                machine.reg_write(C.REGISTERS[index], (0xa5110000 + len(calls) * 0x100 + index) & 0xffffffff)
            machine.reg_write(ar.UC_ARM_REG_R0, value & 0xffffffff)
            if at in F.RET64:
                machine.reg_write(ar.UC_ARM_REG_R1, value >> 32)
            cpsr = (machine.reg_read(ar.UC_ARM_REG_CPSR) & 0x0fffffdf) | [0, 0x10000000, 0x80000000, 0xf0000000][(seed + len(calls)) % 4] | (32 if link & 1 else 0)
            machine.reg_write(ar.UC_ARM_REG_PC, link & ~1)
            machine.reg_write(ar.UC_ARM_REG_CPSR, cpsr)
            return
        if not address <= at < address + len(body) or not machine.reg_read(ar.UC_ARM_REG_CPSR) & 32:
            raise ValueError(('Unexpected friend caller graph/mode escape', hex(at)))
        pcs.append(at)
    def write(machine, access, at, size, value, user):
        allowed = F.SP - 0x4000 <= at and at + size <= F.SP
        allowed |= any(start <= at and at + size <= start + len(raw) for start, raw in regions.items())
        if not allowed:
            raise ValueError(('Friend caller left bounded writable memory', hex(at), size))
        writes.append(('caller', at, size, (value & ((1 << (size * 8)) - 1)).to_bytes(size, 'little').hex()))
    def read(machine, access, at, size, value, user):
        pc = machine.reg_read(ar.UC_ARM_REG_PC)
        if address <= pc < address + len(body) and any(start <= at and at + size <= start + len(raw) for start, raw in regions.items()):
            reads.append((at, size, int.from_bytes(machine.mem_read(at, size), 'little')))
    cpu.hook_add(un.UC_HOOK_CODE, code)
    cpu.hook_add(un.UC_HOOK_MEM_WRITE, write)
    cpu.hook_add(un.UC_HOOK_MEM_READ, read)
    cpu.emu_start(address | 1, F.STOP + 4, count=10000)
    registers = [cpu.reg_read(reg) for reg in C.REGISTERS]
    if not returned or registers[4:12] != initial[4:12] or registers[13] != F.SP:
        raise ValueError('Returning friend caller callee-saved or stack ABI differs')
    actual = {at: bytes(cpu.mem_read(at, len(raw))) for at, raw in expected.items()}
    passed = actual == expected and calls == wanted and (contract == 'void' or registers[0] == result)
    trace = dict(registers=registers, cpsr=cpu.reg_read(ar.UC_ARM_REG_CPSR), writes=writes,
        rawCalls=raw_calls, calls=calls, reads=reads, pcs=pcs, externalMemory={hex(at): raw.hex() for at, raw in actual.items()})
    return dict(topReturned=returned, modelPassed=passed, externalMemoryPassed=actual == expected,
        calls=calls, expectedCalls=wanted, returnValue=registers[0], expectedReturn=result,
        returnContract=contract, observedReadCount=len(reads), traceSha256=hashlib.sha256(json.dumps(trace, sort_keys=True).encode()).hexdigest())


def prove(row, native, source):
    image = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    records = []
    for seed, vector in enumerate(F.cases(int(row['address'], 0))):
        original = run(image, row, native, vector, seed)
        rebuilt = run(image, row, source, vector, seed)
        if original != rebuilt or not original['modelPassed']:
            raise ValueError(('Bounded independent friend model differs', row['address'], vector, original, rebuilt))
        records.append(dict(seed=seed, vector=vector, traceSha256=original['traceSha256'],
            contractCalls=len(original['calls']), observedReadCount=original['observedReadCount']))
    return dict(address=row['address'], cases=len(records), actualNativeAndSourceCallerReturns=2 * len(records),
        records=records, allGprsCpsrCalleeSavedStackAndOrderedWritesCompared=True,
        orderedNativeAndSourceReadsCompared=True, independentlyModeledReadOrder=False,
        definedFriendPrefixAndRecordStrideOnly=True, fixtureControlledProviderContracts=True,
        realProviderBodiesExecuted=0, suppliedCalleeSourceOrExecutionCredit=0,
        realNetworkServiceHardwareOrSceneExecution=0,
        indirectCallbackNamespace='Fixture-only ARM/Thumb callbacks add no native static binding or provider implementation claim')
