#include "context.h"
u32 native_main_02045b98(u32 arg0) {
    switch (arg0) {
    case 0:
        return *(volatile u16 *)0x04000008 & 3;
    case 1:
        return *(volatile u16 *)0x0400000A & 3;
    case 2:
        return *(volatile u16 *)0x0400000C & 3;
    case 3:
        return *(volatile u16 *)0x0400000E & 3;
    default:
        native_fn_02008430();
        return 0U;
    }
}
