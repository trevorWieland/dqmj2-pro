#include "static_matrix_internal_20261107.h"

static int emit(J2pStaticMatrixWalk *walk, uint32_t opcode, const int32_t *arguments, uint32_t count) {
    uint32_t i;
    J2pMatrixCommand value = {0};
    if (walk->written >= 10000) return -5;
    value.owner = walk->owner;
    value.opcode = opcode;
    value.count = count;
    for (i = 0; i < count; ++i) value.arguments[i] = arguments[i];
    if (walk->commands) walk->commands[walk->written] = value;
    ++walk->written;
    return 1;
}

static int sender(J2pStaticMatrixWalk *walk, const J2pNodePose *pose) {
    int32_t arguments[12];
    uint32_t i, inherited = !(pose->result_flags & 24), combined = 0;
    int status;
    if (inherited && (status = emit(walk, 0x1b, pose->scale_ex1, 3)) != 1) return status;
    if (!(pose->result_flags & 4)) {
        if (inherited) {
            for (i = 0; i < 3; ++i) arguments[i] = j2p_node_pose_mul_q12(pose->translation[i], pose->scale_ex0[i]);
            if ((status = emit(walk, 0x1c, arguments, 3)) != 1) return status;
        } else combined = 1;
    }
    if (!(pose->result_flags & 2)) {
        for (i = 0; i < 9; ++i) arguments[i] = pose->rotation[i];
        for (i = 0; i < 3; ++i) arguments[9 + i] = pose->translation[i];
        if ((status = emit(walk, combined ? 0x19 : 0x1a, arguments, combined ? 12 : 9)) != 1) return status;
    } else if (combined && (status = emit(walk, 0x1c, pose->translation, 3)) != 1) return status;
    if (inherited && (status = emit(walk, 0x1b, pose->scale_ex0, 3)) != 1) return status;
    return pose->result_flags & 1 ? 1 : emit(walk, 0x1b, pose->scale, 3);
}

static int material(J2pStaticMatrixWalk *walk, uint32_t index) {
    const uint8_t *p = walk->model;
    uint32_t record, bytes, flags, need = 44;
    int status;
    if (p[24] > 64) return -2;
    status = j2p_static_record(p, walk->nodes.model_size, j2p_static_word(p + 8), 4, p[24], index, &record);
    if (status != 1) return status;
    if (j2p_static_half(p + record)) return -2;
    bytes = j2p_static_half(p + record + 2);
    if (bytes < 44 || bytes > walk->nodes.model_size - record) return -1;
    flags = j2p_static_half(p + record + 30);
    if (flags & 0xc001) return -2;
    if (flags & 0x2000) {
        need += 64;
        if (!(flags & 2)) need += 8;
        if (!(flags & 4)) need += 4;
        if (!(flags & 8)) need += 8;
    }
    return bytes < need ? -1 : 1;
}

static int shape(J2pStaticMatrixWalk *walk, uint32_t index) {
    const uint8_t *p = walk->model;
    uint32_t record, bytes, offset, count;
    int status = j2p_static_record(p, walk->nodes.model_size, j2p_static_word(p + 12), 0, p[25], index, &record);
    if (status != 1) return status;
    if (j2p_static_half(p + record)) return -2;
    bytes = j2p_static_half(p + record + 2);
    if (bytes < 16 || bytes > walk->nodes.model_size - record) return -1;
    offset = j2p_static_word(p + record + 8);
    count = j2p_static_word(p + record + 12);
    if (count < 4 || offset < bytes || offset > walk->nodes.model_size - record || count > walk->nodes.model_size - record - offset) return -1;
    return j2p_static_display_frame(p + record + offset, count);
}

int j2p_static_walk(J2pStaticMatrixWalk *walk) {
    uint32_t pos = 0;
    if (walk->model[20] != 0) return -2;
    while (pos < walk->nodes.sbc_bytes) {
        uint32_t opcode = walk->script[pos], n = j2p_node_pose_command_length(opcode);
        int status;
        if (!n || n > walk->nodes.sbc_bytes - pos) return -2;
        if (opcode == 1) {
            J2pNodePose final_pose;
            return j2p_node_pose_next(walk->space, &walk->nodes, &final_pose) == 0 ? 1 : -1;
        }
        if ((opcode & 31) == 6) {
            J2pNodePose pose;
            int32_t slot;
            status = j2p_node_pose_next(walk->space, &walk->nodes, &pose);
            if (status != 1) return status;
            if (pose.sbc_offset != pos || pose.model_set != walk->owner.model_set || pose.model_index != walk->owner.model_index) return -1;
            if (opcode & 64) {
                slot = walk->script[pos + (opcode & 32 ? 5 : 4)];
                if (slot >= 31) return -2;
                if ((status = emit(walk, 0x14, &slot, 1)) != 1) return status;
            }
            if ((status = sender(walk, &pose)) != 1) return status;
            if (opcode & 32) {
                slot = walk->script[pos + 4];
                if (slot >= 31) return -2;
                if ((status = emit(walk, 0x13, &slot, 1)) != 1) return status;
            }
        } else if (opcode == 0x0b || opcode == 0x2b) {
            int32_t scale[3];
            scale[0] = scale[1] = scale[2] = j2p_static_signed(j2p_static_word(walk->model + (opcode == 0x0b ? 28 : 32)));
            if ((status = emit(walk, 0x1b, scale, 3)) != 1) return status;
        } else if (opcode == 4 || opcode == 0x24 || opcode == 0x44) {
            if ((status = material(walk, walk->script[pos + 1])) != 1) return status;
        } else if (opcode == 5) {
            if ((status = shape(walk, walk->script[pos + 1])) != 1) return status;
        } else if (opcode == 2) {
            if (walk->script[pos + 1] >= walk->nodes.node_count) return -1;
        } else return -2;
        pos += n;
    }
    return -1;
}
