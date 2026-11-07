#ifndef J2P_STREAM_POSITION_20261107_H
#define J2P_STREAM_POSITION_20261107_H
#include "static_scene_events_20261107.h"

typedef struct { J2pSceneOwner scene; uint32_t stream_id, seed_id, coordinate_generation; } J2pPositionOwner;
typedef struct { J2pPositionOwner owner; uint32_t known_axes; int32_t xyz[3]; } J2pPositionSeed;
typedef struct {
    J2pPositionOwner owner;
    uint32_t sbc_address, sbc_offset, event_ordinal, reference_ordinal, submission_ordinal;
    uint32_t shape_index, shape_address, display_address, display_bytes;
    uint32_t header_offset, opcode_slot, parameter_offset, opcode, vertex_ordinal, submission_vertex_ordinal;
    int32_t xyz[3], position[4];
} J2pPositionRecord;
typedef struct { J2pPositionOwner owner; uint32_t version, records, submitted_lists; } J2pPositionHeader;
typedef struct { J2pPositionRecord *records; uint32_t capacity; } J2pPositionBuffer;

int j2p_stream_positions(J2pGuestSpace *, const J2pSceneOwner *, const J2pPositionSeed *, const J2pSceneTape *,
    const J2pSceneEvent *, const J2pSceneSnapshot *, uint32_t, const J2pPositionBuffer *,
    const J2pPositionBuffer *, J2pPositionHeader *, J2pPositionSeed *);
#endif
