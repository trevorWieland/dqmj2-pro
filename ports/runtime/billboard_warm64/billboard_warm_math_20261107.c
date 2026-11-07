#include "billboard_warm_internal_20261107.h"

static void identity(int32_t out[16]) {
    uint32_t i;
    for (i = 0; i < 16; ++i) out[i] = i % 5 ? 0 : 4096;
}

static void from43(int32_t out[16], const int32_t in[12]) {
    uint32_t r, c;
    identity(out);
    for (r = 0; r < 4; ++r) for (c = 0; c < 3; ++c) out[r * 4 + c] = in[r * 3 + c];
}

static int dot(const int32_t *a, const int32_t *b, int32_t *out) {
    uint64_t absolute = 0;
    int64_t total = 0, shifted;
    uint32_t i;
    for (i = 0; i < 4; ++i) {
        int64_t product = (int64_t)a[i] * b[i * 4];
        uint64_t magnitude = product < 0 ? (uint64_t)(-product) : (uint64_t)product;
        if (magnitude > (uint64_t)INT64_MAX - absolute) return 0;
        absolute += magnitude;
        total += product;
    }
    shifted = total / 4096;
    if (total < 0 && total % 4096) --shifted;
    if (shifted < INT32_MIN || shifted > INT32_MAX) return 0;
    *out = (int32_t)shifted;
    return 1;
}

static uint64_t square_root(uint64_t value) {
    uint64_t low = 0, high = INT32_MAX;
    while (high - low > 1) {
        uint64_t middle = low + (high - low) / 2;
        if (middle * middle <= value) low = middle;
        else high = middle;
    }
    return low;
}

static int magnitude(const int32_t in[3], int32_t *out) {
    const uint64_t limit = (UINT64_C(1) << 60) - (UINT64_C(1) << 30);
    uint64_t total = 0;
    uint32_t i;
    for (i = 0; i < 3; ++i) {
        int64_t value = in[i];
        uint64_t squared = (uint64_t)(value * value);
        if (squared > limit - total) return 0;
        total += squared;
    }
    *out = (int32_t)((square_root(total * 4) + 1) / 2);
    return 1;
}

static void command(J2pBb7Effect *effect, uint32_t opcode, const int32_t *values, uint32_t count) {
    J2pMatrixCommand *out = &effect->terminal[effect->terminal_count++];
    uint32_t i;
    out->owner = effect->owner.model;
    out->opcode = opcode;
    out->count = count;
    for (i = 0; i < count; ++i) out->arguments[i] = values[i];
}

int j2p_bb7_calculate(const J2pBb7WarmContext *warm, J2pBb7State *state, J2pBb7Effect *effect) {
    int32_t forward[16], transform[16], packed[12], mode = 2;
    uint32_t r, c, i;
    static const uint32_t operations[9] = {0x10, 0x11, 0x15, 0x10000, 0x12, 0x10, 0x17, 0x19, 0x1b};
    for (i = 0; i < 16; ++i) effect->readback[i] = state->matrix.matrices[1][i];
    if (warm->branch) {
        from43(forward, warm->forward43);
        for (r = 0; r < 4; ++r) for (c = 0; c < 4; ++c)
            if (!dot(effect->readback + r * 4, forward + c, effect->corrected + r * 4 + c)) return -4;
    } else for (i = 0; i < 16; ++i) effect->corrected[i] = effect->readback[i];
    identity(transform);
    for (i = 0; i < 3; ++i) {
        if (!magnitude(effect->corrected + i * 4, effect->magnitudes + i)) return -4;
        transform[12 + i] = effect->translation[i] = effect->corrected[12 + i];
    }
    for (r = 0; r < 4; ++r) for (c = 0; c < 3; ++c) packed[r * 3 + c] = transform[r * 4 + c];
    command(effect, 0x10, &mode, 1);
    if (warm->branch) {
        command(effect, 0x17, warm->stored_inverse43, 12);
        command(effect, 0x19, packed, 12);
    } else command(effect, 0x17, packed, 12);
    command(effect, 0x1b, effect->magnitudes, 3);
    effect->logical_commands = warm->branch ? 8 : 7;
    for (i = 0; i < 9; ++i)
        if (warm->branch || i != 7) effect->source_operations[effect->source_effect_count++] = operations[i];
    return j2p_matrix_apply(&effect->owner.model, &state->matrix, effect->terminal, effect->terminal_count);
}
