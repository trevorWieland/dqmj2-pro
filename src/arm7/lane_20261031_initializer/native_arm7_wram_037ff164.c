#include "native_lane_channel_init_types.h"
void native_arm7_wram_037ff164(void)
{
    for (int i = 0; i < 16; i++)
    {
        SNDExChannel *chn = &native_host_arm7_data_03807ee0[i];
        chn->id = (u8)i;
        chn->flags.syncFlag = 0;
        chn->flags.active = 0;
    }
    native_host_arm7_data_03807eb8[1] = 0;
    native_host_arm7_data_03807eb8[0] = 0;
}
