#include "native_channel_context_types.h"
void native_arm7_wram_037fead8(int chnIdx, int pan)
{
    sOrgPan[chnIdx] = (u8)pan;

    if (sMasterPan >= 0)
    {
        pan = sMasterPan;
    }

    reg_SOUNDxCNT_PAN(chnIdx) = (u8)pan;

    if (sSurroundDecay > 0 && (1 << chnIdx) & 0xFFF5)
    {
        reg_SOUNDxCNT_VOL(chnIdx) = (u8)CalcSurroundDecay(sOrgVolume[chnIdx], pan);
    }
}
