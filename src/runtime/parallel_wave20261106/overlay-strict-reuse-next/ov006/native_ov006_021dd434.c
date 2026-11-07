#include "context.h"
s32 native_ov006_021dd434(s32 level,s32 count,s32 handle) {
    u8 *values;
    s16 sum;
    s32 index;
    values = native_fn_0203cc2c(native_data_ov006_0220d010,handle);
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
        return (s16)(((s32)((u32)(s32)sum * (u32)count + 4U)) / 5);
    }
    return 0;
}
