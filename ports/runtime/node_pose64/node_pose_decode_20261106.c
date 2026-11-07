#include "node_pose_20261106.h"

static uint32_t half(const uint8_t *p) { return p[0] | ((uint32_t)p[1] << 8); }
static uint32_t word(const uint8_t *p) { return half(p) | (half(p + 2) << 16); }
static int32_t signed_word(uint32_t p) { return p <= INT32_MAX ? (int32_t)p : -1 - (int32_t)(UINT32_MAX - p); }
static int32_t signed_half(uint32_t p) { return p < 32768 ? (int32_t)p : -(int32_t)(65536 - p); }
static int has(const uint32_t *bits, uint32_t i) { return (bits[i >> 5] >> (i & 31)) & 1; }
static void set(uint32_t *bits, uint32_t i) { bits[i >> 5] |= 1U << (i & 31); }
static int span(uint32_t start, uint32_t bytes, uint32_t end) { return start <= end && bytes <= end - start; }

static int overlap(const void *a_ptr, uint32_t a_size, const void *b_ptr, uint32_t b_size) {
    uintptr_t a = (uintptr_t)a_ptr, b = (uintptr_t)b_ptr;
    return a_size > UINTPTR_MAX - a || b_size > UINTPTR_MAX - b || (a < b + b_size && b < a + a_size);
}

int j2p_node_pose_next(J2pGuestSpace *space, J2pNodePoseContext *context, J2pNodePose *output) {
    J2pNodePoseContext next;
    J2pNodePose value = {0};
    const uint8_t *model, *script, *dict, *whole;
    uint32_t pos, n, node, parent, entry, record, end, flags, i, pivot, j;
    if (!context || !output || !context->node_count || context->node_count > 64 || context->cursor > context->sbc_bytes ||
        overlap(context, sizeof(*context), output, sizeof(*output))) return -1;
    model = j2p_guest_resolve(space, context->scope, context->model_address, context->model_size, 1);
    script = j2p_guest_resolve(space, context->scope, context->sbc_address, context->sbc_bytes, 1);
    dict = j2p_guest_resolve(space, context->scope, context->node_dict, context->node_dict_bytes, 1);
    whole = j2p_guest_resolve(space, context->scope, context->model_set, context->model_bytes, 1);
    if (!model || !script || !dict || !whole || overlap(output, sizeof(*output), whole, context->model_bytes) ||
        overlap(context, sizeof(*context), whole, context->model_bytes)) return -1;
    pos = context->cursor;
    for (;;) {
        if (pos >= context->sbc_bytes) return -1;
        n = j2p_node_pose_command_length(script[pos]);
        if (!n) return -2;
        if (n > context->sbc_bytes - pos) return -1;
        if (script[pos] == 1) return 0;
        if ((script[pos] & 31) == 6) break;
        pos += n;
    }
    node = script[pos + 1];
    parent = script[pos + 2];
    if (node >= context->node_count || parent >= context->node_count) return -1;
    if (has(context->done_mask, node) || !has(context->ready_mask, parent)) return -3;
    entry = half(dict + 6);
    record = word(dict + entry + 4 + node * half(dict + entry));
    if (record < context->node_dict_bytes || record > UINT32_MAX - 64 || !span(64 + record, 4, context->model_size)) return -1;
    record += 64;
    flags = half(model + record);
    end = 4;
    if (!(flags & 1)) end += 12;
    if (!(flags & 2)) end += flags & 8 ? 4 : 16;
    if (!(flags & 4)) end += 24;
    if (!span(record, end, context->model_size)) return -1;
    value.scope = context->scope;
    value.model_set = context->model_set;
    value.model_index = context->model_index;
    value.node_index = node;
    value.parent_index = parent;
    value.node_address = context->model_address + record;
    value.sbc_address = context->sbc_address;
    value.sbc_offset = pos;
    value.source_flags = flags;
    for (i = 0; i != 3; ++i) value.scale[i] = value.scale_ex0[i] = value.scale_ex1[i] = 4096;
    for (i = 0; i != 9; ++i) value.rotation[i] = i % 4 ? 0 : 4096;
    j = record + 4;
    if (flags & 1) value.result_flags |= 4;
    else for (i = 0; i != 3; ++i) { value.translation[i] = signed_word(word(model + j)); j += 4; }
    if (flags & 2) value.result_flags |= 2;
    else if (flags & 8) {
        int32_t a = signed_half(half(model + j)), b = signed_half(half(model + j + 2));
        uint32_t at = 0;
        pivot = (flags >> 4) & 15;
        if (pivot > 8) return -1;
        for (i = 0; i != 9; ++i) value.rotation[i] = 0;
        value.rotation[pivot] = flags & 256 ? -4096 : 4096;
        for (i = 0; i != 9; ++i) if (i / 3 != pivot / 3 && i % 3 != pivot % 3) {
            value.rotation[i] = at == 0 ? a : at == 1 ? b : at == 2 ? (flags & 512 ? -b : b) : (flags & 1024 ? -a : a);
            ++at;
        }
        j += 4;
    } else {
        value.rotation[0] = signed_half(half(model + record + 2));
        for (i = 1; i != 9; ++i) { value.rotation[i] = signed_half(half(model + j)); j += 2; }
    }
    next = *context;
    if (flags & 4) {
        value.result_flags |= 1;
        if (has(context->unit_mask, parent)) { set(next.unit_mask, node); value.result_flags |= 24; }
        else for (i = 0; i != 6; ++i) next.scale_cache[node][i] = context->scale_cache[parent][i];
    } else {
        next.unit_mask[node >> 5] &= ~(1U << (node & 31));
        for (i = 0; i != 3; ++i) value.scale[i] = signed_word(word(model + j + i * 4));
        if (has(context->unit_mask, parent)) {
            for (i = 0; i != 6; ++i) next.scale_cache[node][i] = signed_word(word(model + j + i * 4));
            value.result_flags |= 24;
        } else for (i = 0; i != 6; ++i)
            next.scale_cache[node][i] = j2p_node_pose_mul_q12(signed_word(word(model + j + i * 4)), context->scale_cache[parent][i]);
    }
    if (!(value.result_flags & 8)) for (i = 0; i != 3; ++i) {
        value.scale_ex0[i] = context->scale_cache[parent][i];
        value.scale_ex1[i] = context->scale_cache[parent][i + 3];
    }
    set(next.ready_mask, node);
    set(next.done_mask, node);
    next.cursor = pos + n;
    *context = next;
    *output = value;
    return 1;
}
