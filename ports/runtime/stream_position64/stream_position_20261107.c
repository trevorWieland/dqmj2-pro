#include "position_internal_20261107.h"

_Static_assert(sizeof(J2pPositionOwner) == 60 && sizeof(J2pPositionSeed) == 76, "Position seed identity");
_Static_assert(sizeof(J2pPositionRecord) == 148 && sizeof(J2pPositionHeader) == 72, "Position owned records");
typedef struct { const void *pointer; uint32_t bytes; } Range;

static int ranges(J2pPositionWalk *w, const J2pPositionSeed *seed, const J2pPositionBuffer *stage,
    const J2pPositionBuffer *output, J2pPositionHeader *header, J2pPositionSeed *final) {
    Range reads[8] = {{w->space, sizeof(*w->space)}, {w->owner, sizeof(*w->owner)}, {seed, sizeof(*seed)}, {w->tape, sizeof(*w->tape)},
        {w->events, w->tape->events * (uint32_t)sizeof(*w->events)},
        {w->snapshots, w->tape->shape_references * (uint32_t)sizeof(*w->snapshots)},
        {stage, stage ? sizeof(*stage) : 0}, {output, output ? sizeof(*output) : 0}};
    Range writes[4] = {{header, sizeof(*header)}, {final, final ? sizeof(*final) : 0}, {0, 0}, {0, 0}};
    uint32_t i, j;
    if (stage) {
        if (stage->capacity > UINT32_MAX / sizeof(J2pPositionRecord) || output->capacity > UINT32_MAX / sizeof(J2pPositionRecord) ||
            (!stage->records != !stage->capacity) || (!output->records != !output->capacity)) return 0;
        writes[2].pointer = stage->records; writes[2].bytes = stage->capacity * (uint32_t)sizeof(J2pPositionRecord);
        writes[3].pointer = output->records; writes[3].bytes = output->capacity * (uint32_t)sizeof(J2pPositionRecord);
    }
    for (i = 0; i < 4; ++i) {
        for (j = 0; j < 8; ++j) if (j2p_position_overlap(writes[i].pointer, writes[i].bytes, reads[j].pointer, reads[j].bytes)) return 0;
        for (j = 0; j < i; ++j) if (j2p_position_overlap(writes[i].pointer, writes[i].bytes, writes[j].pointer, writes[j].bytes)) return 0;
        for (j = 0; j < w->space->count; ++j)
            if (!w->space->regions[j].bytes || !w->space->regions[j].length ||
                j2p_position_overlap(writes[i].pointer, writes[i].bytes, w->space->regions[j].bytes, w->space->regions[j].length)) return 0;
    }
    return 1;
}

int j2p_stream_positions(J2pGuestSpace *space, const J2pSceneOwner *owner, const J2pPositionSeed *seed, const J2pSceneTape *tape,
    const J2pSceneEvent *events, const J2pSceneSnapshot *snapshots, uint32_t snapshot_count, const J2pPositionBuffer *stage,
    const J2pPositionBuffer *output, J2pPositionHeader *header, J2pPositionSeed *final) {
    J2pPositionWalk walk = {0}, start;
    J2pPositionHeader value = {0};
    J2pSceneOwner identity;
    uint64_t model_end;
    uint32_t i, count;
    int status;
    if (!space || space->count > 16 || !owner || !seed || !tape || !events || !header ||
        (!stage != !output) || (!!stage != !!final) || owner->model.scope.program || owner->model.scope.processor != 9 ||
        owner->model.scope.module != 1 || !owner->model.scope.generation || !owner->model.model_set || !owner->model_bytes ||
        !owner->instance_id || !owner->run_generation || !owner->matrix_generation || !owner->material_generation || !owner->attribute_generation ||
        !seed->owner.stream_id || !seed->owner.seed_id || !seed->owner.coordinate_generation || seed->known_axes > 7 ||
        !j2p_position_same(owner, &seed->owner.scene) || !j2p_position_same(owner, &tape->seed.owner) || tape->version != 1 ||
        tape->plan.required_mode != 2 || tape->plan.command_count > 10000 || tape->events > UINT32_MAX / sizeof(*events) ||
        !tape->nodes || tape->nodes > 64 || tape->materials > 64 || tape->shapes > 255 ||
        snapshot_count > UINT32_MAX / sizeof(*snapshots) || snapshot_count != tape->shape_references || (!snapshots && snapshot_count)) return -1;
    if (tape->seed.provider_flags || tape->seed.shader_valid != 31) return -2;
    identity = *owner; identity.model = tape->plan.owner;
    model_end = (uint64_t)tape->plan.model_address + tape->plan.model_size;
    if (!j2p_position_same(owner, &identity) || tape->plan.model_bytes != owner->model_bytes ||
        (uint64_t)owner->model.model_set + owner->model_bytes > UINT64_C(0x100000000) || !tape->plan.model_size ||
        tape->plan.model_address < owner->model.model_set || model_end > (uint64_t)owner->model.model_set + owner->model_bytes ||
        tape->plan.sbc_address < tape->plan.model_address || !tape->plan.sbc_bytes ||
        (uint64_t)tape->plan.sbc_address + tape->plan.sbc_bytes > model_end) return -1;
    for (i = 0; i < 3; ++i)
        if ((seed->known_axes & (1U << i)) ? (seed->xyz[i] < -32768 || seed->xyz[i] > 32767) : seed->xyz[i] != 0) return -1;
    walk.space = space; walk.owner = owner; walk.tape = tape; walk.events = events; walk.snapshots = snapshots; walk.state = *seed;
    if (!ranges(&walk, seed, stage, output, header, final)) return -1;
    if (!j2p_guest_resolve(space, owner->model.scope, owner->model.model_set, owner->model_bytes, 1) ||
        !j2p_guest_resolve(space, owner->model.scope, tape->plan.model_address, tape->plan.model_size, 1)) return -1;
    walk.script = j2p_guest_resolve(space, owner->model.scope, tape->plan.sbc_address, tape->plan.sbc_bytes, 1);
    if (!walk.script) return -1;
    start = walk;
    status = j2p_position_walk(&walk);
    if (status != 1) return status;
    count = walk.count;
    value.owner = seed->owner; value.version = 1; value.records = count; value.submitted_lists = walk.submitted;
    if (stage) {
        if (stage->capacity < count || output->capacity < count) return -5;
        walk = start; walk.output = stage->records;
        status = j2p_position_walk(&walk);
        if (status != 1 || walk.count != count) return -1;
        for (i = 0; i < count; ++i) output->records[i] = stage->records[i];
        *final = walk.state;
    }
    *header = value;
    return 1;
}
