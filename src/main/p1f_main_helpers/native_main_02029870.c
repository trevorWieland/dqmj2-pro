#include "context.h"

extern Vec3 native_data_020edd28;

/* Publish the object's current 0x88 vector into the shared scratch vector and
   replace it with the caller's vector. */
u32 native_main_02029870(u8 *object, const Vec3 *source)
{
    Vec3 *target = (Vec3 *)(object + 0x88);

    native_data_020edd28 = *target;
    *target = *source;
    *(u8 *)(object + 9) = 1;
    return (u32)&native_data_020edd28;
}
