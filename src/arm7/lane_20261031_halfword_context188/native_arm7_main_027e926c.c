#include "native_halfword_views.h"
u32 native_arm7_main_027e926c(const u16 *source)
{
    u32 index=0;
    u16 *destination=((CopyStateView *)native_arm7_data_0380fff4)->values;
    do {
        u16 value=*source++;
        ++index;
        *destination++=value;
    } while(index<16);
    return 0;
}
