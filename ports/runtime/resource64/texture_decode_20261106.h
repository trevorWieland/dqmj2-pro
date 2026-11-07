#ifndef J2P_TEXTURE_DECODE_20261106_H
#define J2P_TEXTURE_DECODE_20261106_H
#include "guest_memory_20261106.h"

typedef struct {
    uint32_t format, width, height, color0_transparent;
    const uint8_t *data1;
    uint32_t data1_bytes;
    const uint8_t *data2;
    uint32_t data2_bytes;
    const uint8_t *palette;
    uint32_t palette_bytes;
} J2pTextureInput;

int j2p_texture_decode_rgba(const J2pTextureInput *, uint8_t *, uint32_t);
int j2p_g3d_texture_rgba(J2pGuestSpace *, J2pScope, uint32_t, uint32_t, uint32_t, uint32_t,
                       uint8_t *, uint32_t, uint32_t *, uint32_t *);
#endif
