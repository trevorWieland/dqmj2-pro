import struct
import ov001_action822_machine_20261102 as M

ENTRY = 0x021F35F0
NEW_HELPERS = {0x0207B20C: 28, 0x021F358C: 100}
NEW_PROVIDERS = {0x021F1F1C: 1, 0x021D7F54: 1, 0x021D7E80: 1, 0x021F34C8: 1, 0x021F32B4: 2, 0x021F30CC: 3, 0x021D8DEC: 1, 0x0205D6F4: 1, 0x021F3178: 2, 0x021F14E4: 0}
ROW = 0x02550000


class Machine(M.Machine):
    def __init__(self, main, overlay, images, profile):
        super().__init__(main, overlay, images, profile)
        self.ranges.update(NEW_HELPERS)
        self.ranges[ENTRY] = 988
        context = bytearray(self.beforeContext)
        context[9] = profile['actionPhase']
        context[0x10] = profile['context10']
        context[0x13] = profile['context13']
        context[0] = profile['oldToken']
        struct.pack_into('<I', context, 0x80, self.current)
        self.beforeContext = bytes(context)
        self.u.mem_write(M.CONTEXT, bytes(context))
        self.u.mem_write(M.MOVES + profile['moveId'] * 40 + 0xC, struct.pack('<h', profile['effect']))
        self.u.mem_write(ROW, bytes(32))
        self.u.mem_write(ROW + 0xC, struct.pack('<H', profile['rowHalf']))
        for base in M.ACTOR_BASES:
            for index in range(3):
                pointer = base + index * 0x440
                side = M.ACTOR_BASES.index(base)
                value = profile.get('flagsBySide', [profile['opponentFlags']] * 4)[side][index] & 0xFF
                self.u.mem_write(pointer + 0x267, bytes([value]))
                actor = bytearray(self.beforeActors[pointer])
                actor[0x267] = value
                self.beforeActors[pointer] = bytes(actor)
        self.ownPcs = set()

    def provider(self, pc, args):
        if pc == 0x021F32B4:
            return self.p['tokenWord']
        if pc == 0x021D8DEC:
            return ROW
        if pc == 0x0205D6F4:
            return self.p['timerWord']
        if pc == 0x021F14E4:
            return self.p['statusWord']
        return super().provider(pc, args)

    def code(self, u, pc, width, unused):
        if pc in NEW_PROVIDERS:
            self.instructions += 1
            if self.instructions > 20000:
                raise ValueError('830 instruction bound')
            words = [u.reg_read(reg) for reg in M.REGS[:4]]
            stack = list(struct.unpack('<4I', bytes(u.mem_read(u.reg_read(M.UC_ARM_REG_SP), 16))))
            args = (words + stack)[:NEW_PROVIDERS[pc]]
            result = self.provider(pc, args) & 0xFFFFFFFF
            self.calls.append(dict(target=hex(pc), callerWords=args, suppliedReturn=result))
            self.rawCalls.append(dict(target=hex(pc), registers=words, stackWords=stack))
            for index in [0, 1, 2, 3, 12]:
                u.reg_write(M.REGS[index], (0xCACE0000 + index * 0x101 + self.p['ordinal']) & 0xFFFFFFFF)
            cpsr = u.reg_read(M.UC_ARM_REG_CPSR)
            u.reg_write(M.UC_ARM_REG_CPSR, (cpsr & 0x0FFFFFFF) | ((self.p['ordinal'] & 15) << 28))
            u.reg_write(M.REGS[0], result)
            u.reg_write(M.UC_ARM_REG_PC, u.reg_read(M.UC_ARM_REG_LR))
            return
        if pc in NEW_HELPERS:
            self.pending.append((pc, u.reg_read(M.UC_ARM_REG_LR)))
            self.nativeEntries.append(dict(address=hex(pc), incomingWords=[u.reg_read(reg) for reg in M.REGS[:4]]))
        super().code(u, pc, width, unused)
        if ENTRY <= pc < ENTRY + 976:
            self.ownPcs.add(pc)
