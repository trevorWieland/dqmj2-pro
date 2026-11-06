#include "native_mmio_pair_types.h"
void native_arm7_wram_037ff0fc(
    int idx, int format, void *captureData, int size, BOOL loop, int capCtrlSrc, int capCtrlDst)
{
    int off = idx * 8;

    reg_SNDCAPxCNT(idx) = (u8)(((u32)format << 3) | ((loop ? SND_CAP_LOOP : SND_CAP_ONESHOT) << 2) |
                               ((u32)capCtrlSrc << 1) | capCtrlDst);
    *(vu32 *)(0x4000510 + off) = (u32)captureData;
    *(vu16 *)(0x4000514 + off) = (u16)size;
}
