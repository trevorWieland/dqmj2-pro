#include "context.h"

/* 0x0221C164 is the ov006 mode descriptor: word 0 is the mode-change callback
   (may be null) and word 1 a pointer to the mode state. The state's mode word
   is at +0x40, its selected index halfword at +0x60 and its result halfword at
   +0x5C. 0x0220E7D0 is the table handed to the callback. */
struct native_mode_0221c164 {
    u32 callback;
    u8 *state;
};

extern struct native_mode_0221c164 native_data_ov006_0221c164;
extern u8 native_data_ov006_0220e7d0[];

extern void native_fn_02008430(void);
extern void native_ov006_02201270(s32 mode);
extern s32 native_ov006_02201a20(u16 index);

/* ov006 row 0x022019D0: 80 bytes. Re-select the mode's entry: the mode word
   must be 7 first (otherwise the ARM panic helper runs), then dispatch mode 1,
   index the entry table by the state's +0x60 halfword, store the answer at
   +0x5C and hand 0x08000000 plus the 0x0220E7D0 table to the mode callback.
   Returns the stored answer. The call at +0x0C targets ARM code and is a BLX
   immediate in the image; the callback is an indirect call through the
   descriptor. Unknown: what 0x02201A20 computes and what the callback does with
   the 0x08000000 tag. */
s32 native_ov006_022019d0(void)
{
    u16 answer;

    if (*(u32 *)(native_data_ov006_0221c164.state + 0x40) != 7)
        native_fn_02008430();

    native_ov006_02201270(1);
    answer = (u16)native_ov006_02201a20(*(u16 *)(native_data_ov006_0221c164.state + 0x60));
    *(u16 *)(native_data_ov006_0221c164.state + 0x5C) = answer;

    if (native_data_ov006_0221c164.callback != 0)
        ((void (*)(u32, u32, u32))native_data_ov006_0221c164.callback)(
            0x08000000, (u32)native_data_ov006_0220e7d0,
            *(u16 *)(native_data_ov006_0221c164.state + 0x5C));
    return *(u16 *)(native_data_ov006_0221c164.state + 0x5C);
}
