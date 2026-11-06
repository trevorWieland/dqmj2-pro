import gc
import json
import re
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import *
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_JUMP, CS_GRP_CALL
BASE, ENTRY, SIZE, CONTEXT, STACK, STOP = (33554432, 35562860, 1232, 35884412, 41877504, 41940992)
OVERLAY_BASE, RNG, TABLE, MOVE, STATE = (35484224, 34562116, 39911424, 39976960, 39981056)
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
PROVIDERS = {35560636: ('initialization', 0), 34058220: ('move-row', 1), 34058820: ('required-value', 3), 35591188: ('flag29', 1), 35715492: ('target-rule', 3), 35661012: ('resource-notify', 3), 34058244: ('move-flag', 2), 33971592: ('state-pointer', 0), 35595012: ('slot-selector', 3), 35590804: ('display-notify', 2), 35525464: ('target-notify', 1), 35589100: ('actor356', 1), 35589184: ('actor346', 1), 35527112: ('busy', 0), 35661160: ('actor-notify', 2), 34063320: ('maximum-base', 2)}
ROOTS = {'main': [33804948, 33836252, 33590648], 'ov001': [35501112, 35502288, 35503408, 35502580, 35502132, 35502028, 35503344]}

def signed(value, bits=32):
    value &= (1 << bits) - 1
    return value - (1 << bits) if value >> bits - 1 else value

def inputs():
    main, arm, main_symbols = measured_module('main')
    module, overlay, overlay_symbols = measured_module('ov001')
    functions = {}
    for name, symbols in [('main', main_symbols), ('ov001', overlay_symbols)]:
        for line in symbols.splitlines():
            found = re.search('kind:function\\((arm|thumb),size=(0x[0-9a-f]+)\\) addr:(0x[0-9a-f]+)', line)
            if found:
                functions[int(found[3], 0)] = dict(module=name, mode=found[1], bytes=int(found[2], 0))
    ranges = {}
    queue = [a for values in ROOTS.values() for a in values]
    while queue:
        address = queue.pop()
        if address in ranges or address in PROVIDERS:
            continue
        row = functions[address]
        ranges[address] = row
        image = arm if row['module'] == 'main' else overlay
        base = BASE if row['module'] == 'main' else OVERLAY_BASE
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM if row['mode'] == 'arm' else CS_MODE_THUMB)
        decoder.detail = True
        for instruction in decoder.disasm(image[address - base:address - base + row['bytes']], address):
            if not (instruction.group(CS_GRP_JUMP) or instruction.group(CS_GRP_CALL)) or not instruction.op_str.startswith('#0x'):
                continue
            target = int(instruction.op_str[1:], 0) & ~1
            if address <= target < address + row['bytes'] or target in PROVIDERS:
                continue
            if target in functions:
                queue.append(target)
    actors = struct.unpack_from('<4I', overlay, 35501220 - OVERLAY_BASE)
    container = struct.unpack_from('<I', arm, 33836300 - BASE)[0]
    return dict(main=main, module=module, arm=arm, overlay=overlay, ranges=ranges, actors=actors, container=container)

