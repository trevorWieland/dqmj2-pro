#include "assets_policy.h"

static uint32_t half(const uint8_t *p) { return p[0] | ((uint32_t)p[1] << 8); }
static uint32_t word(const uint8_t *p) { return half(p) | (half(p + 2) << 16); }

static int unambiguous(const uint8_t *p, uint32_t model_index, uint32_t material_index) {
    uint32_t entry = 8 + half(p + 14), model, mat, lane;
    model = word(p + entry + 4 + model_index * half(p + entry));
    mat = model + word(p + model + 8);
    for (lane = 0; lane != 2; ++lane) {
        uint32_t dict = mat + half(p + mat + lane * 2), i, occurrences = 0;
        entry = dict + half(p + dict + 6);
        for (i = 0; i != p[dict + 1]; ++i) {
            uint32_t record = entry + 4 + i * half(p + entry), j;
            uint32_t list = mat + half(p + record), count = p[record + 2];
            for (j = 0; j != count; ++j) {
                if (p[list + j] == material_index && ++occurrences > 1) return 0;
            }
        }
        if (occurrences != 1) return 0;
    }
    return 1;
}

int j2p_g3d_assets_rgba(J2pGuestSpace *space, J2pScope scope,
                       uint32_t models, uint32_t model_bytes, uint32_t texture, uint32_t texture_bytes,
                       uint32_t model_index, uint32_t material_index,
                       uint8_t *output, uint32_t capacity, uint32_t *width, uint32_t *height) {
    J2pModelMaterialBinding binding;
    const uint8_t *p;
    int status;
    if (!width || !height || width == height) return -1;
    *width = 0;
    *height = 0;
    status = j2p_g3d_model_material_binding(space, scope, models, model_bytes, texture, texture_bytes,
                                         model_index, material_index, &binding);
    if (status != 1) return status;
    p = j2p_guest_resolve(space, scope, models, model_bytes, 1);
    if (!p) return -1;
    if (!unambiguous(p, model_index, material_index)) return -3;
    return j2p_g3d_model_material_rgba(space, scope, models, model_bytes, texture, texture_bytes,
                                      model_index, material_index, output, capacity, width, height);
}
