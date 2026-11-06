#include "native_channel_lock_types.h"
void native_arm7_wram_037ffb30(u32 channelMask, u32 weak)
{
    (void)weak;

    struct SNDExChannel *chn;

    for (int i = 0; i < SND_CHANNEL_COUNT && channelMask != 0; i++, channelMask >>= 1)
    {
        if ((channelMask & 1) == 0)
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
}
