#include "context.h"
u32 native_main_020640f0(u32 includeSecondary)
{
    PartyState *state = partyState();
    u8 counts[9];
    s32 i;
    native_fn_02008d78(counts, 0, sizeof(counts));
    for (i = 0; i < 3; ++i) counts[native_fn_020640b4(state->primary1c[i])]++;
    if (includeSecondary) {
        for (i = 0; i < 3; ++i) counts[native_fn_020640b4(state->secondary28[i])]++;
    }
    for (i = 1; i < 9; ++i) if (counts[i] > 1) return 1;
    return 0;
}
