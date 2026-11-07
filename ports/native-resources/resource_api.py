import ctypes as c
from pathlib import Path


class Scope(c.Structure):
    _fields_ = [(name, c.c_uint32) for name in ('program', 'processor', 'module', 'generation')]


class Region(c.Structure):
    _fields_ = [('scope', Scope), ('base', c.c_uint32), ('length', c.c_uint32), ('bytes', c.c_void_p)]


class Space(c.Structure):
    _fields_ = [('count', c.c_uint32), ('regions', Region * 16)]


class Entry(c.Structure):
    _fields_ = [(name, c.c_uint32) for name in ('id', 'start', 'bytes')]


def bind(path):
    lib = c.CDLL(str(Path(path).resolve()))
    signatures = {
        'j2p_guest_map': (c.c_int, [c.POINTER(Space), Scope, c.c_uint32, c.c_void_p, c.c_uint32]),
        'j2p_nitrofs_mount': (c.c_void_p, [c.c_char_p, c.c_uint32, Scope]),
        'j2p_nitrofs_unmount': (None, [c.c_void_p]),
        'j2p_nitrofs_lookup': (c.c_int, [c.c_void_p, Scope, c.c_char_p, c.POINTER(Entry)]),
        'j2p_nitrofs_file_id': (c.c_int, [c.c_void_p, Scope, c.c_uint32, c.POINTER(Entry)]),
        'j2p_nitrofs_metric': (c.c_uint32, [c.c_void_p, c.c_uint32]),
        'j2p_nitrofs_read': (c.c_int, [c.c_void_p, Scope, c.c_uint32, c.c_uint32, c.POINTER(Space), c.c_uint32, c.c_uint32]),
        'j2p_nitrofs_resource_create': (c.c_void_p, [c.c_void_p, c.POINTER(Space), Scope, c.c_uint32, c.c_uint32, c.c_uint32]),
        'j2p_resource_load': (c.c_uint32, [c.c_void_p, c.c_uint32, c.c_uint32, c.c_uint32]),
        'j2p_resource_release': (c.c_int, [c.c_void_p, c.c_uint32]),
        'j2p_resource_destroy': (None, [c.c_void_p]),
        'j2p_resource_metric': (c.c_uint32, [c.c_void_p, c.c_uint32]),
        'j2p_g3d_dict_data': (c.c_uint32, [c.POINTER(Space), Scope, c.c_uint32, c.c_uint32]),
        'j2p_g3d_dict_index': (c.c_uint32, [c.POINTER(Space), Scope, c.c_uint32, c.c_uint32]),
        'j2p_g3d_material_texture': (c.c_int, [c.POINTER(Space), Scope, c.c_uint32, c.c_uint32, c.c_uint32]),
        'j2p_g3d_material_palette': (c.c_int, [c.POINTER(Space), Scope, c.c_uint32, c.c_uint32, c.c_uint32]),
    }
    for name, (result, arguments) in signatures.items():
        function = getattr(lib, name)
        function.restype, function.argtypes = result, arguments
    return lib


class Mapping:
    def __init__(self, library, scope=None):
        self.lib, self.scope, self.space, self.buffers = library, scope or Scope(0, 9, 1, 1), Space(), []

    def add(self, address, data):
        data = bytes(data)
        raw = (c.c_ubyte * (len(data) + 2))(*([0xa5] * (len(data) + 2)))
        c.memmove(c.addressof(raw) + 1, data, len(data))
        assert self.lib.j2p_guest_map(c.byref(self.space), self.scope, address, c.addressof(raw) + 1, len(data)) == 1
        self.buffers.append(raw)
        return raw

    def guards(self):
        assert all(raw[0] == 0xa5 and raw[-1] == 0xa5 for raw in self.buffers)
