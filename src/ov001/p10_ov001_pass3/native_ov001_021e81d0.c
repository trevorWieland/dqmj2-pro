#include "context.h"

/* native_ov001_021e81d0.c: 32 bytes at 0x021e81d0 in ov001.
 * s32 func(s32 wide, s32 index): pick the 6-byte-record table by flag and
 * index it.  Returning from each arm is what orders the equal load first. */
s32 native_ov001_021e81d0(s32 wide, s32 index)
{
    return wide == 0
        ? (s32)native_data_ov001_02238d1c + index * 6
        : (s32)native_data_ov001_02238d2e + index * 6;
}
