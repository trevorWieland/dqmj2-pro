#include "native_channel_lock_types.h"
void native_arm7_wram_037ffcc0(u32 channelMask, u32 weak)
{
    if (weak & 1)
    {
        sWeakLockedChannelMask &= ~channelMask;
    }
    else
    {
        sLockedChannelMask &= ~channelMask;
    }
}
