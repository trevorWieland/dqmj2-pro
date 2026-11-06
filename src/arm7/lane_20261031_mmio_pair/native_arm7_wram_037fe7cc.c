#include "native_mmio_pair_types.h"
void native_arm7_wram_037fe7cc(
    int leftOutputFrom, int rightOutputFrom, int outputCh1ToMixer, int outputCh3ToMixer)
{
    int masterEnable = (reg_SOUNDCNT_MIX & 0x80) ? 1 : 0;
    reg_SOUNDCNT_MIX = (u8)((masterEnable << 7) | ((u32)outputCh3ToMixer << 5) |
                            ((u32)outputCh1ToMixer << 4) | ((u32)rightOutputFrom << 2) | (leftOutputFrom));
}
