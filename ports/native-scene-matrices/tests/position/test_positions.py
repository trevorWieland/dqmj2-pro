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

scene = types.SimpleNamespace(Owner=Owner, Seed=Seed, Tape=Tape, Event=Event, Snapshot=Snapshot, Entry=Entry, Buffers=Buffers, Work=Work)

class Owner(c.Structure):
    _fields_ = [('scene', scene.Owner)] + [(name, c.c_uint32) for name in ['stream_id', 'seed_id', 'coordinate_generation']]

class Seed(c.Structure):
    _fields_ = [('owner', Owner), ('known_axes', c.c_uint32), ('xyz', c.c_int32 * 3)]

class Record(c.Structure):
    _fields_ = [('owner', Owner)] + [(name, c.c_uint32) for name in ['sbc_address', 'sbc_offset', 'event_ordinal', 'reference_ordinal',
        'submission_ordinal', 'shape_index', 'shape_address', 'display_address', 'display_bytes', 'header_offset', 'opcode_slot',
        'parameter_offset', 'opcode', 'vertex_ordinal', 'submission_vertex_ordinal']] + [('xyz', c.c_int32 * 3), ('position', c.c_int32 * 4)]

class Header(c.Structure):
    _fields_ = [('owner', Owner)] + [(name, c.c_uint32) for name in ['version', 'records', 'submitted_lists']]

class Buffer(c.Structure):
    _fields_ = [('records', c.POINTER(Record)), ('capacity', c.c_uint32)]

def main():
    root = Path(__file__).resolve().parent
    lib = c.CDLL(str(Path(sys.argv[1]).resolve()))
    lib.j2p_guest_map.argtypes = [c.POINTER(Space), Scope, c.c_uint32, c.c_void_p, c.c_uint32]
    lib.j2p_matrix_init.argtypes = [c.POINTER(MatrixOwner), c.POINTER(MatrixSeed), c.POINTER(State)]
    lib.j2p_static_scene_tape.argtypes = [c.POINTER(Space), c.POINTER(scene.Owner), c.POINTER(scene.Seed), c.POINTER(scene.Work), c.POINTER(scene.Buffers), c.POINTER(scene.Tape)]
    lib.j2p_static_scene_snapshots.argtypes = [c.POINTER(scene.Owner), c.POINTER(scene.Tape), c.POINTER(Command), c.POINTER(scene.Event),
        c.POINTER(scene.Entry), c.POINTER(scene.Snapshot), c.c_uint32, c.POINTER(scene.Snapshot), c.c_uint32, c.POINTER(scene.Entry)]
    lib.j2p_stream_positions.argtypes = [c.POINTER(Space), c.POINTER(scene.Owner), c.POINTER(Seed), c.POINTER(scene.Tape),
        c.POINTER(scene.Event), c.POINTER(scene.Snapshot), c.c_uint32, c.POINTER(Buffer), c.POINTER(Buffer), c.POINTER(Header), c.POINTER(Seed)]
    total = 0
    for fixture in json.loads((root / 'copied-position-fixtures.json').read_text()):
        data = bytes(fixture['source'])
        raw = (c.c_uint8 * (len(data) + 2)).from_buffer_copy(b'\xa5' + data + b'\xa5')
        space, model = Space(), MatrixOwner(Scope(0, 9, 1, 1), 0x02700000, 0)
        assert lib.j2p_guest_map(c.byref(space), model.scope, model.model_set, c.addressof(raw) + 1, len(data)) == 1
        owner, tape = scene.Owner(model, len(data), 1, 2, 3, 4, 5), scene.Tape()
        material = scene.Seed(owner, 0, 31)
        material.material_defaults[:] = [0, 0, 0x1f00c0]
        material.initial_shader[:] = [0x1234, 0x5678, 0x1f00c0, 0, 0]
        assert lib.j2p_static_scene_tape(c.byref(space), c.byref(owner), c.byref(material), None, None, c.byref(tape)) == 1
        counts = [max(tape.plan.command_count, 1), max(tape.events, 1), max(tape.shaders, 1)]
        a = [(t * n)() for t, n in zip([Command, scene.Event, Shader], counts)]
        b = [(t * n)() for t, n in zip([Command, scene.Event, Shader], counts)]
        extra = (Command * counts[0])()
        staging, output = [scene.Buffers(v[0], counts[0], v[1], counts[1], v[2], counts[2]) for v in [a, b]]
        work = scene.Work(extra, counts[0], staging)
        assert lib.j2p_static_scene_tape(c.byref(space), c.byref(owner), c.byref(material), c.byref(work), c.byref(output), c.byref(tape)) == 1
        entry, final_matrix = scene.Entry(owner), scene.Entry()
        matrix_seed = MatrixSeed(model, 2)
        for m in matrix_seed.matrices:
            m[:] = [4096 if i % 5 == 0 else 0 for i in range(16)]
        assert lib.j2p_matrix_init(c.byref(model), c.byref(matrix_seed), c.byref(entry.state)) == 1
        n = max(tape.shape_references, 1)
        temp, snapshots = (scene.Snapshot * n)(), (scene.Snapshot * n)()
        assert lib.j2p_static_scene_snapshots(c.byref(owner), c.byref(tape), b[0], b[1], c.byref(entry), temp, n, snapshots, n, c.byref(final_matrix)) == 1
        initial = Seed(Owner(owner, 17, 23, 29), fixture['known'], (c.c_int32 * 3)(*fixture['xyz']))
        header = Header()
        args = [c.byref(space), c.byref(owner), c.byref(initial), c.byref(tape), b[1], snapshots, tape.shape_references]
        assert lib.j2p_stream_positions(*args, None, None, c.byref(header), None) == 1
        n = max(header.records, 1)
        temp_records, records, final = (Record * n)(), (Record * n)(), Seed()
        staging, output = Buffer(temp_records, n), Buffer(records, n)
        assert lib.j2p_stream_positions(*args, c.byref(staging), c.byref(output), c.byref(header), c.byref(final)) == 1
        assert header.records == len(fixture['expected'])
        for ordinal, (r, e) in enumerate(zip(records[:header.records], fixture['expected'])):
            assert list(r.xyz) == e['xyz'] and list(r.position) == e['position']
            assert [r.event_ordinal, r.reference_ordinal, r.submission_ordinal, r.header_offset, r.opcode_slot, r.parameter_offset,
                r.opcode, r.vertex_ordinal, r.submission_vertex_ordinal] == [e['event'], e['reference'], e['submission'], e['header'], e['slot'], e['parameter'], e['opcode'], ordinal, e['local']]
        assert list(final.xyz) == fixture['finalXYZ'] and final.known_axes == fixture['finalKnown']
        before = bytes(records) + bytes(temp_records) + bytes(final) + bytes(header)
        tape.seed.provider_flags = 1
        assert lib.j2p_stream_positions(*args, c.byref(staging), c.byref(output), c.byref(header), c.byref(final)) == -2
        assert before == bytes(records) + bytes(temp_records) + bytes(final) + bytes(header)
        assert bytes(raw) == b'\xa5' + data + b'\xa5'
        total += header.records
    print(json.dumps(dict(status='copied-source-native-position-pipeline-pass', syntheticModels=8, positionRecords=total,
        originalAssetsOrOraclePackages=False, colorLightingUVPolygons=False, rendering=False, deviceExecuted=False)))


if __name__ == '__main__':
    main()
