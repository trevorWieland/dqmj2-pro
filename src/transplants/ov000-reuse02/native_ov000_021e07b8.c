typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef struct { u32 words[3]; } RawPosition;
typedef struct { u8 kind; s8 route; u8 previous; u8 bytes3[2]; s8 marker; u8 bytes6[6]; u32 heading; u8 bytes10[8]; u32 clock; u8 bytes1c[8]; RawPosition position; } WorldContext;
typedef struct { u8 bytes0[4]; u8 mode; u8 bytes5[7]; u8 map; } WorldState;
typedef struct { u8 map; u8 prefix[7]; RawPosition position; u32 heading; } SavedWorld;
extern WorldContext native_data_ov000_02232320;
extern WorldState native_world_state;
extern u32 native_previous_map_get(void);
extern u32 native_previous_map_exchange(u32);
extern u8 *native_world_context_get(void);
extern int native_saved_writeback_enabled(void);
extern void native_runtime_blocks_commit(void);
extern void native_world_counter_update(void);
extern u32 native_world_current_map(int);
extern void native_party_derived_refresh(void);
extern void native_reserve_derived_refresh(void);
extern void native_saved_gold_halve(void);
extern SavedWorld *native_saved_world_pointer(void);
extern void native_world_heading_set(u32);
extern void native_world_clock_set(u32);
s8 saved_world_marker_exchange(int value) {
    s8 previous = native_data_ov000_02232320.marker;
    native_data_ov000_02232320.marker = value;
    return previous;
}
s8 saved_world_marker_get(void) { return native_data_ov000_02232320.marker; }
void saved_world_position_set(const RawPosition *position) { native_data_ov000_02232320.position = *position; }
RawPosition *native_ov000_021e07b8(RawPosition *output) {
    if (output) *output = native_data_ov000_02232320.position;
    return &native_data_ov000_02232320.position;
}
u32 saved_world_heading_get(u32 *output) {
    if (output) *output = native_data_ov000_02232320.heading;
    return native_data_ov000_02232320.heading;
}
u32 saved_world_clock_get(u32 *output) {
    if (output) *output = native_data_ov000_02232320.clock;
    return native_data_ov000_02232320.clock;
}
s8 saved_world_route_exchange(int value) {
    s8 previous = native_data_ov000_02232320.route;
    native_data_ov000_02232320.route = value;
    return previous;
}
s8 saved_world_route_get(void) { return native_data_ov000_02232320.route; }
void saved_world_kind_set(int value) { native_data_ov000_02232320.kind = value; }
u32 saved_world_kind_get(void) { return native_data_ov000_02232320.kind; }
void saved_world_transition_apply(void) {
    switch (saved_world_kind_get()) {
    case 1:
        native_world_state.map = native_previous_map_get();
        native_world_state.mode = 0;
        saved_world_marker_exchange(-1);
        if (native_saved_writeback_enabled()) {
            native_runtime_blocks_commit();
            native_world_counter_update();
        }
        break;
    case 10:
        native_world_state.map = native_previous_map_get();
        native_world_state.mode = 0;
        saved_world_marker_exchange(-1);
        break;
    case 11:
        native_world_state.map = native_previous_map_get();
        native_world_state.mode = 0;
        saved_world_marker_exchange(-1);
        ((u8 *)&native_world_state)[1] = 1;
        break;
    case 3:
        if (native_world_context_get()[11] == 1) {
            native_world_state.map = native_previous_map_get();
            native_world_state.mode = 0;
            saved_world_marker_exchange(-1);
        } else {
            native_world_state.map = native_world_current_map(14);
            native_world_state.mode = 3;
            saved_world_marker_exchange(-2);
        }
        native_runtime_blocks_commit();
        native_party_derived_refresh();
        native_reserve_derived_refresh();
        if (!native_world_context_get()[12]) native_saved_gold_halve();
        break;
    case 4:
        {
            SavedWorld *world = native_saved_world_pointer();
            native_world_state.map = world->map;
            native_world_state.mode = 4;
            saved_world_marker_exchange(-1);
            native_previous_map_exchange(world->map);
            saved_world_position_set(&world->position);
            native_world_heading_set(world->heading);
            native_world_clock_set(world->heading + 0xb4000);
        }
        break;
    case 5:
    case 7:
    case 8:
        native_world_state.map = native_previous_map_get();
        native_world_state.mode = 0;
        break;
    default:
        native_world_state.mode = saved_world_route_get();
        break;
    }
}
