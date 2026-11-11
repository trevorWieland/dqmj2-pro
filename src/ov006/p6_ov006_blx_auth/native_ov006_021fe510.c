#include "context.h"

/* 0x0221C134 holds the pointer to a main-side table whose +4 word is the start
   of the record area addressed here. */
extern u32 native_data_ov006_0221c134;

extern void native_fn_02008bf8(void *dst, u8 *src, u32 size);

/* ov006 row 0x021FE510: 52 bytes. Copy `count` 0x40-byte records: the source
   starts at table + 4 + (index << 1) and each destination is the caller's
   buffer advanced by 0x40, with the copy length taken as size << 1. The count
   guard is measured before the length is formed, and the loop is a bottom-test
   do/while (the measured code enters the body once after the guard). The call
   at +0x20 targets ARM code and is a BLX immediate in the image (0A F6 62 EB).
   Unknown: the record/table layout and the units of index/size (they are
   measured as halfword counts). */
void native_ov006_021fe510(void *dst, s32 index, s32 size, s32 count)
{
    u8 *src = (u8 *)native_data_ov006_0221c134 + 4 + ((u32)index << 1);
    s32 record = 0;
    u32 bytes;

    if (count <= 0)
        return;

    bytes = (u32)size << 1;
    do {
        native_fn_02008bf8(dst, src, bytes);
        dst = (u8 *)dst + 0x40;
        src += 0x40;
        record++;
    } while (record < count);
}
