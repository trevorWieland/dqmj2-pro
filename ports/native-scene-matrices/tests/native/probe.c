#include "stream_position_20261107.h"
#include "billboard_warm_20261107.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int32_t xyz[3], position[4]; uint32_t ids[9]; } ExpectedPosition;
typedef struct {
    const uint8_t *source; uint32_t bytes, known; int32_t xyz[3];
    const ExpectedPosition *records; uint32_t count; int32_t final_xyz[3]; uint32_t final_known;
} PositionFixture;
typedef struct { uint32_t valid_slots; int32_t matrices[4][16]; } ExpectedSnapshot;
typedef struct {
    const uint8_t *source; uint32_t bytes, defaults[3]; const uint32_t (*events)[6]; uint32_t event_count;
    const ExpectedSnapshot *snapshots; uint32_t snapshot_count;
} SceneFixture;
typedef struct { const uint8_t *owner, *context, *entry, *output, *effect; } WarmFixture;
#include "fixtures.h"

static uint32_t total_positions, total_references, total_submissions, refusals;
static int failed(int line) { fprintf(stderr, "C7_ROMFREE_PROBE_FAIL line=%d\n", line); return 0; }
#define CHECK(x) do { if (!(x)) return failed(__LINE__); } while (0)

static void *allocate(uint32_t n, size_t size) {
    void *p = calloc(n ? n : 1, size);
    if (!p) { fputs("C7_ROMFREE_PROBE_FAIL allocation\n", stderr); exit(2); }
    return p;
}

typedef struct {
    J2pGuestSpace space; J2pSceneOwner owner; J2pSceneSeed seed; J2pSceneTape tape;
    J2pSceneBuffers stage, output; J2pSceneWork work;
    J2pSceneEntry entry, final; J2pSceneSnapshot *temporary, *snapshots;
    uint8_t *raw; const uint8_t *source; uint32_t bytes, snapshot_capacity;
} Pipeline;

static int open_pipeline(Pipeline *p, const uint8_t *source, uint32_t bytes, const uint32_t defaults[3]) {
    J2pMatrixSeed matrix = {0}; uint32_t i, j, c, e, s;
    memset(p, 0, sizeof(*p)); p->raw = allocate(bytes + 2, 1); p->source = source; p->bytes = bytes;
    p->raw[0] = p->raw[bytes + 1] = 0xa5; memcpy(p->raw + 1, source, bytes);
    p->owner.model = (J2pMatrixOwner){{0, 9, 1, 1}, 0x02700000, 0};
    p->owner.model_bytes = bytes; p->owner.instance_id = 1; p->owner.run_generation = 2;
    p->owner.matrix_generation = 3; p->owner.material_generation = 4; p->owner.attribute_generation = 5;
    CHECK(j2p_guest_map(&p->space, p->owner.model.scope, 0x02700000, p->raw + 1, bytes) == 1);
    p->seed.owner = p->owner; p->seed.shader_valid = 31;
    memcpy(p->seed.material_defaults, defaults, sizeof(p->seed.material_defaults));
    p->seed.initial_shader[0] = 0x1234; p->seed.initial_shader[1] = 0x5678; p->seed.initial_shader[2] = 0x1f00c0;
    CHECK(j2p_static_scene_tape(&p->space, &p->owner, &p->seed, NULL, NULL, &p->tape) == 1);
    c = p->tape.plan.command_count ? p->tape.plan.command_count : 1;
    e = p->tape.events ? p->tape.events : 1; s = p->tape.shaders ? p->tape.shaders : 1;
    CHECK(c <= 10000 && e <= 1000 && s <= 1000);
    p->stage = (J2pSceneBuffers){allocate(c, sizeof(J2pMatrixCommand)), c, allocate(e, sizeof(J2pSceneEvent)), e, allocate(s, sizeof(J2pSceneShader)), s};
    p->output = (J2pSceneBuffers){allocate(c, sizeof(J2pMatrixCommand)), c, allocate(e, sizeof(J2pSceneEvent)), e, allocate(s, sizeof(J2pSceneShader)), s};
    p->work = (J2pSceneWork){allocate(c, sizeof(J2pMatrixCommand)), c, p->stage};
    CHECK(j2p_static_scene_tape(&p->space, &p->owner, &p->seed, &p->work, &p->output, &p->tape) == 1);
    p->entry.owner = p->owner; matrix.owner = p->owner.model; matrix.mode = 2;
    for (i = 0; i < 4; ++i) for (j = 0; j < 16; ++j) matrix.matrices[i][j] = j % 5 == 0 ? 4096 : 0;
    CHECK(j2p_matrix_init(&p->owner.model, &matrix, &p->entry.state) == 1);
    p->snapshot_capacity = p->tape.shape_references ? p->tape.shape_references : 1;
    CHECK(p->snapshot_capacity <= 1000);
    p->temporary = allocate(p->snapshot_capacity, sizeof(*p->temporary));
    p->snapshots = allocate(p->snapshot_capacity, sizeof(*p->snapshots));
    CHECK(j2p_static_scene_snapshots(&p->owner, &p->tape, p->output.commands, p->output.events, &p->entry,
        p->temporary, p->snapshot_capacity, p->snapshots, p->snapshot_capacity, &p->final) == 1);
    return 1;
}

