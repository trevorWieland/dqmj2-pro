#include "context.h"

/*
 * 0x020B5890 (12 B, Thumb, p032/2.0-base)
 *
 * Tag a record and tail-call the Thumb helper 0x020B4108. The helper reads
 * r0 and r1 as its first two arguments and spills r2, so the caller must
 * leave all three of its own arguments live; the constant 0x67 therefore
 * goes to r3 (not r2), and the helper's address is loaded into r3 only
 * after the tag store. A two-argument hypothesis makes mwcc hoist the pool
 * load and reuse r2, which is the 6-byte diff this row used to show.
 *
 * Unknowns: the record layout behind arg1, and what the 0x67 tag means to
 * the 0x020B4108 helper's consumer.
 */

extern u32 native_fn_020b4108();

void native_main_020b5890(s32 a, u8 *p, s32 c)
{
    p[2] = 0x67;
$HOIST
}
