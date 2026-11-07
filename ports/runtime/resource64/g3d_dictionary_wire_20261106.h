#ifndef J2P_G3D_DICTIONARY_WIRE_20261106_H
#define J2P_G3D_DICTIONARY_WIRE_20261106_H
#include "guest_memory_20261106.h"

int j2p_g3d_dict_lookup(J2pGuestSpace *, J2pScope, uint32_t, uint32_t, uint32_t *, uint32_t *);
uint32_t j2p_g3d_dict_data(J2pGuestSpace *, J2pScope, uint32_t, uint32_t);
uint32_t j2p_g3d_dict_index(J2pGuestSpace *, J2pScope, uint32_t, uint32_t);
#endif
