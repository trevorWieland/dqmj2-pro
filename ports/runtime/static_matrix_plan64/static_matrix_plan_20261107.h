#ifndef J2P_STATIC_MATRIX_PLAN_20261107_H
#define J2P_STATIC_MATRIX_PLAN_20261107_H
#include "matrix_20261106.h"

typedef struct {
    J2pMatrixOwner owner;
    uint32_t model_bytes, model_address, model_size, sbc_address, sbc_bytes, required_mode, command_count;
} J2pStaticMatrixPlan;

int j2p_static_matrix_plan(J2pGuestSpace *, const J2pMatrixOwner *, uint32_t,
    J2pMatrixCommand *, uint32_t, J2pMatrixCommand *, uint32_t, J2pStaticMatrixPlan *);
#endif
