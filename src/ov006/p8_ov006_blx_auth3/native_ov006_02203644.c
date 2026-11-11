#include "context.h"

/* 0x0221C184 holds a pointer to the ov006 resource state; the comparison below
   tests one particular record at +0x610 inside the state. */
extern u32 native_data_ov006_0221c184;

extern void native_ov006_0220498c(s32 mode, u32 handle);
extern u32 native_fn_020040ec(void);
extern void native_fn_02008be0(u32 value, u32 address, u32 size);
extern void native_ov006_02203c20(s32 *handle);

/* ov006 row 0x02203644: 76 bytes. Release one resource record: drop the handle
   at +0x2C through the Thumb helper, clear the shared block (0x6000 bytes for
   the record at state+0x610, 0x3000 for every other record), then release the
   handle at +0x28. Calls at +0x08 and +0x40 are Thumb; the calls at +0x1A,
   +0x2C and +0x36 target ARM code and are BLX immediates in the image.
   Unknown: what 0x020040EC returns (its result is the clear destination) and
   why the special record gets twice the cleared length. */
void native_ov006_02203644(u8 *self)
{
    native_ov006_0220498c(1, *(u32 *)(self + 0x2C));
    if ((u32)self == native_data_ov006_0221c184 + 0x610)
        native_fn_02008be0(0, native_fn_020040ec(), 0x6000);
    else
        native_fn_02008be0(0, native_fn_020040ec(), 0x3000);
    native_ov006_02203c20((s32 *)(self + 0x28));
}