static int close_pipeline(Pipeline *p) {
    CHECK(p->raw[0] == 0xa5 && p->raw[p->bytes + 1] == 0xa5 && !memcmp(p->raw + 1, p->source, p->bytes));
    free(p->stage.commands); free(p->stage.events); free(p->stage.shaders);
    free(p->output.commands); free(p->output.events); free(p->output.shaders);
    free(p->work.plan_scratch); free(p->temporary); free(p->snapshots); free(p->raw);
    return 1;
}

static int scene_case(const SceneFixture *f) {
    Pipeline p; uint32_t i;
    CHECK(open_pipeline(&p, f->source, f->bytes, f->defaults));
    CHECK(p.tape.events == f->event_count && p.tape.shape_references == f->snapshot_count);
    for (i = 0; i < f->event_count; ++i) {
        J2pSceneEvent *e = &p.output.events[i];
        uint32_t values[] = {e->offset, e->opcode, e->flags, e->material, e->material_valid, e->submission};
        CHECK(!memcmp(values, f->events[i], sizeof(values)));
    }
    for (i = 0; i < f->snapshot_count; ++i) {
        CHECK(p.snapshots[i].mode == 2 && p.snapshots[i].valid_slots == f->snapshots[i].valid_slots);
        CHECK(!memcmp(p.snapshots[i].matrices, f->snapshots[i].matrices, sizeof(f->snapshots[i].matrices)));
    }
    total_references += p.tape.shape_references; total_submissions += p.tape.submissions;
    CHECK(close_pipeline(&p)); return 1;
}

static int position_case(const PositionFixture *f) {
    const uint32_t defaults[] = {0, 0, 0x1f00c0};
    Pipeline p; J2pPositionSeed seed = {0}, final = {0}, saved_final; J2pPositionHeader header = {0}, saved_header;
    J2pPositionBuffer stage, output; uint32_t n, i; size_t amount; uint8_t *saved;
    CHECK(open_pipeline(&p, f->source, f->bytes, defaults));
    seed.owner = (J2pPositionOwner){p.owner, 17, 23, 29}; seed.known_axes = f->known;
    memcpy(seed.xyz, f->xyz, sizeof(seed.xyz));
    CHECK(j2p_stream_positions(&p.space, &p.owner, &seed, &p.tape, p.output.events, p.snapshots,
        p.tape.shape_references, NULL, NULL, &header, NULL) == 1);
    CHECK(header.records == f->count); n = header.records ? header.records : 1;
    stage = (J2pPositionBuffer){allocate(n, sizeof(J2pPositionRecord)), n};
    output = (J2pPositionBuffer){allocate(n, sizeof(J2pPositionRecord)), n};
    CHECK(j2p_stream_positions(&p.space, &p.owner, &seed, &p.tape, p.output.events, p.snapshots,
        p.tape.shape_references, &stage, &output, &header, &final) == 1);
    for (i = 0; i < header.records; ++i) {
        J2pPositionRecord *r = &output.records[i];
        uint32_t ids[] = {r->event_ordinal, r->reference_ordinal, r->submission_ordinal, r->header_offset,
            r->opcode_slot, r->parameter_offset, r->opcode, r->vertex_ordinal, r->submission_vertex_ordinal};
        CHECK(!memcmp(r->xyz, f->records[i].xyz, sizeof(r->xyz)));
        CHECK(!memcmp(r->position, f->records[i].position, sizeof(r->position)));
        CHECK(!memcmp(ids, f->records[i].ids, sizeof(ids)));
        CHECK(!memcmp(&r->owner, &seed.owner, sizeof(seed.owner)));
    }
    CHECK(!memcmp(final.xyz, f->final_xyz, sizeof(final.xyz)) && final.known_axes == f->final_known);
    amount = n * sizeof(J2pPositionRecord); saved = allocate(2, amount);
    memcpy(saved, stage.records, amount); memcpy(saved + amount, output.records, amount); saved_final = final; saved_header = header;
    p.tape.seed.provider_flags = 1;
    CHECK(j2p_stream_positions(&p.space, &p.owner, &seed, &p.tape, p.output.events, p.snapshots,
        p.tape.shape_references, &stage, &output, &header, &final) == -2);
    p.tape.seed.provider_flags = 0; ++refusals; ++seed.owner.scene.model.scope.generation;
    CHECK(j2p_stream_positions(&p.space, &p.owner, &seed, &p.tape, p.output.events, p.snapshots,
        p.tape.shape_references, &stage, &output, &header, &final) == -1);
    --seed.owner.scene.model.scope.generation; ++refusals;
    if (f->count) {
        J2pPositionRecord *retained = output.records;
        output.capacity = f->count - 1;
        if (!output.capacity) output.records = NULL;
        CHECK(j2p_stream_positions(&p.space, &p.owner, &seed, &p.tape, p.output.events, p.snapshots,
            p.tape.shape_references, &stage, &output, &header, &final) == -5);
        output.records = retained; output.capacity = n;
        ++refusals;
    }
    CHECK(!memcmp(saved, stage.records, amount) && !memcmp(saved + amount, output.records, amount));
    CHECK(!memcmp(&saved_final, &final, sizeof(final)) && !memcmp(&saved_header, &header, sizeof(header)));
    total_positions += f->count; free(saved); free(stage.records); free(output.records);
    CHECK(close_pipeline(&p)); return 1;
}

