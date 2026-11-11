#include "context.h"

extern u32 native_fn_02029688(u8 *object);

/* Program the object's visible-time pair (current and complement of the
   0x1000 window), latch it and release the slot when the window is zero. */
u32 native_main_02029710(u8 *object, s32 value)
{
    u32 result = 0;

    if (value >= 0x1000)
        value = 0x1000;
    if (value <= 0)
        value = 0;
    *(u32 *)(*(u32 *)(object + 0x64) + 4) = (u32)value;
    *(u32 *)(*(u32 *)(object + 0x60) + 4) = (u32)(0x1000 - value);
    *(u32 *)(object + 0xf8) = (u32)value;
    if (value <= 0) {
        native_fn_02029688(object);
        result = 1;
    }
    return result;
}
