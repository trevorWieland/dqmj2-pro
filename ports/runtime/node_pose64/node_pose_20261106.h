#ifndef J2P_NODE_POSE_20261106_H
#define J2P_NODE_POSE_20261106_H
#include "guest_memory_20261106.h"

typedef struct {
    J2pScope scope;
    uint32_t model_set, model_bytes, model_index, model_address, model_size;
    uint32_t node_dict, node_dict_bytes, node_count, sbc_address, sbc_bytes, cursor;
    uint32_t unit_mask[2], ready_mask[2], done_mask[2];
    int32_t scale_cache[64][6];
} J2pNodePoseContext;

typedef struct {
    J2pScope scope;
    uint32_t model_set, model_index, node_index, parent_index, node_address, sbc_address, sbc_offset;
    uint32_t source_flags, result_flags;
    int32_t scale[3], scale_ex0[3], scale_ex1[3], rotation[9], translation[3];
} J2pNodePose;

int32_t j2p_node_pose_mul_q12(int32_t, int32_t);
uint32_t j2p_node_pose_command_length(uint32_t);
int j2p_node_pose_init(J2pGuestSpace *, J2pScope, uint32_t, uint32_t, uint32_t, J2pNodePoseContext *);
int j2p_node_pose_next(J2pGuestSpace *, J2pNodePoseContext *, J2pNodePose *);
#endif
