#include <stddef.h>
#include "g3d_texture_material_20261106.h"
#include "g3d_dictionary_wire_20261106.h"
#include "g3d_texture_types_20261106.h"

#if __BYTE_ORDER__ != __ORDER_LITTLE_ENDIAN__
#error Native texture scratch objects require a qualified little-endian target
#endif

typedef struct {
    J2pGuestSpace *space;
    J2pScope scope;
    uint32_t dictionary, name_address, expected, palette, calls;
    NNSG3dResTex texture;
    NNSG3dResName name;
    NNSG3dResDictTexData texture_data;
    NNSG3dResDictPlttData palette_data;
    NNSG3dMatAnmResult result;
} J2pMaterialCall;

static J2pMaterialCall *active;

_Static_assert(sizeof(u32) == 4 && sizeof(s32) == 4 && sizeof(NNSG3dMatAnmResultFlag) == 4, "SDK scalar widths");
_Static_assert(sizeof(NNSG3dResTex) == 72 && offsetof(NNSG3dResTex, dict) == 60, "Texture metadata layout");
_Static_assert(offsetof(NNSG3dResTex, tex4x4Info) == 24 && offsetof(NNSG3dResTex, plttInfo) == 44, "Texture key layout");
_Static_assert(sizeof(NNSG3dMatAnmResult) == 56 && offsetof(NNSG3dMatAnmResult, origWidth) == 44, "Material result layout");
_Static_assert(offsetof(NNSG3dMatAnmResult, magW) == 48 && sizeof(NNSG3dResName) == 16, "Material fields");

static uint32_t word(const uint8_t *bytes) {
    return (uint32_t)bytes[0] | ((uint32_t)bytes[1] << 8) | ((uint32_t)bytes[2] << 16) | ((uint32_t)bytes[3] << 24);
}

static int overlap(const void *left, uint32_t first, const void *right, uint32_t second) {
    uintptr_t a = (uintptr_t)left, b = (uintptr_t)right;
    return first > UINTPTR_MAX - a || second > UINTPTR_MAX - b || (a < b + second && b < a + first);
}

void *native_fn_0202bbb4(const NNSG3dResDict *dictionary, const NNSG3dResName *name) {
    uint32_t address, index, i;
    const uint8_t *bytes;
    if (!active || dictionary != &active->texture.dict || name != &active->name ||
        j2p_g3d_dict_lookup(active->space, active->scope, active->dictionary, active->name_address, &address, &index) != 1 ||
        address != active->expected) __builtin_trap();
    bytes = j2p_guest_resolve(active->space, active->scope, address, active->palette ? 4 : 8, 1);
    if (!bytes) __builtin_trap();
    ++active->calls;
    if (active->palette) {
        uint8_t *typed = (uint8_t *)&active->palette_data;
        for (i = 0; i != 4; ++i) typed[i] = bytes[i];
        return &active->palette_data;
    }
    active->texture_data.texImageParam = word(bytes);
    active->texture_data.extraParam = word(bytes + 4);
    return &active->texture_data;
}

fx32 native_fn_0200235c(fx32 numerator, fx32 denominator) {
    (void)numerator;
    (void)denominator;
    __builtin_trap();
}

static int apply(J2pGuestSpace *space, J2pScope scope, uint32_t texture,
                 uint32_t name, uint32_t result, uint32_t palette) {
    J2pMaterialCall call = {0};
    uint8_t *output, *typed;
    const uint8_t *header, *query, *whole;
    uint32_t length, offset, data, index, i, dict_length, entry;
    int found;
    uint64_t dictionary;
    if (active || scope.program != J2P_PROGRAM_HOST || scope.processor != J2P_CPU_ARM9 ||
        scope.module != J2P_MODULE_MAIN || !scope.generation) return -1;
    header = j2p_guest_resolve(space, scope, texture, 60, 1);
    output = j2p_guest_resolve(space, scope, result, 56, 1);
    query = j2p_guest_resolve(space, scope, name, 16, 1);
    if (!header || !output || !query) return -1;
    length = word(header + 4);
    whole = j2p_guest_resolve(space, scope, texture, length, 1);
    if (length < 60 || !whole || overlap(output, 56, whole, length) || overlap(output, 56, query, 16)) return -1;
    offset = palette ? (uint32_t)header[52] | ((uint32_t)header[53] << 8) : 60;
    if (!offset) return 0;
    dictionary = (uint64_t)texture + offset;
    if (dictionary > UINT32_MAX || offset > length - 8) return -1;
    dict_length = (uint32_t)whole[offset + 2] | ((uint32_t)whole[offset + 3] << 8);
    entry = (uint32_t)whole[offset + 6] | ((uint32_t)whole[offset + 7] << 8);
    if (dict_length < 12 || dict_length > length - offset || entry > dict_length - 4 ||
        ((uint32_t)whole[offset + entry] | ((uint32_t)whole[offset + entry + 1] << 8)) < (palette ? 4U : 8U)) return -1;
    found = j2p_g3d_dict_lookup(space, scope, (uint32_t)dictionary, name, &data, &index);
    if (found != 1) return found;
    if (!j2p_guest_resolve(space, scope, data, palette ? 4 : 8, 1)) return -1;
    call.space = space;
    call.scope = scope;
    call.dictionary = (uint32_t)dictionary;
    call.name_address = name;
    call.expected = data;
    call.palette = palette;
    typed = (uint8_t *)&call.texture;
    for (i = 0; i != 60; ++i) typed[i] = header[i];
    call.texture.plttInfo.ofsDict = (u16)offsetof(NNSG3dResTex, dict);
    for (i = 0; i != 16; ++i) call.name.name[i] = (char)query[i];
    typed = (uint8_t *)&call.result;
    for (i = 0; i != 56; ++i) typed[i] = output[i];
    active = &call;
    if (palette) native_main_02034320(&call.texture, &call.name, &call.result);
    else native_main_02034248(&call.texture, &call.name, &call.result);
    active = 0;
    if (call.calls != 1) return -1;
    for (i = 0; i != 56; ++i) output[i] = typed[i];
    return 1;
}

int j2p_g3d_material_texture(J2pGuestSpace *space, J2pScope scope, uint32_t texture, uint32_t name, uint32_t result) {
    return apply(space, scope, texture, name, result, 0);
}

int j2p_g3d_material_palette(J2pGuestSpace *space, J2pScope scope, uint32_t texture, uint32_t name, uint32_t result) {
    return apply(space, scope, texture, name, result, 1);
}
