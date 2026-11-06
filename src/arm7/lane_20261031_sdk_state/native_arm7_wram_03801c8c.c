#include "native_sdk_connected_types.h"
void native_arm7_wram_03801c8c(void)
{
    u16 channelActiveMask = 0;
    u16 channelCaptureMask = 0;

    if (SNDi_SharedWork == NULL)
        return;

    for (s32 i = 0; i < SND_CHANNEL_COUNT; i++)
    {
        if (SND_IsChannelActive(i))
            channelActiveMask |= 1 << i;
    }

    if (SND_IsCaptureActive(0))
        channelCaptureMask |= 0x1;
    if (SND_IsCaptureActive(1))
        channelCaptureMask |= 0x2;

    SNDi_SharedWork->channelStatus = channelActiveMask;
    SNDi_SharedWork->captureStatus = channelCaptureMask;
}
