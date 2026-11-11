#include "context.h"

/* 0x0221C148 holds the main-side renderer/row base pointer; +0x440 is a record
   block copied out of it and +0x4E7 one of its status bytes. The measured code
   reads the base pointer once per access, i.e. the original did not keep a
   local copy across the call. */
extern u32 native_data_ov006_0221c148;

extern void native_fn_02008e0c(void *dst, u8 *src, u32 size);

/* ov006 row 0x021FEE00: 40 bytes. Copy the 0x20-byte record at base+0x440 into
   the caller's buffer and clear the status byte at base+0x4E7. The call at
   +0x0E targets ARM code and is a BLX immediate in the image (09 F6 FE EF).
   Unknown: the record's field layout and what the cleared status byte gates. */
void native_ov006_021fee00(void *dst)
{
    native_fn_02008e0c(dst, (u8 *)native_data_ov006_0221c148 + 0x440, 0x20);
    ((u8 *)native_data_ov006_0221c148)[0x4E7] = 0;
}
