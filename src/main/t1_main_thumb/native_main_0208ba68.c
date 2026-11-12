#include "context.h"

/*
 * 0x0208ba68 (56 B, Thumb, p032/2.0-base)
 *
 * Retire the 0x021cfea0 record pair. The first arm calls the ARM helper
 * 0x02007ff4 and keeps its answer in r4; the second arm calls the ARM helper
 * 0x020068c0 with the 0x021cfea0 block and keeps the answer in r5. When that
 * answer is zero and 0x021cfcf8+0x44 is still clear, the flag is set and the
 * ARM helper 0x0200698c is handed the same block. Whichever path ran, r4 goes
 * through 0x02008008 and r5 is the result.
 *
 * Unknowns: the ownership of the 0x021cfcf8 block and why the 0x021cfea0
 * descriptor is passed as a value rather than dereferenced; the callees'
 * contracts beyond their measured call sites.
 */

extern u32 native_fn_020068c0();
extern u32 native_fn_0200698c();
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u8 native_data_021cfcf8[];
extern u8 native_data_021cfea0[];

u32 native_main_0208ba68(void)
{
    u32 saved_r4;
    u32 saved_r5;

    saved_r4 = native_fn_02007ff4();
    saved_r5 = native_fn_020068c0(native_data_021cfea0);
    if (saved_r5 == 0 && M2C_FIELD(native_data_021cfcf8, s32 *, 0x44) == 0) {
        M2C_FIELD(native_data_021cfcf8, s32 *, 0x44) = 1;
        native_fn_0200698c(native_data_021cfea0);
    }
    native_fn_02008008(saved_r4);
    return saved_r5;
}
