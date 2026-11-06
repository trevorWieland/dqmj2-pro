import arm7_seq_prepare_model_20261030_62 as sequence
import arm7_seq_neighbor_model_20261030 as memory

RANDOM_STATE = 0x038075CC


class Model(sequence.Model):
    def halfword(self, track):
        return self.read(track) | self.read(track) << 8

    def parse(self, arguments):
        track, player, kind = arguments
        if kind == 0:
            return self.read(track)
        if kind == 1:
            return self.halfword(track)
        if kind == 2:
            accumulated = 0
            for unused in range(32):
                byte = self.read(track)
                accumulated = (accumulated << 7 | byte & 127) & 0xFFFFFFFF
                if not byte & 128:
                    return accumulated
            raise ValueError('Synthetic VLV exceeds independently qualified 32-byte extent')
        if kind == 3:
            lower = memory.signed(self.halfword(track), 16)
            upper = memory.signed(self.halfword(track), 16)
            state = (self.get(RANDOM_STATE, 4)*1664525+1013904223) & 0xFFFFFFFF
            self.put(RANDOM_STATE, 4, state)
            product = memory.signed(((upper-lower+1)*(state >> 16)) & 0xFFFFFFFF)
            return (lower+(product >> 16)) & 0xFFFFFFFF
        if kind == 4:
            index = self.read(track)
            shared = self.get(sequence.SHARED, 4)
            if not shared:
                raise ValueError('Null-variable native return is not defined C result')
            pointer = shared+0x20+self.get(player+1, 1)*36+index*2 if index < 16 else shared+0x260+(index-16)*2
            return self.get(pointer, 2, True) & 0xFFFFFFFF
        raise ValueError('Invalid value selector has no defined C result')
