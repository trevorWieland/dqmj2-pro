#include "static_scene_internal_20261107.h"

_Static_assert(sizeof(J2pSceneSnapshot) == 364, "Owned SHP observation layout");

typedef struct { const void *pointer; uint32_t bytes; } ReplayRange;

static int framing(const J2pSceneTape *tape, const J2pSceneOwner *owner) {
    J2pSceneOwner identity = *owner;
    uint64_t model_end = (uint64_t)tape->plan.model_address + tape->plan.model_size;
    identity.model = tape->plan.owner;
    return j2p_scene_owner_equal(owner, &identity) && tape->plan.model_bytes == owner->model_bytes &&
        (uint64_t)owner->model.model_set + owner->model_bytes <= UINT64_C(0x100000000) &&
        tape->plan.model_address >= owner->model.model_set && tape->plan.model_size &&
        model_end <= (uint64_t)owner->model.model_set + owner->model_bytes && tape->plan.sbc_bytes &&
        tape->plan.sbc_address >= tape->plan.model_address && (uint64_t)tape->plan.sbc_address + tape->plan.sbc_bytes <= model_end;
}

static int event_profile(const J2pSceneEvent *e) {
    switch (e->opcode) {
    case 6: case 0x26: case 0x46: case 0x66: return e->matrix_count <= 6 && !e->shader_count && !e->material_evaluation;
    case 0x0b: case 0x2b: return e->matrix_count == 1 && !e->shader_count && !e->material_evaluation;
    case 4: case 0x24: case 0x44: return !e->matrix_count && (e->shader_count == 0 || e->shader_count == 5) && e->material_evaluation;
    case 1: case 2: case 5: return !e->matrix_count && !e->shader_count && !e->material_evaluation;
    default: return 0;
    }
}

static int ranges(const J2pSceneOwner *owner, const J2pSceneTape *tape, const J2pMatrixCommand *commands,
    const J2pSceneEvent *events, const J2pSceneEntry *entry, J2pSceneSnapshot *scratch, uint32_t scratch_capacity,
    J2pSceneSnapshot *output, uint32_t capacity, J2pSceneEntry *final_state) {
    ReplayRange reads[5] = {{owner, sizeof(*owner)}, {tape, sizeof(*tape)}, {commands, 0}, {events, 0}, {entry, sizeof(*entry)}};
    ReplayRange writes[3] = {{scratch, 0}, {output, 0}, {final_state, sizeof(*final_state)}};
    uint32_t i, j;
    if (scratch_capacity > UINT32_MAX / sizeof(*scratch) || capacity > UINT32_MAX / sizeof(*output) ||
        (!scratch != !scratch_capacity) || (!output != !capacity)) return 0;
    reads[2].bytes = tape->plan.command_count * (uint32_t)sizeof(*commands);
    reads[3].bytes = tape->events * (uint32_t)sizeof(*events);
    writes[0].bytes = scratch_capacity * (uint32_t)sizeof(*scratch);
    writes[1].bytes = capacity * (uint32_t)sizeof(*output);
    for (i = 0; i < 3; ++i) {
        for (j = 0; j < 5; ++j)
            if (j2p_scene_overlap(writes[i].pointer, writes[i].bytes, reads[j].pointer, reads[j].bytes)) return 0;
        for (j = 0; j < i; ++j)
            if (j2p_scene_overlap(writes[i].pointer, writes[i].bytes, writes[j].pointer, writes[j].bytes)) return 0;
    }
    return 1;
}

