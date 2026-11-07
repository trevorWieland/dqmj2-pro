#include "g3d_dictionary_wire_20261106.h"

static uint32_t half(const uint8_t *bytes) {
    return (uint32_t)bytes[0] | ((uint32_t)bytes[1] << 8);
}

static int equal_name(const uint8_t *left, const uint8_t *right) {
    uint32_t i;
    for (i = 0; i != 16; ++i) if (left[i] != right[i]) return 0;
    return 1;
}

int j2p_g3d_dict_lookup(J2pGuestSpace *space, J2pScope scope, uint32_t dictionary,
                       uint32_t name, uint32_t *data, uint32_t *index) {
    const uint8_t *dict, *query, *header, *nodes, *candidate;
    uint32_t count, length, entry, unit, names, selected, position, parent, current, bit, steps;
    uint64_t end;
    if (!data || !index || data == index) return -1;
    *data = 0;
    *index = UINT32_MAX;
    if (!space || scope.program != J2P_PROGRAM_HOST || scope.processor != J2P_CPU_ARM9 ||
        scope.module != J2P_MODULE_MAIN || !scope.generation) return -1;
    if (!name) return 0;
    query = j2p_guest_resolve(space, scope, name, 16, 1);
    dict = j2p_guest_resolve(space, scope, dictionary, 8, 1);
    if (!query || !dict) return -1;
    count = dict[1];
    length = half(dict + 2);
    entry = half(dict + 6);
    if (length < 12 || entry < 8 + 4 * (count + 1) || entry > length - 4) return -1;
    dict = j2p_guest_resolve(space, scope, dictionary, length, 1);
    if (!dict) return -1;
    header = dict + entry;
    unit = half(header);
    names = half(header + 2);
    if (names < 4 + unit * count || (uint64_t)entry + names + 16 * count > length) return -1;
    selected = UINT32_MAX;
    if (count < 16) {
        for (position = 0; position != count; ++position) {
            candidate = header + names + position * 16;
            if (equal_name(candidate, query)) { selected = position; break; }
        }
    } else {
        nodes = dict + 8;
        parent = 0;
        current = nodes[1];
        if (!current) return 0;
        steps = 0;
        for (;;) {
            if (current > count || ++steps > 129) return -1;
            if (nodes[parent * 4] <= nodes[current * 4]) break;
            parent = current;
            bit = nodes[current * 4];
            if (bit >= 128) return -1;
            current = nodes[current * 4 + 1 + ((query[bit >> 3] >> (bit & 7)) & 1)];
        }
        position = nodes[current * 4 + 3];
        if (position >= count) return -1;
        candidate = header + names + position * 16;
        if (equal_name(candidate, query)) selected = position;
    }
    if (selected == UINT32_MAX) return 0;
    end = (uint64_t)dictionary + entry + 4 + unit * selected;
    if (end > UINT32_MAX) return -1;
    *data = (uint32_t)end;
    *index = selected;
    return 1;
}

uint32_t j2p_g3d_dict_data(J2pGuestSpace *space, J2pScope scope, uint32_t dictionary, uint32_t name) {
    uint32_t data, index;
    return j2p_g3d_dict_lookup(space, scope, dictionary, name, &data, &index) == 1 ? data : 0;
}

uint32_t j2p_g3d_dict_index(J2pGuestSpace *space, J2pScope scope, uint32_t dictionary, uint32_t name) {
    uint32_t data, index;
    return j2p_g3d_dict_lookup(space, scope, dictionary, name, &data, &index) == 1 ? index : UINT32_MAX;
}
