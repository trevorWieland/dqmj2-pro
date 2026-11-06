#include "native_channel_context_types.h"
void native_arm7_wram_037fe8d0(int chnIdx, int duty, int volume, int volumeDiv, int timer, int pan)
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
        (u32)(0x60000000 | ((u32)duty << 24) | ((u32)pan << 16) | ((u32)volumeDiv << 8) | volume);
    reg_SOUNDoffTMR(off) = (u16)(0x10000u - (u32)timer);
}
