#include "context.h"

/*
 * 0x02092CA8 (16 B, Thumb, p032/2.0-base)
 *
 * Same argument swap and ARM tail call as 0x02092C98, one function later.
 * The two rows differ only in how mwcc spells the moves under this form
 * search; both keep the third argument live so the helper address lands in
 * r3 after the swap.
 *
 * Unknowns: the ARM helper's contract and the third argument's meaning.
 */

extern u32 native_fn_02008e0c();

void native_main_02092ca8(s32 a, s32 b, s32 c)
{
    native_fn_02008e0c(b, a, c);
}
