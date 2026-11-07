#include "model_material_binding_20261106.h"
#include "texture_decode_20261106.h"

static int overlaps(const void *a_ptr, uint32_t a_len, const void *b_ptr, uint32_t b_len) {
    uintptr_t a = (uintptr_t)a_ptr, b = (uintptr_t)b_ptr;
    return a_len > UINTPTR_MAX - a || b_len > UINTPTR_MAX - b || (a < b + b_len && b < a + a_len);
}

int j2p_g3d_model_material_rgba(J2pGuestSpace *space, J2pScope scope,
                               uint32_t models, uint32_t model_bytes, uint32_t texture, uint32_t texture_bytes,
                               uint32_t model_index, uint32_t material_index,
                               uint8_t *output, uint32_t capacity, uint32_t *width, uint32_t *height) {
    J2pModelMaterialBinding binding;
    const uint8_t *source;
    int status;
    if (!width || !height || width == height) return -1;
    *width = 0;
    *height = 0;
    source = j2p_guest_resolve(space, scope, models, model_bytes, 1);
    if (!source || !output || overlaps(output, capacity, source, model_bytes)) return -1;
    status = j2p_g3d_model_material_binding(space, scope, models, model_bytes, texture, texture_bytes,
                                         model_index, material_index, &binding);
    if (status != 1) return status;
    return j2p_g3d_texture_rgba(space, scope, texture, texture_bytes, binding.texture_name,
                               binding.palette_name, output, capacity, width, height);
}
