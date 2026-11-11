#include "../context.h"

/* 0x021e9da4: clear the ten slot words that the probe rejects. */
void native_ov001_021e9da4(void) {
    s32 i = 0;
    do {
        u32 value = ((u32 *)native_data_ov001_02238dec)[i];
        if (value != 0xFFFFFFFF && native_fn_0205d6f4(value) == 0) {
            ((u32 *)native_data_ov001_02238dec)[i] = 0xFFFFFFFF;
        }
        i++;
    } while (i < 10);
}
