#include "context.h"
u32 native_main_02045c14(u32 arg0) {
    switch (arg0) {
    case 0:
        return *(volatile u16 *)0x04001008 & 3;
    case 1:
        return *(volatile u16 *)0x0400100A & 3;
    case 2:
        return *(volatile u16 *)0x0400100C & 3;
    case 3:
        return *(volatile u16 *)0x0400100E & 3;
    default:
        native_fn_02008430();
        return 0U;
    }
}
