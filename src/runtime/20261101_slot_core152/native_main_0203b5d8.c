#include "state.h"

extern u32 native_fn_020388dc(u32);

u32 native_main_0203b5d8(State *state, s32 count, const u8 *slots) {
    u32 mask = 0;
    s32 index;
    index = 0;
    if (count > 0) {
        do {
            state->slots[index] = slots[index];
            mask |= 1U << slots[index];
            index++;
        } while (index < count);
    }
    if (native_fn_020388dc(mask) == 0) {
        return 0;
    }
    state->count = count;
    state->mask = mask;
    return 1;
}
