#include "context.h"

/* 0x0221C134 holds a pointer to the shared 0x608-byte block; byte +0x604 of
   that block is its "in use" flag and +0x04 starts the 0x600-byte payload. */
extern u32 native_data_ov006_0221c134;

extern void native_fn_02007308(u32 block, s32 size);
extern void native_fn_02004cd8(u32 block, s32 value, s32 size);

/* ov006 row 0x021FE544: 60 bytes. Release the shared block: when the in-use
   flag is set, clear the payload twice (whole-range reset, then a value-fill)
   and drop the flag. The calls at +0x12 and +0x22 target ARM code and are BLX
   immediates in the image (08 F6 D8 EE / 06 F6 B8 EB). Unknown: why two
   different ARM clear helpers with the same range are used, and what their
   value argument selects; the global is re-read before each field access
   because the ARM calls may republish it. */
void native_ov006_021fe544(void)
{
    if (((u8 *)native_data_ov006_0221c134)[0x604] != 0) {
        native_fn_02007308((u32)((u8 *)native_data_ov006_0221c134 + 4), 0x600);
        native_fn_02004cd8((u32)((u8 *)native_data_ov006_0221c134 + 4), 0, 0x600);
        ((u8 *)native_data_ov006_0221c134)[0x604] = 0;
    }
}
