#include "native_arena_types.h"
void *native_arm7_wram_037fca94(OSArenaId id)
{
    return OSi_GetArenaInfo().hi[id];
}
