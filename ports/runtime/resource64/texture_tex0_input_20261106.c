#include "texture_decode_20261106.h"
#include "g3d_dictionary_wire_20261106.h"

static uint32_t half(const uint8_t *p) { return p[0] | ((uint32_t)p[1] << 8); }
static uint32_t word(const uint8_t *p) { return half(p) | (half(p + 2) << 16); }

static int dictionary(J2pGuestSpace *space, J2pScope scope, uint32_t base, const uint8_t *input,
                      uint32_t total, uint32_t offset, uint32_t name, uint32_t need, uint32_t *record) {
    uint32_t length, entry, address, index;
    int status;
    if (offset > total || total - offset < 12) return -1;
    length = half(input + offset + 2);
    entry = half(input + offset + 6);
    if (length < 12 || length > total - offset || entry > length - 4 ||
        half(input + offset + entry) < need) return -1;
    status = j2p_g3d_dict_lookup(space, scope, base + offset, name, &address, &index);
    if (status != 1) return status;
    if (address < base || (uint64_t)address + need > (uint64_t)base + total) return -1;
    *record = address - base;
    return 1;
}

static int overlap(const void *left, uint32_t a_size, const void *right, uint32_t b_size) {
    uintptr_t a = (uintptr_t)left, b = (uintptr_t)right;
    return a_size > UINTPTR_MAX - a || b_size > UINTPTR_MAX - b || (a < b + b_size && b < a + a_size);
}

int j2p_g3d_texture_rgba(J2pGuestSpace *space, J2pScope scope, uint32_t texture, uint32_t available,
                        uint32_t texture_name, uint32_t palette_name, uint8_t *output, uint32_t capacity,
                        uint32_t *width, uint32_t *height) {
    const uint8_t *input;
    J2pTextureInput value = {0};
    uint32_t total, record, param, offset, region, region_bytes, need1, need2, palette_dict, palette_record;
    uint32_t palette_region, palette_bytes, palette_start, palette_end, entry, unit, count, i, pixels;
    int status;
    if (!width || !height || width == height) return -1;
    *width = 0;
    *height = 0;
    if (scope.program || scope.processor != 9 || scope.module != 1 || !scope.generation || available < 60 || !output) return -1;
    input = j2p_guest_resolve(space, scope, texture, available, 1);
    if (!input || word(input) != UINT32_C(0x30584554)) return -1;
    total = word(input + 4);
    if (total < 60 || total > available) return -1;
    status = dictionary(space, scope, texture, input, total, half(input + 14), texture_name, 8, &record);
    if (status != 1) return status;
    param = word(input + record);
    value.format = (param >> 26) & 7;
    if (value.format != 3 && value.format != 4 && value.format != 5) return -2;
    value.width = 8U << ((param >> 20) & 7);
    value.height = 8U << ((param >> 23) & 7);
    value.color0_transparent = (param >> 29) & 1;
    pixels = value.width * value.height;
    if (capacity < pixels * 4 || overlap(output, pixels * 4, input, total)) return -1;
    offset = (param & 0xffff) * 8;
    region = word(input + (value.format == 5 ? 36 : 20));
    region_bytes = half(input + (value.format == 5 ? 28 : 12)) * 8;
    need1 = value.format == 3 ? pixels / 2 : value.format == 4 ? pixels : pixels / 4;
    need2 = value.format == 5 ? pixels / 8 : 0;
    if ((uint64_t)region + region_bytes > total || offset > region_bytes || need1 > region_bytes - offset) return -1;
    value.data1 = input + region + offset;
    value.data1_bytes = need1;
    if (need2) {
        region = word(input + 40);
        if ((uint64_t)region + region_bytes / 2 > total || offset / 2 > region_bytes / 2 ||
            need2 > region_bytes / 2 - offset / 2) return -1;
        value.data2 = input + region + offset / 2;
        value.data2_bytes = need2;
    }
    palette_dict = half(input + 52);
    if (!palette_dict) return 0;
    status = dictionary(space, scope, texture, input, total, palette_dict, palette_name, 4, &palette_record);
    if (status != 1) return status;
    palette_region = word(input + 56);
    palette_bytes = half(input + 48) * 8;
    palette_start = half(input + palette_record) * 8;
    if ((uint64_t)palette_region + palette_bytes > total || palette_start > palette_bytes) return -1;
    palette_end = palette_bytes;
    entry = palette_dict + half(input + palette_dict + 6);
    unit = half(input + entry);
    count = input[palette_dict + 1];
    for (i = 0; i != count; ++i) {
        uint32_t next = half(input + entry + 4 + i * unit) * 8;
        if (next > palette_bytes) return -1;
        if (next > palette_start && next < palette_end) palette_end = next;
    }
    value.palette = input + palette_region + palette_start;
    value.palette_bytes = palette_end - palette_start;
    status = j2p_texture_decode_rgba(&value, output, capacity);
    if (status == 1) { *width = value.width; *height = value.height; }
    return status;
}
