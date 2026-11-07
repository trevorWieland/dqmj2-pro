#ifndef J2P_STATIC_SCENE_EVENTS_20261107_H
#define J2P_STATIC_SCENE_EVENTS_20261107_H
#include "static_matrix_plan_20261107.h"

typedef struct {
    J2pMatrixOwner model;
    uint32_t model_bytes, instance_id, run_generation, matrix_generation, material_generation, attribute_generation;
} J2pSceneOwner;

typedef struct {
    J2pSceneOwner owner;
    uint32_t provider_flags, shader_valid, material_defaults[3], initial_shader[5];
} J2pSceneSeed;

typedef struct { uint32_t opcode, parameter; } J2pSceneShader;

typedef struct {
    uint32_t offset, ordinal, opcode, length, matrix_begin, matrix_count, shader_begin, shader_count;
    uint32_t flags, node, description, material, material_valid, material_evaluation;
    uint32_t result[6], shader_state[5], cache_valid[2];
    uint32_t shape_reference, shape_index, shape_address, display_address, display_bytes, submission, submission_ordinal;
} J2pSceneEvent;

typedef struct {
    J2pSceneSeed seed;
    J2pStaticMatrixPlan plan;
    uint32_t version, events, shaders, shape_references, submissions, nodes, materials, shapes;
} J2pSceneTape;

typedef struct {
    J2pMatrixCommand *commands;
    uint32_t command_capacity;
    J2pSceneEvent *events;
    uint32_t event_capacity;
    J2pSceneShader *shaders;
    uint32_t shader_capacity;
} J2pSceneBuffers;

typedef struct { J2pMatrixCommand *plan_scratch; uint32_t plan_capacity; J2pSceneBuffers stage; } J2pSceneWork;
typedef struct { J2pSceneOwner owner; J2pMatrixState state; } J2pSceneEntry;

typedef struct {
    J2pSceneOwner owner;
    uint32_t sbc_address, offset, event_ordinal, shape_index, shape_address, display_address, display_bytes;
    uint32_t reference_ordinal, submission_ordinal, submission, material, material_valid, matrix_prefix, mode, valid_slots;
    int32_t matrices[4][16];
} J2pSceneSnapshot;

int j2p_static_scene_tape(J2pGuestSpace *, const J2pSceneOwner *, const J2pSceneSeed *,
    J2pSceneWork *, J2pSceneBuffers *, J2pSceneTape *);
int j2p_static_scene_snapshots(const J2pSceneOwner *, const J2pSceneTape *, const J2pMatrixCommand *,
    const J2pSceneEvent *, const J2pSceneEntry *, J2pSceneSnapshot *, uint32_t,
    J2pSceneSnapshot *, uint32_t, J2pSceneEntry *);
#endif
