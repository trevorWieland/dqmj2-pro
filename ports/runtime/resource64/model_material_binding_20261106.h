#ifndef J2P_MODEL_MATERIAL_BINDING_20261106_H
#define J2P_MODEL_MATERIAL_BINDING_20261106_H
#include "guest_memory_20261106.h"

typedef struct {
    uint32_t texture_name, palette_name, texture_data, palette_data;
    uint32_t texture_index, palette_index, material_data, material_count;
} J2pModelMaterialBinding;

int j2p_g3d_model_material_binding(J2pGuestSpace *, J2pScope, uint32_t, uint32_t,
                                  uint32_t, uint32_t, uint32_t, uint32_t, J2pModelMaterialBinding *);
int j2p_g3d_model_material_rgba(J2pGuestSpace *, J2pScope, uint32_t, uint32_t,
                               uint32_t, uint32_t, uint32_t, uint32_t,
                               uint8_t *, uint32_t, uint32_t *, uint32_t *);
#endif
