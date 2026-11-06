#include "native_exchannel_flush_types.h"
void native_arm7_wram_037ff1c0(void)
{
    struct SNDExChannel *chn;
    s32 i;

    for (i = 0; i < SND_CHANNEL_COUNT; i++)
    {
        chn = &native_host_arm7_data_03807ee0[i];

        if (chn->flags.syncFlag == 0)
            continue;

        if (chn->flags.syncFlag & SND_CHN_SYNC_STOP)
            native_host_arm7_arm_037fea20(i, 0);

        if (chn->flags.syncFlag & SND_CHN_SYNC_START)
        {
            switch (chn->type)
            {
                case SND_CHN_TYPE_PCM:
                    native_host_arm7_arm_037fe804(i,
                        chn->sound.waveDataPtr,
                        chn->waveParam.format,
                        chn->waveParam.loopEnabled ? 1 : 2,
                        (s32)chn->waveParam.loopStart,
                        (s32)chn->waveParam.loopLength,
                        chn->volume & 0xFF,
                        chn->volume >> 8,
                        chn->timer,
                        chn->pan);
                    break;
                case SND_CHN_TYPE_PSG:
                    native_host_arm7_arm_037fe8d0(i,
                        chn->sound.dutyCycle,
                        chn->volume & 0xFF,
                        chn->volume >> 8,
                        chn->timer,
                        chn->pan);
                    break;
                case SND_CHN_TYPE_NOISE:
                    native_host_arm7_arm_037fe97c(
                        i, chn->volume & 0xFF, chn->volume >> 8, chn->timer, chn->pan);
                    break;
            }
        }
        else
        {
            if (chn->flags.syncFlag & SND_CHN_SYNC_TIMER)
            {
                native_host_arm7_arm_037feac0(i, chn->timer);
            }
            if (chn->flags.syncFlag & SND_CHN_SYNC_VOLUME)
            {
                native_host_arm7_arm_037fea48(i, chn->volume & 0xFF, chn->volume >> 8);
            }
            if (chn->flags.syncFlag & SND_CHN_SYNC_PAN)
            {
                native_host_arm7_arm_037fead8(i, chn->pan);
            }
        }
    }

    for (i = 0; i < SND_CHANNEL_COUNT; i++)
    {
        chn = &native_host_arm7_data_03807ee0[i];

        if (!chn->flags.syncFlag)
            continue;

        if (chn->flags.syncFlag & SND_CHN_SYNC_START)
            (*(volatile u8 *)(0x04000403 + i * 16)) |= 0x80;
        chn->flags.syncFlag = 0;
    }
}
