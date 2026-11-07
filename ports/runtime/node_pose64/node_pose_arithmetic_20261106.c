#include "node_pose_20261106.h"

int32_t j2p_node_pose_mul_q12(int32_t left, int32_t right) {
    int64_t product = (int64_t)left * right;
    int64_t shifted = product >= 0 ? product / 4096 : -((-product + 4095) / 4096);
    uint32_t bits = (uint32_t)shifted;
    return bits <= INT32_MAX ? (int32_t)bits : -1 - (int32_t)(UINT32_MAX - bits);
}

uint32_t j2p_node_pose_command_length(uint32_t opcode) {
    switch (opcode) {
    case 1: case 0x0b: case 0x2b: return 1;
    case 2: return 3;
    case 4: case 0x24: case 0x44: case 5: case 7: case 8: return 2;
    case 6: return 4;
    case 0x26: case 0x46: return 5;
    case 0x66: return 6;
    default: return 0;
    }
}
