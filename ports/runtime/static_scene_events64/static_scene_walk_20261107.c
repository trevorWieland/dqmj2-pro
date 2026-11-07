#include "static_scene_internal_20261107.h"

int j2p_scene_walk(J2pSceneWalk *walk) {
    uint32_t pos = 0, i;
    walk->flags = 1;
    walk->node = walk->description = walk->material = UINT32_MAX;
    for (i = 0; i < 5; ++i) walk->shader[i] = walk->seed->initial_shader[i];
    while (pos < walk->tape->plan.sbc_bytes) {
        J2pSceneEvent event = {0};
        uint32_t opcode = walk->script[pos], n = j2p_node_pose_command_length(opcode);
        int status;
        if (!n || n > walk->tape->plan.sbc_bytes - pos) return -1;
        event.offset = pos;
        event.ordinal = walk->event_count;
        event.opcode = opcode;
        event.length = n;
        event.matrix_begin = walk->matrix_count;
        event.shader_begin = walk->shader_count;
        event.shape_reference = event.shape_index = event.submission_ordinal = UINT32_MAX;
        if ((opcode & 31) == 6) {
            J2pNodePose pose;
            uint32_t flag, inherited;
            status = j2p_node_pose_next(walk->space, &walk->nodes, &pose);
            if (status != 1 || pose.sbc_offset != pos) return status == 1 ? -1 : status;
            flag = pose.result_flags;
            inherited = !(flag & 24);
            event.matrix_count = 2 * inherited + !(flag & 1) + !(flag & 2) +
                (!(flag & 4) && (inherited || (flag & 2))) + !!(opcode & 32) + !!(opcode & 64);
            walk->description = walk->script[pos + 1];
            walk->flags |= 16;
        } else if (opcode == 0x0b || opcode == 0x2b) event.matrix_count = 1;
        else if (opcode == 2) {
            walk->node = walk->script[pos + 1];
            walk->flags = ((walk->flags | 4) & ~1U) | (walk->script[pos + 2] & 1);
        } else if ((opcode & 31) == 4) {
            status = j2p_scene_material(walk, &event, walk->script[pos + 1]);
            if (status != 1) return status;
        } else if (opcode == 5) {
            uint32_t record, offset;
            event.shape_reference = walk->reference_count++;
            event.shape_index = walk->script[pos + 1];
            status = j2p_scene_record(walk->model, walk->tape->plan.model_size, j2p_scene_word(walk->model + 12),
                0, walk->tape->shapes, event.shape_index, &record);
            if (status != 1 || walk->tape->plan.model_size - record < 16) return -1;
            offset = j2p_scene_word(walk->model + record + 8);
            if (offset > walk->tape->plan.model_size - record) return -1;
            event.shape_address = walk->tape->plan.model_address + record;
            event.display_address = event.shape_address + offset;
            event.display_bytes = j2p_scene_word(walk->model + record + 12);
            event.submission = !(walk->flags & 1) ? 2 : walk->flags & 2 ? 3 : 1;
            if (event.submission == 1) event.submission_ordinal = walk->submission_count++;
        } else if (opcode == 1) walk->flags |= 32;
        else return -2;
        if (event.matrix_count > walk->tape->plan.command_count - walk->matrix_count) return -1;
        walk->matrix_count += event.matrix_count;
        event.flags = walk->flags;
        event.node = walk->node;
        event.description = walk->description;
        event.material = walk->material;
        event.material_valid = !!(walk->flags & 8);
        if (walk->result) for (i = 0; i < 6; ++i) event.result[i] = walk->result[i];
        for (i = 0; i < 5; ++i) event.shader_state[i] = walk->shader[i];
        for (i = 0; i < 2; ++i) event.cache_valid[i] = walk->valid[i];
        if (walk->event_count == UINT32_MAX / sizeof(event)) return -5;
        if (walk->output) walk->output->events[walk->event_count] = event;
        ++walk->event_count;
        if (opcode == 1) return walk->matrix_count == walk->tape->plan.command_count ? 1 : -1;
        pos += n;
    }
    return -1;
}
