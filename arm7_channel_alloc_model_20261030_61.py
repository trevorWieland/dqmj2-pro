import arm7_seq_neighbor_model_20261030 as memory

POOL, MASKS, ORDER, SHIFTS = 0x03807EE0, 0x03807EB8, 0x03807250, 0x0380724C


class Model(memory.Model):
    def volume(self, channel):
        value = self.get(channel + 0x24, 2)
        if value >> 8 > 3:
            raise ValueError('Packed-volume high byte outside qualified four-entry table')
        return ((value & 255) << 4) >> self.get(SHIFTS + (value >> 8), 1)

    def allocate(self, arguments):
        mask, priority, flags, callback, callback_data = arguments
        mask &= ~self.get(MASKS + 4, 4)
        if flags == 0:
            mask &= ~self.get(MASKS, 4)
        selected = 0
        for index in range(16):
            candidate_id = self.get(ORDER + index, 1)
            if candidate_id >= 16:
                raise ValueError('Original channel allocation order outside pool')
            if not mask & (1 << candidate_id):
                continue
            channel = POOL + candidate_id * 84
            if not selected:
                selected = channel
            elif self.get(channel + 0x22, 1) < self.get(selected + 0x22, 1):
                selected = channel
            elif self.get(channel + 0x22, 1) == self.get(selected + 0x22, 1) and self.volume(selected) > self.volume(channel):
                selected = channel
        if not selected or memory.signed(priority) < self.get(selected + 0x22, 1):
            return 0
        if self.get(selected + 0x48, 4):
            if self.get(selected + 0x48, 4) != 0x03800B38:
                raise ValueError('Callback outside qualified original linked-list remover')
            self.callback(selected, 0, self.get(selected + 0x4C, 4))
        self.put(selected + 3, 1, (self.get(selected + 3, 1) & 6) | 16)
        for offset, size, value in ((0x50, 4, 0), (0x48, 4, callback), (0x4C, 4, callback_data),
                (0x34, 4, 0), (0x22, 1, priority), (0x24, 2, 127)):
            self.put(selected + offset, size, value)
        self.put(selected + 3, 1, (self.get(selected + 3, 1) & ~2) | 4)
        for offset, size, value in ((8, 1, 60), (5, 1, 60), (9, 1, 127), (10, 1, 0),
                (12, 2, 0), (6, 2, 0), (14, 2, 0), (11, 1, 0), (4, 1, 127),
                (0x32, 2, 0), (0x18, 4, 0), (0x14, 4, 0), (0x1C, 1, 0),
                (0x1E, 2, 65535), (0x1D, 1, 127), (0x20, 2, 65535),
                (0x28, 1, 0), (0x2A, 1, 0), (0x2B, 1, 1), (0x29, 1, 16), (0x2C, 2, 0)):
            self.put(selected + offset, size, value)
        return selected
