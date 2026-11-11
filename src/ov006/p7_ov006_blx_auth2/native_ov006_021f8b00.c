#include "context.h"

/* Shared ov006 display state at 0x0221C0D8: a 16-bit mode at +0x02 and a
   pointer at +0x04 to the record whose byte +0x56 flags "scroll pending". */
struct native_state_021f8b00 {
    u16 field_00;
    u16 field_02;
    u8 *field_04;
};

extern struct native_state_021f8b00 native_data_ov006_0221c0d8;

/* Scale one mode value; ARM code in main, so this is a BLX from Thumb. */
extern s32 native_fn_020024bc(s32 value, s32 scale);

/* ov006 row 0x021F8B00: 60 bytes. When the pending-scroll flag is set, derive a
   vertical scroll offset from the current mode, write it into both BG0 and BG1
   as their 16-bit-high VOFFS field, and clear the flag. The call at +0x12
   targets ARM code and is a BLX immediate in the image (09 F6 D4 EC).
   Unknown: the meaning of mode 0x1C and of the -50 bias, and why both
   background layers receive the identical offset; the 0x01FF0000 mask is what
   keeps only the 9-bit VOFFS field after the <<16. */
void native_ov006_021f8b00(void)
{
    if (native_data_ov006_0221c0d8.field_04[0x56] != 0) {
        u32 offset = ((native_fn_020024bc(native_data_ov006_0221c0d8.field_02, 0x1C) - 50)
                      << 16) & 0x01FF0000;

        *(volatile u32 *)0x04000010 = offset;
        *(volatile u32 *)0x04000018 = offset;
        native_data_ov006_0221c0d8.field_04[0x56] = 0;
    }
}
