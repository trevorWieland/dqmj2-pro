#include "context.h"

/* Interpolate the actor's two position words by the 12-bit fraction the scene
   helper returns, rounding to nearest, and write the scaled pair to the caller's
   vector. */
s32 native_ov000_021e15e0(u8 *actor, u8 *out)
{
    s32 scale = native_fn_0200235c(native_fn_0200285c(out, actor + 0x1E8),
                                   *(s32 *)(actor + 0x200));

    *(s32 *)out = *(s32 *)(actor + 0x1E8)
        + (s32)(((s64)scale * (*(s32 *)(actor + 0x1F4) - *(s32 *)(actor + 0x1E8))
                 + 0x800) >> 12);
    *(s32 *)(out + 8) = *(s32 *)(actor + 0x1F0)
        + (s32)(((s64)scale * (*(s32 *)(actor + 0x1FC) - *(s32 *)(actor + 0x1F0))
                 + 0x800) >> 12);
    return 1;
}
