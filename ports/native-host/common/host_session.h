#ifndef J2P_HOST_SESSION_H
#define J2P_HOST_SESSION_H
#include <stddef.h>
#include <stdint.h>
#include "matrix_20261106.h"
typedef struct {
    J2pMatrixOwner owner;
    J2pMatrixState state;
    uint64_t frames, touches, revision;
    int32_t x, y;
} J2pHostSession;
int j2p_host_init(J2pHostSession *);
int j2p_host_touch(J2pHostSession *, int32_t, int32_t);
void j2p_host_step(J2pHostSession *);
int j2p_host_render(const J2pHostSession *, uint32_t, uint8_t *, size_t, uint32_t, uint32_t, uint32_t);
#endif
