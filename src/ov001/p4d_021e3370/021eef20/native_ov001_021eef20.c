#include "../context.h"

/* 0x021eef20: hand the nineteen table halfwords to the per-entry handler. */
void native_ov001_021eef20(void) {
    s32 i = 0;
    do {
        native_fn_ov001_021eeb70(((u16 *)native_data_ov001_0222ec88)[i]);
        i++;
    } while (i < 19);
}
