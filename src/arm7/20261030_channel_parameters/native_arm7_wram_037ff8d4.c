#include "native_channel_parameter_types.h"
void native_arm7_wram_037ff8d4(struct SNDExChannel *chn, s32 attack)
{
    if (attack < 109)
        chn->attack = (u8)(255u - (u32)attack);
    else
        chn->attack = (native_host_arm7_data_038071e0 + 128)[127 - attack];
}
