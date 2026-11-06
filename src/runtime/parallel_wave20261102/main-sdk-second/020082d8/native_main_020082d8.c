#include "context_00.h"
void native_main_020082d8 (u16 bank, u16 lockId)
{
    u32 workMap;
    s32 zeroBits;
    OSIntrMode enabled = native_fn_02007ff4();
    workMap = (u32)(bank & native_data_main_020e3728.field_0000 & 0x01ff );
    while (1 ) {
        zeroBits = (s32)(31 - native_fn_0200829c((u32)workMap));
        if (zeroBits < 0) {
            break;
        }
        workMap &= ~(0x00000001 << zeroBits);
        if (native_data_main_020e3728.field_0004[zeroBits] == lockId) {
            native_data_main_020e3728.field_0004[zeroBits] = 0;
            native_data_main_020e3728.field_0000 &= ~(0x00000001 << zeroBits);
        }
    }
    (void)native_fn_02008008(enabled);
}
