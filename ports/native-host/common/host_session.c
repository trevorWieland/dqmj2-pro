#include "host_session.h"
#include <string.h>

int j2p_host_init(J2pHostSession *s) {
    J2pMatrixSeed seed = {0};
    uint32_t i, j;
    if (!s) return 0;
    memset(s, 0, sizeof(*s));
    s->owner = (J2pMatrixOwner){{0, 9, 1, 1}, 0x02700000, 0};
    seed.owner = s->owner;
    seed.mode = 2;
    for (i = 0; i < 4; ++i) for (j = 0; j < 16; ++j) seed.matrices[i][j] = j % 5 == 0 ? 4096 : 0;
    s->x = 128; s->y = 96;
    return j2p_matrix_init(&s->owner, &seed, &s->state) == 1;
}

int j2p_host_touch(J2pHostSession *s, int32_t x, int32_t y) {
    J2pMatrixCommand commands[2] = {0};
    if (!s || x < 0 || x >= 256 || y < 0 || y >= 192) return 0;
    commands[0].owner = commands[1].owner = s->owner;
    commands[0].opcode = 0x15;
    commands[1].opcode = 0x1c; commands[1].count = 3;
    commands[1].arguments[0] = (x - 128) * 32;
    commands[1].arguments[1] = (y - 96) * 4096 / 96;
    if (j2p_matrix_apply(&s->owner, &s->state, commands, 2) != 1) return 0;
    s->x = x; s->y = y; ++s->touches; ++s->revision;
    return 1;
}

void j2p_host_step(J2pHostSession *s) { if (s) ++s->frames; }

int j2p_host_render(const J2pHostSession *s, uint32_t slot, uint8_t *rgba, size_t bytes,
    uint32_t width, uint32_t height, uint32_t stride) {
    uint32_t x, y;
    int32_t cx, cy;
    if (!s || !rgba || slot > 1 || !width || !height || width > 4096 || height > 4096 || stride < width * 4 ||
        (uint64_t)stride * height > bytes) return 0;
    cx = (int32_t)(((int64_t)s->state.matrices[1][12] + 4096) * width / 8192);
    cy = (int32_t)(((int64_t)s->state.matrices[1][13] + 4096) * height / 8192);
    for (y = 0; y < height; ++y) for (x = 0; x < width; ++x) {
        uint8_t *p = rgba + (size_t)y * stride + x * 4;
        int32_t dx = (int32_t)x - cx, dy = (int32_t)y - cy;
        int grid = x % (width / 8 + 1) == 0 || y % (height / 6 + 1) == 0;
        int triangle = dy >= -16 && dy <= 16 && dx >= -(dy + 16) / 2 && dx <= (dy + 16) / 2;
        p[0] = triangle ? 245 : grid ? 80 : 18;
        p[1] = triangle ? 195 : grid ? 110 : slot ? 65 : 25;
        p[2] = triangle ? 35 : grid ? 150 : slot ? 30 : 80;
        p[3] = 255;
    }
    return 1;
}
