#ifndef J2P_G3D_FILE_BLOCKS_20261106_H
#define J2P_G3D_FILE_BLOCKS_20261106_H
#include "guest_memory_20261106.h"

enum { J2P_G3D_TEXTURE_BLOCK = 0, J2P_G3D_MODEL_BLOCK = 1 };
int j2p_g3d_file_block(J2pGuestSpace *, J2pScope, uint32_t, uint32_t, uint32_t, uint32_t *, uint32_t *);
#endif
