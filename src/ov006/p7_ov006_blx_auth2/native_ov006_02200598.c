#include "context.h"

/* 0x0221C15C holds a pointer to the ov006 scene state; its byte +0x1A is the
   signed brightness level. */
extern u32 native_data_ov006_0221c15c;

extern void native_fn_02004308(u32 reg, s32 value);
extern void native_ov006_02204970(s32 arg, void *callback);
/* Address taken as data so mwcc folds the Thumb bit into the relocation. */
extern u8 native_ov006_022005d8[];

/* ov006 row 0x02200598: 64 bytes. Lower the scene brightness level by one,
   program the master brightness register with the new level, and once the
   level has reached -12 hand the caller's argument plus the fade-in callback
   0x022005D8 to the overlay. The call at +0x16 targets ARM code and is a BLX
   immediate in the image (03 F6 AC EE). Unknown: why the hand-off threshold is
   exactly -12 (the compiler builds it as 0x1A-0x26), and what the overlay does
   with the callback. */
void native_ov006_02200598(s32 arg)
{
    ((s8 *)native_data_ov006_0221c15c)[0x1A]--;
    native_fn_02004308(0x04000050, ((s8 *)native_data_ov006_0221c15c)[0x1A]);
    if (((s8 *)native_data_ov006_0221c15c)[0x1A] <= -12)
        native_ov006_02204970(arg, (void *)(native_ov006_022005d8 + 1));
}
