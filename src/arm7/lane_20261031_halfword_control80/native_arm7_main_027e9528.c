#include "native_halfword_views.h"
u32 native_arm7_main_027e9528(u32 enabled)
{
    if(enabled>1)return 5;
    WordStateView *work=(WordStateView *)native_arm7_data_0380fff4;
    work->control=(u16)((work->control&~0x80)|(((u16)enabled&1)<<7));
    if(enabled==1)NATIVE_HALFWORD_OUTPUT=NATIVE_HALFWORD_INPUT;
    return 0;
}
