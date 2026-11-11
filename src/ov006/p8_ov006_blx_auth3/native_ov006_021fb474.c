#include "context.h"

/* 0x0221C0EC is an ov006 display descriptor: the halfword at +0x04 is the
   current display mode and the word at +0x08 a pointer to its state, whose
   +0x44 byte marks a pending rebuild. */
struct native_display_0221c0ec {
    u32 unknown0;
    u16 mode;
    u16 unknown6;
    u32 state;
};

extern struct native_display_0221c0ec native_data_ov006_0221c0ec;

/* Byte table of per-mode screen-base offsets used by the rebuild. */
extern u8 native_data_ov006_0220b7f0[];

extern s32 native_fn_02002480(u16 mode, s32 which);
extern s32 native_fn_020024bc(u16 mode, s32 which);

/* ov006 row 0x021FB474: 88 bytes. Rebuild both background control words when
   the state's pending flag at +0x44 is set: query the mode twice through ARM
   helpers, program 0x04000010 with the raw low nine bits of the second answer
   and 0x04000018 with that answer plus the per-mode table offset, then clear
   the flag. Calls at +0x12 and +0x1E target ARM code and are BLX immediates in
   the image. Unknown: what the two helpers return, and why only bits 16-24 of
   each word are written. */
void native_ov006_021fb474(void)
{
    s32 index;
    s32 value;

    if (((u8 *)native_data_ov006_0221c0ec.state)[0x44] == 0)
        return;
    index = native_fn_02002480(native_data_ov006_0221c0ec.mode, 0x1D);
    value = native_fn_020024bc(native_data_ov006_0221c0ec.mode, 0x1D) - 0x33;
    *(volatile u32 *)0x04000010 = ((u32)value << 16) & 0x01FF0000;
    *(volatile u32 *)0x04000018 = ((u32)(value + native_data_ov006_0220b7f0[index]) << 16)
                                  & 0x01FF0000;
    ((u8 *)native_data_ov006_0221c0ec.state)[0x44] = 0;
}
