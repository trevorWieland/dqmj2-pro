typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;

typedef struct {
    u8 prefix[0x120];
    u32 references;
} State;

extern u32 native_fn_0203b5d8(State *, s32, const u8 *);

u32 native_main_0203a650(State *state, s32 count, const u8 *slots) {
    if (state->references == 0 && native_fn_0203b5d8(state, count, slots) == 0) {
        return 0;
    }
    state->references += 1;
    return 1;
}
