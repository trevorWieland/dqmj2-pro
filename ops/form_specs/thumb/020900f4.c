#include "context.h"

/*
 * 0x020900F4 (68 B, Thumb, p032/2.0-base)
 *
 * Latch a pending transition. While 0x021CFD48 is clear, a 0x021D1548 value
 * whose low two bits are 1 triggers a 0x02008058 probe; unless the probe
 * returns 0x12 the 0x02006B7C helper is called with 0xA. Once 0x021CFD48 is
 * set, it is copied into 0x021D1544 exactly once. The function returns the
 * latch in all cases.
 *
 * Unknowns: what the 0xA event and the 0x12 probe answer mean, and which
 * subsystem owns the two globals.
 */

extern u32 native_fn_02006b7c();
extern u32 native_fn_02008058();
extern u32 native_data_021cfd48;
extern u32 native_data_021d1544;
extern u32 native_data_021d1548;

s32 native_main_020900f4(void)
{
    if (native_data_021cfd48 == 0) {
        if ((native_data_021d1548 & 3) == 1 && native_fn_02008058() != 0x12)
            native_fn_02006b7c(0xA);
    } else if (native_data_021d1544 == 0) {
        native_data_021d1544 = native_data_021cfd48;
    }
    return native_data_021cfd48;
}
