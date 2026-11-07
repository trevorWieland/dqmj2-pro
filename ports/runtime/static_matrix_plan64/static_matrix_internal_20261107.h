#ifndef J2P_STATIC_MATRIX_INTERNAL_20261107_H
#define J2P_STATIC_MATRIX_INTERNAL_20261107_H
#include "static_matrix_plan_20261107.h"
#include "node_pose_20261106.h"

typedef struct {
    J2pGuestSpace *space;
    J2pMatrixOwner owner;
    J2pNodePoseContext nodes;
    const uint8_t *model, *script;
    J2pMatrixCommand *commands;
    uint32_t written;
} J2pStaticMatrixWalk;

uint32_t j2p_static_half(const uint8_t *);
uint32_t j2p_static_word(const uint8_t *);
int32_t j2p_static_signed(uint32_t);
int j2p_static_record(const uint8_t *, uint32_t, uint32_t, uint32_t, uint32_t, uint32_t, uint32_t *);
int j2p_static_display_frame(const uint8_t *, uint32_t);
int j2p_static_walk(J2pStaticMatrixWalk *);
#endif
