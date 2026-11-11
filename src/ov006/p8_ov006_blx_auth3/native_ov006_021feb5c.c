#include "context.h"

/* 0x0221C144 holds a pointer to the ov006 transfer state. The poll word is the
   16-bit counter at +0x168C and the busy flag byte at +0x1E5C. */
extern u32 native_data_ov006_0221c144;

extern void native_fn_02012030(u32 counter);
extern s32 native_fn_020127ec(u32 callback);
extern s32 native_fn_02012824(u32 callback);
/* Address taken as data so mwcc folds the Thumb bit into the relocation. */
extern u8 native_ov006_021fec00[];

/* ov006 row 0x021FEB5C: 104 bytes. Mark the transfer busy, poll the +0x168C
   counter through the ARM kick helper, and if it is not yet 2 start the
   0x021FEC00 transfer and wait for the counter to reach 2. Then check the
   completion helper; only a 2 answer succeeds. The calls at +0x12, +0x24,
   +0x36 and +0x48 target ARM code and are BLX immediates in the image.
   Unknown: what the counter counts and what 0x021FEC00 transfers. */
s32 native_ov006_021feb5c(void)
{
    ((u8 *)native_data_ov006_0221c144)[0x1E5C] = 1;
    native_fn_02012030(native_data_ov006_0221c144 + 0x168C);

    if (*(u16 *)(native_data_ov006_0221c144 + 0x168C) != 2) {
        if (native_fn_020127ec((u32)(native_ov006_021fec00 + 1)) != 2)
            return 0;
        do {
            native_fn_02012030(native_data_ov006_0221c144 + 0x168C);
        } while (*(u16 *)(native_data_ov006_0221c144 + 0x168C) != 2);
    }

    if (native_fn_02012824((u32)(native_ov006_021fec00 + 1)) != 2)
        return 0;
    return 1;
}
