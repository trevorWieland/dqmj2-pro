#include "native_arena_types.h"
void *native_arm7_wram_037fcaa8(OSArenaId id)
{
    return OSi_GetArenaInfo().lo[id];
}
