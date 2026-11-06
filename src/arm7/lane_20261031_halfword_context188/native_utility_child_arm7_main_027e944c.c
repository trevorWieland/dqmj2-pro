#include "native_halfword_views.h"
u32 native_utility_child_arm7_main_027e944c(void)
{
    u16 *parameters=(u16 *)(*native_utility_child_arm7_data_0380fff4+0x5f0);
    parameters[2]=(u16)((u32)parameters[2] * *(u16 *)(*native_utility_child_arm7_data_0380fff4+0x5f0)+parameters[1]);
    return parameters[2];
}
