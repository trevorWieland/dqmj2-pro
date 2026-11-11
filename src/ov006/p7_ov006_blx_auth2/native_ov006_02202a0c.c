#include "context.h"

/* 0x0221C170 holds a pointer to the ov006 display state; the 16-bit mode word
   sits at +0xE4. */
extern u32 native_data_ov006_0221c170;

extern void native_fn_020102c4(u16 mode);
extern void native_fn_020102e0(u16 mode);

/* ov006 row 0x02202A0C: 60 bytes. Map a display-state selector to the value the
   caller stores: selectors 9 and 10 reprogram the mode word through their own
   ARM entry point and answer zero, selector 1 answers 4 and everything else
   answers 8. Both calls target ARM code and are BLX immediates in the image
   (0D F6 4E EC / 0D F6 54 EC). Unknown: the meaning of the three answer codes
   and why the mode word is read through two separate ARM entry points instead
   of one call with a selector argument. */
s32 native_ov006_02202a0c(s32 unused, s32 selector)
{
    switch (selector) {
    case 9:
        native_fn_020102c4(*(u16 *)(native_data_ov006_0221c170 + 0xE4));
        return 0;
    case 10:
        native_fn_020102e0(*(u16 *)(native_data_ov006_0221c170 + 0xE4));
        return 0;
    case 1:
        return 4;
    }
    return 8;
}
