#include "../context.h"

/* 0x021f3470: map the mode selector onto the two accepted state groups. */
u32 native_ov001_021f3470(s32 arg0) {
    if (arg0 < 0) {
        arg0 = (s32)native_fn_ov001_021d767c();
    }
    switch (arg0) {
    case 16:
    case 17:
    case 18:
    case 23:
    case 24:
    case 25:
        return 1;
    default:
        return 0;
    }
}
