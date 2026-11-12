#include "context.h"

/*
 * 0x020A2CF0 (64 B, Thumb, p032/2.0-base)
 *
 * Reset and re-time the 0x021D1B88 state block. The block pointer is stored
 * in a global word, and the image reloads that word before every field write,
 * so the source spells the dereference out each time instead of caching it.
 * The block's +8/+0xC words and +2 byte are cleared, the +0x18 counter is
 * stamped from 0x02007A9C, and when the caller passes zero the +0x10 counter
 * is stamped as well.
 *
 * Unknowns: the 64-bit tick/ID returned by 0x02007A9C and the block's owner.
 */

extern s64 native_fn_02007a9c();
extern u32 native_data_021d1b88;

typedef struct {
    u8 f0;
    u8 f1;
    u8 f2;
    u8 pad;
    u32 f4;
    u32 f8;
    u32 fc;
    u64 f10;
    u64 f18;
} StateView;

#define STATE (*(StateView **)&native_data_021d1b88)

void native_main_020a2cf0(u32 arg0)
{
    if (STATE == 0 || STATE->f0 == 0)
        return;
    STATE->f8 = 0;
    STATE->fc = 0;
    STATE->f2 = 0;
    *(s64 *)&STATE->f18 = native_fn_02007a9c();
    if (arg0 == 0)
        *(s64 *)&STATE->f10 = native_fn_02007a9c();
}
