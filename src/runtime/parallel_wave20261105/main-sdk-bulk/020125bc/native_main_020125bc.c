#include "context_00.h"
u16 native_main_020125bc (void)
{
    enum
    { TGID_DEFAULT = (1 << 16) };
    if (native_data_main_020dce84.field_0000 == (u32)TGID_DEFAULT) {
        RTCTime rt[1];
        native_fn_0200f304();
        if (native_fn_0200f48c(rt) == RTC_RESULT_SUCCESS) {
            native_data_main_020dce84.field_0000 = (u16)(rt->second + (rt->minute << 8));
        } else {
            ((void)0) ;
        }
    }
    native_data_main_020dce84.field_0000 = (u16)(native_data_main_020dce84.field_0000 + 1);
    return (u16)native_data_main_020dce84.field_0000;
}
