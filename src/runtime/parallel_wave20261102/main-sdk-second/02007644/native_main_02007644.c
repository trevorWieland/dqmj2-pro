#include "context_00.h"
void * native_main_02007644 (OSArenaId id)
{
    ((void) 0) ;
    ((void) 0) ;
    switch (id) {
    case OS_ARENA_MAIN:
        return (void *)((u32)native_data_main_02249aa0) ;
    case OS_ARENA_MAINEX:
        if (!native_data_main_020e363c.field_0004 ||
            ((native_fn_02006de4() & 0x00000003 ) == 0x00000001 )) {
            return (void *)0;
        } else {
            return (void *)((u32)native_data_main_023e0000) ;
        }
    case OS_ARENA_ITCM:
        return (void *)((u32)native_data_main_01fffbc0) ;
    case OS_ARENA_DTCM:
        return (void *)((u32)native_data_main_027e0080) ;
    case OS_ARENA_SHARED:
        return (void *)((0x02000000 + 0x00800000) - 0x001000) ;
    case OS_ARENA_WRAM_MAIN:
        return (void *)0x037f8000 ;
    default:
        ((void) 0) ;
    }
    return ((void *)0) ;
}
