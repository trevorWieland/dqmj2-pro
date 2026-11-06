typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { int x; int y; int z; } SavedPosition;
typedef struct { u8 map; u8 previous; u8 encounter; u8 reserved; u32 time; SavedPosition position; u32 heading; u8 remaining[28]; } SavedWorld;
extern SavedWorld *save_summary_tail_pointer(void);
extern struct { u8 prefix[12]; u8 map; } native_world_runtime;
extern struct { u8 prefix[2]; u8 previous; } native_world_context;
extern SavedPosition *native_player_position_get(int);
extern u32 *native_player_heading_get(int);
u32 native_previous_map_get(void) { return native_world_context.previous; }
u32 saved_runtime_previous_map_exchange(u32 value) {
    u32 previous = native_world_context.previous;
    native_world_context.previous = value;
    return previous;
}
u32 saved_world_time_get(void) { return save_summary_tail_pointer()->time; }
u32 saved_world_time_exchange(u32 value) {
    u32 previous = save_summary_tail_pointer()->time;
    save_summary_tail_pointer()->time = value;
    return previous;
}
u32 saved_world_encounter_exchange(u32 value) {
    u32 previous = save_summary_tail_pointer()->encounter;
    save_summary_tail_pointer()->encounter = value;
    return previous;
}
u32 saved_world_encounter_get(void) { return save_summary_tail_pointer()->encounter; }
void saved_world_time_mode_set(int mode) {
    if (!mode) saved_world_time_exchange(0);
    else saved_world_time_exchange(0x2a30);
}
u8 saved_world_time_threshold(void) { return saved_world_time_get() >= 0x2a30; }
void saved_world_capture(void) {
    SavedWorld *world = save_summary_tail_pointer();
    world->map = native_world_runtime.map;
    world->previous = native_previous_map_get();
    world->position = *native_player_position_get(0);
    world->heading = native_player_heading_get(0)[1];
}
