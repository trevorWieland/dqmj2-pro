import arm7_seq_neighbor_model_20261030 as memory

CHANNELS, MMIO, SQUARE, SINE = 0x03807EE0, 0x04000000, 0x0380704C, 0x03807028


class UnsupportedDomain(ValueError):
    pass


def divide(value, denominator):
    return abs(value)//abs(denominator)*(-1 if (value < 0) != (denominator < 0) else 1)


class Model(memory.Model):
    def __init__(self, ram, wram, io, services):
        super().__init__(ram, wram)
        self.regions[MMIO] = bytearray(io)
        self.services = services
        self.service_calls = []

    def service(self, number, argument):
        if self.services is None:
            raise UnsupportedDomain('Original BIOS table service is absent')
        if not 0 <= argument <= (767 if number == 27 else 723):
            raise UnsupportedDomain('BIOS table index exceeds bounded service contract')
        result = self.services['pitch' if number == 27 else 'volume']
        if not 0 <= result <= (65535 if number == 27 else 127):
            raise UnsupportedDomain('Synthetic service word exceeds declared ABI')
        self.service_calls.append([number, argument, result])
        return result

    def envelope(self, node, step):
        status = self.get(node+2, 1)
        attenuation = self.get(node+0x10, 4, True)
        if step:
            if status == 0:
                attenuation = -(((-attenuation*self.get(node+0x1C, 1)) & 0xFFFFFFFF) >> 8)
                self.put(node+0x10, 4, attenuation)
                if attenuation == 0:
                    self.put(node+2, 1, 1)
            elif status == 1:
                sustain = self.get(SQUARE+self.get(node+0x1D, 1)*2, 2, True)*128
                attenuation -= self.get(node+0x1E, 2)
                self.put(node+0x10, 4, attenuation)
                if attenuation <= sustain:
                    attenuation = sustain
                    self.put(node+0x10, 4, attenuation)
                    self.put(node+2, 1, 2)
            elif status == 3:
                attenuation -= self.get(node+0x20, 2)
                self.put(node+0x10, 4, attenuation)
        return memory.signed(attenuation) >> 7

    def lfo(self, node, step):
        lfo = node+0x28
        phase, delay = self.get(lfo+8, 2), self.get(lfo+6, 2)
        depth, scale = self.get(lfo+2, 1), self.get(lfo+3, 1)
        result = 0
        if depth and delay >= self.get(lfo+4, 2):
            index = phase >> 8
            if index >= 128:
                raise UnsupportedDomain('Sine index is outside supported initialized phase domain')
            table_index = index if index < 32 else 64-index if index < 64 else index-64 if index < 96 else 128-index
            sine = self.get(SINE+table_index, 1, True)*(-1 if index >= 64 else 1)
            result = sine*depth*scale
        if result:
            target = self.get(lfo, 1)
            result = result*(60 if target == 1 else 64 if target in (0, 2) else 1) >> 14
        if step:
            if delay < self.get(lfo+4, 2):
                self.put(lfo+6, 2, delay+1)
            else:
                value = phase+(self.get(lfo+1, 1) << 6)
                self.put(lfo+8, 2, value)
                self.put(lfo+8, 2, value & 255)
                self.put(lfo+8, 2, (value & 255) | (((value >> 8) % 128) << 8))
        return result

    def timer(self, timer, pitch):
        octave, normalized = divmod(-pitch, 768)
        value = (self.service(27, normalized)+65536)*timer
        shift = octave-16
        if shift <= 0:
            value >>= -shift
        elif shift < 32:
            if value & (((1 << 64)-1) << (32-shift)):
                return 65535
            value <<= shift
        else:
            return 65535
        return max(16, min(65535, value))

    def volume(self, value):
        value = max(-723, min(0, value))
        level = self.service(28, value+723)
        divisor = 3 if value < -240 else 2 if value < -120 else 1 if value < -60 else 0
        return level | divisor << 8

    def update(self, step):
        for index in range(16):
            node = CHANNELS+index*84
            flags = self.get(node+3, 1)
            if not flags & 1:
                continue
            if flags & 2:
                self.put(node+3, 1, flags | 8)
                self.put(node+3, 1, (flags | 8) & ~2)
            elif not self.get(MMIO+0x400+index*16, 4) >> 31:
                callback = self.get(node+0x48, 4)
                if callback:
                    if callback != 0x03800B38:
                        raise UnsupportedDomain('Unqualified callback')
                    self.callback(node, 1, self.get(node+0x4C, 4))
                else:
                    self.put(node+0x22, 1, 0)
                self.put(node+0x24, 2, 0)
                self.put(node+3, 1, self.get(node+3, 1) & ~1)
                continue
            vol = self.get(SQUARE+self.get(node+9, 1)*2, 2, True)+self.envelope(node, step)
            pitch = (self.get(node+8, 1)-self.get(node+5, 1))*64
            sweep, position, length = self.get(node+0x32, 2, True), self.get(node+0x14, 4, True), self.get(node+0x18, 4, True)
            if sweep and position < length:
                if length <= 0 or position < 0:
                    raise UnsupportedDomain('Sweep fixture is outside positive-length bounded domain')
                pitch += divide(sweep*(length-position), length)
                if step and self.get(node+3, 1) & 4:
                    self.put(node+0x14, 4, position+1)
            vol += self.get(node+0xC, 2, True)+self.get(node+6, 2, True)
            pitch += self.get(node+0xE, 2, True)
            value = self.lfo(node, step)
            target, pan = self.get(node+0x28, 1), 0
            if target == 1 and vol > -32768:
                vol += value
            elif target == 2:
                pan += value
            elif target == 0:
                pitch += value
            pan += self.get(node+0xA, 1, True)
            if self.get(node+4, 1) != 127:
                pan = (pan*self.get(node+4, 1)+64) >> 7
            pan += self.get(node+0xB, 1, True)
            if self.get(node+2, 1) == 3 and vol <= -723:
                self.put(node+3, 1, (self.get(node+3, 1) & 7) | 16)
                if self.get(node+0x48, 4):
                    self.callback(node, 1, self.get(node+0x4C, 4))
                else:
                    self.put(node+0x22, 1, 0)
                self.put(node+0x24, 2, 0)
                self.put(node+3, 1, self.get(node+3, 1) & ~1)
                continue
            vol = self.volume(vol)
            timer = self.timer(self.get(node+0x3C, 2), pitch)
            if self.get(node+1, 1) == 1:
                timer &= 0xFFFC
            pan = max(0, min(127, pan+64))
            for offset, size, value, bit in ((0x24, 2, vol, 64), (0x26, 2, timer, 32), (0x23, 1, pan, 128)):
                if self.get(node+offset, size) != value:
                    self.put(node+offset, size, value)
                    self.put(node+3, 1, self.get(node+3, 1) | bit)
