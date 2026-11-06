#include "native_arena_types.h"
void native_utility_child_arm7_wram_037fcf7c(OSArenaId id,void *next)
{
    OSi_GetArenaInfo().lo[id]=next;
}
