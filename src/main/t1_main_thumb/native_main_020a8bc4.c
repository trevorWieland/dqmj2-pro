#include "context.h"

/*
 * 0x020a8bc4 (42 B, Thumb, p032/2.0-base)
 *
 * Stage eight source bytes in an 8-byte stack block, retag the first byte with
 * `tag`, then hand the block to 0x02090310 together with the caller's first
 * argument. The answer becomes the first argument of 0x020a8b4c with selector
 * -1. The countdown do/while is load-bearing: it is what makes mwcc emit the
 * body before `subs`/`bne` instead of the shorter pre-tested loop.
 *
 * Unknowns: the staging record's layout and both callees' contracts.
 */

extern u32 native_fn_02090310();
extern u32 native_fn_020a8b4c();

void native_main_020a8bc4(u32 argument, u8 *source, u8 tag)
{
    u8 buffer[8];
    u8 *destination = buffer;
    s32 remaining = 8;
    u32 result;

    do {
        *destination++ = *source++;
    } while (--remaining != 0);
    buffer[0] = tag;
    result = native_fn_02090310(argument, buffer);
    native_fn_020a8b4c(result, -1);
}