class Machine:

    def __init__(self, original, profile, body=None):
        self.i = original
        self.p = profile
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(BASE, 8388608)
        self.u.mem_write(BASE, original['arm'])
        self.u.mem_write(OVERLAY_BASE, original['overlay'])
        self.ownSize = len(body) if body is not None else SIZE
        if body is not None:
            self.u.mem_write(ENTRY, body)
        self.events = []
        self.frames = []
        self.returns = []
        self.observed = set()
        self.instructions = 0
        self.counter = 0
        self.actorRecords = {}
        for side in range(2):
            for slot in range(3):
                actor = original['actors'][side] + slot * 1088
                record = 40108032 + side * 4096 + slot * 512
                self.actorRecords[actor] = record
                self.u.mem_write(actor, b'\xa5' * 1088)
                self.u.mem_write(record, b'Z' * 512)
                self.word(actor + 488, record)
                self.byte(actor + 796, int(profile['eligible'] >> slot & 1))
                self.byte(actor + 511, 0)
                self.byte(actor + 798, side)
                self.byte(actor + 799, slot)
                self.byte(record + 172, 0)
                self.half(record + 42, side * 3 + slot)
                self.half(TABLE + 100 * (side * 3 + slot) + 4, profile['class'] * 3 << 8)
        self.actor = original['actors'][profile['side']]
        self.target = original['actors'][profile['targetSide']] + profile['targetSlot'] * 1088
        self.record = self.actorRecords[self.actor]
        self.u.mem_write(CONTEXT, b'\xa5' * 128)
        self.word(CONTEXT + 96, self.actor)
        self.word(CONTEXT + 84, self.target)
        self.half(CONTEXT + 54, profile['skill'])
        self.byte(CONTEXT + 30, profile['mode'])
        self.byte(CONTEXT + 41, profile['initial29'])
        self.byte(CONTEXT + 20, profile['context14'])
        self.byte(CONTEXT + 25, profile['selector19'])
        self.byte(self.actor + 597, profile['actor255'])
        self.byte(self.actor + 566, profile['actor236'])
        self.byte(self.actor + 509, profile['actor1FD'])
        self.half(self.actor + 498, profile['available'])
        self.half(self.actor + 542, 0)
        self.word(RNG, profile['seed'])
        self.word(original['container'] + 4, TABLE)
        self.u.mem_write(MOVE, b'\x00' * 16)
        self.half(MOVE + 8, (48 if profile['randomTarget'] else 0) | profile['upperKind'] << 12)
        self.half(MOVE + 10, profile['propertyA'])
        self.u.mem_write(STATE, b'\x00' * 64)
        self.byte(STATE + 45, profile['state2D'])
        self.byte(35843204, profile['display'])
        self.before = bytes(self.u.mem_read(BASE, 8388608))
        self.initial = [2688770048 + j * 256 for j in range(13)]
        self.u.reg_write(UC_ARM_REG_CPSR, 16)
        for register, value in zip(REGS, self.initial):
            self.u.reg_write(register, value)
        self.u.reg_write(UC_ARM_REG_SP, STACK)
        self.u.reg_write(UC_ARM_REG_LR, STOP)
        self.u.hook_add(UC_HOOK_CODE, self.observe)

    def byte(self, address, value):
        self.u.mem_write(address, bytes([value & 255]))

    def half(self, address, value):
        self.u.mem_write(address, struct.pack('<H', value & 65535))

    def word(self, address, value):
        self.u.mem_write(address, struct.pack('<I', value & 4294967295))

    def observe(self, u, address, length, data):
        self.instructions += 1
        while self.frames and address == self.frames[-1]['lr'] & ~1 and (u.reg_read(UC_ARM_REG_SP) == self.frames[-1]['sp']):
            frame = self.frames.pop()
            if [u.reg_read(r) for r in REGS[4:12]] != frame['preserved'] or bool(u.reg_read(UC_ARM_REG_CPSR) & 32) != bool(frame['lr'] & 1):
                raise ValueError('436 native helper return ABI differs')
            self.returns.append(dict(entry=frame['entry'], returnedR0=u.reg_read(UC_ARM_REG_R0), aliases=frame['aliases']))
        if ENTRY <= address < ENTRY + self.ownSize:
            self.observed.add(address)
            return
        if address in PROVIDERS:
            name, arity = PROVIDERS[address]
            args = [u.reg_read(r) for r in REGS[:arity]]
            self.events.append(dict(kind='provided', name=name, address=address, callerPreparedWords=args))
            self.counter += 1
            result = {'initialization': 0, 'move-row': MOVE, 'required-value': self.p['required'], 'flag29': self.p['flag29'], 'target-rule': self.p['rule'], 'resource-notify': 0, 'move-flag': self.p['moveFlag'], 'state-pointer': STATE, 'slot-selector': self.p['newSlot'], 'display-notify': 0, 'target-notify': 0, 'actor356': self.p['actor356'], 'actor346': self.p['actor346'], 'busy': self.p['busy'], 'actor-notify': 0, 'maximum-base': self.p['maximum']}[name]
            u.reg_write(UC_ARM_REG_R0, result & 4294967295)
            for register, tag in zip([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12], [1, 2, 3, 12]):
                u.reg_write(register, 3422552064 | self.counter << 8 | tag)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
            return
        row = self.i['ranges'].get(address)
        if row:
            frame = dict(entry=address, lr=u.reg_read(UC_ARM_REG_LR), sp=u.reg_read(UC_ARM_REG_SP), preserved=[u.reg_read(r) for r in REGS[4:12]], aliases=[])
            if self.frames and frame['sp'] == self.frames[-1]['sp'] and (frame['lr'] == self.frames[-1]['lr']):
                self.frames[-1]['aliases'].append(address)
            else:
                self.frames.append(frame)
            arity = {33804948: 1, 33836252: 1, 33590648: 3, 35501112: 2, 35502288: 1, 35503408: 1, 35502580: 1, 35502132: 2, 35502028: 2, 35503344: 1}.get(address, 0)
            self.events.append(dict(kind='native', address=address, callerPreparedWords=[u.reg_read(r) for r in REGS[:arity]]))
        if not any((start <= address < start + r['bytes'] for start, r in self.i['ranges'].items())):
            raise ValueError(('436 unexpected native PC', hex(address)))

    def run(self):
        self.u.emu_start(ENTRY, STOP, count=32768)
        if self.u.reg_read(UC_ARM_REG_PC) != STOP or self.u.reg_read(UC_ARM_REG_SP) != STACK or self.u.reg_read(UC_ARM_REG_CPSR) & 63 != 16 or ([self.u.reg_read(r) for r in REGS[4:12]] != self.initial[4:12]) or self.frames or (self.u.reg_read(UC_ARM_REG_R0) != 1):
            raise ValueError(('436 actual caller return/frame differs', self.p['name']))
        after = bytes(self.u.mem_read(BASE, 8388608))
        result = dict(profile=self.p, actor=self.actor, record=self.record, initialTarget=self.target, actorRecords=self.actorRecords, actors=list(self.i['actors']), before=self.before, after=after, events=self.events, nativeReturns=self.returns, ownObserved=sorted(self.observed), instructions=self.instructions, returnedR0=self.u.reg_read(UC_ARM_REG_R0), callerActualReturns=1, providedCalls=self.counter, ownImageBytes=self.ownSize)
        self.u = None
        gc.collect()
        return result
