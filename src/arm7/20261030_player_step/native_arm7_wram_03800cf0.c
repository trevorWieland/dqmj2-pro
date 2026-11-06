#include "native_player_step_types.h"
static inline u16 TrackReadU16(SNDTrack *track)
{
    u32 low = native_host_arm7_arm_03800290(track);
    u32 high = native_host_arm7_arm_03800290(track);
    return low | high << 8;
}
static inline void TrackStop(SNDTrack *track, SNDPlayer *player)
{
    native_host_arm7_arm_038009e0(track, player, -1);
    native_host_arm7_arm_03800a48(track);
}
#include "native_track_play.inc"
static inline int TrackStepTicks(
    struct SNDTrack *track, struct SNDPlayer *player, int trackIdx, u32 playNotes)
{
    (void)trackIdx;
    struct SNDExChannel *chn;
    u8 cmd;
    enum SNDSeqVal valueType;
    BOOL specialValueType;
    BOOL runCmd;
    s32 length;
    int midiKey;
    s32 par;
    for (chn = track->channelLLHead; chn; chn = chn->channelLLNext)
    {
        if (chn->length > 0)
            chn->length--;
        if (!chn->flags.autoSweep && chn->sweepCounter < chn->sweepLength)
            chn->sweepCounter++;
    }
    if (track->flags.noteFinishWait)
    {
        if (track->channelLLHead)
            return 0;
        track->flags.noteFinishWait = FALSE;
    }
    if (track->wait > 0)
    {
        track->wait--;
        if (track->wait > 0)
            return 0;
    }
    native_host_arm7_arm_03800784(track->cur);
    while (track->wait == 0 && !track->flags.noteFinishWait)
    {
        specialValueType = FALSE;
        runCmd = TRUE;
        cmd = native_host_arm7_arm_03800290(track);
        if (cmd == 0xA2)
        {
            cmd = native_host_arm7_arm_03800290(track);
            runCmd = track->flags.cmp;
        }
        if (cmd == 0xA0)
        {
            cmd = native_host_arm7_arm_03800290(track);
            valueType = SND_SEQ_VAL_RAN;
            specialValueType = TRUE;
        }
        if (cmd == 0xA1)
        {
            cmd = native_host_arm7_arm_03800290(track);
            valueType = SND_SEQ_VAL_VAR;
            specialValueType = TRUE;
        }
        if ((cmd & 0x80) == 0)
        {
            u8 velocity = native_host_arm7_arm_03800290(track);
            length = native_host_arm7_arm_038007f0(track, player, specialValueType ? valueType : SND_SEQ_VAL_VLV);
            midiKey = cmd + track->transpose;
            if (!runCmd)
                continue;
            if (midiKey < 0)
                midiKey = 0;
            else if (midiKey > 127)
            {
                midiKey = 127;
            }
            if (!track->flags.muted && playNotes != 0)
            {
                TrackPlayNote(track, player, midiKey, velocity, (length > 0) ? length : -1);
            }
            track->portamentoKey = (u8)midiKey;
            if (track->flags.noteWait)
            {
                track->wait = length;
                if (length == 0)
                {
                    track->flags.noteFinishWait = TRUE;
                }
            }
            continue;
        }
        switch (cmd & 0xF0)
        {
            case 0x80:
                par =
                    native_host_arm7_arm_038007f0(track, player, specialValueType ? valueType : SND_SEQ_VAL_VLV);
                if (!runCmd)
                    break;
                switch (cmd)
                {
                    case 0x80:
                        track->wait = par;
                        break;
                    case 0x81:
                        if (par < 0x10000)
                            track->program = (u16)par;
                        break;
                }
                break;
            case 0x90:
                switch (cmd)
                {
                    case 0x93:
                    {
                        u32 off;
                        struct SNDTrack *newTrack;
                        par = native_host_arm7_arm_03800290(track);
                        off = native_host_arm7_arm_038007c0(track);
                        if (!runCmd)
                            break;
                        newTrack = native_host_arm7_arm_03800a7c(player, par);
                        if (newTrack && newTrack != track)
                        {
                            TrackStop(newTrack, player);
                            native_host_arm7_arm_038009d0(newTrack, track->base, off);
                        }
                    }
                    break;
                    case 0x94:
                    {
                        u32 off = native_host_arm7_arm_038007c0(track);
                        if (!runCmd)
                            break;
                        track->cur = &track->base[off];
                    }
                    break;
                    case 0x95:
                    {
                        u32 off = native_host_arm7_arm_038007c0(track);
                        if (!runCmd)
                            break;
                        if (track->callStackDepth < SND_TRACK_MAX_CALL)
                        {
                            track->posCallStack[track->callStackDepth] = track->cur;
                            track->callStackDepth++;
                            track->cur = &track->base[off];
                        }
                        break;
                    }
                }
                break;
            case 0xC0:
            case 0xD0:
            {
                union
                {
                    u8 _u8;
                    s8 _s8;
                } par;
                par._u8 = (u8)native_host_arm7_arm_038007f0(
                    track, player, specialValueType ? valueType : SND_SEQ_VAL_U8);
                if (!runCmd)
                    break;
                switch (cmd)
                {
                    case 0xC1:
                        track->volume = par._u8;
                        break;
                    case 0xD5:
                        track->expression = par._u8;
                        break;
                    case 0xC2:
                        player->volume = par._u8;
                        break;
                    case 0xC5:
                        track->bendRange = par._u8;
                        break;
                    case 0xC6:
                        track->priority = par._u8;
                        break;
                    case 0xC7:
                        track->flags.noteWait = par._u8;
                        break;
                    case 0xCF:
                        track->portamentoTime = par._u8;
                        break;
                    case 0xCA:
                        track->mod.depth = par._u8;
                        break;
                    case 0xCB:
                        track->mod.speed = par._u8;
                        break;
                    case 0xCC:
                        track->mod.target = par._u8;
                        break;
                    case 0xCD:
                        track->mod.range = par._u8;
                        break;
                    case 0xD0:
                        track->envAttack = par._u8;
                        break;
                    case 0xD1:
                        track->envDecay = par._u8;
                        break;
                    case 0xD2:
                        track->envSustain = par._u8;
                        break;
                    case 0xD3:
                        track->envRelease = par._u8;
                        break;
                    case 0xD4:
                        if (track->callStackDepth < SND_TRACK_MAX_CALL)
                        {
                            track->posCallStack[track->callStackDepth] = track->cur;
                            track->loopCount[track->callStackDepth] = par._u8;
                            track->callStackDepth++;
                        }
                        break;
                    case 0xC8:
                        track->flags.tie = par._u8;
                        native_host_arm7_arm_038009e0(track, player, -1);
                        native_host_arm7_arm_03800a48(track);
                        break;
                    case 0xD7:
                        native_host_arm7_arm_038018c8(track, player, par._u8);
                        break;
                    case 0xC9:
                        track->portamentoKey = (u8)(par._u8 + track->transpose);
                        track->flags.portamento = TRUE;
                        break;
                    case 0xCE:
                        track->flags.portamento = par._u8;
                        break;
                    case 0xC3:
                        track->transpose = par._s8;
                        break;
                    case 0xC4:
                        track->pitchBend = par._s8;
                        break;
                    case 0xC0:
                        track->pan = (s8)(par._u8 - 0x40);
                        break;
                    case 0xD6:
                    {
                        s16 *varPtr;
                        if (native_host_arm7_data_03807ec0)
                        {
                            varPtr = native_host_arm7_arm_03801840(player, par._u8);
                        }
                    }
                    break;
                }
            }
            break;
            case 0xE0:
            {
                s16 par = (s16)native_host_arm7_arm_038007f0(
                    track, player, specialValueType ? valueType : SND_SEQ_VAL_U16);
                if (!runCmd)
                    break;
                switch (cmd)
                {
                    case 0xE3:
                        track->sweepPitch = par;
                        break;
                    case 0xE1:
                        player->tempo = (u16)par;
                        break;
                    case 0xE0:
                        track->mod.delay = (u16)par;
                        break;
                }
            }
            break;
            case 0xB0:
            {
                int varNum = native_host_arm7_arm_03800290(track);
                s16 par = (s16)native_host_arm7_arm_038007f0(
                    track, player, specialValueType ? valueType : SND_SEQ_VAL_U16);
                s16 *varPtr = native_host_arm7_arm_03801840(player, varNum);
                if (!runCmd)
                    break;
                if (varPtr == NULL)
                    break;
                switch (cmd)
                {
                    case 0xB0:
                        *varPtr = par;
                        break;
                    case 0xB1:
                        *varPtr += par;
                        break;
                    case 0xB2:
                        *varPtr -= par;
                        break;
                    case 0xB3:
                        *varPtr *= par;
                        break;
                    case 0xB4:
                        if (par != 0)
                            *varPtr /= par;
                        break;
                    case 0xB5:
                        if (par >= 0)
                            *varPtr <<= par;
                        else
                            *varPtr >>= -par;
                        break;
                    case 0xB6:
                    {
                        BOOL neg = FALSE;
                        if (par < 0)
                        {
                            neg = TRUE;
                            par = (s16)(-par);
                        }
                        s32 random = native_host_arm7_arm_037feec4();
                        random = (random * (par + 1)) >> 16;
                        if (neg)
                            random = -random;
                        *varPtr = (s16)random;
                    }
                    break;
                    case 0xB7:
                        break;
                    case 0xB8:
                        track->flags.cmp = *varPtr == par;
                        break;
                    case 0xB9:
                        track->flags.cmp = *varPtr >= par;
                        break;
                    case 0xBA:
                        track->flags.cmp = *varPtr > par;
                        break;
                    case 0xBB:
                        track->flags.cmp = *varPtr <= par;
                        break;
                    case 0xBC:
                        track->flags.cmp = *varPtr < par;
                        break;
                    case 0xBD:
                        track->flags.cmp = *varPtr != par;
                        break;
                }
            }
            break;
            case 0xF0:
                if (!runCmd)
                    break;
                switch (cmd)
                {
                    case 0xFD:
                        if (track->callStackDepth != 0)
                        {
                            track->callStackDepth--;
                            track->cur = track->posCallStack[track->callStackDepth];
                        }
                        break;
                    case 0xFC:
                    {
                        if (track->callStackDepth == 0)
                            break;
                        u8 loopCount = track->loopCount[track->callStackDepth - 1];
                        if (loopCount != 0)
                        {
                            loopCount--;
                            if (loopCount == 0)
                            {
                                track->callStackDepth--;
                                break;
                            }
                        }
                        track->loopCount[track->callStackDepth - 1] = loopCount;
                        track->cur = track->posCallStack[track->callStackDepth - 1];
                    }
                    break;
                    case 0xFE:
                        break;
                    case 0xFF:
                        return -1;
                }
                break;
        }
    }
    return 0;
}
BOOL native_arm7_wram_03800cf0(struct SNDPlayer *player, u32 ticks)
{
    BOOL isPlaying = FALSE;
    for (int i = 0; i < SND_TRACK_COUNT_PER_PLAYER; i++)
    {
        struct SNDTrack *trk = native_host_arm7_arm_03800a7c(player, i);
        if (trk && trk->cur)
        {
            if (TrackStepTicks(trk, player, i, ticks))
                native_host_arm7_arm_03800aa8(player, i);
            else
                isPlaying = TRUE;
        }
    }
    return !isPlaying;
}
