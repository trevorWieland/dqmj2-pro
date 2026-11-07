#include "static_matrix_internal_20261107.h"

_Static_assert(sizeof(J2pStaticMatrixPlan) == 52, "Owned static matrix plan header layout");

static int overlap(const void *first, uint32_t first_bytes, const void *second, uint32_t second_bytes) {
    uintptr_t a = (uintptr_t)first, b = (uintptr_t)second;
    return first_bytes > UINTPTR_MAX - a || second_bytes > UINTPTR_MAX - b ||
        (first_bytes && second_bytes && a < b + second_bytes && b < a + first_bytes);
}

static int clear_of_inputs(J2pGuestSpace *space, const J2pMatrixOwner *owner, const void *output, uint32_t bytes) {
    uint32_t i;
    if (overlap(output, bytes, space, sizeof(*space)) || overlap(output, bytes, owner, sizeof(*owner))) return 0;
    for (i = 0; i < space->count; ++i)
        if (!space->regions[i].bytes || !space->regions[i].length ||
            overlap(output, bytes, space->regions[i].bytes, space->regions[i].length)) return 0;
    return 1;
}

int j2p_static_matrix_plan(J2pGuestSpace *space, const J2pMatrixOwner *owner, uint32_t model_bytes,
    J2pMatrixCommand *scratch, uint32_t scratch_capacity, J2pMatrixCommand *output, uint32_t capacity, J2pStaticMatrixPlan *header) {
    J2pStaticMatrixWalk walk = {0}, start;
    J2pStaticMatrixPlan result = {0};
    uint32_t i, count, output_bytes, scratch_bytes;
    int status;
    if (!space || space->count > 16 || !owner || !header || owner->scope.program || owner->scope.processor != 9 ||
        owner->scope.module != 1 || !owner->scope.generation || !owner->model_set || capacity > 10000 || scratch_capacity > 10000 ||
        (!output != !capacity) || (!scratch != !scratch_capacity) || (!output && scratch) || (output && !scratch)) return -1;
    output_bytes = capacity * (uint32_t)sizeof(*output);
    scratch_bytes = scratch_capacity * (uint32_t)sizeof(*scratch);
    if (!clear_of_inputs(space, owner, header, sizeof(*header)) ||
        (output && (!clear_of_inputs(space, owner, output, output_bytes) || !clear_of_inputs(space, owner, scratch, scratch_bytes) ||
        overlap(output, output_bytes, scratch, scratch_bytes) || overlap(output, output_bytes, header, sizeof(*header)) ||
        overlap(scratch, scratch_bytes, header, sizeof(*header))))) return -1;
    walk.space = space;
    walk.owner = *owner;
    status = j2p_node_pose_init(space, owner->scope, owner->model_set, model_bytes, owner->model_index, &walk.nodes);
    if (status != 1) return status == 0 ? -1 : status;
    walk.model = j2p_guest_resolve(space, owner->scope, walk.nodes.model_address, walk.nodes.model_size, 1);
    walk.script = j2p_guest_resolve(space, owner->scope, walk.nodes.sbc_address, walk.nodes.sbc_bytes, 1);
    if (!walk.model || !walk.script) return -1;
    start = walk;
    status = j2p_static_walk(&walk);
    if (status != 1) return status;
    count = walk.written;
    if (output) {
        if (capacity < count || scratch_capacity < count) return -5;
        walk = start;
        walk.commands = scratch;
        status = j2p_static_walk(&walk);
        if (status != 1 || walk.written != count) return -1;
        for (i = 0; i < count; ++i) output[i] = scratch[i];
    }
    result.owner = *owner;
    result.model_bytes = model_bytes;
    result.model_address = start.nodes.model_address;
    result.model_size = start.nodes.model_size;
    result.sbc_address = start.nodes.sbc_address;
    result.sbc_bytes = start.nodes.sbc_bytes;
    result.required_mode = 2;
    result.command_count = count;
    *header = result;
    return 1;
}
