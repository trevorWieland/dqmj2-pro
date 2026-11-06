#include "native_channel_context_types.h"
void native_arm7_wram_037febe0(int decay)
{
    native_host_arm7_data_03807980 = (u32)decay;

    for (int i = 0; i < SND_CHANNEL_COUNT; i++)
    {
        
        if ((1 << i) & 0xFFF5)
        {
            int pan = reg_SOUNDxCNT_PAN(i);
            reg_SOUNDxCNT_VOL(i) = (u8)CalcSurroundDecay(sOrgVolume[i], pan);
        }
    }
}
