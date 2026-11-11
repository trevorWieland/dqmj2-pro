#include "../context.h"

/* 0x021f307c: report whether the record qualifies for the shared handler. */
u32 native_ov001_021f307c(u8 *arg0, u32 arg1) {
    u8 *record = native_fn_0207afec(arg1);
    if (arg0[0x31c] != 0 && arg0[0x1ff] != 0) {
        if ((((u32)*(u16 *)(record + 8) << 20) >> 28) == 3 || arg1 == 56 || arg1 == 163) {
            return 1;
        }
    }
    return 0;
}
