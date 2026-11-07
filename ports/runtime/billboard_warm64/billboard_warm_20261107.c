#include "billboard_warm_internal_20261107.h"

_Static_assert(sizeof(J2pBb7Owner) == 60 && sizeof(J2pBb7WarmContext) == 176 &&
    sizeof(J2pBb7State) == 4540 && sizeof(J2pBb7Effect) == 732, "Owned fixed-width BB7 layout");

typedef struct { const void *pointer; uint32_t bytes, alignment; } ObjectRange;

static int equal(const J2pBb7Owner *a, const J2pBb7Owner *b) {
    return a->model.scope.program == b->model.scope.program && a->model.scope.processor == b->model.scope.processor &&
        a->model.scope.module == b->model.scope.module && a->model.scope.generation == b->model.scope.generation &&
        a->model.model_set == b->model.model_set && a->model.model_index == b->model.model_index &&
        a->instance_id == b->instance_id && a->run_generation == b->run_generation &&
        a->matrix_generation == b->matrix_generation && a->camera_id == b->camera_id &&
        a->camera_generation == b->camera_generation && a->base_generation == b->base_generation &&
        a->cache_generation == b->cache_generation && a->projection_generation == b->projection_generation &&
        a->queue_generation == b->queue_generation;
}

static int valid(const J2pBb7Owner *p, uint32_t branch) {
    return p->model.scope.program == 0 && p->model.scope.processor == 9 && p->model.scope.module == 1 &&
        p->model.scope.generation && p->model.model_set && p->instance_id && p->run_generation &&
        p->matrix_generation && p->projection_generation && p->queue_generation &&
        (!branch || (p->camera_id && p->camera_generation && p->cache_generation)) &&
        (branch != 2 || p->base_generation);
}

static int ranges(const J2pBb7Owner *owner, const J2pBb7WarmContext *warm, const J2pBb7State *entry,
    J2pBb7State *output, J2pBb7Effect *effect) {
    ObjectRange objects[5] = {{owner, sizeof(*owner), _Alignof(J2pBb7Owner)},
        {warm, sizeof(*warm), _Alignof(J2pBb7WarmContext)}, {entry, sizeof(*entry), _Alignof(J2pBb7State)},
        {output, sizeof(*output), _Alignof(J2pBb7State)}, {effect, sizeof(*effect), _Alignof(J2pBb7Effect)}};
    uint32_t i, j;
    for (i = 0; i < 5; ++i) {
        uintptr_t address = (uintptr_t)objects[i].pointer;
        if (!address || address % objects[i].alignment || objects[i].bytes > UINTPTR_MAX - address) return 0;
    }
    for (i = 3; i < 5; ++i) for (j = 0; j < i; ++j) {
        uintptr_t a = (uintptr_t)objects[i].pointer, b = (uintptr_t)objects[j].pointer;
        if (a < b + objects[j].bytes && b < a + objects[i].bytes) return 0;
    }
    return 1;
}

int j2p_billboard_warm(const J2pBb7Owner *owner, const J2pBb7WarmContext *warm, const J2pBb7State *entry,
    J2pBb7State *output, J2pBb7Effect *effect) {
    J2pBb7State next;
    J2pBb7Effect result = {0};
    uint32_t branch, mask, i;
    int status;
    if (!ranges(owner, warm, entry, output, effect)) return -1;
    if (warm->raw_flush_bits > 3) return -1;
    branch = warm->raw_flush_bits & 1 ? 2 : warm->raw_flush_bits & 2 ? 1 : 0;
    mask = branch == 2 ? 0x80 : branch == 1 ? 8 : 0;
    if (warm->branch != branch || !valid(owner, branch) || !equal(owner, &warm->owner) ||
        !equal(owner, &entry->owner) || entry->projection_saved_valid > 1) return -1;
    if (warm->provider_flags || warm->cache_valid_mask & ~UINT32_C(0x88) ||
        (branch ? warm->selected_state != 2 || !(warm->cache_valid_mask & mask) : warm->selected_state != 0) ||
        entry->matrix.mode != 2 || entry->projection_depth || entry->projection_error_known != 1 ||
        entry->projection_error || entry->queue_complete != 1 || entry->queued_commands ||
        entry->async_known != 1 || entry->async_active) return -2;
    next = *entry;
    status = j2p_matrix_apply(&owner->model, &next.matrix, 0, 0);
    if (status != 1) return status;
    result.owner = *owner;
    result.raw_flush_bits = warm->raw_flush_bits;
    result.branch = branch;
    result.cache_valid_mask = warm->cache_valid_mask;
    status = j2p_bb7_calculate(warm, &next, &result);
    if (status != 1) return status;
    for (i = 0; i < 16; ++i) {
        next.projection_saved[i] = entry->matrix.matrices[0][i];
        result.saved_projection[i] = entry->matrix.matrices[0][i];
    }
    next.projection_saved_valid = result.projection_slot_written = 1;
    *output = next;
    *effect = result;
    return 1;
}
