#include "context.h"

/* 0x0221C1AC holds a pointer to the shared 0x800-byte page block. */
extern u32 native_data_ov006_0221c1ac;

extern void native_fn_02007308(u32 block, s32 size);
extern void native_fn_020049fc(u32 block, s32 value, s32 size);
extern void native_fn_02004a50(u32 block, s32 value, s32 size);

/* ov006 row 0x02204330: 52 bytes. Rebuild the shared page block: reset the
   whole 0x800 bytes, then clear the first 0x400 bytes and the second 0x400
   bytes as two separate ranges. All three calls target ARM code and are BLX
   immediates in the image (02 F6 E6 EF / 00 F6 58 EB / 00 F6 7A EB). Unknown:
   why the whole-block reset is followed by a range clear of exactly the block
   twice, and what the ARM helpers' value argument means. */
void native_ov006_02204330(void)
{
    native_fn_02007308(native_data_ov006_0221c1ac, 0x800);
    native_fn_020049fc(native_data_ov006_0221c1ac, 0, 0x400);
    native_fn_02004a50(native_data_ov006_0221c1ac + 0x400, 0, 0x400);
}
