import arm7_value_parse_model_20261030_63 as values
import arm7_seq_neighbor_model_20261030 as memory
import arm7_channel_alloc_model_20261030_61 as allocation
import arm7_note_on_model_20261030_60 as notes


class UnsupportedDomain(ValueError):
    pass


class Model(values.Model, allocation.Model, notes.Model):
    def read24(self, track):
        return self.read(track) | self.read(track) << 8 | self.read(track) << 16

    def variable(self, player, index):
        shared = self.get(0x03807EDC, 4)
        if not shared:
            return 0
        return shared+0x20+self.get(player+1, 1)*36+index*2 if index < 16 else shared+0x260+(index-16)*2

    def mute(self, track, player, mode):
        if mode == 0:
            self.put(track, 1, self.get(track, 1) & ~4)
        elif mode in (1, 2, 3):
            self.put(track, 1, self.get(track, 1) | 4)
            if mode >= 2:
                self.release(track, player, 127 if mode == 3 else 0xFFFFFFFF)
                if mode == 3:
                    self.free_chain(track)

    def instrument(self, bank, program, midi):
        if program >= self.get(bank+0x38, 4):
            return None
        entry = self.get(bank+0x3C+program*4, 4)
        kind, source = entry & 255, bank+(entry >> 8)
        if 1 <= kind <= 5:
            return bytearray([kind, 0])+bytearray(self.get(source+offset, 1) for offset in range(10))
        if kind == 16:
            low, high = self.get(source, 1), self.get(source+1, 1)
            if not low <= midi <= high:
                return None
            source += 2+(midi-low)*12
        elif kind == 17:
            selected = next((index for index in range(8) if midi <= self.get(source+index, 1)), None)
            if selected is None:
                return None
            source += 8+selected*12
        else:
            return None
        return bytearray(self.get(source+offset, 1) for offset in range(12))

    def play_note(self, track, player, midi, velocity, length):
        channel = self.get(track+0x3C, 4) if self.get(track, 1) & 8 else 0
        if channel:
            self.put(channel+8, 1, midi)
            self.put(channel+9, 1, velocity)
        else:
            bank = self.get(player+0x20, 4)
            instrument = self.instrument(bank, self.get(track+2, 2), midi)
            if instrument is None or instrument[0] not in (1, 2, 3, 4):
                return
            kind = instrument[0]
            allowed = (65535 if kind in (1, 4) else 0x3F00 if kind == 2 else 0xC000) & self.get(track+0x1E, 2)
            priority = self.get(player+4, 1)+self.get(track+0x12, 1)
            channel = allocation.Model.allocate(self, [allowed, priority, int(bool(self.get(track, 1) & 128)), 0x03800B38, track])
            if not channel:
                return
            scratch = 0x023D0000
            self.regions[scratch] = instrument
            try:
                success = notes.Model.note(self, [channel, midi, velocity,
                    0xFFFFFFFF if self.get(track, 1) & 8 else length & 0xFFFFFFFF, bank, scratch])
            finally:
                del self.regions[scratch]
            if not success:
                self.put(channel+0x22, 1, 0)
                self.free(channel)
                return
            self.put(channel+0x50, 4, self.get(track+0x3C, 4))
            self.put(track+0x3C, 4, channel)
        for track_offset, channel_offset, size in ((14, 0x1C, 1), (15, 0x1E, 2), (16, 0x1D, 1), (17, 0x20, 2)):
            value = self.get(track+track_offset, 1)
            if value != 255:
                coefficient = (255-value if value < 109 else self.get(notes.ATTACK+127-value, 1)) if track_offset == 14 else value if track_offset == 16 else notes.decay(value)
                self.put(channel+channel_offset, size, coefficient)
        self.put(channel+0x32, 2, self.get(track+0x16, 2))
        if self.get(track, 1) & 32:
            self.put(channel+0x32, 2, self.get(channel+0x32, 2)+(self.get(track+0x14, 1)-midi)*64)
        time = self.get(track+0x15, 1)
        if time == 0:
            self.put(channel+0x18, 4, length)
            self.put(channel+3, 1, self.get(channel+3, 1) & ~4)
        else:
            sweep = self.get(channel+0x32, 2, True)
            self.put(channel+0x18, 4, (time*time*abs(sweep)) >> 11)
        self.put(channel+0x14, 4, 0)

    def track_step(self, track, player, play_notes):
        node = self.get(track+0x3C, 4)
        while node:
            length = self.get(node+0x34, 4, True)
            if length > 0:
                self.put(node+0x34, 4, length-1)
            if not self.get(node+3, 1) & 4:
                position = self.get(node+0x14, 4, True)
                if position < self.get(node+0x18, 4, True):
                    self.put(node+0x14, 4, position+1)
            node = self.get(node+0x50, 4)
        flags = self.get(track, 1)
        if flags & 16:
            if self.get(track+0x3C, 4):
                return False
            self.put(track, 1, flags & ~16)
        wait = self.get(track+0x20, 4, True)
        if wait > 0:
            self.put(track+0x20, 4, wait-1)
            if wait-1 > 0:
                return False
        self.fetch(self.get(track+0x28, 4))
        for unused in range(128):
            if self.get(track+0x20, 4) or self.get(track, 1) & 16:
                return False
            special, execute, kind = False, True, 0
            command = self.read(track)
            if command == 162:
                command = self.read(track)
                execute = bool(self.get(track, 1) & 64)
            if command == 160:
                command, special, kind = self.read(track), True, 3
            if command == 161:
                command, special, kind = self.read(track), True, 4
            if command < 128:
                velocity = self.read(track)
                length = memory.signed(self.parse([track, player, kind if special else 2]))
                midi = max(0, min(127, command+self.get(track+0x13, 1, True)))
                if not execute:
                    continue
                if not self.get(track, 1) & 4 and play_notes:
                    self.play_note(track, player, midi, velocity, length if length > 0 else -1)
                self.put(track+0x14, 1, midi)
                if self.get(track, 1) & 2:
                    self.put(track+0x20, 4, length)
                    if length == 0:
                        self.put(track, 1, self.get(track, 1) | 16)
                continue
            category = command & 240
            if category == 128:
                parameter = memory.signed(self.parse([track, player, kind if special else 2]))
                if execute and command == 128:
                    self.put(track+0x20, 4, parameter)
                elif execute and command == 129 and parameter < 65536:
                    self.put(track+2, 2, parameter)
            elif category == 144:
                if command == 147:
                    slot = self.read(track)
                    offset = self.read24(track)
                    if execute:
                        other = self.getter(player, slot)
                        if other and other != track:
                            self.release(other, player, 0xFFFFFFFF)
                            self.free_chain(other)
                            self.put(other+0x24, 4, self.get(track+0x24, 4))
                            self.put(other+0x28, 4, self.get(track+0x24, 4)+offset)
                elif command in (148, 149):
                    offset = self.read24(track)
                    if execute and command == 148:
                        self.put(track+0x28, 4, self.get(track+0x24, 4)+offset)
                    elif execute and self.get(track+0x3B, 1) < 3:
                        depth = self.get(track+0x3B, 1)
                        self.put(track+0x2C+depth*4, 4, self.get(track+0x28, 4))
                        self.put(track+0x3B, 1, depth+1)
                        self.put(track+0x28, 4, self.get(track+0x24, 4)+offset)
                else:
                    pass
            elif category in (192, 208):
                parameter = self.parse([track, player, kind if special else 0]) & 255
                if not execute:
                    continue
                fields = {193: (track+4, 1, parameter), 213: (track+5, 1, parameter),
                    194: (player+5, 1, parameter), 197: (track+7, 1, parameter),
                    198: (track+0x12, 1, parameter), 207: (track+0x15, 1, parameter),
                    202: (track+0x1A, 1, parameter), 203: (track+0x19, 1, parameter),
                    204: (track+0x18, 1, parameter), 205: (track+0x1B, 1, parameter),
                    208: (track+14, 1, parameter), 209: (track+15, 1, parameter),
                    210: (track+16, 1, parameter), 211: (track+17, 1, parameter),
                    195: (track+0x13, 1, parameter), 196: (track+6, 1, parameter),
                    192: (track+8, 1, parameter-64)}
                if command in fields:
                    self.put(*fields[command])
                elif command in (199, 206):
                    bit = 2 if command == 199 else 32
                    self.put(track, 1, (self.get(track, 1) & ~bit) | ((parameter & 1)*bit))
                elif command == 200:
                    self.put(track, 1, (self.get(track, 1) & ~8) | ((parameter & 1)*8))
                    self.release(track, player, 0xFFFFFFFF)
                    self.free_chain(track)
                elif command == 201:
                    self.put(track+0x14, 1, parameter+self.get(track+0x13, 1, True))
                    self.put(track, 1, self.get(track, 1) | 32)
                elif command == 212:
                    depth = self.get(track+0x3B, 1)
                    if depth < 3:
                        self.put(track+0x2C+depth*4, 4, self.get(track+0x28, 4))
                        self.put(track+0x38+depth, 1, parameter)
                        self.put(track+0x3B, 1, depth+1)
                elif command == 214:
                    pass
                elif command == 215:
                    self.mute(track, player, parameter)
                else:
                    pass
            elif category == 224:
                parameter = self.parse([track, player, kind if special else 1])
                if execute and command in (224, 225, 227):
                    self.put(player+0x18 if command == 225 else track+(0x16 if command == 227 else 0x1C), 2, parameter)
                elif execute:
                    pass
            elif category == 176:
                index = self.read(track)
                parameter = memory.signed(self.parse([track, player, kind if special else 1]), 16)
                pointer = self.variable(player, index)
                if execute and pointer:
                    current = self.get(pointer, 2, True)
                    if command in (176, 177, 178, 179, 180, 181, 182):
                        if command == 176:
                            value = parameter
                        elif command == 177:
                            value = current+parameter
                        elif command == 178:
                            value = current-parameter
                        elif command == 179:
                            value = current*parameter
                        elif command == 180:
                            if parameter == 0:
                                continue
                            value = abs(current)//abs(parameter)*(-1 if (current < 0) != (parameter < 0) else 1)
                        elif command == 181:
                            count = abs(parameter) & 255
                            value = ((current << count) & 0xFFFFFFFF if count < 32 else 0) if parameter >= 0 else current >> min(count, 32)
                        else:
                            negative = parameter < 0
                            bound = memory.signed((-parameter) & 65535, 16) if negative else parameter
                            state = (self.get(values.RANDOM_STATE, 4)*1664525+1013904223) & 0xFFFFFFFF
                            self.put(values.RANDOM_STATE, 4, state)
                            value = memory.signed(((state >> 16)*(bound+1)) & 0xFFFFFFFF) >> 16
                            if negative:
                                value = -value
                        self.put(pointer, 2, value)
                    elif command == 183:
                        pass
                    elif 184 <= command <= 189:
                        test = (current == parameter, current >= parameter, current > parameter, current <= parameter, current < parameter, current != parameter)[command-184]
                        self.put(track, 1, (self.get(track, 1) & ~64) | int(test)*64)
                    else:
                        pass
            elif category == 240:
                if not execute:
                    continue
                depth = self.get(track+0x3B, 1)
                if command == 255:
                    return True
                if command == 253 and depth:
                    self.put(track+0x3B, 1, depth-1)
                    self.put(track+0x28, 4, self.get(track+0x2C+(depth-1)*4, 4))
                elif command == 252 and depth:
                    count = self.get(track+0x38+depth-1, 1)
                    if count:
                        count -= 1
                        if count == 0:
                            self.put(track+0x3B, 1, depth-1)
                            continue
                    self.put(track+0x38+depth-1, 1, count)
                    self.put(track+0x28, 4, self.get(track+0x2C+(depth-1)*4, 4))
                elif command not in (252, 253, 254):
                    pass
            else:
                pass
        raise UnsupportedDomain('Synthetic instruction stream exhausted model command cap')

    def player_step(self, player, play_notes):
        active = False
        for index in range(16):
            track = self.getter(player, index)
            if track and self.get(track+0x28, 4):
                if self.track_step(track, player, play_notes):
                    self.stop_track(player, index)
                else:
                    active = True
        return int(not active)
