#include "native_exchannel_types.h"
static inline int ExChannelSweepUpdate(struct SNDExChannel *, BOOL);
static inline int ExChannelLfoUpdate(struct SNDExChannel *, BOOL);
void native_arm7_wram_037ff3ac(BOOL step)
{
    struct SNDExChannel *chn;
    s32 i;
    s32 vol;
    s32 pitch;
    s32 pan;
    s32 lfo;
    u16 newTimer;

    for (i = 0; i < SND_CHANNEL_COUNT; i++)
    {
        vol = 0;
        pitch = 0;
        pan = 0;
        chn = &native_host_arm7_data_03807ee0[i];

        if (!chn->flags.active)
            continue;

        if (chn->flags.start)
        {
            chn->flags.syncFlag |= SND_CHN_SYNC_START;
            chn->flags.start = FALSE;
        }
        else if (!native_host_arm7_arm_037feb50(i))
        {
            if (chn->callback)
                chn->callback(chn, 1, chn->callbackUserData);
            else
                chn->priority = 0;
            chn->volume = 0;
            chn->flags.active = FALSE;
            continue;
        }

        vol += native_host_arm7_data_0380704c[chn->velocity];
        pitch += (chn->midiKey - chn->rootMidiKey) * 0x40;

        vol += native_host_arm7_arm_037ff82c(chn, step);
        pitch += ExChannelSweepUpdate(chn, step);

        vol += chn->userDecay;
        vol += chn->userDecay2;
        pitch += chn->userPitch;

        lfo = ExChannelLfoUpdate(chn, step);

        switch (chn->lfo.param.target)
        {
            case SND_LFO_VOLUME:
                if (vol > -0x8000)
                    vol += lfo;
                break;
            case SND_LFO_PAN:
                pan += lfo;
                break;
            case SND_LFO_PITCH:
                pitch += lfo;
                break;
        }

        pan += chn->initPan;
        if (chn->panRange != 127)
        {
            pan = (pan * chn->panRange + 0x40) >> 7;
        }
        pan += chn->userPan;

        if (chn->envStatus == SND_ENV_RELEASE && vol <= -723)
        {
            chn->flags.syncFlag = SND_CHN_SYNC_STOP;
            if (chn->callback)
                chn->callback(chn, 1, chn->callbackUserData);
            else
                chn->priority = 0;
            chn->volume = 0;
            chn->flags.active = 0;
        }
        else
        {
            vol = native_host_arm7_arm_037fedd8(vol);
            newTimer = native_host_arm7_arm_037fecac(chn->waveParam.timer, pitch);

            if (chn->type == SND_CHN_TYPE_PSG)
                newTimer &= 0xFFFC;

            pan += 0x40;
            if (pan < 0)
                pan = 0;
            else if (pan > 127)
                pan = 127;

            if (vol != chn->volume)
            {
                chn->volume = (u16)vol;
                chn->flags.syncFlag |= SND_CHN_SYNC_VOLUME;
            }
            if (newTimer != chn->timer)
            {
                chn->timer = (u16)newTimer;
                chn->flags.syncFlag |= SND_CHN_SYNC_TIMER;
            }
            if (pan != chn->pan)
            {
                chn->pan = (u8)pan;
                chn->flags.syncFlag |= SND_CHN_SYNC_PAN;
            }
        }
    }
}

static inline int ExChannelSweepUpdate(struct SNDExChannel *chn, BOOL step)
{
    s64 result;

    if (chn->sweepPitch == 0)
    {
        result = 0;
    }
    else if (chn->sweepCounter >= chn->sweepLength)
    {
        result = 0;
    }
    else
    {
        result = (s64)chn->sweepPitch * (chn->sweepLength - chn->sweepCounter) / chn->sweepLength;

        if (step && chn->flags.autoSweep)
            chn->sweepCounter++;
    }

    return (int)result;
}

static inline int ExChannelLfoUpdate(struct SNDExChannel *chn, BOOL step)
{
    s64 result = native_host_arm7_arm_037ffe14(&chn->lfo);

    if (result != 0)
    {
        switch (chn->lfo.param.target)
        {
            case SND_LFO_VOLUME:
                result *= 60;
                break;
            case SND_LFO_PITCH:
                result *= 64;
                break;
            case SND_LFO_PAN:
                result *= 64;
                break;
        }
        result >>= 14;
    }

    if (step)
    {
        native_host_arm7_arm_037ffdb4(&chn->lfo);
    }

    return (int)result;
}
