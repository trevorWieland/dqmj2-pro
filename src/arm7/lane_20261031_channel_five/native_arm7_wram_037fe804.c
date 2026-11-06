#include "native_channel_context_types.h"
void native_arm7_wram_037fe804(int chnIdx,
    const void *data,
    int format,
    int loop,
    int loopStart,
    int loopLength,
    int volume,
    int volumeDiv,
    int timer,
    int pan)
{
    int off = chnIdx * 0x10;

    sOrgPan[chnIdx] = (u8)pan;
    if (sMasterPan >= 0)
        pan = sMasterPan;

    sOrgVolume[chnIdx] = (u8)volume;
    if (sSurroundDecay > 0 && (1 << chnIdx) & 0xFFF5)
    {
        volume = CalcSurroundDecay(volume, pan);
    }

    reg_SOUNDoffCNT(off) =
        (u32)(((u32)format << 29) | ((u32)loop << 27) | ((u32)pan << 16) | ((u32)volumeDiv << 8) | (volume));
    reg_SOUNDoffTMR(off) = (u16)(0x10000u - (u32)timer);
    reg_SOUNDoffPNT(off) = (u16)loopStart;
    reg_SOUNDoffLEN(off) = (u32)loopLength;
    reg_SOUNDoffSAD(off) = (u32)data;
}
