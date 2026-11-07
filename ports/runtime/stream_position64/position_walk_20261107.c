#include "position_internal_20261107.h"

static int profile(const J2pSceneEvent *e) {
    switch (e->opcode) {
    case 6: case 0x26: case 0x46: case 0x66: return e->matrix_count <= 6 && !e->shader_count;
    case 0x0b: case 0x2b: return e->matrix_count == 1 && !e->shader_count;
    case 4: case 0x24: case 0x44: return !e->matrix_count && (e->shader_count == 0 || e->shader_count == 5);
    case 1: case 2: case 5: return !e->matrix_count && !e->shader_count;
    default: return 0;
    }
}

static int snapshot(const J2pPositionWalk *w, const J2pSceneEvent *e, const J2pSceneSnapshot *s, uint32_t prefix) {
    return j2p_position_same(w->owner, &s->owner) && s->sbc_address == w->tape->plan.sbc_address &&
        s->offset == e->offset && s->event_ordinal == e->ordinal && s->shape_index == e->shape_index && s->shape_address == e->shape_address &&
        s->display_address == e->display_address && s->display_bytes == e->display_bytes && s->reference_ordinal == e->shape_reference &&
        s->submission_ordinal == e->submission_ordinal && s->submission == e->submission && s->material == e->material &&
        s->material_valid == e->material_valid && s->matrix_prefix == prefix && s->mode == 2 && !(s->valid_slots & UINT32_C(0x80000000));
}

int j2p_position_walk(J2pPositionWalk *w) {
    uint32_t i, at = 0, matrix = 0, shader = 0, reference = 0, submitted = 0;
    for (i = 0; i < w->tape->events; ++i) {
        const J2pSceneEvent *e = w->events + i;
        uint32_t n = j2p_node_pose_command_length(e->opcode);
        if (!profile(e) || e->material_evaluation > 4 ||
            (((e->opcode & 31) == 4) ? !e->material_evaluation : !!e->material_evaluation)) return -2;
        if (at >= w->tape->plan.sbc_bytes || e->offset != at || e->ordinal != i || e->length != n || n > w->tape->plan.sbc_bytes - at ||
            w->script[at] != e->opcode || e->matrix_begin != matrix || e->shader_begin != shader ||
            e->matrix_count > w->tape->plan.command_count - matrix || e->shader_count > w->tape->shaders - shader) return -1;
        if (e->flags & ~63U || e->material_valid != !!(e->flags & 8) ||
            (e->material_valid ? e->material >= w->tape->materials : e->material != UINT32_MAX)) return -1;
        if (((e->flags & 4) && e->node >= w->tape->nodes) || ((e->flags & 16) && e->description >= w->tape->nodes)) return -1;
        if (e->opcode == 5) {
            const J2pSceneSnapshot *s;
            uint32_t decision = !(e->flags & 1) ? 2 : e->flags & 2 ? 3 : 1;
            int status;
            if (reference >= w->tape->shape_references || e->shape_reference != reference || e->submission != decision ||
                e->shape_index >= w->tape->shapes || w->script[at + 1] != e->shape_index || e->display_bytes < 4 || e->display_bytes & 3 ||
                e->shape_address < w->tape->plan.model_address || e->display_address < e->shape_address ||
                (uint64_t)e->display_address + e->display_bytes > (uint64_t)w->tape->plan.model_address + w->tape->plan.model_size) return -1;
            s = w->snapshots + reference++;
            if (!snapshot(w, e, s, matrix)) return -1;
            if (e->submission == 1) {
                if (e->submission_ordinal != submitted++) return -1;
                status = j2p_position_display(w, e, s);
                if (status != 1) return status;
            } else if (e->submission_ordinal != UINT32_MAX) return -1;
        } else if (e->submission || e->shape_reference != UINT32_MAX) return -1;
        matrix += e->matrix_count; shader += e->shader_count; at += n;
        if (e->opcode == 1 && i + 1 != w->tape->events) return -1;
    }
    if (!w->tape->events || w->events[w->tape->events - 1].opcode != 1 || at > w->tape->plan.sbc_bytes ||
        w->tape->plan.sbc_bytes - at > 3 || matrix != w->tape->plan.command_count || shader != w->tape->shaders ||
        reference != w->tape->shape_references || submitted != w->tape->submissions) return -1;
    w->submitted = submitted;
    return 1;
}
