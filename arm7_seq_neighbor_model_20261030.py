BASE, DATA, STACK, RETURN = 0x037F8000, 0x023C0000, 0x023E0000, 0x023FF000
TRACK, PLAYER, NODES, TRACKS, TABLE = DATA + 0x100, DATA + 0x200, DATA + 0x1000, 0x03808660, 0x0380704C


def signed(value, bits=32):
    value &= (1 << bits) - 1
    return value - (1 << bits) if value >> (bits - 1) else value


class Model:
    def __init__(self, ram, wram):
        self.regions = {DATA: bytearray(ram), BASE: bytearray(wram)}
        self.writes = []

    def region(self, address, length):
        for base, data in self.regions.items():
            if base <= address and address + length <= base + len(data):
                return data, address - base
        raise ValueError('Independent model address is outside mapped input')

    def get(self, address, length, negative=False):
        data, offset = self.region(address, length)
        return int.from_bytes(data[offset:offset + length], 'little', signed=negative)

    def put(self, address, length, value):
        data, offset = self.region(address, length)
        value &= (1 << (length * 8)) - 1
        data[offset:offset + length] = value.to_bytes(length, 'little')
        self.writes.append([address, length, value])

    def update(self, track, player):
        volume = sum(self.get(TABLE + self.get(address, 1) * 2, 2, True) for address in (track + 4, track + 5, player + 5))
        volume = max(-32768, volume)
        fader = max(-32768, self.get(track + 10, 2, True) + self.get(player + 6, 2, True))
        pitch = self.get(track + 12, 2, True) + ((self.get(track + 6, 1, True) * (self.get(track + 7, 1) << 6)) >> 7)
        pan, scale = self.get(track + 8, 1, True), self.get(track + 1, 1)
        if scale != 127:
            pan = (pan * scale + 64) >> 7
        pan = max(-128, min(127, pan + self.get(track + 9, 1, True)))
        node = self.get(track + 0x3C, 4)
        while node:
            self.put(node + 6, 2, fader)
            if self.get(node + 2, 1) != 3:
                for offset, size, value in ((12, 2, volume), (14, 2, pitch), (11, 1, pan), (4, 1, scale)):
                    self.put(node + offset, size, value)
                for offset in (0, 2, 4):
                    self.put(node + 0x28 + offset, 2, self.get(track + 0x18 + offset, 2))
            node = self.get(node + 0x50, 4)

    def release(self, track, player, amount):
        self.update(track, player)
        node = self.get(track + 0x3C, 4)
        while node:
            if self.get(node + 3, 1) & 1:
                if signed(amount) >= 0:
                    rate = amount & 255
                    if rate == 127:
                        value = 0xFFFF
                    elif rate == 126:
                        value = 0x3C00
                    elif rate < 50:
                        value = 2 * rate + 1
                    else:
                        denominator = 126 - rate
                        value = (7680 // abs(denominator)) * (1 if denominator > 0 else -1)
                    self.put(node + 0x20, 2, value)
                self.put(node + 0x22, 1, 1)
                self.put(node + 2, 1, 3)
            node = self.get(node + 0x50, 4)

    def free(self, node):
        if node:
            self.put(node + 0x48, 4, 0)
            self.put(node + 0x4C, 4, 0)

    def free_chain(self, track):
        node = self.get(track + 0x3C, 4)
        while node:
            self.free(node)
            node = self.get(node + 0x50, 4)
        self.put(track + 0x3C, 4, 0)

    def getter(self, player, index):
        index = signed(index)
        if index > 15:
            return 0
        slot = self.get(player + 8 + index, 1)
        return 0 if slot == 255 else TRACKS + slot * 64

    def stop_track(self, player, index):
        track = self.getter(player, index)
        if not track:
            return
        self.release(track, player, 0xFFFFFFFF)
        self.free_chain(track)
        slot = self.get(player + 8 + signed(index), 1)
        address = TRACKS + slot * 64
        self.put(address, 1, self.get(address, 1) & ~1)
        self.put(player + 8 + signed(index), 1, 255)

    def callback(self, node, status, track):
        if status == 1:
            self.put(node + 0x22, 1, 0)
            self.free(node)
        if self.get(track + 0x3C, 4) == node:
            self.put(track + 0x3C, 4, self.get(node + 0x50, 4))
            return
        current = self.get(track + 0x3C, 4)
        while self.get(current + 0x50, 4):
            if self.get(current + 0x50, 4) == node:
                self.put(current + 0x50, 4, self.get(node + 0x50, 4))
                return
            current = self.get(current + 0x50, 4)

    def invoke(self, address, arguments):
        first, second, third = arguments
        if address == 0x038009E0:
            self.release(first, second, third)
        elif address == 0x03800A48:
            self.free_chain(first)
        elif address == 0x03800AA8:
            self.stop_track(first, second)
        elif address == 0x03800B00:
            for index in range(16):
                self.stop_track(first, index)
            self.put(first, 1, self.get(first, 1) & ~1)
        elif address == 0x03800B38:
            self.callback(first, second, third)
        else:
            raise ValueError('Unknown ordinary SDK neighbor unit')
