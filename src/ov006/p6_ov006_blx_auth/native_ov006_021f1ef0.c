#include "context.h"

/* Main-module ARM helper that returns a 64-bit value in r0:r1 (ARM EABI). Its
   identity is unknown; only the call shape is measured here. */
extern u64 native_fn_02007a9c(void);

/* Main-module ARM helper taking a 64-bit mantissa split across r0/r1 plus two
   selector words. */
extern u32 native_fn_020260dc(u32 low, u32 high, u32 selector, u32 zero);

/* ov006 row 0x021F1EF0: 28 bytes. Take the 64-bit value returned by
   native_fn_02007a9c, shift it left by six and hand the two halves to
   native_fn_020260dc with a fixed 0x82EA selector and a zero fourth word.
   The low half becomes value << 6; the high half takes the six bits shifted out
   of the low half. Both calls at +0x02 and +0x12 target ARM code and are BLX
   immediates in the image (15 F6 D4 ED / 34 F6 EC E8). Unknown: both callees'
   semantics and the meaning of the 0x82EA selector. */
u32 native_ov006_021f1ef0(void)
{
    u64 value = native_fn_02007a9c();

    return native_fn_020260dc((u32)(value << 6),
                              (u32)(value >> 32) << 6 | (u32)value >> 26,
                              0x82EA, 0);
}
