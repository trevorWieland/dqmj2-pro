#include "context.h"

/*
 * 0x02092BA0 (44 B, Thumb, p032/2.0-base)
 *
 * Tear down the 0x0455/0x0824 fields of the block at record+0xC: clear the
 * byte at +0x455, call the 0x021CFD38 function pointer with the +0x824 word
 * when that word is non-zero, then clear the word. The callback keeps the
 * loaded word in r0, which is why mwcc loads the pointer's value into r1.
 *
 * Unknowns: the meaning of the two offsets and of the 0x021CFD38 callback
 * table; the block's ownership.
 */

typedef struct {
    u8 pad[0xC];
    u32 block;
} ContextView;

extern void (*native_data_021cfd38)(void *);

void native_main_02092ba0(ContextView *context)
{
    u8 *base;
    void *pending;

    base = (u8 *)context->block;
    *(u8 *)(base + 0x455) = 0;
    pending = *(void **)(base + 0x824);
    if (pending != 0)
        native_data_021cfd38(pending);
    *(u32 *)(base + 0x824) = 0;
}
