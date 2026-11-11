#include "context.h"

/* 0x0221C054 holds the pointer to a 0xC0-byte work buffer shared with the
   main-module helpers below. */
extern u32 native_data_ov006_0221c054;

extern void native_fn_02007308(void *buffer, u32 size);
extern void native_fn_02004c18(void *buffer, s32 value, u32 size);
extern void native_ov006_02204974(s32 mode, s32 arg);

/* ov006 row 0x021F2B3C: 40 bytes. Release/clear the shared 0xC0-byte buffer
   (first a teardown call, then a memset-style clear) and dispatch mode 1 with
   the caller's argument. The calls at +0x0A and +0x16 target ARM code and are
   BLX immediates in the image (14 F6 E0 EB / 12 F6 62 E8); the call at +0x1E is
   a Thumb BL into the overlay. Unknown: the two ARM callees' names and what
   native_ov006_02204974 does with the buffer afterwards. */
void native_ov006_021f2b3c(s32 arg)
{
    native_fn_02007308((void *)native_data_ov006_0221c054, 0xC0);
    native_fn_02004c18((void *)native_data_ov006_0221c054, 0, 0xC0);
    native_ov006_02204974(1, arg);
}
