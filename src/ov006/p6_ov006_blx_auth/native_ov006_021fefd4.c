#include "context.h"

/* 0x0221C148 holds the base pointer of the ov006 row table; +0x4C0 is the
   four-byte record row rendered here. 0x0220E1BC is the byte table the shared
   renderer takes as its format argument. */
extern u32 native_data_ov006_0221c148;
extern u8 native_data_ov006_0220e1bc[];

extern void native_fn_0200616c(s32 arg, void *table, u32 a, u32 b, u32 c, u32 d);

/* ov006 row 0x021FEFD4: 44 bytes. Render the record at base+0x4C0 by passing
   its four bytes as the last four arguments (the high two on the stack) of the
   shared renderer. The call at +0x1C targets ARM code and is a BLX immediate in
   the image (07 F6 BC E8). Unknown: the renderer's own argument names and what
   the record's bytes select. */
void native_ov006_021fefd4(s32 arg)
{
    u32 base = native_data_ov006_0221c148;
    u8 *row = (u8 *)(base + 0x4C0);

    native_fn_0200616c(arg, native_data_ov006_0220e1bc, row[0], row[1], row[2], row[3]);
}
