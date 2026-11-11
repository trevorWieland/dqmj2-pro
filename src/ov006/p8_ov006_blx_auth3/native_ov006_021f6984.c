#include "context.h"

/* 0x0221C0A8 is the current ov006 entry byte. Four halfword tables are
   interleaved at 0x0220B5BA..0x0220B5C0 with an eight-byte stride, so each one
   is indexed as a u16 array with a factor of four. */
extern u8 native_data_ov006_0221c0a8;
extern u16 native_data_ov006_0220b5ba[];
extern u16 native_data_ov006_0220b5be[];
extern u16 native_data_ov006_0220b5bc[];
extern u16 native_data_ov006_0220b5c0[];

extern s32 native_fn_020024bc(s32 value, s32 mode);
extern void native_ov006_021ff6d4(s32 mode);
extern void native_ov006_021f29bc(u16 first, u16 second, u16 third, u16 fourth);

/* ov006 row 0x021F6984: 92 bytes. Step the current entry (by two in mode 1, by
   one otherwise) through the ARM helper, map it to its entry-table row, then
   dispatch the four interleaved halfword columns of that row. Calls at +0x0E
   and +0x28 are Thumb; the calls at +0x1E and +0x42 target ARM code and are BLX
   immediates in the image. Unknown: what the four columns mean and what
   0x021FF6D4(8) prepares. */
void native_ov006_021f6984(s32 mode)
{
    if (mode == 1)
        native_data_ov006_0221c0a8 = (u8)native_fn_020024bc(native_data_ov006_0221c0a8 + 2, 3);
    else
        native_data_ov006_0221c0a8 = (u8)native_fn_020024bc(native_data_ov006_0221c0a8 + 1, 3);

    native_ov006_021ff6d4(8);
    native_ov006_021f29bc(native_data_ov006_0220b5ba[native_data_ov006_0221c0a8 * 4],
                          native_data_ov006_0220b5be[native_data_ov006_0221c0a8 * 4],
                          native_data_ov006_0220b5bc[native_data_ov006_0221c0a8 * 4],
                          native_data_ov006_0220b5c0[native_data_ov006_0221c0a8 * 4]);
}
