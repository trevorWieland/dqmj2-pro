#include "native_arena_types.h"
void *native_utility_child_arm7_wram_037fd07c(OSArenaId id)
{
    return OSi_GetArenaInfo().lo[id];
}
