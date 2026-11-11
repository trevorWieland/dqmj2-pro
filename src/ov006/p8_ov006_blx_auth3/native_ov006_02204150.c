#include "context.h"

extern s32 native_fn_0200f0a4(s32 enable);

/* ov006 row 0x02204150: 80 bytes. Keep the 0x0221C18C mode byte in step with
   bit 15 of the 0x027FFFA8 halfword: when the bit is clear and the enable
   helper accepts 1, drop the mode to 0; when the bit is set and the helper
   accepts 0, set the mode to 1. Calls at +0x1A and +0x38 target ARM code and
   are BLX immediates in the image. Unknown: what 0x027FFFA8 is (it is not a
   documented I/O register), and why the helper's answer gates the update
   instead of the bit alone. */
void native_ov006_02204150(void)
{
    if (*(volatile u8 *)0x0221c18c != 0) {
        if (((*(volatile u16 *)0x027fffa8 & 0x8000) >> 15) == 0) {
            if (native_fn_0200f0a4(1) != 0)
                *(volatile u8 *)0x0221c18c = 0;
        }
    } else {
        if (((*(volatile u16 *)0x027fffa8 & 0x8000) >> 15) != 0) {
            if (native_fn_0200f0a4(0) != 0)
                *(volatile u8 *)0x0221c18c = 1;
        }
    }
}
