#include "context.h"
s32 native_ov001_02202230(void)
{
    s32 result = 0;
    s8 state = *(s8 *)(native_data_ov001_02239c10 + 4);
    if (state != 8) {
        native_data_ov001_02239c10[0xC] = state;
        native_data_ov001_02239c10[4] = 8;
        result = 1;
    }
    return result;
}
