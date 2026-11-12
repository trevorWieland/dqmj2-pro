#include "context.h"

/* native_ov001_02213588.c: 76 bytes at 0x02213588 in ov001.
 * void func(Record *record): for each of the +0x24 entries, forward the +0x1c
 * handle through 0x0205f98c and 0x021f1ba0. */
void native_ov001_02213588(u8 *record)
{
    u8 i = 0;
    s8 count = *(s8 *)(record + 0x24);

    if (count <= 0)
        return;
    do {
        native_fn_ov001_021f1ba0(
            native_fn_0205f98c(*(s32 *)(record + 0x1c), i),
            ((i & 0xff) + 0x90) & 0xff);
        i = (i + 1) & 0xff;
    } while (i < *(s8 *)(record + 0x24));
}
