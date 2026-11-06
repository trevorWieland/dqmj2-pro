#include "context_00.h"
void * native_main_02007560 (OSArenaId id)
{
    ((void) 0) ;
    ((void) 0) ;
    switch (id) {
    case OS_ARENA_MAIN:
        return (void *)(0x02000000 + 0x3E0000) ;
    case OS_ARENA_MAINEX:
        if (!native_data_main_020e363c.field_0004 ||
            ((native_fn_02006de4() & 0x00000003 ) == 0x00000001 )) {
            return (void *)0;
        } else {
            return (void *)(0x02000000 + 0x700000) ;
        }
    case OS_ARENA_ITCM:
        return (void *)(0x01ff8000 + 0x8000) ;
    case OS_ARENA_DTCM:
    {
        u32 irqStackLo;
        u32 sysStackLo;
        irqStackLo = (u32)(((((u32)native_data_main_027e0000) + 0x00003fc0) - 0x40)) - ((int)native_data_main_00001000) ;
        if (((int)native_data_main_00001000) == 0) {
            sysStackLo = ((u32)native_data_main_027e0000) ;
            if (sysStackLo < ((u32)native_data_main_027e0080) ) {
                sysStackLo = ((u32)native_data_main_027e0080) ;
            }
        } else if (((int)native_data_main_00001000) < 0)   {
            sysStackLo = ((u32)native_data_main_027e0080) - ((int)native_data_main_00001000) ;
        } else {
            sysStackLo = irqStackLo - ((int)native_data_main_00001000) ;
        }
        ((void) 0) ;
        return (void *)sysStackLo;
    }
    case OS_ARENA_SHARED:
        return (void *)((0x02000000 + 0x007ff800) - 0x160 - 0x20) ;
    case OS_ARENA_WRAM_MAIN:
        return (void *)(void *)0x037f8000 ;
    default:
        ((void) 0) ;
    }
    return ((void *)0) ;
}
