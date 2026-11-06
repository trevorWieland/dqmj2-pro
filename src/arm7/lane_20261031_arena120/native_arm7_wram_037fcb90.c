#include "native_arena_types.h"
void native_arm7_wram_037fcb90(OSArenaId id,void *next)
{
    OSi_GetArenaInfo().lo[id]=next;
}
