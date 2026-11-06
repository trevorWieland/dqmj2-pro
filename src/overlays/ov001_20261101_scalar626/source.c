#include "context.h"
void native_ov001_0222ceb8(s32 index,u32 scalar) {
    u16 value = (u16)native_fn_020243e0(native_fn_02023f78(50.0,native_fn_02024540(1.25,native_fn_02024504(scalar))));
    if (value > 100) {
        native_data_ov001_0224992c[index * 132] = 100;
    } else {
        native_data_ov001_0224992c[index * 132] = (u8)value;
    }
}
