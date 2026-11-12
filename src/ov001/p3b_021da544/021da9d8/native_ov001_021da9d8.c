#include "../context.h"

/* Per-frame fade/settle driver for one effect instance.  Stem 1 clears the
   instance's 0x320 counter, arms the 0x100-unit effect through 0x021eec7c and
   fires the 222/1 cue; stem 2 feeds the counter-derived weight (31 - 2*counter,
   clamped at zero) to 0x021d96d4, bumps the counter and, once it passes 48,
   moves the instance to stem 3 and raises the +0xAC flag of its 0x1E8 record
   through 0x021db410.  Any other stem value is left untouched.  The current stem
   byte is returned. */
u32 native_ov001_021da9d8(u8 *obj) {
    s32 weight;

    switch (obj[0x325]) {
    case 1:
        *(u16 *)(obj + 0x320) = 0;
        obj[0x325] = 2;
        ov001_effect_resource_create_021eec7c(0x100, obj, 0);
        native_fn_ov001_021f949c(0xDE, 1);
        break;
    case 2:
        weight = 31 - (*(s16 *)(obj + 0x320) << 1);
        if (weight < 0) {
            weight = 0;
        }
        native_fn_ov001_021d96d4(obj, weight & 0xFF);
        (*(s16 *)(obj + 0x320))++;
        if (*(s16 *)(obj + 0x320) > 48) {
            obj[0x325] = 3;
            *(u8 *)(*(u32 *)(obj + 0x1E8) + 0xAC) = 1;
            native_fn_ov001_021db410(obj, 0);
        }
        break;
    case 3:
        break;
    }
    return obj[0x325];
}

