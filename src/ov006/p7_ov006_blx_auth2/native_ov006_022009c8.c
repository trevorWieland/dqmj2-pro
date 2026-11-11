#include "context.h"

/* 0x0221C15C holds a pointer to the ov006 scene state; its byte +0x1A is a
   signed brightness level that is written straight into the master brightness
   register. */
extern u32 native_data_ov006_0221c15c;

extern void native_fn_02004308(u32 reg, s32 value);
extern void native_ov006_02204970(s32 arg, void *callback);
/* The address is taken as data so mwcc keeps the Thumb bit in the relocation
   addend (the image word is 0x02200A05). */
extern u8 native_ov006_02200a04[];

/* ov006 row 0x022009C8: 60 bytes. Raise the scene brightness level by one,
   program the master brightness register with the new level, and hand the
   caller's argument plus the fade-out callback 0x02200A04 to the overlay once
   the level is back at or above zero. The call at +0x16 targets ARM code and is
   a BLX immediate in the image (03 F6 94 EC). Unknown: what the +0x1A level
   counts and what the overlay notify does with the callback; the level is
   re-read from memory after the byte store because the store truncates it to a
   signed byte. */
void native_ov006_022009c8(s32 arg)
{
    ((s8 *)native_data_ov006_0221c15c)[0x1A]++;
    native_fn_02004308(0x04000050, ((s8 *)native_data_ov006_0221c15c)[0x1A]);
    if (((s8 *)native_data_ov006_0221c15c)[0x1A] >= 0)
        native_ov006_02204970(arg, (void *)(native_ov006_02200a04 + 1));
}
