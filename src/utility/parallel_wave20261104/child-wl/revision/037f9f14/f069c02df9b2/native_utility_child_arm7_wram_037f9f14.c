#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_wram_037f9f14(void) __attribute__((never_inline))
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPRX_CTRL pRxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->RxCtrl;
    LPRXFRM_MAC pMFrm;
    u32 wlOperation = ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation;
    u16 *pStatus, *pErrSts, *pNextBnry, *pTimeStamp, *pMPDU, *pDur;
    u32 bnry, curr, next_bnry, length, time[4], frameType;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 0) ;
    ;
    ;
    if (pWork->Mode == 0 ) {
        *(vu16 *)((0x04808000) + 0x05A) = *(vu16 *)((0x04808000) + 0x054) ;
    }
    for (;;) {
        bnry = pRxCtrl->wlCurr;
        curr = *(vu16 *)((0x04808000) + 0x054) ;
        if (bnry == curr) {
            break;
        }
        ;
        time[0] = *(vu16 *)((0x04808000) + 0x0F8) ;
        time[1] = *(vu16 *)((0x04808000) + 0x0FA) ;
        time[2] = *(vu16 *)((0x04808000) + 0x0F8) ;
        time[3] = *(vu16 *)((0x04808000) + 0x0FA) ;
        if (time[0] > time[2]) {
            time[0] = (time[2] >> 4) | (time[3] << 12);
        } else {
            time[0] = (time[0] >> 4) | (time[1] << 12);
        }
        ;
        if ((bnry >= (0x1000 + 0x1B0 - 36) / 2) && (bnry <= (0x1000 + 0x1DE ) / 2)) {
            native_utility_child_arm7_arm_027e9f20();
        }
        pMFrm = (LPRXFRM_MAC)((0x04800000 + 0x4000) + ((u32)(bnry) * 2)) ;
        pStatus = (u16 *)pMFrm;
        pErrSts = (u16 *)((u32)pStatus + 2);
        pErrSts = (u16 *)native_utility_child_arm7_arm_037fa9a0(pErrSts);
        pNextBnry = pErrSts;
        pTimeStamp = (u16 *)((u32)pErrSts + 2);
        pTimeStamp = (u16 *)native_utility_child_arm7_arm_037fa9a0(pTimeStamp);
        pMPDU = (u16 *)((u32)pTimeStamp + 4);
        pMPDU = (u16 *)native_utility_child_arm7_arm_037fa9a0(pMPDU);
        pDur = (u16 *)native_utility_child_arm7_arm_037fa9a0(&pMFrm->Dot11Header.DurationID);
        *pStatus |= ((*pErrSts << 1) & (0x0001 << 10) );
        *pTimeStamp = (u16)time[0];
        length = *pMPDU;
        next_bnry = ((bnry * 2 + length + 3 + 12) / 4) * 2;
        if (next_bnry >= 0x1F60 / 2) {
            next_bnry -= pWork->Ofst.RxBuf.Size / 2;
        }
        if (length > (24 + 4 + 2312 + 4 + 4) ) {
            ;
            ;
            *pStatus = 0xFFFF;
            next_bnry = curr;
            pWork->CurrErrCount++;
            ;
        }
        else if (wlOperation & 0x00000001 ) {
            if (next_bnry != curr) {
                LPRXFRM_MAC pNextMFrm;
                u16 nextStatus, nextRate;
                pNextMFrm = (LPRXFRM_MAC)((0x04800000 + 0x4000) + ((u32)(next_bnry) * 2)) ;
                nextStatus = pNextMFrm->MacHeader.Rx.Status;
                if ((u32)pNextMFrm < ((0x04800000 + 0x4000) + 0x1F60 - 6)) {
                    nextRate = LoadLow(&pNextMFrm->MacHeader.Rx.Service_Rate);
                } else {
                    nextRate = *(u16 *)((u32)pNextMFrm - (u32)pWork->Ofst.RxBuf.Size + 6);
                }
                if ((nextStatus & 0x7C00) || ((nextRate != 0x0a ) && (nextRate != 0x14 )) || (length > 0x0FFF)) {
                    ;
                    pWork->CurrErrCount++;
                    *pStatus = 0xFFFF;
                    pRxCtrl->wlCurr = curr;
                    *pNextBnry = curr;
                    break;
                }
            }
        }
        frameType = *pStatus & (0x000F) ;
        if (frameType == (0x000C << 0) ) {
            u16 fc = *(u16 *)native_utility_child_arm7_arm_037fa9a0(&pMFrm->Dot11Header.FrameCtrl.Data);
            u16 seqCtrl = *(u16 *)native_utility_child_arm7_arm_037fa9a0(&pMFrm->Dot11Header.SeqCtrl.Data);
            if ((pRxCtrl->LastMpSeq == seqCtrl) && (fc & 0x0800 )) {
                ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Counter.rx.mpDuplicateErr++;
                *pStatus = 0xFFFF;
            }
            else if ((((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.NullKeyRes == 0) && (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.STA == 0x40 )) {
                if ((*(vu16 *)((0x04808000) + 0x028) != 0) && (*(vu16 *)((0x04808000) + 0x098) & (0x0001 << 15) )) {
                    native_utility_child_arm7_arm_037fda10(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->KeyAlarm);
                    native_utility_child_arm7_arm_037fdb1c(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->KeyAlarm, ((OSTick)(((33514000 / 1000) * (u64)(*pDur)) / 64 / 1000)) , native_utility_child_arm7_arm_027ea1fc, 0 );
                } else {
                    seqCtrl = 0xFFFF;
                    *(u16 *)((0x04800000 + 0x4000) + 0x1f7e) = 0xFFFF;
                    *(u16 *)((0x04808000) + 0x24C) = 0xFFFF;
                    *(u16 *)((0x04808000) + 0x24C + 2) = 0xFFFF;
                    *pStatus = 0xFFFF;
                }
            }
            pRxCtrl->LastMpSeq = seqCtrl;
            if (native_utility_child_arm7_arm_037fa9c8() == 0) {
                ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Counter.multiPoll.txNull++;
            }
        } else if (frameType == (0x000D << 0) ) {
            if ((((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.NullKeyRes == 0) && (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.STA == 0x40 )) {
                if ((*(vu16 *)((0x04808000) + 0x028) == 0) || ((*(vu16 *)((0x04808000) + 0x098) & (0x0001 << 15) ) == 0)) {
                    *pStatus = 0xFFFF;
                }
            }
        }
        pRxCtrl->wlCurr = next_bnry;
        *pNextBnry = next_bnry;
    }
    if (wlOperation & 0x00000001 ) {
        u16 bkcurr = *(vu16 *)((0x04808000) + 0x054) ;
        u32 v = native_utility_child_arm7_arm_037fa9c8();
        if (v && (bkcurr == *(vu16 *)((0x04808000) + 0x054) )) {
            native_utility_child_arm7_arm_027e9164(0x20);
        }
    }
    if (*(vu16 *)((0x04808000) + 0x05A) != *(vu16 *)((0x04808000) + 0x054) ) {
        native_utility_child_arm7_arm_037f8558(0 , 15 );
    }
}
#include "dependency002.h"
