import ctypes as c
import hashlib
import json
from pathlib import Path
import sys


class Scope(c.Structure):
    _fields_ = [(key, c.c_uint32) for key in ['program', 'processor', 'module', 'generation']]


class Owner(c.Structure):
    _fields_ = [('scope', Scope), ('model_set', c.c_uint32), ('model_index', c.c_uint32)]


class Region(c.Structure):
    _fields_ = [('scope', Scope), ('base', c.c_uint32), ('length', c.c_uint32), ('bytes', c.c_void_p)]


class Space(c.Structure):
    _fields_ = [('count', c.c_uint32), ('regions', Region * 16)]


class Command(c.Structure):
    _fields_ = [('owner', Owner), ('opcode', c.c_uint32), ('count', c.c_uint32), ('arguments', c.c_int32 * 16)]


class Header(c.Structure):
    _fields_ = [('owner', Owner)] + [(key, c.c_uint32) for key in ['model_bytes', 'model_address', 'model_size', 'sbc_address', 'sbc_bytes', 'required_mode', 'command_count']]


def main():
    root = Path(__file__).resolve().parent
    fixture = json.loads((root / 'synthetic-fixture.json').read_text())
    data = bytes(fixture['source'])
    raw = (c.c_ubyte * (len(data) + 2)).from_buffer_copy(b'\xa5' + data + b'\xa5')
    library = c.CDLL(str(Path(sys.argv[1]).resolve()))
    library.j2p_guest_map.argtypes = [c.POINTER(Space), Scope, c.c_uint32, c.c_void_p, c.c_uint32]
    library.j2p_static_matrix_plan.argtypes = [c.POINTER(Space), c.POINTER(Owner), c.c_uint32, c.POINTER(Command), c.c_uint32, c.POINTER(Command), c.c_uint32, c.POINTER(Header)]
    scope, space, owned, header = Scope(0, 9, 1, 1), Space(), Owner(Scope(0, 9, 1, 1), 0x02700000, 0), Header()
    assert library.j2p_guest_map(c.byref(space), scope, owned.model_set, c.addressof(raw) + 1, len(data)) == 1
    assert library.j2p_static_matrix_plan(c.byref(space), c.byref(owned), len(data), None, 0, None, 0, c.byref(header)) == 1
    scratch, output = (Command * header.command_count)(), (Command * header.command_count)()
    assert library.j2p_static_matrix_plan(c.byref(space), c.byref(owned), len(data), scratch, len(scratch), output, len(output), c.byref(header)) == 1
    rows = [dict(op=item.opcode, args=list(item.arguments[:item.count])) for item in output]
    assert rows == fixture['expectedCommands'] and header.required_mode == 2
    assert all(bytes(item.owner) == bytes(owned) for item in output)
    assert bytes(raw) == b'\xa5' + data + b'\xa5'
    print(json.dumps(dict(status='independent-source-only-copy-plans-owned-synthetic-model', commands=len(rows),
        commandSha256=hashlib.sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest(),
        originalAssetsOrPrivatePackagesRequired=False, rendering=False, deviceExecuted=False)))


if __name__ == '__main__':
    main()
