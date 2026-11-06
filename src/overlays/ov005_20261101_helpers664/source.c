#include "context.h"
u32 native_ov005_021e664c(const u32 *values,s32 index) {
    if (values != 0) {
        return values[index-1];
    }
    return 0;
}

s32 native_ov005_021e6678(s32 level,s32 count,s32 handle) {
    u8 *values;
    s16 sum;
    s32 index;
    values = native_fn_0203cc2c(native_data_ov005_021e7894,handle);
    if (values != 0) {
        sum = 0;
        index = 0;
        if (level > 0) {
            do {
                sum = (s16)(sum + values[index]);
                index += 1;
            } while (index < level);
        }
        native_fn_0203cf9c(handle,values);
        return (s16)((sum * count + 4) / 5);
    }
    return 0;
}
