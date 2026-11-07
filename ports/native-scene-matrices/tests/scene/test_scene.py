import ctypes as c
import json
from pathlib import Path
import sys
import types

class Scope(c.Structure):
    _fields_ = [(name, c.c_uint32) for name in ('program', 'processor', 'module', 'generation')]

class Owner(c.Structure):
    _fields_ = [('scope', Scope), ('model_set', c.c_uint32), ('model_index', c.c_uint32)]

class Seed(c.Structure):
    _fields_ = [('owner', Owner), ('mode', c.c_uint32), ('matrices', (c.c_int32 * 16) * 4)]

class Command(c.Structure):
    _fields_ = [('owner', Owner), ('opcode', c.c_uint32), ('count', c.c_uint32), ('arguments', c.c_int32 * 16)]

class State(c.Structure):
    _fields_ = [('owner', Owner), ('mode', c.c_uint32), ('valid_slots', c.c_uint32), ('matrices', (c.c_int32 * 16) * 4),
        ('position_stack', (c.c_int32 * 16) * 32), ('vector_stack', (c.c_int32 * 16) * 32)]

MatrixOwner, MatrixSeed = Owner, Seed

class Region(c.Structure):
    _fields_ = [('scope', Scope), ('base', c.c_uint32), ('length', c.c_uint32), ('bytes', c.c_void_p)]

class Space(c.Structure):
    _fields_ = [('count', c.c_uint32), ('regions', Region * 16)]

class Header(c.Structure):
    _fields_ = [('owner', Owner)] + [(key, c.c_uint32) for key in ['model_bytes', 'model_address', 'model_size', 'sbc_address', 'sbc_bytes', 'required_mode', 'command_count']]

matrix = types.SimpleNamespace(Owner=Owner, Command=Command, State=State, Space=Space, Header=Header)

class Owner(c.Structure):
    _fields_ = [('model', matrix.Owner)] + [(n, c.c_uint32) for n in ['model_bytes', 'instance_id', 'run_generation',
        'matrix_generation', 'material_generation', 'attribute_generation']]

class Seed(c.Structure):
    _fields_ = [('owner', Owner), ('provider_flags', c.c_uint32), ('shader_valid', c.c_uint32),
        ('material_defaults', c.c_uint32 * 3), ('initial_shader', c.c_uint32 * 5)]

class Shader(c.Structure):
    _fields_ = [('opcode', c.c_uint32), ('parameter', c.c_uint32)]

class Event(c.Structure):
    _fields_ = [(n, c.c_uint32) for n in ['offset', 'ordinal', 'opcode', 'length', 'matrix_begin', 'matrix_count', 'shader_begin',
        'shader_count', 'flags', 'node', 'description', 'material', 'material_valid', 'material_evaluation']]
    _fields_ += [('result', c.c_uint32 * 6), ('shader_state', c.c_uint32 * 5), ('cache_valid', c.c_uint32 * 2)]
    _fields_ += [(n, c.c_uint32) for n in ['shape_reference', 'shape_index', 'shape_address', 'display_address', 'display_bytes',
        'submission', 'submission_ordinal']]

class Tape(c.Structure):
    _fields_ = [('seed', Seed), ('plan', matrix.Header)] + [(n, c.c_uint32) for n in ['version', 'events', 'shaders',
        'shape_references', 'submissions', 'nodes', 'materials', 'shapes']]

class Buffers(c.Structure):
    _fields_ = [('commands', c.POINTER(matrix.Command)), ('command_capacity', c.c_uint32),
        ('events', c.POINTER(Event)), ('event_capacity', c.c_uint32), ('shaders', c.POINTER(Shader)), ('shader_capacity', c.c_uint32)]

class Work(c.Structure):
    _fields_ = [('plan_scratch', c.POINTER(matrix.Command)), ('plan_capacity', c.c_uint32), ('stage', Buffers)]

class Entry(c.Structure):
    _fields_ = [('owner', Owner), ('state', matrix.State)]

class Snapshot(c.Structure):
    _fields_ = [('owner', Owner)] + [(n, c.c_uint32) for n in ['sbc_address', 'offset', 'event_ordinal', 'shape_index', 'shape_address',
        'display_address', 'display_bytes', 'reference_ordinal', 'submission_ordinal', 'submission', 'material', 'material_valid',
        'matrix_prefix', 'mode', 'valid_slots']] + [('matrices', (c.c_int32 * 16) * 4)]

