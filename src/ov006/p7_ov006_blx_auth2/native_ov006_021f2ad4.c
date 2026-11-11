#include "context.h"

/* 0x0220D72C is the ov006 u32 handle table; 0x0221C054 holds the shared
   0xC0-byte destination block. */
extern u32 native_data_ov006_0220d72c[];
extern u32 native_data_ov006_0221c054;

extern u32 native_ov006_021f2798(u32 entry);
extern u32 native_ov006_02202a80(u32 handle, s32 value, s32 size);
extern void native_fn_02008ca4(u32 first, u32 second, s32 size);
extern void native_ov006_02202b24(u32 handle);
extern void native_ov006_0220490c(s32 which, void *callback, s32 arg2, s32 arg3);
/* Address taken as data so mwcc folds the Thumb bit into the relocation. */
extern u8 native_ov006_021f2b3c[];

/* ov006 row 0x021F2AD4: 64 bytes. Resolve one table entry into a handle, carve
   4 bytes out of it, copy the shared 0xC0-byte block into the result, release
   the handle and arm the frame callback 0x021F2B3C with a 0x78-frame budget.
   The call at +0x1C targets ARM code and is a BLX immediate in the image
   (16 F6 D8 E8). Unknown: what the handle table indexes and what the "4" and
   0x78 arguments mean; the copy helper is only known from its three-argument
   shape. */
void native_ov006_021f2ad4(s32 index)
{
    u32 handle = native_ov006_021f2798(native_data_ov006_0220d72c[index]);

    handle = native_ov006_02202a80(handle, 0, 4);
    native_fn_02008ca4(handle, native_data_ov006_0221c054, 0xC0);
    native_ov006_02202b24(handle);
    native_ov006_0220490c(1, (void *)(native_ov006_021f2b3c + 1), 0, 0x78);
}
