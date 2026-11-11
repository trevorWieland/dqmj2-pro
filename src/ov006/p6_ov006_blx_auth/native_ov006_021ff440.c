#include "context.h"

/* 0x0221C148 holds the main-side renderer/row base pointer. Each caller index
   selects a 0x100-byte record at base + (index << 8); +0xE7 is its status byte. */
extern u32 native_data_ov006_0221c148;

extern void native_fn_02008d78(void *dst, s32 value, u32 size);
extern void native_ov006_021ff4d8(s32 index);

/* ov006 row 0x021FF440: 40 bytes. Clear the 0xEF-byte payload of record
   `index`, stamp 0xFF into its byte +0xE7, then notify the overlay through
   native_ov006_021FF4D8. The call at +0x10 targets ARM code and is a BLX
   immediate in the image (09 F6 92 EC); the call at +0x1E is a Thumb BL.
   Unknown: what the record at +0xE7 means and what the notification does. */
void native_ov006_021ff440(s32 index)
{
    u32 base = native_data_ov006_0221c148;
    u32 offset = (u32)index << 8;

    native_fn_02008d78((u8 *)(base + offset), 0, 0xEF);
    *((u8 *)(base + offset + 0xE7)) = 0xFF;
    native_ov006_021ff4d8(index);
}
