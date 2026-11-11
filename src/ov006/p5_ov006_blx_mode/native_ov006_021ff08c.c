#include "context.h"

/* 0x0221C148 holds the base pointer for the renderer's record rows. */
extern u32 native_data_ov006_0221c148;
/* Byte table handed to the shared renderer as its format argument. */
extern u8 native_data_ov006_0220e1bc[];

extern void native_fn_0200616c(s32 arg, void *table, u32 a, u32 b, u32 c, u32 d);

/* ov006 row 0x021FF08C: 48 bytes, byte-exact with the mode-aware relocation
   application. The call at +0x1A targets ARM 0x0200616C (BLX, 07 F6 62 E8).
   Negative control: the row base 0x4CC -> 0x4C8 must fail the comparison. */
void native_ov006_021ff08c(s32 arg)
{
    u32 base = native_data_ov006_0221c148;
    u8 *row = (u8 *)(base + 0x4CC);

    native_fn_0200616c(arg, native_data_ov006_0220e1bc, row[0], row[1], row[2], row[3]);
}
