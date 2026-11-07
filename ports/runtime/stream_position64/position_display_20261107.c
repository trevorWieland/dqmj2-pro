#include "position_internal_20261107.h"

static int32_t signed_half(uint32_t v) {
    v &= 65535;
    return v < 32768 ? (int32_t)v : -1 - (int32_t)(65535 - v);
}

static int parameters(uint32_t op) {
    switch (op) {
    case 0: case 0x41: return 0;
    case 0x20: case 0x22: case 0x24: case 0x25: case 0x26: case 0x27: case 0x40: return 1;
    case 0x23: return 2;
    default: return -1;
    }
}

int j2p_position_display(J2pPositionWalk *walk, const J2pSceneEvent *e, const J2pSceneSnapshot *s) {
    const uint8_t *p = j2p_guest_resolve(walk->space, walk->owner->model.scope, e->display_address, e->display_bytes, 1);
    uint32_t at = 0, ordinal = 0, ready = 0;
    int32_t clip[16];
    if (!p || e->display_bytes < 4 || e->display_bytes & 3) return -1;
    while (at < e->display_bytes) {
        uint32_t header_at = at, header = j2p_position_word(p + at), slot;
        at += 4;
        for (slot = 0; slot < 4; ++slot) {
            uint32_t op = (header >> (slot * 8)) & 255;
            int n = parameters(op);
            if (n < 0) return -2;
            if ((uint32_t)n > (e->display_bytes - at) / 4) return -1;
            if (op >= 0x23 && op <= 0x27) {
                J2pPositionRecord value = {0};
                uint32_t word = j2p_position_word(p + at), i;
                if (op == 0x23 || op == 0x24) {
                    for (i = 0; i < 3; ++i) {
                        if (op == 0x23) walk->state.xyz[i] = signed_half(i == 2 ? j2p_position_word(p + at + 4) : word >> (i * 16));
                        else {
                            uint32_t f = (word >> (i * 10)) & 1023;
                            walk->state.xyz[i] = (f < 512 ? (int32_t)f : (int32_t)f - 1024) * 64;
                        }
                    }
                    walk->state.known_axes = 7;
                } else {
                    uint32_t a = op == 0x27 ? 1 : 0, b = op == 0x25 ? 1 : 2;
                    walk->state.xyz[a] = signed_half(word);
                    walk->state.xyz[b] = signed_half(word >> 16);
                    walk->state.known_axes |= (1U << a) | (1U << b);
                }
                if (walk->state.known_axes != 7) return -3;
                if (!ready) {
                    if (j2p_position_clip(s, clip) != 1) return -4;
                    ready = 1;
                }
                if (j2p_position_vertex(walk->state.xyz, clip, value.position) != 1) return -4;
                if (walk->count == UINT32_MAX / sizeof(value)) return -5;
                value.owner = walk->state.owner;
                value.sbc_address = walk->tape->plan.sbc_address; value.sbc_offset = e->offset; value.event_ordinal = e->ordinal;
                value.reference_ordinal = e->shape_reference; value.submission_ordinal = e->submission_ordinal;
                value.shape_index = e->shape_index; value.shape_address = e->shape_address;
                value.display_address = e->display_address; value.display_bytes = e->display_bytes;
                value.header_offset = header_at; value.opcode_slot = slot; value.parameter_offset = at; value.opcode = op;
                value.vertex_ordinal = walk->count; value.submission_vertex_ordinal = ordinal++;
                for (i = 0; i < 3; ++i) value.xyz[i] = walk->state.xyz[i];
                if (walk->output) walk->output[walk->count] = value;
                ++walk->count;
            }
            at += (uint32_t)n * 4;
        }
    }
    return 1;
}
