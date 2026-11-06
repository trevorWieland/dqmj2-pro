#include "native_channel_lock_types.h"
void native_arm7_wram_037ffbe0(u32 channelMask, u32 weak)
{
    struct SNDExChannel *chn;
    u32 j = channelMask;
    int i = 0;

    for (; i < SND_CHANNEL_COUNT && j != 0; i++, j >>= 1)
    {
        if ((j & 1) == 0)
            continue;

        chn = &SNDi_Work.channels[i];

        if (sLockedChannelMask & (1 << i))
            continue;

        if (chn->callback)
            chn->callback(chn, 0, chn->callbackUserData);

        SND_StopChannel(i, 0);
        chn->priority = 0;
        SND_FreeExChannel(chn);
        chn->flags.syncFlag = 0;
        chn->flags.active = 0;
    }

    if (weak & 1)
    {
        sWeakLockedChannelMask |= channelMask;
    }
    else
    {
        sLockedChannelMask |= channelMask;
    }
}
