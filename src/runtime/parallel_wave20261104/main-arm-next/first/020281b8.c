#include "context.h"
s32 native_main_020281b8(const Vec3 *value)
{
    u64 total = (u64)((s64)value->x * value->x) + (u64)((s64)value->y * value->y) + (u64)((s64)value->z * value->z);
    return native_fn_0200236c((s32)(total >> 12));
}
