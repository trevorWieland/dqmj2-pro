#include "static_scene_internal_20261107.h"

_Static_assert(sizeof(J2pSceneOwner) == 48 && sizeof(J2pSceneSeed) == 88, "Owned event identities");
_Static_assert(sizeof(J2pSceneEvent) == 136 && sizeof(J2pSceneTape) == 172, "Owned tape records");

typedef struct { const void *pointer; uint32_t bytes; } Range;

static int buffer_ranges(const J2pSceneBuffers *b, Range *r) {
    if ((!b->commands != !b->command_capacity) || (!b->events != !b->event_capacity) || (!b->shaders != !b->shader_capacity) ||
        b->command_capacity > 10000 || b->event_capacity > UINT32_MAX / sizeof(J2pSceneEvent) ||
        b->shader_capacity > UINT32_MAX / sizeof(J2pSceneShader)) return 0;
    r[0].pointer = b->commands; r[0].bytes = b->command_capacity * (uint32_t)sizeof(J2pMatrixCommand);
    r[1].pointer = b->events; r[1].bytes = b->event_capacity * (uint32_t)sizeof(J2pSceneEvent);
    r[2].pointer = b->shaders; r[2].bytes = b->shader_capacity * (uint32_t)sizeof(J2pSceneShader);
    return 1;
}

static int output_ranges(J2pGuestSpace *space, const J2pSceneOwner *owner, const J2pSceneSeed *seed,
    J2pSceneWork *work, J2pSceneBuffers *output, J2pSceneTape *header) {
    Range writes[8] = {{header, sizeof(*header)}};
    Range reads[5] = {{space, sizeof(*space)}, {owner, sizeof(*owner)}, {seed, sizeof(*seed)}, {work, work ? sizeof(*work) : 0},
        {output, output ? sizeof(*output) : 0}};
    uint32_t n = 1, i, j;
    if (work) {
        if ((!work->plan_scratch != !work->plan_capacity) || work->plan_capacity > 10000 ||
            !buffer_ranges(&work->stage, writes + 1) || !buffer_ranges(output, writes + 4)) return 0;
        writes[7].pointer = work->plan_scratch;
        writes[7].bytes = work->plan_capacity * (uint32_t)sizeof(J2pMatrixCommand);
        n = 8;
    }
    for (i = 0; i < n; ++i) {
        for (j = 0; j < 5; ++j)
            if (j2p_scene_overlap(writes[i].pointer, writes[i].bytes, reads[j].pointer, reads[j].bytes)) return 0;
        for (j = 0; j < i; ++j)
            if (j2p_scene_overlap(writes[i].pointer, writes[i].bytes, writes[j].pointer, writes[j].bytes)) return 0;
        for (j = 0; j < space->count; ++j)
            if (!space->regions[j].bytes || !space->regions[j].length ||
                j2p_scene_overlap(writes[i].pointer, writes[i].bytes, space->regions[j].bytes, space->regions[j].length)) return 0;
    }
    return 1;
}

static int traverse(J2pGuestSpace *space, const J2pSceneSeed *seed, J2pSceneTape *tape, J2pSceneBuffers *output) {
    J2pSceneWalk value = {0};
    int status;
    value.space = space;
    value.seed = seed;
    value.tape = tape;
    value.output = output;
    value.model = j2p_guest_resolve(space, seed->owner.model.scope, tape->plan.model_address, tape->plan.model_size, 1);
    value.script = j2p_guest_resolve(space, seed->owner.model.scope, tape->plan.sbc_address, tape->plan.sbc_bytes, 1);
    if (!value.model || !value.script) return -1;
    status = j2p_node_pose_init(space, seed->owner.model.scope, seed->owner.model.model_set, seed->owner.model_bytes,
        seed->owner.model.model_index, &value.nodes);
    if (status != 1) return status == 0 ? -1 : status;
    tape->nodes = value.nodes.node_count;
    tape->materials = value.model[24];
    tape->shapes = value.model[25];
    status = j2p_scene_walk(&value);
    if (status != 1) return status;
    tape->events = value.event_count;
    tape->shaders = value.shader_count;
    tape->shape_references = value.reference_count;
    tape->submissions = value.submission_count;
    return 1;
}

int j2p_static_scene_tape(J2pGuestSpace *space, const J2pSceneOwner *owner, const J2pSceneSeed *seed,
    J2pSceneWork *work, J2pSceneBuffers *output, J2pSceneTape *header) {
    J2pSceneTape value = {0};
    uint32_t i, events, shaders, references, submissions;
    int status;
    if (!space || space->count > 16 || !j2p_scene_owner_valid(owner) || !seed || !header || (!work != !output)) return -1;
    if (!j2p_scene_owner_equal(owner, &seed->owner)) return -1;
    if (seed->provider_flags || seed->shader_valid != 31) return -2;
    if (!output_ranges(space, owner, seed, work, output, header)) return -1;
    value.seed = *seed;
    value.version = 1;
    status = j2p_static_matrix_plan(space, &owner->model, owner->model_bytes, 0, 0, 0, 0, &value.plan);
    if (status != 1) return status;
    status = traverse(space, seed, &value, 0);
    if (status != 1) return status;
    if (work) {
        if (work->plan_capacity < value.plan.command_count || work->stage.command_capacity < value.plan.command_count ||
            output->command_capacity < value.plan.command_count || work->stage.event_capacity < value.events || output->event_capacity < value.events ||
            work->stage.shader_capacity < value.shaders || output->shader_capacity < value.shaders) return -5;
        if (!!work->plan_capacity != !!work->stage.command_capacity) return -1;
        status = j2p_static_matrix_plan(space, &owner->model, owner->model_bytes, work->plan_scratch, work->plan_capacity,
            work->stage.commands, work->stage.command_capacity, &value.plan);
        if (status != 1) return status;
        events = value.events; shaders = value.shaders; references = value.shape_references; submissions = value.submissions;
        status = traverse(space, seed, &value, &work->stage);
        if (status != 1 || value.events != events || value.shaders != shaders || value.shape_references != references || value.submissions != submissions) return -1;
        for (i = 0; i < value.plan.command_count; ++i) output->commands[i] = work->stage.commands[i];
        for (i = 0; i < value.events; ++i) output->events[i] = work->stage.events[i];
        for (i = 0; i < value.shaders; ++i) output->shaders[i] = work->stage.shaders[i];
    }
    *header = value;
    return 1;
}
