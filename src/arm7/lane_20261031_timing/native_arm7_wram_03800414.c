#include "native_lane_sdk_types.h"
void native_arm7_wram_03800414(int player, u32 ticks)
{
    SNDPlayer *ply = &native_host_arm7_data_03808420[player];
    for (int i = 0; i < 16; i++)
    {
        SNDTrack *trk = native_host_arm7_arm_03800a7c(ply, i);
        if (trk)
        {
            native_host_arm7_arm_038009e0(trk, ply, 127);
            native_host_arm7_arm_03800a48(trk);
        }
    }
    native_host_arm7_arm_037fefb4();
    u32 i;
    for (i = 0; i < ticks; i++)
    {
        if (native_host_arm7_arm_03800cf0(ply, 0))
        {
            native_host_arm7_arm_03800b00(ply);
            break;
        }
    }
    native_host_arm7_arm_037fef64();
    if (native_host_arm7_data_03807edc)
        native_host_arm7_data_03807edc->rows[ply->playerId].counter += i;
}
