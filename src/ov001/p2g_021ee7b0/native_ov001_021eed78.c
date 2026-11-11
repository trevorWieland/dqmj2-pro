#include "context.h"

/* Scale the record's three fixed-point words by the caller's factor (12-bit
   fraction), rounding to nearest. Reports whether a record was found. */
s32 native_ov001_021eed78(s32 unused, s32 scale)
{
    u8 *record = native_fn_0205d750();
    u32 value;

    if (record == 0)
        return 0;
    value = (u32)(((s64)*(s32 *)(record + 0x90) * scale + 0x800) >> 12);
    *(u32 *)(record + 0x90) = value;
    *(u32 *)(record + 0x94) = value;
    *(u32 *)(record + 0x98) = value;
    return 1;
}
