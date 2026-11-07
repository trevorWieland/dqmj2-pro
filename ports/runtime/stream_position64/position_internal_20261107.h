#ifndef J2P_POSITION_INTERNAL_20261107_H
#define J2P_POSITION_INTERNAL_20261107_H
#include "stream_position_20261107.h"
#include "node_pose_20261106.h"

typedef struct {
    J2pGuestSpace *space;
    const J2pSceneOwner *owner;
    const J2pSceneTape *tape;
    const J2pSceneEvent *events;
    const J2pSceneSnapshot *snapshots;
    const uint8_t *script;
    J2pPositionSeed state;
    J2pPositionRecord *output;
    uint32_t count, submitted;
} J2pPositionWalk;

uint32_t j2p_position_word(const uint8_t *);
int j2p_position_same(const J2pSceneOwner *, const J2pSceneOwner *);
int j2p_position_overlap(const void *, uint32_t, const void *, uint32_t);
int j2p_position_clip(const J2pSceneSnapshot *, int32_t *);
int j2p_position_vertex(const int32_t *, const int32_t *, int32_t *);
int j2p_position_display(J2pPositionWalk *, const J2pSceneEvent *, const J2pSceneSnapshot *);
int j2p_position_walk(J2pPositionWalk *);
#endif
