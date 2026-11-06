#include "context_00.h"
BOOL native_main_02009a0c (u32 tag)
{
    OSIntrMode bak_psr = native_fn_02007ff4();
    BOOL result;
    if (tag > native_data_main_020e3780.field_0004) {
        if (tag - native_data_main_020e3780.field_0004 < 0x80000000) {
            result = 0 ;
        } else {
            result = 1 ;
        }
    } else {
        if (native_data_main_020e3780.field_0004 - tag < 0x80000000) {
            result = 1 ;
        } else {
            result = 0 ;
        }
    }
    (void)native_fn_02008008(bak_psr);
    return result;
}
