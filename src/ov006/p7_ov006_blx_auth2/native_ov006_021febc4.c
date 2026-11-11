#include "context.h"

/* 0x0221C144 holds a pointer to the shared 0x1E5C-byte arena; 0x0220B9A4 is the
   six-byte pattern every candidate record is compared against. */
extern u32 native_data_ov006_0221c144;
extern u8 native_data_ov006_0220b9a4[];

extern s32 native_fn_0201b248(u8 *record, u8 *pattern, s32 size);

/* ov006 row 0x021FEBC4: 60 bytes. Walk the twenty 0x2A-byte records that start
   0x1300 bytes into the arena, publish the walk base through the out pointer,
   and return how many of them matched the six-byte pattern at +0x20. The call
   at +0x1C targets ARM code and is a BLX immediate in the image (1C F6 32 EB).
   Unknown: what the pattern identifies, and why the out pointer receives the
   walk base rather than the arena base. */
s32 native_ov006_021febc4(u8 **out)
{
    s32 count = 0;
    u8 *base = (u8 *)native_data_ov006_0221c144 + 0x1300;
    s32 i;

    *out = base;
    for (i = 0; i < 0x14; i++) {
        if (native_fn_0201b248(base + 0x20, native_data_ov006_0220b9a4, 6) != 0)
            count++;
        base += 0x2A;
    }
    return count;
}
