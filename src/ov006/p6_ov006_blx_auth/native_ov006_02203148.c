#include "context.h"

/* 0x0221C180 holds the palette handle allocated here. */
extern u32 native_data_ov006_0221c180;

extern u32 native_ov006_02203c08(s32 index, s32 mode);
extern void native_fn_020042e0(u32 reg, s32 value, s32 count);

/* ov006 row 0x02203148: 48 bytes. Allocate palette entry 0x18 in mode 4, save
   the handle, then program the same 0x10-value window into both the main and
   sub engine brightness registers. The call at +0x06 is a Thumb BL into the
   overlay; the calls at +0x14 and +0x22 target ARM code and are BLX immediates
   in the image (01 F6 C0 E8 / 01 F6 BC E8). Unknown: the allocator's argument
   meaning and why both engines get the identical window. */
void native_ov006_02203148(void)
{
    native_data_ov006_0221c180 = native_ov006_02203c08(0x18, 4);
    native_fn_020042e0(0x04000050, 0x3F, 0x10);
    native_fn_020042e0(0x04001050, 0x3F, 0x10);
}
