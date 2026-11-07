#include "static_matrix_internal_20261107.h"

uint32_t j2p_static_half(const uint8_t *p) { return p[0] | ((uint32_t)p[1] << 8); }
uint32_t j2p_static_word(const uint8_t *p) { return j2p_static_half(p) | (j2p_static_half(p + 2) << 16); }
int32_t j2p_static_signed(uint32_t value) { return value <= INT32_MAX ? (int32_t)value : -1 - (int32_t)(UINT32_MAX - value); }

int j2p_static_record(const uint8_t *p, uint32_t size, uint32_t base, uint32_t prefix,
    uint32_t count, uint32_t index, uint32_t *record) {
    uint32_t length, at, unit, names, offset, dictionary;
    if (index >= count || base > size || prefix > size - base) return -1;
    dictionary = base + prefix;
    if (size - dictionary < 8 || p[dictionary + 1] != count) return -1;
    length = j2p_static_half(p + dictionary + 2);
    at = j2p_static_half(p + dictionary + 6);
    if (length < 12 || length > size - dictionary || at < 8 + 4 * (count + 1) || at > length - 4) return -1;
    unit = j2p_static_half(p + dictionary + at);
    names = j2p_static_half(p + dictionary + at + 2);
    if (unit < 4 || names < 4 + unit * count || (uint64_t)at + names + 16 * count > length) return -1;
    offset = j2p_static_word(p + dictionary + at + 4 + unit * index);
    if ((uint64_t)prefix + length > offset || offset > size - base || size - base - offset < 4) return -1;
    *record = base + offset;
    return 1;
}

static int parameters(uint32_t opcode) {
    switch (opcode) {
    case 0: case 0x41: return 0;
    case 0x23: return 2;
    case 0x20: case 0x22: case 0x24: case 0x25: case 0x26: case 0x27: case 0x40: return 1;
    default: return -1;
    }
}

int j2p_static_display_frame(const uint8_t *p, uint32_t bytes) {
    uint32_t cursor = 0;
    if (bytes & 3) return -1;
    while (cursor < bytes) {
        uint32_t packed = j2p_static_word(p + cursor), slot;
        cursor += 4;
        for (slot = 0; slot < 4; ++slot) {
            uint32_t op = (packed >> (slot * 8)) & 255;
            int n = parameters(op);
            if (n < 0) return -2;
            if ((uint32_t)n > (bytes - cursor) / 4) return -1;
            cursor += (uint32_t)n * 4;
        }
    }
    return 1;
}
