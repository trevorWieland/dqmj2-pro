#include "native_setting_types.h"
u32 native_arm7_main_027e8ec8(u32 value)
{
    if (value > 255)
        return 5;
    native_host_arm7_data_0380fff4->value = (s16)value;
    native_host_arm7_data_0480802c = (u16)value;
    return 0;
}
