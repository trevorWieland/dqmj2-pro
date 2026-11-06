import arm7_seq_neighbor_model_20261030 as memory

CHANNELS, MMIO = 0x03807EE0, 0x04000000
PAN_OVERRIDE, ADJUST_GATE, PAN_CACHE, VOLUME_CACHE, FACTOR = 0x038075C8, 0x03807980, 0x03807984, 0x03807994, 0x03807980


class Model(memory.Model):
    def __init__(self, ram, wram, io):
        super().__init__(ram, wram)
        self.regions[MMIO] = bytearray(io)
        self.calls = []

    def scale(self, volume, pan):
        factor = self.get(FACTOR, 4)
        if pan < 24:
            multiplier = factor*(pan+40)+(32767-factor)*64
        elif pan > 104:
            multiplier = -factor*(pan-40)+(factor+32767)*64
        else:
            return volume
        return memory.signed((volume*multiplier) & 0xFFFFFFFF) >> 21

    def adjusted(self, index, volume, pan):
        return self.scale(volume, pan) if self.get(ADJUST_GATE, 4, True) > 0 and (0xFFF5 >> index) & 1 else volume

    def invoke(self, address, arguments):
        self.calls.append([address, [value & 0xFFFFFFFF for value in arguments]])
        index = arguments[0]
        register = MMIO+0x400+index*16
        override = self.get(PAN_OVERRIDE, 4, True)
        if address == 0x037FEA20:
            self.put(register, 4, (self.get(register, 4) & ~0x80000000) | (0x8000 if arguments[1] & 1 else 0))
            return
        if address in (0x037FE804, 0x037FE8D0, 0x037FE97C):
            if address == 0x037FE804:
                _, wave, format_, loop_mode, loop_start, loop_length, volume, divisor, timer, pan = arguments
            elif address == 0x037FE8D0:
                _, duty, volume, divisor, timer, pan = arguments
            else:
                _, volume, divisor, timer, pan = arguments
            self.put(PAN_CACHE+index, 1, pan)
            effective_pan = override if override >= 0 else pan
            self.put(VOLUME_CACHE+index, 1, volume)
            value = self.adjusted(index, volume, effective_pan)
            control = ((loop_mode << 27) | (format_ << 29)) if address == 0x037FE804 else 0x60000000 | (duty << 24 if address == 0x037FE8D0 else 0)
            self.put(register, 4, control | effective_pan << 16 | divisor << 8 | value)
            self.put(register+8, 2, 65536-timer)
            if address == 0x037FE804:
                self.put(register+10, 2, loop_start)
                self.put(register+12, 4, loop_length)
                self.put(register+4, 4, wave)
        elif address == 0x037FEAC0:
            self.put(register+8, 2, 65536-arguments[1])
        elif address == 0x037FEA48:
            _, volume, divisor = arguments
            self.put(VOLUME_CACHE+index, 1, volume)
            self.put(register, 2, self.adjusted(index, volume, self.get(register+2, 1)) | divisor << 8)
        elif address == 0x037FEAD8:
            pan = arguments[1]
            self.put(PAN_CACHE+index, 1, pan)
            effective_pan = override if override >= 0 else pan
            self.put(register+2, 1, effective_pan)
            if self.get(ADJUST_GATE, 4, True) > 0 and (0xFFF5 >> index) & 1:
                self.put(register, 1, self.scale(self.get(VOLUME_CACHE+index, 1), effective_pan))
        else:
            raise ValueError('Unknown original hardware driver')

    def flush(self):
        for index in range(16):
            node = CHANNELS+index*84
            sync = self.get(node+3, 1) >> 3
            if not sync:
                continue
            if sync & 2:
                self.invoke(0x037FEA20, [index, 0])
            volume = self.get(node+0x24, 2)
            timer, pan = self.get(node+0x26, 2), self.get(node+0x23, 1)
            if sync & 1:
                kind = self.get(node+1, 1)
                if kind == 0:
                    self.invoke(0x037FE804, [index, self.get(node+0x44, 4), self.get(node+0x38, 1),
                        1 if self.get(node+0x39, 1) else 2, self.get(node+0x3E, 2), self.get(node+0x40, 4),
                        volume & 255, volume >> 8, timer, pan])
                elif kind == 1:
                    self.invoke(0x037FE8D0, [index, self.get(node+0x44, 4), volume & 255, volume >> 8, timer, pan])
                elif kind == 2:
                    self.invoke(0x037FE97C, [index, volume & 255, volume >> 8, timer, pan])
            else:
                if sync & 4:
                    self.invoke(0x037FEAC0, [index, timer])
                if sync & 8:
                    self.invoke(0x037FEA48, [index, volume & 255, volume >> 8])
                if sync & 16:
                    self.invoke(0x037FEAD8, [index, pan])
        for index in range(16):
            node = CHANNELS+index*84
            flags = self.get(node+3, 1)
            sync = flags >> 3
            if not sync:
                continue
            if sync & 1:
                register = MMIO+0x403+index*16
                self.put(register, 1, self.get(register, 1) | 128)
            self.put(node+3, 1, flags & 7)
