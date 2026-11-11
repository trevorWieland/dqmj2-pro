#include "context.h"

/* 0x0220D3DC is the ov006 network-parameter block: three words of byte-swapped
   data at +0x18, +0x1C and +0x20. The completion flag the wait loop polls is
   the word at 0x021CFD48. */
struct native_block_0220d3dc {
    u8 unknown[0x18];
    u32 first;
    u32 second;
    u32 third;
};

extern struct native_block_0220d3dc native_data_ov006_0220d3dc;
extern u8 native_data_ov006_0220d3e4[];
extern u32 native_data_ov006_021cfd48;

/* Byte-swap helper shared with the rest of the ov006 network code. */
extern u32 native_ov006_021edc50(u32 value);
/* Hand the parameter block to the ARM-side start helper; negative is failure. */
extern s32 native_fn_0209063c(u32 block);
extern void native_fn_02006b7c(s32 ticks);

/* ov006 row 0x021EDB00: 88 bytes. Program the three byte-swapped network
   parameters, start the link through the main-side helper, then wait for the
   completion word at 0x021CFD48 to become non-zero, sleeping 100 ticks per
   poll. Returns -1 when the start helper refuses, 0 otherwise. The call at
   +0x3E targets ARM code and is a BLX immediate in the image. Unknown: what the
   three parameters mean, and who sets the completion word. */
s32 native_ov006_021edb00(u32 first, u32 second, u32 third)
{
    native_data_ov006_0220d3dc.first = native_ov006_021edc50(first);
    native_data_ov006_0220d3dc.second = native_ov006_021edc50(second);
    native_data_ov006_0220d3dc.third = native_ov006_021edc50(third);

    if (native_fn_0209063c((u32)native_data_ov006_0220d3e4) < 0)
        return -1;

    while (native_data_ov006_021cfd48 == 0)
        native_fn_02006b7c(100);
    return 0;
}
