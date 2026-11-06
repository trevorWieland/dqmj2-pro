#include "native_channel_context_types.h"
void native_arm7_wram_037fea48(int chnIdx, int vol, int volDiv)
{
    sOrgVolume[chnIdx] = (u8)vol;

    if (sSurroundDecay > 0 && (1 << chnIdx) & 0xFFF5)
    {
        int pan = reg_SOUNDxCNT_PAN(chnIdx);
        vol = CalcSurroundDecay(vol, pan);
    }

    reg_SOUNDxCNT_VOLS(chnIdx) = (u16)(((u32)volDiv << 8) | vol);
}
