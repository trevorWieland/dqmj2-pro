#include "model_material_binding_20261106.h"
#include "g3d_dictionary_wire_20261106.h"

typedef struct { uint32_t count, entry, unit, names; } Dict;

static uint32_t half(const uint8_t *p) { return p[0] | ((uint32_t)p[1] << 8); }
static uint32_t word(const uint8_t *p) { return half(p) | (half(p + 2) << 16); }
static int span(uint32_t offset, uint32_t bytes, uint32_t end) { return offset <= end && bytes <= end - offset; }

static int dictionary(const uint8_t *p, uint32_t end, uint32_t offset, uint32_t need, Dict *out) {
    uint32_t length, entry, names, count, unit;
    if (!span(offset, 8, end)) return 0;
    length = half(p + offset + 2);
    entry = half(p + offset + 6);
    count = p[offset + 1];
    if (length < 12 || !span(offset, length, end) || entry < 8 + 4 * (count + 1) ||
        !span(entry, 4, length)) return 0;
    unit = half(p + offset + entry);
    names = half(p + offset + entry + 2);
    if (unit < need || names < 4 + count * unit ||
        (uint64_t)entry + names + count * 16 > length) return 0;
    out->count = count;
    out->entry = offset + entry + 4;
    out->unit = unit;
    out->names = offset + entry + names;
    return 1;
}

static int name_for_material(const uint8_t *p, uint32_t end, uint32_t mat, uint32_t offset,
                             uint32_t count, uint32_t selected, uint32_t *name) {
    Dict dict;
    uint32_t i, j;
    uint64_t start = (uint64_t)mat + offset;
    if (start > end || !dictionary(p, end, (uint32_t)start, 4, &dict)) return -1;
    *name = 0;
    for (i = 0; i != dict.count; ++i) {
        uint32_t entry = dict.entry + i * dict.unit, n = p[entry + 2];
        uint64_t list = (uint64_t)mat + half(p + entry);
        if (list > end || !span((uint32_t)list, n, end)) return -1;
        for (j = 0; j != n; ++j) {
            uint32_t index = p[(uint32_t)list + j];
            if (index >= count) return -1;
            if (index == selected) *name = dict.names + i * 16;
        }
    }
    return *name ? 1 : 0;
}

static int overlaps(const void *a_ptr, uint32_t a_len, const void *b_ptr, uint32_t b_len) {
    uintptr_t a = (uintptr_t)a_ptr, b = (uintptr_t)b_ptr;
    return a_len > UINTPTR_MAX - a || b_len > UINTPTR_MAX - b || (a < b + b_len && b < a + a_len);
}

int j2p_g3d_model_material_binding(J2pGuestSpace *space, J2pScope scope,
                                  uint32_t model_set, uint32_t model_available,
                                  uint32_t texture, uint32_t texture_available,
                                  uint32_t model_index, uint32_t material_index, J2pModelMaterialBinding *result) {
    const uint8_t *models, *tex;
    Dict model_dict, materials, target_dict;
    J2pModelMaterialBinding value = {0};
    uint32_t total, tex_total, mdl, mdl_size, end, mat, record, texture_name, palette_name, offset;
    uint64_t address;
    int status;
    if (!result || scope.program || scope.processor != 9 || scope.module != 1 || !scope.generation ||
        model_available < 20 || texture_available < 60) return -1;
    models = j2p_guest_resolve(space, scope, model_set, model_available, 1);
    tex = j2p_guest_resolve(space, scope, texture, texture_available, 1);
    if (!models || !tex || word(models) != UINT32_C(0x304c444d) || word(tex) != UINT32_C(0x30584554)) return -1;
    total = word(models + 4);
    tex_total = word(tex + 4);
    if (total < 20 || total > model_available || tex_total < 60 || tex_total > texture_available ||
        overlaps(result, sizeof(*result), models, total) || overlaps(result, sizeof(*result), tex, tex_total) ||
        !dictionary(models, total, 8, 4, &model_dict)) return -1;
    if (model_index >= model_dict.count) return 0;
    mdl = word(models + model_dict.entry + model_index * model_dict.unit);
    if (!span(mdl, 20, total)) return -1;
    mdl_size = word(models + mdl);
    if (mdl_size < 20 || !span(mdl, mdl_size, total)) return -1;
    end = mdl + mdl_size;
    offset = word(models + mdl + 8);
    if (offset < 20 || !span(offset, 16, mdl_size)) return -1;
    mat = mdl + offset;
    if (!dictionary(models, end, mat + 4, 4, &materials)) return -1;
    if (material_index >= materials.count) return 0;
    address = (uint64_t)mat + word(models + materials.entry + material_index * materials.unit);
    if (address > end || !span((uint32_t)address, 44, end)) return -1;
    record = (uint32_t)address;
    if (half(models + record + 2) < 44 || !span(record, half(models + record + 2), end)) return -1;
    status = name_for_material(models, end, mat, half(models + mat), materials.count, material_index, &texture_name);
    if (status != 1) return status;
    status = name_for_material(models, end, mat, half(models + mat + 2), materials.count, material_index, &palette_name);
    if (status != 1) return status;
    offset = half(tex + 14);
    if (!dictionary(tex, tex_total, offset, 8, &target_dict)) return -1;
    status = j2p_g3d_dict_lookup(space, scope, texture + offset, model_set + texture_name,
                               &value.texture_data, &value.texture_index);
    if (status != 1) return status;
    offset = half(tex + 52);
    if (!offset) return 0;
    if (!dictionary(tex, tex_total, offset, 4, &target_dict)) return -1;
    status = j2p_g3d_dict_lookup(space, scope, texture + offset, model_set + palette_name,
                               &value.palette_data, &value.palette_index);
    if (status != 1) return status;
    value.texture_name = model_set + texture_name;
    value.palette_name = model_set + palette_name;
    value.material_data = model_set + record;
    value.material_count = materials.count;
    *result = value;
    return 1;
}
