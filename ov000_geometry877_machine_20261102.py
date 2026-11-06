import struct
import ov000_geometry872_machine_20261102 as B

ENTRY = B.ENTRY
SP = B.SP
MESH = B.MESH
RECORD = B.RECORD
CONTEXT = B.CONTEXT
POINT = B.POINT
OUTPUT = B.OUTPUT
pack = B.pack
word = B.word


class Machine(B.Machine):
    def __init__(self, main, overlay, images, profile):
        super().__init__(main, overlay, images, profile)
        sx, sz = profile.get('slopeX', 0), profile.get('slopeZ', 0)
        mesh = bytearray(self.beforeMesh)
        magnitude = profile['normalMagnitude']
        sign = -1 if profile['reverse'] else 1
        normal = [sign * magnitude * sx, -sign * magnitude, sign * magnitude * sz]
        if profile['zeroNormal']:
            normal = [0, 0, 0]
        mesh[0x100:0x10C] = pack(normal)
        for index in range(3):
            offset = 0x10C + index * 12
            x, unused, z = struct.unpack_from('<iii', mesh, offset)
            struct.pack_into('<i', mesh, offset + 4, sx * x + sz * z)
        self.beforeMesh = bytes(mesh)
        self.u.mem_write(MESH, self.beforeMesh)
