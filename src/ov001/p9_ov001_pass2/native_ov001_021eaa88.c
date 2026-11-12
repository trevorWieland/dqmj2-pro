#include "context.h"

/*
 * native_ov001_021eaa88.c: 56 bytes at 0x021eaa88 in ov001 (base 0x021d7240).
 *
 * s32 func(void)
 *
 * Early-out latch: when the session-open byte at 0x0222ec84 is clear this
 * returns 0 without touching anything.  Otherwise it runs the teardown and
 * marks the record at 0x02238d7c (+0x27) released.
 */
extern u8 native_data_ov001_0222ec84[];
extern u8 native_data_ov001_02238d7c[];
extern void native_fn_ov001_021f14a4(void);

s32 native_ov001_021eaa88(void)
{
    s32 result = 0;

    if (native_data_ov001_0222ec84[0] != 0) {
        native_fn_ov001_021f14a4();
        *(s8 *)(native_data_ov001_02238d7c + 0x27) = -1;
        result = 1;
    }
    return result;
}
