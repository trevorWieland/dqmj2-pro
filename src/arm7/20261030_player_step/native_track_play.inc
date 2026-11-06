static inline void TrackPlayNote(
    struct SNDTrack *track, struct SNDPlayer *player, int midiKey, int velocity, int length)
{
    struct SNDExChannel *chn = NULL;
    if (track->flags.tie)
    {
        chn = track->channelLLHead;
        if (chn)
        {
            chn->midiKey = (u8)midiKey;
            chn->velocity = (u8)velocity;
        }
    }
    if (chn == NULL)
    {
        struct SNDInstData inst;
        if (!native_host_arm7_arm_03801948(player->bank, track->program, midiKey, &inst))
            return;
        u32 allowedChannels;
        switch (inst.type)
        {
            case SND_INST_PCM:
            case SND_INST_DIRECTPCM:
                allowedChannels = 0xFFFF;
                break;
            case SND_INST_PSG:
                allowedChannels = 0x3F00;
                break;
            case SND_INST_NOISE:
                allowedChannels = 0xC000;
                break;
            default:
                return;
        }
        allowedChannels &= track->channelMask;
        chn = native_host_arm7_arm_037ff950(allowedChannels,
            player->prio + track->priority,
            track->flags.channelMask,
            native_host_arm7_arm_03800b38,
            track);
        if (chn == NULL)
            return;
        if (!native_host_arm7_arm_03801b08(
                chn, midiKey, velocity, track->flags.tie ? -1 : length, player->bank, &inst))
        {
            chn->priority = 0;
            native_host_arm7_arm_037ffb1c(chn);
            return;
        }
        chn->channelLLNext = track->channelLLHead;
        track->channelLLHead = chn;
    }
    if (track->envAttack != 0xFF)
        native_host_arm7_arm_037ff8d4(chn, track->envAttack);
    if (track->envDecay != 0xFF)
        native_host_arm7_arm_037ff8f4(chn, track->envDecay);
    if (track->envSustain != 0xFF)
        native_host_arm7_arm_037ff910(chn, track->envSustain);
    if (track->envRelease != 0xFF)
        native_host_arm7_arm_037ff918(chn, track->envRelease);
    chn->sweepPitch = track->sweepPitch;
    if (track->flags.portamento)
        chn->sweepPitch += (s16)((track->portamentoKey - midiKey) << 6);
    if (track->portamentoTime == 0)
    {
        chn->sweepLength = length;
        chn->flags.autoSweep = FALSE;
    }
    else
    {
        int swp = track->portamentoTime * track->portamentoTime;
        swp *= chn->sweepPitch < 0 ? -chn->sweepPitch : chn->sweepPitch;
        swp >>= 11;
        chn->sweepLength = swp;
    }
    chn->sweepCounter = 0;
}
