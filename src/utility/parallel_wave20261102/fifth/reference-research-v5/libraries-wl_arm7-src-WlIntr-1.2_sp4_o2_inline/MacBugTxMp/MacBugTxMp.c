#include "context000.h"

void MacBugTxMp(void *arg)
{
    u32 x, i;
    u16 seqCtrl, seqCtrl2;
    x = OS_DisableIrqMask((1UL << 24) );
    seqCtrl = *(vu16 *)((0x04808000) + 0x210) ;
    *(vu16 *)((0x04808000) + 0x244) = 0x1000;
    for (i = 100; i > 0; i--) {
        seqCtrl2 = *(vu16 *)((0x04808000) + 0x210) ;
        if (seqCtrl != seqCtrl2) {
            break;
        }
    }
    *(vu16 *)((0x04808000) + 0x244) = 0x0000;
    WlIntrMpEnd(0 );
    OS_EnableIrqMask(x);
    ;
}
