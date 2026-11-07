#include "static_scene_internal_20261107.h"

uint32_t j2p_scene_half(const uint8_t *p) { return p[0] | ((uint32_t)p[1] << 8); }
uint32_t j2p_scene_word(const uint8_t *p) { return j2p_scene_half(p) | (j2p_scene_half(p + 2) << 16); }

int j2p_scene_owner_valid(const J2pSceneOwner *owner) {
    return owner && !owner->model.scope.program && owner->model.scope.processor == 9 && owner->model.scope.module == 1 &&
        owner->model.scope.generation && owner->model.model_set && owner->model_bytes && owner->instance_id && owner->run_generation &&
        owner->matrix_generation && owner->material_generation && owner->attribute_generation;
}

int j2p_scene_owner_equal(const J2pSceneOwner *a, const J2pSceneOwner *b) {
    return a->model.scope.program == b->model.scope.program && a->model.scope.processor == b->model.scope.processor &&
        a->model.scope.module == b->model.scope.module && a->model.scope.generation == b->model.scope.generation &&
        a->model.model_set == b->model.model_set && a->model.model_index == b->model.model_index && a->model_bytes == b->model_bytes &&
        a->instance_id == b->instance_id && a->run_generation == b->run_generation && a->matrix_generation == b->matrix_generation &&
        a->material_generation == b->material_generation && a->attribute_generation == b->attribute_generation;
}

int j2p_scene_overlap(const void *first, uint32_t first_bytes, const void *second, uint32_t second_bytes) {
    uintptr_t a = (uintptr_t)first, b = (uintptr_t)second;
    return first_bytes > UINTPTR_MAX - a || second_bytes > UINTPTR_MAX - b ||
        (first_bytes && second_bytes && a < b + second_bytes && b < a + first_bytes);
}

int j2p_scene_record(const uint8_t *p, uint32_t size, uint32_t base, uint32_t prefix,
    uint32_t count, uint32_t index, uint32_t *record) {
    uint32_t at, length, unit, names, offset, dictionary;
    if (index >= count || base > size || prefix > size - base) return -1;
    dictionary = base + prefix;
    if (size - dictionary < 8 || p[dictionary + 1] != count) return -1;
    length = j2p_scene_half(p + dictionary + 2);
    at = j2p_scene_half(p + dictionary + 6);
    if (length < 12 || length > size - dictionary || at < 8 + 4 * (count + 1) || at > length - 4) return -1;
    unit = j2p_scene_half(p + dictionary + at);
    names = j2p_scene_half(p + dictionary + at + 2);
    if (unit < 4 || names < 4 + unit * count || (uint64_t)at + names + count * 16 > length) return -1;
    offset = j2p_scene_word(p + dictionary + at + 4 + unit * index);
    if ((uint64_t)prefix + length > offset || offset > size - base || size - base - offset < 4) return -1;
    *record = base + offset;
    return 1;
}
