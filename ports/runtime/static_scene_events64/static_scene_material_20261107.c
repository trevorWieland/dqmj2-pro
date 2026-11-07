#include "static_scene_internal_20261107.h"

static uint32_t mask(uint32_t value) {
    return (value & 1 ? UINT32_C(0x7fff) : 0) | (value & 2 ? UINT32_C(0x7fff0000) : 0) | (value & 4 ? UINT32_C(0x8000) : 0);
}

int j2p_scene_material(J2pSceneWalk *walk, J2pSceneEvent *event, uint32_t index) {
    uint32_t record, option = event->opcode & 0xe0, i;
    const uint8_t *p = walk->model;
    if (!(walk->flags & 1) && (walk->flags & 8) && walk->material == index) {
        event->material_evaluation = 1;
        return 1;
    }
    if (index >= walk->tape->materials || index >= 64) return -1;
    if (j2p_scene_record(p, walk->tape->plan.model_size, j2p_scene_word(p + 8), 4, walk->tape->materials, index, &record) != 1) return -1;
    if (walk->tape->plan.model_size - record < 44) return -1;
    walk->material = index;
    walk->flags |= 8;
    if ((option == 32 || option == 64) && (walk->valid[index >> 5] & (1U << (index & 31)))) {
        walk->result = walk->cache[index];
        event->material_evaluation = 4;
    } else {
        uint32_t flags = j2p_scene_half(p + record + 30), m0 = mask((flags >> 6) & 7), m1 = mask((flags >> 9) & 7);
        uint32_t poly_mask = j2p_scene_word(p + record + 16);
        if (flags & 0xc001) return -2;
        if (option == 64) {
            walk->valid[index >> 5] |= 1U << (index & 31);
            walk->result = walk->cache[index];
            event->material_evaluation = 3;
        } else {
            walk->result = walk->temporary;
            event->material_evaluation = 2;
        }
        walk->result[0] = flags & 32 ? 32 : 0;
        walk->result[1] = (walk->seed->material_defaults[0] & ~m0) | (j2p_scene_word(p + record + 4) & m0);
        walk->result[2] = (walk->seed->material_defaults[1] & ~m1) | (j2p_scene_word(p + record + 8) & m1);
        walk->result[3] = (walk->seed->material_defaults[2] & ~poly_mask) | (j2p_scene_word(p + record + 12) & poly_mask);
        walk->result[4] = j2p_scene_word(p + record + 20);
        walk->result[5] = j2p_scene_half(p + record + 28);
    }
    if (!(walk->result[3] & 0x001f0000)) {
        walk->flags |= 2;
        return 1;
    }
    if (walk->result[0] & 32) walk->result[3] &= ~UINT32_C(0x001f0000);
    walk->flags &= ~2U;
    if (walk->shader_count > UINT32_MAX / sizeof(J2pSceneShader) - 5) return -5;
    for (i = 0; i < 5; ++i) {
        static const uint32_t opcodes[5] = {0x30, 0x31, 0x29, 0x2a, 0x2b};
        J2pSceneShader value = {opcodes[i], walk->result[i + 1]};
        if (walk->output) walk->output->shaders[walk->shader_count + i] = value;
        walk->shader[i] = value.parameter;
    }
    walk->shader_count += 5;
    event->shader_count = 5;
    return 1;
}
