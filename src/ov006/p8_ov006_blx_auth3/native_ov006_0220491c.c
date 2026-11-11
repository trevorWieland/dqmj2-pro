#include "context.h"

/* 0x0221C1E8 holds a pointer to the ov006 channel-state array; every channel
   owns a 0x40-byte record whose first word is a table and whose +0x10 word is
   a list head. List nodes keep prev at +0, next at +4, two data words at +8 and
   +0x0C, and two byte keys at +0x10 and +0x11. */
extern u32 native_data_ov006_0221c1e8;

extern u8 *native_ov006_02203114(u8 *table);
extern s32 native_fn_02005d50(s32 lock);
extern void native_fn_02005d20(s32 key);
extern void native_ov006_0220428c(u8 *head, u8 *node);

/* ov006 row 0x0220491C: 84 bytes. Allocate a list node from the channel's table
   and link it before the first node whose +0x10 key it does not exceed, all
   under the shared lock. The call at +0x20 and the insert at +0x3C are Thumb;
   the calls at +0x26 and +0x48 target ARM code and are BLX immediates in the
   image. Unknown: what the table allocates (0x02203114 itself is still
   un-authored), and what the two data words and the +0x11 byte mean. */
u8 *native_ov006_0220491c(s32 channel, u32 first, u32 second, u8 key, u8 tag)
{
    u8 *node;
    u8 *head;
    s32 lock;

    node = native_ov006_02203114(*(u8 **)(native_data_ov006_0221c1e8 + channel * 0x40));
    *(u32 *)(node + 8) = first;
    *(u32 *)(node + 0x0C) = second;
    *(u8 *)(node + 0x10) = key;
    *(u8 *)(node + 0x11) = tag;

    lock = native_fn_02005d50(1);
    head = *(u8 **)(native_data_ov006_0221c1e8 + channel * 0x40 + 0x10);
    for (;;) {
        if (key < *(u8 *)(head + 0x10)) {
            native_ov006_0220428c(head, node);
            break;
        }
        head = *(u8 **)(head + 4);
    }
    native_fn_02005d20(lock);
    return node;
}

