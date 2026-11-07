#include "texture_decode_20261106.h"

static uint32_t half(const uint8_t *p) { return p[0] | ((uint32_t)p[1] << 8); }
static uint32_t word(const uint8_t *p) { return half(p) | (half(p + 2) << 16); }

static int overlap(const void *left, uint32_t a_bytes, const void *right, uint32_t b_bytes) {
    uintptr_t a = (uintptr_t)left, b = (uintptr_t)right;
    if (!a_bytes || !b_bytes) return 0;
    return a_bytes > UINTPTR_MAX - a || b_bytes > UINTPTR_MAX - b || (a < b + b_bytes && b < a + a_bytes);
}

static uint32_t mix(uint32_t a, uint32_t b, uint32_t first, uint32_t second, uint32_t shift) {
    uint32_t r = (((a & 31) * first + (b & 31) * second) >> shift);
    uint32_t g = ((((a >> 5) & 31) * first + ((b >> 5) & 31) * second) >> shift);
    uint32_t blue = ((((a >> 10) & 31) * first + ((b >> 10) & 31) * second) >> shift);
    return r | (g << 5) | (blue << 10);
}

static void pixel(uint8_t *out, uint32_t color, uint32_t alpha) {
    uint32_t r = color & 31, g = (color >> 5) & 31, b = (color >> 10) & 31;
    out[0] = (uint8_t)((r << 3) | (r >> 2));
    out[1] = (uint8_t)((g << 3) | (g >> 2));
    out[2] = (uint8_t)((b << 3) | (b >> 2));
    out[3] = (uint8_t)alpha;
}

int j2p_texture_decode_rgba(const J2pTextureInput *input, uint8_t *output, uint32_t capacity) {
    J2pTextureInput value;
    uint32_t pixels, need1, need2, bytes, i;
    uint64_t total;
    if (!input || !output) return -1;
    value = *input;
    if (value.format != 3 && value.format != 4 && value.format != 5) return -2;
    if (value.width < 8 || value.width > 1024 || (value.width & (value.width - 1)) ||
        value.height < 8 || value.height > 1024 || (value.height & (value.height - 1)) ||
        value.color0_transparent > 1) return -1;
    total = (uint64_t)value.width * value.height;
    if (total > UINT32_MAX / 4 || (value.format == 5 && total > 524288)) return -1;
    pixels = (uint32_t)total;
    bytes = pixels * 4;
    need1 = value.format == 3 ? pixels / 2 : value.format == 4 ? pixels : pixels / 4;
    need2 = value.format == 5 ? pixels / 8 : 0;
    if (capacity < bytes || !value.data1 || value.data1_bytes < need1 ||
        (need2 && (!value.data2 || value.data2_bytes < need2)) || !value.palette ||
        (value.palette_bytes & 1) || overlap(output, bytes, input, sizeof(*input)) ||
        overlap(output, bytes, value.data1, value.data1_bytes) || overlap(output, bytes, value.data2, value.data2_bytes) ||
        overlap(output, bytes, value.palette, value.palette_bytes)) return -1;
    if (value.format != 5) {
        for (i = 0; i != pixels; ++i) {
            uint32_t index = value.format == 3 ? (value.data1[i >> 1] >> ((i & 1) * 4)) & 15 : value.data1[i];
            if ((index + 1) * 2 > value.palette_bytes) return -1;
        }
        for (i = 0; i != pixels; ++i) {
            uint32_t index = value.format == 3 ? (value.data1[i >> 1] >> ((i & 1) * 4)) & 15 : value.data1[i];
            pixel(output + i * 4, half(value.palette + index * 2), value.color0_transparent && !index ? 0 : 255);
        }
    } else {
        for (i = 0; i != pixels / 16; ++i) {
            uint32_t info = half(value.data2 + i * 2), mode = info >> 14;
            uint32_t colors = mode == 0 ? 3 : mode == 2 ? 4 : 2;
            if ((info & 0x3fff) * 4 + colors * 2 > value.palette_bytes) return -1;
        }
        for (i = 0; i != pixels / 16; ++i) {
            uint32_t info = half(value.data2 + i * 2), mode = info >> 14, offset = (info & 0x3fff) * 4;
            uint32_t colors[4], alpha[4] = {255, 255, 255, 255}, codes = word(value.data1 + i * 4), p;
            colors[0] = half(value.palette + offset);
            colors[1] = half(value.palette + offset + 2);
            colors[2] = mode == 1 ? mix(colors[0], colors[1], 1, 1, 1) :
                        mode == 3 ? mix(colors[0], colors[1], 5, 3, 3) : half(value.palette + offset + 4);
            if (mode < 2) { colors[3] = 0; alpha[3] = 0; }
            else colors[3] = mode == 2 ? half(value.palette + offset + 6) : mix(colors[0], colors[1], 3, 5, 3);
            for (p = 0; p != 16; ++p) {
                uint32_t x = (i % (value.width / 4)) * 4 + (p & 3);
                uint32_t y = (i / (value.width / 4)) * 4 + (p >> 2);
                pixel(output + (y * value.width + x) * 4, colors[codes & 3], alpha[codes & 3]);
                codes >>= 2;
            }
        }
    }
    return 1;
}
