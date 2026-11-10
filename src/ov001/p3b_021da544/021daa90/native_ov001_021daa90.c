#include "../context.h"

/* Scans the 60-entry signed-byte key pair lists at `a` and `b` and reports
   whether 0x022094bc maps any live entry to `value`.  An entry with a zero byte
   in list `a` is skipped; the first match stops the scan. */
u32 native_ov001_021daa90(u8 *a, u8 *b, u32 value) {
    s32 i;
    u32 result;
    u32 left;
    u32 right;

    result = 0;
    i = 0;
    do {
        left = *(s8 *)(a + i);
        if (left != 0) {
            right = *(s8 *)(b + i);
            if (value == native_fn_022094bc(i, left, right)) {
                result = 1;
                break;
            }
        }
        i++;
    } while (i < 60);
    return result;
}