static int warm_case(const WarmFixture *f) {
    J2pBb7Owner owner; J2pBb7WarmContext context; J2pBb7State entry, output, saved_output; J2pBb7Effect effect, saved_effect;
    _Static_assert(sizeof(owner) == 60 && sizeof(context) == 176 && sizeof(entry) == 4540 && sizeof(effect) == 732, "Public fixed-width warm layout");
    memcpy(&owner, f->owner, sizeof(owner)); memcpy(&context, f->context, sizeof(context)); memcpy(&entry, f->entry, sizeof(entry));
    memset(&output, 0xa5, sizeof(output)); memset(&effect, 0x5a, sizeof(effect));
    CHECK(j2p_billboard_warm(&owner, &context, &entry, &output, &effect) == 1);
    CHECK(!memcmp(&output, f->output, sizeof(output)) && !memcmp(&effect, f->effect, sizeof(effect)));
    saved_output = output; saved_effect = effect; context.provider_flags = 1;
    CHECK(j2p_billboard_warm(&owner, &context, &entry, &output, &effect) == -2); ++refusals;
    context.provider_flags = 0; ++context.owner.cache_generation;
    CHECK(j2p_billboard_warm(&owner, &context, &entry, &output, &effect) == -1); ++refusals;
    CHECK(!memcmp(&output, &saved_output, sizeof(output)) && !memcmp(&effect, &saved_effect, sizeof(effect)));
    CHECK(!memcmp(&owner, f->owner, sizeof(owner)) && !memcmp(&entry, f->entry, sizeof(entry))); return 1;
}

int main(void) {
    uint32_t i;
    for (i = 0; i < sizeof(scene_fixtures) / sizeof(scene_fixtures[0]); ++i) if (!scene_case(&scene_fixtures[i])) return 1;
    for (i = 0; i < sizeof(position_fixtures) / sizeof(position_fixtures[0]); ++i) if (!position_case(&position_fixtures[i])) return 1;
    for (i = 0; i < sizeof(warm_fixtures) / sizeof(warm_fixtures[0]); ++i) if (!warm_case(&warm_fixtures[i])) return 1;
    printf("{\"status\":\"C7_ROMFREE_PROBE_PASS\",\"sceneModels\":8,\"positionModels\":8,\"positionRecords\":%u,"
        "\"sceneReferences\":%u,\"sceneSubmissions\":%u,\"warmCases\":4,\"refusals\":%u,\"romInputs\":false,\"renderer\":false}\n",
        total_positions, total_references, total_submissions, refusals);
    return 0;
}
