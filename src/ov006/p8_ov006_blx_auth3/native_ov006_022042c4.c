#include "context.h"

/* 0x0221C1AC holds the pointer to the 0x80C-byte ov006 page block. The block's
   first 0x800 bytes are data pages and the words at +0x800 and +0x808 hold the
   two page handles. */
extern u32 native_data_ov006_0221c1ac;

extern u32 ov006_clear_buffer_02203c08(s32 id, s32 size);
extern void native_fn_02008c58(u32 value, u32 block, u32 size);
extern u32 native_ov006_022030a4(s32 first, u32 block, s32 size);
extern u32 native_ov006_0220490c(s32 which, u32 callback, s32 arg2, s32 arg3);
/* Address taken as data so mwcc folds the Thumb bit into the relocation. */
extern u8 native_ov006_02204330[];

/* ov006 row 0x022042C4: 108 bytes. Allocate the 0x80C-byte page block, fill its
   first 0x800 bytes, build both 0x400-byte pages through the Thumb helper and
   store their handles at +0x800 and +0x804, then register the 0x02204330
   callback with 0xC8 and keep the answer at +0x808. Calls at +0x06, +0x22 and
   +0x48 are Thumb; the call at +0x16 targets ARM code and is a BLX immediate in
   the image. Unknown: what the two pages hold and what the 0xC8 argument means. */
void native_ov006_022042c4(void)
{
    s32 index;

    native_data_ov006_0221c1ac = ov006_clear_buffer_02203c08(0x80C, 4);
    native_fn_02008c58(0x200, native_data_ov006_0221c1ac, 0x800);

    for (index = 0; index < 2; index++)
        *(u32 *)(native_data_ov006_0221c1ac + index * 4 + 0x800) =
            native_ov006_022030a4(0x40, native_data_ov006_0221c1ac + index * 0x400, 8);

    *(u32 *)(native_data_ov006_0221c1ac + 0x808) =
        native_ov006_0220490c(1, (u32)(native_ov006_02204330 + 1), 0, 0xC8);
}