def main():
    root = Path(__file__).resolve().parent
    lib = c.CDLL(str(Path(sys.argv[1]).resolve()))
    lib.j2p_guest_map.argtypes = [c.POINTER(Space), Scope, c.c_uint32, c.c_void_p, c.c_uint32]
    lib.j2p_matrix_init.argtypes = [c.POINTER(MatrixOwner), c.POINTER(MatrixSeed), c.POINTER(State)]
    lib.j2p_static_scene_tape.argtypes = [c.POINTER(Space), c.POINTER(Owner), c.POINTER(Seed), c.POINTER(Work), c.POINTER(Buffers), c.POINTER(Tape)]
    lib.j2p_static_scene_snapshots.argtypes = [c.POINTER(Owner), c.POINTER(Tape), c.POINTER(Command), c.POINTER(Event), c.POINTER(Entry),
        c.POINTER(Snapshot), c.c_uint32, c.POINTER(Snapshot), c.c_uint32, c.POINTER(Entry)]
    references, submissions = 0, 0
    for fixture in json.loads((root / 'copied-synthetic-fixtures-v2.json').read_text()):
        data = bytes(fixture['data'])
        raw = (c.c_uint8 * (len(data) + 2)).from_buffer_copy(b'\xa5' + data + b'\xa5')
        space, model = Space(), MatrixOwner(Scope(0, 9, 1, 1), 0x02700000, 0)
        assert lib.j2p_guest_map(c.byref(space), model.scope, model.model_set, c.addressof(raw) + 1, len(data)) == 1
        owner = Owner(model, len(data), 1, 2, 3, 4, 5)
        seed, header = Seed(owner, 0, 31), Tape()
        seed.material_defaults[:] = fixture['defaults']
        seed.initial_shader[:] = [0x1234, 0x5678, 0x1f00c0, 0, 0]
        assert lib.j2p_static_scene_tape(c.byref(space), c.byref(owner), c.byref(seed), None, None, c.byref(header)) == 1
        counts = [max(header.plan.command_count, 1), max(header.events, 1), max(header.shaders, 1)]
        a = [(t * n)() for t, n in zip([Command, Event, Shader], counts)]
        b = [(t * n)() for t, n in zip([Command, Event, Shader], counts)]
        extra = (Command * counts[0])()
        stage, output = [Buffers(v[0], counts[0], v[1], counts[1], v[2], counts[2]) for v in [a, b]]
        work = Work(extra, counts[0], stage)
        assert lib.j2p_static_scene_tape(c.byref(space), c.byref(owner), c.byref(seed), c.byref(work), c.byref(output), c.byref(header)) == 1
        actual = [[e.offset, e.opcode, e.flags, e.material, e.material_valid, e.submission] for e in b[1][:header.events]]
        assert actual == fixture['expectedEvents']
        entry, final = Entry(owner), Entry()
        matrix_seed = MatrixSeed(model, 2)
        identity = [4096 if i % 5 == 0 else 0 for i in range(16)]
        for m in matrix_seed.matrices:
            m[:] = identity
        assert lib.j2p_matrix_init(c.byref(model), c.byref(matrix_seed), c.byref(entry.state)) == 1
        count = max(header.shape_references, 1)
        temporary, result = (Snapshot * count)(), (Snapshot * count)()
        assert lib.j2p_static_scene_snapshots(c.byref(owner), c.byref(header), b[0], b[1], c.byref(entry), temporary, count, result, count, c.byref(final)) == 1
        for observation, expected in zip(result[:header.shape_references], fixture['expectedMatrices']):
            assert observation.mode == 2 and observation.valid_slots == expected['valid_slots']
            assert [list(m) for m in observation.matrices] == expected['matrices']
        preserved = bytes(header) + bytes(extra) + b''.join(bytes(v) for v in a + b)
        seed.provider_flags = 1
        assert lib.j2p_static_scene_tape(c.byref(space), c.byref(owner), c.byref(seed), c.byref(work), c.byref(output), c.byref(header)) == -2
        assert preserved == bytes(header) + bytes(extra) + b''.join(bytes(v) for v in a + b)
        assert bytes(raw) == b'\xa5' + data + b'\xa5'
        references += header.shape_references
        submissions += header.submissions
    print(json.dumps(dict(status='independent-source-only-native-event-and-snapshot-replay-passed', syntheticModels=8,
        shapeReferences=references, submissions=submissions, originalAssetsOrOraclePackages=False, productionVertices=False, rendering=False)))


if __name__ == '__main__':
    main()
