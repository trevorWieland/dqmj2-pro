#ifndef J2P_MATRIX_20261106_H
#define J2P_MATRIX_20261106_H
#include "guest_memory_20261106.h"

typedef struct { J2pScope scope; uint32_t model_set, model_index; } J2pMatrixOwner;
typedef struct { J2pMatrixOwner owner; uint32_t mode; int32_t matrices[4][16]; } J2pMatrixSeed;
typedef struct { J2pMatrixOwner owner; uint32_t opcode, count; int32_t arguments[16]; } J2pMatrixCommand;
typedef struct {
    J2pMatrixOwner owner;
    uint32_t mode, valid_slots;
    int32_t matrices[4][16];
    int32_t position_stack[32][16], vector_stack[32][16];
} J2pMatrixState;

int j2p_matrix_init(const J2pMatrixOwner *, const J2pMatrixSeed *, J2pMatrixState *);
int j2p_matrix_apply(const J2pMatrixOwner *, J2pMatrixState *, const J2pMatrixCommand *, uint32_t);
#endif
