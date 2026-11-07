#ifndef J2P_STATIC_SCENE_INTERNAL_20261107_H
#define J2P_STATIC_SCENE_INTERNAL_20261107_H
#include "static_scene_events_20261107.h"
#include "node_pose_20261106.h"

typedef struct {
    J2pGuestSpace *space;
    const J2pSceneSeed *seed;
    J2pSceneTape *tape;
    const uint8_t *model, *script;
    J2pNodePoseContext nodes;
    J2pSceneBuffers *output;
    uint32_t flags, node, description, material, valid[2], cache[64][6], temporary[6], shader[5];
    uint32_t *result;
    uint32_t event_count, shader_count, reference_count, submission_count, matrix_count;
} J2pSceneWalk;

uint32_t j2p_scene_half(const uint8_t *);
uint32_t j2p_scene_word(const uint8_t *);
int j2p_scene_owner_equal(const J2pSceneOwner *, const J2pSceneOwner *);
int j2p_scene_owner_valid(const J2pSceneOwner *);
int j2p_scene_overlap(const void *, uint32_t, const void *, uint32_t);
int j2p_scene_record(const uint8_t *, uint32_t, uint32_t, uint32_t, uint32_t, uint32_t, uint32_t *);
int j2p_scene_material(J2pSceneWalk *, J2pSceneEvent *, uint32_t);
int j2p_scene_walk(J2pSceneWalk *);
#endif
