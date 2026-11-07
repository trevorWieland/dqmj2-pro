#include "node_pose_20261106.h"

_Static_assert(sizeof(J2pNodePoseContext) == 1620 && sizeof(J2pNodePose) == 136, "Owned fixed-width node pose layout");

static uint32_t half(const uint8_t *p) { return p[0] | ((uint32_t)p[1] << 8); }
static uint32_t word(const uint8_t *p) { return half(p) | (half(p + 2) << 16); }
static int span(uint32_t offset, uint32_t bytes, uint32_t end) { return offset <= end && bytes <= end - offset; }

static int dict(const uint8_t *p, uint32_t offset, uint32_t end, uint32_t *entry, uint32_t *length) {
    uint32_t count, unit, names, at;
    if (!span(offset, 8, end)) return 0;
    count = p[offset + 1];
    *length = half(p + offset + 2);
    at = half(p + offset + 6);
    if (*length < 12 || !span(offset, *length, end) || at < 8 + 4 * (count + 1) || !span(at, 4, *length)) return 0;
    unit = half(p + offset + at);
    names = half(p + offset + at + 2);
    if (unit < 4 || names < 4 + unit * count || (uint64_t)at + names + 16 * count > *length) return 0;
    *entry = offset + at;
    return 1;
}

int j2p_node_pose_init(J2pGuestSpace *space, J2pScope scope, uint32_t model_set,
                       uint32_t available, uint32_t model_index, J2pNodePoseContext *output) {
    J2pNodePoseContext value = {0};
    const uint8_t *p;
    uint32_t total, entry, length, model, size, nodes, sbc, end, i, pos;
    uintptr_t a, b;
    if (!output || scope.program || scope.processor != 9 || scope.module != 1 || !scope.generation || available < 20) return -1;
    p = j2p_guest_resolve(space, scope, model_set, available, 1);
    if (!p || word(p) != UINT32_C(0x304c444d)) return -1;
    total = word(p + 4);
    if (total < 20 || total > available || !dict(p, 8, total, &entry, &length)) return -1;
    if (model_index >= p[9]) return 0;
    model = word(p + entry + 4 + model_index * half(p + entry));
    if (!span(model, 64, total)) return -1;
    size = word(p + model);
    if (size < 76 || !span(model, size, total)) return -1;
    if (p[model + 21] != 2) return -2;
    nodes = p[model + 23];
    if (!nodes || nodes > 64 || !dict(p, model + 64, model + size, &entry, &length) || p[model + 65] != nodes) return -1;
    sbc = word(p + model + 4);
    end = size;
    for (i = 8; i <= 16; i += 4) {
        uint32_t next = word(p + model + i);
        if (next > sbc && next < end) end = next;
    }
    if (sbc < 64 || sbc >= end) return -1;
    pos = sbc;
    for (;;) {
        uint32_t opcode = p[model + pos], n = j2p_node_pose_command_length(opcode);
        if (!n) return -2;
        if (n > end - pos) return -1;
        if (opcode == 1) {
            if (end - pos - 1 > 3) return -1;
            for (i = pos + 1; i < end; ++i) if (p[model + i]) return -1;
            break;
        }
        pos += n;
        if (pos == end) return -1;
    }
    a = (uintptr_t)p;
    b = (uintptr_t)output;
    if (available > UINTPTR_MAX - a || sizeof(*output) > UINTPTR_MAX - b ||
        (a < b + sizeof(*output) && b < a + available)) return -1;
    value.scope = scope;
    value.model_set = model_set;
    value.model_bytes = available;
    value.model_index = model_index;
    value.model_address = model_set + model;
    value.model_size = size;
    value.node_dict = model_set + model + 64;
    value.node_dict_bytes = length;
    value.node_count = nodes;
    value.sbc_address = model_set + model + sbc;
    value.sbc_bytes = end - sbc;
    value.unit_mask[0] = value.ready_mask[0] = 1;
    *output = value;
    return 1;
}
