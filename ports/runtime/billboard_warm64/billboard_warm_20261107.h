#ifndef J2P_BILLBOARD_WARM_20261107_H
#define J2P_BILLBOARD_WARM_20261107_H
#include "matrix_20261106.h"

typedef struct {
    J2pMatrixOwner model;
    uint32_t instance_id, run_generation, matrix_generation, camera_id, camera_generation;
    uint32_t base_generation, cache_generation, projection_generation, queue_generation;
} J2pBb7Owner;

typedef struct {
    J2pBb7Owner owner;
    uint32_t raw_flush_bits, branch, selected_state, cache_valid_mask, provider_flags;
    int32_t forward43[12], stored_inverse43[12];
} J2pBb7WarmContext;

typedef struct {
    J2pBb7Owner owner;
    J2pMatrixState matrix;
    uint32_t projection_depth, projection_error_known, projection_error, projection_saved_valid;
    int32_t projection_saved[16];
    uint32_t queue_complete, queued_commands, async_known, async_active;
} J2pBb7State;

typedef struct {
    J2pBb7Owner owner;
    uint32_t raw_flush_bits, branch, cache_valid_mask, logical_commands, terminal_count, source_effect_count;
    uint32_t projection_depth_before, projection_depth_after, projection_slot_written;
    int32_t readback[16], corrected[16], translation[3], magnitudes[3], saved_projection[16];
    uint32_t source_operations[9];
    J2pMatrixCommand terminal[4];
} J2pBb7Effect;

int j2p_billboard_warm(const J2pBb7Owner *, const J2pBb7WarmContext *, const J2pBb7State *,
    J2pBb7State *, J2pBb7Effect *);
#endif
