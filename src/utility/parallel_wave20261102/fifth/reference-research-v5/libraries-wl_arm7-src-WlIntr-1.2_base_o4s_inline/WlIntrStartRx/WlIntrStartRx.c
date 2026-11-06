#include "context000.h"

#include "context001.h"

static void WlIntrStartRx(void) __attribute__((never_inline))
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 6) ;
    ;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation & 0x00000020 ) {
        if (pTxCtrl->BkKeyOut == 0xFFFF) {
            u32 i, tm;
            u16 *p;
            u16 curr, delt, duration, mpdu, tm_delt;
            ;
            if ((*(vu16 *)((0x04808000) + 0x19C) & ((0x0001 << 0) | (0x0001 << 1) )) != ((0x0001 << 0) | (0x0001 << 1) )) {
                goto not_suspend;
            }
            if (*(vu16 *)((0x04808000) + 0x268) < ((*(vu16 *)(0x04808000 + 0x050) / 2) & 0x0FFF)) {
                ;
                ;
                ;
                goto not_suspend;
            }
            curr = *(vu16 *)((0x04808000) + 0x054) ;
            {
                p = (u16 *)&((LPRXFRM_MAC)((0x04800000 + 0x4000) + ((u32)(curr) * 2)) )->MacHeader.Rx.MPDU;
                p = (u16 *)AdjustRingPointer(p);
                mpdu = *p;
                p += 2;
                p = (u16 *)AdjustRingPointer(p);
                if ((*p++ & 0xE7FF) == (((0x02 * 0x0004) | (0x02 * 0x0010)) | 0x0200) ) {
                    ;
                    ;
                    p = (u16 *)AdjustRingPointer(p);
                    tm = (u32) * (vu16 *)((0x04808000) + 0x0F8) - 0x10000UL;
                    while (1) {
                        delt = *(vu16 *)((0x04808000) + 0x268) - curr;
                        if (delt & 0x8000) {
                            delt += (pWork->Ofst.RxBuf.Size / 2);
                        }
                        if (delt > 6 + 1 + 1 + 3 + 3) {
                            break;
                        }
                        tm_delt = (u16)((u32) * (vu16 *)((0x04808000) + 0x0F8) - tm);
                        if (tm_delt > 16 * 4 ) {
                            goto not_suspend;
                        }
                    }
                    duration = *p;
                    p += 4;
                    for (i = 0; i < 3; i++) {
                        p = (u16 *)AdjustRingPointer(p);
                        if (*p++ != pWork->BSSID[i]) {
                            goto not_suspend;
                        }
                    }
                    p += 5;
                    p = (u16 *)AdjustRingPointer(p);
                    while (1) {
                        delt = *(vu16 *)((0x04808000) + 0x268) - curr;
                        if (delt & 0x8000) {
                            delt += (pWork->Ofst.RxBuf.Size / 2);
                        }
                        if (delt > 6 + 1 + 1 + 3 + 3 + 3 + 1 + 1 + 1) {
                            break;
                        }
                        tm_delt = (u16)((u32) * (vu16 *)((0x04808000) + 0x0F8) - tm);
                        if (tm_delt > 28 * 4 ) {
                            goto not_suspend;
                        }
                    }
                    if ((*p++ & (1UL << *(vu16 *)((0x04808000) + 0x028) )) == 0) {
                        ;
                        pTxCtrl->BkKeyOut = *(vu16 *)((0x04808000) + 0x098) ;
                        *(vu16 *)((0x04808000) + 0x0B4) = (0x0001 << 6) ;
                        pWork->NotPollTxErrCount++;
                        while (1) {
                            if ((*(vu16 *)((0x04808000) + 0x19C) & ((0x0001 << 0) | (0x0001 << 1) )) != ((0x0001 << 0) | (0x0001 << 1) )) {
                                break;
                            }
                        }
                        *(vu16 *)((0x04808000) + 0x244) |= 0x0040;
                        *(vu16 *)((0x04808000) + 0x244) &= ~0x0040;
                        *(vu16 *)((0x04808000) + 0x228) = 0x0008;
                        *(vu16 *)((0x04808000) + 0x228) = 0x0000;
                        MultiPollRevicedClearSeq();
                    }
                }
            }
not_suspend:
            ;
        }
    }
    ;
    ;
}

#include "context002.h"
