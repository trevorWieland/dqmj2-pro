#include "masked_callers.h"
extern u32 native_fn_02049ad0(u32 index);
extern u8 native_data_020ddb08[];

u32 native_main_02049aa8(u32 index) {
    if (native_data_020ddb08[1]==0) {
        index=(s32)(s8)(index+0x24);
    }
    return native_fn_02049ad0(index);
}
