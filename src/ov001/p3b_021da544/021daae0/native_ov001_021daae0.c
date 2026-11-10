#include "../context.h"

/* Reports whether any live entry of the 60-entry key list has the 0x40 bit set
   in the flag byte of its directory record (0x021d8dec).  A zero entry is
   skipped and the first flagged record stops the scan. */
u32 native_ov001_021daae0(u8 *list) {
    s32 i;
    u32 result;
    u8 *entry;

    result = 0;
    i = 0;
    do {
        if (*(s8 *)(list + i) != 0) {
            entry = (u8 *)native_fn_ov001_021d8dec(i);
            if ((entry[3] & 0x40) != 0) {
                result = 1;
                break;
            }
        }
        i++;
    } while (i < 60);
    return result;
}

