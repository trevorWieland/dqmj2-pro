#include "context.h"

/* 0x0221C140 holds a pointer to the ov006 brightness state; the level byte is
   at +0x1A, the same field the fade functions move. */
extern u32 native_data_ov006_0221c140;

extern s32 native_fn_02002480(s32 value, s32 scale);
extern void native_ov006_021ff6ec(u32 value);
extern void native_ov006_021ff700(u32 first, u32 second);

/* ov006 row 0x021FE86C: 100 bytes. Re-fade to a target brightness: take the
   absolute distance between the current +0x1A level and the target, then drive
   two Thumb setters. The first gets 0 for no change, 0x7F for a large distance,
   or the ARM-scaled 0x7F for a small one; the second gets -0x100, 0x100, or the
   ARM-scaled 0x200 minus 0x100. Calls at +0x46 and +0x6E are Thumb; the calls
   at +0x20 and +0x42 target ARM code and are BLX immediates in the image.
   Unknown: why the distance thresholds are 2 and 6, and why the two setters
   work in different ranges. */
void native_ov006_021fe86c(s32 target)
{
    s32 distance = ((u8 *)native_data_ov006_0221c140)[0x1A] - target;
    u32 first;
    u32 second;

    if (distance < 0)
        distance = -distance;

    if (distance < 2)
        first = 0;
    else if (distance < 6)
        first = (u32)native_fn_02002480(0x7F, 6 - distance);
    else
        first = 0x7F;
    native_ov006_021ff6ec(first);

    if (distance < 2)
        second = -0x100;
    else if (distance < 6)
        second = (u32)native_fn_02002480(0x200, 6 - distance) - 0x100;
    else
        second = 0x100;
    native_ov006_021ff700(0xFFFF, second);
}
