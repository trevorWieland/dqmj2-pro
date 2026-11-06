#include "native_arena_types.h"
void native_arm7_wram_037fca58(OSArenaId id)
{
    OSi_GetArenaInfo().hi[id]=native_host_arm7_arm_037fcabc(id);
    OSi_GetArenaInfo().lo[id]=native_host_arm7_arm_037fcb38(id);
}
