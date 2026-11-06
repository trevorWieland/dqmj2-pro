import arm7_seq_neighbor_model_20261030 as memory

ATTACK = 0x03807260


def decay(value):
    if value == 127:
        return 65535
    if value == 126:
        return 15360
    if value < 50:
        return value * 2 + 1
    denominator = 126 - value
    return (7680 // abs(denominator)) * (1 if denominator > 0 else -1) & 65535


class Model(memory.Model):
    def start(self, channel, length):
        for offset, size, value in ((0x10, 4, -92544), (2, 1, 0), (0x34, 4, length), (0x30, 2, 0), (0x2E, 2, 0)):
            self.put(channel + offset, size, value)
        self.put(channel + 3, 1, self.get(channel + 3, 1) | 3)

    def note(self, arguments):
        channel, midi, velocity, length, bank, instrument = arguments
        release = self.get(instrument + 10, 1)
        if release == 255:
            length, release = 0xFFFFFFFF, 0
        kind, wave = self.get(instrument, 1), 0
        if kind in (1, 4):
            if kind == 1:
                archive = self.get(bank + 0x18 + self.get(instrument + 4, 2) * 8, 4)
                index = self.get(instrument + 2, 2)
                if archive and index < self.get(archive + 0x38, 4):
                    stored = self.get(archive + 0x3C + index * 4, 4)
                    if stored:
                        wave = (archive + stored) & 0xFFFFFFFF if stored < 0x02000000 else stored
            else:
                wave = self.get(instrument + 2, 2) | self.get(instrument + 4, 2) << 16
            if not wave:
                return 0
            self.put(channel + 1, 1, 0)
            for offset in (0, 4, 8):
                self.put(channel + 0x38 + offset, 4, self.get(wave + offset, 4))
            self.put(channel + 0x44, 4, wave + 12)
            self.start(channel, length)
        elif kind == 2:
            if not 8 <= self.get(channel, 1) <= 13:
                return 0
            self.put(channel + 1, 1, 1)
            self.put(channel + 0x44, 4, self.get(instrument + 2, 2))
            self.put(channel + 0x3C, 2, 8006)
            self.start(channel, length)
        elif kind == 3:
            if not 14 <= self.get(channel, 1) <= 15:
                return 0
            self.put(channel + 1, 1, 2)
            self.put(channel + 0x3C, 2, 8006)
            self.start(channel, length)
        else:
            return 0
        self.put(channel + 8, 1, midi)
        self.put(channel + 5, 1, self.get(instrument + 6, 1))
        self.put(channel + 9, 1, velocity)
        attack = self.get(instrument + 7, 1)
        coefficient = 255 - attack if attack < 109 else self.get(ATTACK + 127 - attack, 1)
        self.put(channel + 0x1C, 1, coefficient)
        self.put(channel + 0x1E, 2, decay(self.get(instrument + 8, 1)))
        self.put(channel + 0x1D, 1, self.get(instrument + 9, 1))
        self.put(channel + 0x20, 2, decay(release))
        self.put(channel + 10, 1, self.get(instrument + 11, 1) - 64)
        return 1
