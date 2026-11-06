import gc
import struct
import match_runtime as c
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import *
BASE, ENTRY, GETTER, FIELD, STACK, STOP = (33554432, 33834220, 33833964, 34564584, 41877504, 41940992)
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]

def execute(image, mode, body=None):
    u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    u.ctl_set_cpu_model(UC_CPU_ARM_946)
    u.mem_map(BASE, 8388608)
    u.mem_write(BASE, image)
    own_size = len(body) if body is not None else 28
    if body is not None:
        u.mem_write(ENTRY, body)
    u.mem_write(FIELD, bytes([mode]))
    before = bytes(u.mem_read(BASE, 8388608))
    observed = set()
    frame = []
    returned = []
    steps = []
    initial = [2688774144 + j * 256 for j in range(13)]

    def watch(uc, address, length, data):
        observed.add(address)
        steps.append(address)
        if address == GETTER:
            if frame:
                raise ValueError('437 repeated getter entry without return')
            frame.append(dict(lr=uc.reg_read(UC_ARM_REG_LR), sp=uc.reg_read(UC_ARM_REG_SP), preserved=[uc.reg_read(r) for r in REGS[4:12]]))
        if frame and address == frame[0]['lr'] & ~1 and (uc.reg_read(UC_ARM_REG_SP) == frame[0]['sp']):
            f = frame.pop()
            if [uc.reg_read(r) for r in REGS[4:12]] != f['preserved'] or uc.reg_read(UC_ARM_REG_R0) != mode or uc.reg_read(UC_ARM_REG_CPSR) & 63 != 16:
                raise ValueError('437 original getter return/ABI differs')
            returned.append(mode)
        if not (ENTRY <= address < ENTRY + own_size or GETTER <= address < GETTER + 12):
            raise ValueError(('437 unexpected instruction', hex(address)))
    u.hook_add(UC_HOOK_CODE, watch)
    u.reg_write(UC_ARM_REG_CPSR, 16)
    for register, value in zip(REGS, initial):
        u.reg_write(register, value)
    u.reg_write(UC_ARM_REG_SP, STACK)
    u.reg_write(UC_ARM_REG_LR, STOP)
    u.emu_start(ENTRY, STOP, count=128)
    if u.reg_read(UC_ARM_REG_PC) != STOP or u.reg_read(UC_ARM_REG_SP) != STACK or u.reg_read(UC_ARM_REG_CPSR) & 63 != 16 or ([u.reg_read(r) for r in REGS[4:12]] != initial[4:12]) or (returned != [mode]) or frame:
        raise ValueError('437 actual top return/ABI differs')
    after = bytes(u.mem_read(BASE, 8388608))
    cut = STACK - 65536 - BASE
    end = STACK + 4096 - BASE
    if after[:cut] != before[:cut] or after[end:] != before[end:]:
        raise ValueError('437 native nonstack state changed')
    result = dict(rawModeByte=mode, returnedR0=u.reg_read(UC_ARM_REG_R0), actualTopReturns=1, nativeGetterActualReturns=1, providedCalls=0, observedAddresses=sorted(observed), instructions=len(steps), finalRegisters=[u.reg_read(r) for r in REGS], allNonstackMemoryUnchanged=True)
    del u
    gc.collect()
    return result
