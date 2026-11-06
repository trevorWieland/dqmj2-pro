import arm7_seq_neighbor_model_20261030 as memory

PLAYERS, TRACKS, SHARED, CACHE = 0x03808420, 0x03808660, 0x03807EDC, 0x03807EC0


class Model(memory.Model):
    def allocate(self):
        for index in range(32):
            address = TRACKS + index*64
            if not self.get(address, 1) & 1:
                self.put(address, 1, self.get(address, 1) | 1)
                return index
        return -1

    def initialize_track(self, track):
        self.put(track+0x24, 4, 0)
        self.put(track+0x28, 4, 0)
        flags = self.get(track, 1) | 2
        self.put(track, 1, flags)
        for bit in (4, 8, 16):
            flags &= ~bit
            self.put(track, 1, flags)
        self.put(track, 1, (flags & ~32 | 64) & ~128)
        fields = ((0x3B, 1, 0), (2, 2, 0), (0x12, 1, 64), (4, 1, 127), (5, 1, 127),
            (10, 2, 0), (8, 1, 0), (9, 1, 0), (6, 1, 0), (12, 2, 0),
            (14, 1, 255), (15, 1, 255), (16, 1, 255), (17, 1, 255),
            (1, 1, 127), (7, 1, 2), (0x14, 1, 60), (0x15, 1, 0),
            (0x16, 2, 0), (0x13, 1, 0), (0x1E, 2, 65535),
            (0x18, 1, 0), (0x1A, 1, 0), (0x1B, 1, 1), (0x19, 1, 16),
            (0x1C, 2, 0), (0x20, 4, 0), (0x3C, 4, 0))
        for offset, size, value in fields:
            self.put(track+offset, size, value)

    def fetch(self, current):
        begin = current & ~3
        self.put(CACHE+4, 4, begin)
        self.put(CACHE+8, 4, begin+16)
        for index in range(4):
            self.put(CACHE+12+index*4, 4, self.get(begin+index*4, 4))

    def read(self, track):
        current = self.get(track+0x28, 4)
        if not self.get(CACHE+4, 4) <= current < self.get(CACHE+8, 4):
            self.fetch(current)
        result = self.get(CACHE+12+current-self.get(CACHE+4, 4), 1)
        self.put(track+0x28, 4, current+1)
        return result

    def prepare(self, arguments):
        index, sequence, offset, bank = arguments
        player = PLAYERS+index*36
        if self.get(player, 1) & 1:
            self.invoke(0x03800B00, [player, 0, 0])
        self.put(player, 1, self.get(player, 1) & ~4)
        for location, size, value in ((0x20, 4, bank), (0x18, 2, 120), (0x1A, 2, 256),
                (0x1C, 2, 240), (5, 1, 127), (6, 2, 0), (4, 1, 64)):
            self.put(player+location, size, value)
        for slot in range(16):
            self.put(player+8+slot, 1, 255)
        shared = self.get(SHARED, 4)
        if shared:
            identity = self.get(player+1, 1)
            self.put(shared+0x40+identity*36, 4, 0)
            for slot in range(16):
                self.put(shared+0x20+identity*36+slot*2, 2, 65535)
        allocated = self.allocate()
        if allocated < 0:
            return
        track = TRACKS+allocated*64
        self.initialize_track(track)
        self.put(track+0x24, 4, sequence)
        self.put(track+0x28, 4, sequence+offset)
        self.put(player+8, 1, allocated)
        self.fetch(self.get(track+0x28, 4))
        command = self.read(track)
        if command != 254:
            self.put(track+0x28, 4, self.get(track+0x28, 4)-1)
        else:
            mask = (self.read(track) | self.read(track) << 8) >> 1
            slot = 1
            while mask:
                if mask & 1:
                    allocated = self.allocate()
                    if allocated < 0:
                        break
                    self.initialize_track(TRACKS+allocated*64)
                    self.put(player+8+slot, 1, allocated)
                slot, mask = slot+1, mask >> 1
        self.put(player, 1, (self.get(player, 1) | 1) & ~2)
        if shared:
            self.put(shared+4, 4, self.get(shared+4, 4) | 1 << index)
