#include "../context.h"

/* 9-byte stride table walk: `index` selects an entry from the positive or
   negative u32 selector table (0x0222ea30 / 0x0222ea34) and the result is a byte
   in the table the caller passes, biased by the fixed 0x02232b91 base.  A sign of
   zero leaves the index unchanged, which is the behaviour the original keeps. */
u32 native_ov001_021d908c(u32 index, u8 *table, s32 sign) {
    if (sign > 0) {
        index = *(u32 *)(native_data_ov001_0222ea30 + index * 8);
    } else if (sign < 0) {
        index = *(u32 *)(native_data_ov001_0222ea34 + index * 8);
    }
    return table[(u32)(native_data_ov001_02232b91 + index * 9)];
}
