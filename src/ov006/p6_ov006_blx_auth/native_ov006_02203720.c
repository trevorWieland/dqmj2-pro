#include "context.h"

/* 0x0221C184 holds the pointer to the eight-byte row table used below. */
extern u32 native_data_ov006_0221c184;

extern void native_fn_020361f8(s32 arg1, u8 *row, s32 arg2, s32 arg3, s32 arg4, u16 arg5);

/* ov006 row 0x02203720: 44 bytes. Forward the first five arguments unchanged
   except that the second argument is replaced by table + (arg6 << 3), i.e. the
   sixth caller argument selects an eight-byte row; the fifth argument is a
   halfword fetched from the caller's stack. The call at +0x1E targets ARM code
   and is a BLX immediate in the image (32 F6 5C ED). Unknown: the row layout and
   the callee's real argument names; the halfword argument's width is measured. */
void native_ov006_02203720(s32 arg1, s32 arg2, s32 arg3, s32 arg4, u16 arg5, s32 arg6)
{
    native_fn_020361f8(arg1, (u8 *)native_data_ov006_0221c184 + ((u32)arg6 << 3),
                       arg2, arg3, arg4, arg5);
}
