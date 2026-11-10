#include "context.h"

/* Program the sound effect the four-part descriptor names. */
void native_ov006_021e796c(s32 slot, s32 arg1, s32 arg2, s32 arg3)
{
    u8 active = slot < 0x24;

    native_fn_ov006_022078bc((s8)slot, active, arg1, (s16)arg2, (s16)arg3);
}
