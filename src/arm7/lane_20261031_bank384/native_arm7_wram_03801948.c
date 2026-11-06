#include "native_bank_value_types.h"
BOOL native_arm7_wram_03801948(
    const struct SNDBankData *bankData, s32 program, s32 midiKey, struct SNDInstData *instData)
{
    s32 i;
    struct SNDDrumSet *drumSet;
    struct SNDKeySplit *keySplit;
    u32 off;
    u8 minKey, maxKey;

    if (program < 0)
        return FALSE;

    SNDi_LockMutex();

    if (program >= bankData->instCount)
    {
        SNDi_UnlockMutex();
        return FALSE;
    }

    off = bankData->instOffsets[program];
    instData->type = SND_INST_OFFSET_TYPE(off);
    off >>= 8;

    switch (instData->type)
    {
        case SND_INST_PCM:
        case SND_INST_PSG:
        case SND_INST_NOISE:
        case SND_INST_DIRECTPCM:
        case SND_INST_DUMMY:
            instData->param = *SND_INST_OFFSET_NORMAL(bankData, off);
            break;
        case SND_INST_DRUM_TABLE:
            drumSet = SND_INST_OFFSET_DRUMS(bankData, off);

            
            maxKey = drumSet->maxKey;
            minKey = drumSet->minKey;

            if (midiKey < minKey || midiKey > maxKey)
            {
                SNDi_UnlockMutex();
                return FALSE;
            }

            *instData = drumSet->instruments[midiKey - drumSet->minKey];
            break;
        case SND_INST_KEY_SPLIT:
            i = 0;
            keySplit = SND_INST_OFFSET_KEYSPL(bankData, off);

            while (midiKey > keySplit->key[i])
            {
                i++;
                if (i >= SND_INST_MAX_KEYSPLIT)
                {
                    SNDi_UnlockMutex();
                    return FALSE;
                }
            }
            *instData = keySplit->instruments[i];
            break;
        case SND_INST_ILLEGAL:
        default:
            SNDi_UnlockMutex();
            return FALSE;
    }

    SNDi_UnlockMutex();
    return TRUE;
}
