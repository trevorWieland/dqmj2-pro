#include "context.h"

/* 0x0221C150 holds a pointer to the shared 0x600-byte work block. */
extern u32 native_data_ov006_0221c150;

extern void native_fn_02007308(u32 block, s32 size);
extern void native_fn_02004c78(u32 block, s32 value, s32 size);
extern void native_ov006_02202b24(u32 block);
extern void native_ov006_02204974(s32 which, s32 value);

/* ov006 row 0x021FFE28: 52 bytes. Reset the shared block twice (once through
   the ARM fill helper, once through the ARM range clear) and then re-announce
   it to the overlay, finishing with the "which = 1" notify that carries the
   caller's argument. The calls at +0x0C and +0x1A target ARM code and are BLX
   immediates in the image (07 F6 68 EA / 04 F6 1A EF). Unknown: why the block
   is initialised through two different ARM helpers with the same size, and
   what the notify's first parameter selects. */
void native_ov006_021ffe28(s32 value)
{
    native_fn_02007308(native_data_ov006_0221c150, 0x600);
    native_fn_02004c78(native_data_ov006_0221c150, 0, 0x600);
    native_ov006_02202b24(native_data_ov006_0221c150);
    native_ov006_02204974(1, value);
}
