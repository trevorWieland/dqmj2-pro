#include "context.h"
void native_ov001_0222cd00(u32 count) {
    u8 index;
    u32 modifier;
    modifier = native_fn_020c5938();
    native_fn_02008d78(native_data_ov001_022498fc, 0, 396);
    native_fn_02008d78(native_data_ov001_0224983c, 0, 192);
    index = 0;
    if (count > (u32) index) {
        do {
            native_fn_ov001_0222cd84(index);
            native_fn_ov001_0222ceb8(index, modifier);
            native_fn_ov001_0222cf34(index, modifier);
            native_fn_ov001_0222d240(index, modifier);
            index += 1;
        } while ((u32) index < count);
    }
}
