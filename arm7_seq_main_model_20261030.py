import arm7_seq_neighbor_model_20261030 as memory

PLAYERS, SHARED_POINTER = 0x03808420, 0x03807EDC


class UnsupportedScriptPath(ValueError):
    pass


class Model(memory.Model):
    def update(self, track, player, release=0):
        volume = max(-32768, sum(self.get(memory.TABLE + self.get(address, 1) * 2, 2, True)
            for address in (track + 4, track + 5, player + 5)))
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
                if release and self.get(node + 0x34, 4) == 0:
                    self.put(node + 0x22, 1, 1)
                    self.put(node + 2, 1, 3)
            node = self.get(node + 0x50, 4)

    def tick(self, player):
        any_active = False
        for slot in range(16):
            track = self.getter(player, slot)
            if not track or self.get(track + 0x28, 4) == 0:
                continue
            node = self.get(track + 0x3C, 4)
            while node:
                length = self.get(node + 0x34, 4, True)
                if length > 0:
                    self.put(node + 0x34, 4, length - 1)
                if not self.get(node + 3, 1) & 4:
                    position = self.get(node + 0x14, 4, True)
                    if position < self.get(node + 0x18, 4, True):
                        self.put(node + 0x14, 4, position + 1)
                node = self.get(node + 0x50, 4)
            flags = self.get(track, 1)
            if flags & 16:
                if self.get(track + 0x3C, 4):
                    any_active = True
                    continue
                self.put(track, 1, flags & ~16)
            wait = self.get(track + 0x20, 4, True)
            if wait > 0:
                self.put(track + 0x20, 4, wait - 1)
                if wait - 1 > 0:
                    any_active = True
                    continue
            raise UnsupportedScriptPath('Positive caller fixture reached unqualified sequence-byte interpretation')
        return not any_active

    def main(self, step):
        status = 0
        for index in range(16):
            player = PLAYERS + index * 36
            if not self.get(player, 1) & 1:
                continue
            if self.get(player, 1) & 2:
                if step and not self.get(player, 1) & 4:
                    ticks = 0
                    while self.get(player + 0x1C, 2) >= 240:
                        self.put(player + 0x1C, 2, self.get(player + 0x1C, 2) - 240)
                        ticks += 1
                    completed = 0
                    while completed < ticks:
                        if self.tick(player):
                            self.invoke(0x03800B00, [player, 0, 0])
                            break
                        completed += 1
                    shared = self.get(SHARED_POINTER, 4)
                    if shared:
                        address = shared + self.get(player + 1, 1) * 36 + 0x40
                        self.put(address, 4, self.get(address, 4) + completed)
                    product = self.get(player + 0x18, 2) * self.get(player + 0x1A, 2) & 0xFFFFFFFF
                    self.put(player + 0x1C, 2, self.get(player + 0x1C, 2) + (memory.signed(product) >> 8))
                for slot in range(16):
                    track = self.getter(player, slot)
                    if track:
                        self.update(track, player, 1)
            if self.get(player, 1) & 1:
                status |= 1 << index
        shared = self.get(SHARED_POINTER, 4)
        if shared:
            self.put(shared + 4, 4, status)
