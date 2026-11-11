#include "context.h"

/* 0x0221C188 holds the main-side slot pointer; the allocator below writes
   through it. */
extern u32 native_data_ov006_0221c188;

extern s32 native_fn_02005d50(s32 lock);
extern void native_fn_02005d20(s32 key);
extern s32 native_fn_0202b334(u32 slot, s32 a, s32 b);
extern void native_fn_02008430(void);

/* ov006 row 0x02203BD8: 48 bytes. Under the shared lock, allocate with two
   caller-supplied arguments, run the out-of-memory helper on a zero result,
   release the lock and return the allocation result. Calls at +0x08 and +0x24
   target ARM code and are BLX immediates in the image (02 F6 B6 E8 / 02 F6 90
   E8); the allocation call at +0x16 is a BLX immediate (27 F6 A2 EB) and the
   failure call at +0x1E is a BLX immediate too (04 F6 1C EC). Unknown: the
   allocation's argument meaning. */
s32 native_ov006_02203bd8(s32 arg1, s32 arg2)
{
    s32 key = native_fn_02005d50(1);
    s32 result = native_fn_0202b334(native_data_ov006_0221c188, arg1, arg2);

    if (result == 0)
        native_fn_02008430();
    native_fn_02005d20(key);
    return result;
}