static int step(const J2pSceneOwner *owner, const J2pSceneTape *tape, const J2pMatrixCommand *commands,
    const J2pSceneEvent *events, const J2pSceneEntry *entry, J2pSceneSnapshot *snapshots, J2pSceneEntry *final_state) {
    J2pSceneEntry state = *entry;
    uint32_t i, matrix = 0, shader = 0, offset = 0, reference = 0, submission = 0;
    int status = j2p_matrix_apply(&owner->model, &state.state, 0, 0);
    if (status != 1 || state.state.mode != 2) return -1;
    for (i = 0; i < tape->events; ++i) {
        const J2pSceneEvent *e = &events[i];
        if (e->ordinal != i || e->offset != offset || e->matrix_begin != matrix || e->shader_begin != shader ||
            !e->length || e->length != j2p_node_pose_command_length(e->opcode) || e->length > tape->plan.sbc_bytes - offset ||
            e->matrix_count > tape->plan.command_count - matrix || e->shader_count > tape->shaders - shader) return -1;
        if (!event_profile(e) || (e->flags & ~63U) || e->material_valid > 1 || e->material_evaluation > 4 ||
            e->material_valid != !!(e->flags & 8)) return -2;
        if ((e->flags & 4) && e->node >= tape->nodes) return -1;
        if ((e->flags & 16) && e->description >= tape->nodes) return -1;
        if (e->material_valid && e->material >= tape->materials) return -1;
        if (e->opcode == 5) {
            J2pSceneSnapshot value = {0};
            uint32_t r, c, decision = !(e->flags & 1) ? 2 : e->flags & 2 ? 3 : 1;
            if (e->matrix_count || e->shader_count || e->shape_reference != reference || e->shape_index >= tape->shapes ||
                e->submission != decision || e->display_bytes < 4 || e->display_bytes & 3 ||
                e->shape_address < tape->plan.model_address || e->display_address < e->shape_address ||
                (uint64_t)e->display_address + e->display_bytes > (uint64_t)tape->plan.model_address + tape->plan.model_size) return -1;
            if (e->submission == 1) {
                if (e->submission_ordinal != submission++) return -1;
            } else if (e->submission_ordinal != UINT32_MAX) return -1;
            value.owner = *owner;
            value.sbc_address = tape->plan.sbc_address; value.offset = e->offset; value.event_ordinal = i;
            value.shape_index = e->shape_index; value.shape_address = e->shape_address;
            value.display_address = e->display_address; value.display_bytes = e->display_bytes;
            value.reference_ordinal = reference; value.submission_ordinal = e->submission_ordinal; value.submission = e->submission;
            value.material = e->material; value.material_valid = e->material_valid; value.matrix_prefix = matrix;
            value.mode = state.state.mode; value.valid_slots = state.state.valid_slots;
            for (r = 0; r < 4; ++r) for (c = 0; c < 16; ++c) value.matrices[r][c] = state.state.matrices[r][c];
            if (snapshots) snapshots[reference] = value;
            ++reference;
        } else if (e->submission || e->shape_reference != UINT32_MAX) return -1;
        if (e->matrix_count) {
            uint32_t k;
            for (k = 0; k < e->matrix_count; ++k) {
                const J2pMatrixCommand *c = commands + matrix + k;
                if (!((c->opcode == 0x13 || c->opcode == 0x14) && c->count == 1) &&
                    !(c->opcode == 0x19 && c->count == 12) && !(c->opcode == 0x1a && c->count == 9) &&
                    !((c->opcode == 0x1b || c->opcode == 0x1c) && c->count == 3)) return -2;
            }
            status = j2p_matrix_apply(&owner->model, &state.state, commands + matrix, e->matrix_count);
            if (status != 1) return status;
        }
        matrix += e->matrix_count;
        shader += e->shader_count;
        offset += e->length;
        if (e->opcode == 1 && i + 1 != tape->events) return -1;
    }
    if (!tape->events || events[tape->events - 1].opcode != 1 || matrix != tape->plan.command_count || shader != tape->shaders ||
        reference != tape->shape_references || submission != tape->submissions || offset > tape->plan.sbc_bytes || tape->plan.sbc_bytes - offset > 3) return -1;
    *final_state = state;
    return 1;
}

int j2p_static_scene_snapshots(const J2pSceneOwner *owner, const J2pSceneTape *tape, const J2pMatrixCommand *commands,
    const J2pSceneEvent *events, const J2pSceneEntry *entry, J2pSceneSnapshot *scratch, uint32_t scratch_capacity,
    J2pSceneSnapshot *output, uint32_t capacity, J2pSceneEntry *final_state) {
    J2pSceneEntry result;
    uint32_t i;
    int status;
    if (!j2p_scene_owner_valid(owner) || !tape || !entry || !final_state || tape->version != 1 ||
        !j2p_scene_owner_equal(owner, &tape->seed.owner) || !j2p_scene_owner_equal(owner, &entry->owner) ||
        tape->plan.command_count > 10000 || tape->events > UINT32_MAX / sizeof(J2pSceneEvent) ||
        tape->shaders > UINT32_MAX / sizeof(J2pSceneShader) || (!commands && tape->plan.command_count) || !events ||
        !tape->nodes || tape->nodes > 64 || tape->materials > 64 || tape->shapes > 255 || tape->plan.required_mode != 2 ||
        !framing(tape, owner)) return -1;
    if (tape->seed.provider_flags || tape->seed.shader_valid != 31) return -2;
    if (!ranges(owner, tape, commands, events, entry, scratch, scratch_capacity, output, capacity, final_state)) return -1;
    if (scratch_capacity < tape->shape_references || capacity < tape->shape_references) return -5;
    status = step(owner, tape, commands, events, entry, 0, &result);
    if (status != 1) return status;
    status = step(owner, tape, commands, events, entry, scratch, &result);
    if (status != 1) return status;
    for (i = 0; i < tape->shape_references; ++i) output[i] = scratch[i];
    *final_state = result;
    return 1;
}
