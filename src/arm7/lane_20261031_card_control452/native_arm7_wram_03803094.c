#include "native_card_frontier_types.h"
u32 native_arm7_wram_03803094(void)
{
    native_host_arm7_fn_03802f9c(0xb8000000,0);
    *(volatile u32 *)0x040001a4=native_host_arm7_fn_03803070(0x07000000)&~0x1fff;
    while(!(*(volatile u32 *)0x040001a4&0x00800000)) {}
    return *(volatile u32 *)0x04100010;
}
