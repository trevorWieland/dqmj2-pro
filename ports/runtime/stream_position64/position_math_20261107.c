#include "position_internal_20261107.h"

uint32_t j2p_position_word(const uint8_t *p) {
    return p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}

int j2p_position_same(const J2pSceneOwner *a, const J2pSceneOwner *b) {
    return a->model.scope.program == b->model.scope.program && a->model.scope.processor == b->model.scope.processor &&
        a->model.scope.module == b->model.scope.module && a->model.scope.generation == b->model.scope.generation &&
        a->model.model_set == b->model.model_set && a->model.model_index == b->model.model_index && a->model_bytes == b->model_bytes &&
        a->instance_id == b->instance_id && a->run_generation == b->run_generation && a->matrix_generation == b->matrix_generation &&
        a->material_generation == b->material_generation && a->attribute_generation == b->attribute_generation;
}

int j2p_position_overlap(const void *p, uint32_t n, const void *q, uint32_t m) {
    uintptr_t a = (uintptr_t)p, b = (uintptr_t)q;
    return n > UINTPTR_MAX - a || m > UINTPTR_MAX - b || (n && m && a < b + m && b < a + n);
}

static int dot(const int32_t *a, const int32_t *b, uint32_t stride, int32_t *out) {
    int64_t total = 0, value;
    uint64_t magnitude = 0;
    uint32_t k;
    for (k = 0; k < 4; ++k) {
        int64_t product = (int64_t)a[k] * b[k * stride];
        uint64_t absolute = (uint64_t)(product < 0 ? -product : product);
        if (absolute > (uint64_t)INT64_MAX - magnitude) return -4;
        magnitude += absolute;
        total += product;
    }
    value = total / 4096;
    if (total < 0 && total % 4096) --value;
    if (value < INT32_MIN || value > INT32_MAX) return -4;
    *out = (int32_t)value;
    return 1;
}

int j2p_position_clip(const J2pSceneSnapshot *s, int32_t *out) {
    uint32_t r, c;
    for (r = 0; r < 4; ++r) for (c = 0; c < 4; ++c)
        if (dot(s->matrices[1] + r * 4, s->matrices[0] + c, 4, out + r * 4 + c) != 1) return -4;
    return 1;
}

int j2p_position_vertex(const int32_t *xyz, const int32_t *clip, int32_t *out) {
    int32_t v[4] = {xyz[0], xyz[1], xyz[2], 4096};
    uint32_t c;
    for (c = 0; c < 4; ++c) if (dot(v, clip + c, 4, out + c) != 1) return -4;
    return 1;
}
