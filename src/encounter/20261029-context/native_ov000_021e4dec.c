#include "vm_context.h"
extern u32 native_fn_0205bf3c(void);
extern u32 native_fn_02027400(void);
u32 native_ov000_021e4dec(void)
{
    switch (native_fn_0205bf3c()) {
    case 1: {
        u32 mode = native_fn_02027400();
        if (mode == 2)
            return 1;
        if (mode == 4)
            return 2;
        return 3;
    }
    case 2:
        return 4;
    case 5:
        return 6;
    case 3:
        return 7;
    case 4:
        return 8;
    case 6:
        return 9;
    case 7:
        return 10;
    case 8:
        return 11;
    case 9:
        return 12;
    case 10:
        return 13;
    default:
        return 0;
    }
}
