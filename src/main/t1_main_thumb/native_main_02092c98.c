#include "context.h"

/*
 * 0x02092C98 (16 B, Thumb, p032/2.0-base)
 *
 * Swap the first two arguments and tail-call the ARM helper 0x02008E0C,
 * passing the caller's third argument through untouched. The live r2 is
 * what keeps the pool load after the two moves (mwcc loads the helper
 * address into r3 last); a two-argument hypothesis hoists the load and
 * costs six bytes.
 *
 * Unknowns: the ARM helper's contract beyond its measured call sites, and
 * the meaning of the third argument.
 */

extern u32 native_fn_02008e0c();

void native_main_02092c98(s32 a, s32 b, s32 c)
{
    native_fn_02008e0c(b, a, c);
}
