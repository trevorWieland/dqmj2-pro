#include "context.h"
s32 native_main_02066f84(const WeightedGroup *group, s32 required)
{
    s32 result = -1;
    s32 available = group->high - group->low + 1;
    if (available > 0) available = native_fn_0203d294((u32)available);
    if (required <= available + group->low) {
        s32 total = 0;
        s32 i;
        for (i = 0; i < 5; ++i) total += group->weights[i];
        if (total > 0) {
            s32 running = 0;
            s32 random = native_fn_0203d294((u32)total);
            for (i = 0; i < 5; ++i) {
                running += group->weights[i];
                if (random < running) {
                    result = (s8)i;
                    break;
                }
            }
        }
    }
    return result;
}
