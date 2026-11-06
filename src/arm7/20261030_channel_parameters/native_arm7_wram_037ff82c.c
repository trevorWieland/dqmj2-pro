#include "native_channel_parameter_types.h"
s32 native_arm7_wram_037ff82c(struct SNDExChannel *chn, BOOL step)
{
    s32 sustain;
    if (step)
    {
        switch (chn->envStatus)
        {
            case SND_ENV_ATTACK:
                chn->envAttenuation = -((s32)((0u - (u32)chn->envAttenuation) * chn->attack) >> 8);
                if (chn->envAttenuation == 0)
                    chn->envStatus = SND_ENV_DECAY;
                break;
            case SND_ENV_DECAY:
                sustain = native_host_arm7_data_0380704c[chn->sustain] * 128;
                chn->envAttenuation = (s32)((u32)chn->envAttenuation - chn->decay);
                if (chn->envAttenuation <= sustain)
                {
                    chn->envAttenuation = sustain;
                    chn->envStatus = SND_ENV_SUSTAIN;
                }
                break;
            case SND_ENV_SUSTAIN:
                break;
            case SND_ENV_RELEASE:
                chn->envAttenuation = (s32)((u32)chn->envAttenuation - chn->release);
                break;
        }
    }
    return chn->envAttenuation >> 7;
}
