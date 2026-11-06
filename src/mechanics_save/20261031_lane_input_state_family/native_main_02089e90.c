#include "family.h"
extern u32 native_fn_02007ff4(void);
extern u32 native_fn_02008008(u32);
extern void native_fn_0208a5ac(u32);
u32 native_main_02089e90(void) {
    u32 irq=native_fn_02007ff4();
    if (!native_data_021cfcb4) {
        native_fn_02008008(irq);
        return 1;
    }
    switch (FIELD(native_data_021cfcb4,u32,0x2260)) {
    case 6:
        native_fn_0208a5ac(7);
        FIELD(native_data_021cfcb4,u16,0x2280)=4;
        break;
    case 7:
        native_fn_02008008(irq);
        return 2;
    case 3:
        native_fn_02008008(irq);
        return 0;
    default:
        native_fn_02008008(irq);
        return 1;
    }
    native_fn_02008008(irq);
    return 3;
}
